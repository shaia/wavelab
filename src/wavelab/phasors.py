"""Rotating complex amplitudes — the course's one representation of oscillation.

MODEL SPECIFICATION
    System:        one or more harmonic oscillations of a single angular frequency, each
                   represented by a complex amplitude ("phasor"); the observable is the real
                   signal their sum projects out
    Dynamics:      uniform rotation only — every phasor turns as e^{-i omega t} and nothing
                   else happens; there are no equations of motion here
    Boundary:      none; phasors neither grow, decay, nor exchange anything
    Ensemble:      deterministic, except `random_phasor_sum`, whose phases are independent
                   uniform draws from a seeded generator
    Ignored:       everything physical — what oscillates, what drives it, and every mechanism
                   (damping, forcing, nonlinearity) that would change an amplitude in time
    Valid when:    the signals really are single-frequency sinusoids, so a fixed complex
                   amplitude captures each of them completely
    Failure modes: signals of different frequencies summed as if phasors (their relative
                   phase is not constant — see `beat_signal` for the honest treatment), and
                   any nonlinear operation applied to the complex representation instead of
                   the real signal

Everything follows the project phase convention (constants.SIGN_CONVENTION): the physical
signal A cos(omega t + phi) is Re[A e^{-i phi} e^{-i omega t}], so the phasor of amplitude A
and phase phi is A e^{-i phi}, and phasors rotate clockwise.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def phasor(amplitude: float, phase: float) -> complex:
    """The complex amplitude of the oscillation `amplitude * cos(omega t + phase)`.

    Under the course convention this is `amplitude * e^{-i phase}`: the minus sign is what
    makes Re[phasor * e^{-i omega t}] reproduce the cosine with a *plus* phase inside.
    """
    if amplitude < 0:
        raise ValueError("amplitude must be non-negative; put sign flips into the phase")
    return complex(amplitude * np.exp(-1j * phase))


def evaluate(z: complex | np.ndarray, omega: float, t: np.ndarray) -> np.ndarray:
    """Rotate phasor `z` in time: `z * e^{-i omega t}` — the course's one time factor.

    Returns the complex signal; take `.real` for the physical one. Broadcasting is plain
    NumPy, so `z` may be a single phasor or an array of them.
    """
    return np.asarray(z) * np.exp(-1j * omega * np.asarray(t))


def real_signal(amplitude: float, omega: float, phase: float, t: np.ndarray) -> np.ndarray:
    """The physical signal `amplitude * cos(omega t + phase)`, via its phasor.

    Deliberately computed as Re[phasor * e^{-i omega t}] rather than by calling `np.cos`, so
    that this function *is* the convention check: if the phasor sign were wrong, comparing
    against the direct cosine would fail — and a test does exactly that.
    """
    return evaluate(phasor(amplitude, phase), omega, t).real


def superpose(phasors: Sequence[complex]) -> complex:
    """The phasor of a sum of same-frequency oscillations: the plain complex sum.

    That the sum of harmonic oscillations of one frequency is again harmonic at that
    frequency is the superposition theorem of module 00; this one-liner is its whole content.
    """
    return complex(np.sum(np.asarray(phasors, dtype=complex)))


def resultant(amplitudes: Sequence[float], phases: Sequence[float]) -> tuple[float, float]:
    """Amplitude and phase of a sum of same-frequency oscillations.

    Returns `(A, phi)` such that the sum equals `A * cos(omega t + phi)`. For two
    oscillations this reproduces the interference law
    `A^2 = A1^2 + A2^2 + 2 A1 A2 cos(phi1 - phi2)` — the same formula that module 8 will
    read as I = I1 + I2 + 2 sqrt(I1 I2) cos(delta).
    """
    amps = np.asarray(amplitudes, dtype=float)
    phis = np.asarray(phases, dtype=float)
    if amps.shape != phis.shape:
        raise ValueError("amplitudes and phases must have the same length")
    total = superpose([phasor(a, p) for a, p in zip(amps, phis, strict=True)])
    # The phasor is A e^{-i phi}, so the phase is *minus* the argument.
    return abs(total), float(-np.angle(total))


def beat_signal(
    a1: float, a2: float, omega1: float, omega2: float, t: np.ndarray
) -> np.ndarray:
    """Sum of two cosines of different frequencies, evaluated honestly.

    Two frequencies means no single rotating frame, so this returns the plain sum of the two
    real signals. For nearby frequencies the result is a carrier at the mean frequency inside
    an envelope of angular frequency |omega1 - omega2| / 2 — beats, with an *intensity* that
    pulses at the full difference |omega1 - omega2|.
    """
    time = np.asarray(t)
    return real_signal(a1, omega1, 0.0, time) + real_signal(a2, omega2, 0.0, time)


def random_phasor_sum(n: int, rng: np.random.Generator) -> complex:
    """Sum of `n` unit phasors with independent uniform random phases.

    The elementary model of speckle and of incoherent addition: the resultant's *intensity*
    |sum|^2 averages to n (not n^2), so the resultant amplitude grows only as sqrt(n) — the
    same accumulation law as a random walk. A scaling test pins the exponent.
    """
    if n < 1:
        raise ValueError("n must be positive")
    phases = rng.uniform(0.0, 2.0 * np.pi, size=n)
    return superpose(np.exp(-1j * phases))
