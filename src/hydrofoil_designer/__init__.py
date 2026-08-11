"""Traceable calculation core for hydrofoil preliminary design."""

from .constants import (
    DEFAULT_GRAVITY_M_S2,
    PUBLICATION_GENERAL_FOIL_LOADING_MAX_KGF_M2,
    PUBLICATION_GENERAL_FOIL_LOADING_MIN_KGF_M2,
    PUBLICATION_PRACTICAL_FOIL_LOADING_MAX_KGF_M2,
    PUBLICATION_PRACTICAL_FOIL_LOADING_MIN_KGF_M2,
)
from .foil_loading import calculate_foil_areas, scan_foil_loadings
from .foil_loading_models import (
    FoilAreaInputs,
    FoilAreaResult,
    FoilLoadingScanInputs,
    FoilLoadingScanResult,
)
from .load_balance import calculate_static_load_balance
from .models import LoadBalanceInputs, LoadBalanceResult
from .units import (
    kgf_per_m2_to_n_per_m2,
    kgf_to_n,
    knots_to_m_s,
    psf_to_pa,
    psi_to_pa,
)

__all__ = [
    "DEFAULT_GRAVITY_M_S2",
    "PUBLICATION_GENERAL_FOIL_LOADING_MAX_KGF_M2",
    "PUBLICATION_GENERAL_FOIL_LOADING_MIN_KGF_M2",
    "PUBLICATION_PRACTICAL_FOIL_LOADING_MAX_KGF_M2",
    "PUBLICATION_PRACTICAL_FOIL_LOADING_MIN_KGF_M2",
    "FoilAreaInputs",
    "FoilAreaResult",
    "FoilLoadingScanInputs",
    "FoilLoadingScanResult",
    "LoadBalanceInputs",
    "LoadBalanceResult",
    "calculate_foil_areas",
    "calculate_static_load_balance",
    "kgf_per_m2_to_n_per_m2",
    "kgf_to_n",
    "knots_to_m_s",
    "psf_to_pa",
    "psi_to_pa",
    "scan_foil_loadings",
]

__version__ = "0.2.0"
