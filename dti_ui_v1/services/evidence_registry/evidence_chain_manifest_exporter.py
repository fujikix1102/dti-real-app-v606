from pathlib import Path
import hashlib
import json


def sha256_text(text):
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def build_evidence_chain_manifest(
    registry,
    validation,
    failure_report,
):

    manifest = {}

    for source in registry:

        manifest[source] = {
            "registry": registry[source],
            "validation": validation[source],
            "failure_report": failure_report[source],
        }

    return manifest


def write_manifest_files(
    manifest,
    output_dir,
):

    output = Path(output_dir)
    output.mkdir(
        parents=True,
        exist_ok=True,
    )

    registry_file = output / "REGISTRY_MANIFEST.json"
    validation_file = output / "VALIDATION_MANIFEST.json"
    failure_file = output / "FAILURE_REPORT_MANIFEST.json"

    registry_file.write_text(
        json.dumps(
            {
                k:v["registry"]
                for k,v in manifest.items()
            },
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    validation_file.write_text(
        json.dumps(
            {
                k:v["validation"]
                for k,v in manifest.items()
            },
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    failure_file.write_text(
        json.dumps(
            {
                k:v["failure_report"]
                for k,v in manifest.items()
            },
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    hashes = {}

    for f in [
        registry_file,
        validation_file,
        failure_file,
    ]:
        hashes[f.name] = hashlib.sha256(
            f.read_bytes()
        ).hexdigest()

    return hashes
