from __future__ import annotations

from typing import Any

import streamlit as st

from dti_ui_v1.services.perfect_fit_compute_service import compute_perfect_fit
from dti_ui_v1.services.perfect_fit_single_solver_adapter import LockedBaselineRequest
from dti_ui_v1.services.run_store import save_run_artifact

_RESULT_KEY = "perfect_fit_locked_compute_result"
_ERROR_KEY = "perfect_fit_locked_compute_error"


def _payload(result: Any) -> dict[str, Any]:
    value = result.as_dict()
    if not isinstance(value, dict):
        raise TypeError("adapter result must serialize to a dictionary")
    return value


def render_perfect_fit_compute_panel() -> None:
    st.subheader("Locked baseline DESI DR2 BAO compute")
    st.caption(
        "Executes the verified fixed baseline and its DESI DR2 BAO likelihood. "
        "No arbitrary parameters are accepted by this route."
    )
    timeout = st.number_input("HTTP timeout", 1, 600, 120, 1)
    st.code(
        "route=LOCKED_BASELINE_ONLY\nuse_locked_baseline=true\n"
        "arbitrary_parameter_execution=NO\nfallback_endpoint=NO\nretry=NO",
        language="text",
    )
    if st.button("Run locked baseline compute", type="primary", use_container_width=True):
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
                request={"use_locked_baseline": True},
                response=result_payload,
            )
        except Exception as exc:
            st.session_state[_ERROR_KEY] = {
                "exception_type": type(exc).__name__, "detail": str(exc)
            }

    if _ERROR_KEY in st.session_state:
        st.error("Locked baseline request failed.")
        st.json(st.session_state[_ERROR_KEY])

    result = st.session_state.get(_RESULT_KEY)
    if not isinstance(result, dict):
        return
    st.success(f"Adapter status: {result.get('status', 'UNSPECIFIED')}")
    response = result.get("validated_payload", {}).get("response", {})
    if isinstance(response, dict):
        columns = st.columns(3)
        columns[0].metric("DESI log likelihood", f"{float(response.get('model_loglike', 0)):.6f}")
        columns[1].metric("DESI chi-square", f"{float(response.get('model_chi2', 0)):.6f}")
        columns[2].metric("r_drag [Mpc]", f"{float(response.get('rdrag_Mpc', 0)):.6f}")
    artifact = st.session_state.get("perfect_fit_locked_artifact")
    if isinstance(artifact, dict):
        st.caption(
            f"Audit artifact saved · SHA-256 {artifact.get('artifact_sha256')} · "
            f"{artifact.get('path')}"
        )
    with st.expander("Complete validated adapter result"):
        st.json(result)
    st.caption(
        "The backend evaluates the fixed DESI DR2 BAO likelihood. The UI does "
        "not alter returned values and does not run Planck or posterior sampling."
    )
