import streamlit as st
from pathlib import Path


def render_raw_profile_viewer():

    st.subheader(
        "DTI Raw Profile Evidence"
    )


    root=Path(
        "data/research/evidence/dti_raw_profile"
    )


    files=list(root.glob("*"))


    if files:

        st.write(
            [
                str(x)
                for x in files
            ]
        )

    else:

        st.info(
            "No raw profile asset registered"
        )
