"""Unit registry for dimensional checks.

The course's numerical code deliberately works in plain SI floats — students should read
`omega0 = np.sqrt(stiffness / mass)`, not a wrapper. Dimensional correctness is therefore
established in the test suite instead: the same formulas are re-evaluated with `pint`
quantities, so a wrong power of a variable fails loudly even when the number looks plausible.
"""

from __future__ import annotations

import pint

#: Shared registry. One instance only — pint quantities from different registries cannot be
#: combined, and a second registry is the usual cause of baffling test errors.
ureg = pint.UnitRegistry()
Quantity = ureg.Quantity

#: The electromagnetic constants as dimensional quantities, for use in test-side formulas.
C_LIGHT_Q = Quantity(299_792_458.0, "meter / second")
MU_0_Q = Quantity(1.25663706212e-6, "newton / ampere**2")
EPS_0_Q = 1.0 / (MU_0_Q * C_LIGHT_Q**2)


def dimensions_of(quantity: Quantity) -> str:
    """Return the dimensionality string of `quantity`, e.g. '[mass]/[length]/[time]**2'."""
    return str(quantity.dimensionality)


def has_dimensions(quantity: Quantity, expected: str) -> bool:
    """True when `quantity` has the dimensionality named by `expected`, e.g. '[pressure]'.

    Used by the dimensional test category: `has_dimensions(p, "[pressure]")`.
    """
    return quantity.check(expected)
