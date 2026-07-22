import streamlit as st


def render_health_status_panel(status):

    st.subheader(
        "Evidence Chain Health Status"
    )

    st.write(status)

    if status.get("overall") == "PASS":

        st.success(
            "Evidence chain health PASS"
        )

    else:

        st.error(
            "Evidence chain health FAIL"
        )


    st.caption(
        "Read-only health summary. "
        "No freeze mutation, source mutation, "
        "likelihood, posterior, MCMC execution."
    )
