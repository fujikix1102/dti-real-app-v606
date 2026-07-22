def validate(profile):

    rows=profile.get(
        "rows",
        []
    )

    result={

        "points":
            len(rows),

        "has_z":
            all(
                r.get("z") is not None
                for r in rows
            ),

        "has_y":
            all(
                r.get("y") is not None
                for r in rows
            ),

        "source_bound":
            all(
                r.get("source")!="UNKNOWN"
                for r in rows
            )

    }


    result["status"] = (
        "PASS"
        if all(result.values())
        else
        "FAIL"
    )

    return result
