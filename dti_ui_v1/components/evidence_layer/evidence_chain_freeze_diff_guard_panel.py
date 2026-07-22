import streamlit as st


def render_freeze_diff_guard(result):

    st.subheader(
        "Evidence Chain Freeze Diff Guard"
    )

    st.write(result)

    if result.get("guard_status") == "PASS":

        st.success(
            "Freeze integrity guard PASS"
        )

    else:

        st.error(
            "Freeze integrity guard FAIL"
        )

    st.caption(
        "Read-only freeze comparison guard. "
        "No freeze modification, no source mutation, "
        "no likelihood, posterior, MCMC execution."
    )
