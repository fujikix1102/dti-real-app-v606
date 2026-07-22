import streamlit as st


def render_freeze_hash_verify(result):

    st.subheader(
        "Evidence Chain Freeze Hash Verification"
    )

    st.write(result)

    if result.get("status") == "HASH_MATCH":

        st.success(
            "Freeze identity verified."
        )

    elif result.get("status") == "HASH_MISMATCH":

        st.error(
            "Freeze hash mismatch detected."
        )

    else:

        st.warning(
            "Freeze record unavailable."
        )

    st.caption(
        "Read-only freeze identity verification. "
        "No source mutation, no likelihood, "
        "posterior, MCMC, or physical inference."
    )
