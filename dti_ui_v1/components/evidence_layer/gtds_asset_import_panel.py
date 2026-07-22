import streamlit as st

from dti_ui_v1.services.evidence_registry.gtds_asset_importer import save_manifest



def render_gtds_asset_import():

    st.subheader(
        "GTDS Asset Import"
    )


    folder=st.text_input(
        "Asset folder"
    )


    if st.button(
        "Create Manifest"
    ):

        path,data=save_manifest(
            folder
        )

        st.success(
            str(path)
        )

        st.json(data)
