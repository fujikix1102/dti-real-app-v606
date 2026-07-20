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


def _arrow_safe_table_data(data):
    """Convert mixed object columns into deterministic Arrow-safe strings."""
    try:
        import pandas as pd
    except Exception:
        return data

    if not isinstance(data, pd.DataFrame):
        return data

    safe = data.copy()

    def normalize_display_value(value):
        if value is None or value is pd.NA:
            return None

        try:
            missing = pd.isna(value)
        except Exception:
            missing = False

        if isinstance(missing, bool) and missing:
            return None

        return str(value)

    for column in safe.columns:
        series = safe[column]

        if str(series.dtype) == "object":
            safe[column] = series.map(normalize_display_value)

    return safe


def _install_streamlit_arrow_compatibility() -> None:
    """Install display-only wrappers for Streamlit table rendering."""
    import streamlit as st

    if getattr(st, "_dti_arrow_compat_installed", False):
        return

    original_dataframe = st.dataframe
    original_table = st.table
    original_data_editor = getattr(st, "data_editor", None)

    def safe_dataframe(data=None, *args, **kwargs):
        return original_dataframe(
            _arrow_safe_table_data(data),
            *args,
            **kwargs,
        )

    def safe_table(data=None, *args, **kwargs):
        return original_table(
            _arrow_safe_table_data(data),
            *args,
            **kwargs,
        )

    def safe_data_editor(data=None, *args, **kwargs):
        if original_data_editor is None:
            raise AttributeError("streamlit.data_editor is unavailable")

        return original_data_editor(
            _arrow_safe_table_data(data),
            *args,
            **kwargs,
        )

    st.dataframe = safe_dataframe
    st.table = safe_table

    if original_data_editor is not None:
        st.data_editor = safe_data_editor

    st._dti_arrow_compat_installed = True


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
        _install_streamlit_arrow_compatibility()
        run_perfect_fit_app()


if __name__ == "__main__":
    main()
