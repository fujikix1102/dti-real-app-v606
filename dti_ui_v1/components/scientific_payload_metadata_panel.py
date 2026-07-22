from pathlib import Path
import hashlib

import pandas as pd
import streamlit as st


def render_scientific_payload_metadata(source_path):

    path = Path(source_path)

    st.subheader("Scientific Payload Metadata")

    if not path.exists():
        st.warning("Source not found")
        return

    df = pd.read_csv(
        path,
        sep="\t",
        dtype=str,
        keep_default_na=False,
    )

    df = df.astype(str)

    schema_text = "\n".join(
        f"{c}:str"
        for c in df.columns
    )

    schema_hash = hashlib.sha256(
        schema_text.encode()
    ).hexdigest()

    st.write(
        {
            "source": str(path),
            "exists": True,
            "rows": len(df),
            "columns": len(df.columns),
            "schema_hash": schema_hash,
        }
    )

    st.caption(
        "Diagnostic metadata only. "
        "No likelihood, posterior, MCMC, or physical inference."
    )
