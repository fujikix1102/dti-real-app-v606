from __future__ import annotations

import math
import os
import time
from typing import Any

import requests
import streamlit as st


DEFAULT_ENDPOINT = (
    "https://dti-class-api.onrender.com"
    "/axiclass/desi-dr2-bao"
)
REQUEST_TIMEOUT_SECONDS = 300
LOCKED_REQUEST_PAYLOAD = {
    "use_locked_baseline": True,
}


def _endpoint() -> str:
    env_value = os.environ.get(
        "DTI_PUBLIC_PHYSICAL_BAO_API_URL",
        "",
    ).strip()

    if env_value:
        return env_value

    try:
        secret_value = str(
            st.secrets.get(
                "DTI_PUBLIC_PHYSICAL_BAO_API_URL",
                "",
            )
        ).strip()

        if secret_value:
            return secret_value
    except Exception:
        pass

    return DEFAULT_ENDPOINT


def _formatted_number(
    value: Any,
    digits: int,
) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "n/a"

    if not math.isfinite(number):
        return "n/a"

    return f"{number:.{digits}f}"


def _failed_checks(value: Any) -> list[Any]:
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, dict):
        return [
            key
            for key, status in value.items()
            if status is not True
        ]

    return [value]


def _show_advanced(
    endpoint: str,
    response_body: dict[str, Any],
    client_elapsed: float,
) -> None:
    with st.expander(
        "Advanced runtime details",
        expanded=False,
    ):
        st.markdown("**Endpoint**")
        st.code(endpoint, language="text")

        st.markdown("**Submitted request**")
        st.json(LOCKED_REQUEST_PAYLOAD)

        st.markdown("**Client elapsed time**")
        st.code(
            f"{client_elapsed:.9f} seconds",
            language="text",
        )

        st.markdown("**Checks**")
        st.json(response_body.get("checks", {}))

        st.markdown("**Failed checks**")
        st.json(response_body.get("failed_checks", []))

        st.markdown("**Runtime identity**")
        st.json(response_body.get("identity", {}))

        st.markdown("**Boundary**")
        st.json(response_body.get("boundary", {}))

        st.markdown("**Result**")
        st.json(response_body.get("result", {}))

        st.markdown("**Complete backend response**")
        st.json(response_body)


st.set_page_config(
    page_title="DTI Physical BAO",
    layout="centered",
)

st.title("DTI Physical BAO")

st.caption(
    "Run the supported locked Linux AxiCLASS and Cobaya "
    "DESI DR2 BAO evaluation and review its core result."
)

st.info(
    "This public calculation uses one audited locked baseline. "
    "Scientific parameters are not editable in this version."
)

st.caption(
    "This is one locked-baseline physical BAO evaluation. "
    "It is not a sampler, posterior, MCMC result, "
    "historical-chain reproduction, normalized likelihood, "
    "Planck likelihood, or EDE-branch result. "
    "The value 30.06 remains forbidden."
)

endpoint = _endpoint()

run_clicked = st.button(
    "Run locked physical BAO check",
    key="dti_simple_physical_bao_run_v1",
    type="primary",
    use_container_width=True,
)

if run_clicked:
    started = time.time()

    try:
        with st.spinner(
            "Calling the Linux AxiCLASS backend. "
            "A cold start may take several minutes."
        ):
            response = requests.post(
                endpoint,
                json=LOCKED_REQUEST_PAYLOAD,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )

        client_elapsed = time.time() - started

        try:
            parsed_body = response.json()

            if isinstance(parsed_body, dict):
                body: dict[str, Any] = parsed_body
            else:
                body = {
                    "status": "invalid_json_shape",
                    "response": parsed_body,
                }
        except Exception:
            body = {
                "status": "non_json_response",
                "text": response.text[:8000],
            }

        if not response.ok:
            st.error(
                f"Backend HTTP {response.status_code}"
            )
            _show_advanced(
                endpoint,
                body,
                client_elapsed,
            )
            st.stop()

        status = str(
            body.get(
                "status",
                "unknown",
            )
        )

        if status == "ok":
            st.success("Physical provider runtime PASS")
        elif status == "busy":
            st.warning(
                "The backend is busy with another physical solver "
                "request. Retry manually after it completes."
            )
        elif status == "rejected":
            st.error(
                "The backend rejected the request under its locked "
                "execution contract."
            )
        else:
            st.error(
                f"Physical provider runtime status: {status}"
            )

        result_raw = body.get("result", {})
        result = (
            result_raw
            if isinstance(result_raw, dict)
            else {}
        )

        failed = _failed_checks(
            body.get("failed_checks", [])
        )

        runtime_value = body.get(
            "runtime_sec",
            client_elapsed,
        )

        metric_row_1 = st.columns(2)

        metric_row_1[0].metric(
            "rdrag [Mpc]",
            _formatted_number(
                result.get("rdrag_Mpc"),
                9,
            ),
        )

        metric_row_1[1].metric(
            "BAO log-likelihood",
            _formatted_number(
                result.get("model_loglike"),
                12,
            ),
        )

        metric_row_2 = st.columns(2)

        metric_row_2[0].metric(
            "BAO chi-square",
            _formatted_number(
                result.get("model_chi2"),
                12,
            ),
        )

        metric_row_2[1].metric(
            "Runtime [s]",
            _formatted_number(
                runtime_value,
                6,
            ),
        )

        st.metric(
            "Failed checks",
            str(len(failed)),
        )

        if failed:
            st.error(
                "One or more runtime validation checks failed. "
                "Review the advanced details."
            )

        _show_advanced(
            endpoint,
            body,
            client_elapsed,
        )

    except requests.Timeout as exc:
        client_elapsed = time.time() - started

        st.error(
            "The backend request timed out. This is infrastructure "
            "state, not model failure."
        )

        _show_advanced(
            endpoint,
            {
                "status": "timeout",
                "error_type": type(exc).__name__,
                "message": str(exc),
                "boundary": {
                    "infrastructure_state": True,
                    "model_failure": False,
                },
            },
            client_elapsed,
        )

    except requests.RequestException as exc:
        client_elapsed = time.time() - started

        st.error(
            "The backend request could not be completed."
        )

        _show_advanced(
            endpoint,
            {
                "status": "request_exception",
                "error_type": type(exc).__name__,
                "message": str(exc),
                "boundary": {
                    "infrastructure_state": True,
                    "model_failure": False,
                },
            },
            client_elapsed,
        )

with st.expander(
    "Full audit workspace",
    expanded=False,
):
    st.write(
        "The complete research and provenance workspace remains "
        "preserved in app.py. It is not loaded by this simple "
        "entrypoint."
    )
