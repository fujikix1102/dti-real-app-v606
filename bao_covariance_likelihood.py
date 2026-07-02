"""
bao_covariance_likelihood.py

Small local helper for covariance-aware BAO chi2 calculations.

Boundary:
- This module defines helper functions only.
- Importing this module does not read DESI files.
- Importing this module does not parse covariance.
- Importing this module does not compute chi2.
- No posterior, no MCMC, no K2 claim.

Execution occurs only when caller explicitly calls:
- load_desi_bao(...)
- theory_vector_from_callables(...)
- chi2_gls(...)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Sequence, Tuple

import numpy as np


@dataclass(frozen=True)
class DesiBaoData:
    """
    Container for BAO data vector and covariance.

    z:
        Redshift per row.
    observable:
        Observable label per row, typically DM_over_rd or DH_over_rd.
    y:
        Observed value vector.
    cov:
        Covariance matrix.
    mean_path:
        Source path for the data vector.
    cov_path:
        Source path for the covariance matrix.
    """

    z: np.ndarray
    observable: Tuple[str, ...]
    y: np.ndarray
    cov: np.ndarray
    mean_path: str
    cov_path: str


def _read_numeric_table(path: str | Path) -> List[List[str]]:
    """
    Read a whitespace/comma separated text table without interpreting comments.

    Lines beginning with # are skipped.
    Empty lines are skipped.

    This function is intentionally small and strict enough for local audit use.
    """
    p = Path(path)
    rows: List[List[str]] = []
    for raw in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        line = line.replace(",", " ")
        parts = [x for x in line.split() if x]
        if parts:
            rows.append(parts)
    return rows


def _infer_mean_columns(rows: Sequence[Sequence[str]]) -> Tuple[np.ndarray, Tuple[str, ...], np.ndarray]:
    """
    Infer a BAO mean vector from a simple text table.

    Supported row forms:
    - z observable value
    - z value observable
    - observable z value
    - z value

    If observable is absent, rows alternate DM_over_rd, DH_over_rd by row parity.
    """
    z_values: List[float] = []
    labels: List[str] = []
    y_values: List[float] = []

    def is_float(x: str) -> bool:
        try:
            float(x)
            return True
        except Exception:
            return False

    for idx, row in enumerate(rows):
        if len(row) < 2:
            raise ValueError(f"mean row has fewer than 2 columns at row {idx + 1}: {row}")

        if len(row) >= 3:
            a, b, c = row[0], row[1], row[2]

            if is_float(a) and (not is_float(b)) and is_float(c):
                z = float(a)
                obs = b
                y = float(c)
            elif is_float(a) and is_float(b) and (not is_float(c)):
                z = float(a)
                y = float(b)
                obs = c
            elif (not is_float(a)) and is_float(b) and is_float(c):
                obs = a
                z = float(b)
                y = float(c)
            elif is_float(a) and is_float(b):
                z = float(a)
                y = float(b)
                obs = "DM_over_rd" if idx % 2 == 0 else "DH_over_rd"
            else:
                raise ValueError(f"could not infer mean columns at row {idx + 1}: {row}")

        else:
            a, b = row[0], row[1]
            if not (is_float(a) and is_float(b)):
                raise ValueError(f"two-column mean row must be numeric at row {idx + 1}: {row}")
            z = float(a)
            y = float(b)
            obs = "DM_over_rd" if idx % 2 == 0 else "DH_over_rd"

        obs_norm = str(obs).strip()
        low = obs_norm.lower()

        if low in {"dm", "dm_over_rd", "dm/rd", "d_m/r_d", "dmrd"}:
            obs_norm = "DM_over_rd"
        elif low in {"dh", "dh_over_rd", "dh/rd", "d_h/r_d", "dhrd"}:
            obs_norm = "DH_over_rd"
        elif low in {"dv", "dv_over_rd", "dv/rd", "d_v/r_d", "dvrd"}:
            obs_norm = "DV_over_rd"

        z_values.append(z)
        labels.append(obs_norm)
        y_values.append(y)

    return (
        np.asarray(z_values, dtype=float),
        tuple(labels),
        np.asarray(y_values, dtype=float),
    )


def load_desi_bao(mean_path: str | Path, cov_path: str | Path) -> DesiBaoData:
    """
    Load a BAO mean vector and covariance matrix.

    This function performs file I/O only when explicitly called by the app or caller.
    It does not download files and does not infer posterior/MCMC quantities.
    """
    mean_p = Path(mean_path)
    cov_p = Path(cov_path)

    if not mean_p.is_file():
        raise FileNotFoundError(f"mean_path not found: {mean_p}")
    if not cov_p.is_file():
        raise FileNotFoundError(f"cov_path not found: {cov_p}")

    mean_rows = _read_numeric_table(mean_p)
    if not mean_rows:
        raise ValueError(f"mean file has no data rows: {mean_p}")

    z, observable, y = _infer_mean_columns(mean_rows)

    cov = np.loadtxt(cov_p, dtype=float)
    cov = np.atleast_2d(cov)

    if cov.shape[0] != cov.shape[1]:
        raise ValueError(f"covariance is not square: shape={cov.shape}")
    if cov.shape[0] != y.shape[0]:
        raise ValueError(
            f"covariance dimension does not match mean vector: cov={cov.shape}, y={y.shape}"
        )

    return DesiBaoData(
        z=z,
        observable=observable,
        y=y,
        cov=cov,
        mean_path=str(mean_p),
        cov_path=str(cov_p),
    )


def theory_vector_from_callables(
    data: DesiBaoData,
    DM_over_rs: Callable[[float], float],
    DH_over_rs: Callable[[float], float],
    DV_over_rs: Optional[Callable[[float], float]] = None,
) -> np.ndarray:
    """
    Build theory vector in the same observable order as data.

    Required callables:
    - DM_over_rs(z)
    - DH_over_rs(z)

    Optional:
    - DV_over_rs(z), only if data contains DV_over_rd.
    """
    values: List[float] = []

    for z, obs in zip(data.z, data.observable):
        label = str(obs).lower()

        if label in {"dm_over_rd", "dm/rd", "d_m/r_d", "dmrd"}:
            values.append(float(DM_over_rs(float(z))))
        elif label in {"dh_over_rd", "dh/rd", "d_h/r_d", "dhrd"}:
            values.append(float(DH_over_rs(float(z))))
        elif label in {"dv_over_rd", "dv/rd", "d_v/r_d", "dvrd"}:
            if DV_over_rs is None:
                raise ValueError("DV_over_rs callable is required for DV_over_rd rows")
            values.append(float(DV_over_rs(float(z))))
        else:
            raise ValueError(f"unsupported BAO observable label: {obs}")

    return np.asarray(values, dtype=float)


def chi2_gls(data: DesiBaoData, theory: Sequence[float]) -> float:
    """
    Compute generalized least-squares chi2: r^T C^{-1} r.

    residual convention:
    r = theory - observed

    This is a chi2 helper only. It is not a posterior, not MCMC, and not K2.
    """
    theory_arr = np.asarray(theory, dtype=float)
    if theory_arr.shape != data.y.shape:
        raise ValueError(f"theory shape {theory_arr.shape} does not match data shape {data.y.shape}")

    residual = theory_arr - data.y
    solved = np.linalg.solve(data.cov, residual)
    return float(residual.T @ solved)


__all__ = [
    "DesiBaoData",
    "load_desi_bao",
    "theory_vector_from_callables",
    "chi2_gls",
]
