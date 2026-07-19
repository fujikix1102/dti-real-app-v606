from __future__ import annotations

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from dti_ui_v1.components.jump_discontinuity_diagnostics import render_jump_discontinuity_diagnostics


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


@st.cache_data(show_spinner=False)
def _tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t") if path.is_file() else pd.DataFrame()


def render() -> None:
    st.title("Figures")
    st.caption("Live solver plots and source-locked diagnostic figures")
    cmb, section8, grid, toy, inventory = st.tabs(
        ("Live CMB", "Section 8", "81-grid", "Experimental sandbox", "Inventory")
    )
    with cmb:
        st.info("Current and previous CLASS/AxiCLASS spectra are rendered in Results and Compare from actual backend arrays.")
    with section8:
        primary = _tsv(_root() / "data/section8_source_record/section8_primary_comparison_graph_normalized.tsv")
        secondary = _tsv(_root() / "data/section8_source_record/section8_secondary_summary_panel_normalized.tsv")
        st.warning("Source-locked descriptive diagnostic; not a likelihood, posterior, or new numerical adoption.")
        if primary.empty:
            st.error("Section 8 source record is missing.")
        else:
            plot = primary.groupby("x_label", as_index=False)["abs_delta_value"].max()
            chart = alt.Chart(plot).mark_bar().encode(
                x=alt.X("x_label:N", title="Recorded field", sort="-y"),
                y=alt.Y("abs_delta_value:Q", title="Maximum absolute recorded delta"),
                tooltip=["x_label:N", alt.Tooltip("abs_delta_value:Q", format=".8g")],
            ).properties(height=380)
            st.altair_chart(chart, use_container_width=True)
            st.dataframe(primary, hide_index=True, use_container_width=True)
        if not secondary.empty:
            st.markdown("**Secondary source summary**")
            st.dataframe(secondary, hide_index=True, use_container_width=True)
    with grid:
        data = _tsv(_root() / "data/strategy_ab_bao_2x2_diagnostic_81_grid_source_v1.tsv")
        st.warning("Frozen 2x2 BAO diagnostic surface only; not the full DESI likelihood or posterior.")
        if data.empty:
            st.error("81-grid source record is missing.")
        else:
            chart = alt.Chart(data).mark_rect().encode(
                x=alt.X("x_value:O", title="model DM/r_d"),
                y=alt.Y("y_value:O", title="model DH/r_d"),
                color=alt.Color("basin_value:Q", title="diagnostic chi-square", scale=alt.Scale(scheme="viridis")),
                tooltip=["x_value:Q", "y_value:Q", alt.Tooltip("basin_value:Q", format=".6f")],
            ).properties(height=520)
            st.altair_chart(chart, use_container_width=True)
            minimum = data.loc[data["basin_value"].idxmin()]
            st.dataframe(pd.DataFrame([minimum]), hide_index=True, use_container_width=True)
    with toy:
        st.warning("Isolated mathematical sandbox. It is intentionally separated from the evidence-bearing AxiCLASS and likelihood results.")
        render_jump_discontinuity_diagnostics()
    with inventory:
        ledger = _tsv(_root() / "graph_migration/GRAPH_MIGRATION_LEDGER.tsv")
        if ledger.empty:
            st.error("Graph migration ledger is missing.")
        else:
            st.metric("Graph records", len(ledger))
            st.dataframe(ledger, hide_index=True, use_container_width=True)
