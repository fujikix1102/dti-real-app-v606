from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass(frozen=True)
class SchemaBoundaryContract:

    source_id: str
    required_columns: List[str]
    dtype_policy: str
    null_policy: str
    numeric_conversion: str
    schema_execution: str
    source_read: str
    parse_execution: str
    likelihood_usage: str
    posterior_usage: str
    claim_state: str


def build_schema_boundary_contract(
    source_id: str,
) -> Dict:

    contract = SchemaBoundaryContract(

        source_id=source_id,

        required_columns=[
            "source_id",
            "row_id",
            "x_label",
        ],

        dtype_policy="EXPLICIT_STRING_FIRST",

        null_policy="EXPLICIT_HANDLING_REQUIRED",

        numeric_conversion="NOT_EXECUTED",

        schema_execution="NOT_EXECUTED",

        source_read="NO",

        parse_execution="NO",

        likelihood_usage="NO",

        posterior_usage="NO",

        claim_state="NO_CLAIM",
    )

    return asdict(contract)
