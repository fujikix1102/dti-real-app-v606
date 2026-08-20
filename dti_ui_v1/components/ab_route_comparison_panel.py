from __future__ import annotations

import streamlit as st


def render_ab_route_comparison_panel():
    st.subheader("Saved artifact type comparison")
    st.caption(
        "Compares the two saved artifact categories shown in this app. "
        "This is a display contract, not a model ranking."
    )

    table = [
        {
            "Field": "Route A",
            "Value": "Locked baseline reference artifact",
        },
        {
            "Field": "Route B",
            "Value": "Single deterministic CLASS/AxiCLASS run artifact",
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
            "Value": "artifact type comparison only",
        },
    ]

    st.table(table)

    st.info(
        "Contract comparison only. "
        "No recomputation, likelihood inference, "
        "posterior interpretation, or model ranking."
    )
