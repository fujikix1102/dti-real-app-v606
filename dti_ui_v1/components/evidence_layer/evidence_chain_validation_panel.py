import streamlit as st
import pandas as pd


def render_evidence_chain_validation_panel(validation):

    rows = []

    for source, item in validation.items():
        rows.append(
            {
                "source": source,
                **item,
            }
        )

    df = (
        pd.DataFrame(rows)
        .fillna("")
        .astype(str)
    )

    st.subheader(
        "Evidence Chain Validation"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Validation status only. "
        "No likelihood, posterior, MCMC, "
        "or physical inference execution."
    )
