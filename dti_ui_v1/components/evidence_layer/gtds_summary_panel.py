import streamlit as st
from pathlib import Path
import json


def render_gtds_summary():

    st.subheader(
        "GTDS Current Evidence State"
    )


    manifest_root=Path(
        "data/research/evidence/dti_raw_profile"
    )


    result_root=manifest_root/"results"


    summary={

        "manifest_count":
            len(
                list(
                    manifest_root.glob(
                        "manifest_v*.json"
                    )
                )
            ),

        "latest_result":
            (
                str(
                    result_root/"latest_scan.json"
                )
                if
                (result_root/"latest_scan.json").exists()
                else
                None
            ),

        "mode":
            "diagnostic_only",

        "posterior":
            False,

        "detection_claim":
            False
    }


    st.json(summary)
