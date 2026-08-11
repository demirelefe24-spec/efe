"""Validation for foil-loading inputs, areas, residuals, and scans."""

from __future__ import annotations

import math

from .constants import (
    AREA_FRACTION_ABS_TOLERANCE,
    AREA_RESIDUAL_ABS_TOLERANCE_M2,
    AREA_RESIDUAL_REL_TOLERANCE,
    FOIL_LOADING_FORCE_RESIDUAL_ABS_TOLERANCE_N,
    FOIL_LOADING_FORCE_RESIDUAL_REL_TOLERANCE,
    FOIL_LOADING_VALUE_ABS_TOLERANCE_N_M2,
    FOIL_LOADING_VALUE_REL_TOLERANCE,
    LOAD_FRACTION_ABS_TOLERANCE,
    LOAD_PERCENT_ABS_TOLERANCE,
)
from .foil_loading_models import (
    FoilAreaInputs,
    FoilAreaResult,
    FoilLoadingScanInputs,
    FoilLoadingScanResult,
)
from .models import LoadBalanceResult
from .numeric_validation import require_finite_real


def area_residual_tolerance_m2(area_scale_m2: float) -> float:
    """Return the area residual tolerance for a given area scale."""

    return (
        AREA_RESIDUAL_ABS_TOLERANCE_M2
        + AREA_RESIDUAL_REL_TOLERANCE * abs(area_scale_m2)
    )


def loading_force_residual_tolerance_n(force_scale_n: float) -> float:
    """Return the loading-times-area force residual tolerance."""

    return (
        FOIL_LOADING_FORCE_RESIDUAL_ABS_TOLERANCE_N
        + FOIL_LOADING_FORCE_RESIDUAL_REL_TOLERANCE * abs(force_scale_n)
    )


def foil_loading_value_tolerance_n_m2(loading_n_m2: float) -> float:
    """Return the tolerance used when comparing foil-loading values."""

    return (
        FOIL_LOADING_VALUE_ABS_TOLERANCE_N_M2
        + FOIL_LOADING_VALUE_REL_TOLERANCE * abs(loading_n_m2)
    )


def validate_load_balance_for_foil_loading(result: LoadBalanceResult) -> None:
    """Validate the Phase 1 values required by the Phase 2 area calculation."""

    if not isinstance(result, LoadBalanceResult):
        raise TypeError(
            "load_balance must be a LoadBalanceResult from the Phase 1 API; "
            f"received {result!r}."
        )

    for field_name in result.__dataclass_fields__:
        require_finite_real(field_name, getattr(result, field_name))

    if result.weight_n <= 0.0:
        raise ValueError(f"weight_n must be greater than zero; got {result.weight_n!r}.")
    if result.fore_lift_n <= 0.0:
        raise ValueError(
            f"fore_lift_n must be greater than zero; got {result.fore_lift_n!r}."
        )
    if result.aft_lift_n <= 0.0:
        raise ValueError(
            f"aft_lift_n must be greater than zero; got {result.aft_lift_n!r}."
        )

    force_tolerance_n = loading_force_residual_tolerance_n(result.weight_n)
    recomputed_force_residual_n = math.fsum(
        (result.fore_lift_n, result.aft_lift_n, -result.weight_n)
    )
    if abs(recomputed_force_residual_n) > force_tolerance_n:
        raise ValueError(
            "Phase 1 forces are inconsistent: fore_lift_n + aft_lift_n must "
            f"equal weight_n within {force_tolerance_n!r} N; residual is "
            f"{recomputed_force_residual_n!r} N."
        )
    if not math.isclose(
        result.vertical_force_residual_n,
        recomputed_force_residual_n,
        rel_tol=0.0,
        abs_tol=force_tolerance_n,
    ):
        raise ValueError(
            "Phase 1 vertical_force_residual_n is inconsistent with the forces."
        )

    expected_fore_fraction = result.fore_lift_n / result.weight_n
    expected_aft_fraction = result.aft_lift_n / result.weight_n
    fraction_checks = (
        ("fore_load_fraction", result.fore_load_fraction, expected_fore_fraction),
        ("aft_load_fraction", result.aft_load_fraction, expected_aft_fraction),
    )
    for name, actual, expected in fraction_checks:
        if not math.isclose(
            actual,
            expected,
            rel_tol=0.0,
            abs_tol=LOAD_FRACTION_ABS_TOLERANCE,
        ):
            raise ValueError(
                f"Phase 1 {name} is inconsistent with its lift/weight ratio: "
                f"actual={actual!r}, expected={expected!r}."
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
        raise ValueError("Phase 1 load percentages are inconsistent with fractions.")


def validate_foil_area_inputs(inputs: FoilAreaInputs) -> None:
    """Validate Phase 2 inputs and the reused Phase 1 result."""

    if not isinstance(inputs, FoilAreaInputs):
        raise TypeError(f"inputs must be FoilAreaInputs; received {inputs!r}.")
    validate_load_balance_for_foil_loading(inputs.load_balance)
    foil_loading = require_finite_real(
        "foil_loading_n_m2", inputs.foil_loading_n_m2
    )
    if foil_loading <= 0.0:
        raise ValueError(
            "foil_loading_n_m2 must be greater than zero; "
            f"received {inputs.foil_loading_n_m2!r}."
        )


def validate_foil_area_result(
    inputs: FoilAreaInputs, result: FoilAreaResult
) -> None:
    """Independently validate calculated areas, fractions, and residuals."""

    if not isinstance(result, FoilAreaResult):
        raise TypeError(f"result must be FoilAreaResult; received {result!r}.")
    validate_foil_area_inputs(inputs)
    for field_name in result.__dataclass_fields__:
        require_finite_real(field_name, getattr(result, field_name))

    for field_name in ("total_area_m2", "fore_area_m2", "aft_area_m2"):
        value = getattr(result, field_name)
        if value <= 0.0:
            raise ArithmeticError(
                f"Calculated {field_name} must be greater than zero; got {value!r}."
            )

    loading_tolerance = foil_loading_value_tolerance_n_m2(
        inputs.foil_loading_n_m2
    )
    if not math.isclose(
        result.foil_loading_n_m2,
        inputs.foil_loading_n_m2,
        rel_tol=0.0,
        abs_tol=loading_tolerance,
    ):
        raise ArithmeticError(
            "Result foil_loading_n_m2 is inconsistent with the input loading."
        )

    load_balance = inputs.load_balance
    expected_areas = (
        ("total_area_m2", load_balance.weight_n / inputs.foil_loading_n_m2),
        ("fore_area_m2", load_balance.fore_lift_n / inputs.foil_loading_n_m2),
        ("aft_area_m2", load_balance.aft_lift_n / inputs.foil_loading_n_m2),
    )
    for field_name, expected in expected_areas:
        actual = getattr(result, field_name)
        if not math.isclose(
            actual,
            expected,
            rel_tol=0.0,
            abs_tol=area_residual_tolerance_m2(expected),
        ):
            raise ArithmeticError(
                f"Calculated {field_name} is inconsistent with force/loading: "
                f"actual={actual!r}, expected={expected!r}."
            )

    recomputed_area_residual_m2 = math.fsum(
        (result.fore_area_m2, result.aft_area_m2, -result.total_area_m2)
    )
    area_tolerance_m2 = area_residual_tolerance_m2(result.total_area_m2)
    if not math.isclose(
        result.area_sum_residual_m2,
        recomputed_area_residual_m2,
        rel_tol=0.0,
        abs_tol=area_tolerance_m2,
    ):
        raise ArithmeticError(
            "Stored area_sum_residual_m2 is inconsistent with the areas."
        )
    if abs(recomputed_area_residual_m2) > area_tolerance_m2:
        raise ArithmeticError(
            "Fore and aft areas do not sum to total area within tolerance."
        )

    force_residuals = (
        (
            "total_force_residual_n",
            result.foil_loading_n_m2 * result.total_area_m2 - load_balance.weight_n,
            load_balance.weight_n,
        ),
        (
            "fore_force_residual_n",
            result.foil_loading_n_m2 * result.fore_area_m2
            - load_balance.fore_lift_n,
            load_balance.fore_lift_n,
        ),
        (
            "aft_force_residual_n",
            result.foil_loading_n_m2 * result.aft_area_m2 - load_balance.aft_lift_n,
            load_balance.aft_lift_n,
        ),
    )
    for field_name, recomputed, force_scale in force_residuals:
        tolerance_n = loading_force_residual_tolerance_n(force_scale)
        stored = getattr(result, field_name)
        if not math.isclose(
            stored, recomputed, rel_tol=0.0, abs_tol=tolerance_n
        ):
            raise ArithmeticError(
                f"Stored {field_name} is inconsistent with an independent "
                f"recalculation: stored={stored!r}, recomputed={recomputed!r}."
            )
        if abs(recomputed) > tolerance_n:
            raise ArithmeticError(
                f"{field_name} exceeds tolerance: residual={recomputed!r} N, "
                f"tolerance={tolerance_n!r} N."
            )

    expected_fore_area_fraction = result.fore_area_m2 / result.total_area_m2
    expected_aft_area_fraction = result.aft_area_m2 / result.total_area_m2
    area_fraction_checks = (
        (
            "fore_area_fraction",
            result.fore_area_fraction,
            expected_fore_area_fraction,
        ),
        (
            "aft_area_fraction",
            result.aft_area_fraction,
            expected_aft_area_fraction,
        ),
    )
    for field_name, actual, expected in area_fraction_checks:
        if not math.isclose(
            actual,
            expected,
            rel_tol=0.0,
            abs_tol=AREA_FRACTION_ABS_TOLERANCE,
        ):
            raise ArithmeticError(
                f"Calculated {field_name} is inconsistent with the areas."
            )

    fraction_residuals = (
        (
            "fore_area_fraction_residual",
            expected_fore_area_fraction - load_balance.fore_load_fraction,
        ),
        (
            "aft_area_fraction_residual",
            expected_aft_area_fraction - load_balance.aft_load_fraction,
        ),
    )
    for field_name, recomputed in fraction_residuals:
        stored = getattr(result, field_name)
        if not math.isclose(
            stored,
            recomputed,
            rel_tol=0.0,
            abs_tol=AREA_FRACTION_ABS_TOLERANCE,
        ):
            raise ArithmeticError(
                f"Stored {field_name} is inconsistent with the area/load ratios."
            )
        if abs(recomputed) > AREA_FRACTION_ABS_TOLERANCE:
            raise ArithmeticError(
                f"{field_name} exceeds tolerance: residual={recomputed!r}."
            )


def validate_foil_loading_scan_inputs(inputs: FoilLoadingScanInputs) -> None:
    """Validate an inclusive scan range and sample count."""

    if not isinstance(inputs, FoilLoadingScanInputs):
        raise TypeError(
            f"inputs must be FoilLoadingScanInputs; received {inputs!r}."
        )
    validate_load_balance_for_foil_loading(inputs.load_balance)
    minimum = require_finite_real(
        "min_foil_loading_n_m2", inputs.min_foil_loading_n_m2
    )
    maximum = require_finite_real(
        "max_foil_loading_n_m2", inputs.max_foil_loading_n_m2
    )
    if minimum <= 0.0:
        raise ValueError(
            "min_foil_loading_n_m2 must be greater than zero; "
            f"received {inputs.min_foil_loading_n_m2!r}."
        )
    if maximum <= 0.0:
        raise ValueError(
            "max_foil_loading_n_m2 must be greater than zero; "
            f"received {inputs.max_foil_loading_n_m2!r}."
        )
    if minimum > maximum:
        raise ValueError(
            "min_foil_loading_n_m2 must not exceed max_foil_loading_n_m2; "
            f"received min={minimum!r}, max={maximum!r}."
        )
    if isinstance(inputs.sample_count, bool) or not isinstance(inputs.sample_count, int):
        raise TypeError(
            "sample_count must be an integer and must not be bool; "
            f"received {inputs.sample_count!r}."
        )
    if inputs.sample_count <= 0:
        raise ValueError(
            f"sample_count must be greater than zero; got {inputs.sample_count!r}."
        )
    if minimum < maximum and inputs.sample_count < 2:
        raise ValueError(
            "sample_count must be at least 2 when minimum and maximum loadings differ."
        )
    if minimum == maximum and inputs.sample_count != 1:
        raise ValueError(
            "sample_count must be 1 when minimum and maximum loadings are equal."
        )


def validate_foil_loading_scan_result(
    inputs: FoilLoadingScanInputs, result: FoilLoadingScanResult
) -> None:
    """Validate scan endpoints, point count, residuals, and monotonic behaviour."""

    if not isinstance(result, FoilLoadingScanResult):
        raise TypeError(
            f"result must be FoilLoadingScanResult; received {result!r}."
        )
    validate_foil_loading_scan_inputs(inputs)
    if result.sample_count != inputs.sample_count:
        raise ArithmeticError("Scan result sample_count differs from its input.")
    if len(result.points) != inputs.sample_count:
        raise ArithmeticError("Scan point count differs from sample_count.")

    for field_name in (
        "min_foil_loading_n_m2",
        "max_foil_loading_n_m2",
    ):
        actual = require_finite_real(field_name, getattr(result, field_name))
        expected = getattr(inputs, field_name)
        if not math.isclose(
            actual,
            expected,
            rel_tol=0.0,
            abs_tol=foil_loading_value_tolerance_n_m2(expected),
        ):
            raise ArithmeticError(f"Scan result {field_name} differs from its input.")

    if inputs.sample_count == 1:
        expected_loadings = (inputs.min_foil_loading_n_m2,)
    else:
        step = (
            inputs.max_foil_loading_n_m2 - inputs.min_foil_loading_n_m2
        ) / (inputs.sample_count - 1)
        expected_loadings = tuple(
            inputs.min_foil_loading_n_m2 + index * step
            for index in range(inputs.sample_count - 1)
        ) + (inputs.max_foil_loading_n_m2,)

    previous_point: FoilAreaResult | None = None
    for point, expected_loading in zip(result.points, expected_loadings, strict=True):
        validate_foil_area_result(
            FoilAreaInputs(inputs.load_balance, expected_loading), point
        )
        if previous_point is not None:
            if point.foil_loading_n_m2 <= previous_point.foil_loading_n_m2:
                raise ArithmeticError("Foil loading must increase across the scan.")
            if point.total_area_m2 >= previous_point.total_area_m2:
                raise ArithmeticError(
                    "Total area must decrease as foil loading increases."
                )
        previous_point = point

