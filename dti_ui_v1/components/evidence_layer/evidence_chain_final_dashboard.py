import streamlit as st


def render_evidence_chain_final_dashboard(
    registry,
    validation,
    manifest_summary,
    normalized_status,
):

    st.subheader(
        "Evidence Chain Final Dashboard"
    )

    st.write(
        {
            "source_registry_count": len(registry),
            "validation_count": len(validation),
            "manifest_status": manifest_summary.get("status"),
            "normalized_schema": normalized_status,
        }
    )


    st.markdown("### Source Registry")

    for k, v in registry.items():

        st.write(
            {
                "source": k,
                "exists": v.get("exists"),
                "sha256": v.get("sha256"),
                "role": v.get("role"),
            }
        )


    st.markdown("### Validation")

    for k, v in validation.items():

        st.write(
            {
                "source": k,
                "status": v.get(
                    "verification_status"
                ),
            }
        )


    st.markdown("### Manifest")

    st.write(
        manifest_summary
    )


    st.caption(
        "Evidence chain dashboard only. "
        "No likelihood, posterior, MCMC, "
        "or physical inference execution."
    )
