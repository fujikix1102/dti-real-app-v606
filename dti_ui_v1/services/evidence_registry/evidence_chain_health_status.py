from dti_ui_v1.services.evidence_registry.source_identity_registry import (
    build_source_identity_registry,
)

from dti_ui_v1.services.evidence_registry.evidence_chain_validator import (
    validate_evidence_registry,
)

from dti_ui_v1.services.evidence_registry.evidence_chain_freeze_diff_guard import (
    build_diff_guard,
)

from dti_ui_v1.services.evidence_registry.evidence_chain_freeze_alert_router import (
    build_freeze_alerts,
)

from dti_ui_v1.services.evidence_registry.evidence_chain_freeze_reader import (
    load_freeze_record,
)


def build_health_status():

    registry = build_source_identity_registry()

    validation = validate_evidence_registry(
        registry
    )

    guard = build_diff_guard()

    alerts = build_freeze_alerts(
        guard
    )

    freeze = load_freeze_record()


    return {

        "freeze_status":
            freeze.get(
                "status",
                "UNKNOWN"
            ),

        "hash_status":
            guard.get(
                "hash_status"
            ),

        "guard_status":
            guard.get(
                "guard_status"
            ),

        "alert_count":
            alerts.get(
                "alert_count"
            ),

        "review_required":
            alerts.get(
                "review_required"
            ),

        "registry_count":
            len(registry),

        "validation_status":
            "PASS"
            if all(
                x["verification_status"] == "PASS"
                for x in validation.values()
            )
            else "FAIL",

        "timeline_count":
            guard.get(
                "timeline_count"
            ),

        "integrity_score":
            guard.get(
                "integrity_score"
            ),

        "overall":
            "PASS"
            if guard.get("guard_status") == "PASS"
            else "FAIL",

    }
