from __future__ import annotations

import streamlit as st


def render_ab_route_comparison_panel():
    st.subheader("A/B Route Contract Comparison")

    table = [
        {
            "Field": "Route A",
            "Value": "LOCKED_BASELINE_EXECUTION_ARTIFACT_FREEZE_V1",
        },
        {
            "Field": "Route B",
            "Value": "GENERAL_CLASS_AXICLASS_SINGLE_POINT_ARTIFACT_FREEZE_V1",
        },
        {
            "Field": "Execution",
            "Value": "single point",
        },
        {
            "Field": "Posterior",
            "Value": "NO",
        },
        {
            "Field": "MCMC",
            "Value": "NO",
        },
        {
            "Field": "Claim",
            "Value": "artifact/capability comparison only",
        },
    ]

    st.table(table)

    st.info(
        "Contract comparison only. "
        "No recomputation, likelihood inference, "
        "posterior interpretation, or model ranking."
    )
