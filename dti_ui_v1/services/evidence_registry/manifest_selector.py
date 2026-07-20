from pathlib import Path
import json


ROOT = Path(
    "data/research/evidence/dti_raw_profile"
)


def list_manifests():

    return sorted(
        ROOT.glob("manifest_v*.json")
    )


def load_manifest(name):

    path = ROOT / name

    if not path.exists():

        return {}

    return json.loads(
        path.read_text()
    )


def resolve_asset(manifest):

    assets = manifest.get(
        "assets",
        []
    )

    if not assets:

        return None

    return assets[0].get(
        "path"
    )
