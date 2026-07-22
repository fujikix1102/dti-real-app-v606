import streamlit as st


def render_bundle_hash_panel(result):

    st.subheader(
        "Evidence Chain Bundle Hash Verification"
    )

    st.write(
        result
    )

    if result.get("status") == "HASH_READY":

        st.success(
            "Bundle hash verification ready"
        )

    else:

        st.error(
            "Bundle hash verification failed"
        )

    st.caption(
        "Read-only bundle identity check. "
        "No bundle mutation, snapshot mutation, "
        "freeze mutation, likelihood, posterior, MCMC execution."
    )
