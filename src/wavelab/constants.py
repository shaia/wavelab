"""Physical constants and the course's fixed conventions.

SIGN CONVENTION (fixed project-wide, never varied):

    dU = δQ + δW_on

Heat δQ is positive when energy flows INTO the system; work δW_on is positive when work is
done ON the system. Both are inexact differentials — they describe transfers along a path,
not properties of a state. Engine efficiencies, which are conventionally written with work
done BY the system, convert explicitly as W_by = -W_on at the one place that needs it.
"""

from __future__ import annotations

from typing import Final

#: Boltzmann constant [J/K] (SI 2019 exact definition).
K_B: Final[float] = 1.380649e-23

#: Avogadro constant [1/mol] (SI 2019 exact definition).
N_A: Final[float] = 6.02214076e23

#: Molar gas constant [J/(mol*K)], exact product of the two above.
R_GAS: Final[float] = K_B * N_A

#: Atomic mass unit [kg] (CODATA 2018).
AMU: Final[float] = 1.66053906660e-27

#: The one work convention this course uses. Referenced by docs and tests so that a change
#: here would be impossible to make silently.
SIGN_CONVENTION: Final[str] = "dU = dQ + dW_on  (work done ON the system is positive)"
