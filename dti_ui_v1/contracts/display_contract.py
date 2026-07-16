"""Display contracts for the MAXOMEGA / DTI scientific workbench."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class DecimalContract:
    h0: int = 2
    omega_b: int = 5
    omega_cdm: int = 5
    chi2: int = 4
    probability: int = 6
    generic_parameter: int = 6


DECIMALS: Final[DecimalContract] = DecimalContract()

APP_TITLE: Final[str] = "MAXOMEGA / DTI"
APP_SUBTITLE: Final[str] = (
    "Scientific computation and diagnostic workbench"
)
APP_LAYOUT: Final[str] = "wide"
APP_ICON: Final[str] = "◈"

NAVIGATION_ITEMS: Final[tuple[str, ...]] = (
    "Workspace",
    "Compute",
    "Results",
    "Compare",
    "Figures",
    "Evidence",
    "Developer",
)

DEFAULT_PAGE: Final[str] = "Workspace"

WORKSPACE_MODES: Final[tuple[str, ...]] = (
    "Scientific computation",
    "Branch comparison",
    "Profile analysis",
    "Diagnostic audit",
)

RESULT_TABS: Final[tuple[str, ...]] = (
    "Overview",
    "Fit",
    "Likelihood",
    "Profiles",
    "Diagnostics",
    "Charts",
    "Raw",
)

COMPARE_SLOT_COUNT: Final[int] = 4
