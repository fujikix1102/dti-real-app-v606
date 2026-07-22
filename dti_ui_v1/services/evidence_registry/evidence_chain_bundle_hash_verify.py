import hashlib
from pathlib import Path


BUNDLE = Path(
    "../_ROUTE_B_PHASE27_EVIDENCE_CHAIN_SNAPSHOT_EXPORT_BUNDLE_V1_20260721_164100/"
    "bundle/EVIDENCE_CHAIN_SNAPSHOT_BUNDLE.json"
)


def sha256_file(path):

    h = hashlib.sha256()

    with open(path, "rb") as f:

        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()



def verify_bundle_hash():

    actual = sha256_file(
        BUNDLE
    )

    return {

        "path":
            str(BUNDLE),

        "actual_sha256":
            actual,

        "status":
            "HASH_READY",

    }
