from pathlib import Path


def validate_evidence_registry(registry):

    results = {}

    for name, item in registry.items():

        path = Path(item.get("path"))

        exists = path.exists()
        sha_ok = bool(item.get("sha256")) if exists else False

        role_ok = bool(item.get("role"))

        boundary_ok = all(
            key in item
            for key in [
                "likelihood",
                "posterior",
                "claim",
            ]
        )

        results[name] = {
            "exists": exists,
            "sha256_present": sha_ok,
            "role_present": role_ok,
            "boundary_present": boundary_ok,
            "verification_status":
                "PASS"
                if (
                    exists
                    and sha_ok
                    and role_ok
                    and boundary_ok
                )
                else "FAIL",
        }

    return results
