import streamlit as st

from dti_ui_v1.services.evidence_registry.manifest_selector import (
    list_manifests
)

from dti_ui_v1.services.gtds_manifest_executor import (
    execute_manifest_scan
)


def render_gtds_manifest_scan():

    st.subheader(
        "GTDS Manifest Scan"
    )


    manifests = list_manifests()


    if not manifests:

        st.info(
            "No manifest available"
        )

        return


    selected = st.selectbox(
        "Select manifest",
        [
            x.name
            for x in manifests
        ]
    )


    if st.button(
        "Run GTDS Diagnostic"
    ):

        result = execute_manifest_scan(
            selected
        )

        st.json(
            result
        )


        st.caption(
            "Diagnostic only. "
            "No posterior inference. "
            "No detection claim."
        )
