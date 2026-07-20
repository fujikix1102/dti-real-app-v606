import streamlit as st

from dti_ui_v1.components.evidence_layer.gtds_manifest_binding_panel import (
    render_gtds_manifest_binding
)

from dti_ui_v1.components.evidence_layer.gtds_manifest_scan_panel import (
    render_gtds_manifest_scan
)

from dti_ui_v1.components.evidence_layer.gtds_result_viewer import (
    render_gtds_result_history
)


from dti_ui_v1.components.evidence_layer.gtds_route_a_display_panel import (
    render_gtds_route_a_display
)


def render_gtds_evidence_router():

    st.header(
        "GTDS Evidence Diagnostics"
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Manifest",
            "Run Scan",
            "Route A",
            "History"
        ]
    )


    with tab1:

        render_gtds_manifest_binding()


    with tab2:

        render_gtds_manifest_scan()


    with tab3:

        render_gtds_route_a_display(
            {
                "source":
                "GTDS_ROUTE_A_FINAL_HASH_LOCK_V1",

                "mode":
                "DISPLAY_ONLY"
            }
        )


    with tab4:

        render_gtds_result_history()
