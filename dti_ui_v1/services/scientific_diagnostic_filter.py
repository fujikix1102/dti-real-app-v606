from pathlib import Path

from dti_ui_v1.services.scientific_diagnostic_summary import (
    build_diagnostic_summary,
)


SOURCE_WHITELIST = {
    "DESI DR2 Diagnostic Summary":
        "data/desi_dr2_cosmology_products/diagnostic_numeric_summary.tsv",
}


def available_sources():
    return SOURCE_WHITELIST.copy()


def load_filtered_summary(source_label):

    if source_label not in SOURCE_WHITELIST:
        raise ValueError("SOURCE_NOT_ALLOWED")

    summary = build_diagnostic_summary(
        SOURCE_WHITELIST[source_label]
    )

    return summary


def apply_flag_filter(summary, flag_key=None, flag_value=None):

    if not flag_key or not flag_value:
        return summary

    flags = summary.get(
        "diagnostic_flags",
        {}
    )

    values = flags.get(
        flag_key,
        []
    )

    summary["filter_result"] = {
        "key": flag_key,
        "value": flag_value,
        "matched": flag_value in values,
    }

    return summary
