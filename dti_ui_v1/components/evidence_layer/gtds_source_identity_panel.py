import streamlit as st
from pathlib import Path
import json


def render_gtds_source_identity():

    st.subheader(
        "GTDS Source Identity"
    )


    root=Path(
        "data/research/evidence/dti_raw_profile/results"
    )

    f=root/"latest_scan.json"


    if not f.exists():

        st.info(
            "No scan record"
        )

        return


    data=json.loads(
        f.read_text()
    )


    st.json(
        {
            "source_identity":
                data.get(
                    "source_identity",
                    {}
                ),

            "checksum":
                data.get(
                    "checksum"
                )
        }
    )
