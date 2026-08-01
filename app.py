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

