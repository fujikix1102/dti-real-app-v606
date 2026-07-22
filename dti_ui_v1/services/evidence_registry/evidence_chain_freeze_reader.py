import json
from pathlib import Path


FREEZE_PATH = Path(
    "../_ROUTE_B_PHASE17_FIX1_EVIDENCE_CHAIN_FREEZE_RECORD_PATH_FIX_V1_20260721_160158/freeze/EVIDENCE_CHAIN_FREEZE_RECORD.json"
)


def load_freeze_record():

    if not FREEZE_PATH.exists():
        return {
            "status": "FREEZE_NOT_FOUND"
        }

    with open(
        FREEZE_PATH,
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    return {
        "freeze_path": str(FREEZE_PATH),
        "registry_count": len(data.get("registry", {})),
        "timeline_count": len(data.get("timeline", [])),
        "integrity_score": data.get(
            "scorecard",
            {}
        ).get(
            "score"
        ),
        "reproducibility_status": data.get(
            "reproducibility_report",
            {}
        ).get(
            "reproducibility_status"
        ),
        "status": "FREEZE_READY",
    }
