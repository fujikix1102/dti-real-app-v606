import streamlit as st
import pandas as pd


def render_integrity_scorecard(scorecard):

    st.subheader(
        "Evidence Chain Integrity Scorecard"
    )

    df = (
        pd.DataFrame(
            [
                {
                    "check": k,
                    "status": (
                        "PASS"
                        if v
                        else "FAIL"
                    ),
                }
                for k,v in scorecard["checks"].items()
            ]
        )
        .astype(str)
    )

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
    )

    st.metric(
        "Integrity Score",
        scorecard["score"],
    )

    st.caption(
        "Integrity scorecard only. "
        "No likelihood, posterior, MCMC, "
        "or physical inference execution."
    )
