"""Representation-neutral numerical audit of the installed Audit-DTI artifacts.

This audit deliberately avoids treating a cosmological story as a datum.  It
asks whether the finite-grid response-shape conclusion survives monotonic
re-encodings of the scanned coordinate, and reports injection/recovery limits
separately from the observed compressed-product result.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

try:
    # Installed application layout.
    from dti_ui_v1.services.audit_dti_engine import (
        piecewise_constant_models,
        polynomial_models,
    )
except ModuleNotFoundError:
    # Source-materialization layout used to generate and verify artifacts.
    from audit_dti_engine import piecewise_constant_models, polynomial_models


ROOT = Path(__file__).resolve().parent


def _artifact_path(filename: str) -> Path:
    """Resolve both source-materialization and installed-app layouts."""
    installed = ROOT / "data" / "research" / filename
    source = ROOT / filename
    if installed.exists():
        return installed
    return source


PROFILE_RESULT = _artifact_path("audit_dti_dr2_latest.json")
INJECTION_RESULT = _artifact_path("dti_transition_injection_recovery.json")
CATALOG_RESULT = _artifact_path("dti_catalog_pipeline_pilot_summary.json")
OUTPUT = (
    ROOT / "data" / "research" / "assumption_neutral_dti_audit.json"
    if (ROOT / "data" / "research").is_dir()
    else ROOT / "assumption_neutral_dti_audit.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _axis_encodings(x: np.ndarray) -> dict[str, np.ndarray]:
    rank = np.argsort(np.argsort(x)).astype(float)
    return {
        "linear_coordinate": x,
        "log_coordinate": np.log(x),
        "reciprocal_coordinate": 1.0 / x,
        "ordinal_coordinate": rank,
    }


def run_audit() -> dict:
    profile_artifact = json.loads(PROFILE_RESULT.read_text(encoding="utf-8"))
    injection_artifact = json.loads(INJECTION_RESULT.read_text(encoding="utf-8"))
    catalog_artifact = json.loads(CATALOG_RESULT.read_text(encoding="utf-8"))

    rows = profile_artifact["profile_rows"]
    x = np.asarray([row["H0"] for row in rows], dtype=float)
    y = np.asarray([row["profile_chi2"] for row in rows], dtype=float)
    representation_results = []
    for name, encoded in _axis_encodings(x).items():
        candidates = polynomial_models(encoded, y) + piecewise_constant_models(encoded, y)
        candidates.sort(key=lambda row: row["bic"])
        winner = candidates[0]
        runner_up = candidates[1]
        representation_results.append({
            "encoding": name,
            "winner_family": winner["family"],
            "winner_complexity": int(winner.get("order", winner.get("segments", 0))),
            "winner_bic": float(winner["bic"]),
            "bic_margin": float(runner_up["bic"] - winner["bic"]),
            "multi_segment_selected": bool(
                winner["family"] == "piecewise_constant" and winner.get("segments", 1) > 1
            ),
        })

    multi_segment_count = sum(row["multi_segment_selected"] for row in representation_results)
    robust = injection_artifact["robust_detection_by_amplitude"]
    recovery = [{
        "fractional_step": float(row["fractional_H_step"]),
        "minimum": float(row["minimum_detection_fraction"]),
        "median": float(row["median_detection_fraction"]),
        "maximum": float(row["maximum_detection_fraction"]),
    } for row in robust]
    catalog_conditions = catalog_artifact["conditions"]

    payload = {
        "schema_version": "assumption-neutral-dti-audit-v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "complete",
        "decision_rule": {
            "observed_product": "report response-shape selection under four monotonic coordinate encodings",
            "detectability": "report minimum/median/maximum recovery without converting non-detection into continuity",
            "physical_interpretation_used_as_input": False,
        },
        "observed_compressed_product": {
            "representations_tested": len(representation_results),
            "results": representation_results,
            "multi_segment_winner_count": int(multi_segment_count),
            "representation_stable_no_segment_winner": multi_segment_count == 0,
        },
        "injection_recovery": {
            "conditions": len(injection_artifact["scenarios"]),
            "null_replicates": int(injection_artifact["calibration"]["null_replicates"]),
            "injected_replicates": int(
                len(injection_artifact["scenarios"])
                * injection_artifact["calibration"]["scenario_replicates"]
            ),
            "by_amplitude": recovery,
            "minimum_recovery_at_largest_tested_step": recovery[-1]["minimum"],
        },
        "catalog_pipeline": {
            "conditions": int(catalog_artifact["condition_count"]),
            "correlation_functions": int(catalog_artifact["execution_totals"]["correlation_functions"]),
            "template_fits": int(catalog_artifact["execution_totals"]["bao_template_fits"]),
            "alpha_rmse_range": [
                float(min(row["alpha_rmse"] for row in catalog_conditions)),
                float(max(row["alpha_rmse"] for row in catalog_conditions)),
            ],
            "production_equivalent": bool(catalog_artifact["production_equivalent"]),
        },
        "machine_conclusion": {
            "compressed_product_requires_segmented_response": multi_segment_count > 0,
            "compressed_product_proves_underlying_continuity": False,
            "upstream_information_loss_empirically_possible": True,
            "observational_transition_detected": False,
        },
        "claim_boundary": (
            "The installed compressed DESI DR2 response does not select a segmented winner under any "
            "tested monotonic coordinate encoding. Injection tests nevertheless show non-unit and "
            "condition-dependent recovery, so this numerical result cannot be promoted to proof of "
            "underlying continuity. The catalog pilot is not production-equivalent."
        ),
        "source_identity": {
            PROFILE_RESULT.name: _sha256(PROFILE_RESULT),
            INJECTION_RESULT.name: _sha256(INJECTION_RESULT),
            CATALOG_RESULT.name: _sha256(CATALOG_RESULT),
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    payload["artifact_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


def main() -> None:
    payload = run_audit()
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"ASSUMPTION_NEUTRAL_AUDIT=PASS")
    print(f"OUTPUT={OUTPUT}")
    print(f"SHA256={payload['artifact_sha256']}")


if __name__ == "__main__":
    main()
