import csv
from pathlib import Path
import streamlit as st


def render_gtds_frozen_diagnostic():

    st.subheader(
        "GTDS Frozen Diagnostic"
    )

    st.caption(
        "Frozen diagnostic asset display only. "
        "No sampler, likelihood, or posterior execution."
    )

    st.info(
        "Evidence status: FROZEN"
    )

    st.caption(
        "Provenance status: PASS"
    )

    st.caption(
        "Display mode: READ ONLY"
    )

    st.caption(
        "Evidence chain: ledger → figure → visual → handover"
    )

    base = Path(__file__).resolve().parents[3]

    ledger_path = (
        base
        / "_GTDS_MCMC_FINAL_STATE_LEDGER_FREEZE_V1_20260803"
        / "ledger"
        / "GTDS_MCMC_FINAL_STATE_LEDGER.tsv"
    )

    figure_path = (
        base
        / "_PARAMETER_RESPONSE_VISUALIZATION_FIGURE_FREEZE_V1_20260803"
        / "render"
    )

    if ledger_path.exists():

        ledger = {}

        with ledger_path.open() as f:
            for row in csv.DictReader(f, delimiter="\t"):
                ledger[row["key"]] = row["value"]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Chains",
            ledger.get("chain_count", "N/A")
        )

        c2.metric(
            "Max Rhat",
            ledger.get("max_rhat", "N/A")
        )

        c3.metric(
            "Worst parameter",
            ledger.get("worst_parameter", "N/A")
        )

        st.success(
            "GTDS frozen ledger loaded."
        )

    else:

        st.warning(
            "Frozen GTDS ledger not found."
        )

    if figure_path.exists():

        st.subheader(
            "GTDS Frozen Diagnostic Visualization"
        )

        st.caption(
            "Parameter-response diagnostic visualization from frozen GTDS asset. "
            "Display only; no recomputation or posterior evaluation."
        )

        render_root = (
            Path(__file__).resolve().parents[3]
            / "_PARAMETER_RESPONSE_VISUALIZATION_FIGURE_FREEZE_V1_20260803"
            / "render"
        )

        png = (
            render_root
            / "GTDS_FROZEN_DIAGNOSTIC_PARAMETER_RESPONSE_AXIS_REFINED.png"
        )

        if png.exists():

            st.image(
                str(png),
                use_container_width=True
            )

            st.caption(
                f"Source: {png}"
            )

        else:

            st.warning(
                "Frozen rendered figure not found."
            )

    else:

        st.warning(
            "Visualization asset not found."
        )

    st.caption(
        "Interpretation boundary: diagnostic evidence registry only. "
        "No posterior inference. No detection claim."
    )
