"""Accuracy category 1: dimensional consistency.

The library works in plain SI floats so students can read the formulas. These tests
re-evaluate the same expressions with pint quantities, so a wrong power of a variable fails
loudly even when the number looks plausible.
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import oscillators
from wavelab.units import C_LIGHT_Q, EPS_0_Q, MU_0_Q, Quantity

pytestmark = pytest.mark.dimensional

MASS = Quantity(0.5, "kg")
STIFFNESS = Quantity(8.0, "N/m")
DAMPING = Quantity(0.4, "kg/s")
FORCE = Quantity(1.0, "N")


def test_natural_frequency_is_an_inverse_time():
    """omega0 = sqrt(k/m) must come out in radians per second, i.e. 1/[time]."""
    omega0 = (STIFFNESS / MASS) ** 0.5
    assert omega0.check("1/[time]")


def test_spring_potential_energy_is_an_energy():
    assert (0.5 * STIFFNESS * Quantity(0.1, "m") ** 2).check("[energy]")


def test_kinetic_energy_is_an_energy():
    assert (0.5 * MASS * Quantity(0.3, "m/s") ** 2).check("[energy]")


def test_damping_rate_is_an_inverse_time():
    """gamma = b/m: only then can e^{-gamma t / 2} take a dimensionless argument."""
    assert (DAMPING / MASS).check("1/[time]")


def test_quality_factor_is_dimensionless():
    """Q = sqrt(m k) / b — a pure number, or comparing oscillators would be meaningless."""
    q = (MASS * STIFFNESS) ** 0.5 / DAMPING
    assert q.check("[]")


def test_static_response_is_a_length():
    """The omega -> 0 limit of the driven amplitude is F0/k, which must be a displacement."""
    assert (FORCE / STIFFNESS).check("[length]")


def test_driven_amplitude_magnitude_is_a_length():
    """|X| = (F0/m) / |omega0^2 - omega^2 - i gamma omega|: the denominator's magnitude
    carries 1/[time]^2, so the whole expression must reduce to a length."""
    omega = Quantity(3.0, "rad/s")
    denominator_scale = (STIFFNESS / MASS) - omega**2  # the real part sets the dimension
    assert (FORCE / MASS / denominator_scale).check("[length]")


def test_light_speed_from_the_electromagnetic_constants():
    """c = 1/sqrt(mu0 eps0) — checked dimensionally and numerically, module 5's payoff."""
    c = (1.0 / (MU_0_Q * EPS_0_Q)) ** 0.5
    assert c.check("[velocity]")
    assert abs((c / C_LIGHT_Q).to("dimensionless").magnitude - 1.0) < 1e-12


def test_intensity_formula_is_a_power_per_area():
    """I = (1/2) c eps0 n E0^2 with E0 in volts per metre must be watts per square metre."""
    field = Quantity(100.0, "V/m")
    intensity = 0.5 * C_LIGHT_Q * EPS_0_Q * 1.5 * field**2
    assert intensity.check("[power] / [area]")


def test_library_returns_plain_floats():
    """The course promise: numerical code works in plain SI floats, units live in tests."""
    omega0 = oscillators.natural_frequency(0.5, 8.0)
    assert isinstance(omega0, float)
    amplitude, phase = oscillators.amplitude_phase(0.1, 0.2, omega0)
    assert isinstance(amplitude, float) and isinstance(phase, float)
    assert isinstance(oscillators.quality_factor(0.5, 8.0, 0.4), float)


def test_verlet_step_is_dimensionally_consistent():
    """One kick-drift-kick step re-evaluated with units: every update must be coherent."""
    dt = Quantity(0.01, "s")
    x = Quantity(0.1, "m")
    v = Quantity(0.2, "m/s")
    accel = -(STIFFNESS / MASS) * x - (DAMPING / MASS) * v + FORCE / MASS
    assert accel.check("[acceleration]")
    v_half = v + 0.5 * dt * accel
    assert v_half.check("[velocity]")
    assert (x + dt * v_half).check("[length]")
    assert (0.5 * dt * DAMPING / MASS).check("[]")  # the implicit-kick divisor's correction


def test_relative_energy_spread_is_invariant_under_unit_change():
    """A dimensionless ratio must not care whether the trajectory is in metres or millimetres."""
    trajectory = oscillators.simulate(0.5, 8.0, 0.1, 0.0, 0.001, 500)
    _, _, total = oscillators.energies(
        trajectory.positions, trajectory.velocities, 0.5, 8.0
    )
    spread_si = (total.max() - total.min()) / total[0]
    # The same trajectory in mm: x and v both scale by 1000, both energies by 1000^2
    scaled_positions = trajectory.positions * 1000.0
    scaled_velocities = trajectory.velocities * 1000.0
    _, _, total_mm = oscillators.energies(
        scaled_positions, scaled_velocities, 0.5, 8.0
    )
    spread_mm = (total_mm.max() - total_mm.min()) / total_mm[0]
    assert np.isclose(spread_si, spread_mm, rtol=1e-9)
