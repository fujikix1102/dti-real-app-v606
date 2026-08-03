"""
DESI DR2 BAO evidence display contract.

UI integration intentionally separated.
No app.py modification.
"""


def display_contract():
    return {
        "layer": "DESI_DR2_BAO",
        "display_only": True,
        "compute": False,
        "claim": False,
    }
