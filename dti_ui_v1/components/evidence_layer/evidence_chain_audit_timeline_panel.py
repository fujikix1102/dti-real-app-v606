import streamlit as st
import pandas as pd


def render_evidence_chain_audit_timeline(timeline):

    st.subheader(
        "Evidence Chain Audit Timeline"
    )

    df = (
        pd.DataFrame(timeline)
        .fillna("")
        .astype(str)
    )

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
    )

    st.caption(
        "Audit timeline view only. "
        "No likelihood, posterior, MCMC, "
        "or physical inference execution."
    )
