from pathlib import Path
from datetime import datetime


def build_scientific_result_payload(
    source_path=None,
    source_label="LOCAL_DIAGNOSTIC_SOURCE",
):
    path = Path(source_path) if source_path else None

    return {
        "source_label": source_label,
        "source_path": str(path) if path else "NOT_BOUND",
        "source_exists": bool(path and path.exists()),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "claim_boundary": {
            "likelihood": False,
            "posterior": False,
            "mcmc": False,
            "physical_claim": False,
        },
        "status": "DIAGNOSTIC_PAYLOAD_ONLY",
    }
