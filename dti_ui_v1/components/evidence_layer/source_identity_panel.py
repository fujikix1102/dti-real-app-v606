import streamlit as st
from pathlib import Path
import json


def render_source_identity():

    st.subheader(
        "Source Identity Registry"
    )


    root=Path(
        "data/research/evidence/source_identity"
    )


    for f in root.glob("*.json"):

        st.caption(
            f.name
        )

        st.json(
            json.loads(
                f.read_text()
            )
        )
