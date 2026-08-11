"""Data models for hydrofoil preliminary-design calculations."""

from dataclasses import dataclass

from .constants import DEFAULT_GRAVITY_M_S2


@dataclass(frozen=True, slots=True)
class LoadBalanceInputs:
    """Inputs for the two-foil static vertical load balance.

    All positions use the same stern reference and increase forward.

    Args:
        mass_kg: Total boat mass in kilograms.
        lcg_from_stern_m: Longitudinal centre of gravity, in metres from stern.
        aft_foil_from_stern_m: Aft foil lift centre, in metres from stern.
        fore_foil_from_stern_m: Fore foil lift centre, in metres from stern.
        gravity_m_s2: Acceleration of gravity in metres per second squared.
    """

    mass_kg: float
    lcg_from_stern_m: float
    aft_foil_from_stern_m: float
    fore_foil_from_stern_m: float
    gravity_m_s2: float = DEFAULT_GRAVITY_M_S2


@dataclass(frozen=True, slots=True)
class LoadBalanceResult:
    """Result of the two-foil static vertical load balance.

    Force values are in newtons, the moment residual is in newton-metres,
    fractions are dimensionless, and percentages are expressed on a 0-100 scale.
    Residuals retain full floating-point precision and are not rounded.
    """

    weight_n: float
    fore_lift_n: float
    aft_lift_n: float
    fore_load_fraction: float
    aft_load_fraction: float
    fore_load_percent: float
    aft_load_percent: float
    vertical_force_residual_n: float
    moment_residual_nm: float

