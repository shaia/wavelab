"""Accuracy category 2: conservation.

The undamped oscillator conserves energy exactly; its symplectic integrator must keep the
energy error *bounded* — oscillating with amplitude (omega0 dt)^2 / 4 — rather than letting
it drift. Damping must only ever remove energy, and a driven steady state must not run away.
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import fourier, oscillators

pytestmark = pytest.mark.conservation

MASS = 0.5
STIFFNESS = 8.0
OMEGA0 = oscillators.natural_frequency(MASS, STIFFNESS)
PERIOD = 2.0 * np.pi / OMEGA0


def _long_run(n_periods: int = 100) -> tuple[oscillators.Trajectory, int]:
    dt = oscillators.max_stable_dt(MASS, STIFFNESS)
    steps_per_period = round(PERIOD / dt)
    trajectory = oscillators.simulate(
        MASS, STIFFNESS, 0.1, 0.0, dt, n_periods * steps_per_period
    )
    return trajectory, steps_per_period


def test_energy_error_stays_bounded_over_a_hundred_periods():
    """Velocity Verlet's energy error oscillates at (omega0 dt)^2/4 and must not exceed it."""
    trajectory, _ = _long_run()
    _, _, total = oscillators.energies(
        trajectory.positions, trajectory.velocities, MASS, STIFFNESS
    )
    bound = (OMEGA0 * oscillators.max_stable_dt(MASS, STIFFNESS)) ** 2 / 4.0
    assert (total.max() - total.min()) / total[0] < 1.5 * bound


def test_energy_shows_no_secular_drift():
    """Bounded oscillation is symplecticity's promise; the *mean* energy must not walk.

    A non-symplectic scheme (plain Euler, RK4 at this step size) fails this by orders of
    magnitude: its energy error accumulates monotonically instead of averaging out.
    """
    trajectory, steps_per_period = _long_run()
    _, _, total = oscillators.energies(
        trajectory.positions, trajectory.velocities, MASS, STIFFNESS
    )
    first_period = total[:steps_per_period].mean()
    last_period = total[-steps_per_period:].mean()
    assert abs(last_period - first_period) / total[0] < 1e-7


def test_phase_space_trajectory_stays_on_its_ellipse():
    """omega0^2 x^2 + v^2 is energy in disguise; the orbit must not spiral in or out."""
    trajectory, _ = _long_run()
    radius_sq = OMEGA0**2 * trajectory.positions**2 + trajectory.velocities**2
    bound = (OMEGA0 * oscillators.max_stable_dt(MASS, STIFFNESS)) ** 2 / 4.0
    assert (radius_sq.max() - radius_sq.min()) / radius_sq[0] < 1.5 * bound


def test_closed_form_conserves_energy_to_roundoff():
    """The analytic solution has no excuse: its energy is constant to machine precision."""
    t = np.linspace(0.0, 50.0 * PERIOD, 20001)
    x = oscillators.position(t, MASS, STIFFNESS, 0.1, 0.3)
    v = oscillators.velocity(t, MASS, STIFFNESS, 0.1, 0.3)
    _, _, total = oscillators.energies(x, v, MASS, STIFFNESS)
    assert (total.max() - total.min()) / total[0] < 1e-12


def test_damping_only_removes_energy():
    """With b > 0 and no drive, dE/dt = -b v^2 <= 0: the energy must never increase."""
    dt = oscillators.max_stable_dt(MASS, STIFFNESS)
    trajectory = oscillators.simulate(
        MASS, STIFFNESS, 0.1, 0.0, dt, 5000, damping=0.4
    )
    _, _, total = oscillators.energies(
        trajectory.positions, trajectory.velocities, MASS, STIFFNESS
    )
    increases = np.diff(total)
    assert increases.max() <= total[0] * 1e-12


def test_steady_state_input_power_equals_dissipated_power():
    """In the steady state the books balance: <F v> = <b v^2> = `power_absorbed`.

    Both averages are taken from an integration, not from the formula, so the closed form is
    on trial here rather than being assumed. This is where module 02's "the energy has to go
    somewhere" claim stops being rhetoric.
    """
    damping = 0.4
    drive_omega = 3.4
    force_amplitude = 1.0
    dt = PERIOD / 800.0
    trajectory = oscillators.simulate(
        MASS, STIFFNESS, 0.0, 0.0, dt, 80_000,
        damping=damping, drive_amplitude=force_amplitude, drive_omega=drive_omega,
    )

    # Whole cycles only, well past the 2/gamma transient, so the means are unbiased.
    cycle_steps = round(2.0 * np.pi / drive_omega / dt)
    tail = slice(-40 * cycle_steps, None)
    times = trajectory.times[tail]
    velocities = trajectory.velocities[tail]
    drive = force_amplitude * np.cos(drive_omega * times)

    input_power = float(np.mean(drive * velocities))
    dissipated = float(np.mean(damping * velocities**2))
    predicted = float(
        oscillators.power_absorbed(drive_omega, MASS, STIFFNESS, damping, force_amplitude)
    )

    assert np.isclose(input_power, dissipated, rtol=2e-3)
    assert np.isclose(input_power, predicted, rtol=2e-3)


def test_ringdown_energy_decays_at_gamma():
    """A free damped oscillation loses energy as e^{-gamma t}: amplitude decays at half that.

    Measured from the integration by fitting the log of the per-period energy, so it tests
    the integrator and the closed-form damping rate against each other.
    """
    damping = 0.2
    gamma = oscillators.damping_rate(MASS, damping)
    dt = oscillators.max_stable_dt(MASS, STIFFNESS)
    steps_per_period = round(PERIOD / dt)
    trajectory = oscillators.simulate(
        MASS, STIFFNESS, 0.1, 0.0, dt, 20 * steps_per_period, damping=damping
    )
    _, _, total = oscillators.energies(
        trajectory.positions, trajectory.velocities, MASS, STIFFNESS
    )

    n_periods = 20
    per_period = np.array(
        [total[i * steps_per_period : (i + 1) * steps_per_period].mean() for i in range(n_periods)]
    )
    period_times = (np.arange(n_periods) + 0.5) * PERIOD
    measured_gamma = -float(np.polyfit(period_times, np.log(per_period), 1)[0])
    assert np.isclose(measured_gamma, gamma, rtol=1e-2)


def test_driven_oscillator_energy_stays_bounded():
    """The damped driven oscillator settles into a steady state instead of running away."""
    dt = oscillators.max_stable_dt(MASS, STIFFNESS)
    trajectory = oscillators.simulate(
        MASS,
        STIFFNESS,
        0.0,
        0.0,
        dt,
        40_000,
        damping=0.4,
        drive_amplitude=1.0,
        drive_omega=OMEGA0,
    )
    _, _, total = oscillators.energies(
        trajectory.positions, trajectory.velocities, MASS, STIFFNESS
    )
    steady_state = abs(
        oscillators.driven_amplitude(OMEGA0, MASS, STIFFNESS, 0.4, 1.0)
    )
    energy_cap = 0.5 * STIFFNESS * (2.0 * steady_state) ** 2
    assert total.max() < energy_cap


def test_a_kick_deposits_exactly_the_kinetic_energy_it_carries():
    """An impulse J leaves J^2/2m in the oscillator, all of it kinetic, none of it potential.

    This is the energy face of the Green function's initial condition. The kick changes the
    velocity and nothing else, so at t = 0+ the spring is still slack: every joule is kinetic,
    and the total is (1/2) m v^2 with v = J/m. Read off the response itself rather than
    asserted about it, so that a mis-scaled G would fail here as well as in the limits file.
    """
    damping = 0.4
    impulse = 3.0
    dt = PERIOD / 20_000.0
    t = np.arange(4) * dt

    green = oscillators.impulse_response(t, MASS, STIFFNESS, damping)
    velocity = float(np.gradient(green, dt)[0]) * impulse
    assert np.isclose(velocity, impulse / MASS, rtol=1e-3)

    kinetic, potential, total = oscillators.energies(
        np.array([0.0]), np.array([impulse / MASS]), MASS, STIFFNESS
    )
    assert np.isclose(float(total[0]), impulse**2 / (2.0 * MASS), rtol=1e-12)
    assert float(kinetic[0]) == float(total[0])
    assert float(potential[0]) == 0.0


def test_the_convolved_response_never_outlasts_the_energy_put_into_it():
    """Damping only removes: a bounded force cannot leave the oscillator gaining energy.

    A burst is applied and then switched off, and from that moment the mechanical energy of
    the convolved response must decrease monotonically over whole half cycles. It is the
    check that `convolution_response`'s zero padding really did stop the DFT's periodic
    extension from wrapping the tail back onto the start, which would show up here as energy
    reappearing after the force has gone.
    """
    damping = 0.4
    dt = PERIOD / 400.0
    n = 4000
    t = np.arange(n) * dt
    force = np.where(t < 3.0 * PERIOD, np.cos(OMEGA0 * t), 0.0)

    x = oscillators.convolution_response(force, dt, MASS, STIFFNESS, damping)
    v = np.gradient(x, dt)
    _, _, total = oscillators.energies(x, v, MASS, STIFFNESS)

    after = t > 3.5 * PERIOD
    per_half_cycle = total[after][: (total[after].size // 200) * 200].reshape(-1, 200).max(axis=1)
    assert np.all(np.diff(per_half_cycle) < 0.0)


# Harmonic analysis conserves energy too: changing representation must not create or destroy
# any. Parseval is that statement, and it holds in both the periodic and the sampled worlds.
FOURIER_SAMPLES = 4096
FOURIER_DT = 0.01


def test_parseval_holds_for_the_fourier_coefficients():
    """Mean square in time equals the sum of |c_n|^2 — the harmonics carry all the power.

    The signal is built from a finite coefficient set, so it is exactly band-limited and the
    identity is exact rather than approximate: nothing is hiding above the cutoff. That makes
    a failure here unambiguous, which a truncated waveform could not.
    """
    coefficients = fourier.triangle_coefficients(9)
    phase = 2.0 * np.pi * np.arange(FOURIER_SAMPLES) / FOURIER_SAMPLES
    signal = fourier.partial_sum(coefficients, 1.0, phase)

    assert np.isclose(np.sum(np.abs(coefficients) ** 2), np.mean(signal**2), rtol=1e-12)
    recovered = fourier.fourier_coefficients(signal, 9)
    assert np.max(np.abs(recovered - coefficients)) < 1e-12


def test_parseval_holds_for_a_sampled_spectrum():
    """Energy in the record equals energy in its spectrum, once the 1/(2 pi) is respected.

    This is the identity that lets a later module read a spectrum panel as an energy budget
    rather than a picture, and it is where a wrong transform scaling would show up first.
    """
    times = (np.arange(FOURIER_SAMPLES) - FOURIER_SAMPLES // 2) * FOURIER_DT
    signal = fourier.gaussian_pulse(times, 0.3) * np.cos(12.0 * times)
    omega, transform = fourier.spectrum(signal, FOURIER_DT)

    time_energy = np.sum(np.abs(signal) ** 2) * FOURIER_DT
    spectral_energy = np.sum(np.abs(transform) ** 2) * (omega[1] - omega[0]) / (2.0 * np.pi)
    assert np.isclose(time_energy, spectral_energy, rtol=1e-10)


def test_the_spectrum_round_trips_through_its_inverse():
    """Analysis then synthesis returns the signal to machine precision, losing nothing.

    Module 12 propagates wave packets by transforming, multiplying by a phase, and
    transforming back, so any loss here would accumulate into that calculation rather than
    announcing itself.
    """
    times = (np.arange(FOURIER_SAMPLES) - FOURIER_SAMPLES // 2) * FOURIER_DT
    signal = fourier.gaussian_pulse(times, 0.4) * np.cos(9.0 * times)
    _, transform = fourier.spectrum(signal, FOURIER_DT)
    restored = fourier.inverse_spectrum(transform, FOURIER_DT)

    assert np.max(np.abs(restored - signal)) < 1e-12
    assert np.max(np.abs(restored.imag)) < 1e-12
