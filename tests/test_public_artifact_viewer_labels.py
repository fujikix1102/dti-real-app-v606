from dti_ui_v1.components.perfect_fit_artifact_viewer import (
    _compact_r2_rows,
    _research_run_label,
    _run_explanation,
)


def test_class_compute_run_gets_researcher_readable_label() -> None:
    row = {
        "run_id": "20260820T080952.682181Z_class_compute",
        "route": "class_compute",
        "status": "ok",
        "created_at_utc": "2026-08-20T08:09:52.682181+00:00",
        "H0": 72.9,
        "A_DTI": 0,
        "f_EDE": 0.082,
        "z_c": 3500,
    }

    label = _research_run_label(row)

    assert "Single deterministic CLASS/AxiCLASS run" in label
    assert "H0=72.9" in label
    assert "f_EDE=0.082" in label
    assert "20260820T080952.682181Z_class_compute" not in label


def test_artifact_payload_label_falls_back_to_request_parameters() -> None:
    payload = {
        "run_id": "20260820T080952.682181Z_class_compute",
        "route": "class_compute",
        "created_at_utc": "2026-08-20T08:09:52.682181+00:00",
        "request": {
            "H0": 72.9,
            "A_DTI": 0,
            "f_EDE": 0.082,
            "z_c": 3500,
        },
    }

    label = _research_run_label(payload)

    assert "H0=72.9" in label
    assert "z_c=3500" in label


def test_compact_rows_expose_display_name_before_internal_id() -> None:
    frame = _compact_r2_rows(
        [
            {
                "run_id": "20260820T080952.682181Z_class_compute",
                "route": "class_compute",
                "status": "ok",
                "created_at_utc": "2026-08-20T08:09:52.682181+00:00",
                "H0": 72.9,
                "A_DTI": 0,
                "f_EDE": 0.082,
                "z_c": 3500,
                "artifact_sha256": "abcdef1234567890",
            }
        ]
    )

    assert list(frame.columns)[:2] == ["display_name", "meaning"]
    assert frame.loc[0, "internal_run_id"] == "20260820T080952.682181Z_class_compute"
    assert frame.loc[0, "display_name"] != frame.loc[0, "internal_run_id"]


def test_run_explanation_preserves_internal_id_as_detail() -> None:
    explanation = _run_explanation(
        {
            "run_id": "20260820T080952.682181Z_class_compute",
            "route": "class_compute",
            "status": "ok",
            "H0": 72.9,
        }
    )

    assert explanation["meaning"] == "Single deterministic CLASS/AxiCLASS run"
    assert explanation["internal_run_id"] == "20260820T080952.682181Z_class_compute"
    assert "no MCMC" in explanation["scope"]
