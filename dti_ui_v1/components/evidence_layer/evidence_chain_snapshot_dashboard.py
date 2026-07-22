import streamlit as st


def render_evidence_chain_snapshot_dashboard(snapshot):

    st.subheader(
        "Evidence Chain Snapshot Dashboard"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Registry Sources",
            snapshot.get("registry_count", 0),
        )

    with col2:
        st.metric(
            "Health",
            snapshot.get("health_status", "UNKNOWN"),
        )

    with col3:
        st.metric(
            "Readiness",
            snapshot.get("public_readiness", "UNKNOWN"),
        )


    st.divider()


    st.write(
        {
            "freeze_guard":
                snapshot.get("guard_status"),

            "alert_count":
                snapshot.get("alert_count"),

            "snapshot_status":
                snapshot.get("status"),
        }
    )


    if snapshot.get("status") == "SNAPSHOT_READY":

        st.success(
            "Evidence chain snapshot dashboard PASS"
        )

    else:

        st.error(
            "Evidence chain snapshot dashboard FAIL"
        )


    st.caption(
        "Read-only evidence chain dashboard. "
        "No freeze mutation, source mutation, "
        "likelihood, posterior, MCMC execution."
    )
