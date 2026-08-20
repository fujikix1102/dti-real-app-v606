from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
from typing import Any, Mapping
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd
import streamlit as st
import altair as alt

from dti_ui_v1.components.safe_json_display import render_safe_json
from dti_ui_v1.services.run_store import (
    build_notebook_export,
    build_reproduction_package,
    build_run_manifest,
    get_anonymous_page_view_summary,
    get_external_run_index,
    get_run_artifact_store_status,
    load_external_run_artifact,
    list_run_artifact_paths,
    list_run_artifacts,
    rebuild_external_run_index_from_remote,
    rebuild_external_run_index_from_runtime,
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


def _compact_r2_rows(rows: list[Mapping[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "created_at": row.get("created_at_utc"),
                "route": row.get("route"),
                "status": row.get("status"),
                "H0": row.get("H0"),
                "A_DTI": row.get("A_DTI"),
                "f_EDE": row.get("f_EDE"),
                "z_c": row.get("z_c"),
                "sha12": str(row.get("artifact_sha256") or "")[:12],
                "run_id": row.get("run_id"),
            }
            for row in rows
        ]
    )


def _r2_summary_payload(
    *,
    index: Mapping[str, Any],
    rows: list[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": "dti-r2-viewer-summary-v1",
        "backend": index.get("backend"),
        "bucket": index.get("bucket"),
        "index_key": index.get("index_key"),
        "run_count": len(rows),
        "routes": sorted(
            {
                str(row.get("route"))
                for row in rows
                if isinstance(row, Mapping) and row.get("route")
            }
        ),
        "runs": list(rows),
        "boundary": {
            "mcmc": "NO",
            "posterior": "NO",
            "model_comparison_claim": "NO",
            "manuscript_update": "NO",
        },
    }


def _research_notebook_markdown(rows: list[Mapping[str, Any]]) -> str:
    if rows:
        frame = _compact_r2_rows(rows)
        headers = list(frame.columns)
        table_lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
        ]
        for _, row in frame.iterrows():
            table_lines.append(
                "| "
                + " | ".join(str(row.get(column, "")) for column in headers)
                + " |"
            )
        table = "\n".join(table_lines)
    else:
        table = "No R2 runs."
    return "\n".join(
        [
            "# DTI PERFECT FIT R2 Research Notebook",
            "",
            "## Scope",
            "",
            "This notebook summarizes public R2 run artifacts visible to the application.",
            "",
            "## Boundary",
            "",
            "- Compute is not triggered by this export.",
            "- MCMC is not executed.",
            "- Posterior inference is not claimed.",
            "- Model comparison preference is not claimed.",
            "- Manuscript or pointer promotion is not performed by this export.",
            "",
            "## Runs",
            "",
            table,
            "",
            "## Reproducibility",
            "",
            "Each run is represented by an immutable artifact key and artifact SHA when available.",
        ]
    )


def _manuscript_pointer_review(rows: list[Mapping[str, Any]]) -> dict[str, Any]:
    run_count = len(rows)
    has_sha = all(bool(row.get("artifact_sha256")) for row in rows if isinstance(row, Mapping))
    has_multiple_routes = len(
        {
            str(row.get("route"))
            for row in rows
            if isinstance(row, Mapping) and row.get("route")
        }
    ) > 1
    return {
        "schema_version": "dti-manuscript-pointer-admissibility-review-v1",
        "decision": "NOT_PROMOTED_REVIEW_ONLY",
        "manuscript_ready": False,
        "pointer_promotion_ready": False,
        "run_count": run_count,
        "checks": {
            "artifacts_visible": run_count > 0,
            "artifact_sha_present": has_sha,
            "multiple_routes_visible": has_multiple_routes,
            "posterior_claim": "NO",
            "mcmc_claim": "NO",
            "model_comparison_claim": "NO",
        },
        "required_before_promotion": [
            "Explicit manuscript admissibility gate",
            "Claim-by-claim evidence mapping",
            "Independent review of public/private posterior boundaries",
            "Decision record approving any pointer update",
        ],
    }


def _render_r2_comparison_graphs(frame: pd.DataFrame) -> None:
    if frame.empty:
        return
    numeric_columns = ["H0", "A_DTI", "f_EDE", "z_c"]
    available = [
        column
        for column in numeric_columns
        if column in frame.columns and pd.to_numeric(frame[column], errors="coerce").notna().any()
    ]
    if not available:
        return
    chart_frame = frame.copy()
    chart_frame["created_at"] = pd.to_datetime(chart_frame["created_at"], errors="coerce")
    chart_frame = chart_frame.dropna(subset=["created_at"])
    if chart_frame.empty:
        return
    long_frame = chart_frame.melt(
        id_vars=["created_at", "route", "status", "run_id"],
        value_vars=available,
        var_name="parameter",
        value_name="value",
    )
    long_frame["value"] = pd.to_numeric(long_frame["value"], errors="coerce")
    long_frame = long_frame.dropna(subset=["value"])
    if long_frame.empty:
        return
    st.markdown("### R2 multi-run parameter graph")
    chart = (
        alt.Chart(long_frame)
        .mark_line(point=True)
        .encode(
            x=alt.X("created_at:T", title="Created"),
            y=alt.Y("value:Q", title="Value"),
            color=alt.Color("parameter:N", title="Parameter"),
            strokeDash=alt.StrokeDash("route:N", title="Route"),
            tooltip=[
                alt.Tooltip("created_at:T", title="Created"),
                alt.Tooltip("route:N", title="Route"),
                alt.Tooltip("parameter:N", title="Parameter"),
                alt.Tooltip("value:Q", title="Value", format=".6g"),
                alt.Tooltip("run_id:N", title="Run ID"),
            ],
        )
        .properties(height=320)
    )
    st.altair_chart(chart, use_container_width=True)


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
    external_index = get_external_run_index()
    if external_index.get("configured"):
        metrics = get_anonymous_page_view_summary(days=7)
        if metrics.get("configured"):
            st.markdown("### Anonymous page views")
            metric_columns = st.columns(2)
            today_total = 0
            days = metrics.get("days", [])
            if isinstance(days, list) and days:
                today_total = int(days[0].get("total") or 0)
            metric_columns[0].metric("Today views", today_total)
            metric_columns[1].metric("7d views", int(metrics.get("total") or 0))
            render_safe_json(
                {
                    "schema_version": metrics.get("schema_version"),
                    "pages": metrics.get("pages"),
                    "commits": metrics.get("commits"),
                    "privacy": metrics.get("privacy"),
                    "error": metrics.get("error"),
                }
            )
        st.markdown("### R2 artifact index")
        render_safe_json(
            {
                "backend": external_index.get("backend"),
                "bucket": external_index.get("bucket"),
                "index_key": external_index.get("index_key"),
                "run_count": external_index.get("run_count"),
                "error": external_index.get("error"),
            }
        )
        r2_runs = external_index.get("runs", [])
        if isinstance(r2_runs, list) and r2_runs:
            status_values = sorted(
                {
                    str(row.get("status"))
                    for row in r2_runs
                    if isinstance(row, Mapping) and row.get("status")
                }
            )
            search = st.text_input(
                "R2 search",
                value="",
                key="perfect_fit_r2_search_v1",
            ).strip().lower()
            routes = sorted(
                {
                    str(row.get("route"))
                    for row in r2_runs
                    if isinstance(row, Mapping) and row.get("route")
                }
            )
            route_filter = st.selectbox(
                "R2 route filter",
                ["all", *routes],
                key="perfect_fit_r2_route_filter_v1",
            )
            status_filter = st.selectbox(
                "R2 status filter",
                ["all", *status_values],
                key="perfect_fit_r2_status_filter_v1",
            )
            filtered_runs = [
                row
                for row in r2_runs
                if isinstance(row, Mapping)
                and (route_filter == "all" or row.get("route") == route_filter)
                and (status_filter == "all" or row.get("status") == status_filter)
                and (
                    not search
                    or search in json.dumps(row, ensure_ascii=False).lower()
                )
            ]
            r2_frame = _compact_r2_rows(filtered_runs)
            st.dataframe(
                r2_frame,
                hide_index=True,
                use_container_width=True,
            )
            _render_r2_comparison_graphs(r2_frame)
            csv_bytes = r2_frame.to_csv(index=False).encode("utf-8")
            summary_payload = _r2_summary_payload(
                index=external_index,
                rows=filtered_runs,
            )
            export_columns = st.columns(3)
            export_columns[0].download_button(
                "Download R2 runs CSV",
                data=csv_bytes,
                file_name="dti_r2_runs.csv",
                mime="text/csv",
                key="perfect_fit_r2_runs_csv_download_v1",
                width="stretch",
            )
            export_columns[1].download_button(
                "Download R2 summary JSON",
                data=json.dumps(
                    summary_payload,
                    ensure_ascii=False,
                    indent=2,
                    allow_nan=False,
                    default=str,
                ),
                file_name="dti_r2_runs_summary.json",
                mime="application/json",
                key="perfect_fit_r2_summary_json_download_v1",
                width="stretch",
            )
            export_columns[2].download_button(
                "Download R2 audit JSON",
                data=json.dumps(
                    {
                        "schema_version": "dti-r2-token-audit-v1",
                        "backend": external_index.get("backend"),
                        "bucket": external_index.get("bucket"),
                        "index_key": external_index.get("index_key"),
                        "configured": bool(external_index.get("configured")),
                        "last_index_read_error": external_index.get("error"),
                        "visible_run_count": len(filtered_runs),
                        "audit_limit": (
                            "Token scope is verified by successful signed R2 "
                            "read/write operations; token secret material is "
                            "never displayed."
                        ),
                    },
                    ensure_ascii=False,
                    indent=2,
                    allow_nan=False,
                ),
                file_name="dti_r2_token_audit.json",
                mime="application/json",
                key="perfect_fit_r2_token_audit_download_v1",
                width="stretch",
            )
            notebook_text = _research_notebook_markdown(filtered_runs)
            review_payload = _manuscript_pointer_review(filtered_runs)
            extra_export_columns = st.columns(2)
            extra_export_columns[0].download_button(
                "Download research notebook MD",
                data=notebook_text,
                file_name="dti_r2_research_notebook.md",
                mime="text/markdown",
                key="perfect_fit_r2_research_notebook_download_v1",
                width="stretch",
            )
            extra_export_columns[1].download_button(
                "Download manuscript/pointer review JSON",
                data=json.dumps(
                    review_payload,
                    ensure_ascii=False,
                    indent=2,
                    allow_nan=False,
                ),
                file_name="dti_manuscript_pointer_review.json",
                mime="application/json",
                key="perfect_fit_manuscript_pointer_review_download_v1",
                width="stretch",
            )
            choices = [
                row
                for row in filtered_runs
                if isinstance(row, Mapping) and row.get("artifact_key")
            ]
            selected_r2 = st.selectbox(
                "R2 artifact",
                choices,
                format_func=lambda row: str(row.get("run_id")),
                key="perfect_fit_r2_artifact_selector_v1",
            )
            selected_r2_artifact = None
            if st.button(
                "Load R2 artifact",
                key="perfect_fit_r2_artifact_load_v1",
            ):
                try:
                    r2_payload = load_external_run_artifact(
                        str(selected_r2.get("artifact_key"))
                    )
                    st.session_state["perfect_fit_loaded_r2_artifact_v1"] = r2_payload
                except Exception as exc:
                    st.session_state["perfect_fit_loaded_r2_artifact_error_v1"] = {
                        "exception_type": type(exc).__name__,
                        "detail": str(exc),
                    }
            if st.button(
                "Rebuild R2 index from runtime artifacts",
                key="perfect_fit_r2_rebuild_index_v1",
            ):
                st.session_state["perfect_fit_r2_rebuild_result_v1"] = (
                    rebuild_external_run_index_from_runtime()
                )
            if st.button(
                "Rebuild R2 index from bucket",
                key="perfect_fit_r2_remote_rebuild_index_v1",
            ):
                st.session_state["perfect_fit_r2_rebuild_result_v1"] = (
                    rebuild_external_run_index_from_remote()
                )
            rebuild_result = st.session_state.get("perfect_fit_r2_rebuild_result_v1")
            if isinstance(rebuild_result, dict):
                st.caption(
                    "R2 index rebuild: "
                    f"uploaded={rebuild_result.get('uploaded')} · "
                    f"run_count={rebuild_result.get('run_count')} · "
                    f"discovered={rebuild_result.get('discovered_artifact_count', 'runtime')} · "
                    f"error={rebuild_result.get('error')}"
                )
            if selected_r2:
                try:
                    selected_r2_artifact = load_external_run_artifact(
                        str(selected_r2.get("artifact_key"))
                    )
                except Exception:
                    selected_r2_artifact = None
            if isinstance(selected_r2_artifact, dict):
                st.download_button(
                    "Download selected R2 artifact JSON",
                    data=json.dumps(
                        selected_r2_artifact,
                        ensure_ascii=False,
                        indent=2,
                        allow_nan=False,
                        default=str,
                    ),
                    file_name=f"{selected_r2_artifact.get('run_id', 'r2_artifact')}.json",
                    mime="application/json",
                    key="perfect_fit_r2_artifact_download_v1",
                    width="stretch",
                )
            compare_candidates = [
                row
                for row in filtered_runs
                if isinstance(row, Mapping) and row.get("artifact_key")
            ]
            if len(compare_candidates) >= 2:
                comparison = st.multiselect(
                    "Compare R2 runs",
                    compare_candidates,
                    default=compare_candidates[:2],
                    max_selections=2,
                    format_func=lambda row: str(row.get("run_id")),
                    key="perfect_fit_r2_compare_runs_v1",
                )
                if len(comparison) == 2:
                    st.markdown("### R2 run comparison")
                    comparison_frame = pd.DataFrame(
                        _parameter_rows(comparison[0], comparison[1])
                    )
                    st.dataframe(
                        comparison_frame,
                        hide_index=True,
                        use_container_width=True,
                    )
                    st.download_button(
                        "Download R2 comparison CSV",
                        data=comparison_frame.to_csv(index=False).encode("utf-8"),
                        file_name="dti_r2_run_comparison.csv",
                        mime="text/csv",
                        key="perfect_fit_r2_comparison_csv_download_v1",
                        width="stretch",
                    )
        loaded_r2_error = st.session_state.get(
            "perfect_fit_loaded_r2_artifact_error_v1"
        )
        if isinstance(loaded_r2_error, dict):
            st.error("R2 artifact load failed.")
            render_safe_json(loaded_r2_error)
        loaded_r2 = st.session_state.get("perfect_fit_loaded_r2_artifact_v1")
        if isinstance(loaded_r2, dict):
            st.markdown("### Loaded R2 artifact")
            render_safe_json(
                {
                    "run_id": loaded_r2.get("run_id"),
                    "route": loaded_r2.get("route"),
                    "artifact_sha256": loaded_r2.get("artifact_sha256"),
                    "created_at_utc": loaded_r2.get("created_at_utc"),
                    "storage": loaded_r2.get("storage"),
                }
            )

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
