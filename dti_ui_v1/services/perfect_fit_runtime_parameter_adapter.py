"""Runtime parameter adapter for PERFECT FIT Route B.

This module is intentionally isolated from the locked baseline adapter.

Boundary:
- no solver execution
- no HTTP execution
- no likelihood evaluation
- no posterior/MCMC
- no scientific claim generation

This module only defines:
- runtime parameter request contract
- parameter validation
- runtime payload construction
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Mapping


MAX_TIMEOUT_SECONDS = 120.0


class RuntimeParameterValidationError(ValueError):
    pass


@dataclass(frozen=True)
class RuntimeParameterRequest:
    parameters: Mapping[str, float]
    timeout_seconds: float = 120.0


def _validate_number(name: str, value: Any) -> float:
    if isinstance(value, bool):
        raise RuntimeParameterValidationError(
            f"{name}_must_not_be_bool"
        )

    if not isinstance(value, (int, float)):
        raise RuntimeParameterValidationError(
            f"{name}_must_be_numeric"
        )

    value = float(value)

    if not math.isfinite(value):
        raise RuntimeParameterValidationError(
            f"{name}_must_be_finite"
        )

    return value


def validate_runtime_parameter_request(
    request: RuntimeParameterRequest,
) -> None:
    if not isinstance(request, RuntimeParameterRequest):
        raise RuntimeParameterValidationError(
            "request_must_be_RuntimeParameterRequest"
        )

    timeout = _validate_number(
        "timeout_seconds",
        request.timeout_seconds,
    )

    if timeout <= 0 or timeout > MAX_TIMEOUT_SECONDS:
        raise RuntimeParameterValidationError(
            "timeout_out_of_range"
        )

    if not isinstance(request.parameters, Mapping):
        raise RuntimeParameterValidationError(
            "parameters_must_be_mapping"
        )

    if not request.parameters:
        raise RuntimeParameterValidationError(
            "parameters_must_not_be_empty"
        )

    for key, value in request.parameters.items():
        if not isinstance(key, str):
            raise RuntimeParameterValidationError(
                "parameter_name_must_be_string"
            )

        _validate_number(
            key,
            value,
        )


def build_runtime_parameter_payload(
    request: RuntimeParameterRequest,
) -> dict[str, Any]:
    validate_runtime_parameter_request(request)

    return {
        "parameters": {
            key: float(value)
            for key, value in request.parameters.items()
        }
    }


def runtime_parameter_route_enabled() -> bool:
    """
    Route B capability marker only.

    Does not indicate solver availability.
    """

    return True
