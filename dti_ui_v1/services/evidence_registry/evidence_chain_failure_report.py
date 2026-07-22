def build_failure_report(validation):

    report = {}

    for source, item in validation.items():

        failures = []

        if not item.get("exists"):
            failures.append("SOURCE_MISSING")

        if not item.get("sha256_present"):
            failures.append("SHA256_MISSING")

        if not item.get("role_present"):
            failures.append("ROLE_MISSING")

        if not item.get("boundary_present"):
            failures.append("BOUNDARY_MISSING")

        report[source] = {
            "verification_status":
                item.get("verification_status"),
            "failure_count":
                len(failures),
            "failure_reasons":
                failures if failures else ["NONE"],
        }

    return report
