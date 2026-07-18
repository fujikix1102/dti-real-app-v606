from __future__ import annotations

import io
import json
import math
import os
import socket
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request

from dti_ui_v1.services import perfect_fit_http_transport as transport_module
from dti_ui_v1.services.perfect_fit_http_transport import (
    EXACT_ENDPOINT,
    MALFORMED_RESPONSE_SENTINEL,
    MAXIMUM_RESPONSE_BYTES,
    _NoRedirectHandler,
    post_json_transport,
)
from dti_ui_v1.services.perfect_fit_single_solver_adapter import (
    TransportConnectionError,
    TransportResponse,
    TransportTimeoutError,
)


class FakeResponse:
    def __init__(
        self,
        status: int,
        body: bytes,
    ) -> None:
        self.status = status
        self._body = io.BytesIO(body)
        self.read_sizes: list[int] = []

    def read(
        self,
        size: int = -1,
    ) -> bytes:
        self.read_sizes.append(size)
        return self._body.read(size)

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(
        self,
        exc_type: Any,
        exc_value: Any,
        traceback: Any,
    ) -> None:
        return None


class FakeOpener:
    def __init__(
        self,
        outcome: Any,
    ) -> None:
        self.outcome = outcome
        self.calls: list[tuple[Request, float]] = []

    def open(
        self,
        request: Request,
        timeout: float,
    ) -> Any:
        self.calls.append((request, timeout))

        if isinstance(self.outcome, BaseException):
            raise self.outcome

        return self.outcome


def make_http_error(
    code: int,
    body: bytes,
) -> HTTPError:
    return HTTPError(
        url=EXACT_ENDPOINT,
        code=code,
        msg="test error",
        hdrs=None,
        fp=io.BytesIO(body),
    )


class PerfectFitHttpTransportTests(unittest.TestCase):
    def call_with_opener(
        self,
        opener: FakeOpener,
        *,
        endpoint: str = EXACT_ENDPOINT,
        payload: dict[str, Any] | None = None,
        timeout_seconds: float = 12.5,
    ) -> tuple[TransportResponse, Any]:
        if payload is None:
            payload = {"use_locked_baseline": True}

        with patch.object(
            transport_module,
            "build_opener",
            return_value=opener,
        ) as build_mock:
            result = post_json_transport(
                endpoint,
                payload,
                timeout_seconds,
            )

        return result, build_mock

    def test_valid_exact_endpoint_json_post(self):
        response = FakeResponse(
            200,
            b'{"status":"ok","result":{"x":1.0}}',
        )
        opener = FakeOpener(response)

        result, _ = self.call_with_opener(opener)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            result.json_body,
            {
                "status": "ok",
                "result": {"x": 1.0},
            },
        )
        self.assertEqual(len(opener.calls), 1)

    def test_non_finite_request_json_rejected_before_open(self):
        opener = FakeOpener(
            FakeResponse(200, b'{"status":"ok"}')
        )

        with patch.object(
            transport_module,
            "build_opener",
            return_value=opener,
        ):
            with self.assertRaises(ValueError):
                post_json_transport(
                    EXACT_ENDPOINT,
                    {"value": math.nan},
                    12.5,
                )

        self.assertEqual(opener.calls, [])

    def test_socket_timeout_maps_to_transport_timeout(self):
        opener = FakeOpener(socket.timeout("timed out"))

        with self.assertRaises(TransportTimeoutError):
            self.call_with_opener(opener)

    def test_timeout_error_maps_to_transport_timeout(self):
        opener = FakeOpener(TimeoutError("timed out"))

        with self.assertRaises(TransportTimeoutError):
            self.call_with_opener(opener)

    def test_url_error_timeout_reason_maps_to_timeout(self):
        opener = FakeOpener(
            URLError(socket.timeout("timed out"))
        )

        with self.assertRaises(TransportTimeoutError):
            self.call_with_opener(opener)

    def test_url_error_non_timeout_maps_to_connection(self):
        opener = FakeOpener(
            URLError("connection refused")
        )

        with self.assertRaises(TransportConnectionError):
            self.call_with_opener(opener)

    def test_os_error_maps_to_connection(self):
        opener = FakeOpener(
            OSError("network unavailable")
        )

        with self.assertRaises(TransportConnectionError):
            self.call_with_opener(opener)

    def test_http_error_valid_json_preserves_status(self):
        opener = FakeOpener(
            make_http_error(
                503,
                b'{"status":"busy","retryable":true}',
            )
        )

        result, _ = self.call_with_opener(opener)

        self.assertEqual(result.status_code, 503)
        self.assertEqual(
            result.json_body,
            {
                "status": "busy",
                "retryable": True,
            },
        )
        self.assertEqual(len(opener.calls), 1)

    def test_http_error_invalid_json_returns_sentinel(self):
        opener = FakeOpener(
            make_http_error(
                400,
                b"not-json",
            )
        )

        result, _ = self.call_with_opener(opener)

        self.assertEqual(result.status_code, 400)
        self.assertEqual(
            result.json_body,
            MALFORMED_RESPONSE_SENTINEL,
        )

    def test_invalid_utf8_returns_sentinel(self):
        opener = FakeOpener(
            FakeResponse(
                200,
                b"\xff\xfe\xfa",
            )
        )

        result, _ = self.call_with_opener(opener)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            result.json_body,
            MALFORMED_RESPONSE_SENTINEL,
        )

    def test_invalid_json_returns_sentinel(self):
        opener = FakeOpener(
            FakeResponse(
                200,
                b'{"status":',
            )
        )

        result, _ = self.call_with_opener(opener)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            result.json_body,
            MALFORMED_RESPONSE_SENTINEL,
        )

    def test_body_exactly_one_mib_is_accepted(self):
        body = (
            b'"'
            + b"a" * (MAXIMUM_RESPONSE_BYTES - 2)
            + b'"'
        )
        self.assertEqual(
            len(body),
            MAXIMUM_RESPONSE_BYTES,
        )

        response = FakeResponse(200, body)
        opener = FakeOpener(response)

        result, _ = self.call_with_opener(opener)

        self.assertEqual(result.status_code, 200)
        self.assertIsInstance(result.json_body, str)
        self.assertEqual(
            len(result.json_body),
            MAXIMUM_RESPONSE_BYTES - 2,
        )
        self.assertEqual(
            response.read_sizes,
            [MAXIMUM_RESPONSE_BYTES + 1],
        )

    def test_body_larger_than_one_mib_returns_sentinel(self):
        body = b"x" * (MAXIMUM_RESPONSE_BYTES + 1)
        response = FakeResponse(200, body)
        opener = FakeOpener(response)

        result, _ = self.call_with_opener(opener)

        self.assertEqual(
            result.json_body,
            MALFORMED_RESPONSE_SENTINEL,
        )
        self.assertEqual(
            response.read_sizes,
            [MAXIMUM_RESPONSE_BYTES + 1],
        )

    def test_redirect_handler_generates_no_redirect_request(self):
        handler = _NoRedirectHandler()

        redirected = handler.redirect_request(
            Request(EXACT_ENDPOINT),
            None,
            302,
            "Found",
            {},
            "https://example.invalid/alternate",
        )

        self.assertIsNone(redirected)

        opener = FakeOpener(
            make_http_error(
                302,
                b'{"status":"redirect"}',
            )
        )

        result, _ = self.call_with_opener(opener)

        self.assertEqual(result.status_code, 302)
        self.assertEqual(
            result.json_body,
            {"status": "redirect"},
        )
        self.assertEqual(len(opener.calls), 1)

    def test_environment_proxy_is_not_inherited(self):
        response = FakeResponse(
            200,
            b'{"status":"ok"}',
        )
        opener = FakeOpener(response)

        proxy_environment = {
            "HTTP_PROXY": "http://proxy.invalid:8080",
            "HTTPS_PROXY": "http://proxy.invalid:8080",
            "ALL_PROXY": "socks5://proxy.invalid:1080",
        }

        with patch.dict(
            os.environ,
            proxy_environment,
            clear=False,
        ):
            result, build_mock = self.call_with_opener(
                opener
            )

        self.assertEqual(result.status_code, 200)

        handlers = build_mock.call_args.args

        proxy_handlers = [
            handler
            for handler in handlers
            if isinstance(handler, ProxyHandler)
        ]

        self.assertEqual(len(proxy_handlers), 1)
        self.assertEqual(proxy_handlers[0].proxies, {})

    def test_alternate_endpoint_rejected_before_opener(self):
        with patch.object(
            transport_module,
            "build_opener",
        ) as build_mock:
            with self.assertRaises(
                TransportConnectionError
            ):
                post_json_transport(
                    "https://example.invalid/alternate",
                    {"use_locked_baseline": True},
                    12.5,
                )

        build_mock.assert_not_called()

    def test_retryable_busy_response_opens_once(self):
        response = FakeResponse(
            503,
            b'{"status":"busy","retryable":true}',
        )
        opener = FakeOpener(response)

        result, _ = self.call_with_opener(opener)

        self.assertEqual(result.status_code, 503)
        self.assertEqual(
            result.json_body["status"],
            "busy",
        )
        self.assertEqual(len(opener.calls), 1)

    def test_request_headers_and_method(self):
        response = FakeResponse(
            200,
            b'{"status":"ok"}',
        )
        opener = FakeOpener(response)

        self.call_with_opener(opener)

        request, timeout = opener.calls[0]
        headers = {
            key.casefold(): value
            for key, value in request.header_items()
        }

        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(
            headers["content-type"],
            "application/json",
        )
        self.assertEqual(
            headers["accept"],
            "application/json",
        )
        self.assertEqual(timeout, 12.5)

    def test_payload_is_not_mutated(self):
        payload = {
            "use_locked_baseline": True,
            "nested": {
                "values": [1, 2, 3],
            },
        }

        before = json.loads(
            json.dumps(
                payload,
                sort_keys=True,
            )
        )

        response = FakeResponse(
            200,
            b'{"status":"ok"}',
        )
        opener = FakeOpener(response)

        self.call_with_opener(
            opener,
            payload=payload,
        )

        self.assertEqual(payload, before)

    def test_no_raw_payload_or_response_logging(self):
        source = Path(
            transport_module.__file__
        ).read_text(encoding="utf-8")

        forbidden_fragments = (
            "print(",
            "logging.",
            "logger.",
            "basicConfig(",
            "request_body.decode(",
            "repr(payload)",
            "repr(body)",
        )

        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, source)


if __name__ == "__main__":
    unittest.main()
