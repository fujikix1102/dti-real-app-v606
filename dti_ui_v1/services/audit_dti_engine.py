"""Bounded Audit-DTI diagnostics for DESI DR2 BAO profile curves.

This module detects statistical regime changes in a finite, explicitly supplied
grid.  It does not infer a unique physical mechanism and is not a posterior or
Bayesian-evidence calculator.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable

import numpy as np


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_desi_dr2(mean_path: Path, covariance_path: Path) -> tuple[np.ndarray, np.ndarray, list[dict[str, Any]]]:
    metadata: list[dict[str, Any]] = []
    values: list[float] = []
    with mean_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            text = line.strip()
            if not text or text.startswith("#"):
                continue
            redshift, value, observable = text.split()[:3]
            metadata.append({"redshift": float(redshift), "observable": observable})
            values.append(float(value))
    covariance = np.loadtxt(covariance_path, dtype=float)
    mean = np.asarray(values, dtype=float)
    if mean.shape != (13,) or covariance.shape != (13, 13):
        raise ValueError("DESI DR2 contract requires a 13-vector and 13x13 covariance")
    if not np.allclose(covariance, covariance.T, rtol=1e-10, atol=1e-12):
        raise ValueError("DESI DR2 covariance is not symmetric")
    np.linalg.cholesky(covariance)
    return mean, covariance, metadata


def gaussian_chi2(theory: np.ndarray, observed: np.ndarray, precision: np.ndarray) -> np.ndarray:
    residual = np.asarray(theory, dtype=float) - np.asarray(observed, dtype=float)
    return np.einsum("...i,ij,...j->...", residual, precision, residual)


def profile_grid(chi2_grid: np.ndarray, f_ede_grid: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    chi2 = np.asarray(chi2_grid, dtype=float)
    if chi2.ndim != 2 or chi2.shape[1] != len(f_ede_grid):
        raise ValueError("chi2_grid must have shape (n_H0, n_fEDE)")
    indices = np.argmin(chi2, axis=1)
    rows = np.arange(chi2.shape[0])
    return chi2[rows, indices], np.asarray(f_ede_grid, dtype=float)[indices], indices


def _bic_from_rss(rss: float, n: int, parameter_count: int) -> float:
    floor = np.finfo(float).tiny
    return float(n * math.log(max(float(rss) / n, floor)) + parameter_count * math.log(n))


def polynomial_models(x: np.ndarray, y: np.ndarray, degrees: Iterable[int] = (1, 2, 3)) -> list[dict[str, Any]]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    scaled = (x - np.mean(x)) / np.std(x)
    models: list[dict[str, Any]] = []
    for degree in degrees:
        coefficients = np.polyfit(scaled, y, int(degree))
        fitted = np.polyval(coefficients, scaled)
        rss = float(np.sum((y - fitted) ** 2))
        models.append({
            "family": "smooth_polynomial",
            "order": int(degree),
            "parameter_count": int(degree) + 1,
            "rss": rss,
            "bic": _bic_from_rss(rss, len(y), int(degree) + 1),
        })
    return models


def _segment_costs(y: np.ndarray) -> np.ndarray:
    n = len(y)
    sums = np.concatenate(([0.0], np.cumsum(y)))
    squares = np.concatenate(([0.0], np.cumsum(y * y)))
    costs = np.full((n, n + 1), np.inf)
    for start in range(n):
        lengths = np.arange(1, n - start + 1)
        totals = sums[start + lengths] - sums[start]
        totals2 = squares[start + lengths] - squares[start]
        costs[start, start + lengths] = np.maximum(totals2 - totals * totals / lengths, 0.0)
    return costs


def piecewise_constant_models(x: np.ndarray, y: np.ndarray, max_segments: int = 3, min_size: int = 4) -> list[dict[str, Any]]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(y)
    costs = _segment_costs(y)
    models: list[dict[str, Any]] = []
    for segments in range(1, max_segments + 1):
        dp = np.full((segments + 1, n + 1), np.inf)
        parents = np.full((segments + 1, n + 1), -1, dtype=int)
        dp[0, 0] = 0.0
        for count in range(1, segments + 1):
            for end in range(count * min_size, n + 1):
                starts = np.arange((count - 1) * min_size, end - min_size + 1)
                candidate = dp[count - 1, starts] + costs[starts, end]
                choice = int(np.argmin(candidate))
                dp[count, end] = candidate[choice]
                parents[count, end] = int(starts[choice])
        if not math.isfinite(dp[segments, n]):
            continue
        boundaries: list[int] = []
        end = n
        for count in range(segments, 1, -1):
            start = int(parents[count, end])
            boundaries.append(start)
            end = start
        boundaries.reverse()
        break_h0 = [float((x[index - 1] + x[index]) / 2.0) for index in boundaries]
        parameter_count = 2 * segments - 1
        models.append({
            "family": "piecewise_constant",
            "segments": segments,
            "parameter_count": parameter_count,
            "rss": float(dp[segments, n]),
            "bic": _bic_from_rss(float(dp[segments, n]), n, parameter_count),
            "boundary_indices": boundaries,
            "break_H0": break_h0,
        })
    return models


def select_transition_model(h0: np.ndarray, profiled_chi2: np.ndarray) -> dict[str, Any]:
    candidates = polynomial_models(h0, profiled_chi2) + piecewise_constant_models(h0, profiled_chi2)
    candidates.sort(key=lambda row: row["bic"])
    best = dict(candidates[0])
    best["delta_bic_to_runner_up"] = float(candidates[1]["bic"] - candidates[0]["bic"])
    best["transition_selected"] = best["family"] == "piecewise_constant" and best.get("segments", 1) > 1
    return {"best": best, "candidates": candidates}


def covariance_bootstrap(
    *,
    h0_grid: np.ndarray,
    f_ede_grid: np.ndarray,
    theory_grid: np.ndarray,
    observed: np.ndarray,
    covariance: np.ndarray,
    replicates: int = 2000,
    seed: int = 20260719,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    draws = rng.multivariate_normal(observed, covariance, size=replicates)
    precision = np.linalg.inv(covariance)
    flat_theory = np.asarray(theory_grid, dtype=float).reshape(-1, len(observed))
    residual = flat_theory[None, :, :] - draws[:, None, :]
    all_chi2 = np.einsum("bmi,ij,bmj->bm", residual, precision, residual, optimize=True)
    all_chi2 = all_chi2.reshape(replicates, len(h0_grid), len(f_ede_grid))
    profiled = np.min(all_chi2, axis=2)
    model_counts: dict[str, int] = {}
    transition_breaks: list[float] = []
    best_h0: list[float] = []
    best_f_ede: list[float] = []
    for index in range(replicates):
        selected = select_transition_model(h0_grid, profiled[index])["best"]
        label = (
            f"piecewise_K{selected['segments']}"
            if selected["family"] == "piecewise_constant"
            else f"polynomial_degree_{selected['order']}"
        )
        model_counts[label] = model_counts.get(label, 0) + 1
        if selected["family"] == "piecewise_constant" and selected.get("segments", 1) > 1:
            transition_breaks.extend(selected.get("break_H0", []))
        flat_index = int(np.argmin(all_chi2[index]))
        h_index, f_index = np.unravel_index(flat_index, (len(h0_grid), len(f_ede_grid)))
        best_h0.append(float(h0_grid[h_index]))
        best_f_ede.append(float(f_ede_grid[f_index]))
    transition_total = sum(value for key, value in model_counts.items() if key.startswith("piecewise_K") and key != "piecewise_K1")
    quantiles = (0.025, 0.16, 0.5, 0.84, 0.975)
    return {
        "replicates": replicates,
        "seed": seed,
        "model_selection_counts": model_counts,
        "model_selection_fractions": {key: value / replicates for key, value in model_counts.items()},
        "transition_selection_fraction": transition_total / replicates,
        "best_H0_quantiles": dict(zip(map(str, quantiles), map(float, np.quantile(best_h0, quantiles)))),
        "best_f_EDE_quantiles": dict(zip(map(str, quantiles), map(float, np.quantile(best_f_ede, quantiles)))),
        "transition_break_H0_quantiles": (
            dict(zip(map(str, quantiles), map(float, np.quantile(transition_breaks, quantiles))))
            if transition_breaks else None
        ),
    }


def canonical_json_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
