from __future__ import annotations

from typing import Mapping, Any

from dti_ui_v1.components.likelihood_frozen_display import (
    build_frozen_likelihood_display_payload,
)


def build_page_likelihood_section(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Existing page binding helper.

    Display preparation only.
    No compute.
    No inference.
    """

    return build_frozen_likelihood_display_payload(
        payload
    )
