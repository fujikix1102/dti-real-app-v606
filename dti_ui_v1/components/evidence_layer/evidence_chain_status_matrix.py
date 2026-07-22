import streamlit as st
import pandas as pd


def render_evidence_chain_status_matrix(registry):

    rows = []

    for name, item in registry.items():
        rows.append(
            {
                "source": name,
                "exists": item.get("exists"),
                "sha256": item.get("sha256"),
                "role": item.get("role"),
                "likelihood": item.get("likelihood"),
                "posterior": item.get("posterior"),
                "claim": item.get("claim"),
            }
        )

    df = pd.DataFrame(rows)

    df = (
        df
        .fillna("")
        .astype(str)
    )

    st.subheader("Evidence Chain Status Matrix")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Evidence identity matrix only. "
        "No likelihood, posterior, MCMC, "
        "or physical inference execution."
    )
