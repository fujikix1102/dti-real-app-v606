from pathlib import Path
import csv
import hashlib


def checksum(path):

    h=hashlib.sha256()

    with open(path,"rb") as f:

        for b in iter(
            lambda:f.read(1024*1024),
            b""
        ):
            h.update(b)

    return h.hexdigest()



def is_numeric(value):

    try:
        float(value)
        return True

    except Exception:
        return False



def load_profile_safe(path):

    path=Path(path)

    if not path.exists():

        return {
            "status":"MISSING",
            "rows":[]
        }


    rows=[]

    skipped=[]


    with path.open(
        encoding="utf-8"
    ) as f:

        reader=csv.DictReader(
            f,
            delimiter="\t"
        )


        for index,r in enumerate(reader):

            z=r.get("z_i")
            y=r.get("y_i")
            w=r.get("w_i")
            source=r.get(
                "source_id",
                "UNKNOWN"
            )


            if not is_numeric(z) or not is_numeric(y):

                skipped.append(
                    {
                        "line":index+2,
                        "reason":
                        "NON_NUMERIC_ROW"
                    }
                )

                continue


            rows.append(
                {
                    "z":z,
                    "y":y,
                    "w":w,
                    "source":source
                }
            )


    return {

        "status":
            "LOADED",

        "rows":
            rows,

        "points":
            len(rows),

        "skipped_rows":
            skipped,

        "skipped_count":
            len(skipped),

        "checksum":
            checksum(path),

        "claim_boundary":
            [
                "diagnostic_only",
                "no_posterior",
                "no_detection_claim"
            ]

    }
