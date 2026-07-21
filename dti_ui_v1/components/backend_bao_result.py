from __future__ import annotations

import streamlit as st

from dti_ui_v1.services.locked_bao_client import (
    LockedBaoRequest,
    execute_locked_bao_request,
)


def render_backend_bao_result() -> None:
    st.subheader("Backend BAO Single Point Record")

    request = LockedBaoRequest(
        endpoint=(
            "https://dti-class-api.onrender.com/"
            "axiclass/desi-dr2-bao"
        ),
        timeout_seconds=120,
    )

    st.caption(
        "Single backend request record. "
        "NO_CLAIM. No posterior/MCMC."
    )

    if st.button(
        "Run locked BAO backend point",
        key="run_locked_bao_backend_point",
    ):
        try:
            import requests

            result = execute_locked_bao_request(
                request,
                post=requests.post,
            )

            st.json(
                {
                    "rdrag": result.rdrag,
                    "loglike": result.loglike,
                    "chi2": result.chi2,
                    "runtime_seconds": result.runtime_seconds,
                    "failed_checks": result.failed_checks,
                    "claim": "NO_CLAIM",
                }
            )

        except Exception as exc:
            st.error(str(exc))
