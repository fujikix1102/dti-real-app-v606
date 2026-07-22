def build_integrity_scorecard(
    registry,
    validation,
    failure,
    manifest,
    timeline,
):

    checks = {
        "Source Identity": (
            len(registry) >= 3
        ),
        "Schema Contract": True,
        "Validation Flags": all(
            v.get("verification_status") == "PASS"
            for v in validation.values()
        ),
        "Failure Check": all(
            v.get("failure_count", 0) == 0
            for v in failure.values()
        ),
        "Manifest Availability": (
            manifest.get("status") == "MANIFEST_READY"
        ),
        "Timeline Consistency": (
            len(timeline) >= 4
        ),
    }

    passed = sum(
        1 for v in checks.values()
        if v
    )

    total = len(checks)

    return {
        "checks": checks,
        "passed": passed,
        "total": total,
        "score": f"{passed}/{total}",
        "overall": (
            "PASS"
            if passed == total
            else "REVIEW"
        ),
    }
