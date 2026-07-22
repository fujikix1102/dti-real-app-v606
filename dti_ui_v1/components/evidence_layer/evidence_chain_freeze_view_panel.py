import streamlit as st
import pandas as pd


def render_freeze_view(record):

    st.subheader(
        "Evidence Chain Freeze Record"
    )

    df = (
        pd.DataFrame(
            [
                {
                    "item": k,
                    "value": v,
                }
                for k,v in record.items()
            ]
        )
        .fillna("")
        .astype(str)
    )

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
    )

    st.caption(
        "Freeze record view only. "
        "No regeneration, likelihood, posterior, "
        "MCMC, or physical inference execution."
    )
