import pandas as pd


PRIMARY_MAP = {
    "boundary_numeric_adoption": "boundary_numeric_adoption",
    "boundary_likelihood": "boundary_likelihood",
    "boundary_physical_claim": "boundary_physical_claim",
}


SECONDARY_MAP = {
    "boundary_diagnostic_use": "boundary_numeric_adoption",
    "boundary_likelihood_use": "boundary_likelihood",
    "boundary_claim_use": "boundary_physical_claim",
}


def normalize_section8_schema(df: pd.DataFrame, source_type: str):

    df = df.copy()

    df = df.astype(str)

    if source_type == "primary":

        for src, dst in PRIMARY_MAP.items():
            if src in df.columns:
                df[dst] = df[src]

    elif source_type == "secondary":

        for src, dst in SECONDARY_MAP.items():
            if src in df.columns:
                df[dst] = df[src]

    else:
        raise ValueError(
            "unknown source_type"
        )

    required = [
        "boundary_numeric_adoption",
        "boundary_likelihood",
        "boundary_physical_claim",
    ]

    for col in required:
        if col not in df.columns:
            df[col] = "UNRESOLVED"

    return df.astype(str)
