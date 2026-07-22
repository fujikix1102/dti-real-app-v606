from pathlib import Path
import csv
import hashlib


def checksum(path):

    h=hashlib.sha256()

    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)

    return h.hexdigest()



def load_profile(path):

    path=Path(path)

    if not path.exists():

        return {
            "status":"MISSING",
            "points":0,
            "rows":[]
        }


    rows=[]

    with path.open(
        encoding="utf-8"
    ) as f:

        reader=csv.DictReader(
            f,
            delimiter="\t"
        )

        for r in reader:

            rows.append(
                {
                    "z":
                        r.get("z_i"),

                    "y":
                        r.get("y_i"),

                    "w":
                        r.get("w_i"),

                    "source":
                        r.get(
                            "source_id",
                            "UNKNOWN"
                        )
                }
            )


    return {

        "status":
            "LOADED",

        "points":
            len(rows),

        "rows":
            rows,

        "checksum":
            checksum(path),

        "claim_boundary":
            [
                "diagnostic_only",
                "no_posterior",
                "no_detection"
            ]
    }



def profile_summary(profile):

    return {

        "status":
            profile.get("status"),

        "point_count":
            profile.get("points"),

        "source_types":
            sorted(
                list(
                    set(
                        r["source"]
                        for r in profile.get(
                            "rows",
                            []
                        )
                    )
                )
            ),

        "ready_for_gtds":
            profile.get(
                "points",
                0
            ) > 2

    }
