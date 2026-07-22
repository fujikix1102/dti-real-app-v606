from dti_ui_v1.services.scientific_payload_loader import (
    load_scientific_payload,
)


def build_live_scientific_result_context():
    return load_scientific_payload(
        "data/desi_dr2_cosmology_products/diagnostic_numeric_summary.tsv"
    )
