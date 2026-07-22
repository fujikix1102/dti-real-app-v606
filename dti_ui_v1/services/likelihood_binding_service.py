from __future__ import annotations

from typing import Any, Mapping

from dti_ui_v1.services.likelihood_adapter import (
    build_likelihood_response,
    response_as_dict,
)
from dti_ui_v1.services.likelihood_asset_loader import (
    build_frozen_point,
    load_frozen_likelihood_json,
)


def load_likelihood_binding_payload(
    asset_path: str,
) -> Mapping[str, Any]:
    """
    Convert frozen likelihood asset into UI-compatible payload.

    No compute.
    No inference.
    No posterior generation.
    """

    raw = load_frozen_likelihood_json(asset_path)

    point = build_frozen_point(raw)

    response = build_likelihood_response(point)

    return response_as_dict(response)
