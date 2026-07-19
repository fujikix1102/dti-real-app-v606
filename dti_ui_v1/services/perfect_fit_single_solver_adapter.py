"""Fail-closed adapter for the PERFECT FIT locked-baseline BAO backend.

This module intentionally does not perform HTTP communication by itself.
A transport callable must be explicitly injected.

Current physical boundary
-------------------------
The existing backend exposes CLASS-like locked-baseline propagation, but
the audited source does not forward ``f_EDE`` or ``z_c`` into the solver
parameter dictionary. Therefore this adapter must not represent the
backend as an AxiCLASS EDE execution path.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math
from typing import Any, Callable, Mapping, Optional, Protocol


DEFAULT_ENDPOINT = "https://dti-class-api.onrender.com/axiclass/desi-dr2-bao"
PHYSICAL_BOUNDARY_LABEL = (
    "LOCKED_BASELINE_BAO_BACKEND_NOT_AXICLASS_EDE_MICROPHYSICS"
)
BACKEND_CAPABILITY = "CLASS_LCDM_LIKE_LOCKED_BASELINE"

DEFAULT_TIMEOUT_SECONDS = 30.0
MAX_TIMEOUT_SECONDS = 120.0


class AdapterStatus(str, Enum):
    SUCCESS_LOCKED_BASELINE = "SUCCESS_LOCKED_BASELINE"
    REQUEST_VALIDATION_FAILURE = "REQUEST_VALIDATION_FAILURE"
    HTTP_CONNECTION_FAILURE = "HTTP_CONNECTION_FAILURE"
    HTTP_TIMEOUT = "HTTP_TIMEOUT"
    HTTP_STATUS_FAILURE = "HTTP_STATUS_FAILURE"
    MALFORMED_RESPONSE = "MALFORMED_RESPONSE"
    BACKEND_DECLARED_FAILURE = "BACKEND_DECLARED_FAILURE"
    SCHEMA_VALIDATION_FAILURE = "SCHEMA_VALIDATION_FAILURE"
    UNSUPPORTED_EDE_EXECUTION = "UNSUPPORTED_EDE_EXECUTION"
    BOUNDARY_VIOLATION = "BOUNDARY_VIOLATION"


@dataclass(frozen=True)
class LockedBaselineRequest:
    use_locked_baseline: bool = True
    f_EDE: float = 0.0
    z_c: Optional[float] = None
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS


@dataclass(frozen=True)
class TransportResponse:
    status_code: int
    json_body: Any


@dataclass(frozen=True)
class AdapterResult:
    status: AdapterStatus
    accepted: bool
    validated_payload: Optional[Mapping[str, Any]]
    physical_boundary_label: str
    backend_capability: str
    endpoint: str
    detail: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "accepted": self.accepted,
            "validated_payload": self.validated_payload,
            "physical_boundary_label": self.physical_boundary_label,
            "backend_capability": self.backend_capability,
            "endpoint": self.endpoint,
            "detail": self.detail,
        }


class TransportTimeoutError(TimeoutError):
    """Transport-level timeout converted into a fail-closed result."""


class TransportConnectionError(ConnectionError):
    """Transport-level connection failure converted into a fail-closed result."""


class TransportCallable(Protocol):
    def __call__(
        self,
        endpoint: str,
        payload: Mapping[str, Any],
        timeout_seconds: float,
    ) -> TransportResponse:
        ...


def _failure(
    status: AdapterStatus,
    endpoint: str,
    detail: str,
) -> AdapterResult:
    return AdapterResult(
        status=status,
        accepted=False,
        validated_payload=None,
        physical_boundary_label=PHYSICAL_BOUNDARY_LABEL,
        backend_capability=BACKEND_CAPABILITY,
        endpoint=endpoint,
        detail=detail,
    )


def _is_finite_number(value: Any) -> bool:
    # bool is a subclass of int and must not be accepted as a number.
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def _validate_endpoint(endpoint: Any) -> Optional[str]:
    if not isinstance(endpoint, str):
        return "endpoint_must_be_string"

    if endpoint != DEFAULT_ENDPOINT:
        return "endpoint_fallback_or_override_not_permitted"

    return None


def _validate_request(request: Any) -> tuple[Optional[AdapterStatus], Optional[str]]:
    if not isinstance(request, LockedBaselineRequest):
        return (
            AdapterStatus.REQUEST_VALIDATION_FAILURE,
            "request_must_be_LockedBaselineRequest",
        )

    if type(request.use_locked_baseline) is not bool:
        return (
            AdapterStatus.REQUEST_VALIDATION_FAILURE,
            "use_locked_baseline_must_be_literal_bool",
        )

    if request.use_locked_baseline is not True:
        return (
            AdapterStatus.BOUNDARY_VIOLATION,
            "use_locked_baseline_must_be_true",
        )

    if not _is_finite_number(request.timeout_seconds):
        return (
            AdapterStatus.REQUEST_VALIDATION_FAILURE,
            "timeout_must_be_finite_non_boolean_number",
        )

    timeout = float(request.timeout_seconds)
    if timeout <= 0.0 or timeout > MAX_TIMEOUT_SECONDS:
        return (
            AdapterStatus.REQUEST_VALIDATION_FAILURE,
            "timeout_out_of_allowed_range",
        )

    if not _is_finite_number(request.f_EDE):
        return (
            AdapterStatus.REQUEST_VALIDATION_FAILURE,
            "f_EDE_must_be_finite_non_boolean_number",
        )

    if float(request.f_EDE) != 0.0:
        return (
            AdapterStatus.UNSUPPORTED_EDE_EXECUTION,
            "nonzero_f_EDE_is_not_forwarded_by_current_backend",
        )

    if request.z_c is not None:
        if not _is_finite_number(request.z_c):
            return (
                AdapterStatus.REQUEST_VALIDATION_FAILURE,
                "z_c_must_be_none_or_finite_non_boolean_number",
            )

        return (
            AdapterStatus.UNSUPPORTED_EDE_EXECUTION,
            "z_c_dependent_execution_is_not_supported_by_current_backend",
        )

    return None, None


def build_locked_payload(request: LockedBaselineRequest) -> dict[str, bool]:
    """Construct the only payload currently authorized for this backend."""

    status, detail = _validate_request(request)
    if status is not None:
        raise ValueError(f"{status.value}:{detail}")

    return {"use_locked_baseline": True}


def _contains_non_finite_number(value: Any) -> bool:
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return False

    if isinstance(value, (int, float)):
        return not math.isfinite(float(value))

    if isinstance(value, Mapping):
        return any(_contains_non_finite_number(v) for v in value.values())

    if isinstance(value, (list, tuple)):
        return any(_contains_non_finite_number(v) for v in value)

    return False


def _backend_declared_failure(body: Mapping[str, Any]) -> bool:
    if body.get("success") is False:
        return True

    if body.get("ok") is False:
        return True

    status = body.get("status")
    if isinstance(status, str) and status.strip().lower() in {
        "error",
        "failed",
        "failure",
        "busy",
        "rejected",
    }:
        return True

    return False


def _extract_result_payload(body: Mapping[str, Any]) -> Optional[Mapping[str, Any]]:
    for key in ("result", "data", "observables"):
        candidate = body.get(key)
        if isinstance(candidate, Mapping) and candidate:
            return candidate

    return None


def _response_declares_success(body: Mapping[str, Any]) -> bool:
    if body.get("success") is True:
        return True

    if body.get("ok") is True:
        return True

    status = body.get("status")
    return isinstance(status, str) and status.strip().lower() in {
        "ok",
        "success",
        "completed",
    }


def _validate_response_schema(
    body: Any,
) -> tuple[Optional[AdapterStatus], Optional[str], Optional[Mapping[str, Any]]]:
    if not isinstance(body, Mapping):
        return (
            AdapterStatus.MALFORMED_RESPONSE,
            "response_json_root_must_be_mapping",
            None,
        )

    if _backend_declared_failure(body):
        return (
            AdapterStatus.BACKEND_DECLARED_FAILURE,
            "backend_declared_failure",
            None,
        )

    if not _response_declares_success(body):
        return (
            AdapterStatus.SCHEMA_VALIDATION_FAILURE,
            "explicit_success_marker_missing",
            None,
        )

    result_payload = _extract_result_payload(body)
    if result_payload is None:
        return (
            AdapterStatus.SCHEMA_VALIDATION_FAILURE,
            "nonempty_result_data_or_observables_mapping_required",
            None,
        )

    if _contains_non_finite_number(result_payload):
        return (
            AdapterStatus.SCHEMA_VALIDATION_FAILURE,
            "response_contains_non_finite_numeric_value",
            None,
        )

    classification = body.get(
        "backend_capability",
        body.get("model_classification", body.get("classification")),
    )

    if classification is not None:
        if not isinstance(classification, str):
            return (
                AdapterStatus.SCHEMA_VALIDATION_FAILURE,
                "classification_must_be_string_when_present",
                None,
            )

        normalized = classification.upper()
        if "AXICLASS_EDE" in normalized:
            return (
                AdapterStatus.BOUNDARY_VIOLATION,
                "backend_response_overclaims_axiclass_ede_execution",
                None,
            )

    return None, None, result_payload


def execute_locked_baseline(
    request: LockedBaselineRequest,
    *,
    transport: Optional[TransportCallable],
    endpoint: str = DEFAULT_ENDPOINT,
) -> AdapterResult:
    """Execute one explicitly injected locked-baseline transport call.

    No transport means no execution. The function never creates fallback
    values, cached values, partial-success values, or inferred values.
    """

    endpoint_error = _validate_endpoint(endpoint)
    if endpoint_error is not None:
        return _failure(
            AdapterStatus.BOUNDARY_VIOLATION,
            str(endpoint),
            endpoint_error,
        )

    request_status, request_detail = _validate_request(request)
    if request_status is not None:
        return _failure(
            request_status,
            endpoint,
            request_detail or "request_validation_failed",
        )

    if transport is None:
        return _failure(
            AdapterStatus.BOUNDARY_VIOLATION,
            endpoint,
            "explicit_transport_injection_required_no_network_default",
        )

    payload = {"use_locked_baseline": True}

    try:
        response = transport(
            endpoint,
            payload,
            float(request.timeout_seconds),
        )
    except TransportTimeoutError:
        return _failure(
            AdapterStatus.HTTP_TIMEOUT,
            endpoint,
            "transport_timeout",
        )
    except TimeoutError:
        return _failure(
            AdapterStatus.HTTP_TIMEOUT,
            endpoint,
            "transport_timeout",
        )
    except TransportConnectionError:
        return _failure(
            AdapterStatus.HTTP_CONNECTION_FAILURE,
            endpoint,
            "transport_connection_failure",
        )
    except ConnectionError:
        return _failure(
            AdapterStatus.HTTP_CONNECTION_FAILURE,
            endpoint,
            "transport_connection_failure",
        )
    except Exception as exc:
        return _failure(
            AdapterStatus.HTTP_CONNECTION_FAILURE,
            endpoint,
            f"transport_exception:{type(exc).__name__}",
        )

    if not isinstance(response, TransportResponse):
        return _failure(
            AdapterStatus.MALFORMED_RESPONSE,
            endpoint,
            "transport_must_return_TransportResponse",
        )

    if (
        isinstance(response.status_code, bool)
        or not isinstance(response.status_code, int)
    ):
        return _failure(
            AdapterStatus.MALFORMED_RESPONSE,
            endpoint,
            "http_status_code_must_be_integer",
        )

    if response.status_code < 200 or response.status_code >= 300:
        return _failure(
            AdapterStatus.HTTP_STATUS_FAILURE,
            endpoint,
            f"http_status:{response.status_code}",
        )

    schema_status, schema_detail, result_payload = _validate_response_schema(
        response.json_body
    )
    if schema_status is not None:
        return _failure(
            schema_status,
            endpoint,
            schema_detail or "response_schema_validation_failed",
        )

    assert result_payload is not None

    validated_payload = {
        "request": payload,
        "response": dict(result_payload),
        "physical_boundary_label": PHYSICAL_BOUNDARY_LABEL,
        "backend_capability": BACKEND_CAPABILITY,
    }

    return AdapterResult(
        status=AdapterStatus.SUCCESS_LOCKED_BASELINE,
        accepted=True,
        validated_payload=validated_payload,
        physical_boundary_label=PHYSICAL_BOUNDARY_LABEL,
        backend_capability=BACKEND_CAPABILITY,
        endpoint=endpoint,
        detail="locked_baseline_response_validated",
    )
