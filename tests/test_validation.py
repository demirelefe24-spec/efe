"""Tests for independent result-consistency validation."""

from dataclasses import replace

import pytest

from hydrofoil_designer import LoadBalanceInputs, calculate_static_load_balance
from hydrofoil_designer.validation import validate_load_balance_result


def test_tampered_force_residual_is_rejected() -> None:
    inputs = LoadBalanceInputs(
        mass_kg=1000.0,
        lcg_from_stern_m=2.0,
        aft_foil_from_stern_m=1.0,
        fore_foil_from_stern_m=3.0,
    )
    result = calculate_static_load_balance(inputs)
    inconsistent_result = replace(result, vertical_force_residual_n=1.0)

    with pytest.raises(ArithmeticError, match=r"Stored vertical-force residual"):
        validate_load_balance_result(inputs, inconsistent_result)


def test_tampered_moment_residual_is_rejected() -> None:
    inputs = LoadBalanceInputs(
        mass_kg=1000.0,
        lcg_from_stern_m=2.0,
        aft_foil_from_stern_m=1.0,
        fore_foil_from_stern_m=3.0,
    )
    result = calculate_static_load_balance(inputs)
    inconsistent_result = replace(result, moment_residual_nm=1.0)

    with pytest.raises(ArithmeticError, match=r"Stored moment residual"):
        validate_load_balance_result(inputs, inconsistent_result)


def test_negative_calculated_lift_is_rejected() -> None:
    inputs = LoadBalanceInputs(
        mass_kg=1000.0,
        lcg_from_stern_m=2.0,
        aft_foil_from_stern_m=1.0,
        fore_foil_from_stern_m=3.0,
    )
    result = calculate_static_load_balance(inputs)
    invalid_result = replace(result, fore_lift_n=-1.0)

    with pytest.raises(ArithmeticError, match=r"fore_lift_n is negative"):
        validate_load_balance_result(inputs, invalid_result)


def test_tampered_positive_lift_is_rejected_even_if_stored_residual_is_unchanged() -> None:
    inputs = LoadBalanceInputs(
        mass_kg=1000.0,
        lcg_from_stern_m=2.0,
        aft_foil_from_stern_m=1.0,
        fore_foil_from_stern_m=3.0,
    )
    result = calculate_static_load_balance(inputs)
    invalid_result = replace(result, fore_lift_n=result.fore_lift_n + 10.0)

    with pytest.raises(ArithmeticError, match=r"fore_load_fraction is inconsistent"):
        validate_load_balance_result(inputs, invalid_result)
