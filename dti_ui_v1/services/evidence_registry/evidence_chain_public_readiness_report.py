from dti_ui_v1.services.evidence_registry.evidence_chain_health_status import (
    build_health_status,
)


def build_public_readiness_report():

    health = build_health_status()

    report = {

        "freeze_identity":
            health.get(
                "freeze_status"
            ),

        "hash_verification":
            health.get(
                "hash_status"
            ),

        "diff_guard":
            health.get(
                "guard_status"
            ),

        "alert_count":
            health.get(
                "alert_count"
            ),

        "registry_count":
            health.get(
                "registry_count"
            ),

        "validation_status":
            health.get(
                "validation_status"
            ),

        "timeline_count":
            health.get(
                "timeline_count"
            ),

        "integrity_score":
            health.get(
                "integrity_score"
            ),

        "reproducibility":
            "PASS"
            if health.get("overall") == "PASS"
            else "FAIL",

        "boundary":
            {
                "likelihood": "NO",
                "posterior": "NO",
                "mcmc": "NO",
                "physical_claim": "NO",
            },

    }


    report["public_readiness"] = (
        "READY"
        if (
            report["hash_verification"] == "PASS"
            and
            report["diff_guard"] == "PASS"
            and
            report["validation_status"] == "PASS"
        )
        else "BLOCKED"
    )


    return report
