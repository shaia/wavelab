"""Accuracy category 6: independence from the random seed.

A physical conclusion may not depend on which random numbers happened to come up. Every
stochastic function in the library takes an explicit `rng`, and these tests confirm both that
the seed controls reproducibility and that the physics does not change with it.
"""

from __future__ import annotations

import numpy as np
import pytest

from thermolab import kinetics, multiplicity, sampling
from thermolab.validation import seed_study

pytestmark = pytest.mark.seed_independence

ARGON_MASS = 39.948 * 1.66053906660e-27
BOX_2D = (1e-6, 1e-6)


def test_same_seed_reproduces_the_same_gas():
    a = kinetics.initialise_gas(200, BOX_2D, 300.0, ARGON_MASS, np.random.default_rng(9))
    b = kinetics.initialise_gas(200, BOX_2D, 300.0, ARGON_MASS, np.random.default_rng(9))

    assert np.array_equal(a.positions, b.positions)
    assert np.array_equal(a.velocities, b.velocities)


def test_different_seeds_give_different_microstates():
    a = kinetics.initialise_gas(200, BOX_2D, 300.0, ARGON_MASS, np.random.default_rng(1))
    b = kinetics.initialise_gas(200, BOX_2D, 300.0, ARGON_MASS, np.random.default_rng(2))

    assert not np.allclose(a.positions, b.positions)


def test_measured_pressure_agrees_across_seeds_within_statistical_error():
    """The macroscopic answer is seed-independent even though every microstate differs."""

    def measure(rng: np.random.Generator) -> float:
        state = kinetics.initialise_gas(400, BOX_2D, 300.0, ARGON_MASS, rng)
        return kinetics.simulate(state, dt=kinetics.max_stable_dt(state), n_steps=6000).pressure()

    study = seed_study(measure, n_seeds=8)
    expected = kinetics.ideal_gas_pressure(400, 300.0, float(np.prod(BOX_2D)))

    assert study.agrees_with(expected, n_sigma=3.0)
    assert study.relative_spread < 0.05


def test_kinetic_temperature_is_seed_independent_by_construction():
    """Drift removal rescales to the requested temperature, so every seed starts identical."""
    study = seed_study(
        lambda rng: (
            kinetics.initialise_gas(500, BOX_2D, 300.0, ARGON_MASS, rng).kinetic_temperature
        ),
        n_seeds=6,
    )

    assert study.values == pytest.approx(300.0, rel=1e-9)


def test_two_box_equilibrium_occupancy_is_seed_independent():
    def mean_late_fraction(rng: np.random.Generator) -> float:
        occupancy = multiplicity.sample_two_box(300, n_steps=20_000, rng=rng)
        return float(occupancy[len(occupancy) // 2 :].mean() / 300)

    study = seed_study(mean_late_fraction, n_seeds=8)

    assert study.agrees_with(0.5, n_sigma=3.0)


def test_maxwell_boltzmann_variance_is_seed_independent():
    """Each velocity component has variance k_B T / m, whatever the seed."""
    expected = kinetics.mean_kinetic_energy(300.0, dimension=1) * 2 / ARGON_MASS

    study = seed_study(
        lambda rng: float(
            np.var(kinetics.sample_maxwell_boltzmann(50_000, 300.0, ARGON_MASS, rng, 1))
        ),
        n_seeds=6,
    )

    assert study.agrees_with(expected, n_sigma=4.0)


def test_same_seed_reproduces_the_same_rolls():
    """The first thing the orientation lab asks a student to check about randomness here."""
    a = sampling.roll_dice(500, np.random.default_rng(23))
    b = sampling.roll_dice(500, np.random.default_rng(23))
    c = sampling.roll_dice(500, np.random.default_rng(24))

    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)


def test_measured_spread_of_the_average_agrees_across_seeds():
    """A different stream of random numbers must not change the physics being measured."""
    study = seed_study(lambda rng: sampling.relative_spread_of_average(64, 1500, rng), n_seeds=8)

    assert study.agrees_with(sampling.predicted_relative_spread(64), n_sigma=3.0), (
        f"measured {study.mean:.5g} +/- {study.standard_error:.2g}, "
        f"expected {sampling.predicted_relative_spread(64):.5g}"
    )


def test_two_independent_seed_families_give_the_same_spread():
    """Reproducibility across whole seed families, not just within one."""
    first = seed_study(
        lambda rng: sampling.relative_spread_of_average(100, 1200, rng), n_seeds=6, base_seed=1
    )
    second = seed_study(
        lambda rng: sampling.relative_spread_of_average(100, 1200, rng), n_seeds=6, base_seed=999
    )

    combined = np.hypot(first.standard_error, second.standard_error)
    assert abs(first.mean - second.mean) <= 3.0 * combined


def test_conditioning_on_a_lucky_start_does_not_bias_what_follows():
    """The falsifying experiment for "later rolls compensate earlier ones".

    Keep only the runs whose first ten rolls averaged well above 3.5, then look at the *next*
    rolls of those same runs. If the dice compensated, this conditioned mean would sit below
    3.5. It does not: convergence works by dilution, not by correction.
    """

    def mean_of_rolls_after_a_hot_start(rng: np.random.Generator) -> float:
        rolls = sampling.roll_dice(10, rng, n_faces=6)
        while rolls.mean() <= 4.5:  # keep drawing until this run starts hot
            rolls = sampling.roll_dice(10, rng, n_faces=6)
        return float(sampling.roll_dice(4000, rng, n_faces=6).mean())

    study = seed_study(mean_of_rolls_after_a_hot_start, n_seeds=12)

    assert study.agrees_with(sampling.die_mean(6), n_sigma=3.0), (
        f"rolls after a hot start averaged {study.mean:.4g} +/- {study.standard_error:.2g}; "
        "a compensating die would sit below 3.5"
    )


def test_seed_study_detects_a_genuinely_biased_measurement():
    """The guard rail itself must work, or every test above is vacuous."""
    biased = seed_study(lambda rng: 1.0 + 0.5 + rng.normal(0, 1e-6), n_seeds=8)

    assert not biased.agrees_with(1.0, n_sigma=3.0)
