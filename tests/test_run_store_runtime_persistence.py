from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from dti_ui_v1.services import run_store


class RunStoreRuntimePersistenceTests(unittest.TestCase):
    def test_save_run_artifact_returns_runtime_store_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(
                os.environ,
                {"DTI_RUN_ARTIFACT_DIR": tmpdir},
                clear=False,
            ):
                saved = run_store.save_run_artifact(
                    route="locked_baseline_desi_dr2_bao",
                    request={"use_locked_baseline": True},
                    response={"status": "SUCCESS_LOCKED_BASELINE"},
                )

        self.assertEqual(
            saved["storage"]["persistence"],
            "local_or_configured_filesystem",
        )
        self.assertEqual(saved["artifact_count"], 1)
        self.assertTrue(Path(saved["path"]).name.endswith(".json"))

    def test_mount_src_store_is_marked_ephemeral(self) -> None:
        directory = Path("/mount/src/dti-real-app-v606/data/run_artifacts")

        context = run_store._storage_context(directory)

        self.assertEqual(
            context["persistence"],
            "ephemeral_streamlit_runtime",
        )
        self.assertFalse(context["durable_persistence_available"])

    def test_configured_durable_mirror_receives_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as runtime_dir:
            with tempfile.TemporaryDirectory() as durable_dir:
                with patch.dict(
                    os.environ,
                    {
                        "DTI_RUN_ARTIFACT_DIR": runtime_dir,
                        "DTI_DURABLE_ARTIFACT_DIR": durable_dir,
                    },
                    clear=False,
                ):
                    saved = run_store.save_run_artifact(
                        route="class_compute",
                        request={"H0": 73.1},
                        response={"status": "ok"},
                    )
                    manifest = run_store.build_run_manifest(
                        run_store.load_run_artifact(saved["path"])
                    )

                self.assertEqual(
                    saved["storage"]["persistence"],
                    "durable_mirror_configured",
                )
                self.assertIsNotNone(saved["durable_path"])
                self.assertTrue(Path(saved["path"]).is_file())
                self.assertTrue(Path(saved["durable_path"]).is_file())
                self.assertTrue(manifest["durable_storage"]["configured"])
                self.assertEqual(
                    manifest["durable_storage"]["artifact_directory"],
                    str(Path(durable_dir).resolve()),
                )

    def test_r2_external_storage_is_inactive_without_complete_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(
                os.environ,
                {
                    "DTI_RUN_ARTIFACT_DIR": tmpdir,
                    "DTI_EXTERNAL_STORAGE_BACKEND": "r2",
                    "R2_BUCKET": "dti-perfect-fit-artifacts",
                },
                clear=False,
            ):
                saved = run_store.save_run_artifact(
                    route="class_compute",
                    request={"H0": 73.1},
                    response={"status": "ok"},
                )

        self.assertFalse(saved["external_storage"]["configured"])
        self.assertEqual(saved["external_storage"]["uploads"], [])
        self.assertFalse(
            saved["storage"]["external_storage"]["configured"]
        )
        self.assertIn(
            "R2_ACCOUNT_ID",
            saved["storage"]["external_storage"]["missing"],
        )

    def test_r2_external_storage_uploads_artifact_and_latest_index(self) -> None:
        fake_get_response = Mock()
        fake_get_response.status_code = 404
        fake_get_response.headers = {}
        fake_get_response.raise_for_status.return_value = None
        fake_put_response = Mock()
        fake_put_response.status_code = 200
        fake_put_response.headers = {"ETag": '"abc"'}
        fake_put_response.raise_for_status.return_value = None

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(
                os.environ,
                {
                    "DTI_RUN_ARTIFACT_DIR": tmpdir,
                    "DTI_EXTERNAL_STORAGE_BACKEND": "r2",
                    "R2_ACCOUNT_ID": "account",
                    "R2_ACCESS_KEY_ID": "access",
                    "R2_SECRET_ACCESS_KEY": "secret",
                    "R2_BUCKET": "dti-perfect-fit-artifacts",
                    "R2_PREFIX": "research/dti",
                },
                clear=False,
            ):
                with patch(
                    "dti_ui_v1.services.run_store.requests.request",
                    side_effect=[fake_get_response, fake_put_response, fake_put_response, fake_put_response],
                ) as request:
                    saved = run_store.save_run_artifact(
                        route="class_compute",
                        request={"H0": 73.1},
                        response={"status": "ok"},
                    )

        self.assertTrue(saved["external_storage"]["configured"])
        self.assertEqual(saved["external_storage"]["backend"], "r2")
        self.assertEqual(len(saved["external_storage"]["uploads"]), 3)
        self.assertEqual(request.call_count, 4)
        uploaded_urls = [
            call.args[1]
            for call in request.call_args_list
            if call.args[0] == "PUT"
        ]
        self.assertTrue(
            any(url.endswith("/artifact.json") for url in uploaded_urls)
        )
        self.assertTrue(
            any(url.endswith("/research/dti/index/latest.json") for url in uploaded_urls)
        )
        self.assertTrue(
            any(url.endswith("/research/dti/index/runs_manifest.json") for url in uploaded_urls)
        )

    def test_r2_external_run_index_merges_existing_runs(self) -> None:
        fake_get_response = Mock()
        fake_get_response.status_code = 200
        fake_get_response.headers = {}
        fake_get_response.json.return_value = {
            "schema_version": "dti-r2-run-index-v1",
            "runs": [
                {
                    "run_id": "old_run",
                    "created_at_utc": "2026-08-20T00:00:00+00:00",
                    "artifact_key": "research/dti/runs/old/artifact.json",
                }
            ],
        }
        fake_get_response.raise_for_status.return_value = None
        fake_put_response = Mock()
        fake_put_response.status_code = 200
        fake_put_response.headers = {"ETag": '"abc"'}
        fake_put_response.raise_for_status.return_value = None

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(
                os.environ,
                {
                    "DTI_RUN_ARTIFACT_DIR": tmpdir,
                    "DTI_EXTERNAL_STORAGE_BACKEND": "r2",
                    "R2_ACCOUNT_ID": "account",
                    "R2_ACCESS_KEY_ID": "access",
                    "R2_SECRET_ACCESS_KEY": "secret",
                    "R2_BUCKET": "dti-perfect-fit-artifacts",
                    "R2_PREFIX": "research/dti",
                },
                clear=False,
            ):
                with patch(
                    "dti_ui_v1.services.run_store.requests.request",
                    side_effect=[fake_get_response, fake_put_response, fake_put_response, fake_put_response],
                ) as request:
                    saved = run_store.save_run_artifact(
                        route="class_compute",
                        request={"H0": 73.1},
                        response={"status": "ok"},
                    )

        self.assertTrue(saved["external_storage"]["configured"])
        index_call = request.call_args_list[-1]
        index_payload = index_call.kwargs["data"].decode("utf-8")
        self.assertIn("old_run", index_payload)
        self.assertIn(str(saved["run_id"]), index_payload)


if __name__ == "__main__":
    unittest.main()
