"""Fail-closed parser for the locked physical BAO backend response."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from dti_ui_v1.components.value_formatting import finite_float


class LockedBaoResponseError(ValueError):
    """Raised when a backend response violates the locked UI contract."""


@dataclass(frozen=True)
class LockedBaoResult:
    rdrag: float
    loglike: float
    chi2: float
    runtime_seconds: float
    failed_checks: int
    raw: Mapping[str, Any]


def _lookup_path(
    payload: Mapping[str, Any],
    path: Sequence[str],
) -> Any:
    current: Any = payload

    for key in path:
        if not isinstance(current, Mapping):
            return None

        if key not in current:
            return None

        current = current[key]

    return current


def _first_present(
    payload: Mapping[str, Any],
    paths: Sequence[Sequence[str]],
) -> Any:
    for path in paths:
        value = _lookup_path(payload, path)

        if value is not None:
            return value

    return None


def _required_finite(
    payload: Mapping[str, Any],
    *,
    label: str,
    paths: Sequence[Sequence[str]],
) -> float:
    raw_value = _first_present(payload, paths)
    converted = finite_float(raw_value)

    if converted is None:
        raise LockedBaoResponseError(
            f"missing or non-finite field: {label}"
        )

    return converted


def _required_nonnegative_integer(
    payload: Mapping[str, Any],
    *,
    label: str,
    paths: Sequence[Sequence[str]],
) -> int:
    value = _required_finite(
        payload,
        label=label,
        paths=paths,
    )

    if value < 0 or not value.is_integer():
        raise LockedBaoResponseError(
            f"field must be a non-negative integer: {label}"
        )

    return int(value)


def parse_locked_bao_response(
    payload: Mapping[str, Any],
) -> LockedBaoResult:
    """Parse an existing backend result without scientific recomputation."""

    if not isinstance(payload, Mapping):
        raise LockedBaoResponseError(
            "backend payload must be a mapping"
        )

    rdrag = _required_finite(
        payload,
        label="rdrag",
        paths=(
            ("rdrag",),
            ("r_drag",),
            ("rs_drag",),
            ("result", "rdrag"),
            ("result", "r_drag"),
            ("result", "rs_drag"),
        ),
    )

    loglike = _required_finite(
        payload,
        label="loglike",
        paths=(
            ("loglike",),
            ("log_likelihood",),
            ("bao_loglike",),
            ("result", "loglike"),
            ("result", "log_likelihood"),
            ("result", "bao_loglike"),
        ),
    )

    chi2 = _required_finite(
        payload,
        label="chi2",
        paths=(
            ("chi2",),
            ("chi_square",),
            ("bao_chi2",),
            ("result", "chi2"),
            ("result", "chi_square"),
            ("result", "bao_chi2"),
        ),
    )

    runtime_seconds = _required_finite(
        payload,
        label="runtime_seconds",
        paths=(
            ("runtime_seconds",),
            ("runtime",),
            ("elapsed_seconds",),
            ("result", "runtime_seconds"),
            ("result", "runtime"),
            ("result", "elapsed_seconds"),
        ),
    )

    if runtime_seconds < 0:
        raise LockedBaoResponseError(
            "runtime_seconds must be non-negative"
        )

    failed_checks = _required_nonnegative_integer(
        payload,
        label="failed_checks",
        paths=(
            ("failed_checks",),
            ("failed_check_count",),
            ("result", "failed_checks"),
            ("result", "failed_check_count"),
            ("validation", "failed_checks"),
        ),
    )

    return LockedBaoResult(
        rdrag=rdrag,
        loglike=loglike,
        chi2=chi2,
        runtime_seconds=runtime_seconds,
        failed_checks=failed_checks,
        raw=payload,
    )
