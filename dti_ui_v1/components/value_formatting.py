"""Central numeric formatting utilities.

These functions affect display only. They must not be used to mutate
scientific inputs, backend payloads, stored results, or source records.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

from dti_ui_v1.contracts.numeric_precision import (
    ALL_NUMERIC_CONTRACTS,
)


def to_decimal(value: Any) -> Decimal:
    if isinstance(value, Decimal):
        return value

    if isinstance(value, float):
        return Decimal(str(value))

    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"not a finite decimal value: {value!r}") from exc


def format_fixed(
    value: Any,
    places: int,
) -> str:
    decimal_value = to_decimal(value)
    return f"{decimal_value:.{places}f}"


def format_source_precision(value: Any) -> str:
    """Show a decimal without binary-float artifacts or forced zeros."""

    decimal_value = to_decimal(value)

    rendered = format(decimal_value, "f")

    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")

    if rendered in {"-0", ""}:
        return "0"

    return rendered


def format_contract_value(
    key: str,
    value: Any | None = None,
    *,
    source_precision: bool = False,
) -> str:
    contract = ALL_NUMERIC_CONTRACTS[key]

    actual = (
        contract.source_text
        if value is None
        else value
    )

    if source_precision:
        return format_source_precision(actual)

    return format_fixed(
        actual,
        contract.display_places,
    )


def number_input_kwargs(key: str) -> dict[str, Any]:
    contract = ALL_NUMERIC_CONTRACTS[key]

    return {
        "value": contract.float_value,
        "step": contract.input_step,
        "format": f"%.{contract.input_places}f",
    }
