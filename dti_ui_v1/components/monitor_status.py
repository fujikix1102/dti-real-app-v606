"""Live session monitor for the two supported compute routes."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import pandas as pd
import requests
import streamlit as st

from dti_ui_v1.services.general_class_compute_service import (
    DEFAULT_CLASS_ENDPOINT,
    LOCAL_CLASS_ENDPOINT,
)
from dti_ui_v1.services.run_store import list_run_artifacts


GENERAL_HISTORY_KEY = "general_class_compute_history_v1"
LOCKED_RESULT_KEY = "perfect_fit_locked_compute_result"
LOCKED_ERROR_KEY = "perfect_fit_locked_compute_error"
HEALTH_ENDPOINT = DEFAULT_CLASS_ENDPOINT.replace("/class/compute", "/health")
BACKEND_LABEL = "Local backend" if DEFAULT_CLASS_ENDPOINT == LOCAL_CLASS_ENDPOINT else "Compute backend"
REPO_ROOT = Path(__file__).resolve().parents[2]


@st.cache_data(ttl=5, show_spinner=False)
def _health() -> dict[str, Any]:
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=1.5)
        body = response.json()
    except Exception as exc:
        return {"online": False, "status": "unreachable", "detail": str(exc)}

    return {
        "online": response.ok and body.get("status") == "ok",
        "status": body.get("status", f"http_{response.status_code}"),
        "version": body.get("version"),
        "classy_available": body.get("classy_available"),
        "detail": body.get("classy_import_error", ""),
    }


def _general_history() -> list[Mapping[str, Any]]:
    value = st.session_state.get(GENERAL_HISTORY_KEY, [])
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, Mapping)]


def _evidence_candidates() -> tuple[tuple[str, Path], ...]:
    return (
        ("DESI DR2 confirmation JSON", REPO_ROOT / "data/evidence/desi_dr2_bao_external_confirmation_v1.json"),
        ("DESI DR2 confirmation TSV", REPO_ROOT / "data/evidence/desi_dr2_bao_external_confirmation_v1.tsv"),
        ("Fixed-H0 BAO manifest", REPO_ROOT / "assets/fixed_h0_bao_r1/v1/fixed_h0_bao_r1_asset_manifest_v1.tsv"),
        ("Graph migration ledger", REPO_ROOT / "graph_migration/GRAPH_MIGRATION_LEDGER.tsv"),
        ("Hubble ladder comparison contract", REPO_ROOT / "data/research/hubble_ladder_anchors.json"),
    )


def _component_status(response: Mapping[str, Any], key: str) -> str:
    component = response.get(key, {})
    if not isinstance(component, Mapping):
        return "UNAVAILABLE"
    return str(component.get("status", "unavailable")).upper()


def _display_value(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "YES" if value else "NO"
    if isinstance(value, float):
        return f"{value:.8g}"
    return str(value)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _evidence_rows() -> pd.DataFrame:
    rows = []
    for label, path in _evidence_candidates():
        exists = path.is_file()
        rows.append(
            {
                "Record": label,
                "Status": "AVAILABLE" if exists else "MISSING",
                "Bytes": path.stat().st_size if exists else None,
                "SHA256": _sha256(path) if exists else "",
                "Path": str(path.relative_to(REPO_ROOT)) if exists else str(path),
            }
        )
    return pd.DataFrame(rows)


def render_monitor_status() -> None:
    health = _health()
    history = _general_history()
    latest = history[-1] if history else None
    latest_response = latest.get("response", {}) if latest else {}
    if not isinstance(latest_response, Mapping):
        latest_response = {}
    locked = st.session_state.get(LOCKED_RESULT_KEY)
    locked_error = st.session_state.get(LOCKED_ERROR_KEY)
    online = bool(health.get("online"))
    completed = int(latest is not None) + int(isinstance(locked, Mapping))
    evidence = _evidence_rows()
    artifacts = list_run_artifacts()
    missing = int((evidence["Status"] == "MISSING").sum())

    st.header("Session monitor")
    st.caption("Live state for this browser session and the two isolated routes.")

    cards = st.columns(4)
    cards[0].metric(BACKEND_LABEL, "ONLINE" if online else "OFFLINE")
    cards[1].metric("Completed routes", completed)
    cards[2].metric("General runs retained", len(history))
    cards[3].metric("Saved run artifacts", len(artifacts))

    session_tab, routes_tab, evidence_tab, audit_tab = st.tabs(
        ("Current session", "Route activity", "Evidence records", "Audit log")
    )

    with session_tab:
        st.dataframe(
            [
                {"Item": "General CLASS / AxiCLASS backend", "Value": "ONLINE" if online else "OFFLINE"},
                {"Item": "General calculation", "Value": "SUCCESS" if latest else "NOT RUN IN THIS SESSION"},
                {"Item": "Locked baseline calculation", "Value": "SUCCESS" if isinstance(locked, Mapping) else ("FAILED" if locked_error else "NOT RUN IN THIS SESSION")},
                {"Item": "DESI DR2 likelihood", "Value": _component_status(latest_response, "desi_dr2_bao") if latest else "NOT RUN IN THIS SESSION"},
                {"Item": "Planck 2018 likelihood", "Value": _component_status(latest_response, "planck_2018") if latest else "NOT RUN IN THIS SESSION"},
                {"Item": "Pantheon+ likelihood", "Value": _component_status(latest_response, "pantheon_plus") if latest else "NOT RUN IN THIS SESSION"},
                {"Item": "Posterior / MCMC", "Value": "NOT EXECUTED"},
            ],
            hide_index=True,
            use_container_width=True,
        )

        if latest:
            response = latest_response
            submitted = latest.get("submitted_payload", {})
            derived = response.get("derived", {}) if isinstance(response, Mapping) else {}
            boundary = response.get("boundary", {}) if isinstance(response, Mapping) else {}
            st.markdown("**Latest General CLASS / AxiCLASS run**")
            latest_frame = pd.DataFrame(
                [
                    {"Item": "Engine", "Value": response.get("engine")},
                    {"Item": "Requested f_EDE", "Value": submitted.get("f_EDE")},
                    {"Item": "Achieved f_EDE", "Value": derived.get("f_EDE_AxiCLASS")},
                    {"Item": "Requested z_c", "Value": submitted.get("z_c")},
                    {"Item": "Achieved z_c", "Value": derived.get("z_c_AxiCLASS")},
                    {"Item": "EDE microphysics", "Value": boundary.get("ede_microphysics_activated")},
                ]
            )
            latest_frame["Value"] = latest_frame["Value"].map(_display_value)
            st.dataframe(
                latest_frame,
                hide_index=True,
                use_container_width=True,
            )

    with routes_tab:
        st.dataframe(
            [
                {
                    "Route": "General CLASS / AxiCLASS",
                    "Backend": "ONLINE" if online else "OFFLINE",
                    "Session result": "SUCCESS" if latest else "NONE",
                    "Likelihood": (
                        f"DESI={_component_status(latest_response, 'desi_dr2_bao')} · "
                        f"Planck={_component_status(latest_response, 'planck_2018')} · "
                        f"Pantheon+={_component_status(latest_response, 'pantheon_plus')}"
                        if latest else "NOT RUN"
                    ),
                },
                {
                    "Route": "Locked baseline DESI DR2 BAO",
                    "Backend": "REMOTE FIXED CONTRACT",
                    "Session result": "SUCCESS" if isinstance(locked, Mapping) else "NONE",
                    "Likelihood": "FIXED DESI DR2 BAO",
                },
            ],
            hide_index=True,
            use_container_width=True,
        )
        with st.expander("Backend health details", expanded=False):
            st.json(health)

    with evidence_tab:
        display = evidence.copy()
        display["Bytes"] = display["Bytes"].map(lambda value: "" if pd.isna(value) else f"{int(value):,}")
        display["SHA256"] = display["SHA256"].map(lambda value: value if not value else f"{value[:16]}…{value[-8:]}")
        st.dataframe(display, hide_index=True, use_container_width=True)
        if artifacts:
            st.markdown("**Durable run artifacts**")
            st.dataframe(artifacts, hide_index=True, use_container_width=True)

    with audit_tab:
        latest_boundary = latest_response.get("boundary", {}) if isinstance(latest_response, Mapping) else {}
        lines = [
            f"rendered_at_utc={datetime.now(timezone.utc).isoformat()}",
            f"local_backend_online={'YES' if online else 'NO'}",
            f"general_run_count_retained={len(history)}",
            f"general_axiclass_execution={'YES' if latest else 'NO'}",
            f"ede_microphysics_activated={latest_boundary.get('ede_microphysics_activated', 'NOT_RUN')}",
            f"general_desi_bao_likelihood={'YES' if _component_status(latest_response, 'desi_dr2_bao') == 'OK' else 'NO'}",
            f"planck_likelihood_execution={'YES' if _component_status(latest_response, 'planck_2018') == 'OK' else 'NO'}",
            f"pantheon_plus_likelihood_execution={'YES' if _component_status(latest_response, 'pantheon_plus') == 'OK' else 'NO'}",
            f"locked_bao_execution={'YES' if isinstance(locked, Mapping) else 'NO'}",
            "posterior_execution=NO",
            "mcmc_execution=NO",
        ]
        st.code("\n".join(lines), language="text")
        st.success("The monitor now reports actual session execution instead of a fixed offline placeholder.")
