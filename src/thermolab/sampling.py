"""Independent draws, sample averages, and the N^(-1/2) law in its simplest setting.

MODEL SPECIFICATION
    System:        N dice, each showing one of `n_faces` equally likely faces; the observable
                   is the sum or the average of the N faces shown
    Dynamics:      none — every draw is independent of every other, with no memory between
                   them and nothing evolving in time
    Boundary:      closed trivially; N is fixed for one experiment and nothing is exchanged
    Ensemble:      every face equally probable by fiat — the same kind of postulate the course
                   will later make about the microstates of a gas
    Ignored:       all physics of real dice — bounce dynamics, pip asymmetry, air drag, and the
                   deterministic chaos that is the actual reason a throw looks random
    Valid when:    the randomness source is well modelled by independent uniform draws; a
                   seeded pseudo-random generator is, by construction
    Failure modes: correlated draws (memory between rolls), loaded dice (non-uniform faces),
                   and any question about a *single* roll beyond its distribution

The point of dice is that they are not physics. Strip away energy, particles and containers,
and the course's central mechanism is still there: individual outcomes stay unpredictable
while their average becomes reproducible, with a relative scatter that falls as N^(-1/2).
"""

from __future__ import annotations

import numpy as np


def die_mean(n_faces: int = 6) -> float:
    """Mean of one uniform die, (n_faces + 1) / 2 — for a six-sided die, 7/2."""
    _validate_faces(n_faces)
    return (n_faces + 1) / 2.0


def die_variance(n_faces: int = 6) -> float:
    """Variance of one uniform die, (n_faces^2 - 1) / 12 — for a six-sided die, 35/12.

    Worth deriving by hand once: it is the sum over faces of (k - mean)^2 / n_faces, and it
    collapses to this closed form. A one-faced die has zero variance, as it must.
    """
    _validate_faces(n_faces)
    return (n_faces**2 - 1) / 12.0


def die_relative_spread(n_faces: int = 6) -> float:
    """The dimensionless scatter of one die, sigma / mean — about 0.488 for six faces.

    This is the coefficient in front of N^(-1/2): the relative spread of an average of N dice
    is this number divided by sqrt(N). Being a ratio, it is what survives a change of units.
    """
    return float(np.sqrt(die_variance(n_faces)) / die_mean(n_faces))


def roll_dice(n_rolls: int, rng: np.random.Generator, n_faces: int = 6) -> np.ndarray:
    """Roll one die `n_rolls` times; return the faces shown as an integer array."""
    if n_rolls < 1:
        raise ValueError("n_rolls must be positive")
    _validate_faces(n_faces)
    return rng.integers(1, n_faces + 1, size=n_rolls)


def running_average(values: np.ndarray) -> np.ndarray:
    """Average of the first k entries, for every k — the curve that visibly settles.

    Nothing corrects an early run of high rolls; it is simply divided by an ever larger k
    until it no longer matters. The convergence is by dilution, not by compensation.
    """
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        raise ValueError("running_average needs at least one value")
    return np.cumsum(values) / np.arange(1, values.size + 1)


def sample_averages(n_per_sample: int, n_samples: int, rng: np.random.Generator,
                    n_faces: int = 6) -> np.ndarray:
    """Repeat the experiment "average `n_per_sample` dice" `n_samples` times.

    Returns one average per repetition, so the scatter *across* repetitions measures how
    reproducible a single experiment is — which is the quantity the whole module is about.
    """
    if n_per_sample < 1 or n_samples < 1:
        raise ValueError("n_per_sample and n_samples must be positive")
    _validate_faces(n_faces)
    draws = rng.integers(1, n_faces + 1, size=(n_samples, n_per_sample))
    return draws.mean(axis=1)


def relative_spread_of_average(n_per_sample: int, n_samples: int, rng: np.random.Generator,
                               n_faces: int = 6) -> float:
    """Measured standard deviation of the sample average, divided by its mean.

    Compare against `die_relative_spread(n_faces) / sqrt(n_per_sample)`. Reported as a ratio
    because an absolute spread carries the units of the underlying quantity and so cannot be
    compared between systems; this number can.
    """
    if n_samples < 2:
        raise ValueError("estimating a spread needs at least two repetitions")
    averages = sample_averages(n_per_sample, n_samples, rng, n_faces)
    return float(averages.std(ddof=1) / abs(averages.mean()))


def predicted_relative_spread(n_per_sample: int, n_faces: int = 6) -> float:
    """The analytic answer, (sigma_1 / mu_1) * n_per_sample^(-1/2).

    Derived on the module page from two facts only: means always add, and variances add for
    *independent* quantities.
    """
    if n_per_sample < 1:
        raise ValueError("n_per_sample must be positive")
    return die_relative_spread(n_faces) / np.sqrt(n_per_sample)


def _validate_faces(n_faces: int) -> None:
    if n_faces < 1:
        raise ValueError("a die needs at least one face")
