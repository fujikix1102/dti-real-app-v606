import streamlit as st
import pandas as pd


def render_reproducibility_report(report):

    st.subheader(
        "Evidence Chain Reproducibility Report"
    )

    df = (
        pd.DataFrame(
            [
                {
                    "item": k,
                    "status": v,
                }
                for k,v in report.items()
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
        "Reproducibility report only. "
        "No likelihood, posterior, MCMC, "
        "or physical inference execution."
    )
