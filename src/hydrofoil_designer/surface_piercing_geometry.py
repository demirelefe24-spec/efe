"""Canonical geometry calculations for symmetric surface-piercing V-foils."""

from __future__ import annotations

import math

from .surface_piercing_geometry_models import (
    SurfacePiercingVFoilInputs,
    SurfacePiercingVFoilPairInputs,
    SurfacePiercingVFoilPairResult,
    SurfacePiercingVFoilResult,
)
from .surface_piercing_geometry_validation import (
    validate_surface_piercing_v_foil_inputs,
    validate_surface_piercing_v_foil_pair_inputs,
    validate_surface_piercing_v_foil_pair_result,
    validate_surface_piercing_v_foil_result,
)


def calculate_surface_piercing_v_foil_geometry(
    inputs: SurfacePiercingVFoilInputs,
) -> SurfacePiercingVFoilResult:
    """Calculate one straight, symmetric, constant-chord V-foil geometry.

    Both panels share the same developed half-span, chord, and dihedral. The
    calm waterline intersects both panels before their physical tips; hence the
    strict condition ``0 < apex_submergence_m < foil_vertical_height_m``.
    Angles enter the public API in degrees and are converted once here. No
    rounding is applied.
    """

    validate_surface_piercing_v_foil_inputs(inputs)

    dihedral_rad = math.radians(inputs.dihedral_deg)
    sine = math.sin(dihedral_rad)
    cosine = math.cos(dihedral_rad)
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

    result = SurfacePiercingVFoilResult(
        reference_area_m2=inputs.reference_area_m2,
        total_developed_span_m=inputs.total_developed_span_m,
        half_panel_length_m=half_panel_length_m,
        dihedral_deg=inputs.dihedral_deg,
        dihedral_rad=dihedral_rad,
        apex_submergence_m=inputs.apex_submergence_m,
        mean_chord_m=mean_chord_m,
        foil_vertical_height_m=foil_vertical_height_m,
        horizontal_projected_span_m=horizontal_projected_span_m,
        wetted_half_panel_length_m=wetted_half_panel_length_m,
        wetted_area_m2=wetted_area_m2,
        wetted_fraction=wetted_fraction,
        dry_half_panel_length_m=dry_half_panel_length_m,
        emerged_tip_height_m=emerged_tip_height_m,
        waterline_intersection_width_m=waterline_intersection_width_m,
        reference_area_residual_m2=(
            inputs.reference_area_m2
            - mean_chord_m * inputs.total_developed_span_m
        ),
        wetted_area_residual_m2=(
            wetted_area_m2 - wetted_fraction * inputs.reference_area_m2
        ),
        height_residual_m=(
            foil_vertical_height_m
            - (inputs.apex_submergence_m + emerged_tip_height_m)
        ),
        is_surface_piercing=(
            0.0 < inputs.apex_submergence_m < foil_vertical_height_m
        ),
    )
    validate_surface_piercing_v_foil_result(inputs, result)
    return result


def calculate_surface_piercing_v_foil_pair(
    inputs: SurfacePiercingVFoilPairInputs,
) -> SurfacePiercingVFoilPairResult:
    """Apply independent fore/aft geometry to one existing Phase 2 area result.

    This function does not calculate load balance or foil loading. It transfers
    ``fore_area_m2`` and ``aft_area_m2`` directly into the two Phase 3 geometry
    calculations and retains the original Phase 2 result for traceability.
    """

    validate_surface_piercing_v_foil_pair_inputs(inputs)
    phase_2 = inputs.foil_area_result
    fore_geometry = calculate_surface_piercing_v_foil_geometry(
        SurfacePiercingVFoilInputs(
            reference_area_m2=phase_2.fore_area_m2,
            total_developed_span_m=inputs.fore_total_developed_span_m,
            dihedral_deg=inputs.fore_dihedral_deg,
            apex_submergence_m=inputs.fore_apex_submergence_m,
        )
    )
    aft_geometry = calculate_surface_piercing_v_foil_geometry(
        SurfacePiercingVFoilInputs(
            reference_area_m2=phase_2.aft_area_m2,
            total_developed_span_m=inputs.aft_total_developed_span_m,
            dihedral_deg=inputs.aft_dihedral_deg,
            apex_submergence_m=inputs.aft_apex_submergence_m,
        )
    )
    total_reference_area_m2 = math.fsum(
        (fore_geometry.reference_area_m2, aft_geometry.reference_area_m2)
    )

    result = SurfacePiercingVFoilPairResult(
        foil_area_result=phase_2,
        fore_geometry=fore_geometry,
        aft_geometry=aft_geometry,
        total_reference_area_m2=total_reference_area_m2,
        fore_area_transfer_residual_m2=(
            fore_geometry.reference_area_m2 - phase_2.fore_area_m2
        ),
        aft_area_transfer_residual_m2=(
            aft_geometry.reference_area_m2 - phase_2.aft_area_m2
        ),
        pair_area_sum_residual_m2=(
            total_reference_area_m2 - phase_2.total_area_m2
        ),
        is_surface_piercing_pair=(
            fore_geometry.is_surface_piercing
            and aft_geometry.is_surface_piercing
        ),
    )
    validate_surface_piercing_v_foil_pair_result(inputs, result)
    return result
