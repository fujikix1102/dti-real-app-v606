from pathlib import Path

from dti_ui_v1.services.evidence_registry.manifest_selector import (
    load_manifest,
    resolve_asset
)

from dti_ui_v1.services.gtds_profile_validator import validate_profile

from dti_ui_v1.services.gtds_bic_scan import run_gtds_scan

from dti_ui_v1.services.evidence_registry.gtds_scan_pipeline import (
    save_scan_record
)


def execute_manifest_scan(manifest_name):

    manifest = load_manifest(
        manifest_name
    )

    asset = resolve_asset(
        manifest
    )

    if asset is None:

        return {
            "status": "ERROR",
            "reason": "NO_ASSET"
        }


    validation = validate_profile(
        asset,
        Path(
            "data/research/evidence/dti_raw_profile"
        ) / manifest_name
    )


    if validation.get("status") != "PASS":

        return {
            "status": "VALIDATION_FAILED",
            "validation": validation
        }


    result = run_gtds_scan(
        asset
    )


    record = save_scan_record(
        asset,
        result
    )


    return {

        "status": "FINISHED",

        "manifest":
            manifest_name,

        "asset":
            asset,

        "validation":
            validation,

        "gtds":
            result,

        "record":
            str(record)
    }
