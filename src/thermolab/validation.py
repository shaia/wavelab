"""Reusable checks behind the course's scientific-accuracy framework.

Every simulation in ThermoLab has to answer the same questions: does it conserve what it
should, does it reproduce the analytic result in the regime where one exists, does the answer
survive refining the numerics, and is it independent of the random seed within statistical
error? These helpers implement those questions once so each module's tests state the physics
rather than re-derive the statistics.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SeedStudy:
    """Result of running a stochastic measurement under several independent seeds."""

    values: np.ndarray
    mean: float
    standard_error: float

    def agrees_with(self, expected: float, n_sigma: float = 3.0) -> bool:
        """True when `expected` lies within `n_sigma` standard errors of the sample mean.

        A stochastic result can only be compared to theory with an uncertainty attached;
        `n_sigma = 3` gives a ~0.3% false-alarm rate per assertion, which keeps the test
        suite from flickering while still catching real errors.
        """
        if self.standard_error == 0.0:
            return bool(np.isclose(self.mean, expected))
        return abs(self.mean - expected) <= n_sigma * self.standard_error

    @property
    def relative_spread(self) -> float:
        """Standard deviation across seeds, relative to the mean."""
        return float(np.std(self.values, ddof=1) / abs(self.mean)) if self.mean else np.inf


def seed_study(measure: Callable[[np.random.Generator], float], n_seeds: int = 8,
               base_seed: int = 0) -> SeedStudy:
    """Run `measure` under `n_seeds` independent generators and summarise the spread.

    `measure` must take the generator as its only argument, so that no simulation reaches for
    global RNG state — the reason results stay reproducible across notebook runs.
    """
    if n_seeds < 2:
        raise ValueError("a seed study needs at least two seeds to estimate a spread")
    seeds = np.random.SeedSequence(base_seed).spawn(n_seeds)
    values = np.array([measure(np.random.default_rng(s)) for s in seeds], dtype=float)
    mean = float(values.mean())
    standard_error = float(values.std(ddof=1) / np.sqrt(n_seeds))
    return SeedStudy(values=values, mean=mean, standard_error=standard_error)


@dataclass(frozen=True)
class ConvergenceStudy:
    """Result of refining a numerical parameter towards an exact answer."""

    refinements: np.ndarray
    values: np.ndarray
    errors: np.ndarray

    @property
    def observed_order(self) -> float:
        """Convergence order p from a log-log fit of error against refinement.

        With `refinements` counting subdivisions, error ~ h^p ~ n^-p, so the fitted slope is
        -p. Returns +p, the number quoted for a quadrature or integrator.
        """
        usable = self.errors > 0
        if usable.sum() < 2:
            return np.inf  # exact at every refinement — no order to measure
        slope = np.polyfit(np.log(self.refinements[usable]), np.log(self.errors[usable]), 1)[0]
        return float(-slope)


def convergence_study(compute: Callable[[int], float], refinements: Sequence[int],
                      exact: float) -> ConvergenceStudy:
    """Evaluate `compute(n)` over increasing `n` and measure how the error shrinks."""
    ref = np.asarray(list(refinements), dtype=float)
    values = np.array([compute(int(n)) for n in ref], dtype=float)
    scale = abs(exact) if exact != 0 else 1.0
    return ConvergenceStudy(refinements=ref, values=values, errors=np.abs(values - exact) / scale)


def scaling_exponent(sizes: Sequence[float], quantities: Sequence[float]) -> float:
    """Fit `quantity ~ size**alpha` on a log-log plot and return alpha.

    The course uses this to check the N^(-1/2) law for relative fluctuations, which is the
    quantitative form of "large systems have steady macroscopic properties".
    """
    x = np.log(np.asarray(list(sizes), dtype=float))
    y = np.log(np.asarray(list(quantities), dtype=float))
    return float(np.polyfit(x, y, 1)[0])


def relative_error(value: float, expected: float) -> float:
    """|value - expected| / |expected|, or absolute error when `expected` is zero."""
    return abs(value - expected) / abs(expected) if expected != 0 else abs(value)
