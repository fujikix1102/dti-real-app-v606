from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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


if __name__ == "__main__":
    unittest.main()
