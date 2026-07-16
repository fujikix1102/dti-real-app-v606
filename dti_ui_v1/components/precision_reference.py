"""Locked baseline and objective-value reference panel."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dti_ui_v1.components.value_formatting import (
    format_contract_value,
    number_input_kwargs,
)
from dti_ui_v1.contracts.numeric_precision import (
    BASELINE_CONTRACTS,
    OBJECTIVE_CONTRACTS,
    PRESET_LABEL,
)


def _working_key(field_key: str) -> str:
    return f"perfect_fit_precision_working_{field_key}"


def _reset_working_copy() -> None:
    """Reset widget values before the next render begins."""

    for contract in BASELINE_CONTRACTS.values():
        st.session_state[
            _working_key(contract.key)
        ] = contract.float_value


def render_precision_reference() -> None:
    st.subheader("Precision-controlled baseline")

    st.caption(
        "The locked preset remains immutable. Editable fields below are "
        "a separate working copy and do not alter the source preset."
    )

    st.selectbox(
        "Preset",
        options=(PRESET_LABEL,),
        disabled=True,
        key="perfect_fit_precision_preset",
    )

    working_values: dict[str, float] = {}

    parameter_rows = (
        ("H0", "omega_b"),
        ("omega_cdm", "n_s"),
        ("ln10_10_A_s", "tau_reio"),
    )

    for left_key, right_key in parameter_rows:
        left_column, right_column = st.columns(2)

        for column, field_key in (
            (left_column, left_key),
            (right_column, right_key),
        ):
            contract = BASELINE_CONTRACTS[field_key]

            with column:
                working_values[field_key] = st.number_input(
                    f"{contract.symbol} — {contract.label}",
                    key=_working_key(field_key),
                    help=(
                        f"Locked source: {contract.source_text}"
                        + (
                            f" {contract.unit}"
                            if contract.unit
                            else ""
                        )
                    ),
                    **number_input_kwargs(field_key),
                )

    left, right = st.columns(2)

    with left:
        st.button(
            "Reset working copy",
            key="perfect_fit_precision_reset",
            on_click=_reset_working_copy,
        )

    with right:
        st.button(
            "Use working configuration",
            type="primary",
            disabled=True,
            help=(
                "Enabled only after the verified backend request contract "
                "accepts these parameters."
            ),
            key="perfect_fit_precision_apply",
        )

    # precision_two_column_summary_v1
    st.markdown("### Baseline and recorded objective")

    baseline_column, objective_column = st.columns(
        (1.35, 1.0),
        gap="large",
    )

    with baseline_column:
        st.markdown("#### Locked baseline")

        baseline_rows = []

        for key, contract in BASELINE_CONTRACTS.items():
            baseline_rows.append(
                {
                    "Parameter": contract.symbol,
                    "Locked value": format_contract_value(
                        key,
                        source_precision=True,
                    ),
                }
            )

        st.dataframe(
            baseline_rows,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Parameter": st.column_config.TextColumn(
                    "Parameter",
                    width="medium",
                ),
                "Locked value": st.column_config.TextColumn(
                    "Locked value",
                    width="medium",
                ),
            },
        )

    with objective_column:
        st.markdown("#### Recorded objective")

        for contract in OBJECTIVE_CONTRACTS.values():
            st.metric(
                contract.label,
                format_contract_value(
                    contract.key,
                    source_precision=True,
                ),
            )

    st.caption(
        "Full source-precision values. Display formatting does "
        "not change stored values or backend inputs."
    )

    with st.expander("Full source-precision values"):
        rows = []

        for contract in (
            *BASELINE_CONTRACTS.values(),
            *OBJECTIVE_CONTRACTS.values(),
        ):
            rows.append(
                {
                    "key": contract.key,
                    "symbol": contract.symbol,
                    "source_value": contract.source_text,
                    "normal_display": format_contract_value(
                        contract.key
                    ),
                    "input_step": contract.input_step_text,
                    "unit": contract.unit,
                }
            )

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )

        st.code(
            "\n".join(
                f"{contract.key}={contract.source_text}"
                for contract in (
                    *BASELINE_CONTRACTS.values(),
                    *OBJECTIVE_CONTRACTS.values(),
                )
            ),
            language="text",
        )
