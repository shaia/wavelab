"""Accuracy category 4: large-N behaviour.

The course's central claim is that macroscopic steadiness emerges from microscopic noise.
Quantitatively that means relative fluctuations fall off as N^(-1/2) — so these tests measure
the exponent rather than accepting a qualitative "the jitter looks smaller".
"""

from __future__ import annotations

import numpy as np
import pytest

from thermolab import kinetics, multiplicity, sampling
from thermolab.validation import relative_error, scaling_exponent

pytestmark = pytest.mark.large_n

ARGON_MASS = 39.948 * 1.66053906660e-27
BOX_2D = (1e-6, 1e-6)


def sampled_pressure(n_particles: int, rng: np.random.Generator, n_steps: int = 3000) -> float:
    """Pressure of one independently drawn microstate at 300 K.

    `fix_temperature=False` keeps the raw Maxwell-Boltzmann draw, so the energy — and hence
    the pressure — differs from sample to sample exactly as a canonical system's does.
    Rescaling to an exact temperature would erase the fluctuation being measured.
    """
    state = kinetics.initialise_gas(
        n_particles, BOX_2D, 300.0, ARGON_MASS, rng, fix_temperature=False
    )
    return kinetics.simulate(state, dt=kinetics.max_stable_dt(state), n_steps=n_steps).pressure()


def relative_pressure_fluctuation(
    n_particles: int, n_samples: int = 24, base_seed: int = 0
) -> float:
    """Spread of the pressure across independent microstates, relative to its mean."""
    seeds = np.random.SeedSequence(base_seed).spawn(n_samples)
    pressures = np.array([sampled_pressure(n_particles, np.random.default_rng(s)) for s in seeds])
    return float(pressures.std(ddof=1) / pressures.mean())


@pytest.mark.slow
def test_relative_pressure_fluctuation_falls_as_one_over_sqrt_n():
    """The course's central quantitative claim, measured rather than asserted.

    For a 2D ideal gas the time-averaged pressure of a microstate is proportional to the sum
    of 2N squared velocity components, so it is chi-square distributed with 2N degrees of
    freedom and its relative spread is exactly N^(-1/2).
    """
    sizes = [25, 50, 100, 200, 400]
    fluctuations = [relative_pressure_fluctuation(n, n_samples=40, base_seed=7) for n in sizes]

    exponent = scaling_exponent(sizes, fluctuations)

    assert exponent == pytest.approx(-0.5, abs=0.12), (
        f"fitted exponent {exponent:.3f} from fluctuations {fluctuations}"
    )


def test_fluctuation_magnitude_matches_the_chi_square_prediction():
    """Not just the exponent: the coefficient is 1, i.e. sigma_P/<P> = 1/sqrt(N)."""
    for n in (50, 200):
        assert relative_pressure_fluctuation(n, n_samples=40, base_seed=3) == pytest.approx(
            1.0 / np.sqrt(n), rel=0.3
        )


def test_larger_systems_have_steadier_pressure():
    """The cheap version of the same statement, kept out of the slow set."""
    small = relative_pressure_fluctuation(25, n_samples=16, base_seed=101)
    large = relative_pressure_fluctuation(400, n_samples=16, base_seed=101)

    assert large < small


def test_multiplicity_peak_narrows_as_one_over_sqrt_n():
    sizes = [100, 1000, 10_000, 100_000]
    widths = [multiplicity.peak_relative_width(n) for n in sizes]

    assert scaling_exponent(sizes, widths) == pytest.approx(-0.5, abs=1e-9)


def test_odds_of_a_ten_percent_excess_fall_exponentially_in_system_size():
    """Why a gas never gathers in one corner.

    Near the peak, ln[P(n)/P(N/2)] = -2(n - N/2)^2/N, so holding the *fractional* excess at
    10% makes the log-odds fall linearly in N: -0.02 N. Ten thousand particles already put
    the ratio near 1e-87; a mole makes it unreachable.
    """
    sizes = np.array([1000, 5000, 10_000])
    log_ratios = np.array(
        [
            np.log(multiplicity.probability(int(n), int(0.6 * n)))
            - np.log(multiplicity.probability(int(n), int(n) // 2))
            for n in sizes
        ]
    )

    assert np.all(np.diff(log_ratios) < 0)
    assert np.allclose(log_ratios / sizes, -0.02, atol=2e-3)
    assert multiplicity.probability(10_000, 6000) / multiplicity.probability(10_000, 5000) < 1e-80


def test_two_box_occupancy_settles_near_the_even_split():
    """Started from every object on one side, the system drifts to equilibrium and stays."""
    rng = np.random.default_rng(77)
    n_objects = 400
    occupancy = multiplicity.sample_two_box(n_objects, n_steps=40_000, rng=rng)

    late = occupancy[len(occupancy) // 2 :]
    mean_fraction = late.mean() / n_objects
    spread_fraction = late.std() / n_objects

    assert mean_fraction == pytest.approx(0.5, abs=0.02)
    assert spread_fraction < 0.05


def test_relative_spread_of_a_sample_average_falls_as_one_over_sqrt_n():
    """The same law as the pressure fluctuation, stripped of all physics.

    Dice have no energy, no container and no dynamics, so an N^(-1/2) here can only come from
    independence plus the additivity of variance — which is exactly the module's derivation.
    """
    rng = np.random.default_rng(2718)
    sizes = [4, 16, 64, 256, 1024]
    spreads = [sampling.relative_spread_of_average(n, n_samples=800, rng=rng) for n in sizes]

    exponent = scaling_exponent(sizes, spreads)

    assert exponent == pytest.approx(-0.5, abs=0.06), (
        f"fitted exponent {exponent:.3f} from spreads {spreads}"
    )


def test_sample_average_spread_matches_the_predicted_coefficient():
    """Not just the exponent: the prefactor is σ₁/μ₁, measured to a few percent."""
    rng = np.random.default_rng(31415)

    for n in (25, 400):
        measured = sampling.relative_spread_of_average(n, n_samples=2000, rng=rng)
        assert relative_error(measured, sampling.predicted_relative_spread(n)) < 0.1


def test_the_sum_gets_noisier_while_the_average_gets_steadier():
    """The distinction the module's third prediction is built on.

    Absolute scatter of the sum grows as sqrt(N); relative scatter of the average falls as
    1/sqrt(N). Both come from the same line of algebra, and confusing them is the usual error.
    """
    rng = np.random.default_rng(9001)
    sizes = [16, 64, 256, 1024]

    absolute_sum_spreads = []
    relative_average_spreads = []
    for n in sizes:
        averages = sampling.sample_averages(n, 800, rng)
        absolute_sum_spreads.append(float((n * averages).std(ddof=1)))
        relative_average_spreads.append(float(averages.std(ddof=1) / averages.mean()))

    assert scaling_exponent(sizes, absolute_sum_spreads) == pytest.approx(0.5, abs=0.06)
    assert scaling_exponent(sizes, relative_average_spreads) == pytest.approx(-0.5, abs=0.06)


@pytest.mark.slow
def test_two_box_equilibrium_spread_scales_as_one_over_sqrt_n():
    """σ_n/N = 1/(2 sqrt(N)) for the Ehrenfest urn, the same law as the pressure fluctuation."""
    rng = np.random.default_rng(5150)
    sizes = [100, 400, 1600, 6400]
    spreads = []
    for n in sizes:
        occupancy = multiplicity.sample_two_box(n, n_steps=60 * n, rng=rng, n_in_first_state=n // 2)
        late = occupancy[len(occupancy) // 2 :]
        spreads.append(float(late.std() / n))

    assert scaling_exponent(sizes, spreads) == pytest.approx(-0.5, abs=0.12)
