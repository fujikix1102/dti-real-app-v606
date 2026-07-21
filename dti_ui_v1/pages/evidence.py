from __future__ import annotations

import streamlit as st
from dti_ui_v1.components.evidence_layer.evidence_chain_snapshot_dashboard import render_evidence_chain_snapshot_dashboard

from dti_ui_v1.services.evidence_registry.evidence_chain_freeze_reader import load_freeze_record
from dti_ui_v1.components.evidence_layer.evidence_chain_freeze_view_panel import render_freeze_view

from dti_ui_v1.services.evidence_registry.evidence_chain_reproducibility_report import build_reproducibility_report
from dti_ui_v1.components.evidence_layer.evidence_chain_reproducibility_report_panel import render_reproducibility_report

from dti_ui_v1.services.evidence_registry.evidence_chain_integrity_scorecard import build_integrity_scorecard
from dti_ui_v1.components.evidence_layer.evidence_chain_integrity_scorecard_panel import render_integrity_scorecard

from dti_ui_v1.services.evidence_registry.source_identity_registry import build_source_identity_registry
from dti_ui_v1.services.evidence_registry.evidence_chain_validator import validate_evidence_registry
from dti_ui_v1.services.evidence_registry.evidence_chain_failure_report import build_failure_report
from dti_ui_v1.services.evidence_registry.evidence_manifest_reader import load_manifest_summary
from dti_ui_v1.services.evidence_registry.evidence_chain_audit_timeline import build_audit_timeline
from dti_ui_v1.components.evidence_layer.evidence_chain_audit_timeline_panel import render_evidence_chain_audit_timeline
from dti_ui_v1.services.evidence_registry.evidence_export_package_summary import build_export_package_summary
from dti_ui_v1.components.evidence_layer.evidence_export_package_view_panel import render_evidence_export_package_view

from dti_ui_v1.components.evidence_layer.evidence_chain_final_dashboard import render_evidence_chain_final_dashboard
from dti_ui_v1.services.evidence_registry.evidence_manifest_reader import load_manifest_summary
from dti_ui_v1.services.evidence_registry.evidence_chain_validator import validate_evidence_registry
from dti_ui_v1.services.evidence_registry.source_identity_registry import build_source_identity_registry
from dti_ui_v1.services.evidence_registry.evidence_manifest_reader import load_manifest_summary
from dti_ui_v1.components.evidence_layer.evidence_manifest_export_panel import render_evidence_manifest_export
from dti_ui_v1.services.evidence_registry.section8_schema_normalizer import normalize_section8_schema
from dti_ui_v1.components.evidence_layer.normalized_evidence_workbench_panel import render_normalized_evidence_workbench
import pandas as pd
from dti_ui_v1.services.evidence_registry.evidence_chain_failure_report import build_failure_report
from dti_ui_v1.components.evidence_layer.evidence_chain_failure_report_panel import render_evidence_chain_failure_report
from dti_ui_v1.services.evidence_registry.evidence_chain_validator import validate_evidence_registry
from dti_ui_v1.components.evidence_layer.evidence_chain_validation_panel import render_evidence_chain_validation_panel
from dti_ui_v1.components.evidence_layer.evidence_chain_status_matrix import render_evidence_chain_status_matrix
from dti_ui_v1.services.evidence_registry.source_identity_registry import build_source_identity_registry
from dti_ui_v1.components.evidence_layer.source_identity_registry_panel import render_source_identity_registry

from dti_ui_v1.services.run_store import list_run_artifacts


def render() -> None:
    st.title("Evidence")

    with st.expander(
        "Evidence Chain Snapshot Dashboard",
        expanded=False,
    ):
        from dti_ui_v1.services.evidence_registry.evidence_chain_snapshot_reader import (
            load_readiness_snapshot,
        )

        snapshot = load_readiness_snapshot()

        render_evidence_chain_snapshot_dashboard(
            snapshot
        )



    with st.expander(
        "Evidence Chain Freeze Record",
        expanded=False,
    ):
        freeze_record = load_freeze_record()
        render_freeze_view(
            freeze_record
        )



    with st.expander(
        "Evidence Chain Reproducibility Report",
        expanded=False,
    ):
        _report_registry = build_source_identity_registry()
        _report_validation = validate_evidence_registry(
            _report_registry
        )
        _report_failure = build_failure_report(
            _report_validation
        )
        _report_manifest = load_manifest_summary()

        _report_timeline = build_audit_timeline(
            _report_registry,
            _report_validation,
            _report_failure,
            _report_manifest,
        )

        _report_scorecard = build_integrity_scorecard(
            _report_registry,
            _report_validation,
            _report_failure,
            _report_manifest,
            _report_timeline,
        )

        _report = build_reproducibility_report(
            _report_scorecard
        )

        render_reproducibility_report(
            _report
        )



    with st.expander(
        "Evidence Chain Integrity Scorecard",
        expanded=False,
    ):
        _scorecard_registry = build_source_identity_registry()
        _scorecard_validation = validate_evidence_registry(
            _scorecard_registry
        )
        _scorecard_failure = build_failure_report(
            _scorecard_validation
        )
        _scorecard_manifest = load_manifest_summary()

        _scorecard_timeline = build_audit_timeline(
            _scorecard_registry,
            _scorecard_validation,
            _scorecard_failure,
            _scorecard_manifest,
        )

        _scorecard = build_integrity_scorecard(
            _scorecard_registry,
            _scorecard_validation,
            _scorecard_failure,
            _scorecard_manifest,
            _scorecard_timeline,
        )

        render_integrity_scorecard(
            _scorecard
        )



    with st.expander(
        "Evidence Chain Audit Timeline",
        expanded=False,
    ):
        _registry = build_source_identity_registry()
        _validation = validate_evidence_registry(_registry)
        _failure = build_failure_report(_validation)
        _manifest = load_manifest_summary()

        _timeline = build_audit_timeline(
            _registry,
            _validation,
            _failure,
            _manifest,
        )

        render_evidence_chain_audit_timeline(
            _timeline
        )



    with st.expander(
        "Evidence Export Package View",
        expanded=False,
    ):
        package_summary = build_export_package_summary()
        render_evidence_export_package_view(
            package_summary
        )



    with st.expander(
        "Evidence Chain Final Dashboard",
        expanded=False,
    ):

        registry = build_source_identity_registry()

        validation = validate_evidence_registry(
            registry
        )

        manifest_summary = load_manifest_summary()

        render_evidence_chain_final_dashboard(
            registry,
            validation,
            manifest_summary,
            "PASS",
        )



    with st.expander(
        "Evidence Manifest Export",
        expanded=False,
    ):

        manifest_summary = load_manifest_summary()

        render_evidence_manifest_export(
            manifest_summary
        )



    with st.expander(
        "Normalized Evidence Workbench",
        expanded=False,
    ):

        import pandas as pd

        primary = pd.read_csv(
            "data/section8_source_record/section8_primary_comparison_graph_normalized.tsv",
            sep="\t",
            dtype=str,
        )

        secondary = pd.read_csv(
            "data/section8_source_record/section8_secondary_summary_panel_normalized.tsv",
            sep="\t",
            dtype=str,
        )

        primary = normalize_section8_schema(
            primary,
            "primary",
        )

        secondary = normalize_section8_schema(
            secondary,
            "secondary",
        )

        render_normalized_evidence_workbench(
            primary,
            secondary,
        )



    with st.expander(
        "Evidence Chain Failure Report",
        expanded=False,
    ):
        registry = build_source_identity_registry()
        validation = validate_evidence_registry(registry)
        failure_report = build_failure_report(validation)
        render_evidence_chain_failure_report(failure_report)



    with st.expander(
        "Evidence Chain Validation",
        expanded=False,
    ):
        registry = build_source_identity_registry()
        validation = validate_evidence_registry(registry)
        render_evidence_chain_validation_panel(validation)



    with st.expander(
        "Evidence Chain Status Matrix",
        expanded=False,
    ):
        registry = build_source_identity_registry()
        render_evidence_chain_status_matrix(registry)



    with st.expander(
        "Source Identity Registry",
        expanded=False,
    ):
        registry = build_source_identity_registry()
        render_source_identity_registry(registry)


    st.caption("Durable run identities, scientific contracts, and interpretation limits")
    artifacts = list_run_artifacts()
    source_tab, run_tab, boundary_tab = st.tabs(("Source contracts", "Run artifacts", "Boundaries"))
    with source_tab:
        st.dataframe(
            [
                {"Object": "General CLASS / AxiCLASS", "Input": "8 cosmological controls", "Output": "CMB + distances + 3 likelihood families", "Validation": "official data identity + finite outputs"},
                {"Object": "Planck 2018", "Input": "lensed TT/TE/EE", "Output": "Plik-lite + low-T + low-E log L", "Validation": "clipy likelihood self-tests"},
                {"Object": "Pantheon+", "Input": "angular distances", "Output": "marginalized SN chi-square", "Validation": "1701-row source + full covariance"},
                {"Object": "Locked DESI baseline", "Input": "use_locked_baseline=true", "Output": "verified theory vector + DESI likelihood", "Validation": "frozen-vector tolerance"},
                {"Object": "DTI injection/recovery", "Input": "72 transition conditions", "Output": "global 3-sigma recovery rates", "Validation": "10,000 seeded null + 72,000 injected simulations"},
                {"Object": "Catalog-level DTI pilot", "Input": "3 injected H(z) steps × 7 tracers", "Output": "coordinate/reconstruction/correlation/fit/13-value recovery", "Validation": "672 correlation functions + 84 anisotropic BAO fits"},
                {"Object": "Local H0 comparison contract", "Input": "Published SH0ES/CCHP Gaussian summaries", "Output": "Pull and trade-off rail", "Validation": "single-anchor selection + overlap prohibition"},
                {"Object": "Run artifact", "Input": "request + complete response", "Output": "atomic JSON", "Validation": "canonical SHA-256"},
            ], hide_index=True, use_container_width=True,
        )
    with run_tab:
        if artifacts:
            artifact_df = (
                pd.DataFrame(artifacts)
                .fillna("")
                .astype(str)
            )

            st.dataframe(
                artifact_df,
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info("No durable evidence record exists yet.")
    with boundary_tab:
        st.markdown(
            "- General runs propagate LCDM/AxiCLASS EDE and evaluate DESI DR2, Planck 2018, and Pantheon+.\n"
            "- Locked runs evaluate only the frozen baseline contract.\n"
            "- DESI DR2 BAO is a 13-value, seven-effective-redshift Gaussian compression derived from "
            "template-fitted clustering; it is not a raw-catalog transition likelihood.\n"
            "- Audit-DTI smoothness is conditional on that compression and the scanned AxiCLASS family; "
            "it cannot exclude transitions erased or unrepresented upstream.\n"
            "- The injection/recovery result measures a DESI-like transfer surrogate, not the production "
            "catalog, survey systematics, reconstruction, covariance, template fit, or Ly-alpha pipeline.\n"
            "- The catalog-level pilot executes coordinate conversion, FFT reconstruction, Landy-Szalay "
            "correlations, anisotropic BAO fitting, and 13-value compression on deterministic synthetic "
            "survey-shaped catalogs. It is not an official DESI EZmock/Abacus or production result.\n"
            "- Planck calibration A_planck is fixed to 1.0 in this deterministic view.\n"
            "- SH0ES and CCHP values are published summary coordinates only. They overlap supernova information "
            "with Pantheon+ and are never multiplied into the backend joint likelihood.\n"
            "- A reconciliation claim still requires the raw calibrator likelihood/covariance, declared priors, "
            "a converged posterior, and model comparison.\n"
            "- Posterior/MCMC remains outside scope until priors and convergence criteria are declared.\n"
            "- The toy transition laboratory is mathematical UI validation, not an EDE model."
        )
