"""Source-locked HTTP transport for the Perfect Fit single-solver adapter.

This module performs transport duties only. It does not interpret physical
values, execute CLASS locally, retry requests, follow redirects, inherit proxy
configuration, or alter the adapter payload.
"""

from __future__ import annotations

import json
import socket
from collections.abc import Mapping
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import (
    HTTPRedirectHandler,
    ProxyHandler,
    Request,
    build_opener,
)

from dti_ui_v1.services.perfect_fit_single_solver_adapter import (
    DEFAULT_ENDPOINT,
    TransportConnectionError,
    TransportResponse,
    TransportTimeoutError,
)


EXACT_ENDPOINT = DEFAULT_ENDPOINT
MALFORMED_RESPONSE_SENTINEL = "__DTI_TRANSPORT_MALFORMED_RESPONSE__"
MAXIMUM_RESPONSE_BYTES = 1_048_576
MAXIMUM_READ_BYTES = MAXIMUM_RESPONSE_BYTES + 1


class _NoRedirectHandler(HTTPRedirectHandler):
    """Prevent urllib from generating a redirected request."""

    def redirect_request(
        self,
        req: Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        return None


def _read_bounded_json_body(response: Any) -> Any:
    """Read and parse one bounded UTF-8 JSON response body."""

    body = response.read(MAXIMUM_READ_BYTES)

    if len(body) > MAXIMUM_RESPONSE_BYTES:
        return MALFORMED_RESPONSE_SENTINEL

    try:
        text = body.decode("utf-8", errors="strict")
        return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return MALFORMED_RESPONSE_SENTINEL


def _is_timeout_url_error(error: URLError) -> bool:
    reason = error.reason

    if isinstance(reason, (socket.timeout, TimeoutError)):
        return True

    return "timed out" in str(reason).casefold()


def post_json_transport(
    endpoint: str,
    payload: Mapping[str, Any],
    timeout_seconds: float,
) -> TransportResponse:
    """POST one source-locked JSON request and return its HTTP response.

    The callable matches the existing TransportCallable protocol.

    No retry is performed. Redirects and environment proxy inheritance are
    disabled. Malformed, oversized, or invalid UTF-8 response bodies are
    represented by a fixed non-mapping sentinel.
    """

    if endpoint != EXACT_ENDPOINT:
        raise TransportConnectionError(
            "The HTTP transport accepts only the source-locked endpoint."
        )

    request_body = json.dumps(
        payload,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")

    request = Request(
        endpoint,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    opener = build_opener(
        ProxyHandler({}),
        _NoRedirectHandler(),
    )

    try:
        with opener.open(
            request,
            timeout=timeout_seconds,
        ) as response:
            status_code = int(response.status)
            json_body = _read_bounded_json_body(response)

            return TransportResponse(
                status_code=status_code,
                json_body=json_body,
            )

    except HTTPError as error:
        json_body = _read_bounded_json_body(error)

        return TransportResponse(
            status_code=int(error.code),
            json_body=json_body,
        )

    except (socket.timeout, TimeoutError) as error:
        raise TransportTimeoutError(
            "The source-locked HTTP request timed out."
        ) from error

    except URLError as error:
        if _is_timeout_url_error(error):
            raise TransportTimeoutError(
                "The source-locked HTTP request timed out."
            ) from error

        raise TransportConnectionError(
            "The source-locked HTTP request could not connect."
        ) from error

    except OSError as error:
        raise TransportConnectionError(
            "The source-locked HTTP request could not connect."
        ) from error
