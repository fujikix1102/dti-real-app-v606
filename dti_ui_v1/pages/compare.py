"""Comparison of the two most recent General CLASS / AxiCLASS runs."""

from __future__ import annotations

from typing import Any, Mapping

import altair as alt
import pandas as pd
import streamlit as st


HISTORY_KEY = "general_class_compute_history_v1"
T_CMB_SQUARED_UK2 = 2.7255**2 * 1.0e12


def _history() -> list[Mapping[str, Any]]:
    value = st.session_state.get(HISTORY_KEY, [])
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, Mapping)]


def _derived(item: Mapping[str, Any]) -> Mapping[str, Any]:
    response = item.get("response", {})
    value = response.get("derived", {}) if isinstance(response, Mapping) else {}
    return value if isinstance(value, Mapping) else {}


def _number(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def render() -> None:
    st.title("Compare")
    st.caption("Current and immediately preceding General CLASS / AxiCLASS runs")
    history = _history()
    if len(history) < 2:
        st.info("Run General CLASS / AxiCLASS twice to enable comparison. The two most recent runs are retained.")
        return

    previous, current = history[-2], history[-1]
    previous_input = previous.get("submitted_payload", {})
    current_input = current.get("submitted_payload", {})
    previous_derived = _derived(previous)
    current_derived = _derived(current)

    st.subheader("Input differences")
    input_rows = []
    for key in ("H0", "omega_b", "omega_cdm", "n_s", "ln10_10_As", "tau_reio", "f_EDE", "z_c"):
        old = _number(previous_input.get(key))
        new = _number(current_input.get(key))
        if old is not None and new is not None:
            input_rows.append({"Parameter": key, "Previous": old, "Current": new, "Delta": new - old})
    st.dataframe(input_rows, hide_index=True, use_container_width=True)

    st.subheader("Derived differences")
    derived_rows = []
    for label, key in (
        ("Omega_m", "Omega_m_computed"),
        ("sigma8", "sigma8_CLASS"),
        ("S8", "S8_CLASS"),
        ("r_drag [Mpc]", "rs_drag_Mpc_CLASS"),
        ("Age [Gyr]", "age_Gyr_CLASS"),
        ("f_EDE achieved", "f_EDE_AxiCLASS"),
        ("z_c achieved", "z_c_AxiCLASS"),
    ):
        old = _number(previous_derived.get(key))
        new = _number(current_derived.get(key))
        if old is not None and new is not None:
            derived_rows.append({"Quantity": label, "Previous": old, "Current": new, "Delta": new - old})
    st.dataframe(derived_rows, hide_index=True, use_container_width=True)

    previous_response = previous.get("response", {})
    current_response = current.get("response", {})
    likelihood_rows = []
    component_specs = (
        ("DESI DR2 BAO", "desi_dr2_bao", "loglike", "χ²", "chi2"),
        ("Planck 2018", "planck_2018", "loglike", "effective χ²", "chi2_effective"),
        ("Pantheon+ relative SN", "pantheon_plus", "loglike", "χ²", "chi2"),
        ("Independent component sum", "joint_likelihood", "loglike_sum", "effective χ² sum", "chi2_effective_sum"),
    )
    for dataset, response_key, loglike_key, chi2_label, chi2_key in component_specs:
        old_component = previous_response.get(response_key, {}) if isinstance(previous_response, Mapping) else {}
        new_component = current_response.get(response_key, {}) if isinstance(current_response, Mapping) else {}
        if not isinstance(old_component, Mapping) or not isinstance(new_component, Mapping):
            continue
        for label, key in (("log likelihood", loglike_key), (chi2_label, chi2_key)):
            old = _number(old_component.get(key))
            new = _number(new_component.get(key))
            if old is not None and new is not None:
                likelihood_rows.append(
                    {
                        "Dataset": dataset,
                        "Coordinate": label,
                        "Previous": old,
                        "Current": new,
                        "Delta": new - old,
                    }
                )
    if likelihood_rows:
        st.subheader("Likelihood-coordinate differences")
        st.dataframe(likelihood_rows, hide_index=True, use_container_width=True)
        st.caption(
            "The local distance-ladder comparison is intentionally excluded from this sum because it overlaps "
            "Pantheon+/SH0ES information. Use Consistency for the overlap-safe comparison rail."
        )

    old_ell = previous_derived.get("ell")
    new_ell = current_derived.get("ell")
    old_tt = previous_derived.get("dl_tt")
    new_tt = current_derived.get("dl_tt")
    if all(isinstance(value, list) for value in (old_ell, new_ell, old_tt, new_tt)):
        old_size = min(len(old_ell), len(old_tt))
        new_size = min(len(new_ell), len(new_tt))
        frame = pd.concat(
            [
                pd.DataFrame({"ell": old_ell[:old_size], "dl_tt_microK2": pd.Series(old_tt[:old_size]) * T_CMB_SQUARED_UK2, "Run": "Previous"}),
                pd.DataFrame({"ell": new_ell[:new_size], "dl_tt_microK2": pd.Series(new_tt[:new_size]) * T_CMB_SQUARED_UK2, "Run": "Current"}),
            ],
            ignore_index=True,
        )
        frame["ell"] = pd.to_numeric(frame["ell"], errors="coerce")
        frame["dl_tt_microK2"] = pd.to_numeric(frame["dl_tt_microK2"], errors="coerce")
        frame = frame.dropna(subset=["ell", "dl_tt_microK2"])
        frame = frame[(frame["ell"] >= 2) & (frame["ell"] <= 2500)]
        chart = (
            alt.Chart(frame)
            .mark_line()
            .encode(
                x=alt.X("ell:Q", title="Multipole ell", scale=alt.Scale(domain=[0, 2500], nice=False)),
                y=alt.Y("dl_tt_microK2:Q", title="D_ell TT [microK^2]"),
                color=alt.Color("Run:N", title="Run"),
            )
            .properties(height=420, title="TT spectrum comparison")
        )
        st.altair_chart(chart, use_container_width=True)

    st.caption(
        "This comparison includes deterministic DESI DR2, Planck 2018, and Pantheon+ pointwise likelihood coordinates. "
        "It is not a posterior, Bayes factor, or MCMC result."
    )
