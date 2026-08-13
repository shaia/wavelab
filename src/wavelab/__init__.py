"""WaveLab — the physics behind the course.

Every model the notebooks and pages use lives here, in plain vectorized NumPy, so that a
student can read the implementation of any claim the course makes. Notebooks orchestrate
lessons; they never re-implement physics.

Modules:
    constants     physical constants and the fixed phase convention
    units         pint registry used by the dimensional tests
    phasors       rotating complex amplitudes; superposition, beats, random-phase sums
    oscillators   the harmonic oscillator — free, damped, driven — and its integrator
    fourier       harmonic analysis: series, transform, and the bridge to sampled data
    measurement   synthetic noise, cosine fitting, and uncertainty; simulation as experiment
    validation    the reusable accuracy checks (seeds, convergence, scaling)
"""

from __future__ import annotations

from . import fourier, measurement, oscillators, phasors, units, validation
from .constants import C_LIGHT, EPS_0, MU_0, SIGN_CONVENTION

__all__ = [
    "C_LIGHT",
    "EPS_0",
    "MU_0",
    "SIGN_CONVENTION",
    "fourier",
    "measurement",
    "oscillators",
    "phasors",
    "units",
    "validation",
]
