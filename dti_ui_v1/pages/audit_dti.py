"""Read-only presentation of a conditional DESI DR2 Audit-DTI protocol."""

from __future__ import annotations

import json
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


RESULT_PATH = Path(__file__).resolve().parents[2] / "data" / "research" / "audit_dti_dr2_latest.json"
PROFILE_PATH = Path(__file__).resolve().parents[2] / "data" / "research" / "audit_dti_dr2_profile.csv"
INJECTION_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "research"
    / "dti_transition_injection_recovery.json"
)
INJECTION_SUMMARY_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "research"
    / "dti_transition_injection_recovery_summary.csv"
)
CATALOG_PILOT_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "research"
    / "dti_catalog_pipeline_pilot.json"
)
CATALOG_PILOT_SUMMARY_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "research"
    / "dti_catalog_pipeline_pilot_summary.json"
)
CATALOG_PILOT_CSV_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "research"
    / "dti_catalog_pipeline_pilot_summary.csv"
)
NEUTRAL_AUDIT_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "research"
    / "assumption_neutral_dti_audit.json"
)


def _load_result() -> dict:
    return json.loads(RESULT_PATH.read_text(encoding="utf-8"))


def render() -> None:
    st.title("DESI DR2 Audit-DTI")
    st.caption("Conditional response audit of the compressed DESI DR2 BAO likelihood")
    if not RESULT_PATH.exists():
        st.error("The verified Audit-DTI artifact has not been installed.")
        return

    result = _load_result()
    best = result["best_finite_grid_point"]
    bootstrap = result["covariance_bootstrap"]
    selected = result["transition_model_selection"]["best"]
    st.success("Protocol complete · 392/392 solver points · 2,000/2,000 covariance replicates")

    columns = st.columns(5)
    columns[0].metric("Best finite-grid H0", f"{best['H0']:.2f}")
    columns[1].metric("Best finite-grid f_EDE", f"{best['f_EDE']:.3f}")
    columns[2].metric("DESI DR2 χ²", f"{best['chi2']:.4f}")
    columns[3].metric("Conditional winner", "Smooth cubic")
    columns[4].metric("Bootstrap transition rate", f"{100 * bootstrap['transition_selection_fraction']:.1f}%")

    st.warning(
        "Interpretation gate: this is not a raw-galaxy or raw-correlation-function transition test. "
        "The input is a template-derived Gaussian compression at seven effective redshifts, and the "
        "theory scan uses a smooth AxiCLASS parameter map. Upstream reconstruction, fiducial-cosmology "
        "conversion, template fitting, nuisance marginalization, or redshift-bin averaging could attenuate "
        "a transition that is not represented by that measurement model."
    )
    st.info(
        "Conditional result: within the published 13-element DESI DR2 BAO mean/covariance and this "
        "finite AxiCLASS grid, a discontinuous H0-profile is not required. A smooth cubic response is "
        "preferred, and none of the 2,000 seeded covariance replicates selected a multi-segment response. "
        "This establishes internal stability of the compressed likelihood only; it does not establish "
        "continuity of the underlying Universe."
    )
    st.warning(
        "Scope: H0 and f_EDE are scanned on a finite grid; omega_b, omega_cdm, n_s, A_s, tau_reio "
        "and z_c are fixed. This page is not a posterior, Bayes factor, Planck likelihood, or unique "
        "mechanism attribution."
    )

    st.subheader("Assumption-neutral numerical audit")
    if NEUTRAL_AUDIT_PATH.exists():
        neutral = json.loads(NEUTRAL_AUDIT_PATH.read_text(encoding="utf-8"))
        observed = neutral["observed_compressed_product"]
        recovery = neutral["injection_recovery"]
        neutral_columns = st.columns(4)
        neutral_columns[0].metric("Coordinate encodings", observed["representations_tested"])
        neutral_columns[1].metric("Segmented winners", observed["multi_segment_winner_count"])
        neutral_columns[2].metric("Injected realizations", f"{recovery['injected_replicates']:,}")
        neutral_columns[3].metric("Continuity proven", "NO")
        st.info(
            "No physical narrative is supplied to this decision rule. The same finite numerical response "
            "is compared after linear, logarithmic, reciprocal, and ordinal coordinate encodings."
        )
        st.dataframe(pd.DataFrame(observed["results"]), hide_index=True)
        st.warning(neutral["claim_boundary"])
    else:
        st.warning("The assumption-neutral audit artifact has not been installed.")

    with st.expander("Input-assumption audit", expanded=True):
        assumption_columns = st.columns(4)
        assumption_columns[0].metric("Published distance values", "13")
        assumption_columns[1].metric("Effective redshifts", "7")
        assumption_columns[2].metric("Cross-redshift covariance", "0 / 144 nonzero")
        assumption_columns[3].metric("Resampling source", "Same Gaussian product")
        st.markdown(
            "- The published BAO distances are derived from reconstructed two-point clustering with a "
            "fiducial-cosmology template and freely shifted BAO scale parameters.\n"
            "- Broadband nuisance freedom is marginalized before the distance summary is published.\n"
            "- The official robustness suite covers several smooth alternative cosmologies, but does not "
            "demonstrate injection and recovery of a DTI-like sharp transition.\n"
            "- Therefore the bootstrap cannot diagnose smoothing introduced before the 13-value product "
            "was created; every replicate inherits the same compression assumptions."
        )

    st.subheader("Transition injection/recovery audit")
    if INJECTION_PATH.exists():
        injection = json.loads(INJECTION_PATH.read_text(encoding="utf-8"))
        calibration = injection["calibration"]
        robust = pd.DataFrame(injection["robust_detection_by_amplitude"])
        scenarios = pd.DataFrame(injection["scenarios"])

        injection_columns = st.columns(4)
        injection_columns[0].metric("Null simulations", f"{calibration['null_replicates']:,}")
        injection_columns[1].metric(
            "Injected simulations",
            f"{len(scenarios) * int(calibration['scenario_replicates']):,}",
        )
        injection_columns[2].metric("Transition conditions", f"{len(scenarios)}")
        injection_columns[3].metric(
            "Global 3σ threshold",
            f"Δχ² {calibration['thresholds_delta_chi2']['global_3sigma_99.73_percent']:.2f}",
        )
        st.warning(
            "Recovery result: percent-level sharp transitions can be strongly underpowered after broad "
            "redshift-window mixing and 13-value BAO compression. Non-detection in the compressed product "
            "therefore cannot by itself exclude a transition in the underlying clustering data."
        )

        robust["step_percent"] = 100.0 * robust["fractional_H_step"]
        robust["minimum_percent"] = 100.0 * robust["minimum_detection_fraction"]
        robust["median_percent"] = 100.0 * robust["median_detection_fraction"]
        robust["maximum_percent"] = 100.0 * robust["maximum_detection_fraction"]
        robust_records = robust.to_dict(orient="records")
        recovery_chart = alt.Chart(alt.Data(values=robust_records)).mark_line(point=True).encode(
            x=alt.X("step_percent:Q", title="Injected permanent H(z) step [%]"),
            y=alt.Y(
                "median_percent:Q",
                title="Global 3σ recovery fraction [%]",
                scale=alt.Scale(domain=[0, 100]),
            ),
            tooltip=[
                alt.Tooltip("step_percent:Q", title="H(z) step [%]", format=".1f"),
                alt.Tooltip("minimum_percent:Q", title="Minimum recovery [%]", format=".1f"),
                alt.Tooltip("median_percent:Q", title="Median recovery [%]", format=".1f"),
                alt.Tooltip("maximum_percent:Q", title="Maximum recovery [%]", format=".1f"),
            ],
        ).properties(height=330, title="Recovery after DESI-like window mixing and 13-value compression")
        st.altair_chart(recovery_chart)
        st.dataframe(
            robust[["step_percent", "minimum_percent", "median_percent", "maximum_percent"]].rename(
                columns={
                    "step_percent": "H(z) step [%]",
                    "minimum_percent": "Minimum recovery [%]",
                    "median_percent": "Median recovery [%]",
                    "maximum_percent": "Maximum recovery [%]",
                }
            ),
            hide_index=True,
        )
        st.caption(
            "Independent transfer surrogate, not the DESI production pipeline: fine-z H(z) injection → "
            "D_H/D_M propagation → fiducial BAO dilation → tracer-window mixing → narrow/broad BAO-peak "
            "template fits with broadband marginalization → published 13-observable layout and covariance. "
            "It does not include the real survey mask, fiber assignment, pyrecon displacement field, "
            "RascalC covariance, official desilike fit, or Lyα production pipeline."
        )
    else:
        st.warning("The transition injection/recovery artifact has not been installed.")

    st.subheader("Catalog-level upstream pilot")
    if CATALOG_PILOT_SUMMARY_PATH.exists():
        catalog_summary = json.loads(
            CATALOG_PILOT_SUMMARY_PATH.read_text(encoding="utf-8")
        )
        catalog_conditions = pd.DataFrame(catalog_summary["conditions"])
        totals = catalog_summary["execution_totals"]
        catalog_columns = st.columns(4)
        catalog_columns[0].metric("Catalog conditions", catalog_summary["condition_count"])
        catalog_columns[1].metric(
            "Correlation functions", f"{totals['correlation_functions']:,}"
        )
        catalog_columns[2].metric("BAO template fits", f"{totals['bao_template_fits']:,}")
        catalog_columns[3].metric("Production equivalent", "NO")
        st.success(
            "Executed: object catalog → transition injection → coordinate conversion → FFT "
            "reconstruction → Landy-Szalay ξ(s,μ) → anisotropic BAO fit → 13-value compression."
        )
        st.warning(
            "Result: the full stage contract executes, but recovery is incomplete and tracer-dependent. "
            "The QSO radial coordinate remains weakly recovered even for the strongest injected step. "
            "This is a synthetic survey-shaped catalog pilot, not an official DESI EZmock/Abacus or "
            "production-pipeline result."
        )
        catalog_conditions["step_percent"] = (
            100.0 * catalog_conditions["fractional_H_step"]
        )
        catalog_conditions["alpha_rmse_percent"] = (
            100.0 * catalog_conditions["alpha_rmse"]
        )
        catalog_chart = (
            alt.Chart(alt.Data(values=catalog_conditions.to_dict(orient="records")))
            .mark_line(point=True)
            .encode(
                x=alt.X("step_percent:Q", title="Injected permanent H(z) step [%]"),
                y=alt.Y("alpha_rmse_percent:Q", title="Recovered α RMSE [%]"),
                tooltip=[
                    alt.Tooltip("step_percent:Q", title="H(z) step [%]", format=".1f"),
                    alt.Tooltip("alpha_rmse_percent:Q", title="α RMSE [%]", format=".2f"),
                    alt.Tooltip(
                        "QSO_alpha_parallel_error:Q",
                        title="QSO radial α error",
                        format=".4f",
                    ),
                ],
            )
            .properties(height=310, title="Catalog-pipeline recovery error")
        )
        st.altair_chart(catalog_chart)
        st.dataframe(
            catalog_conditions[
                [
                    "step_percent",
                    "alpha_rmse_percent",
                    "QSO_target_alpha_parallel",
                    "QSO_recovered_alpha_parallel",
                    "LYA_target_alpha_parallel",
                    "LYA_recovered_alpha_parallel",
                ]
            ].rename(
                columns={
                    "step_percent": "H(z) step [%]",
                    "alpha_rmse_percent": "α RMSE [%]",
                    "QSO_target_alpha_parallel": "QSO radial target",
                    "QSO_recovered_alpha_parallel": "QSO radial recovered",
                    "LYA_target_alpha_parallel": "Lyα radial target",
                    "LYA_recovered_alpha_parallel": "Lyα radial recovered",
                }
            ),
            hide_index=True,
        )
        st.caption(catalog_summary["claim_boundary"])
    else:
        st.warning("The catalog-level upstream pilot has not been installed.")

    profile = pd.DataFrame(result["profile_rows"])
    plot_columns = ["H0", "delta_chi2", "profile_chi2", "profile_f_EDE"]
    profile_plot = profile[plot_columns].apply(pd.to_numeric, errors="coerce").dropna()
    if len(profile_plot) != len(result["profile_rows"]):
        st.error("The installed profile artifact contains non-numeric plotting rows.")
        return
    profile_records = profile_plot.to_dict(orient="records")
    profile_chart = alt.Chart(alt.Data(values=profile_records)).mark_line(point=True).encode(
        x=alt.X("H0:Q", title="H0 [km s⁻¹ Mpc⁻¹]", scale=alt.Scale(zero=False)),
        y=alt.Y("delta_chi2:Q", title="Profile Δχ²", scale=alt.Scale(zero=True)),
        tooltip=[
            alt.Tooltip("H0:Q", format=".2f"), alt.Tooltip("profile_f_EDE:Q", format=".3f"),
            alt.Tooltip("profile_chi2:Q", title="χ²", format=".5f"),
        ],
    ).properties(height=390, title="DESI DR2 finite-grid profile")
    st.altair_chart(profile_chart)

    c1, c2 = st.columns(2)
    with c1:
        f_chart = alt.Chart(alt.Data(values=profile_records)).mark_line(interpolate="step-after", point=True).encode(
            x=alt.X("H0:Q", title="H0 [km s⁻¹ Mpc⁻¹]", scale=alt.Scale(zero=False)),
            y=alt.Y("profile_f_EDE:Q", title="Selected finite-grid f_EDE"),
            tooltip=["H0:Q", "profile_f_EDE:Q"],
        ).properties(height=300, title="Profile branch selected at each H0")
        st.altair_chart(f_chart)
        st.caption("Steps reflect the discrete f_EDE grid and are not interpreted as physical discontinuities.")
    with c2:
        quantiles = bootstrap["best_H0_quantiles"]
        st.markdown("#### Covariance-resampled best-grid coordinates")
        st.metric("Median H0", f"{quantiles['0.5']:.2f}")
        st.write(f"68% finite-grid interval: {quantiles['0.16']:.2f} to {quantiles['0.84']:.2f}")
        st.write(f"95% finite-grid interval: {quantiles['0.025']:.2f} to {quantiles['0.975']:.2f}")
        f_quantiles = bootstrap["best_f_EDE_quantiles"]
        st.write(f"Median f_EDE grid coordinate: {f_quantiles['0.5']:.3f}")

    st.subheader("Model-selection audit")
    candidates = pd.DataFrame(result["transition_model_selection"]["candidates"])
    candidates["model"] = candidates.apply(
        lambda row: (
            f"Smooth polynomial degree {int(row['order'])}"
            if row["family"] == "smooth_polynomial"
            else f"Piecewise constant K={int(row['segments'])}"
        ), axis=1,
    )
    candidates["ΔBIC"] = candidates["bic"] - candidates["bic"].min()
    st.dataframe(candidates[["model", "parameter_count", "rss", "bic", "ΔBIC"]], hide_index=True)
    st.caption(
        f"Winner: smooth polynomial degree {selected['order']}; BIC margin to runner-up "
        f"{selected['delta_bic_to_runner_up']:.3f}. Parameter counting includes segment boundaries. "
        "This compares response shapes in H0 parameter space, not transitions directly in redshift or cosmic time."
    )

    with st.expander("Reproducibility and source identity"):
        st.json({
            "grid": result["grid"], "fixed_parameters": result["fixed_parameters"],
            "bootstrap": {"replicates": bootstrap["replicates"], "seed": bootstrap["seed"]},
            "failure_accounting": result["failure_accounting"],
            "source_identity": result["source_identity"], "artifact_sha256": result["artifact_sha256"],
        })

    st.subheader("Download research artifacts")
    d1, d2 = st.columns(2)
    d1.download_button(
        "Download complete Audit-DTI JSON", RESULT_PATH.read_bytes(),
        file_name="audit_dti_dr2_latest.json", mime="application/json",
    )
    if PROFILE_PATH.exists():
        d2.download_button(
            "Download profile CSV", PROFILE_PATH.read_bytes(),
            file_name="audit_dti_dr2_profile.csv", mime="text/csv",
        )
    if INJECTION_PATH.exists():
        d3, d4 = st.columns(2)
        d3.download_button(
            "Download injection/recovery JSON", INJECTION_PATH.read_bytes(),
            file_name="dti_transition_injection_recovery.json", mime="application/json",
        )
        if INJECTION_SUMMARY_PATH.exists():
            d4.download_button(
                "Download injection/recovery CSV", INJECTION_SUMMARY_PATH.read_bytes(),
                file_name="dti_transition_injection_recovery_summary.csv", mime="text/csv",
            )
    if CATALOG_PILOT_SUMMARY_PATH.exists():
        d5, d6 = st.columns(2)
        d5.download_button(
            "Download catalog-pilot summary JSON",
            CATALOG_PILOT_SUMMARY_PATH.read_bytes(),
            file_name="dti_catalog_pipeline_pilot_summary.json",
            mime="application/json",
        )
        if CATALOG_PILOT_CSV_PATH.exists():
            d6.download_button(
                "Download catalog-pilot summary CSV",
                CATALOG_PILOT_CSV_PATH.read_bytes(),
                file_name="dti_catalog_pipeline_pilot_summary.csv",
                mime="text/csv",
            )
