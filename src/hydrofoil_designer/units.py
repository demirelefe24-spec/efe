"""Explicit, testable unit conversions used by the design calculations."""

from __future__ import annotations

from .constants import (
    KILOGRAM_FORCE_TO_NEWTON,
    KNOT_TO_METRE_PER_SECOND,
    PSF_TO_PASCAL,
    PSI_TO_PASCAL,
)
from .numeric_validation import require_finite_real


def kgf_to_n(value_kgf: float) -> float:
    """Convert kilogram-force to newtons using standard gravity.

    Args:
        value_kgf: Force in kilogram-force.

    Returns:
        Force in newtons.
    """

    value = require_finite_real("value_kgf", value_kgf)
    return value * KILOGRAM_FORCE_TO_NEWTON


def kgf_per_m2_to_n_per_m2(value_kgf_m2: float) -> float:
    """Convert legacy loading from kgf/m² to N/m².

    Args:
        value_kgf_m2: Force-based loading in kilogram-force per square metre.

    Returns:
        Force-based loading in newtons per square metre.
    """

    value = require_finite_real("value_kgf_m2", value_kgf_m2)
    return value * KILOGRAM_FORCE_TO_NEWTON


def psf_to_pa(value_psf: float) -> float:
    """Convert pound-force per square foot to pascals.

    Args:
        value_psf: Pressure or force-based loading in lbf/ft².

    Returns:
        The corresponding value in pascals.
    """

    value = require_finite_real("value_psf", value_psf)
    return value * PSF_TO_PASCAL


def psi_to_pa(value_psi: float) -> float:
    """Convert pound-force per square inch to pascals.

    Args:
        value_psi: Pressure or force-based loading in lbf/in².

    Returns:
        The corresponding value in pascals.
    """

    value = require_finite_real("value_psi", value_psi)
    return value * PSI_TO_PASCAL


def knots_to_m_s(value_knots: float) -> float:
    """Convert knots to metres per second.

    Args:
        value_knots: Speed in international knots.

    Returns:
        Speed in metres per second.
    """

    value = require_finite_real("value_knots", value_knots)
    return value * KNOT_TO_METRE_PER_SECOND
