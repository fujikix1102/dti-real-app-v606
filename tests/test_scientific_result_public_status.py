from dti_ui_v1.services.scientific_result_adapter import (
    build_scientific_result_payload,
)


def test_scientific_result_payload_has_plain_public_status() -> None:
    payload = build_scientific_result_payload()

    assert payload["status"] == "DIAGNOSTIC_PAYLOAD_ONLY"
    assert payload["public_status"] == (
        "review display only; no posterior, MCMC, or model-ranking claim"
    )
    assert "DIAGNOSTIC_PAYLOAD_ONLY" not in payload["public_status"]
