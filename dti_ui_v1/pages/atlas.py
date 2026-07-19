"""Narrative, data-driven Hubble Tension Atlas."""

from __future__ import annotations

from typing import Any, Mapping

import altair as alt
import pandas as pd
import streamlit as st


HISTORY_KEY = "general_class_compute_history_v1"


def _history() -> list[Mapping[str, Any]]:
    value = st.session_state.get(HISTORY_KEY, [])
    return [item for item in value if isinstance(item, Mapping)] if isinstance(value, list) else []


def _response(item: Mapping[str, Any]) -> Mapping[str, Any]:
    value = item.get("response", {})
    return value if isinstance(value, Mapping) else {}


def _value(response: Mapping[str, Any], key: str) -> Any:
    derived = response.get("derived", {})
    return derived.get(key) if isinstance(derived, Mapping) else None


def render() -> None:
    language = st.segmented_control("Language / 言語", ("日本語", "English"), default="日本語")
    japanese = language != "English"
    st.title("Hubble Tension Atlas")
    st.caption(
        "初期宇宙の変更が音響地平線・距離・観測適合度へ伝わる道筋" if japanese
        else "How early-universe physics propagates into sound horizons, distances, and observed fit"
    )
    history = _history()
    if not history:
        st.info("Compute → ExecutionでCLASS / AxiCLASSを実行してください。" if japanese else "Run CLASS / AxiCLASS from Compute → Execution.")
        return

    current_item = history[-1]
    current = _response(current_item)
    request = current_item.get("submitted_payload", {})
    derived = current.get("derived", {})
    joint = current.get("joint_likelihood", {})

    st.markdown("## 1. 仮説から観測まで" if japanese else "## 1. From hypothesis to observation")
    chain = pd.DataFrame(
        [
            {"stage": "H₀", "value": request.get("H0"), "unit": "km s⁻¹ Mpc⁻¹"},
            {"stage": "f_EDE", "value": derived.get("f_EDE_AxiCLASS"), "unit": "fraction"},
            {"stage": "z_c", "value": derived.get("z_c_AxiCLASS"), "unit": "redshift"},
            {"stage": "r_drag", "value": derived.get("rs_drag_Mpc_CLASS"), "unit": "Mpc"},
            {"stage": "S8", "value": derived.get("S8_CLASS"), "unit": "dimensionless"},
        ]
    ).dropna()
    st.dataframe(chain, hide_index=True, use_container_width=True)
    st.caption(
        "矢印は因果推論ではなく、同一ソルバー実行内の計算順序を示します。"
        if japanese else "The sequence is computational propagation within one solver run, not a causal-inference claim."
    )

    st.markdown("## 2. データは何を言うか" if japanese else "## 2. What the data say")
    components = joint.get("components", []) if isinstance(joint, Mapping) else []
    if isinstance(components, list) and components:
        frame = pd.DataFrame(components)
        chart = alt.Chart(frame).mark_bar(size=54).encode(
            x=alt.X("dataset:N", title=None),
            y=alt.Y("chi2:Q", title="χ² contribution"),
            color=alt.Color("dataset:N", legend=None, scale=alt.Scale(scheme="tableau10")),
            tooltip=["dataset:N", alt.Tooltip("loglike:Q", format=".5f"), alt.Tooltip("chi2:Q", format=".5f")],
        ).properties(height=340)
        st.altair_chart(chart, use_container_width=True)
        st.warning(
            "異なる尤度の絶対χ²は規格化やデータ点数が異なるため、棒の高さだけで優劣を判断できません。比較には同じ成分でのΔχ²を使います。"
            if japanese else "Absolute chi-square values have different normalizations and data counts; compare models with within-component delta chi-square."
        )

    bao = current.get("desi_dr2_bao", {})
    rows = bao.get("theory_vector", []) if isinstance(bao, Mapping) else []
    if isinstance(rows, list) and rows:
        residuals = pd.DataFrame(rows)
        residual_chart = alt.Chart(residuals).mark_circle(size=95).encode(
            x=alt.X("redshift:Q", title="Redshift z"),
            y=alt.Y("residual:Q", title="Prediction − observation"),
            color=alt.Color("observable:N", title="Observable"),
            tooltip=["observable:N", "redshift:Q", alt.Tooltip("observed:Q", format=".5f"), alt.Tooltip("predicted:Q", format=".5f"), alt.Tooltip("residual:Q", format=".5f")],
        ).properties(height=330)
        zero = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(strokeDash=[5, 4]).encode(y="y:Q")
        st.markdown("### DESI DR2 residual map")
        st.altair_chart(residual_chart + zero, use_container_width=True)

    st.markdown("## 3. 直前の宇宙との比較" if japanese else "## 3. Compare with the preceding universe")
    if len(history) < 2:
        st.info("別のH₀またはf_EDEで再計算するとΔχ²比較が現れます。" if japanese else "Run a second parameter point to reveal delta-likelihood comparisons.")
    else:
        previous = _response(history[-2])
        rows = []
        for label, key in (("DESI DR2 BAO", "desi_dr2_bao"), ("Planck 2018", "planck_2018"), ("Pantheon+", "pantheon_plus")):
            old = previous.get(key, {})
            new = current.get(key, {})
            old_chi = old.get("chi2", old.get("chi2_effective")) if isinstance(old, Mapping) else None
            new_chi = new.get("chi2", new.get("chi2_effective")) if isinstance(new, Mapping) else None
            try:
                rows.append({"dataset": label, "previous_chi2": float(old_chi), "current_chi2": float(new_chi), "delta_chi2": float(new_chi) - float(old_chi)})
            except (TypeError, ValueError):
                continue
        if rows:
            delta = pd.DataFrame(rows)
            chart = alt.Chart(delta).mark_bar().encode(
                x=alt.X("dataset:N", title=None),
                y=alt.Y("delta_chi2:Q", title="Δχ² (current − previous)"),
                color=alt.condition("datum.delta_chi2 < 0", alt.value("#20B2AA"), alt.value("#E76F51")),
                tooltip=["dataset:N", alt.Tooltip("delta_chi2:Q", format="+.5f")],
            ).properties(height=320)
            st.altair_chart(chart, use_container_width=True)
            st.dataframe(delta, hide_index=True, use_container_width=True)

    st.markdown("## 4. 科学的境界" if japanese else "## 4. Scientific boundary")
    st.success(
        "実計算済み: AxiCLASS物理伝播、Planck 2018、Pantheon+、DESI DR2の単一点尤度。"
        if japanese else "Computed: AxiCLASS propagation and single-point Planck 2018, Pantheon+, and DESI DR2 likelihoods."
    )
    st.info(
        "未主張: 事後分布、ベイズ因子、発見有意度。これらは明示的な事前分布と収束済みサンプラーを要します。"
        if japanese else "Not claimed: posterior distributions, Bayes factors, or discovery significance; those require explicit priors and a converged sampler."
    )
