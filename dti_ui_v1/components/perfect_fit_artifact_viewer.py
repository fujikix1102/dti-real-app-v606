from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
from typing import Any, Mapping
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd
import streamlit as st

from dti_ui_v1.components.safe_json_display import render_safe_json
from dti_ui_v1.services.run_store import (
    build_notebook_export,
    build_reproduction_package,
    build_run_manifest,
    get_run_artifact_store_status,
    list_run_artifact_paths,
    list_run_artifacts,
)


def _artifacts():
    return list_run_artifact_paths()


def _load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _parameter_rows(
    current: Mapping[str, Any],
    previous: Mapping[str, Any] | None,
) -> list[dict[str, Any]]:
    keys = ("H0", "A_DTI", "omega_b", "omega_cdm", "z_c", "f_EDE")
    rows: list[dict[str, Any]] = []
    for key in keys:
        current_value = current.get(key)
        previous_value = previous.get(key) if previous else None
        row: dict[str, Any] = {
            "parameter": key,
            "current": current_value,
            "previous": previous_value,
            "delta": None,
        }
        try:
            if current_value is not None and previous_value is not None:
                row["delta"] = float(current_value) - float(previous_value)
        except (TypeError, ValueError):
            row["delta"] = None
        rows.append(row)
    return rows


def _nested_value(payload: Mapping[str, Any], dotted_key: str) -> Any:
    value: Any = payload
    for part in dotted_key.split("."):
        if not isinstance(value, Mapping):
            return None
        value = value.get(part)
    return value


def _response_rows(
    current: Mapping[str, Any],
    previous: Mapping[str, Any] | None,
) -> list[dict[str, Any]]:
    keys = (
        ("status", "status"),
        ("engine", "engine"),
        ("model_chi2", "model_chi2"),
        ("model_loglike", "model_loglike"),
        ("rdrag_Mpc", "rdrag_Mpc"),
        ("DESI chi2", "desi_dr2_bao.chi2"),
        ("joint chi2", "joint_likelihood.chi2_effective_sum"),
    )
    rows: list[dict[str, Any]] = []
    for label, key in keys:
        current_value = _nested_value(current, key)
        previous_value = _nested_value(previous, key) if previous else None
        row: dict[str, Any] = {
            "quantity": label,
            "current": current_value,
            "previous": previous_value,
            "delta": None,
        }
        try:
            if current_value is not None and previous_value is not None:
                row["delta"] = float(current_value) - float(previous_value)
        except (TypeError, ValueError):
            row["delta"] = None
        rows.append(row)
    return rows


def _package_zip_bytes(files: Mapping[str, str]) -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w", compression=ZIP_DEFLATED) as archive:
        for name, content in files.items():
            archive.writestr(name, content)
    return buffer.getvalue()


def render_perfect_fit_artifact_viewer():
    st.subheader("PERFECT FIT Artifact Viewer")

    st.info(
        "Workspace runtime notice: this view represents the deployed "
        "Streamlit runtime. Local development files, backups, and review "
        "packages are not included. Public runtime storage is separate "
        "from the local checkout and is not automatically synchronized."
    )
    st.markdown("### Artifact storage")
    render_safe_json(get_run_artifact_store_status())

    files = _artifacts()

    if not files:
        st.info("No run artifact found.")
        return

    history = list_run_artifacts()
    if history:
        st.markdown("### Run history")
        st.dataframe(
            pd.DataFrame(history),
            hide_index=True,
            use_container_width=True,
        )

    selected = st.selectbox(
        "Artifact",
        files,
        format_func=lambda x: x.name,
        key="perfect_fit_artifact_selector_v1",
    )

    payload = _load(selected)
    if not isinstance(payload, dict):
        payload = {}

    st.caption(f"File: {selected}")

    st.markdown("### Identity")

    st.write(
        {
            "run_id": payload.get("run_id"),
            "route": payload.get("route"),
            "artifact_sha256": payload.get("artifact_sha256"),
            "created_at_utc": payload.get("created_at_utc"),
        }
    )

    manifest = build_run_manifest(payload)
    notebook = build_notebook_export(payload)
    package_files = build_reproduction_package(payload)
    package_zip = _package_zip_bytes(package_files)

    st.markdown("### Reproduction exports")
    export_columns = st.columns(3)
    export_columns[0].download_button(
        "Download manifest JSON",
        data=json.dumps(manifest, ensure_ascii=False, indent=2, allow_nan=False),
        file_name=f"{manifest.get('run_id', 'dti_run')}_manifest.json",
        mime="application/json",
        key="perfect_fit_manifest_download_v1",
        width="stretch",
    )
    export_columns[1].download_button(
        "Download notebook MD",
        data=notebook,
        file_name=f"{manifest.get('run_id', 'dti_run')}_notebook.md",
        mime="text/markdown",
        key="perfect_fit_notebook_download_v1",
        width="stretch",
    )
    export_columns[2].download_button(
        "Download reproduction ZIP",
        data=package_zip,
        file_name=f"{manifest.get('run_id', 'dti_run')}_reproduction.zip",
        mime="application/zip",
        key="perfect_fit_reproduction_zip_download_v1",
        width="stretch",
    )

    st.markdown("### Request")

    request = payload.get("request", {})
    if not isinstance(request, dict):
        request = {}
    render_safe_json(request)

    previous_payload = None
    selected_index = files.index(selected)
    if selected_index + 1 < len(files):
        previous_payload = _load(files[selected_index + 1])
    previous_request = (
        previous_payload.get("request", {})
        if isinstance(previous_payload, dict)
        else {}
    )
    previous_response = (
        previous_payload.get("response", {})
        if isinstance(previous_payload, dict)
        else {}
    )
    st.markdown("### Parameter diff")
    st.dataframe(
        pd.DataFrame(
            _parameter_rows(
                request,
                previous_request if isinstance(previous_request, dict) else None,
            )
        ),
        hide_index=True,
        use_container_width=True,
    )

    st.markdown("### Response")

    response = payload.get("response", {})
    if not isinstance(response, dict):
        response = {}

    st.markdown("### Result diff")
    st.dataframe(
        pd.DataFrame(
            _response_rows(
                response,
                previous_response if isinstance(previous_response, dict) else None,
            )
        ),
        hide_index=True,
        use_container_width=True,
    )

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
