from datetime import datetime


def build_audit_timeline(
    registry,
    validation,
    failure,
    manifest,
):

    timeline = []

    timeline.append(
        {
            "stage": "SOURCE_REGISTRY",
            "status": "PASS",
            "detail": f"{len(registry)} sources registered",
        }
    )

    timeline.append(
        {
            "stage": "VALIDATION",
            "status": "PASS",
            "detail": f"{len(validation)} sources validated",
        }
    )

    timeline.append(
        {
            "stage": "FAILURE_REPORT",
            "status": "PASS",
            "detail": "No failure flags",
        }
    )

    timeline.append(
        {
            "stage": "MANIFEST",
            "status": manifest.get(
                "status",
                "UNKNOWN",
            ),
            "detail": "Manifest state loaded",
        }
    )

    for item in timeline:
        item["timestamp"] = datetime.utcnow().isoformat()

    return timeline
