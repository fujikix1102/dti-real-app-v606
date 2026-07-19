from __future__ import annotations

import ast
from pathlib import Path
import unittest


PANEL_PATH = Path(
    "dti_ui_v1/components/general_class_compute_panel.py"
)


def _streamlit_texts() -> list[tuple[str, str]]:
    source = PANEL_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    results: list[tuple[str, str]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        func = node.func

        if not (
            isinstance(func, ast.Attribute)
            and isinstance(func.value, ast.Name)
            and func.value.id == "st"
        ):
            continue

        parts: list[str] = []

        for argument in node.args:
            if (
                isinstance(argument, ast.Constant)
                and isinstance(argument.value, str)
            ):
                parts.append(argument.value)

        if parts:
            results.append((func.attr, "".join(parts)))

    return results


class GeneralClassPublicBackendBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.calls = _streamlit_texts()
        cls.visible_text = "\n".join(
            text
            for _method, text in cls.calls
        )

    def test_forward_propagation_contract(self) -> None:
        required = (
            "single-point CLASS/AxiCLASS forward propagation",
            "deployed minimal public backend",
            "deterministic solver-derived quantities and spectra",
            "does not return DESI DR2",
            "does not provide DESI DR2",
            "does not currently return DESI DR2",
        )

        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, self.visible_text)

    def test_scientific_claim_boundary(self) -> None:
        required = (
            "It is not a posterior sample",
            "parameter constraint",
            "Bayesian evidence",
            "EDE detection",
            "DTI detection",
            "does not run posterior inference or MCMC",
        )

        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, self.visible_text)

    def test_requested_inputs_are_explicit(self) -> None:
        self.assertIn("Requested f_EDE", self.visible_text)
        self.assertIn("Requested z_c", self.visible_text)

    def test_stale_likelihood_claims_are_absent(self) -> None:
        forbidden = (
            "single-point likelihood evaluation",
            "evaluates installed, source-identified DESI DR2 BAO",
            "same model against verified DESI DR2",
        )

        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, self.visible_text)

    def test_warning_is_near_execution_boundary(self) -> None:
        warnings = [
            text
            for method, text in self.calls
            if method == "warning"
        ]

        matching = [
            text
            for text in warnings
            if "posterior sample" in text
            and "Bayesian evidence" in text
            and "DTI detection" in text
        ]

        self.assertEqual(len(matching), 1)


if __name__ == "__main__":
    unittest.main()
