import streamlit as st

from dti_ui_v1.services.evidence_registry.manifest_selector import (
    list_manifests,
    load_manifest,
    resolve_asset
)


def render_gtds_manifest_binding():


    st.subheader(
        "GTDS Manifest Binding"
    )


    files=list_manifests()


    if not files:

        st.info(
            "No manifest registered"
        )

        return None


    selected=st.selectbox(
        "Manifest version",
        [
            x.name
            for x in files
        ]
    )


    manifest=load_manifest(
        selected
    )


    asset=resolve_asset(
        manifest
    )


    st.json(
        {
            "manifest":
                selected,

            "asset":
                asset,

            "checksum":
                manifest.get(
                    "checksum"
                ),

            "claim_boundary":
                manifest.get(
                    "claim_boundary"
                )
        }
    )


    return asset
