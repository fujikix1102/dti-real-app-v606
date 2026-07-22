import json
from pathlib import Path


SNAPSHOT_PATH = (
    "../_ROUTE_B_PHASE24_EVIDENCE_CHAIN_READINESS_SNAPSHOT_EXPORT_V1_20260721_163706/"
    "snapshot/EVIDENCE_CHAIN_READINESS_SNAPSHOT.json"
)


def load_readiness_snapshot():

    p = Path(SNAPSHOT_PATH)

    if not p.exists():
        return {
            "status": "SNAPSHOT_NOT_FOUND"
        }

    with open(
        p,
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    return {
        "status": "SNAPSHOT_READY",
        "registry_count": len(data.get("registry", {})),
        "health_status": data["health"]["overall"],
        "public_readiness": data["public_readiness"]["public_readiness"],
        "guard_status": data["freeze_guard"]["guard_status"],
        "alert_count": data["alerts"]["alert_count"],
        "snapshot_path": str(p),
    }
