import streamlit as st


def render_source_identity_registry(registry):

    st.subheader(
        "Source Identity Registry"
    )

    for name, item in registry.items():

        st.write(
            {
                "source": name,
                "path": item.get("path"),
                "exists": item.get("exists"),
                "sha256": item.get("sha256"),
                "role": item.get("role"),
                "likelihood": item.get("likelihood"),
                "posterior": item.get("posterior"),
                "claim": item.get("claim"),
            }
        )

    st.caption(
        "Source identity record only. "
        "No likelihood, posterior, MCMC, "
        "or physical inference execution."
    )
