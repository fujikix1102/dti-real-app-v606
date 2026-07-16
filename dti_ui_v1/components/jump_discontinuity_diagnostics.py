"""Display-only sharp-transition diagnostics for the DTI toy comparator.

This component evaluates the existing tanh-wall proxy geometry only.
It does not execute CLASS/AxiCLASS, a likelihood, chi-square, MCMC,
posterior inference, or manuscript-level scientific validation.
"""

from __future__ import annotations

from dataclasses import dataclass

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


@dataclass(frozen=True)
class JumpBranch:
    branch_id: str
    label: str
    zc: float
    amplitude: float


BRANCH_ORDER: tuple[str, ...] = (
    "Strategy A",
    "Hybrid A+B",
    "Strategy B",
)

BRANCH_COLORS: tuple[str, ...] = (
    "#4C78A8",
    "#54A24B",
    "#F58518",
)

BRANCH_DASHES: tuple[tuple[int, ...], ...] = (
    (1, 0),
    (8, 4),
    (2, 3),
)


DEFAULT_BRANCHES: tuple[JumpBranch, ...] = (
    JumpBranch(
        branch_id="A",
        label="Strategy A",
        zc=0.78105,
        amplitude=1.00,
    ),
    JumpBranch(
        branch_id="B",
        label="Strategy B",
        zc=0.87505,
        amplitude=1.00,
    ),
    JumpBranch(
        branch_id="HYBRID",
        label="Hybrid A+B",
        zc=0.82805,
        amplitude=1.00,
    ),
)


def transition_profile(
    z: np.ndarray,
    *,
    zc: float,
    dz: float,
    amplitude: float,
) -> np.ndarray:
    """Dimensionless tanh-wall transition response."""

    safe_dz = max(float(dz), 1.0e-8)

    return amplitude * 0.5 * (
        1.0 + np.tanh((z - zc) / safe_dz)
    )


def transition_derivative(
    z: np.ndarray,
    y: np.ndarray,
) -> np.ndarray:
    """Numerical dY/dz on the displayed grid."""

    return np.gradient(y, z)


def branch_frame(
    *,
    branch: JumpBranch,
    dz: float,
    amplitude_scale: float,
    z_min: float,
    z_max: float,
    point_count: int,
) -> pd.DataFrame:
    z = np.linspace(
        z_min,
        z_max,
        int(point_count),
        dtype=float,
    )

    y = transition_profile(
        z,
        zc=branch.zc,
        dz=dz,
        amplitude=branch.amplitude * amplitude_scale,
    )

    derivative = transition_derivative(z, y)

    adjacent = np.empty_like(y)
    adjacent[:] = np.nan
    adjacent[1:] = np.abs(np.diff(y))

    return pd.DataFrame(
        {
            "z": z,
            "Y": y,
            "dY_dz": derivative,
            "abs_dY_dz": np.abs(derivative),
            "adjacent_jump": adjacent,
            "branch_id": branch.branch_id,
            "branch": branch.label,
            "zc": branch.zc,
            "dz": dz,
        }
    )


def derivative_peak_width_fwhm(
    frame: pd.DataFrame,
) -> float:
    """Return the full width at half maximum of |dY/dz|."""

    ordered = frame.sort_values(
        "z",
        kind="stable",
    )

    z = ordered["z"].to_numpy(dtype=float)
    slope = ordered["abs_dY_dz"].to_numpy(dtype=float)

    if len(z) < 3:
        return float("nan")

    peak = float(np.nanmax(slope))

    if not np.isfinite(peak) or peak <= 0:
        return float("nan")

    above = slope >= 0.5 * peak
    indices = np.flatnonzero(above)

    if len(indices) < 2:
        return float("nan")

    return float(
        z[indices[-1]] - z[indices[0]]
    )


def diagnostic_summary(
    frame: pd.DataFrame,
    *,
    zc: float,
    epsilon: float,
) -> dict[str, float]:
    max_slope_index = frame["abs_dY_dz"].idxmax()
    max_jump_index = frame["adjacent_jump"].idxmax()

    z_values = frame["z"].to_numpy(dtype=float)
    y_values = frame["Y"].to_numpy(dtype=float)

    left_z = zc - epsilon
    right_z = zc + epsilon

    left_value = float(np.interp(left_z, z_values, y_values))
    right_value = float(np.interp(right_z, z_values, y_values))

    return {
        "max_abs_dY_dz": float(
            frame.loc[max_slope_index, "abs_dY_dz"]
        ),
        "max_slope_z": float(
            frame.loc[max_slope_index, "z"]
        ),
        "max_adjacent_jump": float(
            frame.loc[max_jump_index, "adjacent_jump"]
        ),
        "max_adjacent_jump_z": float(
            frame.loc[max_jump_index, "z"]
        ),
        "left_sample_z": left_z,
        "right_sample_z": right_z,
        "left_value": left_value,
        "right_value": right_value,
        "finite_window_jump": right_value - left_value,
        "derivative_fwhm": derivative_peak_width_fwhm(
            frame
        ),
    }


def _line_chart(
    data: pd.DataFrame,
    *,
    y_column: str,
    title: str,
    y_title: str,
    height: int = 330,
) -> None:
    chart = (
        alt.Chart(data)
        .mark_line()
        .encode(
            x=alt.X(
                "z:Q",
                title="Redshift z",
                scale=alt.Scale(zero=False),
            ),
            y=alt.Y(
                f"{y_column}:Q",
                title=y_title,
                scale=alt.Scale(zero=False),
            ),
            color=alt.Color(
                "branch:N",
                title="Branch",
                sort=list(BRANCH_ORDER),
                scale=alt.Scale(
                    domain=list(BRANCH_ORDER),
                    range=list(BRANCH_COLORS),
                ),
            ),
            strokeDash=alt.StrokeDash(
                "branch:N",
                title="Branch",
                sort=list(BRANCH_ORDER),
                scale=alt.Scale(
                    domain=list(BRANCH_ORDER),
                    range=[
                        list(pattern)
                        for pattern in BRANCH_DASHES
                    ],
                ),
            ),
            tooltip=[
                alt.Tooltip("branch:N", title="Branch"),
                alt.Tooltip("z:Q", title="z", format=".6f"),
                alt.Tooltip(
                    f"{y_column}:Q",
                    title=y_title,
                    format=".8f",
                ),
                alt.Tooltip("zc:Q", title="zc", format=".6f"),
                alt.Tooltip("dz:Q", title="dz", format=".6f"),
            ],
        )
        .properties(
            title=title,
            height=height,
        )
        .interactive()
    )

    zc_frame = (
        data[
            [
                "branch",
                "zc",
            ]
        ]
        .drop_duplicates()
        .rename(
            columns={
                "zc": "z",
            }
        )
    )

    zc_rules = (
        alt.Chart(zc_frame)
        .mark_rule(
            opacity=0.45,
            strokeWidth=1.5,
        )
        .encode(
            x=alt.X(
                "z:Q",
                title="Redshift z",
            ),
            color=alt.Color(
                "branch:N",
                legend=None,
                sort=list(BRANCH_ORDER),
                scale=alt.Scale(
                    domain=list(BRANCH_ORDER),
                    range=list(BRANCH_COLORS),
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "branch:N",
                    title="Branch",
                ),
                alt.Tooltip(
                    "z:Q",
                    title="zc",
                    format=".6f",
                ),
            ],
        )
    )

    st.altair_chart(
        chart + zc_rules,
        use_container_width=True,
    )


def _render_dz_dependence(
    *,
    branch: JumpBranch,
    amplitude_scale: float,
    z_min: float,
    z_max: float,
    point_count: int,
) -> None:
    dz_values = (
        0.200,
        0.100,
        0.040,
        0.020,
        0.010,
        0.005,
    )

    rows: list[dict[str, float]] = []

    for dz in dz_values:
        frame = branch_frame(
            branch=branch,
            dz=dz,
            amplitude_scale=amplitude_scale,
            z_min=z_min,
            z_max=z_max,
            point_count=point_count,
        )

        summary = diagnostic_summary(
            frame,
            zc=branch.zc,
            epsilon=max(dz, 1.0e-4),
        )

        rows.append(
            {
                "dz": dz,
                "max_abs_dY_dz": summary["max_abs_dY_dz"],
                "peak_position_z": summary["max_slope_z"],
                "derivative_fwhm": summary[
                    "derivative_fwhm"
                ],
                "max_adjacent_jump": summary[
                    "max_adjacent_jump"
                ],
                "finite_window_jump": summary[
                    "finite_window_jump"
                ],
            }
        )

    dependence = pd.DataFrame(rows)

    first_row_left, first_row_right = st.columns(2)

    with first_row_left:
        chart = (
            alt.Chart(dependence)
            .mark_line(point=True)
            .encode(
                x=alt.X(
                    "dz:Q",
                    title="Wall softness dz",
                    scale=alt.Scale(
                        type="log",
                        reverse=True,
                    ),
                ),
                y=alt.Y(
                    "max_abs_dY_dz:Q",
                    title="max |dY/dz|",
                    scale=alt.Scale(zero=False),
                ),
                tooltip=[
                    alt.Tooltip("dz:Q", format=".6f"),
                    alt.Tooltip(
                        "max_abs_dY_dz:Q",
                        format=".8f",
                    ),
                ],
            )
            .properties(
                title="Peak slope versus dz",
                height=320,
            )
        )

        st.altair_chart(
            chart,
            use_container_width=True,
        )

    with first_row_right:
        chart = (
            alt.Chart(dependence)
            .mark_line(point=True)
            .encode(
                x=alt.X(
                    "dz:Q",
                    title="Wall softness dz",
                    scale=alt.Scale(
                        type="log",
                        reverse=True,
                    ),
                ),
                y=alt.Y(
                    "derivative_fwhm:Q",
                    title="Derivative peak FWHM",
                    scale=alt.Scale(zero=False),
                ),
                tooltip=[
                    alt.Tooltip("dz:Q", format=".6f"),
                    alt.Tooltip(
                        "derivative_fwhm:Q",
                        format=".8f",
                    ),
                    alt.Tooltip(
                        "peak_position_z:Q",
                        format=".8f",
                    ),
                ],
            )
            .properties(
                title="Derivative peak width versus dz",
                height=320,
            )
        )

        st.altair_chart(
            chart,
            use_container_width=True,
        )

    second_row_left, second_row_right = st.columns(2)

    with second_row_left:
        chart = (
            alt.Chart(dependence)
            .mark_line(point=True)
            .encode(
                x=alt.X(
                    "dz:Q",
                    title="Wall softness dz",
                    scale=alt.Scale(
                        type="log",
                        reverse=True,
                    ),
                ),
                y=alt.Y(
                    "max_adjacent_jump:Q",
                    title="max |Y(i+1)-Y(i)|",
                    scale=alt.Scale(zero=False),
                ),
                tooltip=[
                    alt.Tooltip(
                        "dz:Q",
                        format=".6f",
                    ),
                    alt.Tooltip(
                        "max_adjacent_jump:Q",
                        format=".8f",
                    ),
                ],
            )
            .properties(
                title="Adjacent-grid score versus dz",
                height=300,
            )
        )

        st.altair_chart(
            chart,
            use_container_width=True,
        )

    with second_row_right:
        chart = (
            alt.Chart(dependence)
            .mark_line(point=True)
            .encode(
                x=alt.X(
                    "dz:Q",
                    title="Wall softness dz",
                    scale=alt.Scale(
                        type="log",
                        reverse=True,
                    ),
                ),
                y=alt.Y(
                    "peak_position_z:Q",
                    title="Peak position z",
                    scale=alt.Scale(zero=False),
                ),
                tooltip=[
                    alt.Tooltip(
                        "dz:Q",
                        format=".6f",
                    ),
                    alt.Tooltip(
                        "peak_position_z:Q",
                        format=".8f",
                    ),
                ],
            )
            .properties(
                title="Peak-position stability",
                height=300,
            )
        )

        st.altair_chart(
            chart,
            use_container_width=True,
        )

    st.dataframe(
        dependence,
        use_container_width=True,
        hide_index=True,
    )


def _branch_identity_frame(
    combined: pd.DataFrame,
) -> pd.DataFrame:
    """Select the branch with largest local |dY/dz| at each z."""

    reduced = combined[
        [
            "z",
            "branch",
            "branch_id",
            "abs_dY_dz",
        ]
    ].copy()

    index = reduced.groupby("z")["abs_dY_dz"].idxmax()
    identity = reduced.loc[index].sort_values("z").reset_index(drop=True)

    previous = identity["branch_id"].shift(1)
    identity["branch_switch"] = (
        identity["branch_id"] != previous
    )

    if not identity.empty:
        identity.loc[0, "branch_switch"] = False

    return identity


def render_jump_discontinuity_diagnostics() -> None:
    st.subheader("Jump / sharp-transition diagnostics")

    st.caption(
        "Display-only diagnostics for the existing tanh-wall toy model. "
        "Finite dz gives a continuous sharp transition, not a proven "
        "mathematical discontinuity or observed cosmological phase transition."
    )

    control_left, control_middle, control_right = st.columns(3)

    with control_left:
        dz = st.number_input(
            "Wall softness dz",
            min_value=0.001,
            max_value=0.500,
            value=0.040,
            step=0.0001,
            format="%.6f",
            key="perfect_fit_jump_diag_dz",
        )

    with control_middle:
        amplitude_scale = st.number_input(
            "Proxy amplitude scale",
            min_value=0.01,
            max_value=10.00,
            value=1.00,
            step=0.001,
            format="%.6f",
            key="perfect_fit_jump_diag_amplitude",
        )

    with control_right:
        epsilon = st.number_input(
            "Finite-window epsilon",
            min_value=0.0001,
            max_value=0.5000,
            value=0.0200,
            step=0.0001,
            format="%.6f",
            key="perfect_fit_jump_diag_epsilon",
        )

    z_min = 0.0
    z_max = 1.5
    minimum_scale = min(
        float(dz),
        float(epsilon),
    )

    if minimum_scale >= 0.01:
        point_count = 3001
    elif minimum_scale >= 0.001:
        point_count = 15001
    else:
        point_count = 60001

    frames = [
        branch_frame(
            branch=branch,
            dz=float(dz),
            amplitude_scale=float(amplitude_scale),
            z_min=z_min,
            z_max=z_max,
            point_count=point_count,
        )
        for branch in DEFAULT_BRANCHES
    ]

    combined = pd.concat(
        frames,
        ignore_index=True,
    )

    (
        profile_tab,
        derivative_tab,
        adjacent_tab,
        limits_tab,
        dz_tab,
        branch_tab,
    ) = st.tabs(
        (
            "Transition profile",
            "max |dY/dz|",
            "Adjacent difference",
            "zc±ε",
            "dz dependence",
            "Branch switching",
        )
    )

    with profile_tab:
        _line_chart(
            combined,
            y_column="Y",
            title="Sharp-transition proxy profiles",
            y_title="Y",
        )

    with derivative_tab:
        _line_chart(
            combined,
            y_column="abs_dY_dz",
            title="Local transition slope",
            y_title="|dY/dz|",
        )

        rows = []

        for branch, frame in zip(DEFAULT_BRANCHES, frames):
            summary = diagnostic_summary(
                frame,
                zc=branch.zc,
                epsilon=float(epsilon),
            )

            rows.append(
                {
                    "branch": branch.label,
                    "zc": branch.zc,
                    "max_abs_dY_dz": summary[
                        "max_abs_dY_dz"
                    ],
                    "max_slope_z": summary[
                        "max_slope_z"
                    ],
                }
            )

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )

    with adjacent_tab:
        adjacent_data = combined.dropna(
            subset=["adjacent_jump"]
        )

        _line_chart(
            adjacent_data,
            y_column="adjacent_jump",
            title="Adjacent-grid transition score",
            y_title="|Y(i+1) − Y(i)|",
        )

        rows = []

        for branch, frame in zip(DEFAULT_BRANCHES, frames):
            summary = diagnostic_summary(
                frame,
                zc=branch.zc,
                epsilon=float(epsilon),
            )

            rows.append(
                {
                    "branch": branch.label,
                    "zc": branch.zc,
                    "max_adjacent_difference": summary[
                        "max_adjacent_jump"
                    ],
                    "location_z": summary[
                        "max_adjacent_jump_z"
                    ],
                    "grid_spacing": (
                        z_max - z_min
                    ) / (point_count - 1),
                }
            )

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )

    with limits_tab:
        rows = []

        for branch, frame in zip(DEFAULT_BRANCHES, frames):
            summary = diagnostic_summary(
                frame,
                zc=branch.zc,
                epsilon=float(epsilon),
            )

            rows.append(
                {
                    "branch": branch.label,
                    "zc": branch.zc,
                    "epsilon": float(epsilon),
                    "Y(zc-epsilon)": summary["left_value"],
                    "Y(zc+epsilon)": summary["right_value"],
                    "finite_window_difference": summary[
                        "finite_window_jump"
                    ],
                    "strict_continuity_for_finite_dz": "YES",
                }
            )

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            "For finite dz, tanh is continuous. These are finite-window "
            "left/right samples, not unequal mathematical one-sided limits."
        )

    with dz_tab:
        branch_label = st.selectbox(
            "Branch for dz scan",
            options=tuple(
                branch.label
                for branch in DEFAULT_BRANCHES
            ),
            key="perfect_fit_jump_diag_dz_branch",
        )

        selected_branch = next(
            branch
            for branch in DEFAULT_BRANCHES
            if branch.label == branch_label
        )

        _render_dz_dependence(
            branch=selected_branch,
            amplitude_scale=float(amplitude_scale),
            z_min=z_min,
            z_max=z_max,
            point_count=point_count,
        )

    with branch_tab:
        identity = _branch_identity_frame(combined)

        identity_numeric = identity.copy()
        mapping = {
            "A": 1,
            "B": 2,
            "HYBRID": 3,
        }

        identity_numeric["branch_code"] = (
            identity_numeric["branch_id"].map(mapping)
        )

        chart = (
            alt.Chart(identity_numeric)
            .mark_line(
                interpolate="step-after"
            )
            .encode(
                x=alt.X(
                    "z:Q",
                    title="Redshift z",
                ),
                y=alt.Y(
                    "branch_code:Q",
                    title="Proxy dominant branch",
                    scale=alt.Scale(
                        domain=[0.5, 3.5],
                    ),
                    axis=alt.Axis(
                        values=[1, 2, 3],
                        labelExpr=(
                            "datum.value == 1 ? 'A' : "
                            "datum.value == 2 ? 'B' : "
                            "'Hybrid'"
                        ),
                    ),
                ),
                tooltip=[
                    alt.Tooltip("z:Q", format=".6f"),
                    alt.Tooltip("branch:N"),
                    alt.Tooltip(
                        "abs_dY_dz:Q",
                        title="|dY/dz|",
                        format=".8f",
                    ),
                ],
            )
            .properties(
                title=(
                    "Branch with largest local proxy transition slope"
                ),
                height=320,
            )
        )

        st.altair_chart(
            chart,
            use_container_width=True,
        )

        switches = identity[
            identity["branch_switch"]
        ][
            [
                "z",
                "branch",
                "branch_id",
                "abs_dY_dz",
            ]
        ]

        st.dataframe(
            switches,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "Branch identity here means the branch with the largest "
            "local toy-model |dY/dz|. It is not a likelihood-selected "
            "physical branch."
        )

    with st.expander("Diagnostic definition and boundaries"):
        st.code(
            "\n".join(
                [
                    "Y(z)=A/2*[1+tanh((z-zc)/dz)]",
                    "derivative=numerical gradient on displayed grid",
                    "adjacent_score=abs(Y[i+1]-Y[i])",
                    "left_right=Y(zc-epsilon), Y(zc+epsilon)",
                    "branch_identity=max local abs(dY/dz)",
                    "finite_dz_continuous=YES",
                    "CLASS_or_AxiCLASS=NO",
                    "likelihood=NO",
                    "chi_square=NO",
                    "MCMC=NO",
                    "posterior=NO",
                    "phase_transition_detection_claim=NO",
                ]
            ),
            language="text",
        )
