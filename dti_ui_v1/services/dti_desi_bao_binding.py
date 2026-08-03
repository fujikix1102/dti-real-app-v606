"""
DESI DR2 BAO source binding contract.

No raw data loading.
No likelihood evaluation.
No posterior calculation.
Display/evidence binding layer only.
"""

SOURCE_BINDING_VERSION = "V1"


def source_contract():
    return {
        "source": "DESI_DR2_BAO",
        "status": "DISPLAY_ONLY",
        "raw_read": False,
        "likelihood": False,
        "posterior": False,
    }
