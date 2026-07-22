"""Cross-dataset Hubble consistency diagnostics without false joint claims."""

from __future__ import annotations

import json
from typing import Any, Mapping

import altair as alt
import pandas as pd
import streamlit as st

from dti_ui_v1.services.hubble_consistency_engine import (
    anchor_by_id,
    anchor_diagnostic,
    comparison_rows,
    likelihood_component_rows,
    load_anchor_contract,
    tradeoff_classification,
)


HISTORY_KEY = "general_class_compute_history_v1"


def _history() -> list[Mapping[str, Any]]:
    value = st.session_state.get(HISTORY_KEY, [])
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, Mapping)]


def _submitted_h0(item: Mapping[str, Any]) -> float | None:
    request = item.get("submitted_payload", {})
    if not isinstance(request, Mapping):
        return None
    try:
        return float(request.get("H0"))
    except (TypeError, ValueError):
        return None


def _response(item: Mapping[str, Any]) -> Mapping[str, Any]:
    response = item.get("response", {})
    return response if isinstance(response, Mapping) else {}


def _anchor_frame(contract: Mapping[str, Any]) -> pd.DataFrame:
    rows = []
    for anchor in contract["anchors"]:
        h0 = float(anchor["H0"])
        sigma = float(anchor["sigma_total"])
        rows.append({
            "id": anchor["id"],
            "label": anchor["label"],
            "method": anchor["method"],
            "H0": h0,
            "sigma": sigma,
            "lower": h0 - sigma,
            "upper": h0 + sigma,
            "source": anchor["source_title"],
        })
    return pd.DataFrame(rows)


def _render_anchor_chart(contract: Mapping[str, Any], model_h0: float | None) -> None:
    frame = _anchor_frame(contract)
    domain = [float(frame["lower"].min()) - 1.0, float(frame["upper"].max()) + 1.0]
    base = alt.Chart(frame)
    rules = base.mark_rule(strokeWidth=3).encode(
        y=alt.Y("label:N", title=None, sort=None),
        x=alt.X("lower:Q", title="H₀ [km s⁻¹ Mpc⁻¹]", scale=alt.Scale(domain=domain, zero=False)),
        x2="upper:Q",
        tooltip=["label:N", alt.Tooltip("H0:Q", format=".2f"), alt.Tooltip("sigma:Q", format=".2f")],
    )
    points = base.mark_point(filled=True, size=100).encode(
        y=alt.Y("label:N", sort=None),
        x=alt.X("H0:Q", scale=alt.Scale(domain=domain, zero=False)),
        color=alt.Color("label:N", legend=None),
        tooltip=["method:N", "source:N"],
    )
    chart = rules + points
    if model_h0 is not None:
        model = pd.DataFrame({"model_H0": [model_h0]})
        model_rule = alt.Chart(model).mark_rule(color="#ff4b4b", strokeWidth=3).encode(
            x=alt.X("model_H0:Q", scale=alt.Scale(domain=domain, zero=False)),
            tooltip=[alt.Tooltip("model_H0:Q", title="Submitted model H₀", format=".3f")],
        )
        chart = chart + model_rule
    st.altair_chart(chart.properties(height=310, title="Published local-ladder summary coordinates"), use_container_width=True)


def render() -> None:
    st.title("Hubble Consistency Engine")
    st.caption("Early-Universe, BAO, relative-supernova, and local-ladder consistency without hidden double counting")

    try:
        contract = load_anchor_contract()
    except Exception as exc:
        st.error(f"The local-ladder comparison contract is unavailable: {exc}")
        return

    anchors = contract["anchors"]
    labels = {str(anchor["label"]): str(anchor["id"]) for anchor in anchors}
    selected_label = st.selectbox(
        "Local distance-ladder comparison",
        options=list(labels),
        help="Exactly one published summary is displayed at a time. CCHP rows are correlated alternatives.",
    )
    anchor = anchor_by_id(contract, labels[selected_label])

    st.warning(
        "Independence gate: the selected local H₀ summary shares supernova information with Pantheon+/SH0ES. "
        "Its Gaussian pull is therefore shown as a comparison rail and is not added to the backend joint likelihood."
    )

    history = _history()
    current_h0 = _submitted_h0(history[-1]) if history else None
    _render_anchor_chart(contract, current_h0)

    st.markdown("### Published ladder contract")
    ladder_table = _anchor_frame(contract)[["label", "method", "H0", "sigma", "source"]]
    st.dataframe(ladder_table, hide_index=True, use_container_width=True)

    if not history or current_h0 is None:
        st.info("Compute → ExecutionでCLASS / AxiCLASSを実行すると、赤い縦線と整合性診断が表示されます。")
    else:
        current = history[-1]
        response = _response(current)
        diagnostic = anchor_diagnostic(current_h0, anchor)
        derived = response.get("derived", {})
        if not isinstance(derived, Mapping):
            derived = {}

        st.markdown("### Current submitted universe")
        columns = st.columns(5)
        columns[0].metric("Submitted H₀", f"{current_h0:.3f}")
        columns[1].metric("Selected ladder H₀", f"{float(anchor['H0']):.2f} ± {float(anchor['sigma_total']):.2f}")
        columns[2].metric("Ladder pull", f"{float(diagnostic['pull_sigma']):+.2f}σ")
        columns[3].metric("r_drag [Mpc]", f"{float(derived.get('rs_drag_Mpc_CLASS')):.3f}" if derived.get("rs_drag_Mpc_CLASS") is not None else "—")
        columns[4].metric("f_EDE achieved", f"{float(derived.get('f_EDE_AxiCLASS')):.4f}" if derived.get("f_EDE_AxiCLASS") is not None else "—")

        component_frame = pd.DataFrame(likelihood_component_rows(response))
        st.markdown("### Same-model observational rails")
        st.dataframe(component_frame, hide_index=True, use_container_width=True)
        unavailable = component_frame[component_frame["status"] != "ok"]
        if len(unavailable):
            st.warning("One or more official likelihood components are unavailable; no cross-dataset consistency claim is made.")

        if len(history) >= 2:
            previous = history[-2]
            previous_h0 = _submitted_h0(previous)
            if previous_h0 is not None:
                deltas = comparison_rows(
                    _response(previous), response, previous_h0, current_h0, anchor
                )
                assessment = tradeoff_classification(deltas)
                st.markdown("### Previous-run directional audit")
                if assessment == "PARETO_IMPROVEMENT":
                    st.success("PARETO_IMPROVEMENT: no displayed rail worsened relative to the preceding run.")
                elif assessment == "PARETO_DETERIORATION":
                    st.error("PARETO_DETERIORATION: no displayed rail improved relative to the preceding run.")
                elif assessment == "CROSS_DATASET_TRADE_OFF":
                    st.warning("CROSS_DATASET_TRADE_OFF: at least one observational rail improved while another worsened.")
                else:
                    st.info("NO_MATERIAL_CHANGE: displayed χ² coordinates did not materially change.")
                delta_frame = pd.DataFrame(deltas)
                delta_chart = alt.Chart(delta_frame).mark_bar().encode(
                    x=alt.X("rail:N", title=None),
                    y=alt.Y("delta_chi2:Q", title="Δχ² current − previous"),
                    color=alt.condition("datum.delta_chi2 <= 0", alt.value("#20B2AA"), alt.value("#E76F51")),
                    tooltip=["rail:N", alt.Tooltip("delta_chi2:Q", format="+.5f"), "combination:N"],
                ).properties(height=330)
                st.altair_chart(delta_chart, use_container_width=True)
                st.dataframe(delta_frame, hide_index=True, use_container_width=True)

    st.markdown("### Reconciliation claim gate")
    st.dataframe(
        [
            {"Requirement": "Same-model AxiCLASS propagation", "Current state": "AVAILABLE after a General run", "Required for final claim": "Yes"},
            {"Requirement": "DESI DR2 + Planck 2018 + relative Pantheon+", "Current state": "Single-point official likelihoods", "Required for final claim": "Yes"},
            {"Requirement": "Raw Cepheid/TRGB/JAGB calibrator likelihood and covariance", "Current state": "NOT INSTALLED — published summaries only", "Required for final claim": "Yes"},
            {"Requirement": "Overlap-safe joint covariance", "Current state": "PROTECTED — local summaries are not summed", "Required for final claim": "Yes"},
            {"Requirement": "Declared priors + converged posterior sampler", "Current state": "NOT EXECUTED", "Required for final claim": "Yes"},
            {"Requirement": "Bayesian evidence / model comparison", "Current state": "NOT EXECUTED", "Required for final claim": "Yes"},
        ],
        hide_index=True,
        use_container_width=True,
    )
    st.info(
        "Current verdict: this page can expose agreement, tension, and cross-dataset trade-offs at submitted points. "
        "It cannot yet declare the Hubble tension reconciled because the raw local-calibrator likelihood and a converged joint posterior are absent."
    )
    st.caption(f"Anchor contract SHA-256: {contract['contract_sha256']}")
    st.download_button(
        "Download local-ladder comparison contract",
        data=json.dumps(contract, ensure_ascii=False, indent=2),
        file_name="hubble_ladder_anchors.json",
        mime="application/json",
        use_container_width=True,
    )
