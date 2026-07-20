import streamlit as st


def render_gtds_route_a_display(payload):

    st.subheader(
        "GTDS Route A Evidence Display"
    )

    st.json(
        payload
    )

    st.caption(
        "Diagnostic evidence display only. "
        "No posterior inference. "
        "No detection claim."
    )
