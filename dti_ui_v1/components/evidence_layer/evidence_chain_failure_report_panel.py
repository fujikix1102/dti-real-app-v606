import streamlit as st
import pandas as pd


def render_evidence_chain_failure_report(report):

    rows = []

    for source, item in report.items():
        rows.append(
            {
                "source": source,
                "verification_status":
                    item["verification_status"],
                "failure_count":
                    item["failure_count"],
                "failure_reasons":
                    ", ".join(item["failure_reasons"]),
            }
        )

    df = (
        pd.DataFrame(rows)
        .fillna("")
        .astype(str)
    )

    st.subheader(
        "Evidence Chain Failure Report"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Failure reporting only. "
        "No likelihood, posterior, MCMC, "
        "or physical inference execution."
    )
