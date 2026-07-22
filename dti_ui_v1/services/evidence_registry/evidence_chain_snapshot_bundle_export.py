import json
import hashlib
from pathlib import Path
from datetime import datetime


SNAPSHOT = Path(
    "../_ROUTE_B_PHASE24_EVIDENCE_CHAIN_READINESS_SNAPSHOT_EXPORT_V1_20260721_163706/"
    "snapshot/EVIDENCE_CHAIN_READINESS_SNAPSHOT.json"
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



def build_snapshot_bundle(output):

    output = Path(output)

    snapshot_hash = sha256_file(
        SNAPSHOT
    )

    with open(
        SNAPSHOT,
        encoding="utf-8",
    ) as f:

        snapshot = json.load(f)


    bundle = {

        "bundle_created":
            datetime.utcnow().isoformat()
            + "Z",

        "snapshot_identity":
            {
                "path": str(SNAPSHOT),
                "sha256": snapshot_hash,
            },

        "snapshot_summary":
            {
                "registry_count":
                    len(snapshot.get("registry", {})),

                "health_status":
                    snapshot["health"]["overall"],

                "public_readiness":
                    snapshot["public_readiness"]["public_readiness"],

                "guard_status":
                    snapshot["freeze_guard"]["guard_status"],

                "alert_count":
                    snapshot["alerts"]["alert_count"],
            },

        "boundary":
            {
                "likelihood": "NO",
                "posterior": "NO",
                "mcmc": "NO",
                "physical_claim": "NO",
            },

        "bundle_status":
            "READY",

    }


    target = (
        output
        /
        "EVIDENCE_CHAIN_SNAPSHOT_BUNDLE.json"
    )


    target.write_text(
        json.dumps(
            bundle,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


    return bundle, target
