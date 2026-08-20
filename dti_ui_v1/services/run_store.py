from __future__ import annotations

import hashlib
import hmac
import json
import os
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import quote
from xml.etree import ElementTree

import requests

SCHEMA_VERSION = "dti-run-artifact-v2"
STREAMLIT_RUNTIME_PREFIX = "/mount/src/"
DURABLE_ARTIFACT_DIR_ENV = "DTI_DURABLE_ARTIFACT_DIR"
EXTERNAL_STORAGE_BACKEND_ENV = "DTI_EXTERNAL_STORAGE_BACKEND"
R2_ACCOUNT_ID_ENV = "R2_ACCOUNT_ID"
R2_ACCESS_KEY_ID_ENV = "R2_ACCESS_KEY_ID"
R2_SECRET_ACCESS_KEY_ENV = "R2_SECRET_ACCESS_KEY"
R2_BUCKET_ENV = "R2_BUCKET"
R2_PREFIX_ENV = "R2_PREFIX"
R2_PUBLIC_BASE_URL_ENV = "R2_PUBLIC_BASE_URL"
PAGE_VIEW_COUNTER_SCHEMA_VERSION = "dti-r2-anonymous-page-view-counter-v1"


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


def _durable_artifact_directory() -> Path | None:
    configured = os.getenv(DURABLE_ARTIFACT_DIR_ENV)
    if not configured:
        return None
    return Path(configured).expanduser().resolve()


def _r2_config() -> dict[str, Any]:
    backend = os.getenv(EXTERNAL_STORAGE_BACKEND_ENV, "").strip().lower()
    account_id = os.getenv(R2_ACCOUNT_ID_ENV, "").strip()
    access_key_id = os.getenv(R2_ACCESS_KEY_ID_ENV, "").strip()
    secret_access_key = os.getenv(R2_SECRET_ACCESS_KEY_ENV, "").strip()
    bucket = os.getenv(R2_BUCKET_ENV, "").strip()
    prefix = os.getenv(R2_PREFIX_ENV, "dti-perfect-fit").strip().strip("/")
    public_base_url = os.getenv(R2_PUBLIC_BASE_URL_ENV, "").strip().rstrip("/")
    configured = backend == "r2" and all(
        (account_id, access_key_id, secret_access_key, bucket)
    )
    return {
        "backend": backend or None,
        "configured": configured,
        "account_id": account_id,
        "access_key_id": access_key_id,
        "secret_access_key": secret_access_key,
        "bucket": bucket,
        "prefix": prefix,
        "public_base_url": public_base_url,
    }


def _external_storage_context() -> dict[str, Any]:
    r2 = _r2_config()
    if r2["backend"] == "r2":
        missing = [
            key
            for key, value in (
                (R2_ACCOUNT_ID_ENV, r2["account_id"]),
                (R2_ACCESS_KEY_ID_ENV, r2["access_key_id"]),
                (R2_SECRET_ACCESS_KEY_ENV, r2["secret_access_key"]),
                (R2_BUCKET_ENV, r2["bucket"]),
            )
            if not value
        ]
        return {
            "backend": "r2",
            "configured": r2["configured"],
            "bucket": r2["bucket"] or None,
            "prefix": r2["prefix"],
            "public_base_url": r2["public_base_url"] or None,
            "missing": missing,
        }
    return {
        "backend": None,
        "configured": False,
        "bucket": None,
        "prefix": None,
        "public_base_url": None,
        "missing": [],
    }


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
    durable_directory = _durable_artifact_directory()
    durable_configured = durable_directory is not None
    persistence = (
        "durable_mirror_configured"
        if durable_configured
        else (
            "ephemeral_streamlit_runtime"
            if is_streamlit_cloud
            else "local_or_configured_filesystem"
        )
    )
    user_visible_notice = (
        f"Durable artifact mirror is configured at {durable_directory}. "
        "Artifacts are written to the runtime store and mirrored there."
        if durable_configured
        else (
        "Streamlit Cloud runtime storage is ephemeral and separate from any "
        "local checkout. Download or copy the JSON before the app runtime is "
        "recycled if durable persistence has not been configured."
        if is_streamlit_cloud
        else "Artifacts are stored in this runtime's configured filesystem. "
        "Counts reflect this checkout or DTI_RUN_ARTIFACT_DIR only."
        )
    )
    return {
        "artifact_directory": str(directory),
        "runtime_filesystem": (
            "streamlit_cloud"
            if is_streamlit_cloud
            else "local_or_configured"
        ),
        "persistence": persistence,
        "durable_persistence_available": durable_configured or not is_streamlit_cloud,
        "durable_mirror_configured": durable_configured,
        "durable_artifact_directory": str(durable_directory) if durable_directory else None,
        "external_storage": _external_storage_context(),
        "user_visible_notice": user_visible_notice,
    }


def _write_artifact_json(directory: Path, filename: str, artifact: Mapping[str, Any]) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / filename
    temporary = directory / f".{filename}.tmp"
    temporary.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2, allow_nan=False),
        encoding="utf-8",
    )
    temporary.replace(destination)
    return destination


def _signing_key(secret_access_key: str, date_stamp: str) -> bytes:
    key_date = hmac.new(
        ("AWS4" + secret_access_key).encode("utf-8"),
        date_stamp.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    key_region = hmac.new(key_date, b"auto", hashlib.sha256).digest()
    key_service = hmac.new(key_region, b"s3", hashlib.sha256).digest()
    return hmac.new(key_service, b"aws4_request", hashlib.sha256).digest()


def _r2_signed_request(
    method: str,
    key: str,
    *,
    now: datetime,
    body: bytes = b"",
    content_type: str = "application/json",
    query: Mapping[str, str] | None = None,
) -> requests.Response:
    config = _r2_config()
    if not config["configured"]:
        raise RuntimeError("r2_not_configured")

    payload_hash = hashlib.sha256(body).hexdigest()
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")
    host = f"{config['account_id']}.r2.cloudflarestorage.com"
    encoded_key = "/".join(quote(part, safe="") for part in key.split("/"))
    canonical_uri = f"/{quote(config['bucket'], safe='')}/{encoded_key}"
    query_items = sorted((query or {}).items())
    canonical_query = "&".join(
        f"{quote(str(key), safe='-_.~')}={quote(str(value), safe='-_.~')}"
        for key, value in query_items
    )
    endpoint = f"https://{host}{canonical_uri}"
    if canonical_query:
        endpoint = f"{endpoint}?{canonical_query}"
    signed_headers = "content-type;host;x-amz-content-sha256;x-amz-date"
    canonical_headers = (
        f"content-type:{content_type}\n"
        f"host:{host}\n"
        f"x-amz-content-sha256:{payload_hash}\n"
        f"x-amz-date:{amz_date}\n"
    )
    canonical_request = "\n".join(
        (
            method.upper(),
            canonical_uri,
            canonical_query,
            canonical_headers,
            signed_headers,
            payload_hash,
        )
    )
    credential_scope = f"{date_stamp}/auto/s3/aws4_request"
    string_to_sign = "\n".join(
        (
            "AWS4-HMAC-SHA256",
            amz_date,
            credential_scope,
            hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
        )
    )
    signature = hmac.new(
        _signing_key(config["secret_access_key"], date_stamp),
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    headers = {
        "Authorization": (
            "AWS4-HMAC-SHA256 "
            f"Credential={config['access_key_id']}/{credential_scope}, "
            f"SignedHeaders={signed_headers}, Signature={signature}"
        ),
        "Content-Type": content_type,
        "x-amz-content-sha256": payload_hash,
        "x-amz-date": amz_date,
    }
    return requests.request(method.upper(), endpoint, data=body, headers=headers, timeout=30)


def _r2_put_json(key: str, payload: Mapping[str, Any], *, now: datetime) -> dict[str, Any]:
    config = _r2_config()
    if not config["configured"]:
        return {"uploaded": False, "reason": "r2_not_configured", "key": key}

    body = json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        allow_nan=False,
        default=str,
    ).encode("utf-8")
    encoded_key = "/".join(quote(part, safe="") for part in key.split("/"))
    response = _r2_signed_request("PUT", key, now=now, body=body)
    response.raise_for_status()
    public_url = (
        f"{config['public_base_url']}/{encoded_key}"
        if config["public_base_url"]
        else None
    )
    return {
        "uploaded": True,
        "backend": "r2",
        "bucket": config["bucket"],
        "key": key,
        "public_url": public_url,
        "etag": response.headers.get("ETag"),
    }


def _r2_get_json(key: str, *, now: datetime) -> dict[str, Any] | None:
    response = _r2_signed_request("GET", key, now=now)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    payload = response.json()
    return payload if isinstance(payload, dict) else None


def _r2_list_artifact_keys(*, now: datetime, max_keys: int = 1000) -> list[str]:
    external = _external_storage_context()
    prefix = str(external.get("prefix") or "").strip("/")
    runs_prefix = f"{prefix}/runs/" if prefix else "runs/"
    response = _r2_signed_request(
        "GET",
        "",
        now=now,
        query={
            "list-type": "2",
            "prefix": runs_prefix,
            "max-keys": str(max_keys),
        },
    )
    response.raise_for_status()
    root = ElementTree.fromstring(response.text)
    keys: list[str] = []
    for key_node in root.findall(".//{*}Key"):
        key = key_node.text or ""
        if key.endswith("/artifact.json"):
            keys.append(key)
    return sorted(set(keys), reverse=True)


def _r2_run_index_entry(artifact: Mapping[str, Any], artifact_key: str) -> dict[str, Any]:
    request = artifact.get("request", {})
    response = artifact.get("response", {})
    if not isinstance(request, Mapping):
        request = {}
    if not isinstance(response, Mapping):
        response = {}
    return {
        "run_id": artifact.get("run_id"),
        "created_at_utc": artifact.get("created_at_utc"),
        "route": artifact.get("route"),
        "artifact_sha256": artifact.get("artifact_sha256"),
        "status": response.get("status"),
        "artifact_key": artifact_key,
        "H0": request.get("H0"),
        "A_DTI": request.get("A_DTI"),
        "f_EDE": request.get("f_EDE"),
        "z_c": request.get("z_c"),
    }


def _merge_r2_run_index(
    artifact: Mapping[str, Any],
    *,
    artifact_key: str,
    index_key: str,
    now: datetime,
    limit: int = 200,
) -> dict[str, Any]:
    current = _r2_get_json(index_key, now=now) or {}
    existing_runs = current.get("runs", [])
    if not isinstance(existing_runs, list):
        existing_runs = []
    entry = _r2_run_index_entry(artifact, artifact_key)
    merged: dict[str, dict[str, Any]] = {}
    for item in existing_runs:
        if isinstance(item, Mapping) and item.get("run_id"):
            merged[str(item["run_id"])] = dict(item)
    if entry.get("run_id"):
        merged[str(entry["run_id"])] = entry
    runs = sorted(
        merged.values(),
        key=lambda item: str(item.get("created_at_utc") or ""),
        reverse=True,
    )[:limit]
    return {
        "schema_version": "dti-r2-run-index-v1",
        "updated_at_utc": now.isoformat(),
        "run_count": len(runs),
        "runs": runs,
    }


def _r2_index_key() -> str:
    external = _external_storage_context()
    prefix = str(external.get("prefix") or "").strip("/")
    return f"{prefix}/index/runs_manifest.json" if prefix else "index/runs_manifest.json"


def _r2_metrics_key(date_label: str) -> str:
    external = _external_storage_context()
    prefix = str(external.get("prefix") or "").strip("/")
    return (
        f"{prefix}/metrics/page_views/{date_label}.json"
        if prefix
        else f"metrics/page_views/{date_label}.json"
    )


def _safe_metric_label(value: str) -> str:
    compact = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    return compact.strip("_")[:80] or "unknown"


def record_anonymous_page_view(
    page: str,
    *,
    app_commit: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    external = _external_storage_context()
    if not external["configured"] or external["backend"] != "r2":
        return {"configured": False, "recorded": False, "error": None}
    checked_at = now or datetime.now(timezone.utc)
    date_label = checked_at.strftime("%Y-%m-%d")
    key = _r2_metrics_key(date_label)
    page_label = _safe_metric_label(page)
    commit_label = _safe_metric_label(app_commit or "unknown")
    try:
        payload = _r2_get_json(key, now=checked_at) or {}
        if payload.get("schema_version") != PAGE_VIEW_COUNTER_SCHEMA_VERSION:
            payload = {
                "schema_version": PAGE_VIEW_COUNTER_SCHEMA_VERSION,
                "date": date_label,
                "updated_at_utc": checked_at.isoformat(),
                "total": 0,
                "pages": {},
                "commits": {},
                "privacy": {
                    "anonymous": True,
                    "stores_ip": False,
                    "stores_user_agent": False,
                    "stores_cookie": False,
                    "stores_session_id": False,
                },
            }
        pages = payload.get("pages")
        if not isinstance(pages, dict):
            pages = {}
            payload["pages"] = pages
        commits = payload.get("commits")
        if not isinstance(commits, dict):
            commits = {}
            payload["commits"] = commits
        payload["date"] = date_label
        payload["updated_at_utc"] = checked_at.isoformat()
        payload["total"] = int(payload.get("total") or 0) + 1
        pages[page_label] = int(pages.get(page_label) or 0) + 1
        commits[commit_label] = int(commits.get(commit_label) or 0) + 1
        upload = _r2_put_json(key, payload, now=checked_at)
    except Exception as exc:
        return {
            "configured": True,
            "recorded": False,
            "key": key,
            "error": str(exc),
        }
    return {
        "configured": True,
        "recorded": bool(upload.get("uploaded")),
        "key": key,
        "date": date_label,
        "page": page_label,
        "app_commit": commit_label,
        "error": None,
    }


def get_anonymous_page_view_summary(
    *,
    days: int = 7,
    now: datetime | None = None,
) -> dict[str, Any]:
    external = _external_storage_context()
    if not external["configured"] or external["backend"] != "r2":
        return {"configured": False, "days": [], "total": 0, "error": None}
    checked_at = now or datetime.now(timezone.utc)
    day_payloads: list[dict[str, Any]] = []
    total = 0
    pages: dict[str, int] = {}
    commits: dict[str, int] = {}
    errors: list[str] = []
    for offset in range(max(1, days)):
        date_label = (
            datetime.fromtimestamp(
                checked_at.timestamp() - offset * 86400,
                timezone.utc,
            ).strftime("%Y-%m-%d")
        )
        key = _r2_metrics_key(date_label)
        try:
            payload = _r2_get_json(key, now=checked_at)
        except Exception as exc:
            errors.append(f"{date_label}:{exc}")
            continue
        if not isinstance(payload, dict):
            continue
        count = int(payload.get("total") or 0)
        total += count
        for name, value in (payload.get("pages") or {}).items():
            pages[str(name)] = pages.get(str(name), 0) + int(value or 0)
        for name, value in (payload.get("commits") or {}).items():
            commits[str(name)] = commits.get(str(name), 0) + int(value or 0)
        day_payloads.append(
            {
                "date": date_label,
                "total": count,
                "key": key,
                "updated_at_utc": payload.get("updated_at_utc"),
            }
        )
    return {
        "schema_version": PAGE_VIEW_COUNTER_SCHEMA_VERSION,
        "configured": True,
        "days": day_payloads,
        "total": total,
        "pages": dict(sorted(pages.items())),
        "commits": dict(sorted(commits.items())),
        "error": "; ".join(errors) if errors else None,
        "privacy": {
            "anonymous": True,
            "stores_ip": False,
            "stores_user_agent": False,
            "stores_cookie": False,
            "stores_session_id": False,
        },
    }


def _r2_artifact_key_for_run(run_id: str) -> str:
    external = _external_storage_context()
    prefix = str(external.get("prefix") or "").strip("/")
    date_prefix = run_id[:8] if len(run_id) >= 8 else "unknown_date"
    key_prefix = (
        f"{prefix}/runs/{date_prefix}/{run_id}"
        if prefix
        else f"runs/{date_prefix}/{run_id}"
    )
    return f"{key_prefix}/artifact.json"


def _mirror_artifact_to_external_storage(
    artifact: Mapping[str, Any],
    *,
    created: datetime,
) -> dict[str, Any]:
    external = _external_storage_context()
    if not external["configured"]:
        return {"configured": False, "uploads": [], "error": None}
    if external["backend"] != "r2":
        return {
            "configured": False,
            "uploads": [],
            "error": f"unsupported_external_backend:{external['backend']}",
        }

    run_id = str(artifact.get("run_id") or "unknown_run")
    date_prefix = created.strftime("%Y%m%d")
    prefix = str(external.get("prefix") or "").strip("/")
    key_prefix = f"{prefix}/runs/{date_prefix}/{run_id}" if prefix else f"runs/{date_prefix}/{run_id}"
    artifact_key = f"{key_prefix}/artifact.json"
    latest_key = f"{prefix}/index/latest.json" if prefix else "index/latest.json"
    run_index_key = _r2_index_key()
    try:
        run_index = _merge_r2_run_index(
            artifact,
            artifact_key=artifact_key,
            index_key=run_index_key,
            now=created,
        )
        uploads = [
            _r2_put_json(artifact_key, artifact, now=created),
            _r2_put_json(latest_key, artifact, now=created),
            _r2_put_json(run_index_key, run_index, now=created),
        ]
    except Exception as exc:
        return {
            "configured": True,
            "backend": "r2",
            "bucket": external.get("bucket"),
            "uploads": [],
            "error": str(exc),
        }
    return {
        "configured": True,
        "backend": "r2",
        "bucket": external.get("bucket"),
        "uploads": uploads,
        "error": None,
    }


def get_external_run_index() -> dict[str, Any]:
    external = _external_storage_context()
    if not external["configured"] or external["backend"] != "r2":
        return {"configured": False, "runs": [], "error": None}
    index_key = _r2_index_key()
    try:
        payload = _r2_get_json(index_key, now=datetime.now(timezone.utc))
    except Exception as exc:
        return {
            "configured": True,
            "backend": "r2",
            "bucket": external.get("bucket"),
            "index_key": index_key,
            "runs": [],
            "error": str(exc),
        }
    if not isinstance(payload, dict):
        payload = {}
    runs = payload.get("runs", [])
    return {
        "configured": True,
        "backend": "r2",
        "bucket": external.get("bucket"),
        "index_key": index_key,
        "run_count": payload.get("run_count", len(runs) if isinstance(runs, list) else 0),
        "runs": runs if isinstance(runs, list) else [],
        "error": None,
    }


def load_external_run_artifact(artifact_key: str) -> dict[str, Any]:
    payload = _r2_get_json(artifact_key, now=datetime.now(timezone.utc))
    if not isinstance(payload, dict):
        raise ValueError("r2_artifact_root_must_be_mapping")
    return payload


def rebuild_external_run_index_from_runtime(limit: int = 200) -> dict[str, Any]:
    external = _external_storage_context()
    if not external["configured"] or external["backend"] != "r2":
        return {"configured": False, "uploaded": False, "run_count": 0, "error": None}
    now = datetime.now(timezone.utc)
    runs: list[dict[str, Any]] = []
    for path in list_run_artifact_paths(limit=limit):
        try:
            payload = load_run_artifact(path)
        except Exception:
            continue
        run_id = str(payload.get("run_id") or "")
        if not run_id:
            continue
        runs.append(_r2_run_index_entry(payload, _r2_artifact_key_for_run(run_id)))
    runs = sorted(
        runs,
        key=lambda item: str(item.get("created_at_utc") or ""),
        reverse=True,
    )[:limit]
    index_payload = {
        "schema_version": "dti-r2-run-index-v1",
        "updated_at_utc": now.isoformat(),
        "run_count": len(runs),
        "runs": runs,
    }
    index_key = _r2_index_key()
    try:
        upload = _r2_put_json(index_key, index_payload, now=now)
    except Exception as exc:
        return {
            "configured": True,
            "uploaded": False,
            "index_key": index_key,
            "run_count": len(runs),
            "error": str(exc),
        }
    return {
        "configured": True,
        "uploaded": bool(upload.get("uploaded")),
        "index_key": index_key,
        "run_count": len(runs),
        "error": None,
    }


def rebuild_external_run_index_from_remote(limit: int = 200) -> dict[str, Any]:
    external = _external_storage_context()
    if not external["configured"] or external["backend"] != "r2":
        return {
            "configured": False,
            "uploaded": False,
            "run_count": 0,
            "error": None,
        }
    now = datetime.now(timezone.utc)
    try:
        artifact_keys = _r2_list_artifact_keys(now=now, max_keys=limit)
    except Exception as exc:
        return {
            "configured": True,
            "uploaded": False,
            "run_count": 0,
            "error": str(exc),
        }
    runs: list[dict[str, Any]] = []
    for key in artifact_keys[:limit]:
        try:
            payload = load_external_run_artifact(key)
        except Exception:
            continue
        runs.append(_r2_run_index_entry(payload, key))
    runs = sorted(
        runs,
        key=lambda item: str(item.get("created_at_utc") or ""),
        reverse=True,
    )[:limit]
    index_payload = {
        "schema_version": "dti-r2-run-index-v1",
        "updated_at_utc": now.isoformat(),
        "run_count": len(runs),
        "runs": runs,
    }
    index_key = _r2_index_key()
    try:
        upload = _r2_put_json(index_key, index_payload, now=now)
    except Exception as exc:
        return {
            "configured": True,
            "uploaded": False,
            "index_key": index_key,
            "run_count": len(runs),
            "discovered_artifact_count": len(artifact_keys),
            "error": str(exc),
        }
    return {
        "configured": True,
        "uploaded": bool(upload.get("uploaded")),
        "index_key": index_key,
        "run_count": len(runs),
        "discovered_artifact_count": len(artifact_keys),
        "error": None,
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
    durable_directory = _durable_artifact_directory()
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

    filename = f"{run_id}_{sha256[:12]}.json"
    destination = _write_artifact_json(directory, filename, artifact)
    durable_destination = None
    if durable_directory is not None and durable_directory != directory:
        durable_destination = _write_artifact_json(durable_directory, filename, artifact)
    external_storage = _mirror_artifact_to_external_storage(artifact, created=created)
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
        "durable_path": str(durable_destination) if durable_destination else None,
        "external_storage": external_storage,
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
        "durable_storage": {
            "configured": bool(storage.get("durable_mirror_configured")),
            "artifact_directory": storage.get("durable_artifact_directory"),
            "persistence": storage.get("persistence"),
        },
        "external_storage": storage.get("external_storage", {}),
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
    readme = "\n".join(
        [
            "# DTI PERFECT FIT reproduction package",
            "",
            "This package contains the saved artifact, manifest, and notebook export.",
            "",
            "## Quick local inspection",
            "",
            "```bash",
            "python -m json.tool *_manifest.json",
            "python -m json.tool *_artifact.json",
            "```",
            "",
            "## Boundary",
            "",
            "This package does not contain posterior samples, MCMC output, or a model-ranking claim.",
            "Full backend replay requires a local CLASS/AxiCLASS environment matching the artifact manifest and backend contract.",
            "",
        ]
    )
    return {
        "README_REPRODUCTION.md": readme,
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
