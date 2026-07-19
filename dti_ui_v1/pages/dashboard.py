from __future__ import annotations

import requests
import streamlit as st

from dti_ui_v1.services.general_class_compute_service import (
    DEFAULT_CLASS_ENDPOINT,
    LOCAL_CLASS_ENDPOINT,
)
from dti_ui_v1.services.run_store import list_run_artifacts


HEALTH_ENDPOINT = DEFAULT_CLASS_ENDPOINT.replace("/class/compute", "/health")
BACKEND_LABEL = "Local backend" if DEFAULT_CLASS_ENDPOINT == LOCAL_CLASS_ENDPOINT else "Compute backend"


def _backend_status() -> tuple[str, str]:
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=2)
        body = response.json()
        if response.ok and body.get("status") == "ok":
            return "ONLINE", str(body.get("version", "unknown"))
    except Exception:
        pass
    return "OFFLINE", "unreachable"


def render() -> None:
    st.title("MAXOMEGA / DTI")
    st.caption("AxiCLASS propagation, joint observational scoring, comparison, and audit")
    backend, version = _backend_status()
    artifacts = list_run_artifacts()
    general = st.session_state.get("general_class_compute_history_v1", [])
    locked = st.session_state.get("perfect_fit_locked_compute_result")
    columns = st.columns(4)
    columns[0].metric(BACKEND_LABEL, backend)
    columns[1].metric("Backend version", version)
    columns[2].metric("Saved run artifacts", len(artifacts))
    columns[3].metric("Session results", len(general) + int(isinstance(locked, dict)))
    st.markdown("## Executable scope")
    st.dataframe(
        [
            {"Route": "General CLASS / AxiCLASS", "Physics": "LCDM or axion-like EDE", "Likelihood": "DESI DR2 + Planck 2018 + Pantheon+", "State": "Executable"},
            {"Route": "Locked baseline", "Physics": "Frozen LCDM-like baseline", "Likelihood": "DESI DR2 BAO", "State": "Executable"},
            {"Route": "Hubble Tension Atlas", "Physics": "Same-run propagation and residuals", "Likelihood": "Component and Δχ² views", "State": "Executable"},
            {"Route": "Hubble Consistency Engine", "Physics": "Cross-dataset trade-off audit", "Likelihood": "3 independent backend rails + 1 overlap-safe ladder comparison", "State": "Executable"},
            {"Route": "Posterior / MCMC", "Physics": "Requires joint likelihood and priors", "Likelihood": "Not claimed", "State": "Excluded from this application"},
        ],
        hide_index=True,
        use_container_width=True,
    )
    st.markdown("## Recent durable runs")
    if artifacts:
        st.dataframe(artifacts, hide_index=True, use_container_width=True)
    else:
        st.info("No saved run artifact yet. Execute either compute route.")
