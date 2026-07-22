from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class NumericSourceAdapterContract:

    source_id: str
    source_path: str
    schema_status: str
    identity_status: str
    numeric_adoption: str
    likelihood_usage: str
    posterior_usage: str
    claim_status: str


def build_numeric_source_adapter_contract(
    source_id: str,
    source_path: str,
) -> Dict:

    contract = NumericSourceAdapterContract(
        source_id=source_id,
        source_path=source_path,
        schema_status="NOT_EXECUTED",
        identity_status="PENDING",
        numeric_adoption="NO",
        likelihood_usage="NO",
        posterior_usage="NO",
        claim_status="NO_CLAIM",
    )

    return asdict(contract)
