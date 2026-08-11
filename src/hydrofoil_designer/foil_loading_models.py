"""Data models for force-based foil loading and reference-area sizing."""

from __future__ import annotations

from dataclasses import dataclass

from .models import LoadBalanceResult


@dataclass(frozen=True, slots=True)
class FoilAreaInputs:
    """Inputs for sizing total, fore, and aft reference areas.

    Args:
        load_balance: A physically consistent result from the Phase 1 API.
        foil_loading_n_m2: Common force-based loading for both foils, in N/m².
            This is not dynamic pressure, even though both use pascals.
    """

    load_balance: LoadBalanceResult
    foil_loading_n_m2: float


@dataclass(frozen=True, slots=True)
class FoilAreaResult:
    """Reference-area result and independently calculated consistency residuals."""

    foil_loading_n_m2: float
    total_area_m2: float
    fore_area_m2: float
    aft_area_m2: float
    fore_area_fraction: float
    aft_area_fraction: float
    area_sum_residual_m2: float
    total_force_residual_n: float
    fore_force_residual_n: float
    aft_force_residual_n: float
    fore_area_fraction_residual: float
    aft_area_fraction_residual: float


@dataclass(frozen=True, slots=True)
class FoilLoadingScanInputs:
    """Inputs for an inclusive, linearly spaced foil-loading scan.

    ``sample_count`` includes both endpoints and defaults to two endpoints only.
    Loading bounds have no defaults and must therefore be selected explicitly.
    """

    load_balance: LoadBalanceResult
    min_foil_loading_n_m2: float
    max_foil_loading_n_m2: float
    sample_count: int = 2


@dataclass(frozen=True, slots=True)
class FoilLoadingScanResult:
    """Deterministic scan result ordered from minimum to maximum loading."""

    min_foil_loading_n_m2: float
    max_foil_loading_n_m2: float
    sample_count: int
    points: tuple[FoilAreaResult, ...]

