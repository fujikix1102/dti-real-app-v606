import json
import tempfile
import unittest
from pathlib import Path

try:
    from dti_ui_v1.components.profile_library import (
        LIBRARY_PATH,
        SESSION_KEYS,
        apply_profile,
        load_profile_library,
    )
except ModuleNotFoundError:
    from profile_library import (
        LIBRARY_PATH,
        SESSION_KEYS,
        apply_profile,
        load_profile_library,
    )


class ProfileLibraryTests(unittest.TestCase):
    def test_installed_library_contract(self):
        profiles = load_profile_library(LIBRARY_PATH)
        self.assertGreaterEqual(len(profiles), 4)
        self.assertEqual(set(profiles[0]["parameters"]), set(SESSION_KEYS))

    def test_apply_sets_only_declared_compute_keys_and_provenance(self):
        profile = load_profile_library(LIBRARY_PATH)[0]
        state = {}
        apply_profile(profile, state)
        for key in SESSION_KEYS.values():
            self.assertIn(key, state)
        self.assertEqual(state["active_cosmology_profile_id_v1"], profile["id"])

    def test_rejects_incomplete_profile(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps({"profiles": [{"id": "x", "parameters": {"H0": 1}}]}))
            with self.assertRaises(ValueError):
                load_profile_library(path)


if __name__ == "__main__":
    unittest.main()
