from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping


REQUIRED_COLUMNS = (
    "Model ID",
    "H0",
    "f_EDE",
    "omega_cdm",
    "omega_b",
    "sigma8",
    "S8",
    "Profile role",
)

DIRECT_PARAMETER_FIELDS = (
    "H0",
    "omega_b",
    "omega_cdm",
    "f_EDE",
)

REFERENCE_OUTPUT_FIELDS = (
    "sigma8",
    "S8",
)

OPTIONAL_UNBOUND_FIELDS = (
    "z_c",
)


class V606ProfileAdapterError(ValueError):
    pass


@dataclass(frozen=True)
class V606Profile:
    profile_id: str
    category: str
    parameters: Mapping[str, str]
    reference_outputs: Mapping[str, str]
    optional_unbound: tuple[str, ...]
    source_row: int

    def parameter_payload(self) -> dict[str, str]:
        return dict(self.parameters)

    def reference_payload(self) -> dict[str, str]:
        return dict(self.reference_outputs)


@dataclass(frozen=True)
class V606ProfileLibrary:
    source_path: str
    source_sha256: str
    profiles: tuple[V606Profile, ...]

    def by_id(self, profile_id: str) -> V606Profile:
        for profile in self.profiles:
            if profile.profile_id == profile_id:
                return profile
        raise KeyError(profile_id)

    def categories(self) -> tuple[str, ...]:
        return tuple(sorted({profile.category for profile in self.profiles}))

    def profile_ids(self) -> tuple[str, ...]:
        return tuple(profile.profile_id for profile in self.profiles)


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_header(fieldnames: Iterable[str] | None) -> tuple[str, ...]:
    if fieldnames is None:
        raise V606ProfileAdapterError("TSV header is missing")

    actual = tuple(fieldnames)
    missing = [field for field in REQUIRED_COLUMNS if field not in actual]

    if missing:
        raise V606ProfileAdapterError(
            "missing required columns: " + ", ".join(missing)
        )

    return actual


def _require_value(row: Mapping[str, str], field: str, source_row: int) -> str:
    value = row.get(field)

    if value is None:
        raise V606ProfileAdapterError(
            f"row {source_row}: missing field {field}"
        )

    value = value.strip()

    if value == "":
        raise V606ProfileAdapterError(
            f"row {source_row}: empty field {field}"
        )

    return value


def _adapt_row(row: Mapping[str, str], source_row: int) -> V606Profile:
    profile_id = _require_value(row, "Model ID", source_row)
    category = _require_value(row, "Profile role", source_row)

    parameters = {
        field: _require_value(row, field, source_row)
        for field in DIRECT_PARAMETER_FIELDS
    }

    reference_outputs = {
        field: _require_value(row, field, source_row)
        for field in REFERENCE_OUTPUT_FIELDS
    }

    return V606Profile(
        profile_id=profile_id,
        category=category,
        parameters=parameters,
        reference_outputs=reference_outputs,
        optional_unbound=OPTIONAL_UNBOUND_FIELDS,
        source_row=source_row,
    )


def load_v606_profile_library(
    path: str | Path,
    *,
    expected_sha256: str | None = None,
    expected_count: int | None = None,
) -> V606ProfileLibrary:
    source = Path(path)

    if not source.is_file():
        raise FileNotFoundError(source)

    actual_sha256 = sha256_file(source)

    if expected_sha256 is not None and actual_sha256 != expected_sha256:
        raise V606ProfileAdapterError(
            f"SHA256 mismatch: expected {expected_sha256}, got {actual_sha256}"
        )

    profiles: list[V606Profile] = []
    seen_ids: set[str] = set()

    with source.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        _validate_header(reader.fieldnames)

        for source_row, row in enumerate(reader, start=2):
            profile = _adapt_row(row, source_row)

            if profile.profile_id in seen_ids:
                raise V606ProfileAdapterError(
                    f"duplicate Model ID: {profile.profile_id}"
                )

            seen_ids.add(profile.profile_id)
            profiles.append(profile)

    if expected_count is not None and len(profiles) != expected_count:
        raise V606ProfileAdapterError(
            f"profile count mismatch: expected {expected_count}, got {len(profiles)}"
        )

    return V606ProfileLibrary(
        source_path=str(source),
        source_sha256=actual_sha256,
        profiles=tuple(profiles),
    )
