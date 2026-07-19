from __future__ import annotations

import json
from typing import Any, Mapping

import altair as alt
import pandas as pd
import streamlit as st


T_CMB_K = 2.7255
K2_TO_UK2 = 1.0e12
HISTORY_KEY = "general_class_compute_history_v1"

from dti_ui_v1.services.general_class_compute_service import (
    GeneralClassRequest,
    execute_general_class_compute,
)
from dti_ui_v1.services.run_store import save_run_artifact


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

    derived = payload.get("derived")

    if isinstance(derived, Mapping):
        for key in keys:
            if key in derived:
                return derived[key]

    return None


def _spectrum_frame(
    derived: Mapping[str, Any],
    *series_keys: str,
) -> pd.DataFrame:
    ell = derived.get("ell")

    if not isinstance(ell, list):
        return pd.DataFrame()

    columns: dict[str, list[Any]] = {}

    for key in series_keys:
        values = derived.get(key)

        if isinstance(values, list):
            size = min(len(ell), len(values))
            columns[key] = values[:size]

    if not columns:
        return pd.DataFrame()

    size = min(len(values) for values in columns.values())
    frame = pd.DataFrame(
        {
            "ell": ell[:size],
            **{key: values[:size] for key, values in columns.items()},
        }
    )

    return frame.set_index("ell")


def _formatted_metric(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)

    if abs(number) >= 100.0:
        return f"{number:.3f}"

    return f"{number:.4f}"


def _line_chart(
    frame: pd.DataFrame,
    *,
    value_column: str,
    y_title: str,
    log_y: bool = False,
) -> None:
    chart_data = frame.reset_index()
    y_scale = alt.Scale(type="log", zero=False) if log_y else alt.Scale()
    chart = (
        alt.Chart(chart_data)
        .mark_line(strokeWidth=1.6)
        .encode(
            x=alt.X(
                "ell:Q",
                title="Multipole ell",
                scale=alt.Scale(domain=[0, 2500], nice=False),
            ),
            y=alt.Y(
                f"{value_column}:Q",
                title=y_title,
                scale=y_scale,
            ),
            tooltip=[
                alt.Tooltip("ell:Q", title="ell", format=".0f"),
                alt.Tooltip(
                    f"{value_column}:Q",
                    title=y_title,
                    format=".6g",
                ),
            ],
        )
        .properties(height=320)
    )
    st.altair_chart(chart, use_container_width=True)


def _comparison_chart(frame: pd.DataFrame) -> None:
    chart_data = frame.reset_index().melt(
        id_vars=["ell"],
        var_name="run",
        value_name="dl_tt_microK2",
    )
    chart = (
        alt.Chart(chart_data)
        .mark_line(strokeWidth=1.5)
        .encode(
            x=alt.X(
                "ell:Q",
                title="Multipole ell",
                scale=alt.Scale(domain=[0, 2500], nice=False),
            ),
            y=alt.Y(
                "dl_tt_microK2:Q",
                title="D_ell TT [microK^2]",
            ),
            color=alt.Color("run:N", title="Run"),
            tooltip=[
                alt.Tooltip("run:N", title="Run"),
                alt.Tooltip("ell:Q", title="ell", format=".0f"),
                alt.Tooltip(
                    "dl_tt_microK2:Q",
                    title="D_ell TT [microK^2]",
                    format=".6g",
                ),
            ],
        )
        .properties(height=360)
    )
    st.altair_chart(chart, use_container_width=True)


def render_general_class_compute_panel() -> None:
    st.subheader("General CLASS / AxiCLASS compute")

    st.caption(
        "Runs the backend /class/compute route with six editable "
        "ΛCDM-like parameters plus f_EDE and z_c, then evaluates the "
        "same model against verified DESI DR2, Planck 2018, and Pantheon+ data."
    )

    st.info(
        "Set f_EDE above zero to activate the AxiCLASS axion-like "
        "scalar-field model (n_axion=3). f_EDE=0 runs the LCDM-like "
        "branch. Planck uses Plik-lite TTTEEE + Commander low-T + SimAll low-E; "
        "Pantheon+ marginalizes the absolute-magnitude intercept analytically. "
        "These are single-point likelihoods, not a posterior."
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

        f_EDE = st.number_input(
            "f_EDE",
            min_value=0.0,
            max_value=0.5,
            value=0.082,
            step=0.001,
            format="%.6f",
            key="perfect_fit_general_class_f_EDE_v2",
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

        z_c = st.number_input(
            "z_c",
            min_value=10.0,
            max_value=100000.0,
            value=3500.0,
            step=10.0,
            format="%.3f",
            key="perfect_fit_general_class_z_c_v2",
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
        "Run CLASS / AxiCLASS computation",
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
        f_EDE=float(f_EDE),
        z_c=float(z_c),
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

    st.success("CLASS / AxiCLASS computation accepted.")

    response = result.response_payload
    try:
        artifact = save_run_artifact(
            route="class_compute",
            request=result.submitted_payload,
            response=response,
        )
    except Exception as exc:
        artifact = None
        st.warning(f"Computation succeeded, but audit artifact saving failed: {exc}")
    if artifact:
        st.caption(
            "Audit artifact saved · "
            f"SHA-256 {artifact['artifact_sha256']} · {artifact['path']}"
        )
    history = st.session_state.setdefault(HISTORY_KEY, [])
    history.append(
        {
            "submitted_payload": dict(result.submitted_payload),
            "response": dict(response),
        }
    )
    del history[:-2]

    metric_specs = (
        ("Omega_m", "Omega_m_computed", "omega_m", "Omega_m"),
        ("sigma8", "sigma8_CLASS", "sigma8"),
        ("S8", "S8_CLASS", "S8"),
        (
            "r_drag [Mpc]",
            "rs_drag_Mpc_CLASS",
            "rdrag_Mpc",
            "r_drag",
            "rs_drag",
        ),
        ("Age [Gyr]", "age_Gyr_CLASS", "age_Gyr", "age"),
        ("f_EDE achieved", "f_EDE_AxiCLASS"),
        ("z_c achieved", "z_c_AxiCLASS"),
    )

    metrics = []

    for spec in metric_specs:
        label = spec[0]
        value = _first_value(response, *spec[1:])

        if value is not None:
            metrics.append((label, value))

    if metrics:
        columns = st.columns(min(5, len(metrics)))

        for index, (label, value) in enumerate(metrics):
            columns[index % len(columns)].metric(
                label,
                _formatted_metric(value),
            )

    desi_bao = response.get("desi_dr2_bao", {})
    if isinstance(desi_bao, Mapping):
        if desi_bao.get("status") == "ok":
            st.markdown("**DESI DR2 BAO likelihood**")
            bao_columns = st.columns(2)
            bao_columns[0].metric(
                "log likelihood",
                _formatted_metric(desi_bao.get("loglike")),
            )
            bao_columns[1].metric(
                "χ² (13 observables)",
                _formatted_metric(desi_bao.get("chi2")),
            )
            theory_rows = desi_bao.get("theory_vector")
            if isinstance(theory_rows, list) and theory_rows:
                with st.expander("DESI DR2 BAO theory vector", expanded=False):
                    st.dataframe(
                        pd.DataFrame(theory_rows),
                        hide_index=True,
                        use_container_width=True,
                    )
                    source_identity = desi_bao.get("source_identity")
                    if isinstance(source_identity, Mapping):
                        st.caption("Official input file identities")
                        st.json(dict(source_identity))
        elif desi_bao.get("status") == "failed":
            st.error(
                "CLASS/AxiCLASS completed, but DESI DR2 BAO likelihood "
                f"evaluation failed: {desi_bao.get('detail', 'unknown error')}"
            )

    joint = response.get("joint_likelihood", {})
    if isinstance(joint, Mapping) and joint.get("status") == "ok":
        st.markdown("### Joint likelihood atlas")
        st.caption(
            "Independent component values evaluated for this exact AxiCLASS output. "
            "The displayed sum is a goodness-of-fit coordinate, not Bayesian evidence."
        )
        components = joint.get("components", [])
        if isinstance(components, list) and components:
            component_frame = pd.DataFrame(components)
            columns = st.columns(3)
            columns[0].metric("Components", int(joint.get("component_count", 0)))
            columns[1].metric("Σ log L", _formatted_metric(joint.get("loglike_sum")))
            columns[2].metric("Σ effective χ²", _formatted_metric(joint.get("chi2_effective_sum")))
            waterfall = (
                alt.Chart(component_frame)
                .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
                .encode(
                    x=alt.X("dataset:N", title=None, sort=None),
                    y=alt.Y("chi2:Q", title="χ² contribution"),
                    color=alt.Color("dataset:N", legend=None, scale=alt.Scale(scheme="tableau10")),
                    tooltip=["dataset:N", alt.Tooltip("loglike:Q", format=".5f"), alt.Tooltip("chi2:Q", format=".5f")],
                )
                .properties(height=300)
            )
            st.altair_chart(waterfall, use_container_width=True)
            st.dataframe(component_frame, hide_index=True, use_container_width=True)

    for label, key in (("Planck 2018", "planck_2018"), ("Pantheon+", "pantheon_plus")):
        component = response.get(key, {})
        if isinstance(component, Mapping):
            if component.get("status") == "ok":
                with st.expander(f"{label} likelihood details"):
                    st.json(dict(component))
            elif component.get("status") == "unavailable":
                st.warning(f"{label} assets were unavailable: {component.get('detail')}")

    derived = response.get("derived", {})

    if isinstance(derived, Mapping):
        temperature_scale = T_CMB_K * T_CMB_K * K2_TO_UK2
        spectrum_specs = (
            ("TT", "dl_tt"),
            ("TE", "dl_te"),
            ("EE", "dl_ee"),
        )

        available_spectra = [
            (label, key)
            for label, key in spectrum_specs
            if isinstance(derived.get(key), list)
        ]

        if available_spectra:
            st.markdown("**CMB angular power spectra**")
            st.caption(
                "D_ell = ell(ell+1)C_ell/(2pi), converted from "
                "dimensionless CLASS lensed spectra to microK^2 "
                f"using T_CMB = {T_CMB_K} K."
            )

            for label, key in available_spectra:
                frame = _spectrum_frame(derived, key)

                if frame.empty:
                    continue

                value_column = f"{label}_microK2"
                frame = frame.rename(columns={key: value_column})
                frame *= temperature_scale
                st.markdown(f"**{label} spectrum**")
                _line_chart(
                    frame,
                    value_column=value_column,
                    y_title=f"D_ell {label} [microK^2]",
                )

        lensing_frame = _spectrum_frame(derived, "cl_pp")

        if not lensing_frame.empty:
            st.markdown("**CMB lensing spectrum**")
            lensing_frame = lensing_frame[
                lensing_frame["cl_pp"] > 0.0
            ]
            _line_chart(
                lensing_frame,
                value_column="cl_pp",
                y_title="C_ell phi-phi",
                log_y=True,
            )

        if len(history) == 2:
            previous_response = history[0].get("response", {})
            previous_derived = previous_response.get("derived", {})

            if isinstance(previous_derived, Mapping):
                current_tt = _spectrum_frame(derived, "dl_tt")
                previous_tt = _spectrum_frame(
                    previous_derived,
                    "dl_tt",
                )

                if not current_tt.empty and not previous_tt.empty:
                    comparison = pd.concat(
                        [
                            previous_tt.rename(
                                columns={"dl_tt": "Previous run"}
                            ),
                            current_tt.rename(
                                columns={"dl_tt": "Current run"}
                            ),
                        ],
                        axis=1,
                    )
                    comparison *= temperature_scale
                    st.markdown("**Previous-run comparison**")
                    st.caption(
                        "TT spectra from the current and immediately "
                        "preceding calculations."
                    )
                    _comparison_chart(comparison)

                delta_specs = (
                    ("Omega_m", "Omega_m_computed"),
                    ("sigma8", "sigma8_CLASS"),
                    ("S8", "S8_CLASS"),
                    ("r_drag [Mpc]", "rs_drag_Mpc_CLASS"),
                    ("Age [Gyr]", "age_Gyr_CLASS"),
                    ("f_EDE achieved", "f_EDE_AxiCLASS"),
                    ("z_c achieved", "z_c_AxiCLASS"),
                )
                delta_rows = []

                for label, key in delta_specs:
                    current_value = derived.get(key)
                    previous_value = previous_derived.get(key)

                    try:
                        current_number = float(current_value)
                        previous_number = float(previous_value)
                    except (TypeError, ValueError):
                        continue

                    delta_rows.append(
                        {
                            "quantity": label,
                            "previous": previous_number,
                            "current": current_number,
                            "delta": current_number - previous_number,
                        }
                    )

                if delta_rows:
                    st.dataframe(
                        pd.DataFrame(delta_rows),
                        hide_index=True,
                        use_container_width=True,
                    )

        export_frame = _spectrum_frame(
            derived,
            "dl_tt",
            "dl_te",
            "dl_ee",
            "cl_pp",
        ).reset_index()

        if not export_frame.empty:
            for key in ("dl_tt", "dl_te", "dl_ee"):
                if key in export_frame.columns:
                    export_frame[key] *= temperature_scale

            export_frame = export_frame.rename(
                columns={
                    "dl_tt": "dl_tt_microK2",
                    "dl_te": "dl_te_microK2",
                    "dl_ee": "dl_ee_microK2",
                }
            )

            st.markdown("**Download results**")
            download_columns = st.columns(3)
            download_columns[0].download_button(
                "Download spectra CSV",
                data=export_frame.to_csv(index=False),
                file_name="general_class_cmb_spectra.csv",
                mime="text/csv",
                key="general_class_spectra_csv_download_v1",
                use_container_width=True,
            )

            summary = {
                "Omega_m": derived.get("Omega_m_computed"),
                "sigma8": derived.get("sigma8_CLASS"),
                "S8": derived.get("S8_CLASS"),
                "r_drag_Mpc": derived.get("rs_drag_Mpc_CLASS"),
                "age_Gyr": derived.get("age_Gyr_CLASS"),
                "f_EDE_target": derived.get("f_EDE_target"),
                "f_EDE_achieved": derived.get("f_EDE_AxiCLASS"),
                "z_c_target": derived.get("z_c_target"),
                "z_c_achieved": derived.get("z_c_AxiCLASS"),
                "desi_dr2_bao_loglike": (
                    desi_bao.get("loglike")
                    if isinstance(desi_bao, Mapping)
                    else None
                ),
                "desi_dr2_bao_chi2": (
                    desi_bao.get("chi2")
                    if isinstance(desi_bao, Mapping)
                    else None
                ),
                "planck_2018_loglike": response.get("planck_2018", {}).get("loglike") if isinstance(response.get("planck_2018"), Mapping) else None,
                "pantheon_plus_loglike": response.get("pantheon_plus", {}).get("loglike") if isinstance(response.get("pantheon_plus"), Mapping) else None,
                "joint_loglike_sum": joint.get("loglike_sum") if isinstance(joint, Mapping) else None,
            }
            download_columns[1].download_button(
                "Download summary CSV",
                data=pd.DataFrame([summary]).to_csv(index=False),
                file_name="general_class_summary.csv",
                mime="text/csv",
                key="general_class_summary_csv_download_v1",
                use_container_width=True,
            )
            download_columns[2].download_button(
                "Download complete JSON",
                data=json.dumps(response, ensure_ascii=False, indent=2),
                file_name="general_class_response.json",
                mime="application/json",
                key="general_class_json_download_v1",
                use_container_width=True,
            )

    with st.expander("Complete backend response", expanded=False):
        st.json(dict(response))

    st.caption(
        "Boundary: this panel performs direct CLASS/AxiCLASS physical "
        "propagation and evaluates verified DESI DR2 BAO, Planck 2018, and "
        "Pantheon+ likelihood components at one parameter point. It does not "
        "run posterior inference or MCMC."
    )
