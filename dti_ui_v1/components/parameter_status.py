"""Route-aware parameter status for the PERFECT FIT application.

The current locked-baseline route does not accept arbitrary scientific
parameter values. Editable working-copy widgets are therefore reported
separately from backend-bound inputs.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pandas as pd
import streamlit as st

from dti_ui_v1.components.value_formatting import (
    format_contract_value,
    format_source_precision,
)
from dti_ui_v1.contracts.numeric_precision import (
    BASELINE_CONTRACTS,
    OBJECTIVE_CONTRACTS,
    PRESET_LABEL,
)


CURRENT_ROUTE_ID = "LOCKED_BASELINE_DIAGNOSTIC"
CURRENT_ROUTE_LABEL = "Locked baseline diagnostic"

WORKING_KEY_PREFIX = "perfect_fit_precision_working_"


def _working_key(field_key: str) -> str:
    return f"{WORKING_KEY_PREFIX}{field_key}"


def _working_value(field_key: str) -> Any:
    contract = BASELINE_CONTRACTS[field_key]

    return st.session_state.get(
        _working_key(field_key),
        contract.float_value,
    )


def _decimal_delta(
    working_value: Any,
    source_text: str,
) -> Decimal:
    return (
        Decimal(str(working_value))
        - Decimal(source_text)
    )


def _parameter_rows() -> pd.DataFrame:
    rows: list[dict[str, str]] = []

    for contract in BASELINE_CONTRACTS.values():
        working = _working_value(contract.key)
        delta = _decimal_delta(
            working,
            contract.source_text,
        )

        changed = delta != 0

        rows.append(
            {
                "Parameter": contract.symbol,
                "Key": contract.key,
                "Locked value": contract.source_text,
                "Working value": format_source_precision(
                    working
                ),
                "Difference": format_source_precision(
                    delta
                ),
                "Backend role": "FIXED_LOCKED_INPUT",
                "Working-copy state": (
                    "MODIFIED_UI_ONLY"
                    if changed
                    else "MATCHES_LOCKED"
                ),
                "Backend binding": "NOT_BOUND",
                "Execution effect": "NONE",
                "Unit": contract.unit,
            }
        )

    return pd.DataFrame(rows)


def _output_rows() -> pd.DataFrame:
    rows: list[dict[str, str]] = []

    for contract in OBJECTIVE_CONTRACTS.values():
        rows.append(
            {
                "Output": contract.label,
                "Symbol": contract.symbol,
                "Recorded value": format_contract_value(
                    contract.key,
                    source_precision=True,
                ),
                "Role": "DISPLAY_ONLY_OUTPUT",
                "Editable": "NO",
                "Backend input": "NO",
            }
        )

    return pd.DataFrame(rows)


def _route_matrix() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Capability": "Read locked baseline values",
                "Current route": "SUPPORTED",
                "UI available": "YES",
                "Backend bound": "YES — LOCKED",
            },
            {
                "Capability": "Edit working-copy values",
                "Current route": "UI ONLY",
                "UI available": "YES",
                "Backend bound": "NO",
            },
            {
                "Capability": "Execute arbitrary six-parameter input",
                "Current route": "UNSUPPORTED",
                "UI available": "NO",
                "Backend bound": "NO",
            },
            {
                "Capability": "Return recorded objective values",
                "Current route": "DISPLAY ONLY",
                "UI available": "YES",
                "Backend bound": "NO NEW EXECUTION",
            },
            {
                "Capability": "Likelihood evaluation",
                "Current route": "DISABLED",
                "UI available": "NO",
                "Backend bound": "NO",
            },
            {
                "Capability": "Posterior / MCMC",
                "Current route": "DISABLED",
                "UI available": "NO",
                "Backend bound": "NO",
            },
        ]
    )


def render_parameter_status_panel() -> None:
    st.subheader("Parameter contract")

    st.caption(
        "Parameter status is route-dependent. The current route uses the "
        "locked baseline. Working-copy edits are visible for preparation "
        "and comparison but are not sent to the backend."
    )

    parameter_frame = _parameter_rows()
    modified_count = int(
        (
            parameter_frame["Working-copy state"]
            == "MODIFIED_UI_ONLY"
        ).sum()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Backend-active inputs", "0")

    with col2:
        st.metric("Fixed / locked inputs", len(parameter_frame))

    with col3:
        st.metric("Modified working values", modified_count)

    with col4:
        st.metric("Display-only outputs", len(OBJECTIVE_CONTRACTS))

    if modified_count:
        st.warning(
            f"{modified_count} working-copy value(s) differ from the "
            "locked preset. These differences currently have no effect "
            "on execution."
        )
    else:
        st.info(
            "The working copy currently matches the locked preset."
        )

    (
        active_tab,
        fixed_tab,
        compatibility_tab,
        raw_tab,
    ) = st.tabs(
        (
            "Active",
            "Fixed / locked",
            "Route compatibility",
            "Raw contract",
        )
    )

    with active_tab:
        st.subheader("Backend-active parameters")

        st.info(
            "There are no freely varying backend inputs for the current "
            "locked-baseline route."
        )

        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Route": CURRENT_ROUTE_LABEL,
                        "Active parameter count": 0,
                        "Reason": (
                            "The current backend contract accepts the "
                            "locked baseline only."
                        ),
                    }
                ]
            ),
            width="stretch",
            hide_index=True,
        )

    with fixed_tab:
        st.subheader("Fixed and locked parameters")

        primary_columns = [
            "Parameter",
            "Locked value",
            "Working value",
            "Difference",
            "Working-copy state",
        ]

        technical_columns = [
            "Key",
            "Backend role",
            "Backend binding",
            "Execution effect",
            "Unit",
        ]

        primary_frame = parameter_frame[
            primary_columns
        ].rename(
            columns={
                "Locked value": "Locked",
                "Working value": "Working",
                "Working-copy state": "State",
            }
        )

        primary_frame["State"] = primary_frame["State"].replace(
            {
                "MATCHES_LOCKED": "Locked",
                "MODIFIED_UI_ONLY": "Modified — UI only",
            }
        )

        technical_frame = parameter_frame[
            technical_columns
        ].copy()

        st.markdown("### Parameter values")

        st.dataframe(
            primary_frame,
            width="stretch",
            hide_index=True,
            column_config={
                "Parameter": st.column_config.TextColumn(
                    "Parameter",
                    width="small",
                ),
                "Locked": st.column_config.TextColumn(
                    "Locked",
                    width="medium",
                ),
                "Working": st.column_config.TextColumn(
                    "Working",
                    width="medium",
                ),
                "Difference": st.column_config.TextColumn(
                    "Difference",
                    width="medium",
                ),
                "State": st.column_config.TextColumn(
                    "State",
                    width="medium",
                ),
            },
        )

        st.markdown("### Technical backend contract")

        # technical_display_human_labels_v1
        technical_frame = technical_frame.copy()

        if "Backend role" in technical_frame.columns:
            technical_frame["Backend role"] = (
                technical_frame["Backend role"].replace(
                    {
                        "FIXED_LOCKED_INPUT": "Locked input",
                        "ACTIVE_BACKEND_INPUT": "Active input",
                        "DISPLAY_ONLY_OUTPUT": "Display-only output",
                    }
                )
            )

        if "Backend binding" in technical_frame.columns:
            technical_frame["Backend binding"] = (
                technical_frame["Backend binding"].replace(
                    {
                        "NOT_BOUND": "Not bound",
                        "BOUND": "Bound",
                        "LOCKED": "Locked",
                    }
                )
            )

        if "Execution effect" in technical_frame.columns:
            technical_frame["Execution effect"] = (
                technical_frame["Execution effect"].replace(
                    {
                        "NONE": "None",
                        "UI_ONLY": "UI only",
                        "BACKEND_INPUT": "Backend input",
                    }
                )
            )

        st.dataframe(
            technical_frame,
            width="stretch",
            hide_index=True,
            column_config={
                "Key": st.column_config.TextColumn(
                    "Key",
                    width="medium",
                ),
                "Backend role": st.column_config.TextColumn(
                    "Role",
                    width="medium",
                ),
                "Backend binding": st.column_config.TextColumn(
                    "Binding",
                    width="medium",
                ),
                "Execution effect": st.column_config.TextColumn(
                    "Effect",
                    width="small",
                ),
                "Unit": st.column_config.TextColumn(
                    "Unit",
                    width="medium",
                ),
            },
        )

        st.markdown("### Recorded outputs")

        output_frame = _output_rows()

        output_display = output_frame[
            [
                "Output",
                "Symbol",
                "Recorded value",
            ]
        ]

        st.dataframe(
            output_display,
            width="stretch",
            hide_index=True,
            column_config={
                "Output": st.column_config.TextColumn(
                    "Output",
                    width="medium",
                ),
                "Symbol": st.column_config.TextColumn(
                    "Symbol",
                    width="small",
                ),
                "Recorded value": st.column_config.TextColumn(
                    "Recorded value",
                    width="large",
                ),
            },
        )

        with st.expander("Output contract"):
            st.dataframe(
                output_frame,
                width="stretch",
                hide_index=True,
            )

    with compatibility_tab:
        st.subheader("Selected-route compatibility")

        st.dataframe(
            _route_matrix(),
            width="stretch",
            hide_index=True,
        )

        st.caption(
            "Controls may be enabled only after a verified backend "
            "request contract explicitly accepts and validates them."
        )

    with raw_tab:
        st.subheader("Advanced raw contract")

        st.caption(
            "Internal identifiers and exact route-contract values. "
            "This section is intended for audit and developer review."
        )

        lines = [
            f"route_id={CURRENT_ROUTE_ID}",
            f"route_label={CURRENT_ROUTE_LABEL}",
            f"preset={PRESET_LABEL}",
            "active_backend_input_count=0",
            f"fixed_locked_input_count={len(BASELINE_CONTRACTS)}",
            f"display_only_output_count={len(OBJECTIVE_CONTRACTS)}",
            "working_copy_backend_binding=NO",
            "arbitrary_parameter_execution=NO",
            "likelihood_execution=NO",
            "posterior_execution=NO",
            "",
        ]

        for contract in BASELINE_CONTRACTS.values():
            lines.extend(
                [
                    f"{contract.key}.symbol={contract.symbol}",
                    f"{contract.key}.locked={contract.source_text}",
                    (
                        f"{contract.key}.working="
                        f"{format_source_precision(_working_value(contract.key))}"
                    ),
                    f"{contract.key}.role=FIXED_LOCKED_INPUT",
                    f"{contract.key}.backend_binding=NOT_BOUND",
                ]
            )

        lines.append("")

        for contract in OBJECTIVE_CONTRACTS.values():
            lines.extend(
                [
                    f"{contract.key}.value={contract.source_text}",
                    f"{contract.key}.role=DISPLAY_ONLY_OUTPUT",
                ]
            )

        st.code(
            "\n".join(lines),
            language="text",
        )
