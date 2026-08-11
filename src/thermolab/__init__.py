"""ThermoLab — the physics behind the course.

Every model the notebooks and pages use lives here, in plain vectorized NumPy, so that a
student can read the implementation of any claim the course makes. Notebooks orchestrate
lessons; they never re-implement physics.

Modules:
    constants     physical constants and the fixed sign convention
    units         pint registry used by the dimensional tests
    sampling      independent draws and sample averages; the N^(-1/2) law at its simplest
    forms         differential forms in the plane; exact versus inexact, as pure mathematics
    kinetics      free particles in a box; the microscopic origin of pressure
    paths         quasistatic paths in the P-V plane; work as a path function
    multiplicity  microstate counting, entropy, and why equilibrium wins
    validation    the reusable accuracy checks (seeds, convergence, scaling)
"""

from __future__ import annotations

from . import forms, kinetics, multiplicity, paths, sampling, units, validation
from .constants import AMU, K_B, N_A, R_GAS, SIGN_CONVENTION

__all__ = [
    "AMU",
    "K_B",
    "N_A",
    "R_GAS",
    "SIGN_CONVENTION",
    "forms",
    "kinetics",
    "multiplicity",
    "paths",
    "sampling",
    "units",
    "validation",
]
