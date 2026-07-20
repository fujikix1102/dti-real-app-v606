from pathlib import Path
import hashlib
import json


def sha256_file(path):

    h = hashlib.sha256()

    with open(path,"rb") as f:

        for chunk in iter(
            lambda:f.read(1024*1024),
            b""
        ):
            h.update(chunk)

    return h.hexdigest()



def validate_profile(
    profile_path,
    manifest_path=None
):

    profile = Path(profile_path)


    result={

        "file":
            str(profile),

        "exists":
            profile.exists(),

        "format":
            "TSV",

        "checks":{}

    }


    if not profile.exists():

        result["status"]="FAIL_NO_FILE"

        return result



    lines=profile.read_text().strip().splitlines()


    result["checks"]["header"] = (
        lines[0].split("\t")
        ==
        [
            "z_i",
            "y_i",
            "w_i"
        ]
    )


    rows=[]


    for line in lines[1:]:

        cols=line.split("\t")

        if len(cols)==3:

            rows.append(
                [
                    float(cols[0]),
                    float(cols[1]),
                    float(cols[2])
                ]
            )


    result["points"]=len(rows)


    result["checks"]["point_count"] = (
        len(rows)==120
    )


    z=[r[0] for r in rows]

    result["checks"]["z_monotonic"]=(
        all(
            z[i] < z[i+1]
            for i in range(len(z)-1)
        )
    )


    result["checks"]["weights_positive"]=(
        all(
            r[2]>0
            for r in rows
        )
    )


    result["checksum"]=sha256_file(
        profile
    )


    if manifest_path:

        mp=Path(manifest_path)

        if mp.exists():

            manifest=json.loads(
                mp.read_text()
            )

            result["manifest"]=manifest


            result["checks"]["manifest_points"] = (
                manifest.get("points")
                ==
                len(rows)
            )


    result["status"]=(
        "PASS"
        if all(result["checks"].values())
        else
        "FAIL"
    )


    return result
