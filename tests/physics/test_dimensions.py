"""Accuracy category 1: dimensional consistency.

The library works in plain SI floats so students can read the formulas. These tests
re-evaluate the same expressions with pint quantities, so a wrong power of a variable fails
loudly even when the number looks plausible.
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import fourier, oscillators
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


def test_cycle_averaged_absorbed_power_is_in_watts():
    """<P> = (1/2) gamma m omega^2 |X|^2. Every factor matters: drop the mass and the
    expression still *looks* like a power on the page, but it is metres-squared per second."""
    omega = Quantity(3.0, "rad/s")
    gamma = DAMPING / MASS
    displacement = FORCE / MASS / ((STIFFNESS / MASS) - omega**2)
    power = 0.5 * gamma * MASS * omega**2 * displacement**2
    assert power.check("[power]")
    assert power.to("watt").magnitude > 0.0


def test_absorbed_power_equals_the_work_rate_of_the_drive():
    """The same number reached the other way, <F v>: force times velocity is a power too,
    and the two expressions must have identical dimensions or the balance is meaningless."""
    omega = Quantity(3.0, "rad/s")
    displacement = FORCE / MASS / ((STIFFNESS / MASS) - omega**2)
    work_rate = 0.5 * FORCE * omega * displacement
    assert work_rate.check("[power]")


def test_quality_factor_expressions_are_all_dimensionless():
    """Q wears three costumes — omega0/gamma, a bandwidth ratio, and half a frequency times
    a phase slope. All three must be pure numbers, or they could not be the same Q."""
    omega0 = (STIFFNESS / MASS) ** 0.5
    gamma = DAMPING / MASS
    assert (omega0 / gamma).check("[]")
    assert (omega0 / Quantity(0.4, "rad/s")).check("[]")  # bandwidth route
    phase_slope = Quantity(2.0, "rad") / Quantity(0.8, "rad/s")  # dphi/domega
    assert (0.5 * omega0 * phase_slope).check("[]")


def test_transient_takeover_time_is_a_time():
    """2/gamma is the transient's lifetime; expressed in periods it is Q/pi, a pure number."""
    gamma = DAMPING / MASS
    omega0 = (STIFFNESS / MASS) ** 0.5
    assert (2.0 / gamma).check("[time]")
    assert ((2.0 / gamma) / (2.0 * np.pi / omega0)).check("[]")


def test_the_green_function_turns_an_impulse_into_a_displacement():
    """G carries [time]/[mass], so that (G * F) dt comes out in metres and nothing else.

    The dimensions are the contract of the whole module: convolving a Green function with a
    force history, integrating over time, must give a position. Written out, G is a length per
    unit impulse — metres per newton-second — and this is the check that the 1/(m omega_d) in
    front of the ringing is not a stray omega away from that.
    """
    omega_d = (STIFFNESS / MASS - (DAMPING / MASS) ** 2 / 4.0) ** 0.5
    green = 1.0 / (MASS * omega_d)
    assert green.check("[time] / [mass]")
    assert (green * FORCE * Quantity(1.0, "s")).check("[length]")

    # The step response is the same statement at zero frequency: F0/k is a length.
    assert (FORCE / STIFFNESS).check("[length]")


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
    assert isinstance(oscillators.resonance_peak_omega(0.5, 8.0, 0.4), float)
    sweep = np.linspace(0.1, 8.0, 401)
    response = oscillators.steady_state_response(sweep, 0.5, 8.0, 0.4, 1.0)
    assert response.dtype == np.complex128
    assert oscillators.power_absorbed(sweep, 0.5, 8.0, 0.4, 1.0).dtype == np.float64
    assert isinstance(oscillators.q_from_bandwidth(sweep, np.abs(response)), float)
    assert isinstance(oscillators.q_from_phase_slope(sweep, np.angle(response)), float)
    ramp = np.linspace(0.0, 4.0, 401)
    assert oscillators.impulse_response(ramp, 0.5, 8.0, 0.4).dtype == np.float64
    assert oscillators.step_response(ramp, 0.5, 8.0, 0.4, 1.0).dtype == np.float64
    assert (
        oscillators.convolution_response(np.ones(401), 0.01, 0.5, 8.0, 0.4).dtype == np.float64
    )
    assert isinstance(fourier.gibbs_overshoot(31), float)
    times = (np.arange(512) - 256) * 0.01
    duration, bandwidth = fourier.rms_widths(fourier.gaussian_pulse(times, 0.3), 0.01)
    assert isinstance(duration, float) and isinstance(bandwidth, float)
    assert fourier.spectrum(fourier.gaussian_pulse(times, 0.3), 0.01)[1].dtype == np.complex128


def test_the_spectrum_axis_is_an_angular_frequency():
    """`spectrum` must return radians per second, not hertz — a factor of 2 pi with a name.

    The library speaks angular frequency everywhere, and this is the one place a stray 2 pi
    could hide without changing any shape on a plot: the curve would look right and every
    frequency read off it would be wrong by 6.28.
    """
    sample_dt = Quantity(0.01, "s")
    count = 4096
    spacing = 2.0 * np.pi / (count * sample_dt)
    assert spacing.check("1/[time]")

    nyquist = np.pi / sample_dt
    assert nyquist.check("1/[time]")

    omega, _ = fourier.spectrum(np.zeros(count), sample_dt.magnitude)
    assert np.isclose(omega[1] - omega[0], spacing.magnitude, rtol=1e-12)
    assert np.isclose(omega.max() + (omega[1] - omega[0]), nyquist.magnitude, rtol=1e-12)


def test_the_uncertainty_product_is_dimensionless():
    """Delta t times Delta omega multiplies a time by an inverse time — a pure number.

    That is what lets one inequality serve a pulse in nanoseconds, a wave packet in microns
    and a laser linewidth in megahertz without ever being restated.
    """
    duration = Quantity(2.0e-3, "s")
    bandwidth = Quantity(250.0, "1/s")
    assert (duration * bandwidth).check("[]")


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
