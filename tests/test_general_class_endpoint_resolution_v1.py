from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from dti_ui_v1.services.general_class_compute_service import (
    GeneralClassRequest,
    PUBLIC_CLASS_ENDPOINT,
    execute_general_class_compute,
)


class _Response:
    status_code = 200
    text = ""

    def json(self):
        return {"status": "ok"}


class GeneralClassEndpointResolutionTests(unittest.TestCase):
    def _request(self) -> GeneralClassRequest:
        return GeneralClassRequest(
            H0=73.0,
            omega_b=0.0224,
            omega_cdm=0.12,
            n_s=0.965,
            ln10_10_As=3.044,
            tau_reio=0.054,
            f_EDE=0.0,
            z_c=3500.0,
        )

    def test_public_endpoint_is_used_without_override(self):
        calls = []

        def fake_post(endpoint, **kwargs):
            calls.append((endpoint, kwargs))
            return _Response()

        with patch.dict(
            os.environ,
            {"DTI_CLASS_ENDPOINT": ""},
            clear=False,
        ):
            result = execute_general_class_compute(
                self._request(),
                post=fake_post,
            )

        self.assertTrue(result.accepted)
        self.assertEqual(result.endpoint, PUBLIC_CLASS_ENDPOINT)
        self.assertEqual(calls[0][0], PUBLIC_CLASS_ENDPOINT)

    def test_environment_override_is_resolved_at_call_time(self):
        calls = []
        local_endpoint = (
            "http://127.0.0.1:8000/class/compute"
        )

        def fake_post(endpoint, **kwargs):
            calls.append((endpoint, kwargs))
            return _Response()

        with patch.dict(
            os.environ,
            {"DTI_CLASS_ENDPOINT": local_endpoint},
            clear=False,
        ):
            result = execute_general_class_compute(
                self._request(),
                post=fake_post,
            )

        self.assertTrue(result.accepted)
        self.assertEqual(result.endpoint, local_endpoint)
        self.assertEqual(calls[0][0], local_endpoint)

    def test_explicit_endpoint_has_highest_priority(self):
        calls = []
        explicit = "https://example.invalid/class/compute"

        def fake_post(endpoint, **kwargs):
            calls.append((endpoint, kwargs))
            return _Response()

        with patch.dict(
            os.environ,
            {
                "DTI_CLASS_ENDPOINT":
                    "http://127.0.0.1:8000/class/compute"
            },
            clear=False,
        ):
            result = execute_general_class_compute(
                self._request(),
                endpoint=explicit,
                post=fake_post,
            )

        self.assertTrue(result.accepted)
        self.assertEqual(result.endpoint, explicit)
        self.assertEqual(calls[0][0], explicit)


if __name__ == "__main__":
    unittest.main()
