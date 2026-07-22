import streamlit as st


def render_normalized_evidence_workbench(
    primary,
    secondary,
):

    st.subheader(
        "Normalized Evidence Workbench"
    )

    st.write(
        {
            "primary_rows": len(primary),
            "secondary_rows": len(secondary),
            "primary_columns": len(primary.columns),
            "secondary_columns": len(secondary.columns),
        }
    )

    required = [
        "boundary_numeric_adoption",
        "boundary_likelihood",
        "boundary_physical_claim",
    ]

    primary_ok = all(
        x in primary.columns
        for x in required
    )

    secondary_ok = all(
        x in secondary.columns
        for x in required
    )

    st.write(
        {
            "primary_schema": "PASS" if primary_ok else "FAIL",
            "secondary_schema": "PASS" if secondary_ok else "FAIL",
        }
    )

    if not primary_ok or not secondary_ok:
        st.warning(
            "Schema mismatch detected"
        )

    with st.expander(
        "Primary normalized source",
        expanded=False,
    ):
        st.dataframe(
            primary.astype(str),
            hide_index=True,
            use_container_width=True,
        )

    with st.expander(
        "Secondary normalized source",
        expanded=False,
    ):
        st.dataframe(
            secondary.astype(str),
            hide_index=True,
            use_container_width=True,
        )

    st.caption(
        "Normalized evidence display only. "
        "No likelihood, posterior, MCMC, "
        "or physical inference execution."
    )
