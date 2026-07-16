"""Independent entry point for MAXOMEGA / DTI PERFECT FIT APP.

New task-first UI:
    streamlit run perfect_fit_app.py

Protected legacy parity route:
    DTI_PERFECT_FIT_MODE=legacy streamlit run perfect_fit_app.py
"""

from __future__ import annotations

import os
import runpy
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
LEGACY_APP = REPO_ROOT / "app.py"


def selected_mode() -> str:
    raw = os.environ.get("DTI_PERFECT_FIT_MODE", "perfect-fit")
    normalized = raw.strip().lower().replace("_", "-")

    if normalized in {"legacy", "legacy-parity", "parity"}:
        return "legacy"

    return "perfect-fit"


def run_legacy_app() -> None:
    if not LEGACY_APP.is_file():
        raise FileNotFoundError(
            f"Protected legacy app not found: {LEGACY_APP}"
        )

    runpy.run_path(str(LEGACY_APP), run_name="__main__")


def run_perfect_fit_app() -> None:
    from dti_ui_v1.app_shell import render_app

    render_app()


def main() -> None:
    if selected_mode() == "legacy":
        run_legacy_app()
    else:
        run_perfect_fit_app()


if __name__ == "__main__":
    main()
