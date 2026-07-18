"""Streamlit binding for the isolated Perfect Fit compute service.

Only the adapter's verified locked-baseline request is exposed here.
Arbitrary six-parameter execution is intentionally not implemented.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from dti_ui_v1.services.perfect_fit_compute_service import (
    compute_perfect_fit,
)
from dti_ui_v1.services.perfect_fit_single_solver_adapter import (
    LockedBaselineRequest,
)


_RESULT_KEY = "perfect_fit_locked_compute_result"
_ERROR_KEY = "perfect_fit_locked_compute_error"
_TIMEOUT_KEY = "perfect_fit_locked_compute_timeout"
_RUN_BUTTON_KEY = "perfect_fit_locked_compute_run"


def _as_display_payload(result: Any) -> dict[str, Any]:
    """Convert the adapter result to a Streamlit-safe mapping."""

    as_dict = getattr(result, "as_dict", None)

    if not callable(as_dict):
        raise TypeError(
            "compute_perfect_fit must return an adapter result "
            "with an as_dict() method"
        )

    payload = as_dict()

    if not isinstance(payload, dict):
        raise TypeError(
            "adapter result as_dict() must return a dictionary"
        )

    return payload


def render_perfect_fit_compute_panel() -> None:
    """Render and execute the verified locked-baseline route."""

    st.subheader("Locked baseline compute")

    st.caption(
        "This control calls the isolated Perfect Fit compute service. "
        "The request is restricted to the verified locked-baseline "
        "adapter contract."
    )

    timeout_seconds = st.number_input(
        "HTTP timeout",
        min_value=1,
        max_value=600,
        value=120,
        step=1,
        key=_TIMEOUT_KEY,
        help=(
            "Maximum client-side wait for the single configured "
            "backend request."
        ),
    )

    st.code(
        "\n".join(
            (
                "route=LOCKED_BASELINE_ONLY",
                "use_locked_baseline=true",
                "f_EDE=0.0",
                "z_c=None",
                "arbitrary_parameter_execution=NO",
                "fallback_endpoint=NO",
                "retry=NO",
            )
        ),
        language="text",
    )

    run_clicked = st.button(
        "Run locked baseline compute",
        key=_RUN_BUTTON_KEY,
        type="primary",
        use_container_width=True,
    )

    if run_clicked:
        st.session_state.pop(_RESULT_KEY, None)
        st.session_state.pop(_ERROR_KEY, None)

        request = LockedBaselineRequest(
            use_locked_baseline=True,
            timeout_seconds=float(timeout_seconds),
            f_EDE=0.0,
            z_c=None,
        )

        try:
            with st.spinner(
                "Submitting the verified locked-baseline request..."
            ):
                result = compute_perfect_fit(
                    request=request,
                )

            st.session_state[_RESULT_KEY] = (
                _as_display_payload(result)
            )

        except Exception as exc:
            st.session_state[_ERROR_KEY] = {
                "exception_type": type(exc).__name__,
                "detail": str(exc),
            }

    error_payload = st.session_state.get(_ERROR_KEY)

    if error_payload is not None:
        st.error("Compute request failed before a valid result was loaded.")
        st.json(error_payload)

    result_payload = st.session_state.get(_RESULT_KEY)

    if result_payload is not None:
        status = result_payload.get(
            "status",
            "UNSPECIFIED",
        )

        st.info(f"Adapter status: {status}")

        st.markdown("#### Adapter result")
        st.json(result_payload)

        st.caption(
            "Displayed values are accepted exactly as returned by the "
            "verified adapter. This panel does not perform likelihood, "
            "posterior, MCMC, or additional scientific interpretation."
        )
