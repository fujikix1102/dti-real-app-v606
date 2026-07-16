from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class ApiResponse:
    status_code: int
    body: dict[str, Any]
    elapsed_seconds: float


class DtiApiClient:
    """Shared HTTP client without automatic retry.

    This module is additive and is not yet connected to app.py.
    """

    def __init__(
        self,
        endpoint: str,
        *,
        timeout_seconds: float = 300.0,
    ) -> None:
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds

    def post(
        self,
        payload: dict[str, Any],
    ) -> ApiResponse:
        response = requests.post(
            self.endpoint,
            json=payload,
            timeout=self.timeout_seconds,
        )

        parsed = response.json()

        if not isinstance(parsed, dict):
            parsed = {
                "status": "invalid_json_shape",
                "response": parsed,
            }

        return ApiResponse(
            status_code=response.status_code,
            body=parsed,
            elapsed_seconds=response.elapsed.total_seconds(),
        )
