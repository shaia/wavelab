"""Accuracy category 6: seed independence.

Stochastic results must be reproducible under a fixed seed, genuinely different across
seeds, and — the point of the category — statistically identical across independent seed
families. The final test turns the guard rail on itself: a biased measurement must FAIL the
agreement check, or the check is decoration.
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import measurement, oscillators, phasors
from wavelab.validation import seed_study

pytestmark = pytest.mark.seed_independence

MASS = 0.5
STIFFNESS = 8.0
OMEGA0 = oscillators.natural_frequency(MASS, STIFFNESS)
TIMES = np.linspace(0.0, 8.0 * 2.0 * np.pi / OMEGA0, 1601)
CLEAN = oscillators.position(TIMES, MASS, STIFFNESS, 0.1, 0.0)
NOISE_SIGMA = 0.02


def _measure_omega(rng: np.random.Generator) -> float:
    noisy = measurement.add_noise(CLEAN, NOISE_SIGMA, rng)
    return measurement.fit_cosine(TIMES, noisy, OMEGA0).omega


def test_same_seed_reproduces_the_same_noise_exactly():
    first = measurement.add_noise(CLEAN, NOISE_SIGMA, np.random.default_rng(123))
    second = measurement.add_noise(CLEAN, NOISE_SIGMA, np.random.default_rng(123))
    assert np.array_equal(first, second)


def test_different_seeds_give_different_noise():
    first = measurement.add_noise(CLEAN, NOISE_SIGMA, np.random.default_rng(123))
    second = measurement.add_noise(CLEAN, NOISE_SIGMA, np.random.default_rng(124))
    assert not np.array_equal(first, second)


def test_random_phasor_sum_is_reproducible_under_a_fixed_seed():
    first = phasors.random_phasor_sum(500, np.random.default_rng(9))
    second = phasors.random_phasor_sum(500, np.random.default_rng(9))
    assert first == second


def test_fitted_frequency_agrees_with_truth_across_seeds():
    """The virtual laboratory's central claim: a noisy measurement pipeline recovers the
    true natural frequency within its scatter, whatever the seed."""
    study = seed_study(_measure_omega, n_seeds=8, base_seed=0)
    assert study.agrees_with(OMEGA0, n_sigma=3.0)
    assert study.relative_spread < 1e-3


def test_two_independent_seed_families_agree_with_each_other():
    """Statistical results must not depend on which family of seeds produced them."""
    family_a = seed_study(_measure_omega, n_seeds=8, base_seed=0)
    family_b = seed_study(_measure_omega, n_seeds=8, base_seed=10_000)
    combined_error = float(
        np.hypot(family_a.standard_error, family_b.standard_error)
    )
    assert abs(family_a.mean - family_b.mean) < 3.0 * combined_error


def test_seed_study_detects_a_genuinely_biased_measurement():
    """The guard rail must guard: fitting a signal whose true frequency is 2% off must
    fail the agreement check against OMEGA0, loudly, or every passing test above is vacuous."""
    biased_clean = oscillators.position(TIMES, MASS, STIFFNESS * 1.04, 0.1, 0.0)

    def biased_measure(rng: np.random.Generator) -> float:
        noisy = measurement.add_noise(biased_clean, NOISE_SIGMA, rng)
        return measurement.fit_cosine(TIMES, noisy, OMEGA0).omega

    study = seed_study(biased_measure, n_seeds=8, base_seed=0)
    assert not study.agrees_with(OMEGA0, n_sigma=3.0)
