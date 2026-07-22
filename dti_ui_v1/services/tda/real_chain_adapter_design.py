from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass(frozen=True)
class RealChainAdapterDesign:

    source_type: str

    adapter_state: str

    required_columns: List[str]

    parameter_vector_rule: str

    weight_policy: str

    burnin_policy: str

    covariance_policy: str

    distance_policy: str

    topology_method: str

    chain_read: str

    numeric_execution: str

    posterior_usage: str

    likelihood_usage: str

    claim_state: str


def build_real_chain_adapter_design() -> Dict:

    design = RealChainAdapterDesign(

        source_type="FUTURE_MCMC_CHAIN",

        adapter_state="DESIGN_ONLY",

        required_columns=[
            "sample_id",
            "seed_id",
            "parameter_vector",
        ],

        parameter_vector_rule=
            "EXPLICIT_PARAMETER_LIST_REQUIRED",

        weight_policy=
            "DECLARED_WEIGHT_HANDLING_REQUIRED",

        burnin_policy=
            "DECLARED_BURNIN_HANDLING_REQUIRED",

        covariance_policy=
            "EXPLICIT_COVARIANCE_SOURCE_REQUIRED",

        distance_policy=
            "MAHALANOBIS_DISTANCE_DESIGN_ONLY",

        topology_method=
            "VIETORIS_RIPS_H0_DESIGN_ONLY",

        chain_read="NO",

        numeric_execution="NO",

        posterior_usage="NO",

        likelihood_usage="NO",

        claim_state="NO_CLAIM",
    )

    return asdict(design)
