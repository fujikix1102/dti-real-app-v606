from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class SourceProvenanceChainContract:

    source_id: str
    source_role: str
    identity_state: str
    provenance_state: str
    schema_state: str
    source_location_state: str
    acquisition_state: str
    transformation_state: str
    numeric_execution: str
    likelihood_usage: str
    posterior_usage: str
    claim_state: str


def build_source_provenance_chain_contract(
    source_id: str,
    source_role: str,
) -> Dict:

    contract = SourceProvenanceChainContract(

        source_id=source_id,

        source_role=source_role,

        identity_state="DECLARED",

        provenance_state="CHAIN_DECLARED",

        schema_state="BOUNDARY_DEFINED",

        source_location_state="NOT_VERIFIED",

        acquisition_state="NOT_EXECUTED",

        transformation_state="NOT_EXECUTED",

        numeric_execution="NO",

        likelihood_usage="NO",

        posterior_usage="NO",

        claim_state="NO_CLAIM",
    )

    return asdict(contract)
