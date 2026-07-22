"""Adapter from frozen likelihood point to existing UI response shape."""

from __future__ import annotations

from typing import Mapping

from .likelihood_contract import (
    FrozenLikelihoodPoint,
    LikelihoodAdapterResponse,
)


def build_likelihood_response(
    point: FrozenLikelihoodPoint,
) -> LikelihoodAdapterResponse:

    return LikelihoodAdapterResponse(
        status="ok",
        engine="FROZEN_LIKELIHOOD_ADAPTER",
        metadata={
            "case_id": point.identity.case_id,
            "source_type": "FROZEN_LIKELIHOOD",
            "inference_boundary": "diagnostic_only",
            "provenance": {
                "mean_sha256": point.identity.mean_sha256,
                "cov_sha256": point.identity.cov_sha256,
                "vector_sha256": point.identity.vector_sha256,
            },
        },
        derived={
            "rs_drag": point.rs_drag,
        },
        desi_dr2_bao={
            "status": "ok",
            "chi2": point.chi2,
            "loglike": point.loglike,
        },
    )


def response_as_dict(
    response: LikelihoodAdapterResponse,
) -> Mapping[str, object]:

    return {
        "status": response.status,
        "engine": response.engine,
        "metadata": dict(response.metadata),
        "derived": dict(response.derived),
        "desi_dr2_bao": dict(response.desi_dr2_bao),
        "posterior": "NO",
        "MCMC": "NO",
    }
