"""Thermodynamic paths in the P-V plane, and the work done along them.

SIGN CONVENTION (project-wide): dU = δQ + δW_on. For a quasistatic change of volume the work
done ON the gas is

    δW_on = -P dV        so        W_on = -∫ P dV,

negative when the gas expands. Everything in this module returns work done ON the system;
`work_by_system` is provided for the one place engine efficiencies need the other sign, and
it is defined as its negation so the two can never drift apart.

MODEL SPECIFICATION
    System:        a fixed amount of ideal gas, N particles
    Dynamics:      quasistatic — the gas is in equilibrium at every point of the path, so a
                   single (P, V) pair describes it and P dV is meaningful
    Boundary:      a cylinder closed by a frictionless piston
    Ensemble:      not applicable; this is macroscopic thermodynamics
    Ignored:       friction, turbulence, finite-rate effects, gas non-ideality
    Valid when:    the process is slow compared to the gas's internal relaxation time
    Failure modes: fast (irreversible) processes, where the gas has no single pressure and
                   the area under a drawn curve is not the work
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np

from .constants import K_B


def ideal_gas_pressure(n_particles: int, temperature: float, volume: float) -> float:
    """P = N k_B T / V."""
    if volume <= 0:
        raise ValueError("volume must be positive")
    return n_particles * K_B * temperature / volume


def ideal_gas_temperature(n_particles: int, pressure: float, volume: float) -> float:
    """T = P V / (N k_B)."""
    return pressure * volume / (n_particles * K_B)


def isothermal_pressure(volumes: np.ndarray, n_particles: int, temperature: float) -> np.ndarray:
    """P(V) along an isotherm: P = N k_B T / V."""
    volumes = np.asarray(volumes, dtype=float)
    return n_particles * K_B * temperature / volumes


def adiabatic_pressure(volumes: np.ndarray, p_ref: float, v_ref: float,
                       gamma: float) -> np.ndarray:
    """P(V) along a quasistatic adiabat: P V^gamma = const.

    `gamma` is the heat-capacity ratio: 5/3 for a monatomic ideal gas in 3D, 2 in 2D.
    """
    volumes = np.asarray(volumes, dtype=float)
    return p_ref * (v_ref / volumes) ** gamma


def work_on_gas(volumes: Sequence[float], pressures: Sequence[float]) -> float:
    """Work done ON the gas along a sampled path: W_on = -∫ P dV, by the trapezoid rule.

    The samples define the path, so this is exactly how a student's hand-drawn curve in the
    P-V plane is turned into a number.
    """
    v = np.asarray(list(volumes), dtype=float)
    p = np.asarray(list(pressures), dtype=float)
    if v.shape != p.shape or v.size < 2:
        raise ValueError("volumes and pressures must have the same shape and at least 2 points")
    return float(-np.trapezoid(p, v))


def work_by_system(volumes: Sequence[float], pressures: Sequence[float]) -> float:
    """Work done BY the gas, +∫ P dV — the negation of `work_on_gas`.

    Defined only so that engine and efficiency discussions can use the conventional sign
    without ever rewriting the first law.
    """
    return -work_on_gas(volumes, pressures)


def work_along(pressure_of_volume: Callable[[np.ndarray], np.ndarray], v_start: float,
               v_end: float, n_points: int = 513) -> float:
    """Work done ON the gas for a path given as a function P(V), sampled on `n_points`.

    Increasing `n_points` is the refinement knob the convergence tests use; the trapezoid
    rule converges at second order, which those tests verify rather than assume.
    """
    volumes = np.linspace(v_start, v_end, n_points)
    return work_on_gas(volumes, np.asarray(pressure_of_volume(volumes), dtype=float))


def isothermal_work_on_gas(n_particles: int, temperature: float, v_start: float,
                           v_end: float) -> float:
    """Exact isothermal result: W_on = -N k_B T ln(V_end / V_start)."""
    return -n_particles * K_B * temperature * float(np.log(v_end / v_start))


def adiabatic_work_on_gas(p_start: float, v_start: float, p_end: float, v_end: float,
                          gamma: float) -> float:
    """Exact quasistatic adiabatic result: W_on = (P_end V_end - P_start V_start)/(gamma - 1).

    Equivalently ΔU, since δQ = 0 along an adiabat — the cleanest illustration that work
    becomes path-independent exactly when the path is constrained enough to fix the state.
    """
    if gamma == 1:
        raise ValueError("gamma = 1 is isothermal, not adiabatic")
    return (p_end * v_end - p_start * v_start) / (gamma - 1.0)


def isobaric_work_on_gas(pressure: float, v_start: float, v_end: float) -> float:
    """Exact isobaric result: W_on = -P (V_end - V_start)."""
    return -pressure * (v_end - v_start)


@dataclass(frozen=True)
class Path:
    """A path in the P-V plane, stored as the points that define it.

    Two paths sharing endpoints generally give different work — that difference is the whole
    point of the module, and `internal_energy_change` shows the contrast: it depends only on
    the endpoints.
    """

    volumes: np.ndarray
    pressures: np.ndarray
    label: str = ""

    def __post_init__(self) -> None:
        v = np.asarray(self.volumes, dtype=float)
        p = np.asarray(self.pressures, dtype=float)
        if v.shape != p.shape or v.size < 2:
            raise ValueError("a path needs matching volume and pressure arrays of length >= 2")
        object.__setattr__(self, "volumes", v)
        object.__setattr__(self, "pressures", p)

    @property
    def start(self) -> tuple[float, float]:
        return float(self.volumes[0]), float(self.pressures[0])

    @property
    def end(self) -> tuple[float, float]:
        return float(self.volumes[-1]), float(self.pressures[-1])

    @property
    def is_closed(self) -> bool:
        return bool(np.isclose(self.volumes[0], self.volumes[-1])
                    and np.isclose(self.pressures[0], self.pressures[-1]))

    def work_on_gas(self) -> float:
        return work_on_gas(self.volumes, self.pressures)

    def internal_energy_change(self, degrees_of_freedom: int = 3) -> float:
        """ΔU between the endpoints of an ideal gas path.

        U = (f/2) N k_B T and N k_B T = PV, so U = (f/2) PV and no particle count is needed.
        A state function: it ignores everything the path did in between, which is exactly
        what makes it different from the work.
        """
        v0, p0 = self.start
        v1, p1 = self.end
        return 0.5 * degrees_of_freedom * (p1 * v1 - p0 * v0)

    def heat_into_gas(self, degrees_of_freedom: int = 3) -> float:
        """Q from the first law: Q = ΔU - W_on. A path function, like the work."""
        return self.internal_energy_change(degrees_of_freedom) - self.work_on_gas()


def isothermal_path(n_particles: int, temperature: float, v_start: float, v_end: float,
                    n_points: int = 257, label: str = "isothermal") -> Path:
    volumes = np.linspace(v_start, v_end, n_points)
    return Path(volumes, isothermal_pressure(volumes, n_particles, temperature), label)


def adiabatic_path(p_start: float, v_start: float, v_end: float, gamma: float,
                   n_points: int = 257, label: str = "adiabatic") -> Path:
    volumes = np.linspace(v_start, v_end, n_points)
    return Path(volumes, adiabatic_pressure(volumes, p_start, v_start, gamma), label)


def isobaric_path(pressure: float, v_start: float, v_end: float, n_points: int = 2,
                  label: str = "isobaric") -> Path:
    volumes = np.linspace(v_start, v_end, n_points)
    return Path(volumes, np.full_like(volumes, pressure), label)


def isochoric_path(volume: float, p_start: float, p_end: float, n_points: int = 2,
                   label: str = "isochoric") -> Path:
    pressures = np.linspace(p_start, p_end, n_points)
    return Path(np.full_like(pressures, volume), pressures, label)


def join(*paths: Path, label: str = "composite") -> Path:
    """Concatenate paths end to end, dropping the duplicated junction points.

    The two-leg route (isobaric then isochoric) versus the direct isotherm between the same
    endpoints is the standard demonstration that work is a path function.
    """
    if not paths:
        raise ValueError("join needs at least one path")
    volumes = [paths[0].volumes]
    pressures = [paths[0].pressures]
    for previous, nxt in zip(paths, paths[1:], strict=False):
        if not (np.isclose(previous.end[0], nxt.start[0])
                and np.isclose(previous.end[1], nxt.start[1])):
            raise ValueError(f"paths do not meet: {previous.end} then {nxt.start}")
        volumes.append(nxt.volumes[1:])
        pressures.append(nxt.pressures[1:])
    return Path(np.concatenate(volumes), np.concatenate(pressures), label)
