"""Validation for surface-piercing V-foil geometry and Phase 2 integration."""

from __future__ import annotations

import math

from .constants import (
    AREA_FRACTION_ABS_TOLERANCE,
    GEOMETRY_LENGTH_RESIDUAL_ABS_TOLERANCE_M,
    GEOMETRY_LENGTH_RESIDUAL_REL_TOLERANCE,
)
from .foil_loading_models import FoilAreaResult
from .foil_loading_validation import (
    area_residual_tolerance_m2,
    loading_force_residual_tolerance_n,
)
from .numeric_validation import require_finite_real
from .surface_piercing_geometry_models import (
    SurfacePiercingVFoilInputs,
    SurfacePiercingVFoilPairInputs,
    SurfacePiercingVFoilPairResult,
    SurfacePiercingVFoilResult,
)


def length_residual_tolerance_m(length_scale_m: float) -> float:
    """Return the length residual tolerance for a given length scale."""

    return (
        GEOMETRY_LENGTH_RESIDUAL_ABS_TOLERANCE_M
        + GEOMETRY_LENGTH_RESIDUAL_REL_TOLERANCE * abs(length_scale_m)
    )


def validate_surface_piercing_v_foil_inputs(
    inputs: SurfacePiercingVFoilInputs,
) -> None:
    """Validate one V-foil input set and the strict surface-piercing state."""

    if not isinstance(inputs, SurfacePiercingVFoilInputs):
        raise TypeError(
            "inputs must be SurfacePiercingVFoilInputs; "
            f"received {inputs!r}."
        )

    for field_name in inputs.__dataclass_fields__:
        require_finite_real(field_name, getattr(inputs, field_name))

    if inputs.reference_area_m2 <= 0.0:
        raise ValueError(
            "reference_area_m2 must be greater than zero; "
            f"received {inputs.reference_area_m2!r}."
        )
    if inputs.total_developed_span_m <= 0.0:
        raise ValueError(
            "total_developed_span_m must be greater than zero; "
            f"received {inputs.total_developed_span_m!r}."
        )
    if not 0.0 < inputs.dihedral_deg < 90.0:
        raise ValueError(
            "dihedral_deg must be strictly between 0 and 90 degrees; "
            f"received {inputs.dihedral_deg!r}."
        )
    if inputs.apex_submergence_m <= 0.0:
        raise ValueError(
            "apex_submergence_m must be greater than zero; "
            f"received {inputs.apex_submergence_m!r}."
        )

    half_panel_length_m = inputs.total_developed_span_m / 2.0
    foil_vertical_height_m = half_panel_length_m * math.sin(
        math.radians(inputs.dihedral_deg)
    )
    if inputs.apex_submergence_m >= foil_vertical_height_m:
        raise ValueError(
            "A true surface-piercing V-foil requires apex_submergence_m to be "
            "strictly less than foil_vertical_height_m; "
            f"received d={inputs.apex_submergence_m!r} m and "
            f"h_f={foil_vertical_height_m!r} m."
        )


def _assert_close(
    field_name: str,
    actual: float,
    expected: float,
    tolerance: float,
) -> None:
    if not math.isclose(actual, expected, rel_tol=0.0, abs_tol=tolerance):
        raise ArithmeticError(
            f"Calculated {field_name} is inconsistent: "
            f"actual={actual!r}, expected={expected!r}."
        )


def validate_surface_piercing_v_foil_result(
    inputs: SurfacePiercingVFoilInputs,
    result: SurfacePiercingVFoilResult,
) -> None:
    """Independently validate one calculated V-foil result."""

    validate_surface_piercing_v_foil_inputs(inputs)
    if not isinstance(result, SurfacePiercingVFoilResult):
        raise TypeError(
            "result must be SurfacePiercingVFoilResult; "
            f"received {result!r}."
        )

    for field_name in result.__dataclass_fields__:
        value = getattr(result, field_name)
        if field_name == "is_surface_piercing":
            if not isinstance(value, bool):
                raise TypeError("is_surface_piercing must be bool.")
            continue
        require_finite_real(field_name, value)

    angle_rad = math.radians(inputs.dihedral_deg)
    sine = math.sin(angle_rad)
    cosine = math.cos(angle_rad)
    half_panel_length_m = inputs.total_developed_span_m / 2.0
    mean_chord_m = inputs.reference_area_m2 / inputs.total_developed_span_m
    foil_vertical_height_m = half_panel_length_m * sine
    horizontal_projected_span_m = inputs.total_developed_span_m * cosine
    wetted_half_panel_length_m = inputs.apex_submergence_m / sine
    wetted_area_m2 = 2.0 * mean_chord_m * wetted_half_panel_length_m
    wetted_fraction = inputs.apex_submergence_m / foil_vertical_height_m
    dry_half_panel_length_m = half_panel_length_m - wetted_half_panel_length_m
    emerged_tip_height_m = foil_vertical_height_m - inputs.apex_submergence_m
    waterline_intersection_width_m = (
        2.0 * wetted_half_panel_length_m * cosine
    )

    area_tolerance_m2 = area_residual_tolerance_m2(inputs.reference_area_m2)
    length_tolerance_m = length_residual_tolerance_m(
        inputs.total_developed_span_m
    )
    checks = (
        (
            "reference_area_m2",
            result.reference_area_m2,
            inputs.reference_area_m2,
            area_tolerance_m2,
        ),
        (
            "total_developed_span_m",
            result.total_developed_span_m,
            inputs.total_developed_span_m,
            length_tolerance_m,
        ),
        (
            "half_panel_length_m",
            result.half_panel_length_m,
            half_panel_length_m,
            length_tolerance_m,
        ),
        ("dihedral_deg", result.dihedral_deg, inputs.dihedral_deg, 1.0e-12),
        ("dihedral_rad", result.dihedral_rad, angle_rad, 1.0e-14),
        (
            "apex_submergence_m",
            result.apex_submergence_m,
            inputs.apex_submergence_m,
            length_tolerance_m,
        ),
        (
            "mean_chord_m",
            result.mean_chord_m,
            mean_chord_m,
            length_tolerance_m,
        ),
        (
            "foil_vertical_height_m",
            result.foil_vertical_height_m,
            foil_vertical_height_m,
            length_tolerance_m,
        ),
        (
            "horizontal_projected_span_m",
            result.horizontal_projected_span_m,
            horizontal_projected_span_m,
            length_tolerance_m,
        ),
        (
            "wetted_half_panel_length_m",
            result.wetted_half_panel_length_m,
            wetted_half_panel_length_m,
            length_tolerance_m,
        ),
        (
            "wetted_area_m2",
            result.wetted_area_m2,
            wetted_area_m2,
            area_tolerance_m2,
        ),
        (
            "wetted_fraction",
            result.wetted_fraction,
            wetted_fraction,
            AREA_FRACTION_ABS_TOLERANCE,
        ),
        (
            "dry_half_panel_length_m",
            result.dry_half_panel_length_m,
            dry_half_panel_length_m,
            length_tolerance_m,
        ),
        (
            "emerged_tip_height_m",
            result.emerged_tip_height_m,
            emerged_tip_height_m,
            length_tolerance_m,
        ),
        (
            "waterline_intersection_width_m",
            result.waterline_intersection_width_m,
            waterline_intersection_width_m,
            length_tolerance_m,
        ),
    )
    for field_name, actual, expected, tolerance in checks:
        _assert_close(field_name, actual, expected, tolerance)

    expected_reference_area_residual_m2 = (
        inputs.reference_area_m2
        - mean_chord_m * inputs.total_developed_span_m
    )
    expected_wetted_area_residual_m2 = (
        wetted_area_m2 - wetted_fraction * inputs.reference_area_m2
    )
    expected_height_residual_m = (
        foil_vertical_height_m
        - (inputs.apex_submergence_m + emerged_tip_height_m)
    )
    residual_checks = (
        (
            "reference_area_residual_m2",
            result.reference_area_residual_m2,
            expected_reference_area_residual_m2,
            area_tolerance_m2,
        ),
        (
            "wetted_area_residual_m2",
            result.wetted_area_residual_m2,
            expected_wetted_area_residual_m2,
            area_tolerance_m2,
        ),
        (
            "height_residual_m",
            result.height_residual_m,
            expected_height_residual_m,
            length_tolerance_m,
        ),
    )
    for field_name, actual, expected, tolerance in residual_checks:
        _assert_close(field_name, actual, expected, tolerance)
        if abs(expected) > tolerance:
            raise ArithmeticError(f"{field_name} exceeds its closure tolerance.")

    if not result.is_surface_piercing:
        raise ArithmeticError("Calculated geometry must be surface-piercing.")


def validate_phase_2_foil_area_result(result: FoilAreaResult) -> None:
    """Validate the self-contained Phase 2 fields required by Phase 3.

    Phase 3 deliberately receives the immutable Phase 2 result rather than
    recomputing loads or areas. The checks therefore use only closures stored in
    that result and quantities independently recoverable from its own fields.
    """

    if not isinstance(result, FoilAreaResult):
        raise TypeError(
            "foil_area_result must be FoilAreaResult from the Phase 2 API; "
            f"received {result!r}."
        )
    for field_name in result.__dataclass_fields__:
        require_finite_real(field_name, getattr(result, field_name))

    if result.foil_loading_n_m2 <= 0.0:
        raise ValueError("Phase 2 foil_loading_n_m2 must be greater than zero.")
    for field_name in ("total_area_m2", "fore_area_m2", "aft_area_m2"):
        if getattr(result, field_name) <= 0.0:
            raise ValueError(f"Phase 2 {field_name} must be greater than zero.")

    area_tolerance_m2 = area_residual_tolerance_m2(result.total_area_m2)
    recomputed_area_residual_m2 = math.fsum(
        (result.fore_area_m2, result.aft_area_m2, -result.total_area_m2)
    )
    if abs(recomputed_area_residual_m2) > area_tolerance_m2:
        raise ValueError("Phase 2 fore and aft areas do not sum to total area.")
    if not math.isclose(
        result.area_sum_residual_m2,
        recomputed_area_residual_m2,
        rel_tol=0.0,
        abs_tol=area_tolerance_m2,
    ):
        raise ValueError("Phase 2 area_sum_residual_m2 is inconsistent.")

    expected_fore_fraction = result.fore_area_m2 / result.total_area_m2
    expected_aft_fraction = result.aft_area_m2 / result.total_area_m2
    fraction_checks = (
        ("fore_area_fraction", result.fore_area_fraction, expected_fore_fraction),
        ("aft_area_fraction", result.aft_area_fraction, expected_aft_fraction),
    )
    for field_name, actual, expected in fraction_checks:
        if not math.isclose(
            actual,
            expected,
            rel_tol=0.0,
            abs_tol=AREA_FRACTION_ABS_TOLERANCE,
        ):
            raise ValueError(f"Phase 2 {field_name} is inconsistent with its areas.")
    if not math.isclose(
        result.fore_area_fraction + result.aft_area_fraction,
        1.0,
        rel_tol=0.0,
        abs_tol=AREA_FRACTION_ABS_TOLERANCE,
    ):
        raise ValueError("Phase 2 area fractions do not sum to one.")

    force_residuals = (
        (result.total_force_residual_n, result.total_area_m2),
        (result.fore_force_residual_n, result.fore_area_m2),
        (result.aft_force_residual_n, result.aft_area_m2),
    )
    for residual_n, area_m2 in force_residuals:
        force_scale_n = result.foil_loading_n_m2 * area_m2
        if abs(residual_n) > loading_force_residual_tolerance_n(force_scale_n):
            raise ValueError("A Phase 2 force residual exceeds its tolerance.")
    for field_name in (
        "fore_area_fraction_residual",
        "aft_area_fraction_residual",
    ):
        if abs(getattr(result, field_name)) > AREA_FRACTION_ABS_TOLERANCE:
            raise ValueError(f"Phase 2 {field_name} exceeds its tolerance.")


def validate_surface_piercing_v_foil_pair_inputs(
    inputs: SurfacePiercingVFoilPairInputs,
) -> None:
    """Validate the Phase 2 hand-off and both fore/aft geometry input sets."""

    if not isinstance(inputs, SurfacePiercingVFoilPairInputs):
        raise TypeError(
            "inputs must be SurfacePiercingVFoilPairInputs; "
            f"received {inputs!r}."
        )
    validate_phase_2_foil_area_result(inputs.foil_area_result)
    validate_surface_piercing_v_foil_inputs(
        SurfacePiercingVFoilInputs(
            reference_area_m2=inputs.foil_area_result.fore_area_m2,
            total_developed_span_m=inputs.fore_total_developed_span_m,
            dihedral_deg=inputs.fore_dihedral_deg,
            apex_submergence_m=inputs.fore_apex_submergence_m,
        )
    )
    validate_surface_piercing_v_foil_inputs(
        SurfacePiercingVFoilInputs(
            reference_area_m2=inputs.foil_area_result.aft_area_m2,
            total_developed_span_m=inputs.aft_total_developed_span_m,
            dihedral_deg=inputs.aft_dihedral_deg,
            apex_submergence_m=inputs.aft_apex_submergence_m,
        )
    )


def validate_surface_piercing_v_foil_pair_result(
    inputs: SurfacePiercingVFoilPairInputs,
    result: SurfacePiercingVFoilPairResult,
) -> None:
    """Validate both geometries and every Phase 2 area-transfer closure."""

    validate_surface_piercing_v_foil_pair_inputs(inputs)
    if not isinstance(result, SurfacePiercingVFoilPairResult):
        raise TypeError(
            "result must be SurfacePiercingVFoilPairResult; "
            f"received {result!r}."
        )
    if result.foil_area_result is not inputs.foil_area_result:
        raise ArithmeticError(
            "The pair result must preserve the Phase 2 result object."
        )

    fore_inputs = SurfacePiercingVFoilInputs(
        inputs.foil_area_result.fore_area_m2,
        inputs.fore_total_developed_span_m,
        inputs.fore_dihedral_deg,
        inputs.fore_apex_submergence_m,
    )
    aft_inputs = SurfacePiercingVFoilInputs(
        inputs.foil_area_result.aft_area_m2,
        inputs.aft_total_developed_span_m,
        inputs.aft_dihedral_deg,
        inputs.aft_apex_submergence_m,
    )
    validate_surface_piercing_v_foil_result(fore_inputs, result.fore_geometry)
    validate_surface_piercing_v_foil_result(aft_inputs, result.aft_geometry)

    for field_name in (
        "total_reference_area_m2",
        "fore_area_transfer_residual_m2",
        "aft_area_transfer_residual_m2",
        "pair_area_sum_residual_m2",
    ):
        require_finite_real(field_name, getattr(result, field_name))
    if not isinstance(result.is_surface_piercing_pair, bool):
        raise TypeError("is_surface_piercing_pair must be bool.")

    total_reference_area_m2 = math.fsum(
        (
            result.fore_geometry.reference_area_m2,
            result.aft_geometry.reference_area_m2,
        )
    )
    expected_residuals = (
        (
            "fore_area_transfer_residual_m2",
            result.fore_geometry.reference_area_m2
            - inputs.foil_area_result.fore_area_m2,
        ),
        (
            "aft_area_transfer_residual_m2",
            result.aft_geometry.reference_area_m2
            - inputs.foil_area_result.aft_area_m2,
        ),
        (
            "pair_area_sum_residual_m2",
            total_reference_area_m2
            - inputs.foil_area_result.total_area_m2,
        ),
    )
    tolerance_m2 = area_residual_tolerance_m2(
        inputs.foil_area_result.total_area_m2
    )
    _assert_close(
        "total_reference_area_m2",
        result.total_reference_area_m2,
        total_reference_area_m2,
        tolerance_m2,
    )
    for field_name, expected in expected_residuals:
        actual = getattr(result, field_name)
        _assert_close(field_name, actual, expected, tolerance_m2)
        if abs(expected) > tolerance_m2:
            raise ArithmeticError(f"{field_name} exceeds its closure tolerance.")
    if not result.is_surface_piercing_pair:
        raise ArithmeticError("Both geometries must be surface-piercing.")
