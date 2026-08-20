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
from dti_ui_v1.components.profile_library import (
    apply_profile,
    load_profile_library,
)


def _working_key(field_key: str) -> str:
    return f"perfect_fit_precision_working_{field_key}"


def _reset_working_copy() -> None:
    """Reset widget values before the next render begins."""

    for contract in BASELINE_CONTRACTS.values():
        st.session_state[
            _working_key(contract.key)
        ] = contract.float_value


def _apply_precision_profile(profile: dict) -> None:
    parameters = profile["parameters"]
    for field_key, source_key in (
        ("H0", "H0"),
        ("omega_b", "omega_b"),
        ("omega_cdm", "omega_cdm"),
        ("n_s", "n_s"),
        ("ln10_10_A_s", "ln10_10_As"),
        ("tau_reio", "tau_reio"),
    ):
        st.session_state[_working_key(field_key)] = float(parameters[source_key])
    apply_profile(profile, st.session_state)
    st.session_state["active_precision_preset_label_v1"] = profile["label"]


def render_precision_reference() -> None:
    st.subheader("Precision-controlled baseline")

    st.caption(
        "The locked preset remains immutable. Editable fields below are "
        "a separate working copy and do not alter the source preset."
    )

    profile_options = [
        {
            "id": "locked_baseline",
            "label": PRESET_LABEL,
            "kind": "LOCKED_BASELINE",
            "source": "Source-precision locked baseline contract",
            "note": "Immutable reference baseline; applying copies values into the working fields.",
            "parameters": {
                "H0": BASELINE_CONTRACTS["H0"].float_value,
                "omega_b": BASELINE_CONTRACTS["omega_b"].float_value,
                "omega_cdm": BASELINE_CONTRACTS["omega_cdm"].float_value,
                "n_s": BASELINE_CONTRACTS["n_s"].float_value,
                "ln10_10_As": BASELINE_CONTRACTS["ln10_10_A_s"].float_value,
                "tau_reio": BASELINE_CONTRACTS["tau_reio"].float_value,
                "f_EDE": 0.0,
                "z_c": 3500.0,
            },
        },
        *load_profile_library(),
    ]
    labels = {profile["label"]: profile for profile in profile_options}
    selected_label = st.selectbox(
        "Preset",
        options=list(labels),
        key="perfect_fit_precision_preset",
    )
    selected_profile = labels[selected_label]
    st.caption(
        f"{selected_profile['kind']} · {selected_profile['source']}"
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
            help="Copies the selected preset into the editable working copy and executable form. It does not run compute.",
            key="perfect_fit_precision_apply",
            on_click=_apply_precision_profile,
            args=(selected_profile,),
        )
    active_preset = st.session_state.get("active_precision_preset_label_v1")
    if active_preset:
        st.success(
            f"Loaded preset into working copy: {active_preset}. "
            "Open Execution to confirm and run one deterministic CLASS/AxiCLASS computation."
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
            width="stretch",
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
            width="stretch",
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
