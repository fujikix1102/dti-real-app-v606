from dti_ui_v1.services.route_c.route_c_contract import ROUTE_C_BOUNDARY


def build_route_c_display_payload(source=None):
    """
    Convert frozen Route C artifacts into display payload.

    No numerical recomputation.
    No inference.
    """

    return {
        "source": source,
        "gtds_chain_identity": None,
        "mahalanobis_geometry": None,
        "tda_beta0_persistence": None,
        "dhz_diagnostic": None,
        "bayesian_evidence_audit": None,
        "boundary": ROUTE_C_BOUNDARY,
    }
