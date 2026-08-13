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
from wavelab.validation import scaling_exponent, seed_study

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


RINGDOWN_DAMPING = 0.1  # Q = 20
RINGDOWN_TIMES = np.linspace(0.0, 30.0 * 2.0 * np.pi / OMEGA0, 12_001)
RINGDOWN_CLEAN = oscillators.damped_position(
    RINGDOWN_TIMES, MASS, STIFFNESS, RINGDOWN_DAMPING, 0.1, 0.0
)
TRUE_Q = oscillators.quality_factor(MASS, STIFFNESS, RINGDOWN_DAMPING)


def _q_from_noisy_ringdown(rng: np.random.Generator) -> float:
    noisy = measurement.add_noise(RINGDOWN_CLEAN, 1e-3, rng)
    return oscillators.q_from_ringdown(RINGDOWN_TIMES, noisy)


def test_three_q_estimators_agree_on_noisy_data_within_one_percent():
    """Module 02's punchline as a test: measure Q three ways from noisy apparatus and get
    one number.

    Each route sees its own noisy record — a ringdown, an amplitude sweep, a phase sweep —
    so agreement here is a statement about the physics, not about shared arithmetic.

    The tolerance is a *total* uncertainty of 1%, not a 3-sigma statistical band, and that is
    the physics rather than a loosened assertion. Each estimator carries a small systematic
    bias on top of its scatter: the bandwidth route is O(1/Q^2) low because the half-power
    width of |X| is only asymptotically gamma, and the ringdown route is O(sigma^2/A^2) high
    because a noisy record's mean square is its signal's plus its noise's. At this noise
    level both biases exceed the seed-to-seed scatter, so an assertion phrased purely in
    standard errors would be testing the noise and ignoring the systematics. Separating the
    two is the lesson the laboratory teaches with the same three numbers.
    """
    omegas = np.linspace(0.5 * OMEGA0, 1.5 * OMEGA0, 4001)
    clean_response = oscillators.steady_state_response(
        omegas, MASS, STIFFNESS, RINGDOWN_DAMPING, 1.0
    )

    def q_from_noisy_sweep(rng: np.random.Generator) -> float:
        amplitude = measurement.add_noise(np.abs(clean_response), 2e-4, rng)
        return oscillators.q_from_bandwidth(omegas, amplitude)

    def q_from_noisy_phase(rng: np.random.Generator) -> float:
        phase = measurement.add_noise(np.angle(clean_response), 2e-3, rng)
        return oscillators.q_from_phase_slope(omegas, phase)

    studies = {
        "ringdown": seed_study(_q_from_noisy_ringdown, n_seeds=8, base_seed=3),
        "bandwidth": seed_study(q_from_noisy_sweep, n_seeds=8, base_seed=3),
        "phase slope": seed_study(q_from_noisy_phase, n_seeds=8, base_seed=3),
    }
    for name, study in studies.items():
        assert abs(study.mean - TRUE_Q) / TRUE_Q < 0.01, f"{name} is off by more than 1%"
        assert study.relative_spread < 0.01, f"{name} is not reproducible across seeds"

    measured = [study.mean for study in studies.values()]
    assert (max(measured) - min(measured)) / TRUE_Q < 0.01


def test_ringdown_q_scatter_shrinks_as_inverse_sqrt_of_seed_count():
    """More repeats, tighter answer: the standard error of measured Q falls as M^(-1/2).

    The N^(-1/2) law from module 00, now doing the job it exists for — telling a student how
    many ringdowns to record before quoting a Q to a given precision. Note what it cannot do:
    the systematic offset the test above budgets for is untouched by any number of repeats.
    """
    counts = [4, 16, 64]
    errors = [
        seed_study(_q_from_noisy_ringdown, n_seeds=n, base_seed=11).standard_error
        for n in counts
    ]
    assert abs(scaling_exponent(counts, errors) - (-0.5)) < 0.2


def test_seed_study_detects_a_genuinely_biased_measurement():
    """The guard rail must guard: fitting a signal whose true frequency is 2% off must
    fail the agreement check against OMEGA0, loudly, or every passing test above is vacuous."""
    biased_clean = oscillators.position(TIMES, MASS, STIFFNESS * 1.04, 0.1, 0.0)

    def biased_measure(rng: np.random.Generator) -> float:
        noisy = measurement.add_noise(biased_clean, NOISE_SIGMA, rng)
        return measurement.fit_cosine(TIMES, noisy, OMEGA0).omega

    study = seed_study(biased_measure, n_seeds=8, base_seed=0)
    assert not study.agrees_with(OMEGA0, n_sigma=3.0)
