"""Finite H0-grid audit across the three installed likelihood components."""

from __future__ import annotations

from typing import Any, Mapping

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from dti_ui_v1.services.general_class_compute_service import GeneralClassRequest, execute_general_class_compute
from dti_ui_v1.services.run_store import save_run_artifact


COMPONENTS = (
    ("DESI DR2 BAO", "desi_dr2_bao", "chi2"),
    ("Planck 2018", "planck_2018", "chi2_effective"),
    ("Pantheon+ relative SN", "pantheon_plus", "chi2"),
)


def _finite_component(response: Mapping[str, Any], response_key: str, chi2_key: str) -> float | None:
    component = response.get(response_key, {})
    if not isinstance(component, Mapping) or component.get("status") != "ok":
        return None
    try:
        value = float(component.get(chi2_key))
    except (TypeError, ValueError):
        return None
    return value if np.isfinite(value) else None


def render_general_class_profile_panel() -> None:
    st.subheader("Joint H₀ grid trade-off audit")
    st.caption(
        "Runs independent AxiCLASS points and follows DESI DR2, Planck 2018, and relative Pantheon+ "
        "coordinates across one finite H₀ grid. The minimum is a recorded grid coordinate, not a posterior estimate."
    )
    c1, c2, c3 = st.columns(3)
    start = c1.number_input("H0 grid start", 40.0, 100.0, 63.0, 1.0)
    stop = c2.number_input("H0 grid stop", 40.0, 100.0, 75.0, 1.0)
    points = c3.number_input("Grid points", 3, 11, 5, 1)
    f_ede = st.number_input("Profile f_EDE", 0.0, 0.5, 0.082, 0.001, format="%.6f")
    z_c = st.number_input("Profile z_c", 10.0, 100000.0, 3500.0, 10.0)
    st.info(
        "The published local distance-ladder summary is not included in this joint sum because it overlaps "
        "Pantheon+/SH0ES supernova information. Its pull is audited separately in Consistency."
    )
    if not st.button("Run joint H0 grid audit", type="primary"):
        return
    if stop <= start:
        st.error("H0 grid stop must be greater than start.")
        return

    rows: list[dict[str, float]] = []
    failures: list[dict[str, Any]] = []
    progress = st.progress(0.0)
    values = np.linspace(float(start), float(stop), int(points))
    for index, h0 in enumerate(values):
        result = execute_general_class_compute(
            GeneralClassRequest(
                H0=float(h0),
                omega_b=0.0244,
                omega_cdm=0.127,
                n_s=0.9847,
                ln10_10_As=3.058,
                tau_reio=0.0511,
                f_EDE=float(f_ede),
                z_c=float(z_c),
                timeout_seconds=240,
            )
        )
        response = result.response_payload if isinstance(result.response_payload, Mapping) else {}
        component_values = {
            label: _finite_component(response, response_key, chi2_key)
            for label, response_key, chi2_key in COMPONENTS
        }
        joint = response.get("joint_likelihood", {})
        joint_chi2 = None
        if isinstance(joint, Mapping) and joint.get("status") == "ok":
            try:
                joint_chi2 = float(joint.get("chi2_effective_sum"))
            except (TypeError, ValueError):
                joint_chi2 = None
        if (
            result.accepted
            and all(value is not None for value in component_values.values())
            and joint_chi2 is not None
            and np.isfinite(joint_chi2)
        ):
            rows.append(
                {
                    "H0": float(h0),
                    "DESI DR2 BAO": float(component_values["DESI DR2 BAO"]),
                    "Planck 2018": float(component_values["Planck 2018"]),
                    "Pantheon+ relative SN": float(component_values["Pantheon+ relative SN"]),
                    "Independent component sum": float(joint_chi2),
                }
            )
        else:
            missing = [label for label, value in component_values.items() if value is None]
            if joint_chi2 is None:
                missing.append("Independent component sum")
            failures.append(
                {
                    "H0": float(h0),
                    "status": result.status,
                    "missing_or_failed": ", ".join(missing),
                    "detail": result.detail,
                }
            )
        progress.progress((index + 1) / len(values))

    if failures:
        st.error("One or more grid points lacked a required likelihood coordinate; no minimum claim is made.")
        st.dataframe(failures, hide_index=True, width="stretch")
        return

    frame = pd.DataFrame(rows)
    best = frame.loc[frame["Independent component sum"].idxmin()].to_dict()
    coordinate_columns = [label for label, _, _ in COMPONENTS] + ["Independent component sum"]
    for column in coordinate_columns:
        frame[f"Δχ² {column}"] = frame[column] - frame[column].min()

    artifact_rows = frame[["H0", *coordinate_columns]].to_dict(orient="records")
    artifact = save_run_artifact(
        route="class_joint_h0_grid_tradeoff_audit",
        request={"H0_start": start, "H0_stop": stop, "points": points, "f_EDE": f_ede, "z_c": z_c},
        response={
            "status": "ok",
            "grid": artifact_rows,
            "recorded_joint_grid_minimum": best,
            "local_ladder_combination": "EXCLUDED_OVERLAP_SAFE",
        },
    )
    st.success(
        f"Grid complete. Recorded independent-component minimum: H₀={best['H0']:.6g}, "
        f"Σχ²={best['Independent component sum']:.6g}."
    )

    delta_columns = [f"Δχ² {column}" for column in coordinate_columns]
    long_frame = frame[["H0", *delta_columns]].melt(
        id_vars="H0", var_name="Rail", value_name="Delta chi-square"
    )
    long_frame["Rail"] = long_frame["Rail"].str.replace("Δχ² ", "", regex=False)
    chart = (
        alt.Chart(long_frame)
        .mark_line(point=True)
        .encode(
            x=alt.X("H0:Q", title="H₀ [km s⁻¹ Mpc⁻¹]"),
            y=alt.Y("Delta chi-square:Q", title="Δχ² from each rail's grid minimum"),
            color=alt.Color("Rail:N", title="Observational rail"),
            strokeWidth=alt.condition("datum.Rail == 'Independent component sum'", alt.value(4), alt.value(2)),
            tooltip=[
                alt.Tooltip("H0:Q", format=".6g"),
                "Rail:N",
                alt.Tooltip("Delta chi-square:Q", format=".8g"),
            ],
        )
        .properties(height=430)
    )
    st.altair_chart(chart, width="stretch")
    st.dataframe(frame, hide_index=True, width="stretch")
    if best["H0"] in (float(start), float(stop)):
        st.warning("The recorded joint grid minimum is on a boundary; behavior outside the grid is not inferred.")
    st.caption(
        "Each component curve is zeroed at its own finite-grid minimum to expose cross-dataset trade-offs. "
        "The displayed sum assumes only the three backend components."
    )
    st.caption(f"Audit artifact SHA-256 {artifact['artifact_sha256']} · {artifact['path']}")
