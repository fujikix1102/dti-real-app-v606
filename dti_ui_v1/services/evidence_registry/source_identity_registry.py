from pathlib import Path
import hashlib


SOURCE_REGISTRY = {
    "DESI_DR2_DIAGNOSTIC_SUMMARY": {
        "path": "data/desi_dr2_cosmology_products/diagnostic_numeric_summary.tsv",
        "role": "DIAGNOSTIC_ONLY",
        "likelihood": "NO",
        "posterior": "NO",
        "claim": "NO",
    },

    "FROZEN_LIKELIHOOD_ASSET": {
        "path": "data/frozen_likelihood_asset/ONE_POINT_LIKELIHOOD_RESULT.FROZEN.tsv",
        "role": "FROZEN_ASSET_RECORD",
        "likelihood": "BOUNDARY_ONLY",
        "posterior": "NO",
        "claim": "NO",
    },

    "SECTION8_SOURCE_RECORD": {
        "path": "data/section8_source_record/section8_primary_comparison_graph_normalized.tsv",
        "role": "SOURCE_RECORD",
        "likelihood": "NO",
        "posterior": "NO",
        "claim": "NO",
    },
}



def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def build_source_identity_registry():

    result = {}

    for key, item in SOURCE_REGISTRY.items():

        p = Path(item["path"])

        record = dict(item)

        record["exists"] = p.exists()

        if p.exists():
            record["sha256"] = sha256_file(p)
        else:
            record["sha256"] = None

        result[key] = record

    return result
