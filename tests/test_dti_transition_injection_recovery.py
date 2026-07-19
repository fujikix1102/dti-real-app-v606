from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np

from run_dti_transition_injection_recovery import expansion_ratios, transition_profile


class TransitionInjectionRecoveryTests(unittest.TestCase):
    def test_zero_transition_is_identity(self) -> None:
        z = np.linspace(0.001, 3.0, 2000)
        dh, dm = expansion_ratios(z, np.zeros_like(z))
        self.assertLess(float(np.max(np.abs(dh - 1.0))), 1e-14)
        self.assertLess(float(np.max(np.abs(dm - 1.0))), 1e-14)

    def test_hubble_step_changes_dh_and_keeps_dm_continuous(self) -> None:
        z = np.linspace(0.001, 3.0, 6000)
        profile = transition_profile(z, 0.02, 1.0, 0.005)
        dh, dm = expansion_ratios(z, profile)
        self.assertLess(float(dh[-1]), 1.0)
        self.assertLess(float(dm[-1]), 1.0)
        self.assertLess(float(np.max(np.abs(np.diff(dm)))), 0.001)

    def test_sharp_transition_reaches_requested_amplitude(self) -> None:
        z = np.linspace(0.0, 2.0, 2001)
        profile = transition_profile(z, 0.05, 1.0, 0.01)
        self.assertLess(float(profile[0]), 1e-6)
        self.assertAlmostEqual(float(profile[-1]), 0.05, places=6)

    def test_published_artifact_has_complete_seeded_ensemble(self) -> None:
        root = Path(__file__).resolve().parent
        candidates = (
            root / "dti_transition_injection_recovery.json",
            root.parent / "data" / "research" / "dti_transition_injection_recovery.json",
        )
        artifact_path = next((path for path in candidates if path.is_file()), None)
        self.assertIsNotNone(artifact_path)
        result = json.loads(artifact_path.read_text(encoding="utf-8"))
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["calibration"]["null_replicates"], 10_000)
        self.assertEqual(result["calibration"]["scenario_replicates"], 1_000)
        self.assertEqual(len(result["scenarios"]), 72)
        self.assertEqual(sum(row["replicates"] for row in result["scenarios"]), 72_000)


if __name__ == "__main__":
    unittest.main()
