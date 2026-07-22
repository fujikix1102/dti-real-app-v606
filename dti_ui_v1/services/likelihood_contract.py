"""Immutable contract definitions for frozen likelihood adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class FrozenLikelihoodIdentity:
    case_id: str
    mean_sha256: str
    cov_sha256: str
    vector_sha256: str


@dataclass(frozen=True)
class FrozenLikelihoodPoint:
    H0: float
    rs_drag: float
    chi2: float
    loglike: float
    identity: FrozenLikelihoodIdentity

    @property
    def case_id(self) -> str:
        return self.identity.case_id


@dataclass(frozen=True)
class LikelihoodAdapterResponse:
    status: str
    engine: str
    metadata: Mapping[str, object]
    derived: Mapping[str, object]
    desi_dr2_bao: Mapping[str, object]
