"""Static vertical load distribution between aft and fore hydrofoils."""

from __future__ import annotations

import math

from .models import LoadBalanceInputs, LoadBalanceResult
from .validation import validate_load_balance_inputs, validate_load_balance_result


def calculate_static_load_balance(inputs: LoadBalanceInputs) -> LoadBalanceResult:
    """Calculate the two-foil static vertical load balance.

    The model enforces the normal arrangement ``x_A < x_G < x_F`` and uses
    upward-positive lift. It solves ``L_F + L_A = W`` together with moment
    equilibrium about the longitudinal centre of gravity. All calculations
    use SI units and no rounding is applied.

    Args:
        inputs: Boat mass, longitudinal positions, and gravity in SI units.

    Returns:
        A :class:`LoadBalanceResult` containing weight, individual foil lifts,
        load fractions and percentages, plus independently recomputed force
        and moment residuals.

    Raises:
        ValueError: If an input is non-finite or physically invalid.
        ArithmeticError: If the calculated result fails a consistency check.
    """

    validate_load_balance_inputs(inputs)

    weight_n = inputs.mass_kg * inputs.gravity_m_s2
    foil_spacing_m = (
        inputs.fore_foil_from_stern_m - inputs.aft_foil_from_stern_m
    )

    fore_lift_n = (
        weight_n
        * (inputs.lcg_from_stern_m - inputs.aft_foil_from_stern_m)
        / foil_spacing_m
    )
    aft_lift_n = (
        weight_n
        * (inputs.fore_foil_from_stern_m - inputs.lcg_from_stern_m)
        / foil_spacing_m
    )

    fore_load_fraction = fore_lift_n / weight_n
    aft_load_fraction = aft_lift_n / weight_n

    vertical_force_residual_n = math.fsum(
        (fore_lift_n, aft_lift_n, -weight_n)
    )
    moment_residual_nm = math.fsum(
        (
            fore_lift_n
            * (inputs.fore_foil_from_stern_m - inputs.lcg_from_stern_m),
            -aft_lift_n
            * (inputs.lcg_from_stern_m - inputs.aft_foil_from_stern_m),
        )
    )

    result = LoadBalanceResult(
        weight_n=weight_n,
        fore_lift_n=fore_lift_n,
        aft_lift_n=aft_lift_n,
        fore_load_fraction=fore_load_fraction,
        aft_load_fraction=aft_load_fraction,
        fore_load_percent=100.0 * fore_load_fraction,
        aft_load_percent=100.0 * aft_load_fraction,
        vertical_force_residual_n=vertical_force_residual_n,
        moment_residual_nm=moment_residual_nm,
    )
    validate_load_balance_result(inputs, result)
    return result

