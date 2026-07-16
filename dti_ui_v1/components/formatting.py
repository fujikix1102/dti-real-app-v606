from __future__ import annotations

import math
from typing import Any


def formatted_number(
    value: Any,
    digits: int,
    *,
    fallback: str = "n/a",
) -> str:
    """Format finite numeric values without mutating the raw value."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return fallback

    if not math.isfinite(number):
        return fallback

    return f"{number:.{digits}f}"
