import streamlit as st


def render_evidence_chain_snapshot_panel(snapshot):

    st.subheader(
        "Evidence Chain Readiness Snapshot"
    )

    st.write(
        snapshot
    )

    if snapshot.get("status") == "SNAPSHOT_READY":
        st.success(
            "Evidence chain snapshot ready"
        )
    else:
        st.error(
            "Evidence chain snapshot unavailable"
        )

    st.caption(
        "Read-only snapshot view. "
        "No freeze mutation, source mutation, "
        "likelihood, posterior, MCMC execution."
    )
