"""Accuracy category 2: conservation.

The undamped oscillator conserves energy exactly; its symplectic integrator must keep the
energy error *bounded* — oscillating with amplitude (omega0 dt)^2 / 4 — rather than letting
it drift. Damping must only ever remove energy, and a driven steady state must not run away.
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import oscillators

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
