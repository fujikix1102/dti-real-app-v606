"""Scientific workspace landing page."""

from __future__ import annotations

import streamlit as st

from dti_ui_v1.components.status_cards import (
    StatusItem,
    render_status_row,
)
from dti_ui_v1.contracts.display_contract import WORKSPACE_MODES


def render() -> None:
    st.title("MAXOMEGA / DTI")
    st.caption("Scientific computation and diagnostic workbench")

    render_status_row(
        (
            StatusItem("Backend", "Locked"),
            StatusItem("Compute engine", "Preserved"),
            StatusItem("Active task", "None"),
            StatusItem("Environment", "Local clone"),
        )
    )

    st.markdown("## Scientific workspace")

    selected_mode = st.selectbox(
        "Workspace mode",
        options=WORKSPACE_MODES,
        index=0,
        key="perfect_fit_workspace_mode",
    )

    mode_descriptions = {
        "Scientific computation": (
            "Configure and execute supported model calculations using the "
            "existing scientific backend."
        ),
        "Branch comparison": (
            "Compare fixed-H0 branches, configurations, likelihood components, "
            "and derived diagnostics."
        ),
        "Profile analysis": (
            "Inspect parameter scans, profile structure, minima, and "
            "branch-dependent response."
        ),
        "Diagnostic audit": (
            "Review convergence, seed stability, source identity, response "
            "integrity, and calculation boundaries."
        ),
    }

    st.write(mode_descriptions[selected_mode])

    col_compute, col_compare, col_results, col_audit = st.columns(4)

    with col_compute:
        with st.container(border=True):
            st.subheader("Compute")
            st.write("Configure scientific inputs and run supported calculations.")
            st.caption("Advanced settings remain available.")

    with col_compare:
        with st.container(border=True):
            st.subheader("Compare")
            st.write("Evaluate branches, models, and likelihood contributions.")
            st.caption("Matched comparisons and profiles.")

    with col_results:
        with st.container(border=True):
            st.subheader("Analyze")
            st.write("Inspect tables, plots, minima, and derived diagnostics.")
            st.caption("Summary and full-detail views.")

    with col_audit:
        with st.container(border=True):
            st.subheader("Audit")
            st.write("Verify provenance, stability, contracts, and raw outputs.")
            st.caption("Evidence remains traceable.")

    st.markdown("## Session workspace")

    left, right = st.columns((2, 1))

    with left:
        st.dataframe(
            [
                {
                    "Task": "Selected mode",
                    "Value": selected_mode,
                },
                {
                    "Task": "Active configuration",
                    "Value": "Not loaded",
                },
                {
                    "Task": "Current execution",
                    "Value": "Idle",
                },
                {
                    "Task": "Loaded result",
                    "Value": "None",
                },
            ],
            use_container_width=True,
            hide_index=True,
        )

    with right:
        with st.container(border=True):
            st.subheader("Calculation status")
            st.metric("Queue", "0")
            st.metric("Completed", "0")
            st.metric("Failed", "0")

    st.markdown("## Capability areas")

    st.dataframe(
        [
            {
                "Area": "Model configuration",
                "Purpose": "Scientific and nuisance parameter setup",
                "Migration": "Source mapping required",
            },
            {
                "Area": "Backend execution",
                "Purpose": "Locked scientific calculation",
                "Migration": "Client module available",
            },
            {
                "Area": "Branch analysis",
                "Purpose": "Fixed-H0 and matched-condition comparison",
                "Migration": "Pending structured migration",
            },
            {
                "Area": "Profile diagnostics",
                "Purpose": "Minima, scans, likelihood components",
                "Migration": "Pending structured migration",
            },
            {
                "Area": "Evidence audit",
                "Purpose": "Sources, hashes, raw responses, boundaries",
                "Migration": "Framework available",
            },
        ],
        use_container_width=True,
        hide_index=True,
    )
