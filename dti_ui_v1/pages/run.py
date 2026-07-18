"""Advanced scientific computation page."""

from __future__ import annotations

import streamlit as st

from dti_ui_v1.components.parameter_status import (
    render_parameter_status_panel,
)



from dti_ui_v1.components.execution_status import render_execution_status
from dti_ui_v1.components.monitor_status import render_monitor_status
from dti_ui_v1.components.perfect_fit_compute_panel import (
    render_perfect_fit_compute_panel,
)
from dti_ui_v1.components.precision_reference import (
    render_precision_reference,
)

def render() -> None:
    st.title("Compute")
    st.caption("Scientific configuration, execution, and monitoring")

    setup_tab, parameters_tab, execution_tab, monitor_tab = st.tabs(
        (
            "Configuration",
            "Parameters",
            "Execution",
            "Monitor",
        )
    )

    with setup_tab:
        render_precision_reference()
        st.divider()

        st.subheader("Calculation configuration")

        col1, col2 = st.columns(2)

        with col1:
            st.selectbox(
                "Calculation route",
                options=(
                    "Locked baseline diagnostic",
                    "Branch comparison",
                    "Profile evaluation",
                    "Source-faithful replay",
                ),
                key="perfect_fit_calculation_route",
            )

            st.selectbox(
                "Configuration source",
                options=(
                    "Locked application configuration",
                    "Saved local configuration",
                    "Imported configuration",
                ),
                key="perfect_fit_configuration_source",
            )

        with col2:
            st.text_input(
                "Run name",
                placeholder="Optional local identifier",
                key="perfect_fit_request_label",
            )

            st.selectbox(
                "Output detail",
                options=(
                    "Standard",
                    "Detailed diagnostics",
                    "Full raw and evidence output",
                ),
                index=1,
                key="perfect_fit_output_detail",
            )

        st.info(
            "Routes are visible now, but execution remains disabled until each "
            "legacy calculation path is mapped to its actual backend contract."
        )

    with parameters_tab:
        render_parameter_status_panel()


    with execution_tab:
        render_execution_status()
        st.divider()
        render_perfect_fit_compute_panel()


    with monitor_tab:
        render_monitor_status()
