def build_reproducibility_report(scorecard):

    checks = scorecard.get(
        "checks",
        {}
    )

    return {
        "source_registry": (
            "PASS"
            if checks.get("Source Identity")
            else "FAIL"
        ),
        "schema_contract": (
            "PASS"
            if checks.get("Schema Contract")
            else "FAIL"
        ),
        "validation": (
            "PASS"
            if checks.get("Validation Flags")
            else "FAIL"
        ),
        "failure_scan": (
            "PASS"
            if checks.get("Failure Check")
            else "FAIL"
        ),
        "manifest": (
            "PASS"
            if checks.get("Manifest Availability")
            else "FAIL"
        ),
        "timeline": (
            "PASS"
            if checks.get("Timeline Consistency")
            else "FAIL"
        ),
        "integrity_score": scorecard.get(
            "score"
        ),
        "reproducibility_status": scorecard.get(
            "overall",
            "UNKNOWN",
        ),
    }
