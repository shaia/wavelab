"""Kinetic theory: a gas of free particles in a rigid box, and the pressure it exerts.

MODEL SPECIFICATION
    System:        N point particles of mass m in a rectangular container
    Dynamics:      free flight between perfectly elastic collisions with the walls;
                   particles do not interact with one another
    Boundary:      rigid, fixed walls (a movable piston is modelled by changing the box size)
    Ensemble:      approximately microcanonical — energy is exactly conserved, and the
                   initial velocities are drawn from a Maxwell-Boltzmann distribution at T
    Ignored:       intermolecular forces, particle size, quantum effects, gravity, and any
                   mechanism that would let the gas thermalise on its own
    Valid when:    dilute classical regime, where the mean free path exceeds the particle size
                   and the thermal de Broglie wavelength is small compared to the spacing
    Failure modes: high density (particle-particle collisions matter), low temperature
                   (quantum statistics), strong interactions (the ideal gas law breaks down)

Because the particles never collide with each other, this model cannot *establish* a
Maxwell-Boltzmann distribution — it can only preserve one. That is the honest limit of the
model, and the reason the distribution is imposed at t = 0.

Pressure here is the time-averaged force per unit wall area, obtained by summing the momentum
each wall collision transfers. In d dimensions the "area" of a wall is a (d-1)-dimensional
measure: a length in 2D, an area in 3D.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .constants import K_B


@dataclass(frozen=True)
class GasState:
    """Positions and velocities of every particle, plus the box that contains them."""

    positions: np.ndarray  # (N, d), metres
    velocities: np.ndarray  # (N, d), metres/second
    box: np.ndarray  # (d,) side lengths, metres
    mass: float  # kilograms per particle

    @property
    def n_particles(self) -> int:
        return int(self.positions.shape[0])

    @property
    def dimension(self) -> int:
        return int(self.positions.shape[1])

    @property
    def volume(self) -> float:
        """Box volume — an area in 2D, a volume in 3D."""
        return float(np.prod(self.box))

    @property
    def wall_measure(self) -> float:
        """Total wall extent that pressure acts on: perimeter in 2D, surface area in 3D."""
        volume = self.volume
        return float(2.0 * np.sum(volume / self.box))

    @property
    def kinetic_energy(self) -> float:
        return float(0.5 * self.mass * np.sum(self.velocities**2))

    @property
    def kinetic_temperature(self) -> float:
        """Temperature read off the mean kinetic energy via equipartition, <E> = (d/2) k_B T."""
        mean_energy = self.kinetic_energy / self.n_particles
        return float(2.0 * mean_energy / (self.dimension * K_B))


def sample_maxwell_boltzmann(n_particles: int, temperature: float, mass: float,
                             rng: np.random.Generator, dimension: int = 2) -> np.ndarray:
    """Draw velocities from the Maxwell-Boltzmann distribution at `temperature`.

    Each Cartesian component is independently Gaussian with variance k_B T / m — the form
    that follows from the Boltzmann factor exp(-m v^2 / 2 k_B T) factorising over components.
    """
    if temperature <= 0 or mass <= 0:
        raise ValueError("temperature and mass must be positive")
    sigma = np.sqrt(K_B * temperature / mass)
    return rng.normal(0.0, sigma, size=(n_particles, dimension))


def initialise_gas(n_particles: int, box: tuple[float, ...], temperature: float, mass: float,
                   rng: np.random.Generator, remove_drift: bool = True,
                   fix_temperature: bool = True) -> GasState:
    """Place particles uniformly in the box with Maxwell-Boltzmann velocities at `temperature`.

    The two flags choose which ensemble the gas is drawn from, and the choice matters:

    `fix_temperature=True` (default) rescales the velocities so the total kinetic energy is
    exactly (d/2) N k_B T. Energy is then sharp and the sample behaves microcanonically —
    convenient when a run should start at the temperature it claims.

    `fix_temperature=False` keeps the raw Maxwell-Boltzmann draw, so the total energy
    fluctuates from sample to sample exactly as a canonical system's does. This is the
    setting to use when studying fluctuations: rescaling would remove the very quantity
    being measured.

    `remove_drift` subtracts the net momentum so the container's rest frame is also the gas's,
    which stops a random overall drift from masquerading as thermal motion.
    """
    box_array = np.asarray(box, dtype=float)
    if np.any(box_array <= 0):
        raise ValueError("box side lengths must be positive")
    dimension = box_array.size

    positions = rng.uniform(0.0, 1.0, size=(n_particles, dimension)) * box_array
    velocities = sample_maxwell_boltzmann(n_particles, temperature, mass, rng, dimension)

    if remove_drift and n_particles > 1:
        velocities -= velocities.mean(axis=0)

    if fix_temperature and n_particles > 1:
        target = 0.5 * dimension * n_particles * K_B * temperature
        current = 0.5 * mass * np.sum(velocities**2)
        velocities *= np.sqrt(target / current)

    return GasState(positions=positions, velocities=velocities, box=box_array, mass=mass)


@dataclass(frozen=True)
class SimulationResult:
    """Per-step record of a run: the impulse delivered to the walls, and the energy."""

    times: np.ndarray  # (steps,) end time of each step
    impulses: np.ndarray  # (steps,) momentum given to the walls during the step
    kinetic_energy: np.ndarray  # (steps,) total kinetic energy after the step
    final_state: GasState
    wall_measure: float

    @property
    def duration(self) -> float:
        return float(self.times[-1])

    def pressure(self, discard_fraction: float = 0.0) -> float:
        """Time-averaged pressure: total wall impulse per unit time per unit wall extent.

        Force on the walls is the rate of momentum transfer, so P = (sum of impulses) /
        (duration x wall measure). `discard_fraction` drops an initial transient, which this
        model does not have but real measurements usually do.
        """
        start = int(discard_fraction * self.impulses.size)
        impulses = self.impulses[start:]
        if impulses.size == 0:
            raise ValueError("discard_fraction left no samples")
        elapsed = self.times[-1] - (self.times[start - 1] if start > 0 else 0.0)
        return float(impulses.sum() / (elapsed * self.wall_measure))

    def windowed_pressures(self, n_windows: int) -> np.ndarray:
        """Pressure measured over `n_windows` consecutive equal time windows.

        This is the time series a pressure gauge would show, and it is what makes "a steady
        macroscopic number out of violent individual events" visible.

        Read its *spread* with care. Non-interacting particles bounce periodically, so each
        one delivers a regular train of impulses and the long-time average is fixed by the
        microstate alone. What is left in the window-to-window scatter is mostly the partial
        bounce at each window edge, not thermal fluctuation. To measure the physical N^(-1/2)
        law, compare pressures across independently drawn microstates
        (`initialise_gas(..., fix_temperature=False)`), which is what the fluctuation tests do.
        """
        if n_windows < 1 or n_windows > self.impulses.size:
            raise ValueError("n_windows must be between 1 and the number of steps")
        usable = (self.impulses.size // n_windows) * n_windows
        chunks = self.impulses[:usable].reshape(n_windows, -1)
        window_time = self.duration * usable / self.impulses.size / n_windows
        return chunks.sum(axis=1) / (window_time * self.wall_measure)


def simulate(state: GasState, dt: float, n_steps: int) -> SimulationResult:
    """Advance the gas by `n_steps` steps of `dt`, recording wall impulses.

    Free flight plus specular reflection is integrated *exactly* rather than approximately:
    a particle that would leave the box is mirrored back, which is what the exact trajectory
    does. The result is therefore independent of `dt` — provided a particle cannot cross more
    than one wall per axis per step, which `max_stable_dt` quantifies.
    """
    if dt <= 0 or n_steps < 1:
        raise ValueError("dt must be positive and n_steps at least 1")

    positions = state.positions.copy()
    velocities = state.velocities.copy()
    box = state.box
    mass = state.mass

    impulses = np.empty(n_steps)
    energies = np.empty(n_steps)

    for step in range(n_steps):
        positions += velocities * dt

        # Reflect off the low walls (x < 0) and the high walls (x > L). A particle is mirrored
        # about the wall it crossed, and hands the wall twice its normal momentum.
        below = positions < 0.0
        above = positions > box
        transferred = 2.0 * mass * (
            np.abs(velocities[below]).sum() + np.abs(velocities[above]).sum()
        )

        positions[below] = -positions[below]
        positions[above] = 2.0 * np.broadcast_to(box, positions.shape)[above] - positions[above]
        velocities[below | above] *= -1.0

        impulses[step] = transferred
        energies[step] = 0.5 * mass * np.sum(velocities**2)

    if np.any(positions < 0.0) or np.any(positions > box):
        raise RuntimeError(
            "a particle crossed a wall more than once in a single step, so the reflection is "
            "no longer exact — reduce dt (see max_stable_dt)"
        )

    final = GasState(positions=positions, velocities=velocities, box=box, mass=mass)
    times = np.arange(1, n_steps + 1, dtype=float) * dt
    return SimulationResult(
        times=times,
        impulses=impulses,
        kinetic_energy=energies,
        final_state=final,
        wall_measure=state.wall_measure,
    )


def max_stable_dt(state: GasState, safety: float = 0.25) -> float:
    """Largest step for which no particle crosses a wall twice in one step.

    Reflection is exact only under that condition, so this is a validity limit of the
    simulation, not a numerical accuracy knob.
    """
    fastest = np.abs(state.velocities).max()
    if fastest == 0:
        return np.inf
    return float(safety * state.box.min() / fastest)


def ideal_gas_pressure(n_particles: int, temperature: float, volume: float) -> float:
    """P = N k_B T / V — the equation of state the simulation is checked against.

    Dimensionally consistent in any dimension: `volume` is an area in 2D and the returned
    pressure is then a force per unit length.
    """
    if volume <= 0:
        raise ValueError("volume must be positive")
    return n_particles * K_B * temperature / volume


def mean_kinetic_energy(temperature: float, dimension: int = 2) -> float:
    """Equipartition: <E> = (d/2) k_B T for a free particle in d dimensions."""
    return 0.5 * dimension * K_B * temperature


def rms_speed(temperature: float, mass: float, dimension: int = 2) -> float:
    """Root-mean-square speed, sqrt(d k_B T / m)."""
    return float(np.sqrt(dimension * K_B * temperature / mass))
