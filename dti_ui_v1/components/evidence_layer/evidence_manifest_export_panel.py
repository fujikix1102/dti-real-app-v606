import streamlit as st


def render_evidence_manifest_export(summary):

    st.subheader(
        "Evidence Manifest Export"
    )

    st.write(
        summary
    )

    if summary.get("status") == "MANIFEST_READY":

        st.success(
            "Manifest chain available"
        )

    else:

        st.warning(
            "Manifest not found"
        )

    st.caption(
        "Manifest inspection only. "
        "No likelihood, posterior, MCMC, "
        "or physical inference execution."
    )
