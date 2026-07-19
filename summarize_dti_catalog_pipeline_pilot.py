"""Aggregate executed catalog-pipeline pilot conditions into research artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUTS = (
    ROOT / "dti_catalog_pipeline_pilot_amp005.json",
    ROOT / "dti_catalog_pipeline_pilot.json",
    ROOT / "dti_catalog_pipeline_pilot_amp020.json",
)
OUTPUT_PATH = ROOT / "dti_catalog_pipeline_pilot_summary.json"
CSV_PATH = ROOT / "dti_catalog_pipeline_pilot_summary.csv"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize(
    inputs: tuple[Path, ...], output_path: Path = OUTPUT_PATH, csv_path: Path = CSV_PATH
) -> dict[str, Any]:
    conditions: list[dict[str, Any]] = []
    total_counts = {
        "paired_catalogs": 0,
        "data_objects_processed": 0,
        "random_objects_processed": 0,
        "correlation_functions": 0,
        "bao_template_fits": 0,
    }
    sources: list[dict[str, str]] = []
    for path in inputs:
        result = json.loads(path.read_text(encoding="utf-8"))
        if result["status"] != "complete":
            raise ValueError(f"incomplete pilot artifact: {path}")
        if result["production_equivalent"] is not False:
            raise ValueError(f"pilot artifact mislabels production status: {path}")
        injection = result["injection"]
        recovery = result["recovery_summary"]
        compression = result["compression"]
        qso = next(row for row in result["tracers"] if row["tracer"] == "QSO")
        lya = next(row for row in result["tracers"] if row["tracer"] == "LYA")
        conditions.append(
            {
                "fractional_H_step": injection["fractional_H_step"],
                "z_transition": injection["z_transition"],
                "width": injection["width"],
                "alpha_rmse": recovery["alpha_rmse"],
                "alpha_maximum_absolute_error": recovery[
                    "alpha_maximum_absolute_error"
                ],
                "compressed_relative_rmse": compression["relative_rmse"],
                "compressed_maximum_absolute_relative_error": compression[
                    "maximum_absolute_relative_error"
                ],
                "QSO_target_alpha_parallel": qso["target_alpha_parallel"],
                "QSO_recovered_alpha_parallel": qso[
                    "recovered_post_alpha_parallel"
                ],
                "QSO_alpha_parallel_error": qso["post_error_alpha_parallel"],
                "LYA_target_alpha_parallel": lya["target_alpha_parallel"],
                "LYA_recovered_alpha_parallel": lya[
                    "recovered_post_alpha_parallel"
                ],
                "LYA_alpha_parallel_error": lya["post_error_alpha_parallel"],
            }
        )
        for key in total_counts:
            total_counts[key] += int(result["execution_counts"][key])
        sources.append({"path": str(path), "sha256": _sha256(path)})

    conditions.sort(key=lambda row: row["fractional_H_step"])
    summary = {
        "schema_version": "dti-catalog-pipeline-pilot-summary-v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "complete",
        "production_equivalent": False,
        "condition_count": len(conditions),
        "execution_totals": total_counts,
        "conditions": conditions,
        "source_artifacts": sources,
        "result": (
            "All catalog-level stage boundaries executed for 5%, 10%, and 20% permanent H(z) "
            "steps. Recovery is incomplete and tracer-dependent; QSO radial recovery remains a "
            "blind spot in this synthetic survey-shaped pilot."
        ),
        "claim_boundary": (
            "This aggregate summarizes deterministic synthetic-catalog controls. It is not the "
            "official DESI mock ensemble, production reconstruction, official covariance, or an "
            "observational transition probability."
        ),
    }
    output_path.write_text(json.dumps(summary, indent=2, allow_nan=False), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(conditions[0]))
        writer.writeheader()
        writer.writerows(conditions)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="*", type=Path)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--csv-output", type=Path, default=CSV_PATH)
    arguments = parser.parse_args()
    paths = tuple(arguments.inputs) if arguments.inputs else DEFAULT_INPUTS
    result = summarize(paths, arguments.output, arguments.csv_output)
    print("DTI_CATALOG_PIPELINE_SUMMARY=PASS")
    print("CONDITIONS=" + str(result["condition_count"]))
    print("CORRELATION_FUNCTIONS=" + str(result["execution_totals"]["correlation_functions"]))
    print("BAO_TEMPLATE_FITS=" + str(result["execution_totals"]["bao_template_fits"]))

