"""Data models for symmetric, straight, constant-chord surface-piercing V-foils."""

from __future__ import annotations

from dataclasses import dataclass

from .foil_loading_models import FoilAreaResult


@dataclass(frozen=True, slots=True)
class SurfacePiercingVFoilInputs:
    """Inputs for one symmetric surface-piercing V-foil.

    ``reference_area_m2`` is the combined dry/reference planform area of both
    complete panels measured in their foil planes. ``total_developed_span_m``
    is the sum of the two physical inclined panel lengths. Dihedral is the
    angle each panel makes with the horizontal. ``apex_submergence_m`` is
    positive downward from the calm waterline to the lowest V apex.
    """

    reference_area_m2: float
    total_developed_span_m: float
    dihedral_deg: float
    apex_submergence_m: float


@dataclass(frozen=True, slots=True)
class SurfacePiercingVFoilResult:
    """Calculated geometry, wetted quantities, and closure residuals."""

    reference_area_m2: float
    total_developed_span_m: float
    half_panel_length_m: float
    dihedral_deg: float
    dihedral_rad: float
    apex_submergence_m: float
    mean_chord_m: float
    foil_vertical_height_m: float
    horizontal_projected_span_m: float
    wetted_half_panel_length_m: float
    wetted_area_m2: float
    wetted_fraction: float
    dry_half_panel_length_m: float
    emerged_tip_height_m: float
    waterline_intersection_width_m: float
    reference_area_residual_m2: float
    wetted_area_residual_m2: float
    height_residual_m: float
    is_surface_piercing: bool


@dataclass(frozen=True, slots=True)
class SurfacePiercingVFoilPairInputs:
    """Fore/aft V-foil geometry inputs tied directly to a Phase 2 result.

    The fore and aft reference areas are deliberately not repeated here. They
    are transferred from ``foil_area_result`` so the Phase 3 API cannot silently
    diverge from the Phase 2 sizing result.
    """

    foil_area_result: FoilAreaResult
    fore_total_developed_span_m: float
    fore_dihedral_deg: float
    fore_apex_submergence_m: float
    aft_total_developed_span_m: float
    aft_dihedral_deg: float
    aft_apex_submergence_m: float


@dataclass(frozen=True, slots=True)
class SurfacePiercingVFoilPairResult:
    """Fore/aft geometry results and Phase 2 area-transfer closures."""

    foil_area_result: FoilAreaResult
    fore_geometry: SurfacePiercingVFoilResult
    aft_geometry: SurfacePiercingVFoilResult
    total_reference_area_m2: float
    fore_area_transfer_residual_m2: float
    aft_area_transfer_residual_m2: float
    pair_area_sum_residual_m2: float
    is_surface_piercing_pair: bool
