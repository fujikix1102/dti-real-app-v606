from __future__ import annotations
import os
from typing import Mapping, Any

def build_frozen_likelihood_display_payload(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Payload-only frozen likelihood display formatter.

    Display layer:
    - consumes prepared payload
    - no raw asset access
    - no calculation
    - no inference
    """

    metadata = payload.get("metadata", {})
    derived = payload.get("derived", {})
    desi = payload.get("desi_dr2_bao", {})

    return {
        "case_id": metadata.get("case_id"),
        "provenance": metadata.get("provenance"),
        "rs_drag": derived.get("rs_drag"),
        "chi2": desi.get("chi2"),
        "loglike": desi.get("loglike"),
        "posterior": (
            "WOC_DTI_MUTED"
            if payload.get("posterior") in (None, "NO")
            else payload.get("posterior")
        ),
        "MCMC": "NO",
        "dti_120_grid": payload.get(
            "dti_120_grid",
            {
                "status": "NOT_PROVIDED",
                "row_count": 0,
                "z_i": [],
                "y_i": [],
                "w_i": [],
            },
        ),
    }
