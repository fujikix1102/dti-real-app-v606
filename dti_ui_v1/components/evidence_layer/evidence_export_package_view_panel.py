import streamlit as st


def render_evidence_export_package_view(summary):

    st.subheader(
        "Evidence Export Package View"
    )

    st.write(
        {
            "registry_count":
                summary.get("registry_count"),
            "registry_status":
                summary.get("registry_status"),
            "validation_status":
                summary.get("validation_status"),
            "failure_status":
                summary.get("failure_status"),
            "manifest_status":
                summary.get("manifest_status"),
        }
    )

    st.write(
        "Manifest keys",
        summary.get("manifest_keys"),
    )

    st.write(
        "Boundary",
        summary.get("boundary"),
    )

    st.caption(
        "Export package view only. "
        "No likelihood, posterior, MCMC, "
        "or physical inference execution."
    )
