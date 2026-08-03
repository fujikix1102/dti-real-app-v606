"""
DESI DR2 BAO Evidence Panel

Display layer only.

No:
- likelihood
- posterior
- MCMC
- raw loader
"""

from dti_ui_v1.components.evidence_layer.dti_desi_bao_integration_adapter import (
    build_display_layer,
)


def render_desi_bao_panel():

    record = {
        "source": "DESI_DR2_BAO",
        "mode": "DISPLAY_ONLY",
    }

    return build_display_layer(record)
