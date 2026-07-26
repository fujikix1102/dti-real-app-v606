from __future__ import annotations

import os
import unittest
from pathlib import Path

from dti_ui_v1.services.v606_profile_adapter import (
    DIRECT_PARAMETER_FIELDS,
    OPTIONAL_UNBOUND_FIELDS,
    REFERENCE_OUTPUT_FIELDS,
    load_v606_profile_library,
)


class V606ProfileAdapterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        source = os.environ.get("V606_PROFILE_ARCHIVE")
        expected_sha = os.environ.get("V606_PROFILE_ARCHIVE_SHA256")

        if not source:
            raise RuntimeError("V606_PROFILE_ARCHIVE is not set")

        if not expected_sha:
            raise RuntimeError("V606_PROFILE_ARCHIVE_SHA256 is not set")

        cls.library = load_v606_profile_library(
            Path(source),
            expected_sha256=expected_sha,
            expected_count=100,
        )

    def test_profile_count(self) -> None:
        self.assertEqual(len(self.library.profiles), 100)

    def test_profile_ids_are_unique(self) -> None:
        ids = self.library.profile_ids()
        self.assertEqual(len(ids), len(set(ids)))

    def test_direct_parameter_contract(self) -> None:
        for profile in self.library.profiles:
            self.assertEqual(
                tuple(profile.parameters.keys()),
                DIRECT_PARAMETER_FIELDS,
            )

    def test_reference_outputs_are_separate(self) -> None:
        for profile in self.library.profiles:
            self.assertEqual(
                tuple(profile.reference_outputs.keys()),
                REFERENCE_OUTPUT_FIELDS,
            )
            self.assertNotIn("sigma8", profile.parameters)
            self.assertNotIn("S8", profile.parameters)

    def test_z_c_is_unbound(self) -> None:
        for profile in self.library.profiles:
            self.assertEqual(
                profile.optional_unbound,
                OPTIONAL_UNBOUND_FIELDS,
            )
            self.assertNotIn("z_c", profile.parameters)

    def test_known_first_profile(self) -> None:
        profile = self.library.by_id("Planck_2018_LCDM_Base")
        self.assertEqual(profile.parameters["H0"], "67.36")
        self.assertEqual(profile.parameters["f_EDE"], "0.000")
        self.assertEqual(profile.category, "baseline reference")


if __name__ == "__main__":
    unittest.main()
