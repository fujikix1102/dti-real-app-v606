from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass(frozen=True)
class RealChainInputContract:

    source_role: str

    input_state: str

    required_fields: List[str]

    parameter_vector_policy: str

    seed_comparison_policy: str

    missing_value_policy: str

    chain_read: str

    posterior_usage: str

    likelihood_usage: str

    numeric_execution: str

    claim_state: str


def build_real_chain_input_contract() -> Dict:

    contract = RealChainInputContract(

        source_role="FUTURE_MCMC_CHAIN",

        input_state="CONTRACT_ONLY",

        required_fields=[
            "sample_id",
            "seed_id",
            "parameter_vector",
        ],

        parameter_vector_policy=
            "EXPLICIT_PARAMETER_SELECTION_REQUIRED",

        seed_comparison_policy=
            "INDEPENDENT_CHAIN_COMPARISON",

        missing_value_policy=
            "FAIL_ON_UNDECLARED_MISSING",

        chain_read="NO",

        posterior_usage="NO",

        likelihood_usage="NO",

        numeric_execution="NO",

        claim_state="NO_CLAIM",
    )

    return asdict(contract)
