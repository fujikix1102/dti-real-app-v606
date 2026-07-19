"""Pure functions for the Hubble Consistency Engine.

Local-ladder entries are published Gaussian summaries used as comparison
coordinates.  They are deliberately kept outside the backend joint likelihood
because they overlap the Pantheon+/SH0ES supernova compilation.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping


DEFAULT_CONTRACT_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "research"
    / "hubble_ladder_anchors.json"
)


def load_anchor_contract(path: Path | None = None) -> dict[str, Any]:
    contract_path = path or DEFAULT_CONTRACT_PATH
    payload = json.loads(contract_path.read_text(encoding="utf-8"))
    validate_anchor_contract(payload)
    payload["contract_sha256"] = hashlib.sha256(contract_path.read_bytes()).hexdigest()
    return payload


def validate_anchor_contract(payload: Mapping[str, Any]) -> None:
    if payload.get("schema_version") != "hubble-ladder-summary-contract-v1":
        raise ValueError("unsupported Hubble ladder contract schema")
    anchors = payload.get("anchors")
    if not isinstance(anchors, list) or not anchors:
        raise ValueError("Hubble ladder contract requires anchors")
    identifiers: set[str] = set()
    for anchor in anchors:
        if not isinstance(anchor, Mapping):
            raise ValueError("anchor rows must be mappings")
        identifier = str(anchor.get("id", ""))
        if not identifier or identifier in identifiers:
            raise ValueError("anchor identifiers must be unique and non-empty")
        identifiers.add(identifier)
        h0 = float(anchor["H0"])
        sigma = float(anchor["sigma_total"])
        if not math.isfinite(h0) or not math.isfinite(sigma) or sigma <= 0.0:
            raise ValueError("anchor H0 and sigma_total must be finite and positive")
        if anchor.get("joint_use_allowed") is not False:
            raise ValueError("summary anchors must be comparison-only")


def anchor_by_id(contract: Mapping[str, Any], identifier: str) -> Mapping[str, Any]:
    for anchor in contract.get("anchors", []):
        if isinstance(anchor, Mapping) and anchor.get("id") == identifier:
            return anchor
    raise KeyError(identifier)


def anchor_diagnostic(h0: float, anchor: Mapping[str, Any]) -> dict[str, float | str]:
    model_h0 = float(h0)
    observed = float(anchor["H0"])
    sigma = float(anchor["sigma_total"])
    residual = model_h0 - observed
    pull = residual / sigma
    absolute_pull = abs(pull)
    if absolute_pull < 1.0:
        band = "within_1_sigma"
    elif absolute_pull < 2.0:
        band = "between_1_and_2_sigma"
    elif absolute_pull < 3.0:
        band = "between_2_and_3_sigma"
    else:
        band = "beyond_3_sigma"
    return {
        "model_H0": model_h0,
        "anchor_H0": observed,
        "sigma_total": sigma,
        "residual": residual,
        "pull_sigma": pull,
        "chi2_summary_coordinate": pull * pull,
        "band": band,
    }


COMPONENT_SPECS = (
    ("DESI DR2 BAO", "desi_dr2_bao", "chi2"),
    ("Planck 2018", "planck_2018", "chi2_effective"),
    ("Pantheon+ relative SN", "pantheon_plus", "chi2"),
)


def likelihood_component_rows(response: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, response_key, chi2_key in COMPONENT_SPECS:
        component = response.get(response_key, {})
        if not isinstance(component, Mapping):
            component = {}
        value = component.get(chi2_key)
        try:
            chi2 = float(value)
        except (TypeError, ValueError):
            chi2 = None
        rows.append({
            "dataset": label,
            "status": component.get("status", "unavailable"),
            "chi2": chi2,
            "independence_role": "backend_joint_component",
        })
    return rows


def comparison_rows(
    previous_response: Mapping[str, Any],
    current_response: Mapping[str, Any],
    previous_h0: float,
    current_h0: float,
    anchor: Mapping[str, Any],
) -> list[dict[str, Any]]:
    old_by_name = {row["dataset"]: row for row in likelihood_component_rows(previous_response)}
    new_by_name = {row["dataset"]: row for row in likelihood_component_rows(current_response)}
    rows: list[dict[str, Any]] = []
    for label, _, _ in COMPONENT_SPECS:
        old = old_by_name[label].get("chi2")
        new = new_by_name[label].get("chi2")
        if old is None or new is None:
            continue
        rows.append({
            "rail": label,
            "previous_chi2": float(old),
            "current_chi2": float(new),
            "delta_chi2": float(new) - float(old),
            "combination": "independent backend component",
        })
    old_anchor = anchor_diagnostic(previous_h0, anchor)["chi2_summary_coordinate"]
    new_anchor = anchor_diagnostic(current_h0, anchor)["chi2_summary_coordinate"]
    rows.append({
        "rail": str(anchor["label"]),
        "previous_chi2": float(old_anchor),
        "current_chi2": float(new_anchor),
        "delta_chi2": float(new_anchor) - float(old_anchor),
        "combination": "comparison only — overlaps Pantheon+",
    })
    return rows


def tradeoff_classification(rows: list[Mapping[str, Any]], tolerance: float = 1e-9) -> str:
    deltas = [float(row["delta_chi2"]) for row in rows]
    improvements = sum(delta < -tolerance for delta in deltas)
    deteriorations = sum(delta > tolerance for delta in deltas)
    if improvements and not deteriorations:
        return "PARETO_IMPROVEMENT"
    if deteriorations and not improvements:
        return "PARETO_DETERIORATION"
    if not improvements and not deteriorations:
        return "NO_MATERIAL_CHANGE"
    return "CROSS_DATASET_TRADE_OFF"
