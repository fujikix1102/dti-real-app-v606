"""Global numeric precision and source-value contracts.

Display precision, input resolution, and internal source values are
separate concerns. Display formatting must never be written back into a
scientific configuration or result object.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from types import MappingProxyType
from typing import Final, Mapping


@dataclass(frozen=True)
class NumericFieldContract:
    key: str
    label: str
    symbol: str
    source_text: str
    display_places: int
    input_places: int
    input_step_text: str
    unit: str = ""

    @property
    def decimal_value(self) -> Decimal:
        return Decimal(self.source_text)

    @property
    def float_value(self) -> float:
        return float(self.decimal_value)

    @property
    def input_step(self) -> float:
        return float(Decimal(self.input_step_text))


_BASELINE_ITEMS = (
    NumericFieldContract(
        key="H0",
        label="Hubble constant",
        symbol="H₀",
        source_text="67.32117",
        display_places=5,
        input_places=5,
        input_step_text="0.00001",
        unit="km s⁻¹ Mpc⁻¹",
    ),
    NumericFieldContract(
        key="omega_b",
        label="Physical baryon density",
        symbol="ω_b",
        source_text="0.0223828",
        display_places=7,
        input_places=7,
        input_step_text="0.0000001",
    ),
    NumericFieldContract(
        key="omega_cdm",
        label="Physical cold-dark-matter density",
        symbol="ω_cdm",
        source_text="0.1201075",
        display_places=7,
        input_places=7,
        input_step_text="0.0000001",
    ),
    NumericFieldContract(
        key="n_s",
        label="Scalar spectral index",
        symbol="n_s",
        source_text="0.965",
        display_places=6,
        input_places=6,
        input_step_text="0.000001",
    ),
    NumericFieldContract(
        key="ln10_10_A_s",
        label="Log scalar amplitude",
        symbol="ln(10¹⁰A_s)",
        source_text="3.044",
        display_places=6,
        input_places=6,
        input_step_text="0.000001",
    ),
    NumericFieldContract(
        key="tau_reio",
        label="Reionization optical depth",
        symbol="τ_reio",
        source_text="0.054",
        display_places=6,
        input_places=6,
        input_step_text="0.000001",
    ),
)

_OBJECTIVE_ITEMS = (
    NumericFieldContract(
        key="model_loglike",
        label="Model log-likelihood",
        symbol="log L",
        source_text="-15.716960481571116",
        display_places=15,
        input_places=15,
        input_step_text="0.000000000000001",
    ),
    NumericFieldContract(
        key="model_chi2",
        label="Model chi-square",
        symbol="χ²",
        source_text="10.282340710817206",
        display_places=15,
        input_places=15,
        input_step_text="0.000000000000001",
    ),
)

BASELINE_CONTRACTS: Final[Mapping[str, NumericFieldContract]] = (
    MappingProxyType({
        item.key: item
        for item in _BASELINE_ITEMS
    })
)

OBJECTIVE_CONTRACTS: Final[Mapping[str, NumericFieldContract]] = (
    MappingProxyType({
        item.key: item
        for item in _OBJECTIVE_ITEMS
    })
)

ALL_NUMERIC_CONTRACTS: Final[
    Mapping[str, NumericFieldContract]
] = MappingProxyType({
    **BASELINE_CONTRACTS,
    **OBJECTIVE_CONTRACTS,
})

PRESET_ID: Final[str] = "LOCKED_BASELINE_67_32117"
PRESET_LABEL: Final[str] = "Locked baseline — H0 67.32117"
