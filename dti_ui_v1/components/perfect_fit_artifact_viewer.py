from __future__ import annotations

import json
from pathlib import Path
import streamlit as st


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = ROOT / "data" / "run_artifacts"


def _artifacts():
    if not ARTIFACT_DIR.exists():
        return []

    return sorted(
        ARTIFACT_DIR.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )


def _load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def render_perfect_fit_artifact_viewer():
    st.subheader("PERFECT FIT Artifact Viewer")

    files = _artifacts()

    if not files:
        st.info("No run artifact found.")
        return

    selected = st.selectbox(
        "Artifact",
        files,
        format_func=lambda x: x.name,
        key="perfect_fit_artifact_selector_v1",
    )

    payload = _load(selected)

    st.caption(f"File: {selected}")

    st.markdown("### Identity")

    st.write(
        {
            "route": payload.get("route"),
            "artifact_sha256": payload.get("artifact_sha256"),
            "created_at_utc": payload.get("created_at_utc"),
        }
    )

    st.markdown("### Request")

    st.json(payload.get("request", {}))

    st.markdown("### Response")

    response = payload.get("response", {})

    st.write(
        {
            "status": response.get("status"),
            "engine": response.get("engine"),
        }
    )

    st.markdown("### Boundary")

    st.warning(
        "Artifact display only. "
        "No posterior, MCMC, evidence, or model preference claim."
    )

    st.json(response.get("boundary", {}))
