import ast
import unittest
from pathlib import Path


TARGET = Path(
    "dti_ui_v1/components/general_class_compute_panel.py"
)


class GeneralClassSolverBoundaryTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tree = ast.parse(TARGET.read_text())
        cls.strings = [
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant)
            and isinstance(node.value, str)
        ]

    def test_solver_forward_propagation_present(self):
        text = "\n".join(self.strings)
        self.assertIn(
            "CLASS/AxiCLASS forward propagation",
            text
        )

    def test_likelihood_overclaim_absent(self):
        text = "\n".join(self.strings)
        self.assertNotIn(
            "evaluates verified DESI DR2 BAO, Planck 2018, and Pantheon+ likelihood components",
            text
        )

    def test_posterior_boundary_present(self):
        text = "\n".join(self.strings)
        self.assertIn(
            "posterior inference",
            text
        )

    def test_solver_only_boundary_present(self):
        text = "\n".join(self.strings)
        self.assertIn(
            "deterministic solver",
            text
        )


if __name__ == "__main__":
    unittest.main()
