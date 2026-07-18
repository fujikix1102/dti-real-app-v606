from __future__ import annotations

from typing import Any, Mapping

import streamlit as st

from dti_ui_v1.services.general_class_compute_service import (
    GeneralClassRequest,
    execute_general_class_compute,
)


def _first_value(
    payload: Mapping[str, Any],
    *keys: str,
) -> Any:
    for key in keys:
        if key in payload:
            return payload[key]

    result = payload.get("result")

    if isinstance(result, Mapping):
        for key in keys:
            if key in result:
                return result[key]

    return None


def render_general_class_compute_panel() -> None:
    st.subheader("General CLASS compute")

    st.caption(
        "Runs the backend /class/compute route with six editable "
        "ΛCDM-like parameters. This is separate from the locked "
        "DESI DR2 BAO likelihood route."
    )

    st.warning(
        "f_EDE and z_c are not active EDE microphysics in this "
        "backend. They are not exposed as scientific controls here."
    )

    column_1, column_2, column_3 = st.columns(3)

    with column_1:
        H0 = st.number_input(
            "H0",
            min_value=1.0,
            max_value=150.0,
            value=72.9,
            step=0.1,
            format="%.6f",
            key="perfect_fit_general_class_H0_v1",
        )

        omega_b = st.number_input(
            "omega_b",
            min_value=0.000001,
            max_value=1.0,
            value=0.02440,
            step=0.00001,
            format="%.8f",
            key="perfect_fit_general_class_omega_b_v1",
        )

    with column_2:
        omega_cdm = st.number_input(
            "omega_cdm",
            min_value=0.000001,
            max_value=2.0,
            value=0.12700,
            step=0.0001,
            format="%.8f",
            key="perfect_fit_general_class_omega_cdm_v1",
        )

        n_s = st.number_input(
            "n_s",
            min_value=0.1,
            max_value=2.0,
            value=0.9847,
            step=0.0001,
            format="%.8f",
            key="perfect_fit_general_class_n_s_v1",
        )

    with column_3:
        ln10_10_As = st.number_input(
            "ln(10¹⁰ A_s)",
            min_value=0.0,
            max_value=10.0,
            value=3.058,
            step=0.001,
            format="%.8f",
            key="perfect_fit_general_class_ln10_10_As_v1",
        )

        tau_reio = st.number_input(
            "tau_reio",
            min_value=0.0,
            max_value=1.0,
            value=0.0511,
            step=0.0001,
            format="%.8f",
            key="perfect_fit_general_class_tau_reio_v1",
        )

    run_requested = st.button(
        "Run general CLASS computation",
        type="primary",
        key="perfect_fit_general_class_run_v1",
    )

    if not run_requested:
        return

    request = GeneralClassRequest(
        H0=float(H0),
        omega_b=float(omega_b),
        omega_cdm=float(omega_cdm),
        n_s=float(n_s),
        ln10_10_As=float(ln10_10_As),
        tau_reio=float(tau_reio),
    )

    with st.spinner("Calling the CLASS backend..."):
        result = execute_general_class_compute(request)

    st.markdown("**Submitted parameters**")
    st.json(dict(result.submitted_payload))

    if not result.accepted:
        st.error(
            f"General CLASS request failed: {result.status}"
        )
        st.caption(result.detail)
        st.json(dict(result.response_payload))
        return

    st.success("General CLASS computation accepted.")

    response = result.response_payload

    metric_specs = (
        ("H0", "H0"),
        ("Omega_m", "omega_m", "Omega_m"),
        ("r_drag [Mpc]", "rdrag_Mpc", "r_drag", "rs_drag"),
        ("Age [Gyr]", "age_Gyr", "age"),
    )

    metrics = []

    for spec in metric_specs:
        label = spec[0]
        value = _first_value(response, *spec[1:])

        if value is not None:
            metrics.append((label, value))

    if metrics:
        columns = st.columns(min(4, len(metrics)))

        for index, (label, value) in enumerate(metrics):
            columns[index % len(columns)].metric(
                label,
                str(value),
            )

    st.markdown("**Backend response**")
    st.json(dict(response))

    st.caption(
        "Boundary: this panel demonstrates direct CLASS parameter "
        "propagation. It is not the locked DESI DR2 BAO likelihood, "
        "not a posterior, not MCMC, and not an EDE implementation."
    )
