"""Independent checks for the project's explicit unit conversions."""

from __future__ import annotations

import math

import pytest

from hydrofoil_designer import (
    kgf_per_m2_to_n_per_m2,
    kgf_to_n,
    knots_to_m_s,
    psf_to_pa,
    psi_to_pa,
)


CONVERSION_REL_TOLERANCE = 1.0e-14
CONVERSION_ABS_TOLERANCE = 1.0e-12


def test_kgf_to_newton_uses_standard_gravity() -> None:
    assert kgf_to_n(2.5) == pytest.approx(
        24.516625,
        rel=CONVERSION_REL_TOLERANCE,
        abs=CONVERSION_ABS_TOLERANCE,
    )


def test_kgf_per_m2_to_n_per_m2() -> None:
    assert kgf_per_m2_to_n_per_m2(3800.0) == pytest.approx(
        37265.27,
        rel=CONVERSION_REL_TOLERANCE,
        abs=CONVERSION_ABS_TOLERANCE,
    )


def test_psf_to_pascal_from_exact_foot_and_pound_definitions() -> None:
    assert psf_to_pa(1.0) == pytest.approx(
        47.88025898033584,
        rel=CONVERSION_REL_TOLERANCE,
        abs=CONVERSION_ABS_TOLERANCE,
    )


def test_psi_is_not_psf() -> None:
    one_psi_pa = psi_to_pa(1.0)
    one_psf_pa = psf_to_pa(1.0)

    assert one_psi_pa == pytest.approx(
        6894.757293168361,
        rel=CONVERSION_REL_TOLERANCE,
        abs=CONVERSION_ABS_TOLERANCE,
    )
    assert one_psf_pa == pytest.approx(
        47.88025898033584,
        rel=CONVERSION_REL_TOLERANCE,
        abs=CONVERSION_ABS_TOLERANCE,
    )
    assert one_psi_pa == pytest.approx(144.0 * one_psf_pa, rel=1.0e-15)
    assert one_psi_pa != one_psf_pa


def test_knot_to_metres_per_second() -> None:
    assert knots_to_m_s(1.0) == pytest.approx(
        0.5144444444444445,
        rel=CONVERSION_REL_TOLERANCE,
        abs=CONVERSION_ABS_TOLERANCE,
    )


def test_publication_practical_range_has_exact_si_conversion() -> None:
    assert kgf_per_m2_to_n_per_m2(3800.0) == pytest.approx(
        37265.27, rel=0.0, abs=1.0e-9
    )
    assert kgf_per_m2_to_n_per_m2(5700.0) == pytest.approx(
        55897.905, rel=0.0, abs=1.0e-9
    )


@pytest.mark.parametrize("invalid_value", [math.nan, math.inf, -math.inf])
def test_conversion_functions_reject_non_finite_values(invalid_value: float) -> None:
    with pytest.raises(ValueError, match=r"must be finite"):
        kgf_per_m2_to_n_per_m2(invalid_value)


@pytest.mark.parametrize("invalid_value", [True, False, "3800"])
def test_conversion_functions_reject_bool_and_non_numeric_types(
    invalid_value: object,
) -> None:
    with pytest.raises(TypeError, match=r"must not be bool"):
        kgf_per_m2_to_n_per_m2(invalid_value)

