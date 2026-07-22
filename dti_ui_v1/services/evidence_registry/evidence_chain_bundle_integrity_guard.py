import hashlib
import json
from pathlib import Path


BUNDLE = Path(
    "../_ROUTE_B_PHASE27_EVIDENCE_CHAIN_SNAPSHOT_EXPORT_BUNDLE_V1_20260721_164100/"
    "bundle/EVIDENCE_CHAIN_SNAPSHOT_BUNDLE.json"
)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_integrity_guard():

    with open(BUNDLE, encoding="utf-8") as f:
        bundle = json.load(f)

    sha = sha256_file(BUNDLE)

    checks = {
        "bundle_exists": BUNDLE.exists(),
        "hash_length": len(sha) == 64,
        "bundle_status":
            bundle.get("bundle_status") == "READY",
        "registry_count":
            bundle["snapshot_summary"]["registry_count"] >= 3,
        "health":
            bundle["snapshot_summary"]["health_status"] == "PASS",
        "readiness":
            bundle["snapshot_summary"]["public_readiness"] == "READY",
    }

    return {
        "checks": checks,
        "sha256": sha,
        "overall": "PASS"
            if all(checks.values())
            else "FAIL",
    }
