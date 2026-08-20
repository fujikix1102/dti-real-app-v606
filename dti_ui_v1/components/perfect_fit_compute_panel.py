from __future__ import annotations

from typing import Any

import streamlit as st

from dti_ui_v1.services.perfect_fit_compute_service import compute_perfect_fit
from dti_ui_v1.services.perfect_fit_single_solver_adapter import LockedBaselineRequest
from dti_ui_v1.components.safe_json_display import render_safe_json

from dti_ui_v1.services.run_store import (
    get_run_artifact_store_status,
    save_run_artifact,
)

_RESULT_KEY = "perfect_fit_locked_compute_result"
_ERROR_KEY = "perfect_fit_locked_compute_error"
_LOCKED_A_DTI_KEY = "perfect_fit_locked_A_DTI_v1"


def _payload(result: Any) -> dict[str, Any]:
    value = result.as_dict()
    if not isinstance(value, dict):
        raise TypeError("adapter result must serialize to a dictionary")
    return value


def render_perfect_fit_compute_panel() -> None:
    st.session_state.setdefault(_LOCKED_A_DTI_KEY, 0.0)
    st.subheader("Locked baseline DESI DR2 BAO compute")

    st.info(
        "Workspace runtime notice: this view represents the deployed "
        "Streamlit runtime. Local development files, backups, and review "
        "packages are not included. Public runtime storage is separate "
        "from the local checkout and is not automatically synchronized."
    )
    st.caption(
        "Executes the verified fixed baseline and its DESI DR2 BAO likelihood. "
        "No arbitrary parameters are accepted by this route."
    )
    store_status = get_run_artifact_store_status()
    st.caption(
        f"Run artifact store: {store_status.get('persistence')} · "
        f"{store_status.get('artifact_directory')} · "
        f"files visible to this runtime: {store_status.get('artifact_count')}"
    )
    external_storage = store_status.get("external_storage", {})
    if isinstance(external_storage, dict):
        st.caption(
            "External artifact storage: "
            f"{external_storage.get('backend') or 'none'} · "
            f"configured={bool(external_storage.get('configured'))}"
        )
    if (
        store_status.get("persistence")
        == "ephemeral_streamlit_runtime"
    ):
        st.warning(
            "Public Streamlit artifacts are saved inside the current Streamlit "
            "runtime only. They do not update a separate local checkout's "
            "data/run_artifacts directory."
        )
    input_columns = st.columns(2)
    with input_columns[0]:
        st.number_input(
            "A_DTI",
            min_value=0.0,
            max_value=1.0,
            step=0.001,
            format="%.6f",
            key=_LOCKED_A_DTI_KEY,
            help="Recorded as a working PERFECT FIT input. Locked baseline backend execution remains fixed.",
        )
    with input_columns[1]:
        timeout = st.number_input("HTTP timeout", 1, 600, 120, 1)
    st.code(
        "route=LOCKED_BASELINE_ONLY\nuse_locked_baseline=true\n"
        "A_DTI_backend_binding=RECORDED_ONLY_NOT_FORWARDED\n"
        "arbitrary_parameter_execution=NO\nfallback_endpoint=NO\nretry=NO",
        language="text",
    )
    render_safe_json(
        {
            "model": "DTI PERFECT FIT locked baseline",
            "working_inputs": {
                "A_DTI": float(st.session_state[_LOCKED_A_DTI_KEY]),
                "timeout_seconds": float(timeout),
            },
            "will_compute": "YES fixed DESI DR2 BAO locked baseline only",
            "will_not_compute": [
                "NO arbitrary parameter execution",
                "NO MCMC",
                "NO posterior",
                "NO scan",
            ],
        }
    )
    confirmed = st.checkbox(
        "Confirm locked baseline single run contract",
        key="perfect_fit_locked_confirm_single_run_v1",
    )
    if not confirmed:
        st.info("Confirm the single run contract to enable the locked baseline run.")
    if st.button(
        "Run locked baseline compute",
        type="primary",
        width="stretch",
        disabled=not confirmed,
    ):
        st.session_state.pop(_RESULT_KEY, None)
        st.session_state.pop(_ERROR_KEY, None)
        request = LockedBaselineRequest(
            use_locked_baseline=True,
            timeout_seconds=float(timeout),
            f_EDE=0.0,
            z_c=None,
        )
        try:
            with st.spinner("Running verified locked baseline..."):
                result_payload = _payload(compute_perfect_fit(request=request))
            st.session_state[_RESULT_KEY] = result_payload
            st.session_state["perfect_fit_locked_artifact"] = save_run_artifact(
                route="locked_baseline_desi_dr2_bao",
                request={
                    "use_locked_baseline": True,
                    "A_DTI": float(st.session_state[_LOCKED_A_DTI_KEY]),
                    "input_contract": "A_DTI_recorded_only_locked_baseline_not_forwarded",
                },
                response=result_payload,
            )
        except Exception as exc:
            st.session_state[_ERROR_KEY] = {
                "exception_type": type(exc).__name__, "detail": str(exc)
            }

    if _ERROR_KEY in st.session_state:
        st.error("Locked baseline request failed.")
        render_safe_json(st.session_state[_ERROR_KEY])

    result = st.session_state.get(_RESULT_KEY)

    if isinstance(result, dict):
        st.success(f"Adapter status: {result.get('status', 'UNSPECIFIED')}")
        response = result.get("validated_payload", {}).get("response", {})
        if isinstance(response, dict):
            columns = st.columns(3)
            columns[0].metric("DESI log likelihood", f"{float(response.get('model_loglike', 0)):.6f}")
            columns[1].metric("DESI chi-square", f"{float(response.get('model_chi2', 0)):.6f}")
            columns[2].metric("r_drag [Mpc]", f"{float(response.get('rdrag_Mpc', 0)):.6f}")
    artifact = st.session_state.get("perfect_fit_locked_artifact")
    if isinstance(artifact, dict):
        storage = artifact.get("storage", {})
        persistence = (
            storage.get("persistence")
            if isinstance(storage, dict)
            else "unknown_runtime_store"
        )
        st.caption(
            f"Audit artifact saved in this app runtime · "
            f"SHA-256 {artifact.get('artifact_sha256')}"
        )
        st.markdown("### Latest Run")
        cards = st.columns(4)
        cards[0].metric("status", "SUCCESS")
        cards[1].metric("run_id", str(artifact.get("run_id", ""))[:18])
        cards[2].metric("artifact files", artifact.get("artifact_count", "n/a"))
        cards[3].metric("sha256", str(artifact.get("artifact_sha256", ""))[:12])
        render_safe_json(
            {
                "run_id": artifact.get("run_id"),
                "artifact_path_this_runtime": artifact.get("path"),
                "artifact_directory_this_runtime": artifact.get("artifact_directory"),
                "saved_artifact_count_this_runtime": artifact.get("artifact_count"),
                "A_DTI": float(st.session_state[_LOCKED_A_DTI_KEY]),
                "runtime_store": persistence,
                "external_storage": artifact.get("external_storage"),
                "local_checkout_sync": False,
                "boundary": (
                    "This count and path describe only the currently running "
                    "app filesystem. Streamlit Cloud /mount/src artifacts are "
                    "not automatically written back to a user's local checkout."
                ),
            }
        )
    with st.expander("Complete validated adapter result"):
        render_safe_json(result)
    st.caption(
        "The backend evaluates the fixed DESI DR2 BAO likelihood. The UI does "
        "not alter returned values and does not run Planck or posterior sampling."
    )
