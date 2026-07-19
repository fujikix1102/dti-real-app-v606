from __future__ import annotations

import unittest
import json
from pathlib import Path

import numpy as np

from run_dti_catalog_pipeline_pilot import (
    LAYOUT,
    _compressed_vector,
    apply_coordinate_injection,
    expansion_ratios,
    resource_audit,
)


class CatalogPipelinePilotTests(unittest.TestCase):
    def test_zero_injection_is_identity(self) -> None:
        z = np.asarray([0.295, 0.51, 0.934, 2.33])
        parallel, perpendicular = expansion_ratios(
            z, amplitude=0.0, z_transition=0.934, width=0.03
        )
        np.testing.assert_allclose(parallel, 1.0, atol=1e-12)
        np.testing.assert_allclose(perpendicular, 1.0, atol=1e-12)

    def test_coordinate_injection_has_declared_axes(self) -> None:
        points = np.asarray([[300.0, 500.0, 600.0], [500.0, 300.0, 200.0]])
        transformed = apply_coordinate_injection(
            points,
            alpha_perpendicular=0.95,
            alpha_parallel=0.90,
            box_size=800.0,
        )
        np.testing.assert_allclose(transformed[0], [305.0, 495.0, 580.0])
        np.testing.assert_allclose(transformed[1], [495.0, 305.0, 220.0])

    def test_13_value_compression_is_identity_at_unit_dilation(self) -> None:
        baseline = np.arange(1.0, 14.0)
        alpha = {
            name: (1.0, 1.0) for name in dict.fromkeys(row["name"] for row in LAYOUT)
        }
        np.testing.assert_allclose(_compressed_vector(baseline, alpha), baseline)

    def test_resource_audit_never_claims_production_without_mock(self) -> None:
        audit = resource_audit()
        if not audit["declared_mock_catalog_exists"]:
            self.assertFalse(audit["production_mode_available"])

    def test_executed_summary_is_complete_and_bounded(self) -> None:
        root = Path(__file__).resolve().parent
        candidates = (
            root / "dti_catalog_pipeline_pilot_summary.json",
            root.parent / "data" / "research" / "dti_catalog_pipeline_pilot_summary.json",
        )
        path = next((candidate for candidate in candidates if candidate.is_file()), None)
        self.assertIsNotNone(path)
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(result["status"], "complete")
        self.assertFalse(result["production_equivalent"])
        self.assertEqual(result["condition_count"], 3)
        self.assertEqual(result["execution_totals"]["correlation_functions"], 672)
        self.assertEqual(result["execution_totals"]["bao_template_fits"], 84)
        self.assertEqual(
            [row["fractional_H_step"] for row in result["conditions"]],
            [0.05, 0.10, 0.20],
        )


if __name__ == "__main__":
    unittest.main()
