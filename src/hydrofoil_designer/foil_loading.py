"""Force-based foil-loading and reference-area calculations."""

from __future__ import annotations

import math

from .foil_loading_models import (
    FoilAreaInputs,
    FoilAreaResult,
    FoilLoadingScanInputs,
    FoilLoadingScanResult,
)
from .foil_loading_validation import (
    validate_foil_area_inputs,
    validate_foil_area_result,
    validate_foil_loading_scan_inputs,
    validate_foil_loading_scan_result,
)


def calculate_foil_areas(inputs: FoilAreaInputs) -> FoilAreaResult:
    """Calculate total, fore, and aft reference areas for one common loading.

    The canonical loading is force per reference area in N/m². The result does
    not define a span, chord, dihedral geometry, or speed-dependent wetted area.
    No rounding is applied.

    Args:
        inputs: A validated Phase 1 load result and one common fore/aft foil
            loading in N/m².

    Returns:
        Total, fore, and aft reference areas in m², their fractions, and
        independent area, force, and fraction residuals.

    Raises:
        TypeError: If a model field has the wrong type or is boolean.
        ValueError: If an input is non-finite, non-positive, or physically
            inconsistent with the Phase 1 force balance.
        ArithmeticError: If a calculated result fails an independent check.
    """

    validate_foil_area_inputs(inputs)
    load_balance = inputs.load_balance
    foil_loading_n_m2 = inputs.foil_loading_n_m2

    total_area_m2 = load_balance.weight_n / foil_loading_n_m2
    fore_area_m2 = load_balance.fore_lift_n / foil_loading_n_m2
    aft_area_m2 = load_balance.aft_lift_n / foil_loading_n_m2
    fore_area_fraction = fore_area_m2 / total_area_m2
    aft_area_fraction = aft_area_m2 / total_area_m2

    result = FoilAreaResult(
        foil_loading_n_m2=foil_loading_n_m2,
        total_area_m2=total_area_m2,
        fore_area_m2=fore_area_m2,
        aft_area_m2=aft_area_m2,
        fore_area_fraction=fore_area_fraction,
        aft_area_fraction=aft_area_fraction,
        area_sum_residual_m2=math.fsum(
            (fore_area_m2, aft_area_m2, -total_area_m2)
        ),
        total_force_residual_n=(
            foil_loading_n_m2 * total_area_m2 - load_balance.weight_n
        ),
        fore_force_residual_n=(
            foil_loading_n_m2 * fore_area_m2 - load_balance.fore_lift_n
        ),
        aft_force_residual_n=(
            foil_loading_n_m2 * aft_area_m2 - load_balance.aft_lift_n
        ),
        fore_area_fraction_residual=(
            fore_area_fraction - load_balance.fore_load_fraction
        ),
        aft_area_fraction_residual=(
            aft_area_fraction - load_balance.aft_load_fraction
        ),
    )
    validate_foil_area_result(inputs, result)
    return result


def scan_foil_loadings(inputs: FoilLoadingScanInputs) -> FoilLoadingScanResult:
    """Return an inclusive deterministic scan ordered by increasing loading.

    A linearly spaced ``sample_count`` is used. The first point is minimum
    loading and maximum area; the last is maximum loading and minimum area.

    Args:
        inputs: Phase 1 result, explicit minimum/maximum loading in N/m², and
            the inclusive sample count.

    Returns:
        Ordered scan metadata and one fully validated area result per point.

    Raises:
        TypeError: If a field has the wrong type or is boolean.
        ValueError: If bounds/count are invalid or the Phase 1 result is
            physically inconsistent.
        ArithmeticError: If any point or monotonicity check fails.
    """

    validate_foil_loading_scan_inputs(inputs)
    if inputs.sample_count == 1:
        loadings = (inputs.min_foil_loading_n_m2,)
    else:
        step = (
            inputs.max_foil_loading_n_m2 - inputs.min_foil_loading_n_m2
        ) / (inputs.sample_count - 1)
        loadings = tuple(
            inputs.min_foil_loading_n_m2 + index * step
            for index in range(inputs.sample_count - 1)
        ) + (inputs.max_foil_loading_n_m2,)

    points = tuple(
        calculate_foil_areas(FoilAreaInputs(inputs.load_balance, loading))
        for loading in loadings
    )
    result = FoilLoadingScanResult(
        min_foil_loading_n_m2=inputs.min_foil_loading_n_m2,
        max_foil_loading_n_m2=inputs.max_foil_loading_n_m2,
        sample_count=inputs.sample_count,
        points=points,
    )
    validate_foil_loading_scan_result(inputs, result)
    return result
