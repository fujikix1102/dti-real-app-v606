"""End-to-end catalog-level DTI transition injection/recovery pilot.

This executable is deliberately separated from the DESI production claim.  It
uses a deterministic survey-shaped synthetic object catalog and implements the
same stage boundaries that a production run must satisfy: pre-coordinate DTI
injection, fiducial coordinate conversion, FFT displacement reconstruction,
Landy-Szalay correlation estimation, anisotropic BAO template fitting, and the
published 13-observable compression layout.

When the official cosmodesi packages and a declared DESI mock catalog are
present, the resource audit records them.  This pilot never labels itself DESI
production-equivalent merely because those resources are absent or partial.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.ndimage import map_coordinates
from scipy.optimize import least_squares
from scipy.spatial import cKDTree


ROOT = Path(__file__).resolve().parent
DEFAULT_BACKEND_ROOT = Path(
    "/Users/fujikijunichi/Desktop/MAXOMEGA/_paper_journal/"
    "paper_20260305_102018_audit_sensitivity/"
    "_EXISTING_RENDER_DTI_CLASS_API_SOURCE_MATERIALIZATION_V1_20260716_102303/"
    "clones/dti-class-api"
)
OUTPUT_PATH = ROOT / "dti_catalog_pipeline_pilot.json"

LAYOUT = (
    {"name": "BGS", "z_eff": 0.295, "observable": "DV_over_rs"},
    {"name": "LRG1", "z_eff": 0.510, "observable": "DM_over_rs"},
    {"name": "LRG1", "z_eff": 0.510, "observable": "DH_over_rs"},
    {"name": "LRG2", "z_eff": 0.706, "observable": "DM_over_rs"},
    {"name": "LRG2", "z_eff": 0.706, "observable": "DH_over_rs"},
    {"name": "LRG3ELG1", "z_eff": 0.934, "observable": "DM_over_rs"},
    {"name": "LRG3ELG1", "z_eff": 0.934, "observable": "DH_over_rs"},
    {"name": "ELG2", "z_eff": 1.321, "observable": "DM_over_rs"},
    {"name": "ELG2", "z_eff": 1.321, "observable": "DH_over_rs"},
    {"name": "QSO", "z_eff": 1.484, "observable": "DM_over_rs"},
    {"name": "QSO", "z_eff": 1.484, "observable": "DH_over_rs"},
    {"name": "LYA", "z_eff": 2.330, "observable": "DH_over_rs"},
    {"name": "LYA", "z_eff": 2.330, "observable": "DM_over_rs"},
)
TRACERS = tuple(dict.fromkeys(row["name"] for row in LAYOUT))
Z_BY_TRACER = {row["name"]: float(row["z_eff"]) for row in LAYOUT}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_official_mean(data_dir: Path) -> tuple[np.ndarray, list[dict[str, Any]]]:
    path = data_dir / "OFFICIAL_DESI_DR2_MEAN.txt"
    rows: list[dict[str, Any]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        text = raw.strip()
        if not text or text.startswith("#"):
            continue
        redshift, value, observable = text.split()[:3]
        rows.append(
            {"redshift": float(redshift), "value": float(value), "observable": observable}
        )
    mean = np.asarray([row["value"] for row in rows], dtype=float)
    if mean.shape != (13,):
        raise ValueError("official DESI DR2 mean must contain 13 observables")
    expected = [(round(row["z_eff"], 3), row["observable"]) for row in LAYOUT]
    actual = [(round(row["redshift"], 3), row["observable"]) for row in rows]
    if actual != expected:
        raise ValueError(f"official 13-value ordering changed: {actual!r}")
    return mean, rows


def resource_audit() -> dict[str, Any]:
    packages = (
        "pycorr",
        "pypower",
        "pyrecon",
        "desilike",
        "mockfactory",
        "cosmoprimo",
        "fitsio",
    )
    package_status = {
        package: importlib.util.find_spec(package) is not None for package in packages
    }
    declared_mock = os.environ.get("DTI_DESI_MOCK_CATALOG", "").strip()
    mock_path = Path(declared_mock).expanduser() if declared_mock else None
    official_stack_ready = all(
        package_status[name] for name in ("pycorr", "pyrecon", "desilike", "fitsio")
    )
    return {
        "packages": package_status,
        "official_stack_ready": official_stack_ready,
        "declared_mock_catalog": str(mock_path) if mock_path else None,
        "declared_mock_catalog_exists": bool(mock_path and mock_path.is_file()),
        "production_mode_available": bool(
            official_stack_ready and mock_path and mock_path.is_file()
        ),
    }


def transition_profile(
    z: np.ndarray, amplitude: float, z_transition: float, width: float
) -> np.ndarray:
    if width <= 0.0:
        step = (z >= z_transition).astype(float)
    else:
        step = 0.5 * (1.0 + np.tanh((z - z_transition) / width))
    return float(amplitude) * step


def expansion_ratios(
    z_eval: np.ndarray,
    *,
    amplitude: float,
    z_transition: float,
    width: float,
    omega_m: float = 0.315,
) -> tuple[np.ndarray, np.ndarray]:
    z_grid = np.linspace(0.0001, max(4.3, float(np.max(z_eval)) + 0.1), 20_000)
    e_fid = np.sqrt(omega_m * (1.0 + z_grid) ** 3 + 1.0 - omega_m)
    change = transition_profile(z_grid, amplitude, z_transition, width)
    e_injected = e_fid * (1.0 + change)
    dh_ratio_grid = e_fid / e_injected
    dm_fid = cumulative_trapezoid(1.0 / e_fid, z_grid, initial=0.0)
    dm_injected = cumulative_trapezoid(1.0 / e_injected, z_grid, initial=0.0)
    dm_ratio_grid = np.ones_like(z_grid)
    valid = dm_fid > 0.0
    dm_ratio_grid[valid] = dm_injected[valid] / dm_fid[valid]
    return (
        np.interp(z_eval, z_grid, dh_ratio_grid),
        np.interp(z_eval, z_grid, dm_ratio_grid),
    )


def _inside_survey_mask(points: np.ndarray, box_size: float) -> np.ndarray:
    x, y, z = points.T
    center_x = box_size * (0.50 + 0.05 * np.sin(2.0 * np.pi * z / box_size))
    center_y = box_size * (0.50 + 0.04 * np.cos(2.0 * np.pi * z / box_size))
    elliptical = (
        ((x - center_x) / (0.42 * box_size)) ** 2
        + ((y - center_y) / (0.36 * box_size)) ** 2
        < 1.0
    )
    hole = (
        (x - 0.58 * box_size) ** 2 + (y - 0.48 * box_size) ** 2
        > (0.055 * box_size) ** 2
    )
    radial_selection = (z > 0.10 * box_size) & (z < 0.90 * box_size)
    return elliptical & hole & radial_selection


def sample_survey_points(
    rng: np.random.Generator, count: int, box_size: float
) -> np.ndarray:
    accepted: list[np.ndarray] = []
    total = 0
    while total < count:
        draw = rng.uniform(0.0, box_size, size=(max(2_000, count), 3))
        selected = draw[_inside_survey_mask(draw, box_size)]
        accepted.append(selected)
        total += len(selected)
    return np.concatenate(accepted, axis=0)[:count]


def generate_bao_catalog(
    *,
    seed: int,
    pair_count: int,
    random_count: int,
    box_size: float,
    bao_scale: float,
    damping_sigma: float,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    centers = sample_survey_points(rng, pair_count, box_size)
    directions = rng.normal(size=(pair_count, 3))
    directions /= np.linalg.norm(directions, axis=1)[:, None]
    radii = rng.normal(bao_scale, damping_sigma, size=pair_count)
    first = centers - 0.5 * radii[:, None] * directions
    second = centers + 0.5 * radii[:, None] * directions
    data = np.concatenate((first, second), axis=0)
    valid = (
        np.all((data > 0.0) & (data < box_size), axis=1)
        & _inside_survey_mask(data, box_size)
    )
    data = data[valid]
    randoms = sample_survey_points(rng, random_count, box_size)
    return data, randoms


def apply_coordinate_injection(
    points: np.ndarray,
    *,
    alpha_perpendicular: float,
    alpha_parallel: float,
    box_size: float,
) -> np.ndarray:
    transformed = np.asarray(points, dtype=float).copy()
    center = 0.5 * box_size
    transformed[:, :2] = center + alpha_perpendicular * (
        transformed[:, :2] - center
    )
    transformed[:, 2] = center + alpha_parallel * (transformed[:, 2] - center)
    return transformed


def fft_reconstruct(
    data: np.ndarray,
    randoms: np.ndarray,
    *,
    box_size: float,
    nmesh: int = 28,
    smoothing_radius: float = 15.0,
    bias: float = 2.0,
) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    edges = [np.linspace(0.0, box_size, nmesh + 1)] * 3
    data_grid = np.histogramdd(data, bins=edges)[0]
    random_grid = np.histogramdd(randoms, bins=edges)[0]
    alpha = len(data) / len(randoms)
    expected = alpha * random_grid
    delta = np.zeros_like(data_grid)
    covered = expected > 0.15
    delta[covered] = data_grid[covered] / expected[covered] - 1.0
    delta -= float(np.mean(delta[covered])) if np.any(covered) else 0.0

    cell = box_size / nmesh
    frequencies = 2.0 * np.pi * np.fft.fftfreq(nmesh, d=cell)
    kx, ky, kz = np.meshgrid(frequencies, frequencies, frequencies, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    smooth = np.exp(-0.5 * k2 * smoothing_radius**2)
    delta_k = np.fft.fftn(delta) * smooth
    safe_k2 = np.where(k2 == 0.0, np.inf, k2)
    displacement_grids = [
        np.fft.ifftn(1j * component * delta_k / (safe_k2 * bias)).real
        for component in (kx, ky, kz)
    ]

    def interpolate(points: np.ndarray) -> np.ndarray:
        coordinates = (points / cell - 0.5).T
        values = [
            map_coordinates(grid, coordinates, order=1, mode="nearest")
            for grid in displacement_grids
        ]
        return np.column_stack(values)

    data_displacement = interpolate(data)
    random_displacement = interpolate(randoms)
    shifted_data = np.clip(data - data_displacement, 1e-6, box_size - 1e-6)
    shifted_randoms = np.clip(randoms - random_displacement, 1e-6, box_size - 1e-6)
    return shifted_data, shifted_randoms, {
        "data_rms_displacement": float(
            np.sqrt(np.mean(np.sum(data_displacement**2, axis=1)))
        ),
        "random_rms_displacement": float(
            np.sqrt(np.mean(np.sum(random_displacement**2, axis=1)))
        ),
        "nmesh": nmesh,
        "smoothing_radius": smoothing_radius,
    }


def _pair_histogram(
    first: np.ndarray,
    second: np.ndarray,
    separation_edges: np.ndarray,
    mu_edges: np.ndarray,
    *,
    autocorrelation: bool,
) -> np.ndarray:
    first_tree = cKDTree(first)
    if autocorrelation:
        indices = first_tree.query_pairs(
            float(separation_edges[-1]), output_type="ndarray"
        )
        differences = first[indices[:, 0]] - first[indices[:, 1]]
    else:
        pairs = first_tree.sparse_distance_matrix(
            cKDTree(second), float(separation_edges[-1]), output_type="ndarray"
        )
        differences = first[pairs["i"]] - second[pairs["j"]]
    separation = np.linalg.norm(differences, axis=1)
    mu = np.abs(differences[:, 2]) / np.maximum(separation, 1e-12)
    return np.histogram2d(
        separation, mu, bins=(separation_edges, mu_edges)
    )[0]


def landy_szalay(
    data: np.ndarray,
    randoms: np.ndarray,
    separation_edges: np.ndarray,
    mu_edges: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    dd = _pair_histogram(
        data, data, separation_edges, mu_edges, autocorrelation=True
    )
    rr = _pair_histogram(
        randoms, randoms, separation_edges, mu_edges, autocorrelation=True
    )
    dr = _pair_histogram(
        data, randoms, separation_edges, mu_edges, autocorrelation=False
    )
    dd /= len(data) * (len(data) - 1) / 2.0
    rr_normalization = len(randoms) * (len(randoms) - 1) / 2.0
    rr /= rr_normalization
    dr /= len(data) * len(randoms)
    xi = (dd - 2.0 * dr + rr) / np.maximum(rr, 1e-15)
    return xi, rr * rr_normalization


def fit_anisotropic_bao(
    xi: np.ndarray,
    rr_counts: np.ndarray,
    separation_edges: np.ndarray,
    mu_edges: np.ndarray,
    *,
    bao_scale: float,
) -> dict[str, Any]:
    separation = 0.5 * (separation_edges[:-1] + separation_edges[1:])
    mu = 0.5 * (mu_edges[:-1] + mu_edges[1:])
    separation_grid, mu_grid = np.meshgrid(separation, mu, indexing="ij")
    s = separation_grid.ravel()
    m = mu_grid.ravel()
    observed = xi.ravel()
    weight = np.minimum(np.sqrt(np.maximum(rr_counts.ravel(), 1.0)), 30.0)
    mu_bin = np.minimum((m * len(mu)).astype(int), len(mu) - 1)

    def residual(parameters: np.ndarray) -> np.ndarray:
        alpha_perpendicular, alpha_parallel, sigma = parameters[:3]
        offset = 3
        amplitude = parameters[offset : offset + len(mu)]
        offset += len(mu)
        broadband_0 = parameters[offset : offset + len(mu)]
        offset += len(mu)
        broadband_1 = parameters[offset : offset + len(mu)]
        dilation = np.sqrt(
            alpha_perpendicular**2 * (1.0 - m**2) + alpha_parallel**2 * m**2
        )
        peak = bao_scale * dilation
        model = (
            amplitude[mu_bin] * np.exp(-0.5 * ((s - peak) / sigma) ** 2)
            + broadband_0[mu_bin]
            + broadband_1[mu_bin] * (s - bao_scale) / 30.0
        )
        return (model - observed) * weight

    mu_count = len(mu)
    initial = np.concatenate(
        ([1.0, 1.0, 7.0], np.full(mu_count, 0.1), np.zeros(2 * mu_count))
    )
    lower = np.concatenate(
        ([0.70, 0.70, 2.0], np.zeros(mu_count), np.full(2 * mu_count, -2.0))
    )
    upper = np.concatenate(
        ([1.30, 1.30, 22.0], np.full(mu_count, 3.0), np.full(2 * mu_count, 2.0))
    )
    fit = least_squares(
        residual,
        initial,
        bounds=(lower, upper),
        max_nfev=4_000,
        xtol=1e-9,
        ftol=1e-9,
    )
    return {
        "alpha_perpendicular_raw": float(fit.x[0]),
        "alpha_parallel_raw": float(fit.x[1]),
        "sigma_peak": float(fit.x[2]),
        "success": bool(fit.success),
        "cost": float(fit.cost),
        "evaluations": int(fit.nfev),
    }


def _compressed_vector(
    official_mean: np.ndarray,
    alpha_by_tracer: dict[str, tuple[float, float]],
) -> np.ndarray:
    output: list[float] = []
    for baseline, row in zip(official_mean, LAYOUT, strict=True):
        alpha_perpendicular, alpha_parallel = alpha_by_tracer[row["name"]]
        if row["observable"] == "DM_over_rs":
            dilation = alpha_perpendicular
        elif row["observable"] == "DH_over_rs":
            dilation = alpha_parallel
        elif row["observable"] == "DV_over_rs":
            dilation = (alpha_perpendicular**2 * alpha_parallel) ** (1.0 / 3.0)
        else:
            raise ValueError(f"unsupported observable: {row['observable']}")
        output.append(float(baseline * dilation))
    return np.asarray(output)


def run(
    *,
    data_dir: Path,
    replicates: int,
    pair_count: int,
    random_count: int,
    seed: int,
    amplitude: float,
    z_transition: float,
    width: float,
    output_path: Path = OUTPUT_PATH,
) -> dict[str, Any]:
    if replicates < 2:
        raise ValueError("at least two catalog replicates are required")
    official_mean, metadata = load_official_mean(data_dir)
    audit = resource_audit()
    if audit["production_mode_available"]:
        execution_class = "catalog_level_pilot_official_resources_detected_not_invoked"
    else:
        execution_class = "catalog_level_synthetic_end_to_end_pilot"

    box_size = 800.0
    bao_scale = 105.0
    separation_edges = np.linspace(75.0, 135.0, 31)
    mu_edges = np.linspace(0.0, 1.0, 6)
    z_values = np.asarray([Z_BY_TRACER[name] for name in TRACERS])
    target_parallel, target_perpendicular = expansion_ratios(
        z_values,
        amplitude=amplitude,
        z_transition=z_transition,
        width=width,
    )

    tracer_rows: list[dict[str, Any]] = []
    recovered_post: dict[str, tuple[float, float]] = {}
    target_by_tracer: dict[str, tuple[float, float]] = {}
    total_catalogs = 0
    total_data_objects = 0
    total_random_objects = 0

    for tracer_index, tracer in enumerate(TRACERS):
        target_ap = float(target_perpendicular[tracer_index])
        target_al = float(target_parallel[tracer_index])
        target_by_tracer[tracer] = (target_ap, target_al)
        correlations: dict[str, list[np.ndarray]] = {
            "baseline_pre": [],
            "injected_pre": [],
            "baseline_post": [],
            "injected_post": [],
        }
        rr_counts: dict[str, list[np.ndarray]] = {key: [] for key in correlations}
        reconstruction_rows: list[dict[str, float]] = []

        for replicate in range(replicates):
            catalog_seed = seed + 10_000 * tracer_index + replicate
            baseline_data, baseline_randoms = generate_bao_catalog(
                seed=catalog_seed,
                pair_count=pair_count,
                random_count=random_count,
                box_size=box_size,
                bao_scale=bao_scale,
                damping_sigma=8.5,
            )
            injected_data = apply_coordinate_injection(
                baseline_data,
                alpha_perpendicular=target_ap,
                alpha_parallel=target_al,
                box_size=box_size,
            )
            valid = (
                np.all((injected_data > 0.0) & (injected_data < box_size), axis=1)
                & _inside_survey_mask(injected_data, box_size)
            )
            injected_data = injected_data[valid]

            for key, data in (
                ("baseline_pre", baseline_data),
                ("injected_pre", injected_data),
            ):
                xi, rr = landy_szalay(
                    data, baseline_randoms, separation_edges, mu_edges
                )
                correlations[key].append(xi)
                rr_counts[key].append(rr)

            baseline_post, baseline_shifted_randoms, baseline_reconstruction = (
                fft_reconstruct(
                    baseline_data,
                    baseline_randoms,
                    box_size=box_size,
                )
            )
            injected_post, injected_shifted_randoms, injected_reconstruction = (
                fft_reconstruct(
                    injected_data,
                    baseline_randoms,
                    box_size=box_size,
                )
            )
            reconstruction_rows.append(
                {
                    "baseline_data_rms": baseline_reconstruction[
                        "data_rms_displacement"
                    ],
                    "injected_data_rms": injected_reconstruction[
                        "data_rms_displacement"
                    ],
                }
            )
            for key, data, randoms in (
                ("baseline_post", baseline_post, baseline_shifted_randoms),
                ("injected_post", injected_post, injected_shifted_randoms),
            ):
                xi, rr = landy_szalay(data, randoms, separation_edges, mu_edges)
                correlations[key].append(xi)
                rr_counts[key].append(rr)

            total_catalogs += 2
            total_data_objects += len(baseline_data) + len(injected_data)
            total_random_objects += 2 * len(baseline_randoms)

        fits: dict[str, dict[str, Any]] = {}
        for key in correlations:
            fits[key] = fit_anisotropic_bao(
                np.mean(correlations[key], axis=0),
                np.sum(rr_counts[key], axis=0),
                separation_edges,
                mu_edges,
                bao_scale=bao_scale,
            )
            if not fits[key]["success"]:
                raise RuntimeError(f"BAO fit failed for {tracer} {key}")

        recovered_pre_ap = (
            fits["injected_pre"]["alpha_perpendicular_raw"]
            / fits["baseline_pre"]["alpha_perpendicular_raw"]
        )
        recovered_pre_al = (
            fits["injected_pre"]["alpha_parallel_raw"]
            / fits["baseline_pre"]["alpha_parallel_raw"]
        )
        recovered_post_ap = (
            fits["injected_post"]["alpha_perpendicular_raw"]
            / fits["baseline_post"]["alpha_perpendicular_raw"]
        )
        recovered_post_al = (
            fits["injected_post"]["alpha_parallel_raw"]
            / fits["baseline_post"]["alpha_parallel_raw"]
        )
        recovered_post[tracer] = (recovered_post_ap, recovered_post_al)
        tracer_rows.append(
            {
                "tracer": tracer,
                "z_eff": Z_BY_TRACER[tracer],
                "target_alpha_perpendicular": target_ap,
                "target_alpha_parallel": target_al,
                "recovered_pre_alpha_perpendicular": recovered_pre_ap,
                "recovered_pre_alpha_parallel": recovered_pre_al,
                "recovered_post_alpha_perpendicular": recovered_post_ap,
                "recovered_post_alpha_parallel": recovered_post_al,
                "post_error_alpha_perpendicular": recovered_post_ap - target_ap,
                "post_error_alpha_parallel": recovered_post_al - target_al,
                "baseline_pre_sigma_peak": fits["baseline_pre"]["sigma_peak"],
                "baseline_post_sigma_peak": fits["baseline_post"]["sigma_peak"],
                "mean_reconstruction_rms": float(
                    np.mean(
                        [row["baseline_data_rms"] for row in reconstruction_rows]
                    )
                ),
                "fits": fits,
            }
        )
        print(
            "CATALOG_PIPELINE "
            f"tracer={tracer} z={Z_BY_TRACER[tracer]:.3f} "
            f"target=({target_ap:.5f},{target_al:.5f}) "
            f"recovered=({recovered_post_ap:.5f},{recovered_post_al:.5f})",
            flush=True,
        )

    target_vector = _compressed_vector(official_mean, target_by_tracer)
    recovered_vector = _compressed_vector(official_mean, recovered_post)
    relative_error = (recovered_vector - target_vector) / target_vector
    alpha_errors = np.asarray(
        [
            value
            for row in tracer_rows
            for value in (
                row["post_error_alpha_perpendicular"],
                row["post_error_alpha_parallel"],
            )
        ]
    )
    result = {
        "schema_version": "dti-catalog-pipeline-pilot-v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "complete",
        "execution_class": execution_class,
        "production_equivalent": False,
        "official_resource_audit": audit,
        "injection": {
            "model": "permanent_tanh_step_in_H_of_z",
            "fractional_H_step": amplitude,
            "z_transition": z_transition,
            "width": width,
        },
        "configuration": {
            "replicates_per_tracer": replicates,
            "bao_pairs_per_catalog": pair_count,
            "random_objects_per_catalog": random_count,
            "seed": seed,
            "box_size_Mpc_over_h": box_size,
            "bao_scale_Mpc_over_h": bao_scale,
            "separation_bins": (len(separation_edges) - 1),
            "mu_bins": (len(mu_edges) - 1),
        },
        "executed_pipeline": [
            "survey-shaped synthetic object catalog generation",
            "known H(z) transition injection before fiducial coordinate conversion",
            "anisotropic transverse/radial coordinate dilation",
            "FFT-smoothed displacement-field reconstruction",
            "Landy-Szalay xi(s,mu) correlation estimation",
            "anisotropic shifted-BAO template fit with per-mu broadband nuisance",
            "published DESI DR2 13-observable ordering and compression",
        ],
        "execution_counts": {
            "paired_catalogs": total_catalogs,
            "data_objects_processed": total_data_objects,
            "random_objects_processed": total_random_objects,
            "correlation_functions": 4 * replicates * len(TRACERS),
            "bao_template_fits": 4 * len(TRACERS),
            "compressed_values": 13,
        },
        "tracers": tracer_rows,
        "compression": {
            "metadata": metadata,
            "official_baseline": official_mean.tolist(),
            "target_injected_vector": target_vector.tolist(),
            "recovered_post_reconstruction_vector": recovered_vector.tolist(),
            "relative_error": relative_error.tolist(),
            "relative_rmse": float(np.sqrt(np.mean(relative_error**2))),
            "maximum_absolute_relative_error": float(np.max(np.abs(relative_error))),
        },
        "recovery_summary": {
            "alpha_rmse": float(np.sqrt(np.mean(alpha_errors**2))),
            "alpha_maximum_absolute_error": float(np.max(np.abs(alpha_errors))),
            "pipeline_completed": True,
            "transition_recovery_scientifically_calibrated": False,
        },
        "input_identity": {
            "mean_path": str(data_dir / "OFFICIAL_DESI_DR2_MEAN.txt"),
            "mean_sha256": sha256(data_dir / "OFFICIAL_DESI_DR2_MEAN.txt"),
        },
        "claim_boundary": (
            "This is an executed catalog-level end-to-end pilot with real coordinate conversion, "
            "FFT reconstruction, pair counting, correlation estimation, template fitting, and "
            "13-value compression. Its object catalog and mask are deterministic synthetic controls, "
            "not an official DESI EZmock/Abacus/DR2 production catalog. It calibrates implementation "
            "and information transfer only; it is not an observational DTI detection or exclusion."
        ),
        "next_production_replacement_contract": [
            "replace synthetic catalog loader with declared official DESI mock FITS catalog",
            "replace internal FFT reconstruction with official pyrecon configuration",
            "replace internal pair counter with official pycorr configuration",
            "replace Gaussian BAO shell template with official desilike BAO model",
            "run null and injected ensembles with declared survey covariance and global calibration",
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_BACKEND_ROOT / "app" / "data" / "desi_dr2_bao",
    )
    parser.add_argument("--replicates", type=int, default=8)
    parser.add_argument("--pair-count", type=int, default=1_800)
    parser.add_argument("--random-count", type=int, default=6_500)
    parser.add_argument("--seed", type=int, default=20260719)
    parser.add_argument("--amplitude", type=float, default=0.10)
    parser.add_argument("--z-transition", type=float, default=0.934)
    parser.add_argument("--width", type=float, default=0.03)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    arguments = parser.parse_args()
    result = run(
        data_dir=arguments.data_dir,
        replicates=arguments.replicates,
        pair_count=arguments.pair_count,
        random_count=arguments.random_count,
        seed=arguments.seed,
        amplitude=arguments.amplitude,
        z_transition=arguments.z_transition,
        width=arguments.width,
        output_path=arguments.output,
    )
    print("DTI_CATALOG_PIPELINE_PILOT=PASS")
    print("OUTPUT=" + str(arguments.output))
    print("ALPHA_RMSE=" + f"{result['recovery_summary']['alpha_rmse']:.8f}")
    print("PRODUCTION_EQUIVALENT=NO")

