"""Unit registry for dimensional checks.

The course's numerical code deliberately works in plain SI floats — students should read
`P = N * K_B * T / V`, not a wrapper. Dimensional correctness is therefore established in the
test suite instead: the same formulas are re-evaluated with `pint` quantities, so a wrong
power of a variable fails loudly even when the number looks plausible.
"""

from __future__ import annotations

import pint

#: Shared registry. One instance only — pint quantities from different registries cannot be
#: combined, and a second registry is the usual cause of baffling test errors.
ureg = pint.UnitRegistry()
Quantity = ureg.Quantity

#: Boltzmann constant as a dimensional quantity, for use in test-side formulas.
K_B_Q = Quantity(1.380649e-23, "joule / kelvin")


def dimensions_of(quantity: Quantity) -> str:
    """Return the dimensionality string of `quantity`, e.g. '[mass]/[length]/[time]**2'."""
    return str(quantity.dimensionality)


def has_dimensions(quantity: Quantity, expected: str) -> bool:
    """True when `quantity` has the dimensionality named by `expected`, e.g. '[pressure]'.

    Used by the dimensional test category: `has_dimensions(p, "[pressure]")`.
    """
    return quantity.check(expected)
