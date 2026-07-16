"""Source-locked Fixed-H0 BAO diagnostic charts.

The component displays the five legacy scientific series using the
existing verified loader and 27-point asset bundle. No scientific
recomputation is performed.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from dti_fixed_h0_bao_r1_loader_v1 import (
    FixedH0BAOAssetError,
    load_fixed_h0_bao_r1_assets,
)


@dataclass(frozen=True)
class ChartDefinition:
    column: str
    title: str
    y_title: str
    decimals: int


CHARTS: tuple[ChartDefinition, ...] = (
    ChartDefinition(
        column="chi2",
        title="Conditional BAO χ²",
        y_title="χ²",
        decimals=6,
    ),
    ChartDefinition(
        column="delta_chi2_from_recorded_minimum",
        title="Δχ² from recorded minimum",
        y_title="Δχ²",
        decimals=6,
    ),
    ChartDefinition(
        column="omega_b",
        title="Baryon density",
        y_title="Ωb",
        decimals=6,
    ),
    ChartDefinition(
        column="omega_cdm",
        title="Cold-dark-matter density",
        y_title="Ωcdm",
        decimals=6,
    ),
    ChartDefinition(
        column="rdrag_Mpc",
        title="Sound horizon",
        y_title="rdrag [Mpc]",
        decimals=4,
    ),
)

REQUIRED_COLUMNS: tuple[str, ...] = (
    "H0",
    *(chart.column for chart in CHARTS),
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


@st.cache_data(show_spinner=False)
def load_points_table() -> pd.DataFrame:
    """Load the verified point record through the existing loader."""

    assets = load_fixed_h0_bao_r1_assets(_repo_root())
    frame = pd.DataFrame(assets.points)

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in frame.columns
    ]

    if missing:
        raise FixedH0BAOAssetError(
            "missing graph columns: " + ", ".join(missing)
        )

    frame = frame.copy()

    for column in REQUIRED_COLUMNS:
        frame[column] = pd.to_numeric(
            frame[column],
            errors="raise",
        )

    frame = frame.sort_values(
        "H0",
        kind="stable",
    ).reset_index(drop=True)

    if len(frame) != 27:
        raise FixedH0BAOAssetError(
            f"unexpected point count: {len(frame)}"
        )

    return frame


def _axis_domain(series: pd.Series) -> list[float]:
    """Return a padded display domain without changing source values."""

    minimum = float(series.min())
    maximum = float(series.max())
    span = maximum - minimum

    if span == 0:
        padding = max(abs(minimum) * 0.02, 1e-9)
    else:
        padding = span * 0.08

    return [
        minimum - padding,
        maximum + padding,
    ]


def _render_chart(
    frame: pd.DataFrame,
    definition: ChartDefinition,
    *,
    height: int = 330,
) -> None:
    """Render a source-value-preserving line and point chart."""

    plot_frame = frame[
        [
            "H0",
            definition.column,
            "target_id",
            "classification",
            "source_class",
        ]
    ].copy()

    y_domain = _axis_domain(plot_frame[definition.column])

    base = alt.Chart(plot_frame).encode(
        x=alt.X(
            "H0:Q",
            title="H0 [km s⁻¹ Mpc⁻¹]",
            scale=alt.Scale(zero=False),
        ),
        y=alt.Y(
            f"{definition.column}:Q",
            title=definition.y_title,
            scale=alt.Scale(
                zero=False,
                domain=y_domain,
            ),
        ),
        tooltip=[
            alt.Tooltip(
                "H0:Q",
                title="H0",
                format=".5f",
            ),
            alt.Tooltip(
                f"{definition.column}:Q",
                title=definition.y_title,
                format=f".{definition.decimals}f",
            ),
            alt.Tooltip(
                "target_id:N",
                title="Target",
            ),
            alt.Tooltip(
                "classification:N",
                title="Classification",
            ),
            alt.Tooltip(
                "source_class:N",
                title="Source class",
            ),
        ],
    )

    line = base.mark_line()
    points = base.mark_circle(size=55)

    chart = (
        (line + points)
        .properties(
            title=definition.title,
            height=height,
        )
        .interactive()
    )

    st.altair_chart(
        chart,
        use_container_width=True,
    )


def render_fixed_h0_bao_charts() -> None:
    """Render the migrated Fixed-H0 BAO diagnostic family."""

    st.subheader("Fixed-H0 BAO conditional-coordinate audit")

    try:
        points = load_points_table()
    except (FixedH0BAOAssetError, OSError, ValueError) as exc:
        st.error(f"Fixed-H0 BAO assets could not be loaded: {exc}")
        return

    minimum_index = points["chi2"].idxmin()
    minimum_row = points.loc[minimum_index]

    h0_min = float(points["H0"].min())
    h0_max = float(points["H0"].max())
    recorded_minimum_h0 = float(minimum_row["H0"])

    is_boundary_minimum = recorded_minimum_h0 in {
        h0_min,
        h0_max,
    }

    metric_h0, metric_chi2, metric_points, metric_position = st.columns(4)

    with metric_h0:
        st.metric(
            "Recorded minimum H0",
            f"{recorded_minimum_h0:.5g}",
        )

    with metric_chi2:
        st.metric(
            "Recorded minimum χ²",
            f'{minimum_row["chi2"]:.6f}',
        )

    with metric_points:
        st.metric(
            "Recorded points",
            f"{len(points)}",
        )

    with metric_position:
        st.metric(
            "Minimum position",
            (
                "Boundary"
                if is_boundary_minimum
                else "Interior"
            ),
        )

    if is_boundary_minimum:
        st.info(
            "The recorded minimum lies at the edge of the displayed "
            "H0 range. This panel reports the recorded grid and does "
            "not infer behavior outside that range."
        )

    fit_tab, density_tab, sound_tab = st.tabs(
        (
            "Fit structure",
            "Density response",
            "Sound horizon",
        )
    )

    by_column = {
        definition.column: definition
        for definition in CHARTS
    }

    with fit_tab:
        fit_left, fit_right = st.columns(2)

        with fit_left:
            _render_chart(
                points,
                by_column["chi2"],
            )

        with fit_right:
            _render_chart(
                points,
                by_column[
                    "delta_chi2_from_recorded_minimum"
                ],
            )

    with density_tab:
        density_left, density_right = st.columns(2)

        with density_left:
            _render_chart(
                points,
                by_column["omega_b"],
            )

        with density_right:
            _render_chart(
                points,
                by_column["omega_cdm"],
            )

    with sound_tab:
        _render_chart(
            points,
            by_column["rdrag_Mpc"],
            height=380,
        )

    with st.expander("Point table"):
        display_columns = [
            column
            for column in (
                "target_id",
                "H0",
                "chi2",
                "delta_chi2_from_recorded_minimum",
                "omega_b",
                "omega_cdm",
                "rdrag_Mpc",
                "classification",
                "source_class",
            )
            if column in points.columns
        ]

        st.dataframe(
            points[display_columns],
            use_container_width=True,
            hide_index=True,
        )

    with st.expander("Source identity"):
        st.code(
            "\n".join(
                [
                    "loader=dti_fixed_h0_bao_r1_loader_v1.py",
                    "loader_sha256="
                    "6c59d106e55093ceef8e82e9ae5f48d5c543ffc7a47109e5e638d51cdf4ab1c7",
                    "points=assets/fixed_h0_bao_r1/v1/"
                    "fixed_h0_bao_r1_27_point_record_v1.tsv",
                    "points_sha256="
                    "5b187e6f3890a9e2f01911b10fd36fcd3cf47a655e0a9e5d16af9cb20ebe6289",
                    "point_count=27",
                    "manifest_verification=PASS",
                    "display_axis_zero=False",
                    "scientific_recomputation=NO",
                ]
            ),
            language="text",
        )
