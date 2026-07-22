from pathlib import Path
import hashlib
import json
import datetime


SUPPORTED = {
    ".tsv",
    ".csv",
    ".fits",
    ".fit",
    ".parquet"
}


def checksum(path):

    h = hashlib.sha256()

    with open(path,"rb") as f:

        for block in iter(
            lambda:f.read(1024*1024),
            b""
        ):
            h.update(block)

    return h.hexdigest()



def detect_assets(folder):

    folder=Path(folder)

    assets=[]

    for p in folder.rglob("*"):

        if p.is_file() and p.suffix.lower() in SUPPORTED:

            assets.append(
                {
                    "path":str(p),
                    "format":p.suffix.lower().replace(".","").upper(),
                    "bytes":p.stat().st_size,
                    "checksum":checksum(p)
                }
            )

    return assets



def build_manifest(folder):

    assets=detect_assets(folder)

    manifest={

        "manifest_timestamp":
            str(datetime.datetime.now()),

        "asset_count":
            len(assets),

        "assets":
            assets,

        "claim_boundary":
            [
                "diagnostic_only",
                "no_posterior",
                "no_detection_claim"
            ]
    }

    return manifest



def save_manifest(folder):

    out=Path(
        "data/research/evidence/dti_raw_profile"
    )

    out.mkdir(
        parents=True,
        exist_ok=True
    )

    versions=sorted(
        out.glob("manifest_v*.json")
    )

    v=len(versions)+1

    path=out/f"manifest_v{v}.json"

    data=build_manifest(folder)

    path.write_text(
        json.dumps(
            data,
            indent=2
        )
    )

    return path,data
