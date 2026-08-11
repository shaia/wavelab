"""The harmonic oscillator: free, damped, driven — closed forms and a numerical integrator.

MODEL SPECIFICATION
    System:        a point mass on a massless linear spring, moving in one dimension; the
                   observables are position, velocity, and the kinetic/potential energies
    Dynamics:      Newton's second law with force -k x - b v + F0 cos(omega t); closed-form
                   solutions where they exist, velocity-Verlet integration elsewhere
    Boundary:      none — the mass moves on an infinite line and nothing is exchanged
    Ensemble:      a single deterministic trajectory per choice of initial conditions; no
                   randomness anywhere in this module
    Ignored:       spring mass, nonlinearity at large extension, static friction, and every
                   microscopic mechanism behind the damping coefficient b
    Valid when:    displacements stay in the linear regime of the real spring and the time
                   step stays well below the oscillation period
    Failure modes: amplitudes that feel the spring's nonlinearity, time steps near the
                   stability limit, and any question about where the dissipated energy goes

Closed forms follow the project phase convention (constants.SIGN_CONVENTION): the driven
steady state is the complex amplitude X = (F0/m) / (omega0^2 - omega^2 - i gamma omega),
whose argument is the angle by which the displacement *lags* the drive.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Trajectory:
    """A numerically integrated trajectory, initial state included.

    `times[0] == 0` with the given initial conditions; all three arrays share one length.
    """

    times: np.ndarray
    positions: np.ndarray
    velocities: np.ndarray


def natural_frequency(mass: float, stiffness: float) -> float:
    """The undamped angular frequency, omega0 = sqrt(k / m) [rad/s]."""
    _validate_oscillator(mass, stiffness)
    return float(np.sqrt(stiffness / mass))


def amplitude_phase(x0: float, v0: float, omega0: float) -> tuple[float, float]:
    """Amplitude and phase of the free oscillation with the given initial conditions.

    Returns `(A, phi)` such that `x(t) = A cos(omega0 t + phi)`. Starting at rest from x0
    gives phi = 0; starting at the origin moving in +x gives phi = -pi/2.
    """
    if omega0 <= 0:
        raise ValueError("omega0 must be positive")
    amplitude = float(np.hypot(x0, v0 / omega0))
    phase = float(np.arctan2(-v0 / omega0, x0))
    return amplitude, phase


def position(
    t: np.ndarray, mass: float, stiffness: float, x0: float, v0: float
) -> np.ndarray:
    """Closed-form position of the undamped oscillator, x(t) = A cos(omega0 t + phi)."""
    omega0 = natural_frequency(mass, stiffness)
    amplitude, phase = amplitude_phase(x0, v0, omega0)
    return amplitude * np.cos(omega0 * np.asarray(t) + phase)


def velocity(
    t: np.ndarray, mass: float, stiffness: float, x0: float, v0: float
) -> np.ndarray:
    """Closed-form velocity of the undamped oscillator, the time derivative of `position`."""
    omega0 = natural_frequency(mass, stiffness)
    amplitude, phase = amplitude_phase(x0, v0, omega0)
    return -amplitude * omega0 * np.sin(omega0 * np.asarray(t) + phase)


def energies(
    positions: np.ndarray, velocities: np.ndarray, mass: float, stiffness: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Kinetic, potential, and total energy along a trajectory, in that order [J]."""
    _validate_oscillator(mass, stiffness)
    kinetic = 0.5 * mass * np.asarray(velocities) ** 2
    potential = 0.5 * stiffness * np.asarray(positions) ** 2
    return kinetic, potential, kinetic + potential


def damping_rate(mass: float, damping: float) -> float:
    """The damping rate gamma = b / m [1/s]; amplitude decays as e^{-gamma t / 2}."""
    _validate_oscillator(mass, 1.0)
    if damping < 0:
        raise ValueError("damping must be non-negative")
    return damping / mass


def quality_factor(mass: float, stiffness: float, damping: float) -> float:
    """The quality factor Q = sqrt(m k) / b = omega0 / gamma, dimensionless."""
    _validate_oscillator(mass, stiffness)
    if damping <= 0:
        raise ValueError("damping must be positive — an undamped oscillator has no Q")
    return float(np.sqrt(mass * stiffness) / damping)


def damping_regime(mass: float, stiffness: float, damping: float) -> str:
    """Which of the three regimes: 'underdamped', 'critical', or 'overdamped'.

    The boundary is b = 2 sqrt(m k), i.e. gamma = 2 omega0. Floating point makes exact
    criticality a measure-zero event; this reports 'critical' only on exact equality and is
    meant for labelling, not for choosing numerical branches — `damped_position` handles the
    near-critical region continuously.
    """
    _validate_oscillator(mass, stiffness)
    if damping < 0:
        raise ValueError("damping must be non-negative")
    critical = 2.0 * np.sqrt(mass * stiffness)
    if damping < critical:
        return "underdamped"
    if damping > critical:
        return "overdamped"
    return "critical"


def damped_position(
    t: np.ndarray, mass: float, stiffness: float, damping: float, x0: float, v0: float
) -> np.ndarray:
    """Closed-form position of the damped free oscillator, in all three regimes.

    Underdamped: e^{-gamma t/2} (C cos omega_d t + D sin omega_d t) with
    omega_d = sqrt(omega0^2 - gamma^2/4); critical: (C + D t) e^{-omega0 t}; overdamped: the
    sum of two decaying exponentials. The three branches agree in the limit, and a test
    approaches the critical boundary from both sides to hold this function to that.
    """
    omega0 = natural_frequency(mass, stiffness)
    gamma = damping_rate(mass, damping)
    time = np.asarray(t, dtype=float)
    discriminant = omega0**2 - gamma**2 / 4.0

    if discriminant > 0:  # underdamped
        omega_d = np.sqrt(discriminant)
        c1 = x0
        c2 = (v0 + gamma * x0 / 2.0) / omega_d
        return np.exp(-gamma * time / 2.0) * (
            c1 * np.cos(omega_d * time) + c2 * np.sin(omega_d * time)
        )
    if discriminant == 0:  # critical
        return (x0 + (v0 + omega0 * x0) * time) * np.exp(-omega0 * time)
    # overdamped: real roots r = -gamma/2 +/- sqrt(gamma^2/4 - omega0^2)
    root = np.sqrt(-discriminant)
    r_plus = -gamma / 2.0 + root
    r_minus = -gamma / 2.0 - root
    c_plus = (v0 - r_minus * x0) / (r_plus - r_minus)
    c_minus = x0 - c_plus
    return c_plus * np.exp(r_plus * time) + c_minus * np.exp(r_minus * time)


def driven_amplitude(
    omega_drive: float,
    mass: float,
    stiffness: float,
    damping: float,
    force_amplitude: float,
) -> complex:
    """The steady-state complex amplitude of the driven, damped oscillator.

    With drive F0 cos(omega t) and the course's e^{-i omega t} time factor, the steady state
    is x(t) = Re[X e^{-i omega t}] with

        X = (F0 / m) / (omega0^2 - omega^2 - i gamma omega).

    |X| is the response amplitude and arg(X) the angle by which the displacement lags the
    drive: +pi/2 exactly at omega0, and the *amplitude* peak sits below omega0, at
    omega^2 = omega0^2 - gamma^2/2, whenever there is damping.
    """
    omega0 = natural_frequency(mass, stiffness)
    gamma = damping_rate(mass, damping)
    if omega_drive < 0:
        raise ValueError("omega_drive must be non-negative")
    denominator = omega0**2 - omega_drive**2 - 1j * gamma * omega_drive
    if denominator == 0:
        raise ValueError("undamped oscillator driven exactly at resonance has no steady state")
    return complex(force_amplitude / mass / denominator)


def max_stable_dt(mass: float, stiffness: float) -> float:
    """A time step comfortably inside the integrator's accurate regime: T0 / 100.

    Velocity Verlet only becomes unstable near dt = 2/omega0, but accuracy degrades long
    before that; one hundred steps per period keeps the phase error per period below a
    fraction of a percent. Mirrors the role of the same-named function in courses' other
    simulation modules.
    """
    omega0 = natural_frequency(mass, stiffness)
    return 2.0 * np.pi / omega0 / 100.0


def simulate(
    mass: float,
    stiffness: float,
    x0: float,
    v0: float,
    dt: float,
    n_steps: int,
    damping: float = 0.0,
    drive_amplitude: float = 0.0,
    drive_omega: float = 0.0,
) -> Trajectory:
    """Integrate m x'' = -k x - b x' + F0 cos(omega t) by velocity Verlet.

    Kick-drift-kick. The closing kick is implicit in the velocity — for a force linear in v
    that is one division, `(1 + gamma dt / 2)` — which keeps the scheme second order with
    damping and reduces *exactly* to standard velocity Verlet when b = 0, where it is
    symplectic: the energy error stays bounded over arbitrarily many periods instead of
    drifting. The conservation and convergence test categories pin both properties.
    """
    _validate_oscillator(mass, stiffness)
    if damping < 0:
        raise ValueError("damping must be non-negative")
    if dt <= 0:
        raise ValueError("dt must be positive")
    if n_steps < 1:
        raise ValueError("n_steps must be positive")

    gamma = damping_rate(mass, damping)
    omega0_sq = stiffness / mass
    force_per_mass = drive_amplitude / mass

    times = np.arange(n_steps + 1) * dt
    positions = np.empty(n_steps + 1)
    velocities = np.empty(n_steps + 1)
    positions[0] = x0
    velocities[0] = v0

    x = float(x0)
    v = float(v0)
    for step in range(n_steps):
        t_now = step * dt
        t_next = t_now + dt
        accel_now = -omega0_sq * x - gamma * v + force_per_mass * np.cos(drive_omega * t_now)
        v_half = v + 0.5 * dt * accel_now
        x = x + dt * v_half
        conservative_next = -omega0_sq * x + force_per_mass * np.cos(drive_omega * t_next)
        v = (v_half + 0.5 * dt * conservative_next) / (1.0 + 0.5 * dt * gamma)
        positions[step + 1] = x
        velocities[step + 1] = v

    return Trajectory(times=times, positions=positions, velocities=velocities)


def _validate_oscillator(mass: float, stiffness: float) -> None:
    if mass <= 0:
        raise ValueError("mass must be positive")
    if stiffness <= 0:
        raise ValueError("stiffness must be positive")
