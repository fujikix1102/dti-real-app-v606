"""
DTI Stage 2 lightweight lookup solver skeleton.

Boundary:
- No raw DESI DR2 parsing.
- No loader execution.
- No likelihood evaluation.
- No posterior inference.
- No MCMC.
- No scientific claim upgrade.
- No manuscript or pointer promotion.
- Diagnostic fail-closed infrastructure only.

This module is intentionally conservative. It validates source-like
metadata and provides fail-closed query behavior until a later validation
gate explicitly enables numeric lookup use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional


BOUNDARY_LABEL = (
    "DIAGNOSTIC_LOOKUP_SKELETON_ONLY_"
    "NO_RAW_PARSE_NO_LOADER_NO_LIKELIHOOD_NO_POSTERIOR_NO_MCMC"
)


@dataclass(frozen=True)
class LookupResult:
    """A bounded diagnostic lookup response."""

    status: str
    value: Optional[float]
    reason: str
    boundary: str = BOUNDARY_LABEL


class Stage2LookupSolver:
    """
    Fail-closed Stage 2 lookup solver skeleton.

    The current implementation does not instantiate lookup numeric values.
    It exists to make future validation boundaries explicit.
    """

    def __init__(
        self,
        axis_contract_path: Optional[str | Path] = None,
        asset_manifest_path: Optional[str | Path] = None,
    ) -> None:
        self.axis_contract_path = Path(axis_contract_path) if axis_contract_path else None
        self.asset_manifest_path = Path(asset_manifest_path) if asset_manifest_path else None
        self._validated = False

    def validate_sources(self) -> LookupResult:
        """
        Validate source path presence only.

        This does not parse raw DESI DR2, does not execute the loader,
        and does not compute any cosmological quantity.
        """

        missing = []
        for label, path in [
            ("axis_contract_path", self.axis_contract_path),
            ("asset_manifest_path", self.asset_manifest_path),
        ]:
            if path is None:
                missing.append(label)
            elif not path.exists():
                missing.append(f"{label}:{path}")

        if missing:
            self._validated = False
            return LookupResult(
                status="BLOCKED_MISSING_SOURCE",
                value=None,
                reason="missing required source path(s): " + ",".join(missing),
            )

        self._validated = True
        return LookupResult(
            status="VALIDATED_METADATA_PATHS_ONLY",
            value=None,
            reason="source paths exist; no numeric lookup performed",
        )

    def query_nearest(self, coordinates: Mapping[str, Any]) -> LookupResult:
        """
        Future nearest-neighbor query placeholder.

        Current behavior is fail-closed. It never returns a numeric value.
        """

        if not self._validated:
            return LookupResult(
                status="BLOCKED_NOT_VALIDATED",
                value=None,
                reason="validate_sources must pass before query",
            )

        if not coordinates:
            return LookupResult(
                status="BLOCKED_EMPTY_COORDINATES",
                value=None,
                reason="coordinates are empty",
            )

        return LookupResult(
            status="BLOCKED_NOT_IMPLEMENTED",
            value=None,
            reason="nearest lookup is not implemented in this gate",
        )

    def query_multilinear(self, coordinates: Mapping[str, Any]) -> LookupResult:
        """
        Future multilinear interpolation placeholder.

        Current behavior is fail-closed. It never returns a numeric value.
        """

        return LookupResult(
            status="BLOCKED_INTERPOLATION_NOT_ENABLED",
            value=None,
            reason="multilinear interpolation requires a later validation gate",
        )

    def return_blocked_oob(self, reason: str = "out of bounds") -> LookupResult:
        """Return the required fail-closed out-of-bounds response."""

        return LookupResult(
            status="BLOCKED_OOB",
            value=None,
            reason=reason,
        )


def module_boundary() -> Mapping[str, Any]:
    """Return machine-readable non-claim boundaries."""

    return {
        "boundary": BOUNDARY_LABEL,
        "raw_desi_dr2_parse": False,
        "loader_execution": False,
        "likelihood": False,
        "posterior": False,
        "mcmc": False,
        "scientific_claim_upgrade": False,
        "manuscript_update": False,
        "pointer_promotion": False,
        "lookup_numeric_values_instantiated": False,
        "interpolation_execution": False,
    }
