import streamlit as st
from pathlib import Path

from dti_ui_v1.services.gtds_profile_validator import validate_profile



def render_gtds_validation_panel():


    st.subheader(
        "GTDS profile validation"
    )


    profile=Path(
        "data/research/evidence/dti_raw_profile/profile_120.tsv"
    )


    manifest=Path(
        "data/research/evidence/dti_raw_profile/profile_manifest.json"
    )


    result=validate_profile(
        profile,
        manifest
    )


    st.json(
        result
    )


    if result.get("status")=="PASS":

        st.success(
            "GTDS profile validation PASS"
        )

    else:

        st.warning(
            "GTDS profile validation failed"
        )
