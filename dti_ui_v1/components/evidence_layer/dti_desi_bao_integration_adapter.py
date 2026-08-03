"""
DESI DR2 BAO Evidence Layer Integration Adapter

Display-only integration boundary.

No:
- likelihood
- posterior
- MCMC
- optimization
- raw data loading

Purpose:
connect source binding contract to evidence display layer.
"""

from dti_ui_v1.components.evidence_layer.dti_desi_bao_display import (
    display_contract,
)


def build_display_layer(source_record: dict) -> dict:
    return {
        "contract": display_contract(),
        "record": source_record,
    }
