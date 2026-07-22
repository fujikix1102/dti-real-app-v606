import streamlit as st

from dti_ui_v1.services.scientific_diagnostic_filter import (
    available_sources,
    load_filtered_summary,
    apply_flag_filter,
)


def render_scientific_diagnostic_filter():

    st.subheader(
        "Diagnostic Interaction Filter"
    )

    sources = available_sources()

    label = st.selectbox(
        "Source",
        list(sources.keys()),
    )

    flag_key = st.selectbox(
        "Diagnostic Flag",
        [
            "",
            "diagnostic_use",
            "likelihood_use",
            "claim_use",
        ],
    )

    flag_value = st.text_input(
        "Flag value",
        value="",
    )

    summary = load_filtered_summary(label)

    summary = apply_flag_filter(
        summary,
        flag_key,
        flag_value,
    )

    st.write(
        {
            "source": summary.get("source_path"),
            "status": summary.get("status"),
            "filter": summary.get("filter_result"),
        }
    )

    st.caption(
        "Diagnostic interaction only. "
        "No likelihood, posterior, MCMC, "
        "or physical inference execution."
    )




def render_scientific_diagnostic_filter_panel():
    return render_scientific_diagnostic_filter()

