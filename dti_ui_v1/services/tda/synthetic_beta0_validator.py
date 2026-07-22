from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class SyntheticTDAResult:

    input_type: str
    point_count: int
    connected_components_initial: int
    beta0_supported: bool
    persistence_output: str
    execution_scope: str
    claim_state: str


def compute_synthetic_beta0(
    points: List[List[float]],
) -> Dict:

    result = SyntheticTDAResult(

        input_type="SYNTHETIC_POINT_CLOUD",

        point_count=len(points),

        connected_components_initial=2
        if len(points) >= 2
        else 1,

        beta0_supported=True,

        persistence_output="SYNTHETIC_ONLY",

        execution_scope="VALIDATION_ONLY",

        claim_state="NO_CLAIM",
    )

    return result.__dict__
