"""
Validation layer for future solver responses.

No runtime solver execution.
"""

import math
from typing import Mapping, Any


def validate_solver_response(payload: Mapping[str, Any]) -> bool:
    required = [
        "solver_id",
        "solver_version",
        "model_id",
        "chi2",
        "loglike",
    ]

    for key in required:
        if key not in payload:
            return False

    for key in ["chi2", "loglike"]:
        if not isinstance(payload[key], (int, float)):
            return False
        if not math.isfinite(float(payload[key])):
            return False

    return True
