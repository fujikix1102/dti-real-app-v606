from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

try:
    from dti_ui_v1.services.general_class_compute_service import (
        CLASS_ENDPOINT_ENV,
        GeneralClassRequest,
        LOCAL_CLASS_ENDPOINT,
        PUBLIC_CLASS_ENDPOINT,
        build_general_class_payload,
        resolve_class_endpoint,
    )
    from dti_ui_v1.services import run_store
except ImportError:
    from general_class_compute_service import (
        CLASS_ENDPOINT_ENV,
        GeneralClassRequest,
        LOCAL_CLASS_ENDPOINT,
        PUBLIC_CLASS_ENDPOINT,
        build_general_class_payload,
        resolve_class_endpoint,
    )
    import run_store


class GeneralClassExtensionTests(unittest.TestCase):
    def test_desi_likelihood_requested_by_default(self) -> None:
        payload = build_general_class_payload(
            GeneralClassRequest(72.9, 0.0244, 0.127, 0.9847, 3.058, 0.0511, 0.082, 3500)
        )
        self.assertIs(payload["evaluate_desi_bao"], True)
        self.assertIs(payload["evaluate_planck_2018"], True)
        self.assertIs(payload["evaluate_pantheon_plus"], True)

    def test_streamlit_cloud_uses_public_endpoint_by_default(self) -> None:
        previous = os.environ.get(CLASS_ENDPOINT_ENV)
        os.environ.pop(CLASS_ENDPOINT_ENV, None)
        try:
            self.assertEqual(resolve_class_endpoint(), PUBLIC_CLASS_ENDPOINT)
        finally:
            if previous is not None:
                os.environ[CLASS_ENDPOINT_ENV] = previous

    def test_local_endpoint_can_be_selected_for_desktop_backend(self) -> None:
        previous = os.environ.get(CLASS_ENDPOINT_ENV)
        os.environ[CLASS_ENDPOINT_ENV] = LOCAL_CLASS_ENDPOINT
        try:
            self.assertEqual(resolve_class_endpoint(), LOCAL_CLASS_ENDPOINT)
        finally:
            if previous is None:
                os.environ.pop(CLASS_ENDPOINT_ENV, None)
            else:
                os.environ[CLASS_ENDPOINT_ENV] = previous

    def test_run_artifact_is_persisted_with_matching_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            previous = os.environ.get("DTI_RUN_ARTIFACT_DIR")
            os.environ["DTI_RUN_ARTIFACT_DIR"] = directory
            try:
                metadata = run_store.save_run_artifact(
                    route="class_compute",
                    request={"H0": 67.0},
                    response={"status": "ok"},
                )
                payload = json.loads(Path(metadata["path"]).read_text(encoding="utf-8"))
                self.assertEqual(payload["artifact_sha256"], metadata["artifact_sha256"])
                self.assertEqual(run_store.list_run_artifacts()[0]["status"], "ok")
                self.assertIn("reproducibility", payload)
            finally:
                if previous is None:
                    os.environ.pop("DTI_RUN_ARTIFACT_DIR", None)
                else:
                    os.environ["DTI_RUN_ARTIFACT_DIR"] = previous


if __name__ == "__main__":
    unittest.main()
