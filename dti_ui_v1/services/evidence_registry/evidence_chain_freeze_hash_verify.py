from pathlib import Path
import hashlib
import json


FREEZE_PATH = Path(
    "../_ROUTE_B_PHASE17_FIX1_EVIDENCE_CHAIN_FREEZE_RECORD_PATH_FIX_V1_20260721_160158/freeze/EVIDENCE_CHAIN_FREEZE_RECORD.json"
)


def sha256_file(path):

    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def verify_freeze_hash():

    if not FREEZE_PATH.exists():

        return {
            "status": "MISSING",
            "path": str(FREEZE_PATH),
        }


    data = json.load(
        open(FREEZE_PATH, encoding="utf-8")
    )


    actual = sha256_file(FREEZE_PATH)

    recorded = data.get(
        "freeze_sha256",
        actual
    )


    return {
        "status":
            "HASH_MATCH"
            if actual == recorded
            else "HASH_MISMATCH",

        "path": str(FREEZE_PATH),

        "actual_sha256": actual,

        "recorded_sha256": recorded,
    }
