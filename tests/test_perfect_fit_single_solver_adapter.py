from __future__ import annotations

import math
import unittest

from dti_ui_v1.services.perfect_fit_single_solver_adapter import (
    AdapterStatus,
    BACKEND_CAPABILITY,
    DEFAULT_ENDPOINT,
    PHYSICAL_BOUNDARY_LABEL,
    LockedBaselineRequest,
    TransportConnectionError,
    TransportResponse,
    TransportTimeoutError,
    build_locked_payload,
    execute_locked_baseline,
)


class RecordingTransport:
    def __init__(self, response: TransportResponse):
        self.response = response
        self.calls = []

    def __call__(self, endpoint, payload, timeout_seconds):
        self.calls.append(
            {
                "endpoint": endpoint,
                "payload": payload,
                "timeout_seconds": timeout_seconds,
            }
        )
        return self.response


class PerfectFitSingleSolverAdapterTests(unittest.TestCase):
    def test_build_locked_payload_exact(self):
        payload = build_locked_payload(LockedBaselineRequest())
        self.assertEqual(payload, {"use_locked_baseline": True})

    def test_valid_locked_baseline_response(self):
        transport = RecordingTransport(
            TransportResponse(
                status_code=200,
                json_body={
                    "success": True,
                    "backend_capability": "CLASS_LCDM_LIKE_LOCKED_BASELINE",
                    "result": {
                        "DM_over_rd": 17.529060304302188,
                        "DH_over_rd": 19.97950604135878,
                    },
                },
            )
        )

        result = execute_locked_baseline(
            LockedBaselineRequest(),
            transport=transport,
        )

        self.assertTrue(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.SUCCESS_LOCKED_BASELINE,
        )
        self.assertEqual(result.endpoint, DEFAULT_ENDPOINT)
        self.assertEqual(
            result.physical_boundary_label,
            PHYSICAL_BOUNDARY_LABEL,
        )
        self.assertEqual(result.backend_capability, BACKEND_CAPABILITY)
        self.assertIsNotNone(result.validated_payload)
        self.assertEqual(len(transport.calls), 1)
        self.assertEqual(
            transport.calls[0]["payload"],
            {"use_locked_baseline": True},
        )

    def test_no_transport_means_no_execution(self):
        result = execute_locked_baseline(
            LockedBaselineRequest(),
            transport=None,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.BOUNDARY_VIOLATION,
        )
        self.assertIsNone(result.validated_payload)

    def test_use_locked_baseline_false_rejected_before_transport(self):
        transport = RecordingTransport(
            TransportResponse(
                status_code=200,
                json_body={
                    "success": True,
                    "result": {"x": 1.0},
                },
            )
        )

        result = execute_locked_baseline(
            LockedBaselineRequest(use_locked_baseline=False),
            transport=transport,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.BOUNDARY_VIOLATION,
        )
        self.assertEqual(transport.calls, [])

    def test_bool_timeout_rejected(self):
        request = LockedBaselineRequest(timeout_seconds=True)

        result = execute_locked_baseline(
            request,
            transport=None,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.REQUEST_VALIDATION_FAILURE,
        )

    def test_nan_timeout_rejected(self):
        request = LockedBaselineRequest(timeout_seconds=math.nan)

        result = execute_locked_baseline(
            request,
            transport=None,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.REQUEST_VALIDATION_FAILURE,
        )

    def test_infinite_timeout_rejected(self):
        request = LockedBaselineRequest(timeout_seconds=math.inf)

        result = execute_locked_baseline(
            request,
            transport=None,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.REQUEST_VALIDATION_FAILURE,
        )

    def test_timeout_upper_bound_enforced(self):
        request = LockedBaselineRequest(timeout_seconds=120.0001)

        result = execute_locked_baseline(
            request,
            transport=None,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.REQUEST_VALIDATION_FAILURE,
        )

    def test_nonzero_f_ede_rejected_without_transport(self):
        transport = RecordingTransport(
            TransportResponse(
                status_code=200,
                json_body={
                    "success": True,
                    "result": {"x": 1.0},
                },
            )
        )

        result = execute_locked_baseline(
            LockedBaselineRequest(f_EDE=0.01),
            transport=transport,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.UNSUPPORTED_EDE_EXECUTION,
        )
        self.assertIsNone(result.validated_payload)
        self.assertEqual(transport.calls, [])

    def test_z_c_request_rejected_without_transport(self):
        transport = RecordingTransport(
            TransportResponse(
                status_code=200,
                json_body={
                    "success": True,
                    "result": {"x": 1.0},
                },
            )
        )

        result = execute_locked_baseline(
            LockedBaselineRequest(z_c=3500.0),
            transport=transport,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.UNSUPPORTED_EDE_EXECUTION,
        )
        self.assertEqual(transport.calls, [])

    def test_endpoint_override_rejected_without_transport(self):
        transport = RecordingTransport(
            TransportResponse(
                status_code=200,
                json_body={
                    "success": True,
                    "result": {"x": 1.0},
                },
            )
        )

        result = execute_locked_baseline(
            LockedBaselineRequest(),
            transport=transport,
            endpoint="https://example.invalid/fallback",
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.BOUNDARY_VIOLATION,
        )
        self.assertEqual(transport.calls, [])

    def test_timeout_failure_creates_no_numeric_payload(self):
        def timeout_transport(endpoint, payload, timeout_seconds):
            raise TransportTimeoutError("offline simulated timeout")

        result = execute_locked_baseline(
            LockedBaselineRequest(),
            transport=timeout_transport,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(result.status, AdapterStatus.HTTP_TIMEOUT)
        self.assertIsNone(result.validated_payload)

    def test_connection_failure_creates_no_numeric_payload(self):
        def connection_transport(endpoint, payload, timeout_seconds):
            raise TransportConnectionError("offline simulated connection failure")

        result = execute_locked_baseline(
            LockedBaselineRequest(),
            transport=connection_transport,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.HTTP_CONNECTION_FAILURE,
        )
        self.assertIsNone(result.validated_payload)

    def test_non_2xx_rejected(self):
        transport = RecordingTransport(
            TransportResponse(
                status_code=503,
                json_body={
                    "success": False,
                    "detail": "unavailable",
                },
            )
        )

        result = execute_locked_baseline(
            LockedBaselineRequest(),
            transport=transport,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.HTTP_STATUS_FAILURE,
        )
        self.assertIsNone(result.validated_payload)

    def test_malformed_json_root_rejected(self):
        transport = RecordingTransport(
            TransportResponse(
                status_code=200,
                json_body=["not", "a", "mapping"],
            )
        )

        result = execute_locked_baseline(
            LockedBaselineRequest(),
            transport=transport,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.MALFORMED_RESPONSE,
        )
        self.assertIsNone(result.validated_payload)

    def test_backend_declared_failure_rejected(self):
        transport = RecordingTransport(
            TransportResponse(
                status_code=200,
                json_body={
                    "success": False,
                    "result": {"x": 1.0},
                },
            )
        )

        result = execute_locked_baseline(
            LockedBaselineRequest(),
            transport=transport,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.BACKEND_DECLARED_FAILURE,
        )

    def test_missing_result_mapping_rejected(self):
        transport = RecordingTransport(
            TransportResponse(
                status_code=200,
                json_body={
                    "success": True,
                    "message": "no result",
                },
            )
        )

        result = execute_locked_baseline(
            LockedBaselineRequest(),
            transport=transport,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.SCHEMA_VALIDATION_FAILURE,
        )

    def test_non_finite_response_value_rejected(self):
        transport = RecordingTransport(
            TransportResponse(
                status_code=200,
                json_body={
                    "success": True,
                    "result": {"DM_over_rd": math.nan},
                },
            )
        )

        result = execute_locked_baseline(
            LockedBaselineRequest(),
            transport=transport,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.SCHEMA_VALIDATION_FAILURE,
        )

    def test_axiclass_ede_overclaim_rejected(self):
        transport = RecordingTransport(
            TransportResponse(
                status_code=200,
                json_body={
                    "success": True,
                    "backend_capability": "AXICLASS_EDE_EXECUTION",
                    "result": {"DM_over_rd": 17.5},
                },
            )
        )

        result = execute_locked_baseline(
            LockedBaselineRequest(),
            transport=transport,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.BOUNDARY_VIOLATION,
        )

    def test_backend_busy_status_rejected(self):
        transport = RecordingTransport(
            TransportResponse(
                status_code=200,
                json_body={
                    "status": "busy",
                    "message": "A physical solver request is already running.",
                    "retryable": True,
                },
            )
        )

        result = execute_locked_baseline(
            LockedBaselineRequest(),
            transport=transport,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.BACKEND_DECLARED_FAILURE,
        )

    def test_backend_rejected_status_rejected(self):
        transport = RecordingTransport(
            TransportResponse(
                status_code=200,
                json_body={
                    "status": "rejected",
                    "message": "Only the locked baseline contract is currently allowed.",
                },
            )
        )

        result = execute_locked_baseline(
            LockedBaselineRequest(),
            transport=transport,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.status,
            AdapterStatus.BACKEND_DECLARED_FAILURE,
        )


if __name__ == "__main__":
    unittest.main()
