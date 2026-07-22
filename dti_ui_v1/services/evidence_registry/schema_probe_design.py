from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class SchemaProbeDesign:

    source_id: str

    required_columns: list

    dtype_policy: str

    null_policy: str

    probe_execution: str

    source_read: str

    parse_execution: str

    numeric_execution: str

    likelihood_usage: str

    posterior_usage: str

    claim_state: str


def build_schema_probe_design(
    source_id: str,
) -> Dict:

    design = SchemaProbeDesign(

        source_id=source_id,

        required_columns=[
            "source_id",
            "row_id",
            "x_label",
        ],

        dtype_policy="STRING_FIRST_EXPLICIT_CAST",

        null_policy="FAIL_ON_UNDECLARED_NULL",

        probe_execution="DESIGN_ONLY",

        source_read="NO",

        parse_execution="NO",

        numeric_execution="NO",

        likelihood_usage="NO",

        posterior_usage="NO",

        claim_state="NO_CLAIM",
    )

    return asdict(design)
