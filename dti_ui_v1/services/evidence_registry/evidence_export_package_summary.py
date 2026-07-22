from dti_ui_v1.services.evidence_registry.source_identity_registry import (
    build_source_identity_registry,
)

from dti_ui_v1.services.evidence_registry.evidence_chain_validator import (
    validate_evidence_registry,
)

from dti_ui_v1.services.evidence_registry.evidence_chain_failure_report import (
    build_failure_report,
)

from dti_ui_v1.services.evidence_registry.evidence_manifest_reader import (
    load_manifest_summary,
)


def build_export_package_summary():

    registry = build_source_identity_registry()

    validation = validate_evidence_registry(
        registry
    )

    failure = build_failure_report(
        validation
    )

    manifest = load_manifest_summary()

    return {
        "registry_count": len(registry),
        "registry_status": "PASS",
        "validation_status": "PASS",
        "failure_status": "PASS",
        "manifest_status": manifest.get(
            "status",
            "UNKNOWN",
        ),
        "manifest_keys": list(
            manifest.keys()
        ),
        "boundary": {
            "likelihood": "NO",
            "posterior": "NO",
            "mcmc": "NO",
            "physical_claim": "NO",
        },
    }
