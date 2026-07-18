from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any, Callable, Mapping

import requests


DEFAULT_CLASS_ENDPOINT = (
    "https://dti-class-api.onrender.com/class/compute"
)


@dataclass(frozen=True)
class GeneralClassRequest:
    H0: float
    omega_b: float
    omega_cdm: float
    n_s: float
    ln10_10_As: float
    tau_reio: float
    timeout_seconds: float = 180.0


@dataclass(frozen=True)
class GeneralClassResult:
    status: str
    accepted: bool
    endpoint: str
    submitted_payload: Mapping[str, float]
    response_payload: Mapping[str, Any]
    detail: str


def _validated_float(
    name: str,
    value: float,
    *,
    strictly_positive: bool = False,
    nonnegative: bool = False,
) -> float:
    result = float(value)

    if not isfinite(result):
        raise ValueError(f"{name} must be finite")

    if strictly_positive and result <= 0.0:
        raise ValueError(f"{name} must be greater than zero")

    if nonnegative and result < 0.0:
        raise ValueError(f"{name} must be nonnegative")

    return result


def build_general_class_payload(
    request: GeneralClassRequest,
) -> dict[str, float]:
    payload = {
        "H0": _validated_float(
            "H0",
            request.H0,
            strictly_positive=True,
        ),
        "omega_b": _validated_float(
            "omega_b",
            request.omega_b,
            strictly_positive=True,
        ),
        "omega_cdm": _validated_float(
            "omega_cdm",
            request.omega_cdm,
            strictly_positive=True,
        ),
        "n_s": _validated_float(
            "n_s",
            request.n_s,
            strictly_positive=True,
        ),
        "ln10_10_As": _validated_float(
            "ln10_10_As",
            request.ln10_10_As,
        ),
        "tau_reio": _validated_float(
            "tau_reio",
            request.tau_reio,
            nonnegative=True,
        ),

        # The backend currently accepts these fields for interface
        # compatibility but does not apply EDE microphysics.
        "f_EDE": 0.0,
        "z_c": 3500.0,
    }

    return payload


def execute_general_class_compute(
    request: GeneralClassRequest,
    *,
    endpoint: str = DEFAULT_CLASS_ENDPOINT,
    post: Callable[..., Any] = requests.post,
) -> GeneralClassResult:
    payload = build_general_class_payload(request)

    try:
        response = post(
            endpoint,
            json=payload,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            timeout=float(request.timeout_seconds),
        )
    except requests.Timeout as exc:
        return GeneralClassResult(
            status="timeout",
            accepted=False,
            endpoint=endpoint,
            submitted_payload=payload,
            response_payload={},
            detail=str(exc),
        )
    except requests.RequestException as exc:
        return GeneralClassResult(
            status="request_error",
            accepted=False,
            endpoint=endpoint,
            submitted_payload=payload,
            response_payload={},
            detail=str(exc),
        )

    try:
        body = response.json()
    except Exception:
        body = {
            "raw_text": getattr(response, "text", ""),
        }

    if not isinstance(body, Mapping):
        body = {
            "raw_response": body,
        }

    accepted = (
        200 <= int(response.status_code) < 300
        and body.get("status") != "error"
    )

    return GeneralClassResult(
        status=(
            "accepted"
            if accepted
            else f"http_{response.status_code}"
        ),
        accepted=accepted,
        endpoint=endpoint,
        submitted_payload=payload,
        response_payload=dict(body),
        detail=(
            "General CLASS computation completed."
            if accepted
            else "Backend rejected or failed the request."
        ),
    )
