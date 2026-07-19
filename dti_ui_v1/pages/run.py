"""Scientific computation page with live route contracts."""

from __future__ import annotations

import streamlit as st

from dti_ui_v1.components.execution_status import render_execution_status
from dti_ui_v1.components.general_class_compute_panel import (
    render_general_class_compute_panel,
)
from dti_ui_v1.components.general_class_profile_panel import render_general_class_profile_panel
from dti_ui_v1.components.monitor_status import render_monitor_status
from dti_ui_v1.components.parameter_status import render_parameter_status_panel
from dti_ui_v1.components.perfect_fit_compute_panel import (
    render_perfect_fit_compute_panel,
)
from dti_ui_v1.components.precision_reference import render_precision_reference
from dti_ui_v1.components.profile_library import render_profile_library


def render() -> None:
    st.title("Compute")
    st.caption("Junichi Fujiki · jun@fujikix.com")
    st.caption("Scientific configuration, execution, and monitoring")

    setup_tab, parameters_tab, execution_tab, monitor_tab = st.tabs(
        ("Configuration", "Parameters", "Execution", "Monitor")
    )

    with setup_tab:
        render_precision_reference()
        st.divider()
        st.subheader("Available calculation routes")
        st.dataframe(
            [
                {
                    "Route": "Locked baseline DESI DR2 BAO",
                    "State": "AVAILABLE — FIXED BASELINE",
                    "Editable physics": "No",
                    "Likelihood": "Fixed DESI DR2 BAO component",
                },
                {
                    "Route": "General CLASS / AxiCLASS",
                    "State": "AVAILABLE WHEN LOCAL BACKEND IS ONLINE",
                    "Editable physics": "6 LCDM-like + f_EDE + z_c",
                    "Likelihood": "DESI DR2 BAO + Planck 2018 + Pantheon+",
                },
                {
                    "Route": "Hubble Consistency Engine",
                    "State": "AVAILABLE AFTER A GENERAL RUN",
                    "Editable physics": "Uses the submitted H0",
                    "Likelihood": "Published ladder summary is comparison-only",
                },
            ],
            hide_index=True,
            use_container_width=True,
        )
        st.info(
            "Both routes evaluate DESI DR2 BAO under different contracts. "
            "The general route additionally evaluates verified Planck 2018 and "
            "Pantheon+ single-point likelihoods. Neither route performs posterior "
            "inference or MCMC. Local ladder summaries are never added to the Pantheon+ joint sum."
        )

    with parameters_tab:
        render_parameter_status_panel()

    with execution_tab:
        render_execution_status()
        st.divider()
        render_perfect_fit_compute_panel()
        st.divider()
        render_profile_library()
        st.divider()
        render_general_class_compute_panel()
        st.divider()
        render_general_class_profile_panel()

    with monitor_tab:
        render_monitor_status()
