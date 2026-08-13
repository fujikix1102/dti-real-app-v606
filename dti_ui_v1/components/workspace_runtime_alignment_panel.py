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

    st.markdown(
        "- Runtime status\n"
        "- Artifact viewer\n"
        "- Evidence display\n"
        "- Diagnostic display"
    )

    st.markdown("### Local-only items")

    st.markdown(
        "- Development backups\n"
        "- Review archives\n"
        "- Freeze packages\n"
        "- Temporary patch records"
    )

    st.warning(
        "Public runtime storage is not automatically synchronized with "
        "the local checkout. Local files are not expected to appear here."
    )
