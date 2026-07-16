from __future__ import annotations

import math
import unittest
from typing import Any

from dti_ui_v1.components.value_formatting import (
    finite_float,
    format_fixed,
    format_integer,
    format_runtime_seconds,
)
from dti_ui_v1.services.locked_bao_client import (
    LOCKED_PAYLOAD,
    LockedBaoRequest,
    build_locked_payload,
    execute_locked_bao_request,
)
from dti_ui_v1.services.response_parser import (
    LockedBaoResponseError,
    parse_locked_bao_response,
)


class FakeResponse:
    def __init__(self, payload: Any) -> None:
        self._payload = payload
        self.status_checked = False

    def raise_for_status(self) -> None:
        self.status_checked = True

    def json(self) -> Any:
        return self._payload


class FormattingTests(unittest.TestCase):
    def test_finite_float(self) -> None:
        self.assertEqual(
            finite_float("147.05426111673114"),
            147.05426111673114,
        )
        self.assertEqual(finite_float(0), 0.0)
        self.assertIsNone(finite_float(None))
        self.assertIsNone(finite_float(True))
        self.assertIsNone(finite_float(math.nan))
        self.assertIsNone(finite_float(math.inf))

    def test_public_precision_contract(self) -> None:
        self.assertEqual(
            format_fixed(
                147.05426111673114,
                9,
            ),
            "147.054261117",
        )
        self.assertEqual(
            format_fixed(
                -15.716960481571116,
                12,
            ),
            "-15.716960481571",
        )
        self.assertEqual(
            format_fixed(
                31.43392096314223,
                12,
            ),
            "31.433920963142",
        )
        self.assertEqual(
            format_runtime_seconds(
                0.799657,
                digits=6,
            ),
            "0.799657",
        )
        self.assertEqual(format_integer(0), "0")

    def test_invalid_display_values(self) -> None:
        self.assertEqual(format_fixed(None, 4), "—")
        self.assertEqual(format_integer(1.5), "—")
        self.assertEqual(
            format_runtime_seconds(-1),
            "—",
        )

        with self.assertRaises(ValueError):
            format_fixed(1.0, -1)


class ParserTests(unittest.TestCase):
    def test_flat_payload(self) -> None:
        result = parse_locked_bao_response(
            {
                "rdrag": 147.05426111673114,
                "loglike": -15.716960481571116,
                "chi2": 31.43392096314223,
                "runtime_seconds": 0.799657,
                "failed_checks": 0,
            }
        )

        self.assertAlmostEqual(
            result.rdrag,
            147.05426111673114,
        )
        self.assertAlmostEqual(
            result.loglike,
            -15.716960481571116,
        )
        self.assertAlmostEqual(
            result.chi2,
            31.43392096314223,
        )
        self.assertEqual(
            result.runtime_seconds,
            0.799657,
        )
        self.assertEqual(result.failed_checks, 0)

    def test_nested_alias_payload(self) -> None:
        result = parse_locked_bao_response(
            {
                "result": {
                    "rs_drag": 147.0,
                    "bao_loglike": -15.0,
                    "bao_chi2": 30.0,
                    "runtime": 1.25,
                    "failed_check_count": 0,
                }
            }
        )

        self.assertEqual(result.rdrag, 147.0)
        self.assertEqual(result.runtime_seconds, 1.25)
        self.assertEqual(result.failed_checks, 0)

    def test_missing_field_fails_closed(self) -> None:
        with self.assertRaises(
            LockedBaoResponseError
        ):
            parse_locked_bao_response(
                {
                    "rdrag": 147.0,
                    "loglike": -15.0,
                    "chi2": 30.0,
                    "runtime_seconds": 1.0,
                }
            )

    def test_nonfinite_field_fails_closed(self) -> None:
        with self.assertRaises(
            LockedBaoResponseError
        ):
            parse_locked_bao_response(
                {
                    "rdrag": math.nan,
                    "loglike": -15.0,
                    "chi2": 30.0,
                    "runtime_seconds": 1.0,
                    "failed_checks": 0,
                }
            )


class LockedClientTests(unittest.TestCase):
    def test_payload_is_exact_and_fresh(self) -> None:
        first = build_locked_payload()
        second = build_locked_payload()

        self.assertEqual(
            first,
            {"use_locked_baseline": True},
        )
        self.assertEqual(
            first,
            dict(LOCKED_PAYLOAD),
        )
        self.assertIsNot(first, second)

    def test_offline_injected_post(self) -> None:
        calls: list[dict[str, Any]] = []

        def fake_post(
            endpoint: str,
            **kwargs: Any,
        ) -> FakeResponse:
            calls.append(
                {
                    "endpoint": endpoint,
                    **kwargs,
                }
            )

            return FakeResponse(
                {
                    "rdrag": 147.05426111673114,
                    "loglike": -15.716960481571116,
                    "chi2": 31.43392096314223,
                    "runtime_seconds": 0.799657,
                    "failed_checks": 0,
                }
            )

        request = LockedBaoRequest()

        result = execute_locked_bao_request(
            request,
            post=fake_post,
        )

        self.assertEqual(len(calls), 1)
        self.assertEqual(
            calls[0]["json"],
            {"use_locked_baseline": True},
        )
        self.assertEqual(
            calls[0]["timeout"],
            120.0,
        )
        self.assertEqual(result.failed_checks, 0)

    def test_invalid_endpoint_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            LockedBaoRequest(
                endpoint="file:///tmp/backend"
            )


if __name__ == "__main__":
    unittest.main()
