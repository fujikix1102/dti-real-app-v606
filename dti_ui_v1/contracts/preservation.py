from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MigrationStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    EXTRACTED = "EXTRACTED"
    VERIFIED = "VERIFIED"
    ACTIVATED = "ACTIVATED"
    ROLLBACK_READY = "ROLLBACK_READY"


@dataclass(frozen=True)
class FeaturePreservationRecord:
    source_name: str
    source_start_line: int
    source_end_line: int
    source_sha256: str
    target_module: str
    status: MigrationStatus
    input_count_before: int = 0
    input_count_after: int = 0
    display_count_before: int = 0
    display_count_after: int = 0
    claim_boundary_preserved: bool = False
    provenance_preserved: bool = False
    numeric_precision_preserved: bool = False
