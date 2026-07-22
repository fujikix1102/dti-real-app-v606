from pathlib import Path
import json


def find_latest_manifest(base=".."):

    candidates = sorted(
        Path(base).glob(
            "_ROUTE_B_PHASE7_EVIDENCE_CHAIN_EXPORT_MANIFEST_V1_*/manifest"
        )
    )

    if not candidates:
        return None

    return candidates[-1]


def load_manifest_summary():

    manifest_dir = find_latest_manifest()

    if manifest_dir is None:
        return {
            "status": "NO_MANIFEST_FOUND"
        }

    result = {}

    for name in [
        "REGISTRY_MANIFEST.json",
        "VALIDATION_MANIFEST.json",
        "FAILURE_REPORT_MANIFEST.json",
    ]:

        p = manifest_dir / name

        if p.exists():

            data = json.loads(
                p.read_text(
                    encoding="utf-8"
                )
            )

            result[name] = {
                "exists": True,
                "entries": len(data),
            }

        else:

            result[name] = {
                "exists": False,
                "entries": 0,
            }


    result["manifest_path"] = str(
        manifest_dir
    )

    result["status"] = "MANIFEST_READY"

    return result
