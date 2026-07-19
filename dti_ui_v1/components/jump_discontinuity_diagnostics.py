"""Mathematically validated toy transition laboratory; not a cosmology solver."""

from __future__ import annotations

import math

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


def _profile(z: np.ndarray, amplitude: float, center: float, width: float) -> np.ndarray:
    return 0.5 * amplitude * (1.0 + np.tanh((z - center) / width))


def _derivative(z: np.ndarray, amplitude: float, center: float, width: float) -> np.ndarray:
    u = (z - center) / width
    return 0.5 * amplitude / width / np.cosh(u) ** 2


def render_jump_discontinuity_diagnostics() -> None:
    st.subheader("Toy transition laboratory")
    st.warning(
        "Auxiliary mathematical diagnostic only. This dimensionless tanh profile "
        "is not CLASS/AxiCLASS EDE, not an observed transition, and not likelihood evidence."
    )
    c1, c2, c3 = st.columns(3)
    amplitude = c1.number_input("Toy amplitude A", 0.001, 5.0, 1.0, 0.01)
    center = c2.number_input("Toy center z_toy", 0.0, 5.0, 0.82805, 0.001)
    width = c3.number_input("Toy width Delta_z_toy", 0.0001, 2.0, 0.03, 0.001)
    z = np.linspace(max(0.0, center - 8 * width), center + 8 * width, 3001)
    analytic = _derivative(z, amplitude, center, width)
    numeric = np.gradient(_profile(z, amplitude, center, width), z)
    frame = pd.DataFrame(
        {"z_toy": z, "Y": _profile(z, amplitude, center, width), "analytic_dY_dz": analytic}
    )
    long = frame.melt("z_toy", var_name="quantity", value_name="value")
    chart = alt.Chart(long).mark_line().encode(
        x=alt.X("z_toy:Q", title="Toy coordinate z_toy"),
        y=alt.Y("value:Q", title="Dimensionless value"),
        color=alt.Color("quantity:N", title="Quantity"),
        tooltip=["quantity:N", alt.Tooltip("z_toy:Q", format=".6f"), alt.Tooltip("value:Q", format=".8g")],
    ).properties(height=360)
    st.altair_chart(chart, use_container_width=True)

    exact_peak = amplitude / (2.0 * width)
    exact_fwhm = 2.0 * math.acosh(math.sqrt(2.0)) * width
    columns = st.columns(3)
    columns[0].metric("Exact maximum slope", f"{exact_peak:.8g}")
    columns[1].metric("Exact derivative FWHM", f"{exact_fwhm:.8g}")
    columns[2].metric("Numeric derivative max error", f"{np.max(np.abs(numeric - analytic)):.3e}")

    convergence = []
    for count in (501, 1001, 3001, 10001):
        grid = np.linspace(max(0.0, center - 8 * width), center + 8 * width, count)
        exact = _derivative(grid, amplitude, center, width)
        approx = np.gradient(_profile(grid, amplitude, center, width), grid)
        convergence.append({"grid_points": count, "max_derivative_error": float(np.max(np.abs(approx - exact)))})
    st.markdown("**Numerical convergence check**")
    st.dataframe(pd.DataFrame(convergence), hide_index=True, use_container_width=True)
    st.caption(
        "Legacy centers 0.78105, 0.82805, and 0.87505 are UI comparison constants only; "
        "they are not inferred values and are unrelated to cosmological z_c near 3500."
    )
