from dti_ui_v1.services.likelihood_solver_validator import (
    validate_solver_response,
)


def test_solver_response_validation():
    payload = {
        "solver_id": "TEST",
        "solver_version": "V1",
        "model_id": "MODEL",
        "chi2": 1.0,
        "loglike": -0.5,
    }

    assert validate_solver_response(payload)


def test_invalid_nan_response():
    payload = {
        "solver_id": "TEST",
        "solver_version": "V1",
        "model_id": "MODEL",
        "chi2": float("nan"),
        "loglike": -0.5,
    }

    assert not validate_solver_response(payload)
