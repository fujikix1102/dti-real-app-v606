from pathlib import Path
import json
import datetime
import hashlib


def checksum(path):

    h=hashlib.sha256()

    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)

    return h.hexdigest()



def build_scan_record(asset, result):

    return {

        "timestamp":
            str(datetime.datetime.now()),

        "asset":
            str(asset),

        "checksum":
            checksum(asset)
            if Path(asset).exists()
            else None,

        "result":
            result,

        "source_identity":
            {
                "source_path":
                    str(asset),

                "role":
                    "diagnostic_input"
            },

        "claim_boundary":
            [
                "diagnostic_only",
                "no_posterior",
                "no_detection_claim"
            ]
    }



def save_scan_record(asset,result):

    root=Path(
        "data/research/evidence/dti_raw_profile/results"
    )

    root.mkdir(
        parents=True,
        exist_ok=True
    )

    out=root/"latest_scan.json"

    out.write_text(
        json.dumps(
            build_scan_record(asset,result),
            indent=2
        )
    )

    return out
