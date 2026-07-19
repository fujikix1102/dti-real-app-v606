from __future__ import annotations

import unittest

from dti_ui_v1.services.general_class_compute_service import (
    GeneralClassRequest,
    build_general_class_payload,
    execute_general_class_compute,
)


class FakeResponse:
    status_code = 200

    def json(self):
        return {
            "status": "ok",
            "result": {
                "H0": 73.0,
                "rdrag_Mpc": 147.0,
            },
        }


class GeneralClassComputeServiceTests(unittest.TestCase):
    def test_payload_forwards_submitted_compute_parameters(self) -> None:
        payload = build_general_class_payload(
            GeneralClassRequest(
                H0=73.0,
                omega_b=0.0224,
                omega_cdm=0.12,
                n_s=0.965,
                ln10_10_As=3.044,
                tau_reio=0.054,
            )
        )

        self.assertEqual(payload["H0"], 73.0)
        self.assertEqual(payload["omega_b"], 0.0224)
        self.assertEqual(payload["omega_cdm"], 0.12)
        self.assertEqual(payload["n_s"], 0.965)
        self.assertEqual(payload["ln10_10_As"], 3.044)
        self.assertEqual(payload["tau_reio"], 0.054)

        self.assertEqual(payload["f_EDE"], 0.0)
        self.assertEqual(payload["z_c"], 3500.0)

    def test_execute_accepts_successful_response(self) -> None:
        calls = []

        def fake_post(endpoint, **kwargs):
            calls.append((endpoint, kwargs))
            return FakeResponse()

        result = execute_general_class_compute(
            GeneralClassRequest(
                H0=73.0,
                omega_b=0.0224,
                omega_cdm=0.12,
                n_s=0.965,
                ln10_10_As=3.044,
                tau_reio=0.054,
            ),
            post=fake_post,
        )

        self.assertTrue(result.accepted)
        self.assertEqual(result.status, "accepted")
        self.assertEqual(len(calls), 1)
        self.assertTrue(
            calls[0][0].endswith("/class/compute")
        )


if __name__ == "__main__":
    unittest.main()
