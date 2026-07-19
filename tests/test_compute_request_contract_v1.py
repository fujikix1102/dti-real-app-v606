from __future__ import annotations

import json
import math
import unittest

from dti_ui_v1.contracts.compute_request import (
    ComputeContractError,
)
from dti_ui_v1.services.compute_request_builder import (
    build_compute_request,
)


PARAMETERS = [
    {
        "name": "H0",
        "value": 67.32117,
        "unit": "km s^-1 Mpc^-1",
        "role": "fixed",
    },
    {
        "name": "omega_b",
        "value": 0.0223828,
        "unit": "dimensionless",
        "role": "fixed",
    },
]


class ComputeRequestTests(unittest.TestCase):
    def test_valid_request(self) -> None:
        request = build_compute_request(
            solver="CLASS",
            route="SINGLE_BACKGROUND",
            parameters=PARAMETERS,
            request_id="pf-test-request-0001",
        )

        payload = request.to_payload()

        self.assertEqual(payload["solver"], "CLASS")
        self.assertEqual(
            payload["route"],
            "SINGLE_BACKGROUND",
        )
        self.assertEqual(payload["state"], "VALIDATED")
        self.assertEqual(len(request.sha256()), 64)
        self.assertEqual(
            json.loads(request.canonical_json()),
            payload,
        )

    def test_duplicate_parameter_rejected(self) -> None:
        with self.assertRaises(ComputeContractError):
            build_compute_request(
                solver="CLASS",
                route="SINGLE_BACKGROUND",
                parameters=PARAMETERS + [PARAMETERS[0]],
                request_id="pf-test-request-0002",
            )

    def test_nan_rejected(self) -> None:
        bad = [dict(PARAMETERS[0])]
        bad[0]["value"] = math.nan

        with self.assertRaises(ComputeContractError):
            build_compute_request(
                solver="CLASS",
                route="SINGLE_BACKGROUND",
                parameters=bad,
                request_id="pf-test-request-0003",
            )

    def test_unknown_solver_rejected(self) -> None:
        with self.assertRaises(ComputeContractError):
            build_compute_request(
                solver="UNKNOWN",
                route="SINGLE_BACKGROUND",
                parameters=PARAMETERS,
                request_id="pf-test-request-0004",
            )

    def test_unknown_route_rejected(self) -> None:
        with self.assertRaises(ComputeContractError):
            build_compute_request(
                solver="CLASS",
                route="UNKNOWN",
                parameters=PARAMETERS,
                request_id="pf-test-request-0005",
            )

    def test_timeout_rejected(self) -> None:
        with self.assertRaises(ComputeContractError):
            build_compute_request(
                solver="CLASS",
                route="SINGLE_BACKGROUND",
                parameters=PARAMETERS,
                timeout_seconds=0,
                request_id="pf-test-request-0006",
            )


if __name__ == "__main__":
    unittest.main()
