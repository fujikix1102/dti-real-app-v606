import streamlit as st


def render_public_readiness_report(report):

    st.subheader(
        "Evidence Chain Public Readiness Report"
    )

    st.write(report)

    if report.get("public_readiness") == "READY":

        st.success(
            "Evidence chain public readiness READY"
        )

    else:

        st.warning(
            "Evidence chain public readiness BLOCKED"
        )


    st.caption(
        "Read-only readiness report. "
        "No public deployment, no source mutation, "
        "no likelihood, posterior, MCMC execution."
    )
