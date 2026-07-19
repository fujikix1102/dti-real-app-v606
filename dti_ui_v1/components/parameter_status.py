"""Route-aware parameter status for locked BAO and General AxiCLASS."""

from __future__ import annotations

from typing import Any, Mapping

import pandas as pd
import streamlit as st

from dti_ui_v1.contracts.numeric_precision import BASELINE_CONTRACTS


HISTORY_KEY = "general_class_compute_history_v1"


def _latest() -> Mapping[str, Any] | None:
    history = st.session_state.get(HISTORY_KEY, [])
    if not isinstance(history, list) or not history:
        return None
    value = history[-1]
    return value if isinstance(value, Mapping) else None


def _general_working_rows() -> pd.DataFrame:
    specs = (
        ("H0", "perfect_fit_general_class_H0_v1", 72.9),
        ("omega_b", "perfect_fit_general_class_omega_b_v1", 0.0244),
        ("omega_cdm", "perfect_fit_general_class_omega_cdm_v1", 0.127),
        ("n_s", "perfect_fit_general_class_n_s_v1", 0.9847),
        ("ln(10^10 A_s)", "perfect_fit_general_class_ln10_10_As_v1", 3.058),
        ("tau_reio", "perfect_fit_general_class_tau_reio_v1", 0.0511),
        ("f_EDE", "perfect_fit_general_class_f_EDE_v2", 0.082),
        ("z_c", "perfect_fit_general_class_z_c_v2", 3500.0),
    )
    return pd.DataFrame(
        [
            {
                "Parameter": label,
                "Working value": st.session_state.get(key, default),
                "Backend binding": "ACTIVE ON GENERAL ROUTE",
            }
            for label, key, default in specs
        ]
    )


def render_parameter_status_panel() -> None:
    latest = _latest()
    latest_response = latest.get("response", {}) if latest else {}
    if not isinstance(latest_response, Mapping):
        latest_response = {}

    def component_state(key: str) -> str:
        component = latest_response.get(key, {})
        if not latest:
            return "EVALUATED ON EXECUTION"
        if not isinstance(component, Mapping):
            return "UNAVAILABLE"
        return str(component.get("status", "unavailable")).upper()
    st.subheader("Parameter contracts")
    st.caption("Parameter binding depends on the selected execution route.")

    cards = st.columns(4)
    cards[0].metric("General backend inputs", 8)
    cards[1].metric("Locked-route editable inputs", 0)
    cards[2].metric("General result", "LOADED" if latest else "NOT RUN")
    cards[3].metric("Posterior parameters", 0)

    general_tab, locked_tab, compatibility_tab = st.tabs(
        ("General CLASS / AxiCLASS", "Locked baseline BAO", "Compatibility")
    )

    with general_tab:
        st.success("These eight values are bound to the local /class/compute route.")
        st.dataframe(_general_working_rows(), hide_index=True, use_container_width=True)
        if latest:
            submitted = latest.get("submitted_payload", {})
            response = latest.get("response", {})
            derived = response.get("derived", {}) if isinstance(response, Mapping) else {}
            st.markdown("**Latest submitted and achieved EDE values**")
            st.dataframe(
                [
                    {"Quantity": "f_EDE", "Submitted": submitted.get("f_EDE"), "Achieved": derived.get("f_EDE_AxiCLASS")},
                    {"Quantity": "z_c", "Submitted": submitted.get("z_c"), "Achieved": derived.get("z_c_AxiCLASS")},
                ],
                hide_index=True,
                use_container_width=True,
            )

    with locked_tab:
        rows = [
            {
                "Parameter": contract.symbol,
                "Locked value": contract.source_text,
                "Backend binding": "FIXED LOCKED INPUT",
            }
            for contract in BASELINE_CONTRACTS.values()
        ]
        st.info("This route accepts only use_locked_baseline=true; arbitrary values are not forwarded.")
        st.dataframe(rows, hide_index=True, use_container_width=True)

    with compatibility_tab:
        st.dataframe(
            [
                {"Capability": "Editable LCDM-like parameters", "General route": "SUPPORTED", "Locked BAO route": "FIXED"},
                {"Capability": "AxiCLASS EDE: f_EDE and z_c", "General route": "SUPPORTED", "Locked BAO route": "NOT FORWARDED"},
                {"Capability": "CMB spectra", "General route": "SUPPORTED", "Locked BAO route": "NOT RETURNED"},
                {"Capability": "DESI DR2 BAO likelihood", "General route": component_state("desi_dr2_bao"), "Locked BAO route": "FIXED COMPONENT"},
                {"Capability": "Planck 2018 likelihood", "General route": component_state("planck_2018"), "Locked BAO route": "NOT EVALUATED"},
                {"Capability": "Pantheon+ relative-SN likelihood", "General route": component_state("pantheon_plus"), "Locked BAO route": "NOT EVALUATED"},
                {"Capability": "Local distance-ladder summaries", "General route": "COMPARISON ONLY", "Locked BAO route": "NOT COMBINED"},
                {"Capability": "Posterior / MCMC", "General route": "DISABLED", "Locked BAO route": "DISABLED"},
            ],
            hide_index=True,
            use_container_width=True,
        )
