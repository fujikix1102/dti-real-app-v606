from __future__ import annotations

import json
from pathlib import Path
import streamlit as st

from dti_ui_v1.components.safe_json_display import render_safe_json


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

    st.info(
        "Workspace runtime notice: this view represents the deployed "
        "Streamlit runtime. Local development files, backups, and review "
        "packages are not included. Public runtime storage is separate "
        "from the local checkout and is not automatically synchronized."
    )

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

    render_safe_json(payload.get("request", {}))

    st.markdown("### Response")

    response = payload.get("response", {})
    if not isinstance(response, dict):
        response = {}

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

    render_safe_json(response.get("boundary", {}))
