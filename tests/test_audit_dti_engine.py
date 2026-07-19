from __future__ import annotations

import unittest

import numpy as np

try:
    from audit_dti_engine import gaussian_chi2, profile_grid, select_transition_model
except ImportError:
    from dti_ui_v1.services.audit_dti_engine import gaussian_chi2, profile_grid, select_transition_model


class AuditDtiEngineTests(unittest.TestCase):
    def test_gaussian_chi2(self) -> None:
        theory = np.asarray([[1.0, 2.0], [2.0, 4.0]])
        observed = np.asarray([1.0, 1.0])
        precision = np.eye(2)
        np.testing.assert_allclose(gaussian_chi2(theory, observed, precision), [1.0, 10.0])

    def test_profile_grid(self) -> None:
        values, f_ede, indices = profile_grid(
            np.asarray([[3.0, 1.0], [0.5, 2.0]]), np.asarray([0.0, 0.1])
        )
        np.testing.assert_allclose(values, [1.0, 0.5])
        np.testing.assert_allclose(f_ede, [0.1, 0.0])
        np.testing.assert_array_equal(indices, [1, 0])

    def test_detects_strong_piecewise_regime(self) -> None:
        x = np.linspace(0.0, 10.0, 41)
        y = np.where(x < 5.0, 1.0, 9.0) + 0.01 * np.sin(x)
        result = select_transition_model(x, y)["best"]
        self.assertTrue(result["transition_selected"])
        self.assertIn(4.875, result["break_H0"])

    def test_smooth_quadratic_prefers_smooth_family(self) -> None:
        x = np.linspace(-2.0, 2.0, 49)
        y = 1.0 + 0.5 * x + 2.0 * x * x
        result = select_transition_model(x, y)["best"]
        self.assertEqual(result["family"], "smooth_polynomial")
        self.assertEqual(result["order"], 2)


if __name__ == "__main__":
    unittest.main()
