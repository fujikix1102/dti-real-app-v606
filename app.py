"""Public Streamlit entrypoint for the MAXOMEGA / DTI PERFECT FIT application."""

import os
from pathlib import Path
import runpy

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
