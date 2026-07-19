"""Live execution-contract status for supported compute routes."""

from __future__ import annotations

from typing import Any, Mapping

import pandas as pd
import requests
import streamlit as st

from dti_ui_v1.services.general_class_compute_service import (
    DEFAULT_CLASS_ENDPOINT,
    LOCAL_CLASS_ENDPOINT,
)


HISTORY_KEY = "general_class_compute_history_v1"
HEALTH_ENDPOINT = DEFAULT_CLASS_ENDPOINT.replace(
    "/class/compute",
    "/health",
)
BACKEND_LABEL = "Local backend" if DEFAULT_CLASS_ENDPOINT == LOCAL_CLASS_ENDPOINT else "Compute backend"


@st.cache_data(ttl=5, show_spinner=False)
def _backend_health() -> dict[str, Any]:
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=1.5)
        body = response.json()
    except Exception as exc:
        return {
            "online": False,
            "status": "unreachable",
            "detail": str(exc),
        }

    return {
        "online": response.ok and body.get("status") == "ok",
        "status": body.get("status", f"http_{response.status_code}"),
        "version": body.get("version"),
        "classy_available": body.get("classy_available"),
        "detail": body.get("classy_import_error", ""),
    }


def _latest_general_run() -> Mapping[str, Any] | None:
    history = st.session_state.get(HISTORY_KEY, [])

    if not isinstance(history, list) or not history:
        return None

    latest = history[-1]
    return latest if isinstance(latest, Mapping) else None


def _display_value(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "YES" if value else "NO"
    if isinstance(value, float):
        return f"{value:.8g}"
    return str(value)


def render_execution_status() -> None:
    health = _backend_health()
    latest = _latest_general_run()
    online = bool(health.get("online"))
    latest_response = latest.get("response", {}) if latest else {}
    if not isinstance(latest_response, Mapping):
        latest_response = {}
    component_statuses = []
    for key in ("desi_dr2_bao", "planck_2018", "pantheon_plus"):
        component = latest_response.get(key, {})
        component_statuses.append(component.get("status") if isinstance(component, Mapping) else None)
    likelihood_ok_count = sum(status == "ok" for status in component_statuses)

    st.header("Execution contract")
    st.caption(
        "Live status for two verified execution routes. The locked baseline "
        "remains separate; the general route reports a three-component "
        "single-point likelihood."
    )

    cards = st.columns(4)
    cards[0].metric(
        BACKEND_LABEL,
        "ONLINE" if online else "OFFLINE",
        help=HEALTH_ENDPOINT,
    )
    cards[1].metric(
        "General solver",
        "AXICLASS EDE" if online else "UNAVAILABLE",
        help="f_EDE > 0 activates the axion-like scalar-field branch.",
    )
    cards[2].metric(
        "General likelihoods",
        f"{likelihood_ok_count}/3 OK" if latest else ("READY" if online else "UNAVAILABLE"),
        help="DESI DR2 BAO, Planck 2018, and Pantheon+ are independently status-checked.",
    )
    cards[3].metric(
        "Posterior / MCMC",
        "DISABLED",
        help="No sampler contract is active.",
    )

    st.subheader("Verified route contracts")
    contracts = pd.DataFrame(
        [
            {
                "Route": "General CLASS / AxiCLASS",
                "Endpoint": DEFAULT_CLASS_ENDPOINT,
                "State": "READY" if online else "OFFLINE",
                "Physical solver": "AxiCLASS EDE when f_EDE > 0; LCDM-like when f_EDE = 0",
                "Likelihood": "DESI DR2 BAO + Planck 2018 + Pantheon+",
                "Posterior": "None",
            },
            {
                "Route": "Locked baseline DESI DR2 BAO",
                "Endpoint": "https://dti-class-api.onrender.com/axiclass/desi-dr2-bao",
                "State": "LOCKED VERIFIED CONTRACT",
                "Physical solver": "Fixed LCDM-like baseline",
                "Likelihood": "Fixed DESI DR2 BAO component",
                "Posterior": "None",
            },
        ]
    )
    st.dataframe(contracts, hide_index=True, use_container_width=True)

    st.subheader("Execution pipeline")
    general_completed = latest is not None
    if not general_completed:
        general_likelihood_state = "READY" if online else "BLOCKED"
    elif likelihood_ok_count == 3:
        general_likelihood_state = "SUCCESS — 3/3"
    else:
        general_likelihood_state = f"PARTIAL — {likelihood_ok_count}/3"
    pipeline = pd.DataFrame(
        [
            {
                "Stage": "① Validate parameters",
                "General AxiCLASS": "READY" if online else "BLOCKED",
                "Locked BAO": "LOCKED",
            },
            {
                "Stage": "② Submit backend request",
                "General AxiCLASS": "SUCCESS" if general_completed else ("READY" if online else "BLOCKED"),
                "Locked BAO": "AVAILABLE",
            },
            {
                "Stage": "③ Physical solver",
                "General AxiCLASS": "SUCCESS" if general_completed else ("READY" if online else "BLOCKED"),
                "Locked BAO": "FIXED BASELINE",
            },
            {
                "Stage": "④ Likelihood",
                "General AxiCLASS": general_likelihood_state,
                "Locked BAO": "FIXED DESI DR2 BAO",
            },
            {
                "Stage": "⑤ Posterior / MCMC",
                "General AxiCLASS": "DISABLED",
                "Locked BAO": "DISABLED",
            },
            {
                "Stage": "⑥ Export results",
                "General AxiCLASS": "READY" if general_completed else "AFTER RUN",
                "Locked BAO": "JSON RESPONSE",
            },
        ]
    )
    st.dataframe(pipeline, hide_index=True, use_container_width=True)

    st.subheader("Current session")

    if latest is None:
        st.info("No General AxiCLASS calculation has been recorded in this browser session yet.")
    else:
        response = latest.get("response", {})
        submitted = latest.get("submitted_payload", {})
        derived = response.get("derived", {}) if isinstance(response, Mapping) else {}
        boundary = response.get("boundary", {}) if isinstance(response, Mapping) else {}
        bao = response.get("desi_dr2_bao", {}) if isinstance(response, Mapping) else {}
        planck = response.get("planck_2018", {}) if isinstance(response, Mapping) else {}
        pantheon = response.get("pantheon_plus", {}) if isinstance(response, Mapping) else {}
        joint = response.get("joint_likelihood", {}) if isinstance(response, Mapping) else {}
        session = pd.DataFrame(
            [
                {"Item": "Backend status", "Value": response.get("status")},
                {"Item": "Engine", "Value": response.get("engine")},
                {"Item": "Requested f_EDE", "Value": submitted.get("f_EDE")},
                {"Item": "Achieved f_EDE", "Value": derived.get("f_EDE_AxiCLASS")},
                {"Item": "Requested z_c", "Value": submitted.get("z_c")},
                {"Item": "Achieved z_c", "Value": derived.get("z_c_AxiCLASS")},
                {
                    "Item": "EDE microphysics activated",
                    "Value": boundary.get("ede_microphysics_activated"),
                },
                {"Item": "DESI DR2 BAO status", "Value": bao.get("status") if isinstance(bao, Mapping) else None},
                {"Item": "DESI DR2 BAO chi-square", "Value": bao.get("chi2") if isinstance(bao, Mapping) else None},
                {"Item": "Planck 2018 status", "Value": planck.get("status") if isinstance(planck, Mapping) else None},
                {"Item": "Planck effective chi-square", "Value": planck.get("chi2_effective") if isinstance(planck, Mapping) else None},
                {"Item": "Pantheon+ status", "Value": pantheon.get("status") if isinstance(pantheon, Mapping) else None},
                {"Item": "Pantheon+ chi-square", "Value": pantheon.get("chi2") if isinstance(pantheon, Mapping) else None},
                {"Item": "Joint component count", "Value": joint.get("component_count") if isinstance(joint, Mapping) else None},
                {"Item": "Joint effective chi-square", "Value": joint.get("chi2_effective_sum") if isinstance(joint, Mapping) else None},
                {"Item": "Posterior / MCMC", "Value": "NOT EXECUTED"},
            ]
        )
        session["Value"] = session["Value"].map(_display_value)
        st.dataframe(session, hide_index=True, use_container_width=True)

    with st.expander("Backend health details", expanded=False):
        st.json(health)

    st.subheader("Safety boundary")
    st.success("✓ General AxiCLASS physical recomputation — enabled on the local route")
    st.success("✓ DESI DR2 BAO likelihood — general AxiCLASS and verified locked-baseline contracts")
    st.success("✓ Planck 2018 and Pantheon+ — verified single-point likelihoods on the general route")
    st.info("Posterior inference, MCMC, Bayesian evidence, and discovery significance remain outside this application's installed scientific contract.")
