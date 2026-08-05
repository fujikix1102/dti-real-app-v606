"""Wiring service for the isolated Perfect Fit application.

Route boundary:
- locked: existing locked-baseline adapter path
- runtime: Route B runtime parameter adapter preparation path

This module does not:
- execute solver
- execute HTTP transport for runtime route
- evaluate likelihood
- run posterior/MCMC
"""

from __future__ import annotations

from typing import Any

from dti_ui_v1.services.general_class_compute_service import (
    execute_general_class_compute,
)

from dti_ui_v1.services.perfect_fit_http_transport import (
    post_json_transport,
)

from dti_ui_v1.services.perfect_fit_single_solver_adapter import (
    execute_locked_baseline as _locked_entrypoint,
)

from dti_ui_v1.services.perfect_fit_runtime_parameter_adapter import (
    RuntimeParameterRequest,
    build_runtime_parameter_payload,
)

from dti_ui_v1.services.perfect_fit_route_b_general_class_bridge import (
    build_general_class_request_from_route_b,
    general_class_request_to_dict,
)


_TRANSPORT_PARAMETER = "transport"


def compute_perfect_fit(
    *args: Any,
    route: str = "locked",
    **kwargs: Any,
) -> Any:
    """
    Route-aware compute entrypoint.

    Default route remains locked for backward compatibility.
    """

    if route == "locked":

        if _TRANSPORT_PARAMETER in kwargs:
            raise TypeError(
                f"{_TRANSPORT_PARAMETER} is controlled by "
                "perfect_fit_compute_service"
            )

        delegated_kwargs = dict(kwargs)
        delegated_kwargs[_TRANSPORT_PARAMETER] = post_json_transport

        return _locked_entrypoint(
            *args,
            **delegated_kwargs,
        )

    if route == "runtime":
        request = kwargs.get("request")

        if not isinstance(request, RuntimeParameterRequest):
            raise TypeError(
                "runtime route requires RuntimeParameterRequest"
            )

        general_request = (
            build_general_class_request_from_route_b(
                request
            )
        )

        return {
            "status": "ROUTE_B_PAYLOAD_READY",
            "payload": build_runtime_parameter_payload(request),
            "general_class_request": (
                general_class_request_to_dict(
                    general_request
                )
            ),
            "solver_execution": False,
            "http_execution": False,
        }

    raise ValueError(
        f"unsupported_compute_route:{route}"
    )
