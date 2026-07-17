"""Route-aware execution status for the PERFECT FIT application.

This component describes the current execution contract without starting
a backend, CLASS/AxiCLASS, Cobaya, likelihood, posterior, or MCMC run.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


CURRENT_ROUTE_ID = "LOCKED_BASELINE_DIAGNOSTIC"
CURRENT_ROUTE_LABEL = "Locked baseline diagnostic"


STATUS_CARDS = (
    (
        "Execution mode",
        "LOCKED",
        "No executable route selected",
        "Current route is display-only.",
    ),
    (
        "Backend",
        "OFFLINE",
        "No backend request binding",
        "No verified backend request contract.",
    ),
    (
        "Likelihood",
        "DISABLED",
        "No likelihood execution",
        "No likelihood request was issued.",
    ),
    (
        "Posterior",
        "DISABLED",
        "No posterior or MCMC",
        "No sampler contract is active.",
    ),
)


BACKEND_CONTRACT = pd.DataFrame(
    [
        {
            "Component": "Current route",
            "Status": CURRENT_ROUTE_ID,
            "Reason": "Locked recorded baseline display route",
        },
        {
            "Component": "Backend API",
            "Status": "NOT BOUND",
            "Reason": "No verified request contract is active",
        },
        {
            "Component": "CLASS / AxiCLASS",
            "Status": "NOT EXECUTED",
            "Reason": "No physical solver request was issued",
        },
        {
            "Component": "Cobaya",
            "Status": "NOT EXECUTED",
            "Reason": "No Cobaya configuration was submitted",
        },
        {
            "Component": "Likelihood",
            "Status": "DISABLED",
            "Reason": "Likelihood execution is outside the current route",
        },
        {
            "Component": "Posterior / MCMC",
            "Status": "DISABLED",
            "Reason": "No sampler or posterior contract is active",
        },
    ]
)


EXECUTION_PIPELINE = pd.DataFrame(
    [
        {
            "Step": "01",
            "Stage": "Parameter validation",
            "Purpose": "Validate UI values against a route contract",
            "Current status": "PENDING CONTRACT",
        },
        {
            "Step": "02",
            "Stage": "Backend translation",
            "Purpose": "Translate validated UI values into a backend request",
            "Current status": "NOT BOUND",
        },
        {
            "Step": "03",
            "Stage": "Physical solver",
            "Purpose": "Execute CLASS or AxiCLASS where explicitly supported",
            "Current status": "DISABLED",
        },
        {
            "Step": "04",
            "Stage": "Likelihood evaluation",
            "Purpose": "Evaluate a verified likelihood contract",
            "Current status": "DISABLED",
        },
        {
            "Step": "05",
            "Stage": "Posterior / MCMC",
            "Purpose": "Run sampling only for an approved sampler route",
            "Current status": "DISABLED",
        },
        {
            "Step": "06",
            "Stage": "Result export",
            "Purpose": "Export validated results and provenance records",
            "Current status": "PENDING CONTRACT",
        },
    ]
)


SESSION_STATUS = pd.DataFrame(
    [
        {
            "Item": "Session state",
            "Value": "IDLE",
        },
        {
            "Item": "Reason",
            "Value": "Execution intentionally disabled for the current route",
        },
        {
            "Item": "Backend request",
            "Value": "NOT SENT",
        },
        {
            "Item": "Physical solver",
            "Value": "NOT EXECUTED",
        },
        {
            "Item": "Likelihood",
            "Value": "NOT EXECUTED",
        },
        {
            "Item": "Posterior",
            "Value": "NOT EXECUTED",
        },
        {
            "Item": "MCMC",
            "Value": "NOT EXECUTED",
        },
        {
            "Item": "Result artifact",
            "Value": "NONE",
        },
    ]
)


SAFETY_BOUNDARIES = (
    ("Backend", "Execution disabled"),
    ("Likelihood", "Execution disabled"),
    ("Posterior / MCMC", "Execution disabled"),
    ("Scientific recomputation", "Disabled"),
)


def _render_status_cards() -> None:
    columns = st.columns(len(STATUS_CARDS))

    for column, (
        label,
        value,
        help_text,
        caption,
    ) in zip(
        columns,
        STATUS_CARDS,
    ):
        with column:
            st.metric(
                label,
                value,
                help=help_text,
            )
            st.caption(caption)


def _render_pipeline() -> None:
    st.subheader("Planned execution pipeline")

    st.caption(
        "The pipeline is defined in advance, but no stage is executable "
        "until its backend contract has been verified."
    )

    pipeline_display = EXECUTION_PIPELINE.copy()

    # execution_stage_human_labels_v1
    pipeline_display["Stage"] = (
        pipeline_display["Stage"].replace(
            {
                "Parameter validation": "① Validate parameters",
                "Backend translation": "② Translate request",
                "Physical solver": "③ Physical solver",
                "Likelihood evaluation": "④ Likelihood",
                "Posterior / MCMC": "⑤ Posterior / MCMC",
                "Result export": "⑥ Export results",
            }
        )
    )


    pipeline_display["Status"] = (
        pipeline_display["Current status"]
        .map(
            {
                "PENDING CONTRACT": "🟡 Pending contract",
                "NOT BOUND": "⚪ Not bound",
                "DISABLED": "🔴 Disabled",
                "READY": "🟢 Ready",
                "RUNNING": "🔵 Running",
                "SUCCESS": "🟢 Success",
                "FAILED": "🔴 Failed",
            }
        )
        .fillna(pipeline_display["Current status"])
    )

    pipeline_display = pipeline_display.drop(
        columns=["Current status"]
    )

    st.dataframe(
        pipeline_display,
        width="stretch",
        hide_index=True,
        column_config={
            "Step": st.column_config.TextColumn(
                "Step",
                width="small",
            ),
            "Stage": st.column_config.TextColumn(
                "Stage",
                width="medium",
            ),
            "Purpose": st.column_config.TextColumn(
                "Purpose",
                width="large",
            ),
            "Status": st.column_config.TextColumn(
                "Status",
                width="medium",
            ),
        },
    )


def _render_execution_log() -> None:
    st.subheader("Current session")

    st.dataframe(
        SESSION_STATUS,
        width="stretch",
        hide_index=True,
        column_config={
            "Item": st.column_config.TextColumn(
                "Item",
                width="medium",
            ),
            "Value": st.column_config.TextColumn(
                "Value",
                width="large",
            ),
        },
    )

    with st.expander("Raw execution log"):
        st.code(
            "\n".join(
                [
                    f"route_id={CURRENT_ROUTE_ID}",
                    "session_state=IDLE",
                    "execution_authorized=NO",
                    "backend_request_sent=NO",
                    "class_execution=NO",
                    "axiclass_execution=NO",
                    "cobaya_execution=NO",
                    "likelihood_execution=NO",
                    "posterior_execution=NO",
                    "mcmc_execution=NO",
                    "scientific_recomputation=NO",
                    "result_artifact=NONE",
                ]
            ),
            language="text",
        )


def _render_safety_boundary() -> None:
    st.subheader("Safety boundary")

    columns = st.columns(2)

    for index, (label, value) in enumerate(
        SAFETY_BOUNDARIES
    ):
        with columns[index % 2]:
            st.success(f"✓ **{label}** — {value}")

    st.caption(
        "These statuses report the current session only. They do not "
        "assert scientific validation or future backend capability."
    )


def render_execution_status() -> None:
    st.header("Execution contract")

    _render_status_cards()

    st.divider()

    st.subheader("Backend contract")

    st.dataframe(
        BACKEND_CONTRACT,
        width="stretch",
        hide_index=True,
        column_config={
            "Component": st.column_config.TextColumn(
                "Component",
                width="medium",
            ),
            "Status": st.column_config.TextColumn(
                "Status",
                width="medium",
            ),
            "Reason": st.column_config.TextColumn(
                "Reason",
                width="large",
            ),
        },
    )

    st.divider()

    _render_pipeline()

    st.divider()

    _render_execution_log()

    st.divider()

    _render_safety_boundary()
