"""Scientific comparison workspace."""

from __future__ import annotations

import streamlit as st

from dti_ui_v1.contracts.display_contract import COMPARE_SLOT_COUNT


COMPARISON_SOURCES: tuple[str, ...] = (
    "None",
    "Current result",
    "Saved session",
    "Locked reference",
    "Representative hypothesis preset",
    "DTI audited reference",
    "DTI latest just-fit",
    "Custom configuration",
)


def _render_slot(slot_number: int) -> None:
    with st.container(border=True):
        st.subheader(f"Slot {slot_number}")

        source = st.selectbox(
            "Source",
            options=COMPARISON_SOURCES,
            key=f"perfect_fit_compare_source_{slot_number}",
        )

        if source == "None":
            st.caption("No comparison object selected.")
            return

        st.selectbox(
            "Object",
            options=("Source mapping pending",),
            disabled=True,
            key=f"perfect_fit_compare_object_{slot_number}",
        )

        st.caption(
            "The object selector will be enabled after saved results, "
            "presets, and run identities are bound."
        )


def render() -> None:
    st.title("Compare")
    st.caption(
        "Side-by-side and overlaid comparison of runs, references, "
        "hypotheses, and DTI solutions"
    )

    setup_tab, metrics_tab, overlay_tab, differences_tab = st.tabs(
        (
            "Setup",
            "Metrics",
            "Overlay",
            "Differences",
        )
    )

    with setup_tab:
        st.subheader("Comparison set")

        first_row = st.columns(2)
        second_row = st.columns(2)
        slots = (*first_row, *second_row)

        for index, column in enumerate(
            slots,
            start=1,
        ):
            with column:
                _render_slot(index)

        assert len(slots) == COMPARE_SLOT_COUNT

        st.markdown("### Comparison controls")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.selectbox(
                "Alignment",
                options=(
                    "Exact parameter identity",
                    "Matched H0",
                    "Matched model family",
                    "Matched data configuration",
                ),
                key="perfect_fit_compare_alignment",
            )

        with col2:
            st.selectbox(
                "Reference",
                options=(
                    "Slot 1",
                    "Minimum χ²",
                    "DTI audited reference",
                    "Custom reference",
                ),
                key="perfect_fit_compare_reference",
            )

        with col3:
            st.multiselect(
                "Comparison layers",
                options=(
                    "Parameters",
                    "Likelihood components",
                    "Profiles",
                    "Diagnostics",
                    "Provenance",
                ),
                default=(
                    "Parameters",
                    "Likelihood components",
                ),
                key="perfect_fit_compare_layers",
            )

        st.button(
            "Build comparison",
            type="primary",
            disabled=True,
            help=(
                "Enabled after source objects and comparison contracts "
                "are fully mapped."
            ),
        )

    with metrics_tab:
        st.info("No comparison set has been built.")

        st.dataframe(
            [
                {
                    "Metric": "H0",
                    "Slot 1": "—",
                    "Slot 2": "—",
                    "Difference": "—",
                },
                {
                    "Metric": "Total χ²",
                    "Slot 1": "—",
                    "Slot 2": "—",
                    "Difference": "—",
                },
                {
                    "Metric": "BAO χ²",
                    "Slot 1": "—",
                    "Slot 2": "—",
                    "Difference": "—",
                },
            ],
            use_container_width=True,
            hide_index=True,
        )

    with overlay_tab:
        st.caption(
            "Parameter curves, profile traces, and likelihood components "
            "will be overlaid here."
        )

    with differences_tab:
        st.caption(
            "Absolute, signed, normalized, and reference-relative "
            "differences will be shown here."
        )
