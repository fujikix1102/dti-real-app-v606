"""Validated immutable compute-request contract for PERFECT FIT."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
import math
import re
from typing import Any, Mapping
from uuid import uuid4


_REQUEST_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{7,127}$")


class ComputeContractError(ValueError):
    """Raised when a request violates the compute contract."""


class SolverKind(str, Enum):
    CLASS = "CLASS"
    AXICLASS = "AXICLASS"


class ExecutionRoute(str, Enum):
    SINGLE_BACKGROUND = "SINGLE_BACKGROUND"
    SINGLE_BAO = "SINGLE_BAO"


class RequestState(str, Enum):
    VALIDATED = "VALIDATED"


@dataclass(frozen=True)
class ParameterValue:
    name: str
    value: float
    unit: str
    role: str

    def validate(self) -> None:
        if not self.name.strip():
            raise ComputeContractError("parameter name is empty")

        if not math.isfinite(self.value):
            raise ComputeContractError(
                f"parameter {self.name!r} must be finite"
            )

        if self.role not in {"fixed", "editable"}:
            raise ComputeContractError(
                f"invalid role for {self.name!r}: {self.role!r}"
            )


@dataclass(frozen=True)
class ComputeRequest:
    schema_version: str
    request_id: str
    solver: SolverKind
    route: ExecutionRoute
    parameters: tuple[ParameterValue, ...]
    timeout_seconds: int
    source: str
    state: RequestState = RequestState.VALIDATED

    def validate(self) -> None:
        if self.schema_version != "perfect-fit.compute-request.v1":
            raise ComputeContractError(
                f"unsupported schema: {self.schema_version}"
            )

        if not _REQUEST_ID_RE.fullmatch(self.request_id):
            raise ComputeContractError(
                f"invalid request_id: {self.request_id!r}"
            )

        if not 1 <= self.timeout_seconds <= 600:
            raise ComputeContractError(
                "timeout_seconds must be between 1 and 600"
            )

        if not self.source.strip():
            raise ComputeContractError("source is empty")

        if not self.parameters:
            raise ComputeContractError(
                "at least one parameter is required"
            )

        names: set[str] = set()

        for parameter in self.parameters:
            parameter.validate()

            if parameter.name in names:
                raise ComputeContractError(
                    f"duplicate parameter: {parameter.name}"
                )

            names.add(parameter.name)

    def to_payload(self) -> dict[str, Any]:
        self.validate()

        return {
            "schema_version": self.schema_version,
            "request_id": self.request_id,
            "solver": self.solver.value,
            "route": self.route.value,
            "parameters": [
                asdict(parameter)
                for parameter in self.parameters
            ],
            "timeout_seconds": self.timeout_seconds,
            "source": self.source,
            "state": self.state.value,
        }

    def canonical_json(self) -> str:
        return json.dumps(
            self.to_payload(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )

    def sha256(self) -> str:
        return sha256(
            self.canonical_json().encode("utf-8")
        ).hexdigest()


def new_request_id(prefix: str = "pf") -> str:
    safe_prefix = re.sub(
        r"[^A-Za-z0-9._:-]",
        "-",
        prefix,
    ).strip("-") or "pf"

    return f"{safe_prefix}-{uuid4().hex}"


def parameter_from_mapping(
    item: Mapping[str, Any],
) -> ParameterValue:
    required = {"name", "value", "unit", "role"}
    missing = required.difference(item)

    if missing:
        raise ComputeContractError(
            f"parameter missing keys: {sorted(missing)}"
        )

    try:
        value = float(item["value"])
    except (TypeError, ValueError) as exc:
        raise ComputeContractError(
            f"non-numeric value for {item.get('name')!r}"
        ) from exc

    parameter = ParameterValue(
        name=str(item["name"]),
        value=value,
        unit=str(item["unit"]),
        role=str(item["role"]),
    )
    parameter.validate()
    return parameter
