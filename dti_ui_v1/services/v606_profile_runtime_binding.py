from __future__ import annotations

from dataclasses import dataclass
from typing import MutableMapping

from dti_ui_v1.services.v606_profile_adapter import (
    V606Profile,
    V606ProfileLibrary,
)


SESSION_KEY_MAP = {
    "H0": "perfect_fit_general_class_H0_v1",
    "omega_b": "perfect_fit_general_class_omega_b_v1",
    "omega_cdm": "perfect_fit_general_class_omega_cdm_v1",
    "f_EDE": "perfect_fit_general_class_f_EDE_v2",
}

REFERENCE_ONLY_FIELDS = ("sigma8", "S8")
OPTIONAL_UNBOUND_FIELDS = ("z_c",)


class V606ProfileRuntimeBindingError(ValueError):
    pass


@dataclass(frozen=True)
class V606RuntimeBindingResult:
    profile_id: str
    category: str
    session_payload: dict[str, float]
    reference_outputs: dict[str, str]
    optional_unbound: tuple[str, ...]


def build_session_payload(profile: V606Profile) -> dict[str, float]:
    missing = [
        field
        for field in SESSION_KEY_MAP
        if field not in profile.parameters
    ]

    if missing:
        raise V606ProfileRuntimeBindingError(
            "missing direct parameters: " + ", ".join(missing)
        )

    payload: dict[str, float] = {}

    for field, session_key in SESSION_KEY_MAP.items():
        raw_value = profile.parameters[field]

        try:
            payload[session_key] = float(raw_value)
        except (TypeError, ValueError) as exc:
            raise V606ProfileRuntimeBindingError(
                f"invalid numeric value for {field}: {raw_value!r}"
            ) from exc

    return payload


def prepare_runtime_binding(
    library: V606ProfileLibrary,
    profile_id: str,
) -> V606RuntimeBindingResult:
    try:
        profile = library.by_id(profile_id)
    except KeyError as exc:
        raise V606ProfileRuntimeBindingError(
            f"unknown profile_id: {profile_id}"
        ) from exc

    return V606RuntimeBindingResult(
        profile_id=profile.profile_id,
        category=profile.category,
        session_payload=build_session_payload(profile),
        reference_outputs=profile.reference_payload(),
        optional_unbound=profile.optional_unbound,
    )


def apply_runtime_binding(
    state: MutableMapping[str, object],
    binding: V606RuntimeBindingResult,
) -> tuple[str, ...]:
    changed: list[str] = []

    for key, value in binding.session_payload.items():
        if state.get(key) != value:
            state[key] = value
            changed.append(key)

    return tuple(changed)

PENDING_SESSION_PAYLOAD_KEY = "perfect_fit_v606_pending_session_payload_v1"


def queue_runtime_binding(
    state: MutableMapping[str, object],
    binding: V606RuntimeBindingResult,
) -> tuple[str, ...]:
    payload = dict(binding.session_payload)

    invalid_keys = sorted(set(payload) - set(SESSION_KEY_MAP.values()))
    if invalid_keys:
        raise V606ProfileRuntimeBindingError(
            "invalid pending session keys: " + ", ".join(invalid_keys)
        )

    for key, value in payload.items():
        if not isinstance(value, float):
            raise V606ProfileRuntimeBindingError(
                f"pending value for {key} must be float"
            )

    state[PENDING_SESSION_PAYLOAD_KEY] = payload
    return tuple(payload)


def consume_pending_runtime_binding(
    state: MutableMapping[str, object],
) -> tuple[str, ...]:
    pending = state.pop(PENDING_SESSION_PAYLOAD_KEY, None)

    if pending is None:
        return ()

    if not isinstance(pending, dict):
        raise V606ProfileRuntimeBindingError(
            "pending session payload must be a dictionary"
        )

    allowed = set(SESSION_KEY_MAP.values())
    invalid_keys = sorted(set(pending) - allowed)

    if invalid_keys:
        raise V606ProfileRuntimeBindingError(
            "invalid pending session keys: " + ", ".join(invalid_keys)
        )

    changed: list[str] = []

    for key, value in pending.items():
        if not isinstance(value, float):
            raise V606ProfileRuntimeBindingError(
                f"pending value for {key} must be float"
            )

        if state.get(key) != value:
            state[key] = value
            changed.append(key)

    return tuple(changed)
