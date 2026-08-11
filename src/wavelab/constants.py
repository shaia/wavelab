"""Physical constants and the course's fixed conventions.

SIGN CONVENTION (fixed project-wide, never varied):

    psi(x, t) = Re[A e^{i(k x - omega t)}]

The time factor is e^{-i omega t}; a wave with positive k travels toward +x; phasors rotate
clockwise. Forward Fourier transforms carry e^{-i.} with the 1/(2 pi) on the inverse — the
same sign `numpy.fft` uses — and an absorbing medium has complex index n + i kappa. The
engineering convention e^{j(omega t - k x)} converts by i <-> -j and appears nowhere in this
codebase.
"""

from __future__ import annotations

from typing import Final

#: Speed of light in vacuum [m/s] (exact — the SI metre is defined from it).
C_LIGHT: Final[float] = 299_792_458.0

#: Vacuum permeability [N/A^2] (CODATA 2018 — measured, no longer exactly 4*pi*1e-7).
MU_0: Final[float] = 1.25663706212e-6

#: Vacuum permittivity [F/m], fixed by c and mu_0 through c^2 = 1/(mu_0 eps_0).
EPS_0: Final[float] = 1.0 / (MU_0 * C_LIGHT**2)

#: The one phase convention this course uses. Referenced by docs and tests so that a change
#: here would be impossible to make silently.
SIGN_CONVENTION: Final[str] = (
    "psi(x,t) = Re[A e^{i(kx - omega t)}]  "
    "(time factor e^{-i omega t}; positive k travels toward +x)"
)
