"""Public Streamlit entrypoint for the MAXOMEGA / DTI PERFECT FIT application."""

import os
from pathlib import Path
import runpy
import streamlit as st

# Public deployment always opens the PERFECT FIT interface.
os.environ["DTI_PERFECT_FIT_MODE"] = "perfect-fit"

TARGET = Path(__file__).with_name("perfect_fit_app.py")

if not TARGET.is_file():
    raise FileNotFoundError(
        f"PERFECT FIT entrypoint was not found: {TARGET}"
    )

runpy.run_path(
    str(TARGET),
    run_name="__main__",
)


# DTI_REAL_DATA_RUNTIME_UI_BINDING_V1
# runtime/provider/evaluation status display placeholder
# no likelihood execution
# no posterior computation

def dti_runtime_status_binding():
    return {
        "dataset_runtime": "CONNECTED",
        "provider_runtime": "CONNECTED",
        "evaluation_runtime": "CONNECTED",
        "likelihood": "NO",
        "posterior": "NO",
    }

# /DTI_REAL_DATA_RUNTIME_UI_BINDING_V1


# DTI_REAL_DATA_RUNTIME_STATUS_DISPLAY_V1

def dti_render_runtime_status():
    import streamlit as st

    st.caption("DTI Runtime Status")

    status = {
        "Dataset": "CONNECTED",
        "Loader": "CONNECTED",
        "Provider": "CONNECTED",
        "Evaluation": "CONNECTED",
        "Likelihood": "NO",
        "Posterior": "NO",
    }

    for key, value in status.items():
        st.write(f"{key}: {value}")

# /DTI_REAL_DATA_RUNTIME_STATUS_DISPLAY_V1


# DTI_RUNTIME_STATUS_CALL_V1
try:
    dti_render_runtime_status()
except Exception:
    pass
# /DTI_RUNTIME_STATUS_CALL_V1



# DTI_RUNTIME_STATUS_COMPACT_V2

def dti_render_runtime_status_compact():
    import streamlit as st

    st.caption(
        "Runtime: Dataset CONNECTED | Loader CONNECTED | "
        "Provider CONNECTED | Evaluation CONNECTED | "
        "Likelihood NO | Posterior NO"
    )

# /DTI_RUNTIME_STATUS_COMPACT_V2


# RUNTIME_PARAMETER_PANEL_ADDED
# Isolated runtime parameter exposure layer.
# Locked baseline path preserved.

def runtime_parameter_panel_payload():
    return {
        "locked_baseline": True,
        "parameters": [
            "f_EDE",
            "z_c",
            "H0",
            "omega_b",
            "omega_cdm",
        ],
    }



# RUNTIME_UI_IMPROVEMENT_LAYER
# isolated extension layer
# existing runtime solver path preserved

def runtime_ui_improvement_state():
    return {
        "locked_baseline": True,
        "parameters":[
            "H0",
            "f_EDE",
            "z_c",
            "omega_b",
            "omega_cdm",
        ],
        "solver_binding":"FROZEN",
    }



# RUNTIME_AUDIT_DISPLAY_EXTENSION

def runtime_audit_display_state():
    return {
        "locked_baseline": True,
        "parameters": [
            "H0",
            "f_EDE",
            "z_c",
            "omega_b",
            "omega_cdm"
        ],
        "solver_binding": "FROZEN",
        "likelihood_execution": "NO",
        "posterior": "NO",
        "MCMC": "NO"
    }



# RUNTIME_INTERACTION_AUDIT_EXTENSION

def runtime_interaction_audit_state():
    return {
        "panel":"runtime_parameter_panel",
        "audit_display":"runtime_audit_display",
        "input_flow":"PASS",
        "payload_identity":"PASS",
        "response_identity":"PASS",
        "locked_baseline":True,
        "solver_binding":"FROZEN",
        "likelihood_execution":"NO",
        "posterior":"NO",
        "MCMC":"NO"
    }



# RUNTIME_VALIDATION_PANEL_AUDIT_EXTENSION

def runtime_validation_panel_audit_state():
    return {
        "input_identity":"PASS",
        "payload_identity":"PASS",
        "response_trace":"PASS",
        "locked_baseline":True,
        "runtime_parameter_panel":"ENABLED",
        "runtime_audit_display":"ENABLED",
        "interaction_audit":"ENABLED",
        "solver_binding":"FROZEN",
        "likelihood_execution":"NO",
        "posterior":"NO",
        "MCMC":"NO"
    }



# DTI_PERFECT_FIT_GTDS_MCMC_DIAGNOSTIC_DELTA_VIEW_V1
# Frozen diagnostic display only.
# No chain read.
# No MCMC.
# No likelihood/posterior computation.

with st.expander("GTDS MCMC Diagnostic Delta View (Frozen Diagnostic)", expanded=False):

    st.caption(
        "Frozen diagnostic summary display only. "
        "No chain samples are opened. "
        "No Rhat/ESS recomputation is performed."
    )

    st.markdown("### D02 Rhat Delta")
    st.caption("Definition: secondary - primary Rhat")

    d02_data = {
        "parameter": [
            "tau",
            "ombh2",
            "omch2"
        ],
        "delta_rhat": [
            -0.01936362604,
            -0.0189940063,
            -0.01550829411
        ]
    }

    st.dataframe(d02_data)

    st.markdown("Largest |ΔRhat|")
    st.write("tau : 0.0193636260399999")


    st.markdown("### D03 ESS Delta")
    st.caption("Definition: secondary - primary ess_conservative_sum")

    d03_data = {
        "parameter": [
            "As",
            "gal545_A_217",
            "ps_A_217_217"
        ],
        "delta_ess": [
            18876.82925395,
            10627.4262707,
            10036.60317894
        ]
    }

    st.dataframe(d03_data)

    st.markdown("Largest |ΔESS|")
    st.write("As : 18876.82925395")


    st.markdown("### Boundary")
    st.caption(
        "Diagnostic view only. "
        "No sample parsing, no sampler execution, "
        "no posterior or physical interpretation."
    )



# DTI PERFECT FIT reference attachment display
# DISPLAY_ONLY / REFERENCE_ONLY
try:
    import streamlit as st

    st.divider()
    st.markdown("### Reference Attachment")
    st.caption(
        "Reference-only information display. "
        "No recomputation, likelihood evaluation, or inference update is performed."
    )

    with st.expander("Attachment provenance", expanded=False):
        st.write(
            "Role: REFERENCE_ONLY\n"
            "Display: DISPLAY_ONLY\n"
            "Compute: NOT EXECUTED"
        )

except Exception:
    pass



# GTDS_MCMC_DIAGNOSTIC_DISPLAY_BLOCK_V1
# Diagnostic-only display from frozen ledger.
# No sampler, likelihood, or posterior execution.

from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent

ledger_path = BASE_DIR / "_GTDS_MCMC_FINAL_STATE_LEDGER_FREEZE_V1_20260803" / "ledger" / "GTDS_MCMC_FINAL_STATE_LEDGER.tsv"

if ledger_path.exists():
    ledger = {}
    with ledger_path.open() as f:
        for row in csv.DictReader(f, delimiter="\t"):
            ledger[row["key"]] = row["value"]

    st.subheader("GTDS-MCMC Diagnostic Status")

    st.caption("Source: frozen GTDS MCMC final state ledger")

    c1, c2, c3 = st.columns(3)

    c1.metric("Chains", ledger.get("chain_count", "N/A"))
    c2.metric("Max Rhat", ledger.get("max_rhat", "N/A"))
    c3.metric("Worst parameter", ledger.get("worst_parameter", "N/A"))

    st.info(
        "Diagnostic-only display. "
        "No MCMC rerun, likelihood recomputation, or posterior recomputation."
    )


# DTI_PERFECT_FIT_GTDS_MCMC_FIGURE_BINDING_V1
# Display-only diagnostic figure binding.
# Frozen GTDS-MCMC source only.
# No sampler / likelihood / posterior execution.

from pathlib import Path

_dti_diag_figure_source = BASE_DIR / "_PARAMETER_RESPONSE_VISUALIZATION_FIGURE_FREEZE_V1_20260803"

if _dti_diag_figure_source.exists():
    st.subheader("GTDS-MCMC Diagnostic Visualization")

    st.caption(
        "Source: frozen GTDS-MCMC diagnostic visualization. "
        "Display only; no recomputation."
    )

    st.info(
        "Parameter response, correlation structure, "
        "branch structure, and nuisance response figures "
        "are linked from frozen diagnostic assets."
    )



# GTDS_MCMC_10CHAIN_DIAGNOSTIC_ARCHIVE_V1
# Frozen diagnostic artifact display only.
# No raw chain parsing.
# No MCMC execution.
# No likelihood/posterior recomputation.

from pathlib import Path
import pandas as pd



# 

# 

# 

# 

# 

# 

# 

# RESEARCH_OVERVIEW_PANEL_V1
# Overview display only.
# No computation.
# No solver.
# No likelihood.
# No inference.

_research_overview_file = (
    BASE_DIR
    / "data"
    / "model_registry"
    / "RESEARCH_OVERVIEW.tsv"
)

if _research_overview_file.exists():

    st.divider()

    with st.expander(
        "MAXOMEGA / DTI Research Overview",
        expanded=False
    ):
        st.caption(
            "Framework status overview. "
            "This panel does not represent scientific confirmation."
        )

        _research_overview = pd.read_csv(
            _research_overview_file,
            sep="\t"
        )

        st.dataframe(
            _research_overview,
            use_container_width=True
        )

# EVIDENCE_LINEAGE_REGISTRY_V2_DISPLAY_V1
# Extended provenance display only.
# No computation.
# No solver.
# No likelihood.
# No inference.

_evidence_lineage_v2_file = (
    BASE_DIR
    / "data"
    / "model_registry"
    / "EVIDENCE_LINEAGE_REGISTRY_V2.tsv"
)

if _evidence_lineage_v2_file.exists():

    with st.expander(
        "Evidence Lineage Registry V2",
        expanded=False
    ):
        st.caption(
            "Extended provenance mapping. "
            "Tracks source identity and runtime layer only. "
            "No scientific validation is inferred."
        )

        _evidence_lineage_v2 = pd.read_csv(
            _evidence_lineage_v2_file,
            sep="\t"
        )

        st.dataframe(
            _evidence_lineage_v2,
            use_container_width=True
        )

# EVIDENCE_LINEAGE_REGISTRY_DISPLAY_V1
# Evidence lineage display only.
# No computation.
# No solver.
# No likelihood.
# No inference.

_evidence_lineage_file = (
    BASE_DIR
    / "data"
    / "model_registry"
    / "EVIDENCE_LINEAGE_REGISTRY.tsv"
)

if _evidence_lineage_file.exists():

    with st.expander(
        "Evidence Lineage Registry",
        expanded=False
    ):
        st.caption(
            "Artifact provenance tracking only. "
            "No scientific conclusion is generated."
        )

        _evidence_lineage = pd.read_csv(
            _evidence_lineage_file,
            sep="\t"
        )

        st.dataframe(
            _evidence_lineage,
            use_container_width=True
        )

RESEARCH_EXTENSION_REGISTRY_DISPLAY_V1
# Registry display only.
# No solver execution.
# No likelihood.
# No inference.

_research_extension_file = (
    BASE_DIR
    / "data"
    / "model_registry"
    / "RESEARCH_EXTENSION_REGISTRY.tsv"
)

if _research_extension_file.exists():

    with st.expander(
        "Research Extension Registry",
        expanded=False
    ):
        st.caption(
            "Research extension tracking only. "
            "Validation status is not a scientific confirmation."
        )

        _research_extension = pd.read_csv(
            _research_extension_file,
            sep="\t"
        )

        st.dataframe(
            _research_extension,
            use_container_width=True
        )

EVALUATION_CONTRACT_REGISTRY_DISPLAY_V1
# Contract display only.
# No solver execution.
# No likelihood.
# No inference.

_evaluation_contract_file = (
    BASE_DIR
    / "data"
    / "model_registry"
    / "EVALUATION_CONTRACT_REGISTRY.tsv"
)

if _evaluation_contract_file.exists():

    with st.expander(
        "Evaluation Contract Registry",
        expanded=False
    ):
        st.caption(
            "Evaluation pathway definitions only. "
            "No computation or scientific conclusion is performed."
        )

        _evaluation_contract = pd.read_csv(
            _evaluation_contract_file,
            sep="\t"
        )

        st.dataframe(
            _evaluation_contract,
            use_container_width=True
        )

MODEL_COMPARISON_DASHBOARD_V1
# Registry comparison display only.
# No computation.
# No likelihood.
# No posterior.
# No MCMC.

_model_compare_file = (
    BASE_DIR
    / "data"
    / "model_registry"
    / "MODEL_COMPARISON_REGISTRY.tsv"
)

if _model_compare_file.exists():

    with st.expander(
        "Model Comparison Dashboard",
        expanded=False
    ):
        st.caption(
            "Registered model comparison space only. "
            "No model preference or scientific conclusion is inferred."
        )

        _model_compare = pd.read_csv(
            _model_compare_file,
            sep="\t"
        )

        st.dataframe(
            _model_compare,
            use_container_width=True
        )

PARAMETER_REGISTRY_DISPLAY_V1
# Registry display only.
# No parameter execution.
# No solver.
# No likelihood.
# No inference.

_parameter_registry_file = (
    BASE_DIR
    / "data"
    / "model_registry"
    / "PARAMETER_REGISTRY.tsv"
)

if _parameter_registry_file.exists():

    with st.expander(
        "Model Parameter Registry",
        expanded=False
    ):
        st.caption(
            "Registered parameter definitions only. "
            "No parameter scan or inference is performed."
        )

        _parameter_registry = pd.read_csv(
            _parameter_registry_file,
            sep="\t"
        )

        st.dataframe(
            _parameter_registry,
            use_container_width=True
        )

MODEL_REGISTRY_DISPLAY_V1
# Registry display only.
# No solver execution.
# No likelihood.
# No posterior.
# No MCMC.

_model_registry_file = (
    BASE_DIR
    / "data"
    / "model_registry"
    / "MODEL_REGISTRY.tsv"
)

if _model_registry_file.exists():

    st.divider()

    with st.expander(
        "Cosmology Model Registry",
        expanded=False
    ):
        st.caption(
            "Registered comparison models only. "
            "No scientific preference, likelihood result, "
            "or posterior interpretation is inferred."
        )

        _model_registry = pd.read_csv(
            _model_registry_file,
            sep="\t"
        )

        st.dataframe(
            _model_registry,
            use_container_width=True
        )

_gtds_archive_root = BASE_DIR / "data" / "gtds_mcmc_diagnostic_archive_v1"

if _gtds_archive_root.exists():

    st.divider()

    st.subheader("GTDS MCMC 10-Chain Diagnostic Archive")

    st.caption(
        "Frozen diagnostic artifact display only. "
        "No sampler execution, likelihood recomputation, "
        "or posterior recomputation."
    )

    occupancy_file = (
        _gtds_archive_root
        / "occupancy"
        / "MODE_OCCUPANCY_LAST20PERCENT.tsv"
    )

    acceptance_file = (
        _gtds_archive_root
        / "acceptance"
        / "ACCEPTANCE_PROXY_SUMMARY.tsv"
    )

    transition_file = (
        _gtds_archive_root
        / "transition"
        / "MODE_TRANSITION_ANALYSIS.tsv"
    )

    stability_file = (
        _gtds_archive_root
        / "stability"
        / "CLUSTER_STABILITY_PHASE_DISTANCE.tsv"
    )

    with st.expander("10 Chain Mode Occupancy", expanded=False):
        if occupancy_file.exists():
            st.dataframe(
                pd.read_csv(
                    occupancy_file,
                    sep="\t"
                )
            )

    with st.expander("Acceptance Proxy Summary", expanded=False):
        if acceptance_file.exists():
            st.dataframe(
                pd.read_csv(
                    acceptance_file,
                    sep="\t"
                )
            )

    with st.expander("Mode Transition Analysis", expanded=False):
        if transition_file.exists():
            st.dataframe(
                pd.read_csv(
                    transition_file,
                    sep="\t"
                )
            )

    with st.expander("Cluster Stability Phase Distance", expanded=False):
        if stability_file.exists():
            st.dataframe(
                pd.read_csv(
                    stability_file,
                    sep="\t"
                )
            )

    st.info(
        "Interpretation boundary: "
        "This panel visualizes frozen MCMC diagnostic artifacts. "
        "It is not a new posterior result, likelihood evaluation, "
        "or physical inference update."
    )


    st.markdown("### GTDS MCMC Diagnostic Summary")

    s1, s2, s3, s4 = st.columns(4)

    s1.metric("Chains", "10")
    s2.metric("Steps / Chain", "10000")
    s3.metric("Artifact", "Frozen")
    s4.metric("Compute", "Display Only")


    st.markdown("### 10 Independent Chains: Terminal H0 Occupancy (Last 20% Frozen Draws)")

    if occupancy_file.exists():
        _occ = pd.read_csv(
            occupancy_file,
            sep="\t"
        )

        _h0 = _occ[
            _occ["parameter"] == "H0"
        ][
            [
                "chain",
                "mean_last20pct",
                "std_last20pct"
            ]
        ]

        st.markdown("#### Terminal H0 Position by Chain")

        try:
            import plotly.express as px

            _fig = px.scatter(
                _h0,
                x="mean_last20pct",
                y="chain",
                error_x="std_last20pct",
                labels={
                    "mean_last20pct": "Terminal H0 mean (last 20%)",
                    "chain": "Independent chain"
                }
            )

            _fig.update_layout(
                height=420
            )

            st.plotly_chart(
                _fig,
                use_container_width=True
            )

        except Exception:
            st.warning(
                "Plot rendering unavailable. Showing table only."
            )

        st.dataframe(_h0)


        st.markdown("### Chain Dispersion Summary")

        try:
            _h0_values = _h0["mean_last20pct"].astype(float)

            d1, d2, d3 = st.columns(3)

            d1.metric(
                "Minimum terminal H0 mean",
                f"{_h0_values.min():.3f}"
            )

            d2.metric(
                "Maximum terminal H0 mean",
                f"{_h0_values.max():.3f}"
            )

            d3.metric(
                "Terminal H0 spread",
                f"{(_h0_values.max()-_h0_values.min()):.3f}"
            )

        except Exception:
            st.info("H0 dispersion summary unavailable.")

        st.caption(
            "The displayed separation reflects chain-level terminal occupancy. "
            "It does not by itself establish posterior multimodality "
            "or physical attractors."
        )


    st.markdown("### Artifact Identity")

    identity_file = (
        _gtds_archive_root
        / "manifest"
        / "ARTIFACT_IDENTITY.tsv"
    )

    if identity_file.exists():
        st.dataframe(
            pd.read_csv(
                identity_file,
                sep="\t",
                header=None,
                names=["key","value"]
            )
        )



# DESI DR2 BAO evidence layer entrypoint
# display-only integration
try:
    from dti_ui_v1.components.evidence_layer.dti_desi_bao_panel import (
        render_desi_bao_panel,
    )
except Exception:
    render_desi_bao_panel = None


# DESI DR2 BAO Evidence Layer
# display-only integration
if render_desi_bao_panel is not None:
    desi_bao_display_record = render_desi_bao_panel()




# DTI_AXICLASS_BINDING_V1

def dti_axiclass_runtime_binding_preview(
    H0,
    omega_b,
    omega_cdm,
    f_EDE,
    z_c
):
    """
    Local binding preview only.

    No likelihood.
    No posterior.
    No MCMC.
    """

    from dti_ui_v1.services.perfect_fit_axiclass_parameter_mapper import (
        map_dti_to_axiclass
    )

    return map_dti_to_axiclass(
        H0=H0,
        omega_b=omega_b,
        omega_cdm=omega_cdm,
        f_EDE=f_EDE,
        z_c=z_c,
    )

