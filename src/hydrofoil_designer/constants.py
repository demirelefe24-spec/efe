"""Physical constants and numerical tolerances used by the calculation core."""

from typing import Final


DEFAULT_GRAVITY_M_S2: Final[float] = 9.80665
"""Standard acceleration of gravity in metres per second squared."""

KILOGRAM_FORCE_TO_NEWTON: Final[float] = DEFAULT_GRAVITY_M_S2
"""Newtons in one kilogram-force under standard gravity."""

POUND_FORCE_TO_NEWTON: Final[float] = 4.4482216152605
"""Newtons in one international avoirdupois pound-force."""

FOOT_TO_METRE: Final[float] = 0.3048
"""Metres in one international foot."""

INCH_TO_METRE: Final[float] = 0.0254
"""Metres in one international inch."""

NAUTICAL_MILE_TO_METRE: Final[float] = 1852.0
"""Metres in one international nautical mile."""

SECONDS_PER_HOUR: Final[float] = 3600.0
"""Seconds in one hour."""

PSF_TO_PASCAL: Final[float] = POUND_FORCE_TO_NEWTON / FOOT_TO_METRE**2
"""Pascals in one pound-force per square foot."""

PSI_TO_PASCAL: Final[float] = POUND_FORCE_TO_NEWTON / INCH_TO_METRE**2
"""Pascals in one pound-force per square inch."""

KNOT_TO_METRE_PER_SECOND: Final[float] = (
    NAUTICAL_MILE_TO_METRE / SECONDS_PER_HOUR
)
"""Metres per second in one knot."""

PUBLICATION_GENERAL_FOIL_LOADING_MIN_KGF_M2: Final[float] = 3000.0
"""Lower end of the publications' general plotting range, in kgf/m²."""

PUBLICATION_GENERAL_FOIL_LOADING_MAX_KGF_M2: Final[float] = 7000.0
"""Upper end of the publications' general plotting range, in kgf/m²."""

PUBLICATION_PRACTICAL_FOIL_LOADING_MIN_KGF_M2: Final[float] = 3800.0
"""Lower end of the publications' practical range, in kgf/m²."""

PUBLICATION_PRACTICAL_FOIL_LOADING_MAX_KGF_M2: Final[float] = 5700.0
"""Upper end of the publications' practical range, in kgf/m²."""

FORCE_RESIDUAL_ABS_TOLERANCE_N: Final[float] = 1.0e-9
"""Absolute floor for the vertical-force equilibrium check, in newtons."""

FORCE_RESIDUAL_REL_TOLERANCE: Final[float] = 1.0e-12
"""Relative tolerance applied to the force scale in the equilibrium check."""

MOMENT_RESIDUAL_ABS_TOLERANCE_NM: Final[float] = 1.0e-9
"""Absolute floor for the moment equilibrium check, in newton-metres."""

MOMENT_RESIDUAL_REL_TOLERANCE: Final[float] = 1.0e-12
"""Relative tolerance applied to the moment scale in the equilibrium check."""

LOAD_FRACTION_ABS_TOLERANCE: Final[float] = 1.0e-12
"""Absolute tolerance for a load-fraction sum of one."""

LOAD_PERCENT_ABS_TOLERANCE: Final[float] = 1.0e-10
"""Absolute tolerance for a load-percentage sum of 100."""

NEGATIVE_LIFT_TOLERANCE_N: Final[float] = 1.0e-9
"""Numerical allowance used when checking for physically invalid negative lift."""

AREA_RESIDUAL_ABS_TOLERANCE_M2: Final[float] = 1.0e-12
"""Absolute floor for foil-area consistency checks, in square metres."""

AREA_RESIDUAL_REL_TOLERANCE: Final[float] = 1.0e-12
"""Relative tolerance applied to the total-area scale."""

AREA_FRACTION_ABS_TOLERANCE: Final[float] = 1.0e-12
"""Absolute tolerance for area and load fraction consistency checks."""

FOIL_LOADING_FORCE_RESIDUAL_ABS_TOLERANCE_N: Final[float] = 1.0e-9
"""Absolute floor for loading-times-area force residuals, in newtons."""

FOIL_LOADING_FORCE_RESIDUAL_REL_TOLERANCE: Final[float] = 1.0e-12
"""Relative tolerance applied to the corresponding force scale."""

FOIL_LOADING_VALUE_ABS_TOLERANCE_N_M2: Final[float] = 1.0e-9
"""Absolute floor for foil-loading value comparisons, in N/m²."""

FOIL_LOADING_VALUE_REL_TOLERANCE: Final[float] = 1.0e-12
"""Relative tolerance applied to a foil-loading value."""

