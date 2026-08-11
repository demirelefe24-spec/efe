"""Tests for the two-foil static load-balance calculation."""

from __future__ import annotations

import math

import pytest

from hydrofoil_designer import (
    DEFAULT_GRAVITY_M_S2,
    LoadBalanceInputs,
    calculate_static_load_balance,
)
from hydrofoil_designer.constants import (
    FORCE_RESIDUAL_ABS_TOLERANCE_N,
    LOAD_PERCENT_ABS_TOLERANCE,
    MOMENT_RESIDUAL_ABS_TOLERANCE_NM,
)


CALCULATION_REL_TOLERANCE = 1.0e-12
CALCULATION_ABS_TOLERANCE = 1.0e-9


def make_inputs(*, lcg_from_stern_m: float = 2.0) -> LoadBalanceInputs:
    """Return a normal arrangement using software-test geometry only."""

    return LoadBalanceInputs(
        mass_kg=1000.0,
        lcg_from_stern_m=lcg_from_stern_m,
        aft_foil_from_stern_m=1.0,
        fore_foil_from_stern_m=3.0,
    )


def test_symmetric_arrangement_shares_load_equally() -> None:
    result = calculate_static_load_balance(make_inputs())

    assert result.fore_lift_n == pytest.approx(
        result.aft_lift_n,
        rel=CALCULATION_REL_TOLERANCE,
        abs=CALCULATION_ABS_TOLERANCE,
    )
    assert result.fore_load_fraction == pytest.approx(0.5, abs=1.0e-15)
    assert result.aft_load_fraction == pytest.approx(0.5, abs=1.0e-15)


def test_lcg_near_aft_foil_increases_aft_load() -> None:
    result = calculate_static_load_balance(make_inputs(lcg_from_stern_m=1.25))

    assert result.aft_lift_n > result.fore_lift_n
    assert result.aft_load_fraction == pytest.approx(0.875, abs=1.0e-15)


def test_lcg_near_fore_foil_increases_fore_load() -> None:
    result = calculate_static_load_balance(make_inputs(lcg_from_stern_m=2.75))

    assert result.fore_lift_n > result.aft_lift_n
    assert result.fore_load_fraction == pytest.approx(0.875, abs=1.0e-15)


def test_vertical_forces_sum_to_weight() -> None:
    result = calculate_static_load_balance(make_inputs(lcg_from_stern_m=2.31))

    assert result.fore_lift_n + result.aft_lift_n == pytest.approx(
        result.weight_n,
        rel=CALCULATION_REL_TOLERANCE,
        abs=CALCULATION_ABS_TOLERANCE,
    )
    assert abs(result.vertical_force_residual_n) <= (
        FORCE_RESIDUAL_ABS_TOLERANCE_N
        + CALCULATION_REL_TOLERANCE * result.weight_n
    )


def test_moment_residual_is_within_tolerance() -> None:
    result = calculate_static_load_balance(make_inputs(lcg_from_stern_m=1.73))

    assert abs(result.moment_residual_nm) <= (
        MOMENT_RESIDUAL_ABS_TOLERANCE_NM
        + CALCULATION_REL_TOLERANCE * result.weight_n * 2.0
    )


def test_load_percentages_sum_to_100() -> None:
    result = calculate_static_load_balance(make_inputs(lcg_from_stern_m=2.21))

    assert result.fore_load_percent + result.aft_load_percent == pytest.approx(
        100.0,
        rel=0.0,
        abs=LOAD_PERCENT_ABS_TOLERANCE,
    )


def test_reference_boat_weight_for_1299_kg() -> None:
    inputs = LoadBalanceInputs(
        mass_kg=1299.0,
        lcg_from_stern_m=1.987,
        aft_foil_from_stern_m=0.75,
        fore_foil_from_stern_m=3.25,
        gravity_m_s2=DEFAULT_GRAVITY_M_S2,
    )

    result = calculate_static_load_balance(inputs)

    assert result.weight_n == pytest.approx(
        12738.83835,
        rel=CALCULATION_REL_TOLERANCE,
        abs=CALCULATION_ABS_TOLERANCE,
    )


@pytest.mark.parametrize(
    ("lcg_from_stern_m", "aft_foil_from_stern_m", "fore_foil_from_stern_m"),
    [
        (0.5, 1.0, 3.0),
        (3.5, 1.0, 3.0),
        (2.0, 3.0, 1.0),
    ],
)
def test_invalid_normal_foil_order_is_rejected(
    lcg_from_stern_m: float,
    aft_foil_from_stern_m: float,
    fore_foil_from_stern_m: float,
) -> None:
    inputs = LoadBalanceInputs(
        mass_kg=1000.0,
        lcg_from_stern_m=lcg_from_stern_m,
        aft_foil_from_stern_m=aft_foil_from_stern_m,
        fore_foil_from_stern_m=fore_foil_from_stern_m,
    )

    with pytest.raises(ValueError, match=r"x_A < x_G < x_F"):
        calculate_static_load_balance(inputs)


def test_coincident_foil_positions_are_rejected_explicitly() -> None:
    inputs = LoadBalanceInputs(
        mass_kg=1000.0,
        lcg_from_stern_m=2.0,
        aft_foil_from_stern_m=2.0,
        fore_foil_from_stern_m=2.0,
    )

    with pytest.raises(ValueError, match=r"must not be equal"):
        calculate_static_load_balance(inputs)


def test_negative_mass_is_rejected() -> None:
    inputs = LoadBalanceInputs(
        mass_kg=-1.0,
        lcg_from_stern_m=2.0,
        aft_foil_from_stern_m=1.0,
        fore_foil_from_stern_m=3.0,
    )

    with pytest.raises(ValueError, match=r"mass_kg must be greater than zero"):
        calculate_static_load_balance(inputs)


@pytest.mark.parametrize("gravity_m_s2", [0.0, -9.80665])
def test_non_positive_gravity_is_rejected(gravity_m_s2: float) -> None:
    inputs = LoadBalanceInputs(
        mass_kg=1000.0,
        lcg_from_stern_m=2.0,
        aft_foil_from_stern_m=1.0,
        fore_foil_from_stern_m=3.0,
        gravity_m_s2=gravity_m_s2,
    )

    with pytest.raises(ValueError, match=r"gravity_m_s2 must be greater than zero"):
        calculate_static_load_balance(inputs)


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("mass_kg", math.nan),
        ("mass_kg", math.inf),
        ("lcg_from_stern_m", -math.inf),
        ("aft_foil_from_stern_m", math.nan),
        ("fore_foil_from_stern_m", math.inf),
        ("gravity_m_s2", math.nan),
    ],
)
def test_non_finite_inputs_are_rejected(
    field_name: str, invalid_value: float
) -> None:
    values = {
        "mass_kg": 1000.0,
        "lcg_from_stern_m": 2.0,
        "aft_foil_from_stern_m": 1.0,
        "fore_foil_from_stern_m": 3.0,
        "gravity_m_s2": DEFAULT_GRAVITY_M_S2,
    }
    values[field_name] = invalid_value
    inputs = LoadBalanceInputs(**values)

    with pytest.raises(ValueError, match=rf"{field_name} must be finite"):
        calculate_static_load_balance(inputs)

