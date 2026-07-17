"""Advanced scientific result analysis page."""

from __future__ import annotations

import streamlit as st

from dti_ui_v1.components.desi_external_confirmation import (
    render_desi_external_confirmation,
)


from dti_ui_v1.components.value_formatting import (
    format_contract_value,
)

from dti_ui_v1.components.fixed_h0_bao_charts import (
    render_fixed_h0_bao_charts,
)
from dti_ui_v1.contracts.display_contract import RESULT_TABS


def _render_overview() -> None:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "H0",
            format_contract_value("H0"),
        )

    with col2:
        st.metric(
            "Model χ²",
            format_contract_value(
                "model_chi2",
                source_precision=True,
            ),
        )

    with col3:
        st.metric(
            "Model log-likelihood",
            format_contract_value(
                "model_loglike",
                source_precision=True,
            ),
        )

    with col4:
        st.metric("CMB χ²", "—")

    st.info("No active calculation result is loaded.")

    st.markdown("### Result identity")

    st.dataframe(
        [
            {
                "Item": "Run",
                "Value": "None",
            },
            {
                "Item": "Preset",
                "Value": "None",
            },
            {
                "Item": "Model family",
                "Value": "None",
            },
            {
                "Item": "Source status",
                "Value": "No active result",
            },
        ],
        width="stretch",
        hide_index=True,
    )


def _render_fit() -> None:
    st.subheader("Fit")

    parameter_tab, residual_tab, components_tab = st.tabs(
        (
            "Parameters",
            "Residuals",
            "Components",
        )
    )

    with parameter_tab:
        st.caption(
            "Best-fit, fixed, nuisance, derived, and custom values "
            "will be shown here."
        )

    with residual_tab:
        st.caption(
            "Residual structure and observation-to-model differences "
            "will be shown here."
        )

    with components_tab:
        st.caption(
            "Fit contribution tables and component-level summaries "
            "will be shown here."
        )


def _render_profiles() -> None:
    st.subheader("Profiles")

    profile_tab, minima_tab, basin_tab, grid_tab = st.tabs(
        (
            "Profile curves",
            "Minima",
            "Basins",
            "Grid",
        )
    )

    with profile_tab:
        st.caption(
            "One- and multi-parameter profile curves will be shown here."
        )

    with minima_tab:
        st.caption(
            "Recorded minima, repeated starts, and minimum-spread "
            "diagnostics will be shown here."
        )

    with basin_tab:
        st.caption(
            "Basin structure and branch-dependent response will be "
            "shown here."
        )

    with grid_tab:
        st.caption(
            "The mapped 81-grid parameter-space diagnostic will be "
            "migrated here."
        )


def _render_diagnostics() -> None:
    st.subheader("Diagnostics")

    stability_tab, convergence_tab, backend_tab, source_tab = st.tabs(
        (
            "Stability",
            "Convergence",
            "Backend",
            "Source",
        )
    )

    with stability_tab:
        st.caption(
            "Seed recurrence, repeated starts, and stability checks "
            "will be shown here."
        )

    with convergence_tab:
        st.caption(
            "Optimizer state and convergence diagnostics will be "
            "shown here."
        )

    with backend_tab:
        st.caption(
            "Execution contract and backend response status will be "
            "shown here."
        )

    with source_tab:
        render_desi_external_confirmation(compact=True)


def _render_charts() -> None:
    st.subheader("Charts")

    st.info(
        "The graph gallery is available from the main Figures page. "
        "Task-specific charts remain embedded in the relevant result tabs."
    )


def _render_raw() -> None:
    st.subheader("Raw")

    response_tab, tables_tab, config_tab = st.tabs(
        (
            "Response",
            "Tables",
            "Configuration",
        )
    )

    with response_tab:
        st.code("No backend response loaded.", language="text")

    with tables_tab:
        st.caption("No raw result tables are loaded.")

    with config_tab:
        st.code("No run configuration loaded.", language="text")


def render() -> None:
    st.title("Results")
    st.caption(
        "Scientific outputs, fit structure, profiles, and diagnostics"
    )

    (
        overview_tab,
        fit_tab,
        likelihood_tab,
        profiles_tab,
        diagnostics_tab,
        charts_tab,
        raw_tab,
    ) = st.tabs(RESULT_TABS)

    with overview_tab:
        _render_overview()

    with fit_tab:
        _render_fit()

    with likelihood_tab:
        render_fixed_h0_bao_charts()

    with profiles_tab:
        _render_profiles()

    with diagnostics_tab:
        _render_diagnostics()

    with charts_tab:
        _render_charts()

    with raw_tab:
        _render_raw()
