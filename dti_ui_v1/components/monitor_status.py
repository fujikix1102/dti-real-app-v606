"""Session and provenance monitor for the PERFECT FIT application.

This component observes local UI, file, and execution-contract state.
It does not execute a backend, CLASS/AxiCLASS, Cobaya, likelihood,
posterior, MCMC, or scientific recomputation.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st


CURRENT_ROUTE_ID = "LOCKED_BASELINE_DIAGNOSTIC"
CURRENT_ROUTE_LABEL = "Locked baseline diagnostic"

REPO_ROOT = Path(__file__).resolve().parents[2]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _current_session_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Item": "Application state",
                "Value": "READY",
                "Meaning": "Local PERFECT FIT application is available",
            },
            {
                "Item": "Selected route",
                "Value": CURRENT_ROUTE_ID,
                "Meaning": CURRENT_ROUTE_LABEL,
            },
            {
                "Item": "Execution state",
                "Value": "IDLE",
                "Meaning": "No calculation is active",
            },
            {
                "Item": "Backend state",
                "Value": "OFFLINE",
                "Meaning": "No verified backend request contract",
            },
            {
                "Item": "Working-copy binding",
                "Value": "NOT BOUND",
                "Meaning": "Editable UI values are not sent to a backend",
            },
            {
                "Item": "Active request",
                "Value": "NONE",
                "Meaning": "No request identifier exists",
            },
            {
                "Item": "Loaded result",
                "Value": "NONE",
                "Meaning": "No newly executed result is loaded",
            },
        ]
    )


def _backend_request_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Layer": "UI parameter validation",
                "State": "PENDING CONTRACT",
                "Request": "NONE",
                "Reason": "No executable route contract is active",
            },
            {
                "Layer": "Backend translation",
                "State": "NOT BOUND",
                "Request": "NONE",
                "Reason": "UI values have not been translated",
            },
            {
                "Layer": "CLASS / AxiCLASS",
                "State": "NOT EXECUTED",
                "Request": "NONE",
                "Reason": "No physical-solver request was issued",
            },
            {
                "Layer": "Cobaya",
                "State": "NOT EXECUTED",
                "Request": "NONE",
                "Reason": "No Cobaya configuration was submitted",
            },
            {
                "Layer": "Likelihood",
                "State": "NOT EXECUTED",
                "Request": "NONE",
                "Reason": "Likelihood execution is disabled",
            },
            {
                "Layer": "Posterior / MCMC",
                "State": "NOT EXECUTED",
                "Request": "NONE",
                "Reason": "No sampler contract is active",
            },
        ]
    )


def _recent_event_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Sequence": "01",
                "Event": "Application source loaded",
                "Status": "PASS",
                "Effect": "UI available",
            },
            {
                "Sequence": "02",
                "Event": "Locked baseline contract loaded",
                "Status": "PASS",
                "Effect": "Six locked values available",
            },
            {
                "Sequence": "03",
                "Event": "Parameter contract evaluated",
                "Status": "PASS",
                "Effect": "Backend-active input count remains zero",
            },
            {
                "Sequence": "04",
                "Event": "Execution contract evaluated",
                "Status": "LOCKED",
                "Effect": "No calculation authorized",
            },
            {
                "Sequence": "05",
                "Event": "Backend request check",
                "Status": "NONE",
                "Effect": "No request sent",
            },
            {
                "Sequence": "06",
                "Event": "Scientific recomputation check",
                "Status": "NONE",
                "Effect": "No recomputation performed",
            },
        ]
    )


def _evidence_candidates() -> tuple[tuple[str, Path], ...]:
    return (
        (
            "DESI DR2 external confirmation JSON",
            REPO_ROOT
            / "data/evidence/"
            "desi_dr2_bao_external_confirmation_v1.json",
        ),
        (
            "DESI DR2 external confirmation TSV",
            REPO_ROOT
            / "data/evidence/"
            "desi_dr2_bao_external_confirmation_v1.tsv",
        ),
        (
            "DESI DR2 confirmation identity",
            REPO_ROOT
            / "data/evidence/"
            "desi_dr2_bao_external_confirmation_v1.sha256.tsv",
        ),
        (
            "Fixed-H0 BAO manifest",
            REPO_ROOT
            / "assets/fixed_h0_bao_r1/v1/"
            "fixed_h0_bao_r1_asset_manifest_v1.tsv",
        ),
        (
            "Fixed-H0 BAO point record",
            REPO_ROOT
            / "assets/fixed_h0_bao_r1/v1/"
            "fixed_h0_bao_r1_27_point_record_v1.tsv",
        ),
        (
            "Graph migration ledger",
            REPO_ROOT
            / "graph_migration/"
            "GRAPH_MIGRATION_LEDGER.tsv",
        ),
    )


def _evidence_rows() -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for record, path in _evidence_candidates():
        exists = path.is_file()

        rows.append(
            {
                "Record": record,
                "Status": (
                    "AVAILABLE"
                    if exists
                    else "MISSING"
                ),
                "Bytes": (
                    path.stat().st_size
                    if exists
                    else None
                ),
                "SHA256": (
                    _sha256(path)
                    if exists
                    else ""
                ),
                "Relative path": _relative(path),
            }
        )

    return pd.DataFrame(rows)


def _audit_text() -> str:
    rendered_at = datetime.now(
        timezone.utc
    ).isoformat()

    evidence = _evidence_rows()
    available_count = int(
        (evidence["Status"] == "AVAILABLE").sum()
    )
    missing_count = int(
        (evidence["Status"] == "MISSING").sum()
    )

    return "\n".join(
        [
            f"rendered_at_utc={rendered_at}",
            f"route_id={CURRENT_ROUTE_ID}",
            f"route_label={CURRENT_ROUTE_LABEL}",
            "application_state=READY",
            "execution_state=IDLE",
            "backend_state=OFFLINE",
            "working_copy_backend_binding=NO",
            "backend_request_count=0",
            "class_execution=NO",
            "axiclass_execution=NO",
            "cobaya_execution=NO",
            "likelihood_execution=NO",
            "posterior_execution=NO",
            "mcmc_execution=NO",
            "scientific_recomputation=NO",
            "new_result_artifact=NONE",
            f"evidence_available_count={available_count}",
            f"evidence_missing_count={missing_count}",
            "public_update=NO",
        ]
    )


def render_monitor_status() -> None:
    st.header("Session monitor")

    st.caption(
        "Current-session state, backend-request visibility, "
        "recent events, evidence identity, and audit boundaries."
    )

    evidence = _evidence_rows()
    evidence_available = int(
        (evidence["Status"] == "AVAILABLE").sum()
    )
    evidence_missing = int(
        (evidence["Status"] == "MISSING").sum()
    )

    card1, card2, card3, card4 = st.columns(4)

    with card1:
        st.metric(
            "Session",
            "READY",
            help="The local application is available.",
        )

    with card2:
        st.metric(
            "Execution",
            "IDLE",
            help="No calculation is active.",
        )

    with card3:
        st.metric(
            "📨 Backend requests",
            "0",
            help="No backend request has been sent.",
        )

    with card4:
        st.metric(
            "Missing evidence",
            evidence_missing,
            help="Local evidence records not currently found.",
        )

    (
        session_tab,
        requests_tab,
        events_tab,
        evidence_tab,
        audit_tab,
    ) = st.tabs(
        (
            "🟢 Current session",
            "Backend requests",
            "🕒 Recent events",
            "🗂 Evidence records",
            "📜 Audit log",
        )
    )

    with session_tab:
        st.subheader("Current session")

        st.dataframe(
            _current_session_rows(),
            width="stretch",
            hide_index=True,
            column_config={
                "Item": st.column_config.TextColumn(
                    "Item",
                    width="medium",
                ),
                "Value": st.column_config.TextColumn(
                    "Value",
                    width="medium",
                ),
                "Meaning": st.column_config.TextColumn(
                    "Meaning",
                    width="large",
                ),
            },
        )

        st.info(
            "The current route is display-only. Editable working-copy "
            "values are not bound to a scientific backend."
        )

    with requests_tab:
        st.subheader("Backend requests")

        st.info(
            "No backend, solver, likelihood, posterior, or MCMC "
            "request has been created or sent."
        )

        st.dataframe(
            _backend_request_rows(),
            width="stretch",
            hide_index=True,
            column_config={
                "Layer": st.column_config.TextColumn(
                    "Layer",
                    width="medium",
                ),
                "State": st.column_config.TextColumn(
                    "State",
                    width="medium",
                ),
                "Request": st.column_config.TextColumn(
                    "Request",
                    width="small",
                ),
                "Reason": st.column_config.TextColumn(
                    "Reason",
                    width="large",
                ),
            },
        )

    with events_tab:
        st.subheader("Recent events")

        st.caption(
            "These are current-render contract events, not a "
            "persistent scientific execution history."
        )

        st.dataframe(
            _recent_event_rows(),
            width="stretch",
            hide_index=True,
        )

    with evidence_tab:
        st.subheader("Evidence records")

        metric1, metric2, metric3 = st.columns(3)

        with metric1:
            st.metric(
                "Checked records",
                len(evidence),
            )

        with metric2:
            st.metric(
                "Available",
                evidence_available,
            )

        with metric3:
            st.metric(
                "Missing",
                evidence_missing,
            )

        display = evidence.copy()

        display["Bytes"] = display["Bytes"].map(
            lambda value: (
                ""
                if pd.isna(value)
                else f"{int(value):,}"
            )
        )

        display["SHA256"] = display["SHA256"].map(
            lambda value: (
                value
                if not value
                else f"{value[:16]}…{value[-8:]}"
            )
        )

        st.dataframe(
            display,
            width="stretch",
            hide_index=True,
            column_config={
                "Record": st.column_config.TextColumn(
                    "Record",
                    width="large",
                ),
                "Status": st.column_config.TextColumn(
                    "Status",
                    width="small",
                ),
                "Bytes": st.column_config.TextColumn(
                    "Bytes",
                    width="small",
                ),
                "SHA256": st.column_config.TextColumn(
                    "SHA256",
                    width="medium",
                ),
                "Relative path": st.column_config.TextColumn(
                    "Relative path",
                    width="large",
                ),
            },
        )

        with st.expander("Full evidence identities"):
            st.dataframe(
                evidence,
                width="stretch",
                hide_index=True,
            )

    with audit_tab:
        st.subheader("Audit log")

        st.code(
            _audit_text(),
            language="text",
        )

        st.success(
            "No backend execution, likelihood evaluation, "
            "posterior computation, MCMC, or scientific "
            "recomputation occurred in this session."
        )
