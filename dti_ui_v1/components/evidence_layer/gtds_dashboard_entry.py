import streamlit as st

from .gtds_evidence_router import render_gtds_evidence_router


def render_gtds_dashboard_entry():

    st.subheader(
        "DTI Evidence Layer"
    )

    st.caption(
        "Diagnostic evidence registry only. "
        "No posterior inference. "
        "No detection claim."
    )

    render_gtds_evidence_router()
