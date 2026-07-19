"""Live scientific results from the current browser session."""

from __future__ import annotations

from typing import Any, Mapping

import altair as alt
import pandas as pd
import streamlit as st

from dti_ui_v1.components.fixed_h0_bao_charts import render_fixed_h0_bao_charts


HISTORY_KEY = "general_class_compute_history_v1"
LOCKED_RESULT_KEY = "perfect_fit_locked_compute_result"
T_CMB_SQUARED_UK2 = 2.7255**2 * 1.0e12


def _history() -> list[Mapping[str, Any]]:
    value = st.session_state.get(HISTORY_KEY, [])
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, Mapping)]


def _latest_response() -> Mapping[str, Any] | None:
    history = _history()
    if not history:
        return None
    response = history[-1].get("response")
    return response if isinstance(response, Mapping) else None


def _metric(response: Mapping[str, Any], key: str) -> Any:
    derived = response.get("derived", {})
    return derived.get(key) if isinstance(derived, Mapping) else None


def _display_value(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "YES" if value else "NO"
    if isinstance(value, float):
        return f"{value:.8g}"
    return str(value)


def _spectrum_frame(response: Mapping[str, Any], key: str) -> pd.DataFrame:
    derived = response.get("derived", {})
    if not isinstance(derived, Mapping):
        return pd.DataFrame()
    ell = derived.get("ell")
    values = derived.get(key)
    if not isinstance(ell, list) or not isinstance(values, list):
        return pd.DataFrame()
    size = min(len(ell), len(values))
    frame = pd.DataFrame({"ell": ell[:size], key: values[:size]})
    frame = frame.apply(pd.to_numeric, errors="coerce").dropna()
    return frame[(frame["ell"] >= 2) & (frame["ell"] <= 2500)]


def _render_overview(response: Mapping[str, Any] | None) -> None:
    if response is None:
        st.info("No General CLASS / AxiCLASS result is loaded. Run it from Compute → Execution.")
        return

    specs = (
        ("Omega_m", "Omega_m_computed"),
        ("sigma8", "sigma8_CLASS"),
        ("S8", "S8_CLASS"),
        ("r_drag [Mpc]", "rs_drag_Mpc_CLASS"),
        ("Age [Gyr]", "age_Gyr_CLASS"),
        ("f_EDE achieved", "f_EDE_AxiCLASS"),
        ("z_c achieved", "z_c_AxiCLASS"),
    )
    available = [(label, _metric(response, key)) for label, key in specs]
    available = [(label, value) for label, value in available if value is not None]
    columns = st.columns(min(5, max(1, len(available))))
    for index, (label, value) in enumerate(available):
        try:
            text = f"{float(value):.6g}"
        except (TypeError, ValueError):
            text = str(value)
        columns[index % len(columns)].metric(label, text)

    boundary = response.get("boundary", {})
    bao = response.get("desi_dr2_bao", {})
    overview_frame = pd.DataFrame(
        [
            {"Item": "Status", "Value": response.get("status")},
            {"Item": "Engine", "Value": response.get("engine")},
            {"Item": "EDE microphysics activated", "Value": boundary.get("ede_microphysics_activated") if isinstance(boundary, Mapping) else None},
            {"Item": "DESI DR2 BAO likelihood", "Value": bao.get("status") if isinstance(bao, Mapping) else "UNAVAILABLE"},
            {"Item": "DESI DR2 BAO chi-square", "Value": bao.get("chi2") if isinstance(bao, Mapping) else None},
            {"Item": "Planck 2018 likelihood", "Value": response.get("planck_2018", {}).get("status") if isinstance(response.get("planck_2018"), Mapping) else "UNAVAILABLE"},
            {"Item": "Pantheon+ likelihood", "Value": response.get("pantheon_plus", {}).get("status") if isinstance(response.get("pantheon_plus"), Mapping) else "UNAVAILABLE"},
            {"Item": "Posterior / MCMC", "Value": "NOT EXECUTED"},
        ]
    )
    overview_frame["Value"] = overview_frame["Value"].map(_display_value)
    st.dataframe(
        overview_frame,
        hide_index=True,
        use_container_width=True,
    )
    if isinstance(bao, Mapping) and isinstance(bao.get("theory_vector"), list):
        with st.expander("DESI DR2 BAO theory vector"):
            st.dataframe(bao["theory_vector"], hide_index=True, use_container_width=True)


def _render_cmb(response: Mapping[str, Any] | None) -> None:
    if response is None:
        st.info("No CMB result is loaded.")
        return
    for label, key in (("TT", "dl_tt"), ("TE", "dl_te"), ("EE", "dl_ee")):
        frame = _spectrum_frame(response, key)
        if frame.empty:
            continue
        value_key = "spectrum_microK2"
        frame[value_key] = frame[key] * T_CMB_SQUARED_UK2
        chart = (
            alt.Chart(frame)
            .mark_line()
            .encode(
                x=alt.X("ell:Q", title="Multipole ell", scale=alt.Scale(domain=[0, 2500], nice=False)),
                y=alt.Y(f"{value_key}:Q", title=f"D_ell {label} [microK^2]"),
                tooltip=[alt.Tooltip("ell:Q", format=".0f"), alt.Tooltip(f"{value_key}:Q", title=f"D_ell {label} [microK^2]", format=".6g")],
            )
            .properties(height=340, title=f"{label} spectrum")
        )
        st.altair_chart(chart, use_container_width=True)


def render() -> None:
    st.title("Results")
    st.caption("Results retained in the current browser session")
    response = _latest_response()
    locked = st.session_state.get(LOCKED_RESULT_KEY)
    overview_tab, cmb_tab, locked_tab, raw_tab = st.tabs(
        ("Overview", "General CMB", "Locked DESI DR2 BAO", "Raw")
    )
    with overview_tab:
        _render_overview(response)
    with cmb_tab:
        _render_cmb(response)
    with locked_tab:
        if isinstance(locked, Mapping):
            st.success("A locked-baseline result is loaded in this session.")
            st.json(dict(locked))
        else:
            st.info("No locked-baseline result is loaded in this session.")
        st.divider()
        render_fixed_h0_bao_charts()
    with raw_tab:
        if response is not None:
            st.markdown("**General CLASS / AxiCLASS response**")
            st.json(dict(response))
        if isinstance(locked, Mapping):
            st.markdown("**Locked baseline response**")
            st.json(dict(locked))
        if response is None and not isinstance(locked, Mapping):
            st.info("No session result is loaded.")
