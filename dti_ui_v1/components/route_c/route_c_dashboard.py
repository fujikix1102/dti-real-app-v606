import streamlit as st

from dti_ui_v1.services.route_c.route_c_adapter import (
    build_route_c_display_payload,
)


def render_route_c_dashboard():

    st.subheader("Route C Diagnostic Adapter")

    payload = build_route_c_display_payload()

    st.json(payload)
