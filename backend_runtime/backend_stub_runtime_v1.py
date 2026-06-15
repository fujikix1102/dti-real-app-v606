from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from contract_constants_v1 import BOUNDARY, CACHE_ID, CONTRACT_ID, RUNTIME_ID, STUB_ID, CACHE_PAYLOAD_SHA256

class RuntimeBoundaryError(ValueError):
    pass

@dataclass(frozen=True)
class RuntimeResponse:
    status: str
    payload: Dict[str, Any]
    boundary: Dict[str, str]

def _base_payload() -> Dict[str, Any]:
    return {
        "runtime_id": RUNTIME_ID,
        "stub_id": STUB_ID,
        "contract_id": CONTRACT_ID,
        "cache_id": CACHE_ID,
        "cache_payload_sha256": CACHE_PAYLOAD_SHA256,
        "mode": "diagnostic_only",
    }

def health() -> RuntimeResponse:
    return RuntimeResponse(status="ok", payload=_base_payload(), boundary=dict(BOUNDARY))

def cache_identity() -> RuntimeResponse:
    payload = _base_payload()
    payload["identity_status"] = "locked_static_identity"
    return RuntimeResponse(status="ok", payload=payload, boundary=dict(BOUNDARY))

def cache_boundary() -> RuntimeResponse:
    return RuntimeResponse(status="ok", payload={"boundary": dict(BOUNDARY)}, boundary=dict(BOUNDARY))

def source_identity() -> RuntimeResponse:
    payload = _base_payload()
    payload.update({
        "source_family": "SYNTHETIC_SCHEMA_TEST",
        "source_download": False,
        "raw_desi_ingest": False,
        "scientific_cache": False,
    })
    return RuntimeResponse(status="ok", payload=payload, boundary=dict(BOUNDARY))

def _validate_request(request: Dict[str, Any]) -> None:
    if request.get("cache_id") != CACHE_ID:
        raise RuntimeBoundaryError("CACHE_ID_MISMATCH")
    if request.get("allow_interpolation") is not False:
        raise RuntimeBoundaryError("FORBIDDEN_INTERPOLATION")
    if request.get("allow_extrapolation") is not False:
        raise RuntimeBoundaryError("FORBIDDEN_EXTRAPOLATION")
    if request.get("allow_silent_fallback") is not False:
        raise RuntimeBoundaryError("FORBIDDEN_SILENT_FALLBACK")
    if request.get("claim_mode") != "diagnostic_only":
        raise RuntimeBoundaryError("CLAIM_BOUNDARY_TRIGGER")
    if request.get("query_mode") not in {"identity", "boundary", "source_identity"}:
        raise RuntimeBoundaryError("QUERY_MODE_FORBIDDEN")

def cache_query(request: Dict[str, Any]) -> RuntimeResponse:
    _validate_request(request)
    mode = request["query_mode"]
    if mode == "identity":
        return cache_identity()
    if mode == "boundary":
        return cache_boundary()
    if mode == "source_identity":
        return source_identity()
    raise RuntimeBoundaryError("QUERY_MODE_FORBIDDEN")
