"""Graph gallery and migration-aware figure workspace."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd
import streamlit as st

from dti_ui_v1.components.desi_external_confirmation import (
    render_desi_evidence_chain,
)

from dti_ui_v1.components.jump_discontinuity_diagnostics import (
    render_jump_discontinuity_diagnostics,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


@st.cache_data(show_spinner=False)
def load_graph_ledger() -> pd.DataFrame:
    path = (
        _repo_root()
        / "graph_migration"
        / "GRAPH_MIGRATION_LEDGER.tsv"
    )

    if not path.is_file():
        return pd.DataFrame()

    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    return pd.DataFrame(rows)


def _render_graph_summary(ledger: pd.DataFrame) -> None:
    total = len(ledger)

    if total == 0:
        migrated = 0
        parity_ready = 0
        pending = 0
    else:
        migrated = int(
            ledger["migration_status"]
            .fillna("")
            .str.startswith("MIGRATED")
            .sum()
        )
        parity_ready = int(
            ledger["render_parity"]
            .fillna("")
            .str.contains("PARITY_READY")
            .sum()
        )
        pending = total - migrated

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Direct graph records", total)

    with col2:
        st.metric("Migrated", migrated)

    with col3:
        st.metric("Parity ready", parity_ready)

    with col4:
        st.metric("Pending", pending)


def render() -> None:
    st.title("Figures")
    st.caption(
        "Scientific graph gallery, profile views, and legacy migration index"
    )

    ledger = load_graph_ledger()
    _render_graph_summary(ledger)

    (
        gallery_tab,
        likelihood_tab,
        profile_tab,
        section8_tab,
        strategy_tab,
        jump_tab,
        audit_tab,
        inventory_tab,
    ) = st.tabs(
        (
            "Gallery",
            "Likelihood",
            "Profiles",
            "Section 8",
            "Strategy A/B",
            "Jump diagnostics",
            "Audit",
            "Inventory",
        )
    )

    with gallery_tab:
        st.subheader("Figure gallery")

        st.info(
            "Migrated figures will be collected here without removing "
            "their task-specific placements in Results."
        )

        if not ledger.empty:
            summary_columns = [
                column
                for column in (
                    "graph_id",
                    "scientific_role",
                    "target_page",
                    "target_tab",
                    "migration_status",
                    "render_parity",
                )
                if column in ledger.columns
            ]

            st.dataframe(
                ledger[summary_columns],
                use_container_width=True,
                hide_index=True,
            )

    with likelihood_tab:
        st.subheader("Likelihood figures")
        st.write(
            "The five source-locked Fixed-H0 BAO charts are currently "
            "available under Results → Likelihood."
        )

        if st.button(
            "Open Results",
            key="perfect_fit_figures_open_results",
        ):
            st.session_state[
                "perfect_fit_navigation_request"
            ] = "Results"
            st.rerun()

    with profile_tab:
        st.subheader("Profile figures")
        st.caption(
            "Profile curves, minima structure, basin response, and the "
            "81-grid diagnostic will be placed here."
        )

    with section8_tab:
        st.subheader("Section 8")
        st.caption(
            "The two source-bound Section 8 comparison charts are mapped "
            "and awaiting component migration."
        )

    with strategy_tab:
        st.subheader("Strategy A/B")
        st.caption(
            "Proxy, grid, basin, and matched-route figures will remain "
            "separate from fully computed scientific results."
        )

    with jump_tab:
        render_jump_discontinuity_diagnostics()

    with audit_tab:
        st.subheader("Audit figures")
        st.caption(
            "Source identity, repeatability, parity, and migration review "
            "visuals are collected here."
        )

        st.markdown("### DESI DR2 BAO evidence chain")
        render_desi_evidence_chain()

    with inventory_tab:
        st.subheader("Graph migration inventory")

        if ledger.empty:
            st.warning("Graph migration ledger is unavailable.")
        else:
            st.dataframe(
                ledger,
                use_container_width=True,
                hide_index=True,
            )
