import streamlit as st
from pathlib import Path
import json


def render_gtds_result_history():

    st.subheader(
        "GTDS Result History"
    )


    root = Path(
        "data/research/evidence/dti_raw_profile/results"
    )


    if not root.exists():

        st.info(
            "No GTDS results"
        )

        return


    for f in sorted(root.glob("*.json")):

        st.caption(
            f.name
        )

        st.json(
            json.loads(
                f.read_text()
            )
        )
