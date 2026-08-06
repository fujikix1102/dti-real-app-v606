"""Narrative, data-driven Hubble Tension Atlas."""

from __future__ import annotations

from pathlib import Path
import csv
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

    current_item = history[-1] if history else {}
    current = _response(current_item)
    request = current_item.get("submitted_payload", {}) if isinstance(current_item, Mapping) else {}
    derived = current.get("derived", {})
    joint = current.get("joint_likelihood", {})

    if history:
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


    st.markdown("## GTDS-MCMC Frozen Diagnostic Reference")

    st.info(
        "凍結済みGTDS-MCMC診断アーティファクトの参照表示です。"
        "サンプラー実行、尤度再計算、事後分布更新は行いません。"
        if japanese else
        "Frozen GTDS-MCMC diagnostic artifact reference only. "
        "No sampler execution, likelihood recomputation, or posterior update."
    )

    gtds_col1, gtds_col2, gtds_col3, gtds_col4 = st.columns(4)

    gtds_col1.metric("Chains", "10")
    gtds_col2.metric("Steps / Chain", "10000")
    gtds_col3.metric("Max Rhat", "1.03516090252")
    gtds_col4.metric("Worst parameter", "tau")

    st.caption(
        "Diagnostic-only display. Frozen artifact reference; not a posterior result."
        if not japanese else
        "Diagnostic-only display. Frozen artifact reference; not a posterior result."
    )


    st.subheader("GTDS-MCMC Diagnostic Status")

    st.caption(
        "Source: frozen GTDS MCMC final state ledger"
    )

    status_col1, status_col2, status_col3 = st.columns(3)

    status_col1.metric(
        "Chains",
        "10"
    )

    status_col2.metric(
        "Max Rhat",
        "1.03516090252"
    )

    status_col3.metric(
        "Worst parameter",
        "tau"
    )

    st.info(
        "Diagnostic-only display. "
        "No MCMC rerun, likelihood recomputation, "
        "or posterior recomputation."
    )


    
    st.markdown("### GTDS MCMC 10-Chain Diagnostic Archive")

    st.caption(
        "Frozen diagnostic artifact display only. "
        "No sampler execution, likelihood recomputation, "
        "or posterior recomputation."
    )

    archive_root = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "gtds_mcmc_diagnostic_archive_v1"
    )

    occupancy_file = (
        archive_root
        / "occupancy"
        / "MODE_OCCUPANCY_LAST20PERCENT.tsv"
    )

    transition_file = (
        archive_root
        / "transition"
        / "MODE_TRANSITION_ANALYSIS.tsv"
    )

    stability_file = (
        archive_root
        / "stability"
        / "CLUSTER_STABILITY_PHASE_DISTANCE.tsv"
    )

    with st.expander("10 Chain Mode Occupancy", expanded=False):
        if occupancy_file.exists():
            st.dataframe(
                pd.read_csv(occupancy_file, sep="\t"),
                hide_index=True,
                use_container_width=True,
            )


    with st.expander("GTDS H0 Mean Summary", expanded=True):

        if occupancy_file.exists():
            occupancy = pd.read_csv(
                occupancy_file,
                sep="\t"
            )

            h0 = occupancy[
                occupancy["parameter"] == "H0"
            ].copy()

            h0["mean_last20pct"] = pd.to_numeric(
                h0["mean_last20pct"],
                errors="coerce"
            )
            h0["min"] = pd.to_numeric(
                h0["min"],
                errors="coerce"
            )
            h0["max"] = pd.to_numeric(
                h0["max"],
                errors="coerce"
            )
            h0["std_last20pct"] = pd.to_numeric(
                h0["std_last20pct"],
                errors="coerce"
            )

            h0 = h0.dropna(
                subset=[
                    "chain",
                    "mean_last20pct",
                    "min",
                    "max",
                ]
            )

            center = float(h0["mean_last20pct"].median())
            spread = float(h0["mean_last20pct"].max() - h0["mean_last20pct"].min())

            st.markdown("#### Terminal H0 Mean by Chain")

            st.caption(
                "This diagnostic view uses H0-only rows from the frozen GTDS last-20% ledger. "
                "Points show mean_last20pct; the vertical line shows the median across chains. "
                "This is not a posterior distribution or sampler rerun."
            )

            m1, m2, m3 = st.columns(3)
            m1.metric("Minimum chain mean", f"{h0['mean_last20pct'].min():.3f}")
            m2.metric("Maximum chain mean", f"{h0['mean_last20pct'].max():.3f}")
            m3.metric("Chain spread", f"{spread:.3f}")


            st.caption(
                "The mean-point chart is not repeated here. "
                "Use the GTDS H0 Chain Range View below for the visual comparison: "
                "yellow point = mean_last20pct; blue line = min–max."
            )

            st.dataframe(
                h0[
                    [
                        "chain",
                        "tail_draws",
                        "mean_last20pct",
                        "std_last20pct",
                        "min",
                        "max",
                    ]
                ].sort_values("mean_last20pct"),
                hide_index=True,
                use_container_width=True,
            )


    with st.expander("GTDS H0 Chain Range View", expanded=True):

        if occupancy_file.exists():

            occupancy = pd.read_csv(
                occupancy_file,
                sep="\t"
            )

            h0 = occupancy[
                occupancy["parameter"] == "H0"
            ].copy()

            h0["mean_last20pct"] = pd.to_numeric(
                h0["mean_last20pct"],
                errors="coerce"
            )
            h0["min"] = pd.to_numeric(
                h0["min"],
                errors="coerce"
            )
            h0["max"] = pd.to_numeric(
                h0["max"],
                errors="coerce"
            )

            h0 = h0.dropna(
                subset=[
                    "chain",
                    "mean_last20pct",
                    "min",
                    "max",
                ]
            )

            st.markdown(
                "#### GTDS 10 Independent Chains: Terminal H0 Range"
            )

            st.caption(
                "Render marker: GTDS_H0_MIN_MAX_RANGE_VIEW_V2. "
                "This panel uses H0-only rows from MODE_OCCUPANCY_LAST20PERCENT.tsv."
            )

            st.caption(
                "Frozen diagnostic display only. "
                "Horizontal line shows min–max within the last 20% frozen draws; "
                "point shows mean_last20pct. "
                "No sampler execution, likelihood recomputation, or posterior update."
            )

            base = alt.Chart(h0).encode(
                y=alt.Y(
                    "chain:N",
                    title="Independent chain",
                    sort=[
                        "CHAIN10",
                        "CHAIN09",
                        "CHAIN08",
                        "CHAIN07",
                        "CHAIN06",
                        "CHAIN05",
                        "CHAIN04",
                        "CHAIN03",
                        "CHAIN02",
                        "CHAIN01",
                    ],
                )
            )

            range_line = base.mark_rule(
                strokeWidth=4,
                color="#4EA5FF",
            ).encode(
                x=alt.X(
                    "min:Q",
                    title="Terminal H0 range / mean (last 20% frozen draws)",
                    scale=alt.Scale(domain=[66.5, 70.8]),
                ),
                x2="max:Q",
                tooltip=[
                    "chain:N",
                    alt.Tooltip("mean_last20pct:Q", format=".4f"),
                    alt.Tooltip("min:Q", format=".4f"),
                    alt.Tooltip("max:Q", format=".4f"),
                    alt.Tooltip("std_last20pct:Q", format=".4f"),
                    alt.Tooltip("tail_draws:Q"),
                ],
            )

            mean_point = base.mark_point(
                filled=True,
                size=150,
                color="#FFD166",
            ).encode(
                x="mean_last20pct:Q",
                tooltip=[
                    "chain:N",
                    alt.Tooltip("mean_last20pct:Q", format=".4f"),
                    alt.Tooltip("min:Q", format=".4f"),
                    alt.Tooltip("max:Q", format=".4f"),
                    alt.Tooltip("std_last20pct:Q", format=".4f"),
                    alt.Tooltip("tail_draws:Q"),
                ],
            )

            st.altair_chart(
                (range_line + mean_point).properties(
                    height=360
                ),
                use_container_width=True,
            )



    with st.expander("Frozen GTDS Artifact Identity", expanded=False):

        manifest_file = (
            archive_root
            / "manifest"
            / "ARTIFACT_IDENTITY.tsv"
        )

        sha_file = (
            archive_root
            / "manifest"
            / "SHA256SUMS.tsv"
        )

        st.caption(
            "Reference-only artifact identity. "
            "This panel records source/provenance metadata for the frozen GTDS diagnostic archive. "
            "No sampler execution, likelihood recomputation, posterior update, or physical inference update is performed."
        )

        if manifest_file.exists():
            st.markdown("#### Artifact identity")
            st.dataframe(
                pd.read_csv(manifest_file, sep="\t"),
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info(
                "Artifact identity manifest is not available in the deployed archive path."
            )

        if sha_file.exists():
            st.markdown("#### Archive file checksums")
            st.dataframe(
                pd.read_csv(sha_file, sep="\t", header=None),
                hide_index=True,
                use_container_width=True,
            )

        st.info(
            "Interpretation boundary: frozen diagnostic reference only. "
            "Not a posterior result, not a convergence proof, not a likelihood evaluation, "
            "and not evidence for physical attractors by itself."
        )


    with st.expander("All-Parameter Last-20% Frozen Summary", expanded=False):

        if occupancy_file.exists():

            all_params = pd.read_csv(
                occupancy_file,
                sep="\t"
            )

            numeric_cols = [
                "tail_draws",
                "mean_last20pct",
                "std_last20pct",
                "min",
                "max",
            ]

            for col in numeric_cols:
                if col in all_params.columns:
                    all_params[col] = pd.to_numeric(
                        all_params[col],
                        errors="coerce"
                    )

            st.caption(
                "Frozen last-20% diagnostic summary for all recorded parameters. "
                "This is a chain-level diagnostic table, not posterior statistics."
            )

            st.dataframe(
                all_params,
                hide_index=True,
                use_container_width=True,
            )

            if "parameter" in all_params.columns:
                param_count = all_params["parameter"].nunique()
                chain_count = all_params["chain"].nunique() if "chain" in all_params.columns else None

                c1, c2 = st.columns(2)
                c1.metric("Recorded parameters", str(param_count))
                c2.metric("Recorded chains", str(chain_count) if chain_count is not None else "N/A")

        else:
            st.info(
                "All-parameter last-20% summary file is not available in the deployed archive path."
            )


    with st.expander("Mode Transition Analysis", expanded=False):
        if transition_file.exists():
            st.dataframe(
                pd.read_csv(transition_file, sep="\t"),
                hide_index=True,
                use_container_width=True,
            )

    with st.expander("Cluster Stability Phase Distance", expanded=False):
        if stability_file.exists():
            st.dataframe(
                pd.read_csv(stability_file, sep="\t"),
                hide_index=True,
                use_container_width=True,
            )



    st.markdown("## 4. 科学的境界" if japanese else "## 4. Scientific boundary")
    st.success(
        "実計算済み: AxiCLASS物理伝播、Planck 2018、Pantheon+、DESI DR2の単一点尤度。"
        if japanese else "Computed: AxiCLASS propagation and single-point Planck 2018, Pantheon+, and DESI DR2 likelihoods."
    )
    st.info(
        "未主張: 事後分布、ベイズ因子、発見有意度。これらは明示的な事前分布と収束済みサンプラーを要します。"
        if japanese else "Not claimed: posterior distributions, Bayes factors, or discovery significance; those require explicit priors and a converged sampler."
    )
