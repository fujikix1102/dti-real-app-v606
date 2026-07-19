"""Static tests for the Streamlit-to-compute-service binding."""

from __future__ import annotations

import ast
from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

RUN_PAGE = (
    REPOSITORY_ROOT
    / "dti_ui_v1"
    / "pages"
    / "run.py"
)

PANEL = (
    REPOSITORY_ROOT
    / "dti_ui_v1"
    / "components"
    / "perfect_fit_compute_panel.py"
)


def _tree(path: Path) -> ast.Module:
    return ast.parse(
        path.read_text(encoding="utf-8"),
        filename=str(path),
    )


def _call_names(tree: ast.AST) -> list[str]:
    names: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        if isinstance(node.func, ast.Name):
            names.append(node.func.id)

        elif isinstance(node.func, ast.Attribute):
            names.append(node.func.attr)

    return names


class PerfectFitStreamlitComputeBindingTests(
    unittest.TestCase
):
    def test_run_page_renders_compute_panel(self) -> None:
        tree = _tree(RUN_PAGE)

        imported = False

        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue

            if (
                node.module
                == "dti_ui_v1.components."
                "perfect_fit_compute_panel"
                and any(
                    alias.name
                    == "render_perfect_fit_compute_panel"
                    for alias in node.names
                )
            ):
                imported = True

        self.assertTrue(imported)
        self.assertIn(
            "render_perfect_fit_compute_panel",
            _call_names(tree),
        )

    def test_panel_calls_compute_service_directly(
        self,
    ) -> None:
        tree = _tree(PANEL)

        imported = False

        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue

            if (
                node.module
                == "dti_ui_v1.services."
                "perfect_fit_compute_service"
                and any(
                    alias.name == "compute_perfect_fit"
                    for alias in node.names
                )
            ):
                imported = True

        self.assertTrue(imported)
        self.assertIn(
            "compute_perfect_fit",
            _call_names(tree),
        )

    def test_panel_builds_only_locked_baseline_request(
        self,
    ) -> None:
        tree = _tree(PANEL)

        request_calls = [
            node
            for node in ast.walk(tree)
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "LockedBaselineRequest"
            )
        ]

        self.assertEqual(len(request_calls), 1)

        keywords = {
            keyword.arg: keyword.value
            for keyword in request_calls[0].keywords
            if keyword.arg is not None
        }

        self.assertEqual(
            set(keywords),
            {
                "use_locked_baseline",
                "timeout_seconds",
                "f_EDE",
                "z_c",
            },
        )

        use_locked = keywords["use_locked_baseline"]
        f_ede = keywords["f_EDE"]
        z_c = keywords["z_c"]

        self.assertIsInstance(use_locked, ast.Constant)
        self.assertIs(use_locked.value, True)

        self.assertIsInstance(f_ede, ast.Constant)
        self.assertEqual(f_ede.value, 0.0)

        self.assertIsInstance(z_c, ast.Constant)
        self.assertIsNone(z_c.value)

    def test_transport_is_not_exposed_by_ui(
        self,
    ) -> None:
        source = PANEL.read_text(encoding="utf-8")
        tree = _tree(PANEL)

        compute_calls = [
            node
            for node in ast.walk(tree)
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "compute_perfect_fit"
            )
        ]

        self.assertEqual(len(compute_calls), 1)

        keyword_names = {
            keyword.arg
            for keyword in compute_calls[0].keywords
        }

        self.assertEqual(
            keyword_names,
            {"request"},
        )

        self.assertNotIn(
            "transport=",
            source,
        )


if __name__ == "__main__":
    unittest.main()
