from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class NumericSourceReadonlyBinding:

    source_id: str
    contract_available: str
    identity_available: str
    schema_available: str
    provenance_available: str

    registry_access: str

    source_read: str
    source_parse: str
    numeric_execution: str

    likelihood_usage: str
    posterior_usage: str
    claim_state: str


def build_readonly_binding(
    source_id: str,
) -> Dict:

    binding = NumericSourceReadonlyBinding(

        source_id=source_id,

        contract_available="YES",

        identity_available="YES",

        schema_available="YES",

        provenance_available="YES",

        registry_access="REFERENCE_ONLY",

        source_read="NO",

        source_parse="NO",

        numeric_execution="NO",

        likelihood_usage="NO",

        posterior_usage="NO",

        claim_state="NO_CLAIM",
    )

    return asdict(binding)
