from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any
from urllib.request import Request, urlopen

from dti_ui_v1.services.run_store import (
    _external_storage_context,
    _r2_get_json,
    get_external_run_index,
    load_external_run_artifact,
)


def _check_public_url(url: str | None, timeout: int) -> dict[str, Any]:
    if not url:
        return {"checked": False, "ok": True, "reason": "not_configured"}
    try:
        request = Request(url, headers={"User-Agent": "dti-r2-artifact-smoke/1.0"})
        with urlopen(request, timeout=timeout) as response:
            status = int(response.status)
            return {"checked": True, "ok": 200 <= status < 400, "status": status}
    except Exception as exc:
        return {"checked": True, "ok": False, "error": str(exc)}


def _check_artifact(payload: dict[str, Any], *, expected_key: str | None = None) -> list[str]:
    failures: list[str] = []
    if payload.get("schema_version") != "dti-run-artifact-v2":
        failures.append("artifact_schema_version_invalid")
    if not payload.get("run_id"):
        failures.append("artifact_run_id_missing")
    if not payload.get("created_at_utc"):
        failures.append("artifact_created_at_utc_missing")
    if not payload.get("artifact_sha256"):
        failures.append("artifact_sha256_missing")
    response = payload.get("response")
    if not isinstance(response, dict):
        failures.append("artifact_response_not_object")
    if expected_key and not expected_key.endswith("/artifact.json"):
        failures.append("artifact_key_invalid")
    return failures


def run_smoke(args: argparse.Namespace) -> dict[str, Any]:
    checked_at = datetime.now(timezone.utc).isoformat()
    failures: list[str] = []
    public = _check_public_url(args.public_url, args.timeout)
    if not public.get("ok"):
        failures.append("public_url_unreachable")

    external = _external_storage_context()
    if not external.get("configured"):
        failures.append("r2_not_configured")

    index = get_external_run_index()
    if index.get("error"):
        failures.append(f"r2_index_error:{index['error']}")
    runs = index.get("runs") if isinstance(index.get("runs"), list) else []
    run_count = int(index.get("run_count") or len(runs))
    if run_count < args.min_run_count:
        failures.append(f"r2_run_count_below_min:{run_count}<{args.min_run_count}")

    latest_key = (
        f"{external.get('prefix')}/index/latest.json"
        if external.get("prefix")
        else "index/latest.json"
    )
    latest_ok = False
    try:
        latest = _r2_get_json(latest_key, now=datetime.now(timezone.utc))
        if isinstance(latest, dict):
            latest_ok = True
            failures.extend(f"latest:{failure}" for failure in _check_artifact(latest))
        else:
            failures.append("r2_latest_missing")
    except Exception as exc:
        failures.append(f"r2_latest_error:{exc}")

    artifact_checks: list[dict[str, Any]] = []
    for item in runs[: args.max_artifacts]:
        if not isinstance(item, dict):
            failures.append("r2_index_run_entry_not_object")
            continue
        artifact_key = str(item.get("artifact_key") or "")
        if not artifact_key:
            failures.append("r2_index_artifact_key_missing")
            continue
        try:
            artifact = load_external_run_artifact(artifact_key)
            artifact_failures = _check_artifact(artifact, expected_key=artifact_key)
        except Exception as exc:
            artifact_failures = [f"artifact_load_error:{exc}"]
        if artifact_failures:
            failures.extend(f"{artifact_key}:{failure}" for failure in artifact_failures)
        artifact_checks.append(
            {
                "artifact_key": artifact_key,
                "ok": not artifact_failures,
                "failures": artifact_failures,
            }
        )

    return {
        "schema_version": "dti-r2-artifact-smoke-v1",
        "checked_at_utc": checked_at,
        "ok": not failures,
        "failures": failures,
        "public": public,
        "r2": {
            "configured": bool(external.get("configured")),
            "bucket": external.get("bucket"),
            "prefix": external.get("prefix"),
            "index_key": index.get("index_key"),
            "run_count": run_count,
            "latest_key": latest_key,
            "latest_ok": latest_ok,
            "artifact_checks": artifact_checks,
        },
        "boundary": {
            "compute": "NO",
            "mcmc": "NO",
            "posterior": "NO",
            "model_comparison_claim": "NO",
            "manuscript_update": "NO",
            "pointer_promotion": "NO",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-check public DTI R2 artifacts.")
    parser.add_argument("--public-url", default="")
    parser.add_argument("--min-run-count", type=int, default=1)
    parser.add_argument("--max-artifacts", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()

    result = run_smoke(args)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
