"""Read-only loader for frozen likelihood assets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .likelihood_contract import (
    FrozenLikelihoodIdentity,
    FrozenLikelihoodPoint,
)


class FrozenLikelihoodAssetError(ValueError):
    pass


def load_frozen_likelihood_json(
    path: str | Path,
) -> Mapping[str, Any]:
    source = Path(path)

    if not source.exists():
        raise FrozenLikelihoodAssetError(
            "frozen likelihood asset missing"
        )

    data = json.loads(
        source.read_text()
    )

    if not isinstance(data, Mapping):
        raise FrozenLikelihoodAssetError(
            "asset root must be mapping"
        )

    return data


def build_frozen_point(
    data: Mapping[str, Any],
) -> FrozenLikelihoodPoint:

    identity = FrozenLikelihoodIdentity(
        case_id=str(data["case_id"]),
        mean_sha256=str(data["mean_sha256"]),
        cov_sha256=str(data["cov_sha256"]),
        vector_sha256=str(data["vector_sha256"]),
    )

    return FrozenLikelihoodPoint(
        H0=float(data["H0"]),
        rs_drag=float(data["rs_drag"]),
        chi2=float(data["chi2"]),
        loglike=float(
            data["minus_half_chi2_loglike"]
        ),
        identity=identity,
    )
