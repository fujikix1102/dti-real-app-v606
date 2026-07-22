def build_freeze_alerts(guard):

    alerts = []

    if guard.get("hash_status") != "PASS":
        alerts.append(
            {
                "type": "HASH_FAIL",
                "severity": "HIGH",
                "message": "Freeze hash verification failed."
            }
        )

    if guard.get("registry_count") != 3:
        alerts.append(
            {
                "type": "REGISTRY_COUNT_CHANGE",
                "severity": "MEDIUM",
                "message": "Registry source count changed."
            }
        )

    if guard.get("timeline_count") != 4:
        alerts.append(
            {
                "type": "TIMELINE_CHANGE",
                "severity": "MEDIUM",
                "message": "Audit timeline count changed."
            }
        )

    if not alerts:

        alerts.append(
            {
                "type": "NONE",
                "severity": "INFO",
                "message": "Freeze integrity verified."
            }
        )


    return {
        "alert_count": len(
            alerts
        ),
        "alerts": alerts,
        "review_required":
            any(
                x["severity"] in [
                    "HIGH",
                    "MEDIUM"
                ]
                for x in alerts
            )
    }
