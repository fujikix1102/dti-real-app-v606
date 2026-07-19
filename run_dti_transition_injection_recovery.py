"""DTI transition injection/recovery transfer audit for DESI-like BAO compression.

This is an independent correlation-function surrogate, not the DESI production
pipeline.  It injects a transition into H(z), propagates it to D_H and D_M,
maps it to fiducial-coordinate BAO dilations, averages over broad tracer
redshift windows, fits a single shifted BAO template with broadband nuisance
terms, compresses to the published 13-value layout, and measures recovery
against the published covariance after profiling smooth H(z) responses.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.linalg import solve_triangular


ROOT = Path(__file__).resolve().parent
DEFAULT_BACKEND_ROOT = Path(
    "/Users/fujikijunichi/Desktop/MAXOMEGA/_paper_journal/"
    "paper_20260305_102018_audit_sensitivity/"
    "_EXISTING_RENDER_DTI_CLASS_API_SOURCE_MATERIALIZATION_V1_20260716_102303/"
    "clones/dti-class-api"
)
OUTPUT_PATH = ROOT / "dti_transition_injection_recovery.json"
SUMMARY_PATH = ROOT / "dti_transition_injection_recovery_summary.csv"


# Redshift-window proxy matching the published tracer layout and effective z.
# Exact selection functions are not public in the current workspace.
TRACERS = (
    {"name": "BGS", "z_eff": 0.295, "z_min": 0.10, "z_max": 0.40},
    {"name": "LRG1", "z_eff": 0.510, "z_min": 0.40, "z_max": 0.60},
    {"name": "LRG2", "z_eff": 0.706, "z_min": 0.60, "z_max": 0.80},
    {"name": "LRG3ELG1", "z_eff": 0.934, "z_min": 0.80, "z_max": 1.10},
    {"name": "ELG2", "z_eff": 1.321, "z_min": 1.10, "z_max": 1.60},
    {"name": "QSO", "z_eff": 1.484, "z_min": 0.80, "z_max": 2.10},
    {"name": "LYA", "z_eff": 2.330, "z_min": 1.77, "z_max": 4.20},
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_bao_contract(data_dir: Path) -> tuple[np.ndarray, np.ndarray, list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    mean_path = data_dir / "OFFICIAL_DESI_DR2_MEAN.txt"
    covariance_path = data_dir / "OFFICIAL_DESI_DR2_COVARIANCE.txt"
    for raw in mean_path.read_text(encoding="utf-8").splitlines():
        text = raw.strip()
        if not text or text.startswith("#"):
            continue
        redshift, value, observable = text.split()[:3]
        rows.append({"redshift": float(redshift), "value": float(value), "observable": observable})
    mean = np.asarray([row["value"] for row in rows], dtype=float)
    covariance = np.loadtxt(covariance_path, dtype=float)
    if mean.shape != (13,) or covariance.shape != (13, 13):
        raise ValueError("DESI DR2 compressed contract must be 13 values and a 13x13 covariance")
    np.linalg.cholesky(covariance)
    return mean, covariance, rows


def transition_profile(z: np.ndarray, amplitude: float, z_transition: float, width: float) -> np.ndarray:
    if width <= 0:
        step = (z >= z_transition).astype(float)
    else:
        step = 0.5 * (1.0 + np.tanh((z - z_transition) / width))
    return float(amplitude) * step


def expansion_ratios(z: np.ndarray, fractional_h_change: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return D_H/D_H_fid and D_M/D_M_fid for a flat LCDM reference."""
    omega_m = 0.315
    e_fid = np.sqrt(omega_m * (1.0 + z) ** 3 + 1.0 - omega_m)
    if np.any(1.0 + fractional_h_change <= 0.0):
        raise ValueError("injected H(z) must remain positive")
    e_true = e_fid * (1.0 + fractional_h_change)
    dh_ratio = e_fid / e_true
    dm_fid = cumulative_trapezoid(1.0 / e_fid, z, initial=0.0)
    dm_true = cumulative_trapezoid(1.0 / e_true, z, initial=0.0)
    dm_ratio = np.ones_like(z)
    valid = dm_fid > 0.0
    dm_ratio[valid] = dm_true[valid] / dm_fid[valid]
    return dh_ratio, dm_ratio


def tracer_weight(z: np.ndarray, tracer: dict[str, float | str]) -> np.ndarray:
    left = float(tracer["z_min"])
    center = float(tracer["z_eff"])
    right = float(tracer["z_max"])
    weight = np.zeros_like(z)
    left_mask = (z >= left) & (z <= center)
    right_mask = (z > center) & (z <= right)
    weight[left_mask] = (z[left_mask] - left) / max(center - left, 1e-12)
    weight[right_mask] = (right - z[right_mask]) / max(right - center, 1e-12)
    total = np.trapezoid(weight, z)
    if total <= 0.0:
        raise ValueError(f"empty tracer window: {tracer['name']}")
    return weight / total


class BaoPeakFitter:
    """Single-peak BAO template fit with linear broadband marginalization."""

    def __init__(self, sigma_peak: float) -> None:
        self.s = np.linspace(70.0, 140.0, 141)
        self.r_bao = 105.0
        self.alpha_grid = np.linspace(0.86, 1.14, 561)
        broadband = np.column_stack([np.ones_like(self.s), 1.0 / self.s, 1.0 / self.s**2])
        q, _ = np.linalg.qr(broadband, mode="reduced")
        self.q_broadband = q
        peaks = np.exp(
            -0.5 * ((self.s[None, :] - self.r_bao * self.alpha_grid[:, None]) / sigma_peak) ** 2
        )
        peaks -= (peaks @ q) @ q.T
        norms = np.linalg.norm(peaks, axis=1)
        self.normalized_templates = peaks / norms[:, None]
        self.sigma_peak = float(sigma_peak)

    def fit(self, z: np.ndarray, alpha_of_z: np.ndarray, weight: np.ndarray) -> float:
        selected = weight > 0.0
        local_z = z[selected]
        local_alpha = alpha_of_z[selected]
        local_weight = weight[selected]
        peak_stack = np.exp(
            -0.5
            * ((self.s[None, :] - self.r_bao * local_alpha[:, None]) / self.sigma_peak) ** 2
        )
        data = np.trapezoid(local_weight[:, None] * peak_stack, local_z, axis=0)
        data -= self.q_broadband @ (self.q_broadband.T @ data)
        scores = (self.normalized_templates @ data) ** 2
        return float(self.alpha_grid[int(np.argmax(scores))])


def _fitted_alphas(
    z: np.ndarray,
    dh_ratio: np.ndarray,
    dm_ratio: np.ndarray,
    fitter: BaoPeakFitter,
) -> dict[float, tuple[float, float]]:
    output: dict[float, tuple[float, float]] = {}
    for tracer in TRACERS:
        weight = tracer_weight(z, tracer)
        alpha_parallel = fitter.fit(z, dh_ratio, weight)
        alpha_perpendicular = fitter.fit(z, dm_ratio, weight)
        output[float(tracer["z_eff"])] = (alpha_parallel, alpha_perpendicular)
    return output


def compressed_vector(
    *,
    z: np.ndarray,
    fractional_h_change: np.ndarray,
    mean: np.ndarray,
    metadata: list[dict[str, Any]],
    fitter: BaoPeakFitter,
    baseline_alphas: dict[float, tuple[float, float]],
) -> np.ndarray:
    dh_ratio, dm_ratio = expansion_ratios(z, fractional_h_change)
    fitted = _fitted_alphas(z, dh_ratio, dm_ratio, fitter)
    values: list[float] = []
    for index, row in enumerate(metadata):
        redshift = float(row["redshift"])
        alpha_parallel, alpha_perpendicular = fitted[redshift]
        base_parallel, base_perpendicular = baseline_alphas[redshift]
        alpha_parallel /= base_parallel
        alpha_perpendicular /= base_perpendicular
        observable = row["observable"]
        if observable == "DH_over_rs":
            alpha = alpha_parallel
        elif observable == "DM_over_rs":
            alpha = alpha_perpendicular
        elif observable == "DV_over_rs":
            alpha = (alpha_perpendicular**2 * alpha_parallel) ** (1.0 / 3.0)
        else:
            raise ValueError(f"unsupported observable: {observable}")
        values.append(float(mean[index] * alpha))
    return np.asarray(values)


def point_sample_vector(
    *,
    z: np.ndarray,
    fractional_h_change: np.ndarray,
    mean: np.ndarray,
    metadata: list[dict[str, Any]],
) -> np.ndarray:
    dh_ratio, dm_ratio = expansion_ratios(z, fractional_h_change)
    values: list[float] = []
    for index, row in enumerate(metadata):
        redshift = float(row["redshift"])
        alpha_parallel = float(np.interp(redshift, z, dh_ratio))
        alpha_perpendicular = float(np.interp(redshift, z, dm_ratio))
        observable = row["observable"]
        if observable == "DH_over_rs":
            alpha = alpha_parallel
        elif observable == "DM_over_rs":
            alpha = alpha_perpendicular
        else:
            alpha = (alpha_perpendicular**2 * alpha_parallel) ** (1.0 / 3.0)
        values.append(float(mean[index] * alpha))
    return np.asarray(values)


def residual_projection(covariance: np.ndarray, smooth_design: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    cholesky = np.linalg.cholesky(covariance)
    whitened_design = solve_triangular(cholesky, smooth_design, lower=True)
    q, _ = np.linalg.qr(whitened_design, mode="reduced")
    projector = np.eye(covariance.shape[0]) - q @ q.T
    return cholesky, projector


def _residualized_whitened(
    vector: np.ndarray, cholesky: np.ndarray, projector: np.ndarray
) -> np.ndarray:
    return projector @ solve_triangular(cholesky, vector, lower=True)


def build_smooth_design(
    *,
    z: np.ndarray,
    mean: np.ndarray,
    metadata: list[dict[str, Any]],
    fitter: BaoPeakFitter,
    baseline_alphas: dict[float, tuple[float, float]],
    baseline_vector: np.ndarray,
) -> np.ndarray:
    scaled = (z - 1.2) / 1.2
    epsilon = 0.002
    columns: list[np.ndarray] = []
    for profile in (np.ones_like(z), scaled, scaled**2):
        vector = compressed_vector(
            z=z,
            fractional_h_change=epsilon * profile,
            mean=mean,
            metadata=metadata,
            fitter=fitter,
            baseline_alphas=baseline_alphas,
        )
        columns.append((vector - baseline_vector) / epsilon)
    return np.column_stack(columns)


def run(
    *,
    data_dir: Path,
    null_replicates: int,
    scenario_replicates: int,
    seed: int,
    output_path: Path = OUTPUT_PATH,
    summary_path: Path = SUMMARY_PATH,
) -> dict[str, Any]:
    mean, covariance, metadata = load_bao_contract(data_dir)
    z = np.linspace(0.0005, 4.30, 6000)
    zero = np.zeros_like(z)
    post_fitter = BaoPeakFitter(sigma_peak=8.0)
    pre_fitter = BaoPeakFitter(sigma_peak=15.0)
    unit_dh, unit_dm = expansion_ratios(z, zero)
    post_baseline_alphas = _fitted_alphas(z, unit_dh, unit_dm, post_fitter)
    pre_baseline_alphas = _fitted_alphas(z, unit_dh, unit_dm, pre_fitter)
    post_baseline = compressed_vector(
        z=z,
        fractional_h_change=zero,
        mean=mean,
        metadata=metadata,
        fitter=post_fitter,
        baseline_alphas=post_baseline_alphas,
    )
    pre_baseline = compressed_vector(
        z=z,
        fractional_h_change=zero,
        mean=mean,
        metadata=metadata,
        fitter=pre_fitter,
        baseline_alphas=pre_baseline_alphas,
    )
    if np.max(np.abs(post_baseline - mean)) > 1e-12:
        raise RuntimeError("baseline compression is not identity")

    smooth_design = build_smooth_design(
        z=z,
        mean=mean,
        metadata=metadata,
        fitter=post_fitter,
        baseline_alphas=post_baseline_alphas,
        baseline_vector=post_baseline,
    )
    cholesky, projector = residual_projection(covariance, smooth_design)

    candidate_z = np.round(np.arange(0.20, 2.401, 0.05), 3)
    candidate_widths = (0.005, 0.03, 0.15)
    reference_amplitude = 0.01
    bank_rows: list[dict[str, float]] = []
    bank_vectors: list[np.ndarray] = []
    bank_norms: list[float] = []
    for z_transition in candidate_z:
        for width in candidate_widths:
            profile = transition_profile(z, reference_amplitude, float(z_transition), width)
            vector = compressed_vector(
                z=z,
                fractional_h_change=profile,
                mean=mean,
                metadata=metadata,
                fitter=post_fitter,
                baseline_alphas=post_baseline_alphas,
            )
            template = (vector - post_baseline) / reference_amplitude
            residualized = _residualized_whitened(template, cholesky, projector)
            norm = float(np.linalg.norm(residualized))
            if norm <= 1e-12:
                continue
            bank_rows.append({"z_transition": float(z_transition), "width": float(width)})
            bank_vectors.append(residualized / norm)
            bank_norms.append(norm)
    bank = np.asarray(bank_vectors)
    bank_norms_array = np.asarray(bank_norms)

    rng = np.random.default_rng(seed)
    null_noise = rng.standard_normal((null_replicates, 13))
    null_residual = null_noise @ projector.T
    null_statistic = np.max((null_residual @ bank.T) ** 2, axis=1)
    thresholds = {
        "global_95_percent": float(np.quantile(null_statistic, 0.95)),
        "global_99_percent": float(np.quantile(null_statistic, 0.99)),
        "global_3sigma_99.73_percent": float(np.quantile(null_statistic, 0.9973)),
    }
    detection_threshold = thresholds["global_3sigma_99.73_percent"]

    scenario_z = (0.51, 0.934, 1.321, 1.484)
    scenario_widths = (0.005, 0.03, 0.15)
    # Extend beyond the physically interesting percent-level regime so the
    # experiment measures a recovery threshold instead of merely reporting
    # a sequence of non-detections.
    scenario_amplitudes = (0.005, 0.01, 0.02, 0.05, 0.10, 0.20)
    scenario_rows: list[dict[str, Any]] = []
    for z_transition in scenario_z:
        for width in scenario_widths:
            for amplitude in scenario_amplitudes:
                profile = transition_profile(z, amplitude, z_transition, width)
                post_vector = compressed_vector(
                    z=z,
                    fractional_h_change=profile,
                    mean=mean,
                    metadata=metadata,
                    fitter=post_fitter,
                    baseline_alphas=post_baseline_alphas,
                )
                pre_vector = compressed_vector(
                    z=z,
                    fractional_h_change=profile,
                    mean=mean,
                    metadata=metadata,
                    fitter=pre_fitter,
                    baseline_alphas=pre_baseline_alphas,
                )
                point_vector = point_sample_vector(
                    z=z,
                    fractional_h_change=profile,
                    mean=mean,
                    metadata=metadata,
                )
                post_signal = _residualized_whitened(post_vector - post_baseline, cholesky, projector)
                pre_signal = _residualized_whitened(pre_vector - pre_baseline, cholesky, projector)
                point_signal = _residualized_whitened(point_vector - mean, cholesky, projector)
                point_norm = float(np.linalg.norm(point_signal))
                post_norm = float(np.linalg.norm(post_signal))
                pre_norm = float(np.linalg.norm(pre_signal))

                noise = rng.standard_normal((scenario_replicates, 13))
                residualized_data = noise @ projector.T + post_signal[None, :]
                scores = (residualized_data @ bank.T) ** 2
                best_indices = np.argmax(scores, axis=1)
                best_scores = scores[np.arange(scenario_replicates), best_indices]
                detected = best_scores >= detection_threshold
                recovered_z = np.asarray([bank_rows[int(index)]["z_transition"] for index in best_indices])
                recovered_width = np.asarray([bank_rows[int(index)]["width"] for index in best_indices])
                signed_projection = np.sum(
                    residualized_data * bank[best_indices], axis=1
                )
                recovered_amplitude = signed_projection / bank_norms_array[best_indices]
                location_tolerance = max(0.10, 2.0 * width)
                located = np.abs(recovered_z - z_transition) <= location_tolerance
                detected_count = int(np.count_nonzero(detected))
                scenario_rows.append({
                    "z_transition": z_transition,
                    "width": width,
                    "fractional_H_step": amplitude,
                    "replicates": scenario_replicates,
                    "compressed_post_signal_snr": post_norm,
                    "compressed_pre_signal_snr": pre_norm,
                    "point_sample_signal_snr": point_norm,
                    "compression_attenuation": post_norm / point_norm if point_norm > 0 else None,
                    "post_to_pre_snr_ratio": post_norm / pre_norm if pre_norm > 0 else None,
                    "global_3sigma_detection_fraction": detected_count / scenario_replicates,
                    "detected_and_located_fraction": float(np.mean(detected & located)),
                    "location_success_given_detection": (
                        float(np.mean(located[detected])) if detected_count else None
                    ),
                    "median_recovered_z": float(np.median(recovered_z[detected])) if detected_count else None,
                    "median_recovered_width": (
                        float(np.median(recovered_width[detected])) if detected_count else None
                    ),
                    "median_recovered_fractional_H_step": (
                        float(np.median(recovered_amplitude[detected])) if detected_count else None
                    ),
                })
                print(
                    "INJECTION_RECOVERY "
                    f"z={z_transition:.3f} width={width:.3f} amplitude={amplitude:.3f} "
                    f"detection={detected_count / scenario_replicates:.3f}",
                    flush=True,
                )

    robust_by_amplitude: list[dict[str, float]] = []
    for amplitude in scenario_amplitudes:
        selected = [row for row in scenario_rows if row["fractional_H_step"] == amplitude]
        fractions = np.asarray([row["global_3sigma_detection_fraction"] for row in selected])
        robust_by_amplitude.append({
            "fractional_H_step": amplitude,
            "minimum_detection_fraction": float(np.min(fractions)),
            "median_detection_fraction": float(np.median(fractions)),
            "maximum_detection_fraction": float(np.max(fractions)),
        })

    result = {
        "schema_version": "dti-transition-injection-recovery-v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "complete",
        "experiment_class": "independent_DESI_like_correlation_function_transfer_surrogate",
        "pipeline": [
            "fine-redshift H(z) transition injection",
            "D_H and integral D_M propagation",
            "fiducial-coordinate alpha_parallel and alpha_perpendicular",
            "broad tracer-window mixing",
            "pre/post reconstruction BAO-width bracket",
            "single shifted BAO-peak template fit with broadband marginalization",
            "published 13-observable layout and covariance",
            "smooth H(z) response profiling",
            "look-elsewhere calibrated transition-template search",
        ],
        "input_contract": {
            "values": 13,
            "effective_redshifts": sorted({row["redshift"] for row in metadata}),
            "tracer_windows": list(TRACERS),
            "mean_sha256": _sha256(data_dir / "OFFICIAL_DESI_DR2_MEAN.txt"),
            "covariance_sha256": _sha256(data_dir / "OFFICIAL_DESI_DR2_COVARIANCE.txt"),
        },
        "template_bank": {
            "candidate_count": len(bank_rows),
            "z_transition_grid": candidate_z.tolist(),
            "widths": list(candidate_widths),
        },
        "calibration": {
            "null_replicates": null_replicates,
            "scenario_replicates": scenario_replicates,
            "seed": seed,
            "thresholds_delta_chi2": thresholds,
        },
        "robust_detection_by_amplitude": robust_by_amplitude,
        "scenarios": scenario_rows,
        "claim_boundary": (
            "This quantifies transition attenuation and recoverability in an independent DESI-like "
            "correlation-function and compression surrogate. It is stronger than resampling the final "
            "13-value likelihood, but it is not the DESI production catalog, pyrecon reconstruction, "
            "RascalC covariance, desilike fit, or an observational DTI detection/exclusion."
        ),
        "known_missing_production_components": [
            "public DESI DR2 object/LSS catalogs and exact n(z)",
            "IterativeFFT displacement-field reconstruction",
            "survey window, masks, fiber assignment, and observational systematics",
            "RascalC correlation-function covariance",
            "official desilike configuration-space BAO model",
            "separate production Ly-alpha forest pipeline",
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(scenario_rows[0]))
        writer.writeheader()
        writer.writerows(scenario_rows)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_BACKEND_ROOT / "app" / "data" / "desi_dr2_bao",
    )
    parser.add_argument("--null-replicates", type=int, default=10000)
    parser.add_argument("--scenario-replicates", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260719)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--summary-output", type=Path, default=SUMMARY_PATH)
    args = parser.parse_args()
    output = run(
        data_dir=args.data_dir,
        null_replicates=args.null_replicates,
        scenario_replicates=args.scenario_replicates,
        seed=args.seed,
        output_path=args.output,
        summary_path=args.summary_output,
    )
    print("DTI_TRANSITION_INJECTION_RECOVERY=PASS")
    print("ROBUST_DETECTION=" + json.dumps(output["robust_detection_by_amplitude"], sort_keys=True))
