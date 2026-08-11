"""Reusable validation for scalar numerical inputs."""

from __future__ import annotations

import math
from numbers import Real


def require_finite_real(name: str, value: object) -> float:
    """Return a finite real value as ``float`` while rejecting booleans.

    Args:
        name: Field name used in an error message.
        value: Candidate scalar value.

    Returns:
        The value converted to ``float``.

    Raises:
        TypeError: If ``value`` is a boolean or is not a real number.
        ValueError: If ``value`` is NaN or positive/negative infinity.
    """

    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(
            f"{name} must be a real number and must not be bool; "
            f"received {value!r}."
        )
    float_value = float(value)
    if not math.isfinite(float_value):
        raise ValueError(f"{name} must be finite; received {value!r}.")
    return float_value

