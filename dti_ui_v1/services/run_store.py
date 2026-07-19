from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


SCHEMA_VERSION = "dti-run-artifact-v2"


def _runtime_identity() -> dict[str, Any]:
    versions: dict[str, str] = {}
    for package in ("classy", "numpy", "scipy", "streamlit", "altair", "cobaya"):
        try:
            module = __import__(package)
            versions[package] = str(getattr(module, "__version__", "installed"))
        except Exception:
            versions[package] = "unavailable"
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": versions,
    }


def _artifact_directory() -> Path:
    override = os.getenv("DTI_RUN_ARTIFACT_DIR")
    if override:
        return Path(override).expanduser().resolve()
    return Path(__file__).resolve().parents[2] / "data" / "run_artifacts"


def save_run_artifact(
    *,
    route: str,
    request: Mapping[str, Any],
    response: Mapping[str, Any],
) -> dict[str, Any]:
    created_at = datetime.now(timezone.utc).isoformat()
    core = {
        "schema_version": SCHEMA_VERSION,
        "created_at_utc": created_at,
        "route": route,
        "request": dict(request),
        "response": dict(response),
        "reproducibility": {
            "runtime": _runtime_identity(),
            "request_replay": {"route": route, "payload": dict(request)},
            "scientific_boundary": "Single-point deterministic calculation; no posterior or evidence claim.",
        },
    }
    canonical = json.dumps(
        core,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    sha256 = hashlib.sha256(canonical).hexdigest()
    artifact = {**core, "artifact_sha256": sha256}

    directory = _artifact_directory()
    directory.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    filename = f"{stamp}_{route.replace('/', '_').strip('_')}_{sha256[:12]}.json"
    destination = directory / filename
    temporary = directory / f".{filename}.tmp"
    temporary.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2, allow_nan=False),
        encoding="utf-8",
    )
    temporary.replace(destination)
    return {
        "schema_version": SCHEMA_VERSION,
        "created_at_utc": created_at,
        "artifact_sha256": sha256,
        "path": str(destination),
    }


def list_run_artifacts(limit: int = 100) -> list[dict[str, Any]]:
    directory = _artifact_directory()
    if not directory.exists():
        return []
    records: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.json"), reverse=True)[:limit]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        records.append(
            {
                "path": str(path),
                "route": payload.get("route"),
                "created_at_utc": payload.get("created_at_utc"),
                "artifact_sha256": payload.get("artifact_sha256"),
                "status": payload.get("response", {}).get("status"),
            }
        )
    return records
