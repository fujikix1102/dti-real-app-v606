"""Audit-only Stage 2 loader skeleton.

This module defines interface objects only. It does not touch external
resources, perform data loading, perform numeric conversion, or execute a
scientific calculation. All executable paths are intentionally closed until
a later explicit gate opens them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


STATUS_PASS = "PASS"
STATUS_FAIL = "FAIL"
STATUS_STOP = "STOP"
STATUS_SKIP = "SKIP"
STATUS_LOCKED = "LOCKED"
STATUS_QUARANTINED = "QUARANTINED"


@dataclass(frozen=True)
class LoaderSourceIdentity:
    """String-only source identity record."""

    source_id: str
    source_url: str
    provenance_gate: str
    local_path: Optional[str] = None
    sha256: Optional[str] = None


@dataclass(frozen=True)
class LoaderSchemaContract:
    """Schema-name contract. This object carries names only."""

    schema_id: str
    required_columns: List[str] = field(default_factory=list)
    optional_columns: List[str] = field(default_factory=list)
    forbidden_semantic_columns: List[str] = field(default_factory=list)
    numeric_cast_policy: str = STATUS_LOCKED


@dataclass(frozen=True)
class LoaderRunConfig:
    """Execution gates. Defaults are closed."""

    mode: str = "metadata_only"
    allow_file_access: bool = False
    allow_numeric_conversion: bool = False
    allow_semantic_assignment: bool = False


@dataclass(frozen=True)
class LoaderResult:
    """Result manifest placeholder. No table object is returned."""

    status: str
    source_identity: LoaderSourceIdentity
    message: str
    schema_report_path: Optional[str] = None
    quarantine_report_path: Optional[str] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None


class DTIStage2Loader:
    """Closed loader shell for future audited gates."""

    def __init__(
        self,
        source_identity: LoaderSourceIdentity,
        schema_contract: LoaderSchemaContract,
        run_config: Optional[LoaderRunConfig] = None,
    ) -> None:
        self.source_identity = source_identity
        self.schema_contract = schema_contract
        self.run_config = run_config or LoaderRunConfig()

    def validate_contract(self) -> LoaderResult:
        """Validate object-level contract fields only."""
        if not self.source_identity.source_id:
            return LoaderResult(
                status=STATUS_FAIL,
                source_identity=self.source_identity,
                message="missing source_id",
            )
        if not self.source_identity.source_url:
            return LoaderResult(
                status=STATUS_FAIL,
                source_identity=self.source_identity,
                message="missing source_url",
            )
        if not self.source_identity.provenance_gate:
            return LoaderResult(
                status=STATUS_FAIL,
                source_identity=self.source_identity,
                message="missing provenance_gate",
            )
        if not self.schema_contract.schema_id:
            return LoaderResult(
                status=STATUS_FAIL,
                source_identity=self.source_identity,
                message="missing schema_id",
            )
        if self.run_config.allow_file_access:
            return LoaderResult(
                status=STATUS_STOP,
                source_identity=self.source_identity,
                message="file access is locked in this skeleton",
            )
        if self.run_config.allow_numeric_conversion:
            return LoaderResult(
                status=STATUS_STOP,
                source_identity=self.source_identity,
                message="numeric conversion is locked in this skeleton",
            )
        if self.run_config.allow_semantic_assignment:
            return LoaderResult(
                status=STATUS_STOP,
                source_identity=self.source_identity,
                message="semantic assignment is locked in this skeleton",
            )
        return LoaderResult(
            status=STATUS_PASS,
            source_identity=self.source_identity,
            message="contract objects validated; executable paths remain locked",
        )

    def plan_fixture(self) -> Dict[str, str]:
        """Return a future fixture plan without executing it."""
        return {
            "status": STATUS_LOCKED,
            "mode": self.run_config.mode,
            "schema_id": self.schema_contract.schema_id,
            "message": "fixture execution is reserved for a later explicit gate",
        }


__all__ = [
    "STATUS_PASS",
    "STATUS_FAIL",
    "STATUS_STOP",
    "STATUS_SKIP",
    "STATUS_LOCKED",
    "STATUS_QUARANTINED",
    "LoaderSourceIdentity",
    "LoaderSchemaContract",
    "LoaderRunConfig",
    "LoaderResult",
    "DTIStage2Loader",
]
