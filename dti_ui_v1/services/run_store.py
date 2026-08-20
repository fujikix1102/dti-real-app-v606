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
STREAMLIT_RUNTIME_PREFIX = "/mount/src/"


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


def _is_streamlit_cloud_runtime(directory: Path) -> bool:
    directory_text = str(directory)
    return (
        directory_text == "/mount/src"
        or directory_text.startswith(STREAMLIT_RUNTIME_PREFIX)
        or os.getenv("STREAMLIT_SHARING_MODE") is not None
        or os.getenv("STREAMLIT_CLOUD") is not None
    )


def _storage_context(directory: Path) -> dict[str, Any]:
    is_streamlit_cloud = _is_streamlit_cloud_runtime(directory)
    persistence = (
        "ephemeral_streamlit_runtime"
        if is_streamlit_cloud
        else "local_or_configured_filesystem"
    )
    user_visible_notice = (
        "Streamlit Cloud runtime storage is ephemeral and separate from any "
        "local checkout. Download or copy the JSON before the app runtime is "
        "recycled if durable persistence has not been configured."
        if is_streamlit_cloud
        else "Artifacts are stored in this runtime's configured filesystem. "
        "Counts reflect this checkout or DTI_RUN_ARTIFACT_DIR only."
    )
    return {
        "artifact_directory": str(directory),
        "runtime_filesystem": (
            "streamlit_cloud"
            if is_streamlit_cloud
            else "local_or_configured"
        ),
        "persistence": persistence,
        "durable_persistence_available": not is_streamlit_cloud,
        "user_visible_notice": user_visible_notice,
    }


def get_run_artifact_store_status() -> dict[str, Any]:
    directory = _artifact_directory()
    existing_count = (
        len(list(directory.glob("*.json")))
        if directory.exists()
        else 0
    )
    return {
        **_storage_context(directory),
        "artifact_count": existing_count,
        "schema_version": SCHEMA_VERSION,
    }


def save_run_artifact(
    *,
    route: str,
    request: Mapping[str, Any],
    response: Mapping[str, Any],
) -> dict[str, Any]:
    created = datetime.now(timezone.utc)
    created_at = created.isoformat()
    directory = _artifact_directory()
    storage = _storage_context(directory)
    route_label = route.replace("/", "_").strip("_")
    stamp = created.strftime("%Y%m%dT%H%M%S.%fZ")
    run_id = f"{stamp}_{route_label}"
    core = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "created_at_utc": created_at,
        "route": route,
        "request": dict(request),
        "response": dict(response),
        "reproducibility": {
            "runtime": _runtime_identity(),
            "request_replay": {"route": route, "payload": dict(request)},
            "scientific_boundary": "Single-point deterministic calculation; no posterior or evidence claim.",
        },
        "storage": storage,
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

    directory.mkdir(parents=True, exist_ok=True)
    filename = f"{run_id}_{sha256[:12]}.json"
    destination = directory / filename
    temporary = directory / f".{filename}.tmp"
    temporary.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2, allow_nan=False),
        encoding="utf-8",
    )
    temporary.replace(destination)
    artifact_count = len(list(directory.glob("*.json")))
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "created_at_utc": created_at,
        "artifact_sha256": sha256,
        "path": str(destination),
        "artifact_directory": str(directory),
        "artifact_count": artifact_count,
        "storage": storage,
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
                "run_id": payload.get("run_id"),
                "path": str(path),
                "route": payload.get("route"),
                "created_at_utc": payload.get("created_at_utc"),
                "artifact_sha256": payload.get("artifact_sha256"),
                "status": payload.get("response", {}).get("status"),
                "H0": payload.get("request", {}).get("H0"),
                "A_DTI": payload.get("request", {}).get("A_DTI"),
                "f_EDE": payload.get("request", {}).get("f_EDE"),
                "z_c": payload.get("request", {}).get("z_c"),
                "runtime_store": payload.get("storage", {}).get("persistence"),
            }
        )
    return records


def list_run_artifact_paths(limit: int = 100) -> list[Path]:
    directory = _artifact_directory()
    if not directory.exists():
        return []
    return sorted(
        directory.glob("*.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )[:limit]


def load_run_artifact(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("run_artifact_root_must_be_mapping")
    return payload


def build_run_manifest(payload: Mapping[str, Any]) -> dict[str, Any]:
    request = payload.get("request", {})
    response = payload.get("response", {})
    reproducibility = payload.get("reproducibility", {})
    storage = payload.get("storage", {})
    if not isinstance(request, Mapping):
        request = {}
    if not isinstance(response, Mapping):
        response = {}
    if not isinstance(reproducibility, Mapping):
        reproducibility = {}
    if not isinstance(storage, Mapping):
        storage = {}
    return {
        "manifest_schema": "dti-run-manifest-v1",
        "run_id": payload.get("run_id"),
        "created_at_utc": payload.get("created_at_utc"),
        "route": payload.get("route"),
        "artifact_sha256": payload.get("artifact_sha256"),
        "status": response.get("status"),
        "parameters": {
            key: request.get(key)
            for key in ("H0", "A_DTI", "omega_b", "omega_cdm", "z_c", "f_EDE")
            if key in request
        },
        "result_summary": {
            key: response.get(key)
            for key in (
                "engine",
                "model_loglike",
                "model_chi2",
                "rdrag_Mpc",
            )
            if key in response
        },
        "runtime": reproducibility.get("runtime", {}),
        "request_replay": reproducibility.get("request_replay", {}),
        "storage": storage,
        "boundary": reproducibility.get(
            "scientific_boundary",
            "Single-point deterministic calculation; no posterior or evidence claim.",
        ),
    }


def build_notebook_export(payload: Mapping[str, Any]) -> str:
    manifest = build_run_manifest(payload)
    parameters = manifest.get("parameters", {})
    lines = [
        "# DTI PERFECT FIT run notebook",
        "",
        f"- run_id: {manifest.get('run_id')}",
        f"- created_at_utc: {manifest.get('created_at_utc')}",
        f"- route: {manifest.get('route')}",
        f"- status: {manifest.get('status')}",
        f"- artifact_sha256: {manifest.get('artifact_sha256')}",
        "",
        "## Parameters",
        "",
    ]
    if isinstance(parameters, Mapping) and parameters:
        for key, value in parameters.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- No editable parameters recorded.")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            str(manifest.get("boundary")),
            "",
            "## Reproduction",
            "",
            "Replay the request using the route and payload recorded in the run manifest.",
            "This export does not contain posterior samples, MCMC output, or model-comparison claims.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_reproduction_package(payload: Mapping[str, Any]) -> dict[str, str]:
    manifest = build_run_manifest(payload)
    run_id = str(manifest.get("run_id") or "dti_run")
    return {
        f"{run_id}_manifest.json": json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        ),
        f"{run_id}_notebook.md": build_notebook_export(payload),
        f"{run_id}_artifact.json": json.dumps(
            dict(payload),
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
            default=str,
        ),
    }
