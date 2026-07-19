"""Builder for validated PERFECT FIT compute requests."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from dti_ui_v1.contracts.compute_request import (
    ComputeContractError,
    ComputeRequest,
    ExecutionRoute,
    SolverKind,
    new_request_id,
    parameter_from_mapping,
)


def build_compute_request(
    *,
    solver: str,
    route: str,
    parameters: list[Mapping[str, Any]],
    timeout_seconds: int = 120,
    request_id: str | None = None,
    source: str = "perfect_fit_ui",
) -> ComputeRequest:
    try:
        solver_kind = SolverKind(solver)
    except ValueError as exc:
        raise ComputeContractError(
            f"unsupported solver: {solver!r}"
        ) from exc

    try:
        execution_route = ExecutionRoute(route)
    except ValueError as exc:
        raise ComputeContractError(
            f"unsupported route: {route!r}"
        ) from exc

    request = ComputeRequest(
        schema_version="perfect-fit.compute-request.v1",
        request_id=request_id or new_request_id(),
        solver=solver_kind,
        route=execution_route,
        parameters=tuple(
            parameter_from_mapping(item)
            for item in parameters
        ),
        timeout_seconds=int(timeout_seconds),
        source=source,
    )

    request.validate()
    return request
