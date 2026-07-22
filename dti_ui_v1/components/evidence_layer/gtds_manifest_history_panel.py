import streamlit as st
from pathlib import Path
import json


def render_gtds_manifest_history():

    st.subheader(
        "GTDS Manifest History"
    )

    root=Path(
        "data/research/evidence/dti_raw_profile"
    )

    files=sorted(
        root.glob("manifest_v*.json")
    )

    if not files:

        st.info(
            "No manifest history"
        )

        return


    selected=st.selectbox(
        "Select manifest version",
        [
            x.name
            for x in files
        ]
    )


    data=json.loads(
        (
            root/selected
        ).read_text()
    )


    st.json(data)
