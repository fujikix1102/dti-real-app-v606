"""Display-only numeric formatting; never mutates scientific values."""

from __future__ import annotations

import math
from decimal import Decimal, InvalidOperation
from typing import Any

from dti_ui_v1.contracts.numeric_precision import ALL_NUMERIC_CONTRACTS


def finite_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return result if math.isfinite(result) else None


def to_decimal(value: Any) -> Decimal:
    if isinstance(value, bool) or finite_float(value) is None:
        raise ValueError(f"not a finite decimal value: {value!r}")
    try:
        return value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"not a finite decimal value: {value!r}") from exc


def format_fixed(value: Any, places: int) -> str:
    if places < 0:
        raise ValueError("places must be nonnegative")
    if finite_float(value) is None:
        return "—"
    return f"{to_decimal(value):.{places}f}"


def format_integer(value: Any) -> str:
    number = finite_float(value)
    if number is None or not number.is_integer():
        return "—"
    return f"{int(number)}"


def format_runtime_seconds(value: Any, *, digits: int = 3) -> str:
    number = finite_float(value)
    if number is None or number < 0.0 or digits < 0:
        return "—"
    return f"{number:.{digits}f}"


def format_source_precision(value: Any) -> str:
    if finite_float(value) is None:
        return "—"
    rendered = format(to_decimal(value), "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return "0" if rendered in {"-0", ""} else rendered


def format_contract_value(key: str, value: Any | None = None, *, source_precision: bool = False) -> str:
    contract = ALL_NUMERIC_CONTRACTS[key]
    actual = contract.source_text if value is None else value
    return format_source_precision(actual) if source_precision else format_fixed(actual, contract.display_places)


def number_input_kwargs(key: str) -> dict[str, Any]:
    contract = ALL_NUMERIC_CONTRACTS[key]
    return {"value": contract.float_value, "step": contract.input_step, "format": f"%.{contract.input_places}f"}
