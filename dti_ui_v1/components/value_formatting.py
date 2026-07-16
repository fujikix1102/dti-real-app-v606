"""Pure display-formatting helpers for the perfect-fit DTI application.

This module performs no network access, file access, Streamlit rendering,
likelihood computation, sampler execution, CLASS execution, or inference.
"""

from __future__ import annotations

import math
from numbers import Real
from typing import Any


DEFAULT_MISSING_TEXT = "—"


def finite_float(value: Any) -> float | None:
    """Return a finite float, otherwise return ``None``."""

    if value is None or isinstance(value, bool):
        return None

    if isinstance(value, Real):
        converted = float(value)
    else:
        try:
            converted = float(value)
        except (TypeError, ValueError, OverflowError):
            return None

    if not math.isfinite(converted):
        return None

    return converted


def format_fixed(
    value: Any,
    digits: int,
    *,
    missing: str = DEFAULT_MISSING_TEXT,
) -> str:
    """Format one finite value with a fixed decimal-place contract."""

    if not isinstance(digits, int) or isinstance(digits, bool):
        raise TypeError("digits must be an integer")

    if digits < 0 or digits > 18:
        raise ValueError("digits must be between 0 and 18")

    converted = finite_float(value)

    if converted is None:
        return missing

    return f"{converted:.{digits}f}"


def format_integer(
    value: Any,
    *,
    missing: str = DEFAULT_MISSING_TEXT,
) -> str:
    """Format an integer-valued finite number without silent rounding."""

    converted = finite_float(value)

    if converted is None or not converted.is_integer():
        return missing

    return str(int(converted))


def format_runtime_seconds(
    value: Any,
    *,
    digits: int = 6,
    missing: str = DEFAULT_MISSING_TEXT,
) -> str:
    """Format a non-negative runtime value in seconds."""

    converted = finite_float(value)

    if converted is None or converted < 0:
        return missing

    return format_fixed(
        converted,
        digits,
        missing=missing,
    )
