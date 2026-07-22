from pathlib import Path
import hashlib
import pandas as pd


def build_diagnostic_summary(source_path):

    path = Path(source_path)

    if not path.exists():
        return {
            "source_exists": False,
            "status": "SOURCE_NOT_FOUND",
        }

    df = pd.read_csv(
        path,
        sep="\t",
        dtype=str,
        keep_default_na=False,
    )

    df = df.astype(str)

    schema = "\n".join(
        f"{c}:str"
        for c in df.columns
    )

    flags = {}

    for col in [
        "diagnostic_use",
        "likelihood_use",
        "claim_use",
    ]:
        if col in df.columns:
            flags[col] = sorted(
                df[col].unique().tolist()
            )

    return {
        "source_exists": True,
        "source_path": str(path),
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "schema_hash": hashlib.sha256(
            schema.encode()
        ).hexdigest(),
        "diagnostic_flags": flags,
        "boundary_flags": {
            "likelihood": "NO_EXECUTION",
            "posterior": "NO_EXECUTION",
            "mcmc": "NO_EXECUTION",
            "physical_claim": "NO_EXECUTION",
        },
        "status": "DIAGNOSTIC_SUMMARY_READY",
    }
