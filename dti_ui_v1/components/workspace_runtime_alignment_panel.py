from __future__ import annotations

import streamlit as st


def render_workspace_runtime_alignment_panel() -> None:
    st.subheader("DTI PERFECT FIT Workspace Runtime")

    st.info(
        "This workspace view represents the deployed Streamlit runtime. "
        "The public runtime and the local development workspace are separate "
        "filesystem environments."
    )

    st.markdown("### Public runtime includes")

    st.table(
        [{"item": item} for item in (
            "Runtime status",
            "Artifact viewer",
            "Evidence display",
            "Diagnostic display",
        )]
    )

    st.markdown("### Local-only items")

    st.table(
        [{"item": item} for item in (
            "Development backups",
            "Review archives",
            "Freeze packages",
            "Temporary patch records",
        )]
    )

    st.warning(
        "Public runtime storage is not automatically synchronized with "
        "the local checkout. Local files are not expected to appear here."
    )
