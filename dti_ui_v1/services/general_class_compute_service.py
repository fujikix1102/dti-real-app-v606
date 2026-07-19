from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
import os
from typing import Any, Callable, Mapping

import requests


PUBLIC_CLASS_ENDPOINT = "https://dti-class-api.onrender.com/class/compute"
LOCAL_CLASS_ENDPOINT = "http://127.0.0.1:8000/class/compute"
CLASS_ENDPOINT_ENV = "DTI_CLASS_ENDPOINT"


def resolve_class_endpoint() -> str:
    endpoint = os.environ.get(CLASS_ENDPOINT_ENV, "").strip()
    if endpoint:
        return endpoint

    try:
        import streamlit as st

        secret_endpoint = str(st.secrets.get(CLASS_ENDPOINT_ENV, "")).strip()
    except Exception:
        secret_endpoint = ""

    return secret_endpoint or PUBLIC_CLASS_ENDPOINT


DEFAULT_CLASS_ENDPOINT = resolve_class_endpoint()


@dataclass(frozen=True)
class GeneralClassRequest:
    H0: float
    omega_b: float
    omega_cdm: float
    n_s: float
    ln10_10_As: float
    tau_reio: float
    f_EDE: float = 0.0
    z_c: float = 3500.0
    evaluate_desi_bao: bool = True
    evaluate_planck_2018: bool = True
    evaluate_pantheon_plus: bool = True
    timeout_seconds: float = 300.0


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
) -> dict[str, Any]:
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

        "f_EDE": _validated_float(
            "f_EDE",
            request.f_EDE,
            nonnegative=True,
        ),
        "z_c": _validated_float(
            "z_c",
            request.z_c,
            strictly_positive=True,
        ),
        "evaluate_desi_bao": bool(request.evaluate_desi_bao),
        "evaluate_planck_2018": bool(request.evaluate_planck_2018),
        "evaluate_pantheon_plus": bool(request.evaluate_pantheon_plus),
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
        and body.get("status") == "ok"
    )

    return GeneralClassResult(
        status=(
            "accepted"
            if accepted
            else (
                f"backend_{body.get('status')}"
                if 200 <= int(response.status_code) < 300
                else f"http_{response.status_code}"
            )
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
