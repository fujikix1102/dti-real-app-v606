import json
from pathlib import Path


_THIS_FILE = Path(__file__).resolve()
_REPO_ROOT = _THIS_FILE.parents[3]

SNAPSHOT_CANDIDATE_PATHS = [
    _REPO_ROOT / "data" / "evidence" / "EVIDENCE_CHAIN_READINESS_SNAPSHOT.json",
    _REPO_ROOT.parent
    / "_ROUTE_B_PHASE24_EVIDENCE_CHAIN_READINESS_SNAPSHOT_EXPORT_V1_20260721_163706"
    / "snapshot"
    / "EVIDENCE_CHAIN_READINESS_SNAPSHOT.json",
]


def load_readiness_snapshot():

    checked_paths = []

    for p in SNAPSHOT_CANDIDATE_PATHS:

        checked_paths.append(str(p))

        if not p.exists():
            continue

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

    return {
        "status": "SNAPSHOT_NOT_FOUND",
        "candidate_paths": checked_paths,
    }
