import streamlit as st


def render_scientific_diagnostic_summary(summary):

    st.subheader(
        "Scientific Diagnostic Summary"
    )

    st.write(
        {
            "source": summary.get("source_path"),
            "rows": summary.get("row_count"),
            "columns": summary.get("column_count"),
            "schema_hash": summary.get("schema_hash"),
        }
    )

    st.write(
        "Diagnostic flags",
        summary.get("diagnostic_flags"),
    )

    st.write(
        "Boundary flags",
        summary.get("boundary_flags"),
    )

    st.caption(
        "Diagnostic workbench only. "
        "No likelihood, posterior, MCMC, "
        "or physical inference execution."
    )
