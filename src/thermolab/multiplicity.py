"""Multiplicity, entropy, and why equilibrium is overwhelmingly probable.

MODEL SPECIFICATION
    System:        N distinguishable objects, each in one of two states — particles in a left
                   or right half of a box, coins showing heads or tails, spins up or down
    Dynamics:      for the sampled version, one randomly chosen object changes state per step
    Boundary:      closed; N is fixed
    Ensemble:      microcanonical in the sense that every microstate is equally probable —
                   the fundamental assumption whose consequences this module explores
    Ignored:       interactions between objects, energy differences between the two states,
                   and any dynamics that would prefer one state over the other
    Valid when:    the two states are energetically equivalent and objects are independent
    Failure modes: interacting systems (an Ising magnet below its critical temperature),
                   or states with different energies, where the Boltzmann factor takes over

The central result is not that equilibrium is *likely* but how brutally likely it becomes:
the fraction of microstates within a given relative distance of the even split narrows as
N^(-1/2), so by N ~ 10^20 the gas has no realistic chance of visibly departing from it.
"""

from __future__ import annotations

import numpy as np
from scipy.special import gammaln

from .constants import K_B


def multiplicity(n_objects: int, n_in_first_state: int) -> float:
    """Ω(N, n) = N! / (n! (N-n)!), the number of microstates in the macrostate.

    Returned as a float via the log form, because Ω overflows an integer type well before
    N reaches interesting sizes.
    """
    _validate(n_objects, n_in_first_state)
    return float(np.exp(log_multiplicity(n_objects, n_in_first_state)))


def log_multiplicity(n_objects: int, n_in_first_state: int) -> float:
    """ln Ω(N, n), computed with log-gamma so it stays exact for large N."""
    _validate(n_objects, n_in_first_state)
    n, k = float(n_objects), float(n_in_first_state)
    return float(gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1))


def log_multiplicity_array(n_objects: int, counts: np.ndarray) -> np.ndarray:
    """Vectorised ln Ω over an array of macrostate labels."""
    counts = np.asarray(counts, dtype=float)
    n = float(n_objects)
    return gammaln(n + 1) - gammaln(counts + 1) - gammaln(n - counts + 1)


def entropy(n_objects: int, n_in_first_state: int) -> float:
    """Boltzmann entropy S = k_B ln Ω of a single macrostate [J/K]."""
    return K_B * log_multiplicity(n_objects, n_in_first_state)


def probability(n_objects: int, n_in_first_state: int) -> float:
    """Probability of the macrostate, Ω(N, n) / 2^N, under equal microstate probabilities."""
    log_p = log_multiplicity(n_objects, n_in_first_state) - n_objects * np.log(2.0)
    return float(np.exp(log_p))


def stirling_log_factorial(n: int, order: int = 1) -> float:
    """Stirling's approximation to ln(N!).

    order=0 gives the form used in most thermodynamics derivations, N ln N - N;
    order=1 adds the (1/2) ln(2πN) term. The exact value is `gammaln(n+1)`, so the tests can
    measure how good the approximation is instead of taking it on faith.
    """
    if n < 1:
        raise ValueError("Stirling's approximation needs n >= 1")
    value = n * np.log(n) - n
    if order >= 1:
        value += 0.5 * np.log(2.0 * np.pi * n)
    return float(value)


def gaussian_multiplicity_fraction(n_objects: int, counts: np.ndarray) -> np.ndarray:
    """Gaussian approximation to Ω(N, n)/2^N near the peak.

    Expanding ln Ω about n = N/2 gives a Gaussian of standard deviation sqrt(N)/2 — the
    origin of the N^(-1/2) narrowing of relative fluctuations.
    """
    counts = np.asarray(counts, dtype=float)
    sigma = np.sqrt(n_objects) / 2.0
    return np.exp(-((counts - n_objects / 2.0) ** 2) / (2.0 * sigma**2)) / (
        sigma * np.sqrt(2.0 * np.pi)
    )


def peak_relative_width(n_objects: int) -> float:
    """Relative width of the multiplicity peak, σ_n / (N/2) = N^(-1/2).

    This single line is the quantitative answer to "why does an isolated gas never gather in
    one corner": the accessible spread shrinks as the square root of the system size.
    """
    if n_objects < 1:
        raise ValueError("n_objects must be positive")
    return float((np.sqrt(n_objects) / 2.0) / (n_objects / 2.0))


def sample_two_box(n_objects: int, n_steps: int, rng: np.random.Generator,
                   n_in_first_state: int | None = None) -> np.ndarray:
    """Simulate objects hopping between two boxes; return the occupancy after each step.

    One randomly chosen object switches side per step (the Ehrenfest urn model). Started from
    an extreme macrostate, the trajectory drifts to the even split and then stays near it —
    not because anything forbids the extreme, but because so few microstates sit there.
    """
    if n_objects < 1 or n_steps < 1:
        raise ValueError("n_objects and n_steps must be positive")
    count = n_objects if n_in_first_state is None else n_in_first_state
    _validate(n_objects, count)

    # Object index picked per step; it moves out of box one if it is currently there.
    picks = rng.integers(0, n_objects, size=n_steps)
    in_first = np.zeros(n_objects, dtype=bool)
    in_first[:count] = True

    occupancy = np.empty(n_steps, dtype=np.int64)
    running = count
    for step, index in enumerate(picks):
        running += -1 if in_first[index] else 1
        in_first[index] = not in_first[index]
        occupancy[step] = running
    return occupancy


def _validate(n_objects: int, n_in_first_state: int) -> None:
    if n_objects < 0:
        raise ValueError("n_objects must be non-negative")
    if not 0 <= n_in_first_state <= n_objects:
        raise ValueError("n_in_first_state must lie between 0 and n_objects")
