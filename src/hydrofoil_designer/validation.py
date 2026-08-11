"""Validation for static load-balance inputs and calculated results."""

from __future__ import annotations

import math
from collections.abc import Iterable

from .constants import (
    FORCE_RESIDUAL_ABS_TOLERANCE_N,
    FORCE_RESIDUAL_REL_TOLERANCE,
    LOAD_FRACTION_ABS_TOLERANCE,
    LOAD_PERCENT_ABS_TOLERANCE,
    MOMENT_RESIDUAL_ABS_TOLERANCE_NM,
    MOMENT_RESIDUAL_REL_TOLERANCE,
    NEGATIVE_LIFT_TOLERANCE_N,
)
from .models import LoadBalanceInputs, LoadBalanceResult


def _require_finite(name: str, value: float) -> None:
    try:
        is_finite = math.isfinite(value)
    except TypeError as exc:
        raise ValueError(
            f"{name} must be a finite real number; received {value!r}."
        ) from exc

    if not is_finite:
        raise ValueError(f"{name} must be finite; received {value!r}.")


def _require_all_finite(values: Iterable[tuple[str, float]]) -> None:
    for name, value in values:
        _require_finite(name, value)


def validate_load_balance_inputs(inputs: LoadBalanceInputs) -> None:
    """Validate inputs for the normal aft-LCG-fore foil arrangement.

    Args:
        inputs: Static load-balance inputs in SI units.

    Raises:
        ValueError: If a value is non-finite, a positive quantity is not
            positive, foil positions coincide, or ``x_A < x_G < x_F`` is not
            satisfied. Foil identities are never swapped automatically.
    """

    _require_all_finite(
        (
            ("mass_kg", inputs.mass_kg),
            ("lcg_from_stern_m", inputs.lcg_from_stern_m),
            ("aft_foil_from_stern_m", inputs.aft_foil_from_stern_m),
            ("fore_foil_from_stern_m", inputs.fore_foil_from_stern_m),
            ("gravity_m_s2", inputs.gravity_m_s2),
        )
    )

    if inputs.mass_kg <= 0.0:
        raise ValueError(
            f"mass_kg must be greater than zero; received {inputs.mass_kg!r}."
        )
    if inputs.gravity_m_s2 <= 0.0:
        raise ValueError(
            "gravity_m_s2 must be greater than zero; "
            f"received {inputs.gravity_m_s2!r}."
        )
    if inputs.aft_foil_from_stern_m == inputs.fore_foil_from_stern_m:
        raise ValueError(
            "aft_foil_from_stern_m and fore_foil_from_stern_m must not be "
            f"equal; both are {inputs.aft_foil_from_stern_m!r} m."
        )
    if not (
        inputs.aft_foil_from_stern_m
        < inputs.lcg_from_stern_m
        < inputs.fore_foil_from_stern_m
    ):
        raise ValueError(
            "Normal foil arrangement requires aft_foil_from_stern_m < "
            "lcg_from_stern_m < fore_foil_from_stern_m "
            "(x_A < x_G < x_F); received "
            f"x_A={inputs.aft_foil_from_stern_m!r} m, "
            f"x_G={inputs.lcg_from_stern_m!r} m, and "
            f"x_F={inputs.fore_foil_from_stern_m!r} m. This arrangement "
            "would invalidate the normal positive-lift model."
        )


def force_residual_tolerance_n(weight_n: float) -> float:
    """Return the allowed force residual for a given weight, in newtons."""

    return (
        FORCE_RESIDUAL_ABS_TOLERANCE_N
        + FORCE_RESIDUAL_REL_TOLERANCE * abs(weight_n)
    )


def moment_residual_tolerance_nm(
    inputs: LoadBalanceInputs, result: LoadBalanceResult
) -> float:
    """Return the allowed moment residual for the current load scale."""

    fore_moment_nm = result.fore_lift_n * (
        inputs.fore_foil_from_stern_m - inputs.lcg_from_stern_m
    )
    aft_moment_nm = result.aft_lift_n * (
        inputs.lcg_from_stern_m - inputs.aft_foil_from_stern_m
    )
    moment_scale_nm = max(
        abs(fore_moment_nm),
        abs(aft_moment_nm),
        abs(result.weight_n)
        * (inputs.fore_foil_from_stern_m - inputs.aft_foil_from_stern_m),
    )
    return (
        MOMENT_RESIDUAL_ABS_TOLERANCE_NM
        + MOMENT_RESIDUAL_REL_TOLERANCE * moment_scale_nm
    )


def validate_load_balance_result(
    inputs: LoadBalanceInputs, result: LoadBalanceResult
) -> None:
    """Validate finiteness, physical sign, fractions, and equilibrium residuals.

    Args:
        inputs: The validated inputs used for the calculation.
        result: The calculated static load-balance result.

    Raises:
        ArithmeticError: If the calculated result is non-finite, contains a
            negative lift, has inconsistent fractions, or exceeds a named
            force or moment residual tolerance.
    """

    result_values = (
        (field_name, getattr(result, field_name))
        for field_name in result.__dataclass_fields__
    )
    try:
        _require_all_finite(result_values)
    except ValueError as exc:
        raise ArithmeticError(f"Calculated result is invalid: {exc}") from exc

    if result.fore_lift_n < -NEGATIVE_LIFT_TOLERANCE_N:
        raise ArithmeticError(
            "Calculated fore_lift_n is negative, which indicates invalid foil "
            f"geometry or a calculation inconsistency: {result.fore_lift_n!r} N."
        )
    if result.aft_lift_n < -NEGATIVE_LIFT_TOLERANCE_N:
        raise ArithmeticError(
            "Calculated aft_lift_n is negative, which indicates invalid foil "
            f"geometry or a calculation inconsistency: {result.aft_lift_n!r} N."
        )

    expected_weight_n = inputs.mass_kg * inputs.gravity_m_s2
    force_tolerance_n = force_residual_tolerance_n(expected_weight_n)
    if not math.isclose(
        result.weight_n,
        expected_weight_n,
        rel_tol=0.0,
        abs_tol=force_tolerance_n,
    ):
        raise ArithmeticError(
            "Calculated weight_n is inconsistent with mass_kg * gravity_m_s2: "
            f"weight_n={result.weight_n!r} N, "
            f"expected={expected_weight_n!r} N."
        )

    expected_fore_fraction = result.fore_lift_n / result.weight_n
    expected_aft_fraction = result.aft_lift_n / result.weight_n
    if not math.isclose(
        result.fore_load_fraction,
        expected_fore_fraction,
        rel_tol=0.0,
        abs_tol=LOAD_FRACTION_ABS_TOLERANCE,
    ):
        raise ArithmeticError(
            "fore_load_fraction is inconsistent with fore_lift_n / weight_n: "
            f"fraction={result.fore_load_fraction!r}, "
            f"expected={expected_fore_fraction!r}."
        )
    if not math.isclose(
        result.aft_load_fraction,
        expected_aft_fraction,
        rel_tol=0.0,
        abs_tol=LOAD_FRACTION_ABS_TOLERANCE,
    ):
        raise ArithmeticError(
            "aft_load_fraction is inconsistent with aft_lift_n / weight_n: "
            f"fraction={result.aft_load_fraction!r}, "
            f"expected={expected_aft_fraction!r}."
        )

    if not math.isclose(
        result.fore_load_fraction + result.aft_load_fraction,
        1.0,
        rel_tol=0.0,
        abs_tol=LOAD_FRACTION_ABS_TOLERANCE,
    ):
        raise ArithmeticError(
            "Calculated load fractions do not sum to one: "
            f"fore={result.fore_load_fraction!r}, "
            f"aft={result.aft_load_fraction!r}."
        )
    if not math.isclose(
        result.fore_load_percent + result.aft_load_percent,
        100.0,
        rel_tol=0.0,
        abs_tol=LOAD_PERCENT_ABS_TOLERANCE,
    ):
        raise ArithmeticError(
            "Calculated load percentages do not sum to 100: "
            f"fore={result.fore_load_percent!r}, "
            f"aft={result.aft_load_percent!r}."
        )

    if not math.isclose(
        result.fore_load_percent,
        100.0 * result.fore_load_fraction,
        rel_tol=0.0,
        abs_tol=LOAD_PERCENT_ABS_TOLERANCE,
    ) or not math.isclose(
        result.aft_load_percent,
        100.0 * result.aft_load_fraction,
        rel_tol=0.0,
        abs_tol=LOAD_PERCENT_ABS_TOLERANCE,
    ):
        raise ArithmeticError(
            "Calculated load percentages are inconsistent with their fractions."
        )

    recomputed_force_residual_n = math.fsum(
        (result.fore_lift_n, result.aft_lift_n, -result.weight_n)
    )
    if not math.isclose(
        result.vertical_force_residual_n,
        recomputed_force_residual_n,
        rel_tol=0.0,
        abs_tol=force_tolerance_n,
    ):
        raise ArithmeticError(
            "Stored vertical-force residual is inconsistent with an independent "
            "recalculation: "
            f"stored={result.vertical_force_residual_n!r} N, "
            f"recomputed={recomputed_force_residual_n!r} N."
        )
    if abs(recomputed_force_residual_n) > force_tolerance_n:
        raise ArithmeticError(
            "Vertical-force equilibrium residual exceeds tolerance: "
            f"residual={recomputed_force_residual_n!r} N, "
            f"tolerance={force_tolerance_n!r} N."
        )

    moment_tolerance_nm = moment_residual_tolerance_nm(inputs, result)
    recomputed_moment_residual_nm = math.fsum(
        (
            result.fore_lift_n
            * (inputs.fore_foil_from_stern_m - inputs.lcg_from_stern_m),
            -result.aft_lift_n
            * (inputs.lcg_from_stern_m - inputs.aft_foil_from_stern_m),
        )
    )
    if not math.isclose(
        result.moment_residual_nm,
        recomputed_moment_residual_nm,
        rel_tol=0.0,
        abs_tol=moment_tolerance_nm,
    ):
        raise ArithmeticError(
            "Stored moment residual is inconsistent with an independent "
            "recalculation: "
            f"stored={result.moment_residual_nm!r} N m, "
            f"recomputed={recomputed_moment_residual_nm!r} N m."
        )
    if abs(recomputed_moment_residual_nm) > moment_tolerance_nm:
        raise ArithmeticError(
            "Moment equilibrium residual exceeds tolerance: "
            f"residual={recomputed_moment_residual_nm!r} N m, "
            f"tolerance={moment_tolerance_nm!r} N m."
        )
