"""Bounded client for the locked physical BAO endpoint.

The only request body permitted by this module is:
{"use_locked_baseline": true}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping, Protocol

from dti_ui_v1.services.response_parser import (
    LockedBaoResult,
    parse_locked_bao_response,
)


DEFAULT_ENDPOINT = (
    "https://dti-class-api.onrender.com/"
    "axiclass/desi-dr2-bao"
)

LOCKED_PAYLOAD: Mapping[str, bool] = {
    "use_locked_baseline": True,
}


class ResponseLike(Protocol):
    def raise_for_status(self) -> None: ...

    def json(self) -> Any: ...


PostCallable = Callable[..., ResponseLike]


@dataclass(frozen=True)
class LockedBaoRequest:
    endpoint: str = DEFAULT_ENDPOINT
    timeout_seconds: float = 120.0

    def __post_init__(self) -> None:
        if not self.endpoint.startswith(
            ("https://", "http://")
        ):
            raise ValueError(
                "endpoint must use HTTP or HTTPS"
            )

        if self.timeout_seconds <= 0:
            raise ValueError(
                "timeout_seconds must be positive"
            )


def build_locked_payload() -> dict[str, bool]:
    """Return a fresh copy of the immutable scientific-input contract."""

    return dict(LOCKED_PAYLOAD)


def execute_locked_bao_request(
    request: LockedBaoRequest,
    *,
    post: PostCallable,
    headers: Mapping[str, str] | None = None,
) -> LockedBaoResult:
    """Execute one injected POST and parse its bounded response."""

    response = post(
        request.endpoint,
        json=build_locked_payload(),
        headers=dict(headers or {}),
        timeout=request.timeout_seconds,
    )

    response.raise_for_status()

    return parse_locked_bao_response(
        response.json()
    )
