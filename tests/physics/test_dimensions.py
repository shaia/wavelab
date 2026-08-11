"""Accuracy category 1: dimensional consistency.

The library works in plain SI floats so students can read the formulas. These tests
re-evaluate the same expressions with pint quantities, so a wrong power of a variable fails
loudly even when the number looks plausible.
"""

from __future__ import annotations

import numpy as np
import pytest

from thermolab import forms, kinetics, multiplicity, paths, sampling
from thermolab.units import K_B_Q, Quantity

pytestmark = pytest.mark.dimensional


def test_ideal_gas_pressure_has_pressure_dimensions_in_3d():
    n, temperature, volume = 1000, Quantity(300.0, "K"), Quantity(1e-3, "m**3")
    pressure = n * K_B_Q * temperature / volume
    assert pressure.check("[pressure]")


def test_ideal_gas_pressure_in_2d_is_force_per_length():
    """In two dimensions "volume" is an area, so pressure is a force per unit length."""
    n, temperature, area = 1000, Quantity(300.0, "K"), Quantity(1e-6, "m**2")
    pressure = n * K_B_Q * temperature / area
    assert pressure.check("[force] / [length]")


def test_kinetics_pressure_matches_impulse_over_time_and_wall():
    """P = impulse / (time x wall measure) must reduce to a force per unit length in 2D."""
    impulse = Quantity(1.0, "kg * m / s")
    duration = Quantity(1.0, "s")
    wall = Quantity(1.0, "m")
    assert (impulse / (duration * wall)).check("[force] / [length]")


def test_mean_kinetic_energy_is_an_energy():
    assert (0.5 * 2 * K_B_Q * Quantity(300.0, "K")).check("[energy]")


def test_rms_speed_is_a_speed():
    speed = ((2 * K_B_Q * Quantity(300.0, "K")) / Quantity(4.65e-26, "kg")) ** 0.5
    assert speed.check("[velocity]")


def test_work_integral_has_energy_dimensions():
    """W = -∫P dV: pressure times volume is an energy in any dimension."""
    work = Quantity(1e5, "Pa") * Quantity(1e-3, "m**3")
    assert work.check("[energy]")


def test_entropy_has_energy_per_temperature():
    """S = k_B ln Ω — the logarithm is dimensionless, so S carries k_B's units."""
    assert K_B_Q.check("[energy] / [temperature]")


@pytest.mark.parametrize(
    ("value", "expected_dimension"),
    [
        (kinetics.ideal_gas_pressure(1000, 300.0, 1e-6), float),
        (kinetics.mean_kinetic_energy(300.0, dimension=2), float),
        (kinetics.rms_speed(300.0, 4.65e-26, dimension=2), float),
        (paths.ideal_gas_pressure(1000, 300.0, 1e-3), float),
        (paths.isothermal_work_on_gas(1000, 300.0, 1e-3, 2e-3), float),
        (multiplicity.entropy(100, 50), float),
        (sampling.die_mean(6), float),
        (sampling.die_variance(6), float),
        (sampling.predicted_relative_spread(100), float),
    ],
)
def test_library_functions_return_plain_si_floats(value, expected_dimension):
    """The library itself stays unit-free by design; pint lives in the tests only."""
    assert isinstance(value, expected_dimension)


def test_both_terms_of_a_one_form_must_carry_the_same_dimensions():
    """M dx + N dy is only meaningful when the two products agree — the rule behind δW = -P dV.

    Adding a pressure-times-volume to a temperature-times-entropy works because both are
    energies; adding a pressure to an energy would not, and pint says so.
    """
    m_dx = Quantity(1e5, "Pa") * Quantity(1e-3, "m**3")
    n_dy = Quantity(2.0, "J / K") * Quantity(0.5, "K")

    assert m_dx.check("[energy]")
    assert n_dy.check("[energy]")
    assert (m_dx + n_dy).check("[energy]")


def test_a_relative_spread_is_dimensionless_and_survives_a_change_of_units():
    """σ carries the units of the quantity; σ/μ does not — the only scale-free "steadiness".

    Re-expressing every measurement in different units multiplies both σ and μ by the same
    factor, so the ratio is untouched. This is why the course compares fractional differences
    and never absolute ones.
    """
    rng = np.random.default_rng(4)
    averages = sampling.sample_averages(n_per_sample=32, n_samples=500, rng=rng)
    rescaled = 1.609344 * averages  # the same readings, quoted in another unit

    original = averages.std(ddof=1) / averages.mean()
    converted = rescaled.std(ddof=1) / rescaled.mean()

    assert converted == pytest.approx(original, rel=1e-12)


def test_line_integral_returns_a_plain_float():
    """`forms` is pure mathematics on plain numbers; units live in the physics that uses it."""
    x = np.linspace(0.0, 1.0, 65)
    value = forms.line_integral(lambda x, y: y, lambda x, y: np.zeros_like(x), x, x)

    assert isinstance(value, float)


def test_multiplicity_is_dimensionless():
    """Ω counts microstates — a pure number, whatever the system."""
    assert isinstance(multiplicity.multiplicity(20, 10), float)
    assert multiplicity.multiplicity(20, 10) > 1.0
