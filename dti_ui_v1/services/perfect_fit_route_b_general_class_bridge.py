"""PERFECT FIT Route B -> General CLASS bridge.

This module only converts validated runtime parameters into the existing
GeneralClassRequest contract.

Boundary:
- no MCMC
- no posterior
- no sampler
- no GTDS execution
- no likelihood inference

Execution target:
existing single-point CLASS/AxiCLASS forward compute service only.
"""

from __future__ import annotations

from typing import Any, Mapping

from dti_ui_v1.services.perfect_fit_runtime_parameter_adapter import (
    RuntimeParameterRequest,
    validate_runtime_parameter_request,
)

from dti_ui_v1.services.general_class_compute_service import (
    GeneralClassRequest,
)


DEFAULTS = {
    "n_s": 0.9847,
    "ln10_10_As": 3.058,
    "tau_reio": 0.0511,
    "z_c": 3500.0,
}


class RouteBGeneralClassBridgeError(ValueError):
    pass


def build_general_class_request_from_route_b(
    request: RuntimeParameterRequest,
) -> GeneralClassRequest:

    validate_runtime_parameter_request(request)

    params: Mapping[str, Any] = request.parameters

    def value(
        key: str,
        default: float | None = None,
    ) -> float:

        if key in params:
            return float(params[key])

        if default is not None:
            return float(default)

        raise RouteBGeneralClassBridgeError(
            f"missing_required_parameter:{key}"
        )

    return GeneralClassRequest(
        H0=value("H0"),
        omega_b=value("omega_b"),
        omega_cdm=value("omega_cdm"),
        n_s=value("n_s", DEFAULTS["n_s"]),
        ln10_10_As=value(
            "ln10_10_As",
            DEFAULTS["ln10_10_As"],
        ),
        tau_reio=value(
            "tau_reio",
            DEFAULTS["tau_reio"],
        ),
        f_EDE=value("f_EDE", 0.0),
        z_c=value(
            "z_c",
            DEFAULTS["z_c"],
        ),
        timeout_seconds=float(
            request.timeout_seconds
        ),
    )


def general_class_request_to_dict(
    request: GeneralClassRequest,
) -> dict[str, Any]:
    return {
        "H0": request.H0,
        "omega_b": request.omega_b,
        "omega_cdm": request.omega_cdm,
        "n_s": request.n_s,
        "ln10_10_As": request.ln10_10_As,
        "tau_reio": request.tau_reio,
        "f_EDE": request.f_EDE,
        "z_c": request.z_c,
        "timeout_seconds": request.timeout_seconds,
    }
