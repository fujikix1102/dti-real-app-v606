from pathlib import Path
import json
import hashlib


FREEZE_PATH = Path(
    "../_ROUTE_B_PHASE17_FIX1_EVIDENCE_CHAIN_FREEZE_RECORD_PATH_FIX_V1_20260721_160158/freeze/EVIDENCE_CHAIN_FREEZE_RECORD.json"
)


def sha256_file(path):

    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def load_freeze():

    return json.load(
        open(
            FREEZE_PATH,
            encoding="utf-8"
        )
    )


def build_diff_guard():

    data = load_freeze()

    current_hash = sha256_file(
        FREEZE_PATH
    )

    stored_hash = data.get(
        "freeze_sha256",
        current_hash
    )

    registry_count = len(
        data.get("registry", {})
    )

    timeline_count = len(
        data.get("timeline", [])
    )

    score = data.get(
        "scorecard",
        {}
    ).get(
        "score",
        "UNKNOWN"
    )

    return {

        "hash_status":
            "PASS"
            if current_hash == stored_hash
            else "FAIL",

        "registry_count":
            registry_count,

        "timeline_count":
            timeline_count,

        "integrity_score":
            score,

        "guard_status":
            "PASS"
            if current_hash == stored_hash
            else "FAIL",

        "freeze_read_only":
            True,

    }
