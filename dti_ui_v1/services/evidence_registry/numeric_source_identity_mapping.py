from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class NumericSourceIdentityMapping:

    source_id: str
    source_role: str
    source_path: str
    identity_state: str
    provenance_state: str
    schema_state: str
    numeric_execution: str
    likelihood_usage: str
    posterior_usage: str
    claim_state: str


def build_identity_mapping(
    source_id: str,
    source_role: str,
    source_path: str,
) -> Dict:

    mapping = NumericSourceIdentityMapping(
        source_id=source_id,
        source_role=source_role,
        source_path=source_path,
        identity_state="DECLARED",
        provenance_state="PENDING_VALIDATION",
        schema_state="NOT_EXECUTED",
        numeric_execution="NO",
        likelihood_usage="NO",
        posterior_usage="NO",
        claim_state="NO_CLAIM",
    )

    return asdict(mapping)
