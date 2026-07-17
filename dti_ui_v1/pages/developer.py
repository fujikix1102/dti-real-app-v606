"""Developer surface for the PERFECT FIT APP."""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st


def render() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    st.title("Developer")
    st.caption("Implementation and migration details")

    runtime_tab, architecture_tab, legacy_tab = st.tabs(
        (
            "Runtime",
            "Architecture",
            "Legacy parity",
        )
    )

    with runtime_tab:
        st.code(
            "\n".join(
                [
                    f"repository={repo_root}",
                    "entrypoint=perfect_fit_app.py",
                    "protected_legacy_entrypoint=app.py",
                    f"mode={os.environ.get('DTI_PERFECT_FIT_MODE', 'perfect-fit')}",
                    "backend_change=NO",
                    "physical_compute=NO",
                    "public_deploy=NO",
                ]
            ),
            language="text",
        )

    with architecture_tab:
        st.dataframe(
            [
                {
                    "Layer": "pages",
                    "Responsibility": "Task-level screen composition",
                },
                {
                    "Layer": "components",
                    "Responsibility": "Reusable presentation elements",
                },
                {
                    "Layer": "services",
                    "Responsibility": "Backend and response boundaries",
                },
                {
                    "Layer": "contracts",
                    "Responsibility": "Display and request contracts",
                },
                {
                    "Layer": "app_shell",
                    "Responsibility": "Navigation and dispatch",
                },
            ],
            width="stretch",
            hide_index=True,
        )

    with legacy_tab:
        st.markdown("#### Exact legacy route")

        st.code(
            "DTI_PERFECT_FIT_MODE=legacy "
            "streamlit run perfect_fit_app.py",
            language="bash",
        )

        st.warning(
            "Legacy mode is retained for parity comparison. It is not the "
            "target information architecture."
        )
