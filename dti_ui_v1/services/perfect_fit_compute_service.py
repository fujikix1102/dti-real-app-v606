"""Wiring service for the isolated Perfect Fit application.

This module performs no scientific calculation itself. It connects the
existing fail-closed single-solver adapter to the frozen HTTP transport.

The adapter remains responsible for payload construction, endpoint policy,
response validation, status interpretation, and numeric-result acceptance.
"""

from __future__ import annotations

from typing import Any

from dti_ui_v1.services.perfect_fit_http_transport import (
    post_json_transport,
)
from dti_ui_v1.services.perfect_fit_single_solver_adapter import (
    execute_locked_baseline as _adapter_entrypoint,
)


_TRANSPORT_PARAMETER = "transport"


def compute_perfect_fit(*args: Any, **kwargs: Any) -> Any:
    """Execute the existing adapter with the fixed HTTP transport injected.

    The transport cannot be supplied or replaced by the caller. All other
    positional and keyword arguments are passed unchanged to the existing
    adapter entrypoint.
    """

    if _TRANSPORT_PARAMETER in kwargs:
        raise TypeError(
            f"{_TRANSPORT_PARAMETER} is controlled by "
            "perfect_fit_compute_service"
        )

    delegated_kwargs = dict(kwargs)
    delegated_kwargs[_TRANSPORT_PARAMETER] = post_json_transport

    return _adapter_entrypoint(
        *args,
        **delegated_kwargs,
    )
