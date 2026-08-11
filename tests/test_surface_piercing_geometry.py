"""Tests for canonical surface-piercing V-foil geometry and Phase 2 hand-off."""

from __future__ import annotations

import math
from dataclasses import replace

import pytest

from hydrofoil_designer import (
    FoilAreaInputs,
    LoadBalanceInputs,
    SurfacePiercingVFoilInputs,
    SurfacePiercingVFoilPairInputs,
    calculate_foil_areas,
    calculate_static_load_balance,
    calculate_surface_piercing_v_foil_geometry,
    calculate_surface_piercing_v_foil_pair,
)
from hydrofoil_designer.surface_piercing_geometry_validation import (
    validate_surface_piercing_v_foil_result,
)


REL_TOL = 1.0e-12
ABS_TOL = 1.0e-12


def canonical_inputs() -> SurfacePiercingVFoilInputs:
    """Return a geometry with simple hand-calculable 30-degree values."""

    return SurfacePiercingVFoilInputs(
        reference_area_m2=0.4,
        total_developed_span_m=2.0,
        dihedral_deg=30.0,
        apex_submergence_m=0.25,
    )


def simple_phase_2_result(*, loading_n_m2: float = 500.0):
    """Return a valid Phase 2 result without duplicating its formulas here."""

    load_balance = calculate_static_load_balance(
        LoadBalanceInputs(
            mass_kg=100.0,
            lcg_from_stern_m=2.0,
            aft_foil_from_stern_m=1.0,
            fore_foil_from_stern_m=3.0,
            gravity_m_s2=10.0,
        )
    )
    return calculate_foil_areas(FoilAreaInputs(load_balance, loading_n_m2))


def pair_inputs(*, loading_n_m2: float = 500.0):
    """Return valid fore/aft geometry tied to a simple Phase 2 result."""

    return SurfacePiercingVFoilPairInputs(
        foil_area_result=simple_phase_2_result(loading_n_m2=loading_n_m2),
        fore_total_developed_span_m=2.0,
        fore_dihedral_deg=30.0,
        fore_apex_submergence_m=0.25,
        aft_total_developed_span_m=2.4,
        aft_dihedral_deg=45.0,
        aft_apex_submergence_m=0.30,
    )


def test_known_30_degree_geometry_matches_independent_values() -> None:
    result = calculate_surface_piercing_v_foil_geometry(canonical_inputs())

    assert result.half_panel_length_m == pytest.approx(1.0, abs=ABS_TOL)
    assert result.mean_chord_m == pytest.approx(0.2, abs=ABS_TOL)
    assert result.foil_vertical_height_m == pytest.approx(0.5, abs=ABS_TOL)
    assert result.horizontal_projected_span_m == pytest.approx(
        math.sqrt(3.0), rel=REL_TOL
    )
    assert result.wetted_half_panel_length_m == pytest.approx(0.5, abs=ABS_TOL)
    assert result.wetted_area_m2 == pytest.approx(0.2, abs=ABS_TOL)
    assert result.wetted_fraction == pytest.approx(0.5, abs=ABS_TOL)
    assert result.wetted_fraction == pytest.approx(
        canonical_inputs().apex_submergence_m
        / result.foil_vertical_height_m,
        rel=REL_TOL,
    )
    assert result.dry_half_panel_length_m == pytest.approx(0.5, abs=ABS_TOL)
    assert result.emerged_tip_height_m == pytest.approx(0.25, abs=ABS_TOL)
    assert result.apex_submergence_m == pytest.approx(0.25, abs=ABS_TOL)
    assert result.waterline_intersection_width_m == pytest.approx(
        math.sqrt(3.0) / 2.0, rel=REL_TOL
    )
    assert result.is_surface_piercing is True


def test_waterline_width_is_independent_of_full_panel_length() -> None:
    short = calculate_surface_piercing_v_foil_geometry(
        SurfacePiercingVFoilInputs(0.4, 2.0, 40.0, 0.2)
    )
    long = calculate_surface_piercing_v_foil_geometry(
        SurfacePiercingVFoilInputs(0.8, 3.0, 40.0, 0.2)
    )
    independent_expected = 2.0 * 0.2 / math.tan(math.radians(40.0))

    assert short.waterline_intersection_width_m == pytest.approx(
        independent_expected, rel=REL_TOL
    )
    assert long.waterline_intersection_width_m == pytest.approx(
        independent_expected, rel=REL_TOL
    )


def test_geometry_closure_residuals_remain_within_tolerance() -> None:
    result = calculate_surface_piercing_v_foil_geometry(
        SurfacePiercingVFoilInputs(0.731, 2.37, 37.0, 0.41)
    )

    assert abs(result.reference_area_residual_m2) <= 2.0e-12
    assert abs(result.wetted_area_residual_m2) <= 2.0e-12
    assert abs(result.height_residual_m) <= 3.0e-12


def test_core_does_not_round_repeating_geometry_values() -> None:
    result = calculate_surface_piercing_v_foil_geometry(
        SurfacePiercingVFoilInputs(1.0, 3.0, 30.0, 0.25)
    )

    assert result.mean_chord_m == 1.0 / 3.0
    assert result.mean_chord_m != 0.333


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("reference_area_m2", 0.0),
        ("reference_area_m2", -1.0),
        ("total_developed_span_m", 0.0),
        ("total_developed_span_m", -1.0),
    ],
)
def test_non_positive_area_and_span_are_rejected(
    field_name: str, invalid_value: float
) -> None:
    values = {
        "reference_area_m2": 0.4,
        "total_developed_span_m": 2.0,
        "dihedral_deg": 30.0,
        "apex_submergence_m": 0.25,
    }
    values[field_name] = invalid_value

    with pytest.raises(ValueError, match=rf"{field_name} must be greater"):
        calculate_surface_piercing_v_foil_geometry(
            SurfacePiercingVFoilInputs(**values)
        )


@pytest.mark.parametrize("dihedral_deg", [0.0, -1.0, 90.0, 100.0])
def test_dihedral_must_be_strictly_between_zero_and_ninety(
    dihedral_deg: float,
) -> None:
    with pytest.raises(ValueError, match=r"strictly between 0 and 90"):
        calculate_surface_piercing_v_foil_geometry(
            replace(canonical_inputs(), dihedral_deg=dihedral_deg)
        )


@pytest.mark.parametrize("submergence_m", [0.0, -1.0, 0.5, 0.6])
def test_submergence_must_define_a_true_surface_piercing_state(
    submergence_m: float,
) -> None:
    with pytest.raises(ValueError, match=r"greater than zero|true surface-piercing"):
        calculate_surface_piercing_v_foil_geometry(
            replace(canonical_inputs(), apex_submergence_m=submergence_m)
        )


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("reference_area_m2", math.nan),
        ("total_developed_span_m", math.inf),
        ("dihedral_deg", -math.inf),
        ("apex_submergence_m", math.nan),
    ],
)
def test_non_finite_geometry_inputs_are_rejected(
    field_name: str, invalid_value: float
) -> None:
    with pytest.raises(ValueError, match=rf"{field_name} must be finite"):
        calculate_surface_piercing_v_foil_geometry(
            replace(canonical_inputs(), **{field_name: invalid_value})
        )


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("reference_area_m2", True),
        ("total_developed_span_m", "2.0"),
        ("dihedral_deg", False),
    ],
)
def test_bool_and_wrong_geometry_types_are_rejected(
    field_name: str, invalid_value: object
) -> None:
    with pytest.raises(TypeError, match=r"must be a real number|must not be bool"):
        calculate_surface_piercing_v_foil_geometry(
            replace(canonical_inputs(), **{field_name: invalid_value})
        )


def test_pair_transfers_phase_2_areas_without_recalculation() -> None:
    inputs = pair_inputs()
    result = calculate_surface_piercing_v_foil_pair(inputs)

    assert result.foil_area_result is inputs.foil_area_result
    assert (
        result.fore_geometry.reference_area_m2
        == inputs.foil_area_result.fore_area_m2
    )
    assert (
        result.aft_geometry.reference_area_m2
        == inputs.foil_area_result.aft_area_m2
    )
    assert result.total_reference_area_m2 == pytest.approx(
        inputs.foil_area_result.total_area_m2, abs=ABS_TOL
    )
    assert abs(result.fore_area_transfer_residual_m2) <= ABS_TOL
    assert abs(result.aft_area_transfer_residual_m2) <= ABS_TOL
    assert abs(result.pair_area_sum_residual_m2) <= ABS_TOL


def test_loading_change_propagates_only_through_phase_2_reference_areas() -> None:
    lower_loading = calculate_surface_piercing_v_foil_pair(
        pair_inputs(loading_n_m2=500.0)
    )
    double_loading = calculate_surface_piercing_v_foil_pair(
        pair_inputs(loading_n_m2=1000.0)
    )

    assert double_loading.fore_geometry.reference_area_m2 == pytest.approx(
        lower_loading.fore_geometry.reference_area_m2 / 2.0, rel=REL_TOL
    )
    assert double_loading.aft_geometry.reference_area_m2 == pytest.approx(
        lower_loading.aft_geometry.reference_area_m2 / 2.0, rel=REL_TOL
    )
    assert double_loading.fore_geometry.foil_vertical_height_m == pytest.approx(
        lower_loading.fore_geometry.foil_vertical_height_m, rel=REL_TOL
    )


def test_pair_preserves_independent_fore_and_aft_geometry() -> None:
    result = calculate_surface_piercing_v_foil_pair(pair_inputs())

    assert result.fore_geometry.dihedral_deg == 30.0
    assert result.aft_geometry.dihedral_deg == 45.0
    assert result.fore_geometry.total_developed_span_m == 2.0
    assert result.aft_geometry.total_developed_span_m == 2.4
    assert result.fore_geometry.wetted_fraction != pytest.approx(
        result.aft_geometry.wetted_fraction
    )
    assert result.fore_geometry.wetted_fraction == pytest.approx(
        result.fore_geometry.apex_submergence_m
        / result.fore_geometry.foil_vertical_height_m,
        rel=REL_TOL,
    )
    assert result.aft_geometry.wetted_fraction == pytest.approx(
        result.aft_geometry.apex_submergence_m
        / result.aft_geometry.foil_vertical_height_m,
        rel=REL_TOL,
    )
    assert result.is_surface_piercing_pair is True


def test_inconsistent_phase_2_area_closure_is_rejected() -> None:
    inputs = pair_inputs()
    inconsistent_phase_2 = replace(
        inputs.foil_area_result,
        fore_area_m2=inputs.foil_area_result.fore_area_m2 + 0.1,
    )

    with pytest.raises(ValueError, match=r"areas do not sum"):
        calculate_surface_piercing_v_foil_pair(
            replace(inputs, foil_area_result=inconsistent_phase_2)
        )


def test_inconsistent_phase_2_force_residual_is_rejected() -> None:
    inputs = pair_inputs()
    inconsistent_phase_2 = replace(
        inputs.foil_area_result,
        total_force_residual_n=1.0,
    )

    with pytest.raises(ValueError, match=r"force residual exceeds"):
        calculate_surface_piercing_v_foil_pair(
            replace(inputs, foil_area_result=inconsistent_phase_2)
        )


def test_tampered_geometry_result_is_rejected_independently() -> None:
    inputs = canonical_inputs()
    result = calculate_surface_piercing_v_foil_geometry(inputs)
    tampered = replace(result, wetted_area_m2=result.wetted_area_m2 + 0.01)

    with pytest.raises(ArithmeticError, match=r"wetted_area_m2 is inconsistent"):
        validate_surface_piercing_v_foil_result(inputs, tampered)
