from __future__ import annotations

import requests
import streamlit as st

from dti_ui_v1.services.general_class_compute_service import (
    DEFAULT_CLASS_ENDPOINT,
    LOCAL_CLASS_ENDPOINT,
)
from dti_ui_v1.services.run_store import (
    get_run_artifact_store_status,
    list_run_artifacts,
)


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
    artifact_store = get_run_artifact_store_status()
    general = st.session_state.get("general_class_compute_history_v1", [])
    locked = st.session_state.get("perfect_fit_locked_compute_result")
    columns = st.columns(4)
    columns[0].metric(BACKEND_LABEL, backend)
    columns[1].metric("Backend version", version)
    columns[2].metric("Runtime artifact files", len(artifacts))
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

    # BEGIN APP_READONLY_RUNTIME_SMOKE_PANEL_DASHBOARD_V1
    # Read-only frozen CLASS/classy runtime smoke display.
    # No input widgets.
    # No buttons.
    # No CLASS call.
    # No compute().
    # No get_background().
    # No likelihood/posterior/chi2/MCMC.

    st.divider()

    st.markdown("### CLASS / classy runtime smoke status")

    st.caption(
        "RUNTIME SMOKE ONLY / NOT LIKELIHOOD / "
        "NOT POSTERIOR / NOT CHI2 / NO MCMC"
    )

    with st.expander(
        "CLASS / classy runtime smoke identity and frozen values",
        expanded=True
    ):

        st.caption("Runtime identity")

        st.table([
            {
                "key": "classy_so_sha256",
                "value": "a40752db43ea56f1291d63482a357f000f7345f09402a4e449495f155a6a294f",
            },
            {
                "key": "background_c_sha256",
                "value": "0134082fdc09dfdff27b4a672e76a76c724bc3ccac63d12ead0053cb4d9854dd",
            },
            {
                "key": "classy_pyx_sha256",
                "value": "88a794b02c31d29d75fde2665c41d68dcadfdf563a054535e762677383621b1d",
            },
        ])

        st.caption("Frozen runtime smoke values")

        st.table([
            {
                "quantity": "rs_drag",
                "value": "147.11418585917818",
            },
            {
                "quantity": "H [1/Mpc] first3",
                "value": "2.1572562928018544e+22, 2.15378192038101e+22, 2.1503131436160117e+22",
            },
        ])

        st.caption(
            "Display-only frozen runtime smoke record. "
            "No computation is executed."
        )

    # END APP_READONLY_RUNTIME_SMOKE_PANEL_DASHBOARD_V1


    # BEGIN A_DTI_PARAMETER_INPUT_UI_IMPLEMENTATION_V1
    # Input display only.
    # No automatic compute.
    # No likelihood.
    # No posterior.
    # No MCMC.

    st.markdown("### A_DTI parameter input")

    a_dti_value = st.number_input(
        "A_DTI",
        min_value=0.0,
        value=0.0,
        step=1e-8,
        format="%.8e",
        help="Parameter input only. No automatic compute execution."
    )

    st.caption(
        f"A_DTI current input: {a_dti_value}. "
        "Baseline reference remains A_DTI=0.0."
    )

    # END A_DTI_PARAMETER_INPUT_UI_IMPLEMENTATION_V1

    st.markdown("## Recent runtime artifacts")
    st.caption(
        f"Store: {artifact_store.get('persistence')} · "
        f"{artifact_store.get('artifact_directory')}. "
        "Counts are for this running app filesystem only."
    )
    if (
        artifact_store.get("persistence")
        == "ephemeral_streamlit_runtime"
    ):
        st.warning(
            "This public Streamlit runtime store is ephemeral and separate "
            "from any local data/run_artifacts directory."
        )
    if artifacts:
        st.dataframe(artifacts, hide_index=True, use_container_width=True)
    else:
        st.info("No run artifact is visible in this runtime store yet.")
