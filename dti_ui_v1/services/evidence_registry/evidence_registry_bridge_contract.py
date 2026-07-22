from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class EvidenceRegistryBridgeContract:

    source_id: str

    identity_mapping: str

    schema_contract: str

    provenance_contract: str

    registry_binding: str

    source_read: str

    parse_execution: str

    numeric_execution: str

    likelihood_usage: str

    posterior_usage: str

    claim_state: str


def build_registry_bridge_contract(
    source_id: str,
) -> Dict:

    contract = EvidenceRegistryBridgeContract(

        source_id=source_id,

        identity_mapping="AVAILABLE",

        schema_contract="AVAILABLE",

        provenance_contract="AVAILABLE",

        registry_binding="CONTRACT_ONLY",

        source_read="NO",

        parse_execution="NO",

        numeric_execution="NO",

        likelihood_usage="NO",

        posterior_usage="NO",

        claim_state="NO_CLAIM",
    )

    return asdict(contract)
