"""Tests for force-based foil loading and reference-area sizing."""

from __future__ import annotations

import math
from dataclasses import replace

import pytest

from hydrofoil_designer import (
    FoilAreaInputs,
    FoilLoadingScanInputs,
    LoadBalanceInputs,
    LoadBalanceResult,
    calculate_foil_areas,
    calculate_static_load_balance,
    scan_foil_loadings,
)
from hydrofoil_designer.constants import (
    AREA_FRACTION_ABS_TOLERANCE,
    AREA_RESIDUAL_ABS_TOLERANCE_M2,
    FOIL_LOADING_FORCE_RESIDUAL_ABS_TOLERANCE_N,
)
from hydrofoil_designer.foil_loading_validation import validate_foil_area_result


CALCULATION_REL_TOLERANCE = 1.0e-12
CALCULATION_ABS_TOLERANCE = 1.0e-12


def simple_load_balance() -> LoadBalanceResult:
    """Return an analytically simple and physically consistent Phase 1 result."""

    return LoadBalanceResult(
        weight_n=1000.0,
        fore_lift_n=400.0,
        aft_lift_n=600.0,
        fore_load_fraction=0.4,
        aft_load_fraction=0.6,
        fore_load_percent=40.0,
        aft_load_percent=60.0,
        vertical_force_residual_n=0.0,
        moment_residual_nm=0.0,
    )


def test_known_foil_loading_to_area_calculation() -> None:
    result = calculate_foil_areas(
        FoilAreaInputs(simple_load_balance(), foil_loading_n_m2=500.0)
    )

    assert result.total_area_m2 == pytest.approx(2.0, abs=1.0e-15)
    assert result.fore_area_m2 == pytest.approx(0.8, abs=1.0e-15)
    assert result.aft_area_m2 == pytest.approx(1.2, abs=1.0e-15)


def test_phase_1_result_integrates_with_foil_area_calculation() -> None:
    load_balance = calculate_static_load_balance(
        LoadBalanceInputs(
            mass_kg=1299.0,
            lcg_from_stern_m=1.987,
            aft_foil_from_stern_m=0.750,
            fore_foil_from_stern_m=3.250,
        )
    )

    result = calculate_foil_areas(
        FoilAreaInputs(load_balance, foil_loading_n_m2=49033.25)
    )

    assert result.total_area_m2 == pytest.approx(
        0.2598,
        rel=CALCULATION_REL_TOLERANCE,
        abs=CALCULATION_ABS_TOLERANCE,
    )
    assert result.fore_area_m2 == pytest.approx(
        0.12854904,
        rel=CALCULATION_REL_TOLERANCE,
        abs=CALCULATION_ABS_TOLERANCE,
    )
    assert result.aft_area_m2 == pytest.approx(
        0.13125096,
        rel=CALCULATION_REL_TOLERANCE,
        abs=CALCULATION_ABS_TOLERANCE,
    )


def test_fore_and_aft_areas_sum_to_total_area() -> None:
    result = calculate_foil_areas(
        FoilAreaInputs(simple_load_balance(), foil_loading_n_m2=333.0)
    )

    assert result.fore_area_m2 + result.aft_area_m2 == pytest.approx(
        result.total_area_m2,
        rel=CALCULATION_REL_TOLERANCE,
        abs=CALCULATION_ABS_TOLERANCE,
    )


def test_area_fractions_equal_phase_1_load_fractions() -> None:
    load_balance = simple_load_balance()
    result = calculate_foil_areas(
        FoilAreaInputs(load_balance, foil_loading_n_m2=777.0)
    )

    assert result.fore_area_fraction == pytest.approx(
        load_balance.fore_load_fraction, abs=AREA_FRACTION_ABS_TOLERANCE
    )
    assert result.aft_area_fraction == pytest.approx(
        load_balance.aft_load_fraction, abs=AREA_FRACTION_ABS_TOLERANCE
    )


def test_all_area_and_force_residuals_are_within_tolerance() -> None:
    result = calculate_foil_areas(
        FoilAreaInputs(simple_load_balance(), foil_loading_n_m2=333.0)
    )

    assert abs(result.area_sum_residual_m2) <= (
        AREA_RESIDUAL_ABS_TOLERANCE_M2
        + CALCULATION_REL_TOLERANCE * result.total_area_m2
    )
    assert abs(result.total_force_residual_n) <= (
        FOIL_LOADING_FORCE_RESIDUAL_ABS_TOLERANCE_N + 1.0e-9
    )
    assert abs(result.fore_force_residual_n) <= (
        FOIL_LOADING_FORCE_RESIDUAL_ABS_TOLERANCE_N + 4.0e-10
    )
    assert abs(result.aft_force_residual_n) <= (
        FOIL_LOADING_FORCE_RESIDUAL_ABS_TOLERANCE_N + 6.0e-10
    )
    assert abs(result.fore_area_fraction_residual) <= AREA_FRACTION_ABS_TOLERANCE
    assert abs(result.aft_area_fraction_residual) <= AREA_FRACTION_ABS_TOLERANCE


def test_loading_scan_is_inclusive_and_area_decreases_monotonically() -> None:
    result = scan_foil_loadings(
        FoilLoadingScanInputs(
            load_balance=simple_load_balance(),
            min_foil_loading_n_m2=100.0,
            max_foil_loading_n_m2=500.0,
            sample_count=5,
        )
    )

    assert [point.foil_loading_n_m2 for point in result.points] == [
        100.0,
        200.0,
        300.0,
        400.0,
        500.0,
    ]
    assert all(
        earlier.total_area_m2 > later.total_area_m2
        for earlier, later in zip(result.points, result.points[1:])
    )
    assert result.points[0].total_area_m2 == pytest.approx(10.0)
    assert result.points[-1].total_area_m2 == pytest.approx(2.0)


def test_equal_loading_bounds_allow_one_point() -> None:
    result = scan_foil_loadings(
        FoilLoadingScanInputs(
            load_balance=simple_load_balance(),
            min_foil_loading_n_m2=500.0,
            max_foil_loading_n_m2=500.0,
            sample_count=1,
        )
    )

    assert len(result.points) == 1
    assert result.points[0].total_area_m2 == pytest.approx(2.0)


@pytest.mark.parametrize(
    "invalid_loading",
    [0.0, -1.0, math.nan, math.inf, -math.inf],
)
def test_invalid_foil_loading_is_rejected(invalid_loading: float) -> None:
    with pytest.raises(ValueError):
        calculate_foil_areas(FoilAreaInputs(simple_load_balance(), invalid_loading))


@pytest.mark.parametrize("invalid_loading", [True, False, "500"])
def test_bool_and_non_numeric_foil_loading_are_rejected(
    invalid_loading: object,
) -> None:
    with pytest.raises(TypeError, match=r"must not be bool"):
        calculate_foil_areas(FoilAreaInputs(simple_load_balance(), invalid_loading))


@pytest.mark.parametrize(
    ("minimum", "maximum", "sample_count"),
    [
        (500.0, 100.0, 2),
        (0.0, 500.0, 2),
        (100.0, 0.0, 2),
        (100.0, 500.0, 0),
        (100.0, 500.0, -1),
        (100.0, 500.0, 1),
        (500.0, 500.0, 2),
    ],
)
def test_invalid_scan_inputs_are_rejected(
    minimum: float, maximum: float, sample_count: int
) -> None:
    with pytest.raises(ValueError):
        scan_foil_loadings(
            FoilLoadingScanInputs(
                load_balance=simple_load_balance(),
                min_foil_loading_n_m2=minimum,
                max_foil_loading_n_m2=maximum,
                sample_count=sample_count,
            )
        )


@pytest.mark.parametrize("sample_count", [True, 2.5, "5"])
def test_scan_sample_count_rejects_bool_and_wrong_types(sample_count: object) -> None:
    with pytest.raises(TypeError, match=r"sample_count must be an integer"):
        scan_foil_loadings(
            FoilLoadingScanInputs(
                load_balance=simple_load_balance(),
                min_foil_loading_n_m2=100.0,
                max_foil_loading_n_m2=500.0,
                sample_count=sample_count,
            )
        )


@pytest.mark.parametrize("invalid_bound", [math.nan, math.inf, -math.inf])
def test_scan_rejects_non_finite_bounds(invalid_bound: float) -> None:
    with pytest.raises(ValueError, match=r"must be finite"):
        scan_foil_loadings(
            FoilLoadingScanInputs(
                load_balance=simple_load_balance(),
                min_foil_loading_n_m2=invalid_bound,
                max_foil_loading_n_m2=500.0,
                sample_count=2,
            )
        )


def test_inconsistent_phase_1_forces_are_rejected() -> None:
    inconsistent = replace(simple_load_balance(), fore_lift_n=401.0)

    with pytest.raises(ValueError, match=r"Phase 1 forces are inconsistent"):
        calculate_foil_areas(FoilAreaInputs(inconsistent, 500.0))


@pytest.mark.parametrize("invalid_area", [0.0, -1.0])
def test_zero_and_negative_calculated_areas_are_rejected(invalid_area: float) -> None:
    inputs = FoilAreaInputs(simple_load_balance(), 500.0)
    result = calculate_foil_areas(inputs)
    invalid_result = replace(result, total_area_m2=invalid_area)

    with pytest.raises(ArithmeticError, match=r"must be greater than zero"):
        validate_foil_area_result(inputs, invalid_result)


def test_tampered_area_residual_is_rejected() -> None:
    inputs = FoilAreaInputs(simple_load_balance(), 500.0)
    result = calculate_foil_areas(inputs)
    invalid_result = replace(result, area_sum_residual_m2=1.0)

    with pytest.raises(ArithmeticError, match=r"Stored area_sum_residual"):
        validate_foil_area_result(inputs, invalid_result)


def test_core_does_not_round_repeating_area_result() -> None:
    load_balance = LoadBalanceResult(
        weight_n=1.0,
        fore_lift_n=0.25,
        aft_lift_n=0.75,
        fore_load_fraction=0.25,
        aft_load_fraction=0.75,
        fore_load_percent=25.0,
        aft_load_percent=75.0,
        vertical_force_residual_n=0.0,
        moment_residual_nm=0.0,
    )

    result = calculate_foil_areas(FoilAreaInputs(load_balance, 3.0))

    assert result.total_area_m2 == 1.0 / 3.0
    assert result.total_area_m2 != 0.333

