import streamlit as st
from pathlib import Path

from dti_ui_v1.services.gtds_bic_scan import run_gtds_scan



def render_gtds_profile_panel():


    st.subheader(
        "GTDS 120-point BIC profile audit"
    )


    path=Path(
        "data/research/evidence/dti_raw_profile/profile_120.tsv"
    )


    if not path.exists():

        st.info(
            "No GTDS profile registered"
        )

        return


    result=run_gtds_scan(
        path
    )


    st.json(
        result
    )


    st.caption(
        "Diagnostic only. "
        "No posterior inference. "
        "No detection claim."
    )
