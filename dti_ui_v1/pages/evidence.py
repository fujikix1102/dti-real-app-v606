"""Evidence and technical-boundary page."""

from __future__ import annotations

import streamlit as st

from dti_ui_v1.components.desi_external_confirmation import (
    render_desi_external_confirmation,
)


def render() -> None:
    st.title("Evidence")
    st.caption("Sources, contracts, audit status, and interpretation limits")

    source_tab, contract_tab, interpretation_tab, migration_tab = st.tabs(
        (
            "Sources",
            "API contract",
            "Interpretation",
            "Migration",
        )
    )

    with source_tab:
        st.dataframe(
            [
                {
                    "Object": "Legacy application",
                    "Role": "Protected reference",
                    "Status": "Unchanged",
                },
                {
                    "Object": "Locked BAO client",
                    "Role": "Backend service",
                    "Status": "Available",
                },
                {
                    "Object": "Response parser",
                    "Role": "Response validation",
                    "Status": "Available",
                },
                {
                    "Object": "Value formatter",
                    "Role": "Display formatting",
                    "Status": "Available",
                },
            ],
            use_container_width=True,
            hide_index=True,
        )

    with contract_tab:
        st.subheader("Request contract")

        st.code(
            "\n".join(
                [
                    "use_locked_baseline=true",
                    "unsupported inputs=hidden",
                    "response validation=fail closed",
                    "display formatting=presentation only",
                ]
            ),
            language="text",
        )

    with interpretation_tab:
        st.subheader("Interpretation limits")

        st.markdown(
            """
The application displays source-traceable diagnostic outputs.

The interface itself does not:

- create a new likelihood,
- create a posterior constraint,
- change a scientific value,
- prove a physical mechanism,
- authorize manuscript claims,
- authorize public deployment.
"""
        )

        with st.expander("Full scientific wording"):
            st.write(
                "Displayed diagnostics must be interpreted within the source "
                "analysis and its recorded assumptions. UI formatting, grouping, "
                "navigation, and visual presentation do not constitute an "
                "independent scientific calculation."
            )

    with migration_tab:
        st.subheader("Zero Loss migration")

        st.write(
            "Existing functions are moved only after their source, inputs, "
            "outputs, and dependencies are mapped."
        )

        st.dataframe(
            [
                {
                    "Area": "Legacy app.py",
                    "Status": "Protected",
                },
                {
                    "Area": "Independent entry point",
                    "Status": "Created",
                },
                {
                    "Area": "Backend binding",
                    "Status": "Pending",
                },
                {
                    "Area": "Results migration",
                    "Status": "Pending",
                },
                {
                    "Area": "Visual parity",
                    "Status": "Pending",
                },
            ],
            use_container_width=True,
            hide_index=True,
        )

    st.divider()
    render_desi_external_confirmation()
