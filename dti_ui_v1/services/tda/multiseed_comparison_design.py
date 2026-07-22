from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass(frozen=True)
class MultiSeedComparisonDesign:

    comparison_scope: str

    seed_unit: str

    input_state: str

    comparison_metrics: List[str]

    beta0_comparison: str

    persistence_comparison: str

    outlier_policy: str

    chain_read: str

    numeric_execution: str

    posterior_usage: str

    likelihood_usage: str

    claim_state: str


def build_multiseed_comparison_design() -> Dict:

    design = MultiSeedComparisonDesign(

        comparison_scope=
            "INDEPENDENT_SEED_DIAGNOSTIC",

        seed_unit=
            "CHAIN_SEED_ID",

        input_state=
            "SYNTHETIC_DESIGN_ONLY",

        comparison_metrics=[
            "initial_beta0",
            "persistence_lifetime_summary",
            "component_count_curve",
        ],

        beta0_comparison=
            "BETWEEN_SEED_COMPARISON",

        persistence_comparison=
            "DISTRIBUTION_LEVEL_COMPARISON",

        outlier_policy=
            "PREDEFINED_REVIEW_REQUIRED",

        chain_read="NO",

        numeric_execution="NO",

        posterior_usage="NO",

        likelihood_usage="NO",

        claim_state="NO_CLAIM",
    )

    return asdict(design)
