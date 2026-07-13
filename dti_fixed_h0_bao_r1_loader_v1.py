"""
DTI fixed-H0 BAO R1 static asset loader V1.

DESIGN-ONLY REFERENCE IMPLEMENTATION.

This file is not installed into the app repository by this gate.
It performs static local reads only. It must never call a backend,
API, optimizer, CLASS/AxiCLASS, sampler, or likelihood runtime.
"""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ASSET_SCHEMA_VERSION = "FIXED_H0_BAO_R1_APP_ASSET_V1"
ASSET_DIR_RELATIVE = Path("assets/fixed_h0_bao_r1/v1")

POINTS_NAME = "fixed_h0_bao_r1_27_point_record_v1.tsv"
SUMMARY_NAME = "fixed_h0_bao_r1_summary_v1.json"
REPEATABILITY_NAME = "fixed_h0_bao_r1_repeatability_v1.tsv"
EXTENSION_NAME = "fixed_h0_bao_r1_extension_82_85_v1.tsv"
CLAIMS_NAME = "fixed_h0_bao_r1_claim_boundary_v1.tsv"
PROVENANCE_NAME = "fixed_h0_bao_r1_provenance_v1.tsv"
PROFILE_DESIGN_NAME = "fixed_h0_bao_r1_profile_grid_design_v1.tsv"
MANIFEST_NAME = "fixed_h0_bao_r1_asset_manifest_v1.tsv"

EXPECTED_POINT_COLUMNS = [
    "record_index",
    "target_id",
    "H0",
    "omega_b",
    "omega_cdm",
    "chi2",
    "loglike",
    "rdrag_Mpc",
    "delta_chi2_from_recorded_minimum",
    "optimizer_success",
    "classification",
    "source_class",
    "is_recorded_minimum",
    "is_recorded_upper_endpoint",
    "claim_scope",
]


class FixedH0BAOAssetError(RuntimeError):
    pass


@dataclass(frozen=True)
class FixedH0BAOAssets:
    summary: dict[str, Any]
    points: list[dict[str, Any]]
    repeatability: list[dict[str, str]]
    extension: list[dict[str, str]]
    claims: list[dict[str, str]]
    provenance: list[dict[str, str]]
    profile_design: list[dict[str, str]]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _load_manifest(asset_dir: Path) -> dict[str, dict[str, str]]:
    rows = _read_tsv(asset_dir / MANIFEST_NAME)

    manifest = {
        row["filename"]: row
        for row in rows
    }

    required = {
        POINTS_NAME,
        SUMMARY_NAME,
        REPEATABILITY_NAME,
        EXTENSION_NAME,
        CLAIMS_NAME,
        PROVENANCE_NAME,
        PROFILE_DESIGN_NAME,
    }

    missing = sorted(required - set(manifest))

    if missing:
        raise FixedH0BAOAssetError(
            f"manifest missing assets: {missing}"
        )

    return manifest


def _verify_hashes(
    asset_dir: Path,
    manifest: dict[str, dict[str, str]],
) -> None:
    for filename, row in manifest.items():
        path = asset_dir / filename

        if not path.is_file():
            raise FixedH0BAOAssetError(
                f"asset missing: {path}"
            )

        actual = _sha256(path)
        expected = row["sha256"]

        if actual != expected:
            raise FixedH0BAOAssetError(
                f"asset hash mismatch: {filename}"
            )


def _parse_points(path: Path) -> list[dict[str, Any]]:
    raw = _read_tsv(path)

    if len(raw) != 27:
        raise FixedH0BAOAssetError(
            f"point count={len(raw)}"
        )

    if list(raw[0].keys()) != EXPECTED_POINT_COLUMNS:
        raise FixedH0BAOAssetError(
            "point schema mismatch"
        )

    points: list[dict[str, Any]] = []

    for row in raw:
        point = dict(row)

        point["record_index"] = int(row["record_index"])

        for key in (
            "H0",
            "omega_b",
            "omega_cdm",
            "chi2",
            "loglike",
            "rdrag_Mpc",
            "delta_chi2_from_recorded_minimum",
        ):
            point[key] = float(row[key])

        points.append(point)

    h0 = [row["H0"] for row in points]
    chi2 = [row["chi2"] for row in points]

    if h0 != sorted(h0) or len(set(h0)) != len(h0):
        raise FixedH0BAOAssetError(
            "H0 order or uniqueness failure"
        )

    if h0[0] != 59.5 or h0[-1] != 85.0:
        raise FixedH0BAOAssetError(
            "H0 endpoint mismatch"
        )

    if not all(
        right < left
        for left, right in zip(chi2[:-1], chi2[1:])
    ):
        raise FixedH0BAOAssetError(
            "chi2 monotonicity failure"
        )

    recorded_minimum = [
        row
        for row in points
        if row["is_recorded_minimum"] == "YES"
    ]

    upper_endpoint = [
        row
        for row in points
        if row["is_recorded_upper_endpoint"] == "YES"
    ]

    if len(recorded_minimum) != 1:
        raise FixedH0BAOAssetError(
            "recorded minimum marker count failure"
        )

    if len(upper_endpoint) != 1:
        raise FixedH0BAOAssetError(
            "upper endpoint marker count failure"
        )

    if recorded_minimum[0]["H0"] != 85.0:
        raise FixedH0BAOAssetError(
            "recorded minimum H0 mismatch"
        )

    if upper_endpoint[0]["H0"] != 85.0:
        raise FixedH0BAOAssetError(
            "upper endpoint H0 mismatch"
        )

    return points


def load_fixed_h0_bao_r1_assets(
    app_root: Path,
) -> FixedH0BAOAssets:
    asset_dir = app_root / ASSET_DIR_RELATIVE

    manifest = _load_manifest(asset_dir)
    _verify_hashes(asset_dir, manifest)

    summary = json.loads(
        (asset_dir / SUMMARY_NAME).read_text(encoding="utf-8")
    )

    if summary.get("schema_version") != ASSET_SCHEMA_VERSION:
        raise FixedH0BAOAssetError(
            "summary schema version mismatch"
        )

    points = _parse_points(asset_dir / POINTS_NAME)

    return FixedH0BAOAssets(
        summary=summary,
        points=points,
        repeatability=_read_tsv(asset_dir / REPEATABILITY_NAME),
        extension=_read_tsv(asset_dir / EXTENSION_NAME),
        claims=_read_tsv(asset_dir / CLAIMS_NAME),
        provenance=_read_tsv(asset_dir / PROVENANCE_NAME),
        profile_design=_read_tsv(asset_dir / PROFILE_DESIGN_NAME),
    )
