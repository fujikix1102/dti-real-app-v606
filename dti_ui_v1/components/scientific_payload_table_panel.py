from pathlib import Path

import pandas as pd
import streamlit as st


def render_scientific_payload_table(source_path):

    path = Path(source_path)

    st.subheader("Scientific Payload Table")

    if not path.exists():
        st.warning("Diagnostic source not found")
        return

    try:
        df = pd.read_csv(
            path,
            sep="\t",
            dtype=str,
            keep_default_na=False,
        )

        # Force stable display schema before Streamlit/PyArrow conversion
        df = df.astype(str)

        st.write(
            {
                "source": str(path),
                "rows": len(df),
                "columns": list(df.columns),
            }
        )

        st.dataframe(
            df,
            use_container_width=True,
        )

        st.caption(
            "Diagnostic payload display only. "
            "No likelihood, posterior, MCMC, or physical inference execution."
        )

    except Exception as exc:
        st.error(
            "Payload table load failed: " + str(exc)
        )
