from pathlib import Path
import json
import hashlib
from datetime import datetime


ROOT = Path(
    "data/research/evidence/manifests"
)

ROOT.mkdir(
    parents=True,
    exist_ok=True
)


def sha256_file(path):

    h = hashlib.sha256()

    with open(path,"rb") as f:

        for chunk in iter(
            lambda:f.read(1024*1024),
            b""
        ):
            h.update(chunk)

    return h.hexdigest()



def register_manifest(
    source_path,
    metadata=None
):

    data = {

        "timestamp":
            str(datetime.now()),

        "source_path":
            str(source_path),

        "metadata":
            metadata or {},

        "checksum":
            sha256_file(source_path)
            if Path(source_path).exists()
            else "NOT_AVAILABLE"
    }


    out = ROOT / (
        "manifest_"
        + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
        + ".json"
    )


    out.write_text(
        json.dumps(
            data,
            indent=2
        )
    )

    return data
