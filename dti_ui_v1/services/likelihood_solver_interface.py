"""
Future runtime solver interface.

This module defines contracts only.
No solver execution.
No likelihood computation.
No backend connection.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SolverRequest:
    model_id: str
    parameter_vector: dict[str, Any]
    cosmology_config: dict[str, Any]
    likelihood_config: dict[str, Any]
    solver_version: str


@dataclass(frozen=True)
class SolverResponse:
    solver_id: str
    solver_version: str
    model_id: str
    chi2: float
    loglike: float
    metadata: dict[str, Any]
