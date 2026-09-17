"""Waves on a one-dimensional medium — the field y(x, t) and the equation that moves it.

MODEL SPECIFICATION
    System:        the transverse displacement field y(x, t) of a one-dimensional medium on a
                   finite grid — a uniform or piecewise-uniform string here; dispersive media
                   in the extensions that part IV adds to this file
    Dynamics:      the linear wave equation mu y_tt = T y_xx, integrated by leapfrog FDTD or
                   evaluated from exact solutions; part IV adds dispersive generalisations
    Boundary:      fixed or free ends, or an impedance junction between two media; part IV may
                   add wide "open" windows for packet studies
    Ensemble:      deterministic; callers add noise via `wavelab.measurement`
    Ignored:       stiffness, damping, gravity sag, longitudinal motion, nonlinearity
    Valid when:    |dy/dx| << 1, and numerically when the Courant number S = v dt/dx <= 1 with
                   pulses resolved by many grid points
    Failure modes: CFL violation (exponential grid-scale blow-up); order-one slopes (the model,
                   not the code, breaks); grid dispersion on under-resolved features read as
                   physics

Space enters the course here. Until now a system's state was a list of numbers, one per mass;
from this file on it is a function of position, and the oscillator equation becomes a partial
differential equation. Nothing about the physics has changed to make that happen. The solver
below updates each grid point from its two neighbours, which is exactly what a chain of masses
on springs does — the computer solves the continuum equation by quietly rebuilding the chain
that `wavelab.coupled` describes, with mass `mu dx` at every point and springs of stiffness
`T / dx` between them.

The string always has uniform tension. That is not a simplification but a consequence of the
model: with purely transverse motion nothing pushes the string sideways, so the horizontal
force balance on every element makes T the same everywhere. Density is free to vary from point
to point, and a jump in it is how a junction between two media is built.

The energy functions answer what the solver leaves open: if no piece of the medium travels with
a pulse, what does? A density pair and a flux — u_K = (1/2) mu y_t^2, u_P = (1/2) T y_x^2 and
P = -T y_x y_t — obey du/dt + dP/dx = 0, which is the first local conservation law in the
course and the template for every later one. They are diagnostics: `simulate_string` never
consults them, so agreement between them and it is evidence rather than construction.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import overload

import numpy as np

# How far past 1 a Courant number may sit before it counts as a violation. `cfl_max_dt` returns
# dx / v, and v dt / dx computed back from that lands on 1 +/- a few 1e-16 rather than on 1, so
# an exact comparison would reject the very step the bound recommends. The genuine instability
# at S = 1 + epsilon grows by (1 + O(sqrt(epsilon))) per step and needs a physically meaningful
# epsilon to show up in any run a laboratory can afford; 1e-12 is far below that.
COURANT_TOLERANCE = 1e-12


@dataclass(frozen=True)
class StringEvolution:
    """A string integrated in time, sampled at the steps the solver was asked to keep.

    `x` holds the grid coordinates, starting at 0. `times[j]` is the time of saved step `j`,
    with `times[0] == 0`, and `y[j]` and `dydt[j]` are the displacement and transverse velocity
    of every grid point at that time, so both arrays have shape (len(times), len(x)). The
    velocity is kept so that energy diagnostics never have to difference noisy displacements
    to recover it.
    """

    times: np.ndarray
    x: np.ndarray
    y: np.ndarray
    dydt: np.ndarray


@overload
def wave_speed(tension: float, mu: float) -> float: ...
@overload
def wave_speed(tension: float | np.ndarray, mu: np.ndarray) -> np.ndarray: ...
@overload
def wave_speed(tension: np.ndarray, mu: float | np.ndarray) -> np.ndarray: ...
def wave_speed(tension: float | np.ndarray, mu: float | np.ndarray) -> float | np.ndarray:
    """The speed a disturbance travels at, v = sqrt(T / mu) [m/s].

    Two properties of the medium and nothing else: how hard the string pulls its pieces back
    toward the line, and how much inertia those pieces have. The amplitude, the width and the
    shape of the pulse do not appear, which is the sense in which the medium chooses the speed
    and the hand only chooses the shape.

    Either argument may be an array — a density that varies along the string gives a speed
    that does — and the result is a plain float when both are scalars.
    """
    tension_arr = np.asarray(tension, dtype=float)
    mu_arr = np.asarray(mu, dtype=float)
    if np.any(tension_arr <= 0):
        raise ValueError("tension must be positive")
    if np.any(mu_arr <= 0):
        raise ValueError("mu must be positive")
    speed = np.sqrt(tension_arr / mu_arr)
    return float(speed) if speed.ndim == 0 else speed


def cfl_max_dt(dx: float, v_max: float) -> float:
    """The largest stable time step for the leapfrog string, dt = dx / v_max [s].

    The Courant-Friedrichs-Lewy condition S = v dt / dx <= 1 says that in one step nothing may
    travel further than one grid spacing. The update of a grid point only consults its
    immediate neighbours, so a disturbance that genuinely moved further than that in one step
    would be outrunning the only information the scheme has; past S = 1 the shortest
    wavelengths the grid can hold grow exponentially instead, and the solution is destroyed
    from the grid scale upward.

    This is the bound itself, not a recommendation to sit on it. S = 1 exactly is a special
    step — see `simulate_string` — but on a string whose density varies, this step puts
    S = 1 only where the string is lightest and the waves fastest; everywhere else S < 1.
    """
    if dx <= 0:
        raise ValueError("dx must be positive")
    if v_max <= 0:
        raise ValueError("v_max must be positive")
    return float(dx) / float(v_max)


def simulate_string(
    y0: np.ndarray,
    v0: np.ndarray,
    dx: float,
    dt: float,
    tension: float,
    mu: float | np.ndarray,
    n_steps: int,
    boundary: tuple[str, str] = ("fixed", "fixed"),
    allow_unstable: bool = False,
    save_every: int = 1,
) -> StringEvolution:
    """Integrate mu y_tt = T y_xx on a grid, by the leapfrog scheme.

    Grid point i sits at x_i = i dx and obeys

        y_i^{n+1} = 2 y_i^n - y_i^{n-1} + S_i^2 (y_{i+1}^n - 2 y_i^n + y_{i-1}^n),

    with S_i = v_i dt / dx. Read as physics rather than as a stencil, this is Newton's law for
    a mass `mu dx` pulled by springs of stiffness `T / dx` toward its two neighbours: the
    discretisation runs the continuum limit backwards, and the string on the computer is a
    chain of masses again.

    The steps are taken in kick-drift-kick form — the velocity Verlet that
    `oscillators.simulate` and `coupled.simulate_coupled` use — and eliminating the velocity
    from it returns the stencil above exactly, starting from y^1 = y^0 + dt v^0 + (dt^2/2) a^0.
    The velocity form is used because it delivers dy/dt at the same instants as y, which the
    energy diagnostics need.

    Stability. The scheme is stable when S = max(v) dt / dx <= 1 and grows exponentially from
    the grid scale when it is not. By default a violation raises `ValueError` before any work
    is done; `allow_unstable=True` runs it anyway, for the laboratory that exists to watch the
    blow-up, and the displacement then overflows to inf and nan rather than raising.

    The magic step. At S = 1 on a uniform string the update becomes
    y_i^{n+1} = y_{i+1}^n + y_{i-1}^n - y_i^{n-1}, which transports a travelling shape by
    exactly one grid spacing per step with no error at all — given exact values at the first
    two steps. A shape released from rest gets them, so a pluck is reproduced to rounding for
    as long as the run lasts. A start with velocity does not: its second level is off by
    O(dt^3), and the transport, faithful to that too, splits the defect into counter-moving
    pieces whose sum settles at O(dt^2) — several times smaller than S = 1/2 gives on the same
    grid, but no longer exact.

    Boundaries, one entry per end:

    - `"fixed"` holds the end at zero displacement, whatever `y0` and `v0` say there.
    - `"free"` lets the end move with zero slope, as a ring sliding on a frictionless rod. The
      end point then carries half a cell of string, `mu dx / 2`, which is what makes the
      trapezoid weights in `total_energy` the conserved ones.

    `mu` may be a scalar or one value per grid point, lumped at that point; a jump in it is a
    junction between two media. `tension` is a scalar, for the reason the module docstring
    gives. `save_every` keeps every k-th step (step 0 always), so a long run on a fine grid can
    be animated without storing all of it.
    """
    y = np.array(y0, dtype=float)
    velocity = np.array(v0, dtype=float)
    if y.ndim != 1 or y.size < 3:
        raise ValueError("y0 must be a one-dimensional grid of at least three points")
    if velocity.shape != y.shape:
        raise ValueError("v0 must have the same shape as y0")
    if dx <= 0:
        raise ValueError("dx must be positive")
    if dt <= 0:
        raise ValueError("dt must be positive")
    if np.ndim(tension) != 0:
        raise ValueError("tension must be a scalar — a string at rest has uniform tension")
    if tension <= 0:
        raise ValueError("tension must be positive")
    if n_steps < 1:
        raise ValueError("n_steps must be at least one")
    if save_every < 1:
        raise ValueError("save_every must be at least one")
    if len(boundary) != 2 or any(side not in ("fixed", "free") for side in boundary):
        raise ValueError(f"boundary must be a pair of 'fixed' or 'free', not {boundary!r}")

    if np.shape(mu) not in ((), y.shape):
        raise ValueError("mu must be a scalar or one value per grid point")
    density = np.broadcast_to(np.asarray(mu, dtype=float), y.shape)
    if np.any(density <= 0):
        raise ValueError("mu must be positive")

    courant = float(np.max(np.sqrt(tension / density))) * dt / dx
    if courant > 1.0 + COURANT_TOLERANCE and not allow_unstable:
        raise ValueError(
            f"Courant number {courant:.4g} exceeds 1: the scheme is unstable "
            "(pass allow_unstable=True to watch it fail)"
        )

    # T / (mu dx^2) is the chain's k_s / m at every point; the ends are handled separately.
    coefficient = tension / (density * dx**2)
    fixed = [index for index, side in ((0, boundary[0]), (-1, boundary[1])) if side == "fixed"]
    y[fixed] = 0.0
    velocity[fixed] = 0.0

    def acceleration(displacement: np.ndarray) -> np.ndarray:
        result = np.empty_like(displacement)
        result[1:-1] = coefficient[1:-1] * (
            displacement[2:] - 2.0 * displacement[1:-1] + displacement[:-2]
        )
        # A free end reflects its neighbour into a ghost point, y_{-1} = y_1, so the slope there
        # vanishes; a fixed end never accelerates.
        result[0] = 2.0 * coefficient[0] * (displacement[1] - displacement[0])
        result[-1] = 2.0 * coefficient[-1] * (displacement[-2] - displacement[-1])
        result[fixed] = 0.0
        return result

    saved = n_steps // save_every + 1
    displacements = np.empty((saved, y.size))
    velocities = np.empty_like(displacements)
    displacements[0] = y
    velocities[0] = velocity

    # An unstable run is expected to overflow; that is the result, not an accident to report.
    errors = "ignore" if allow_unstable else "warn"
    with np.errstate(over=errors, invalid=errors):
        current = acceleration(y)
        for step in range(1, n_steps + 1):
            velocity += 0.5 * dt * current
            y += dt * velocity
            current = acceleration(y)
            velocity += 0.5 * dt * current
            if step % save_every == 0:
                displacements[step // save_every] = y
                velocities[step // save_every] = velocity

    return StringEvolution(
        times=np.arange(saved) * save_every * dt,
        x=np.arange(y.size) * dx,
        y=displacements,
        dydt=velocities,
    )


def dalembert_solution(
    y0_func: Callable[[np.ndarray], np.ndarray],
    v: float,
    x: np.ndarray,
    t: float | np.ndarray,
    v0_integral: Callable[[np.ndarray], np.ndarray] | None = None,
) -> np.ndarray:
    """The exact motion of an unbounded string from its initial shape and velocity.

        y(x, t) = [y0(x - vt) + y0(x + vt)] / 2 + [W(x + vt) - W(x - vt)] / (2 v),

    where W is any antiderivative of the initial velocity, W' = v0. Every solution of the wave
    equation is a right-mover f(x - vt) plus a left-mover g(x + vt); this is the pair the
    initial conditions select.

    The two terms are the two ways to start a string. A pluck — a shape held still and
    released — has no velocity term, and splits into two copies of half the height running
    apart. It *must* split: a single copy moving one way would need a velocity from the start.
    A strike — a flat string given a velocity — has no shape term, and spreads into a plateau
    whose edges run outward at v.

    The velocity enters through its antiderivative rather than as a function to be integrated
    numerically, so the result is exact for any velocity profile whose integral can be written
    down, including a discontinuous one: a rectangular strike of speed w over [a, b] has
    W(s) = w * clip(s - a, 0, b - a).

    Both callables must accept arrays. `x` is a one-dimensional array; `t` may be a scalar,
    giving an array like `x`, or an array, giving shape (len(t), len(x)). No boundaries exist
    here, so comparing this with `simulate_string` means keeping the pulses away from the ends.
    """
    if v <= 0:
        raise ValueError("v must be positive")
    positions = np.asarray(x, dtype=float)
    if positions.ndim != 1:
        raise ValueError("x must be a one-dimensional array")
    times = np.atleast_1d(np.asarray(t, dtype=float))

    behind = positions[np.newaxis, :] - v * times[:, np.newaxis]  # argument of the right-mover
    ahead = positions[np.newaxis, :] + v * times[:, np.newaxis]  # argument of the left-mover
    displacement = 0.5 * (np.asarray(y0_func(behind)) + np.asarray(y0_func(ahead)))
    if v0_integral is not None:
        displacement = displacement + (
            np.asarray(v0_integral(ahead)) - np.asarray(v0_integral(behind))
        ) / (2.0 * v)
    displacement = np.broadcast_to(displacement, behind.shape).astype(float)

    return displacement[0] if np.ndim(t) == 0 else displacement


def kinetic_density(dydt: np.ndarray | float, mu: np.ndarray | float) -> np.ndarray | float:
    """Kinetic energy per unit length of a moving string, u_K = (1/2) mu (dy/dt)^2 [J/m].

    A length dx of string is a particle of mass mu dx moving sideways at dy/dt, and this is
    its kinetic energy divided by dx. Nothing here is special to waves: it is module 01's
    (1/2) m v^2, written per metre because there is now a string's worth of it everywhere.

    `dydt` may be a single snapshot, a whole history of shape (n_times, n_points), or one
    number; `mu` may be a scalar or one value per grid point.
    """
    velocity = np.asarray(dydt, dtype=float)
    density = np.asarray(mu, dtype=float)
    if np.any(density <= 0):
        raise ValueError("mu must be positive")
    return 0.5 * density * velocity**2


def potential_density(dydx: np.ndarray | float, tension: float) -> np.ndarray | float:
    """Potential energy per unit length of a stretched string, u_P = (1/2) T (dy/dx)^2 [J/m].

    A string stores energy by being longer than it was. Tilting a length dx to a slope y_x
    lengthens it to sqrt(1 + y_x^2) dx, and the work done against a constant tension T is
    T times that extra length,

        T (sqrt(1 + y_x^2) - 1) dx = (1/2) T y_x^2 dx + O(y_x^4) dx,

    so the density is (1/2) T y_x^2. The expansion is the small-slope assumption again, one
    order deeper than the wave equation needed it: where the equation of motion dropped terms
    of order y_x^2, the energy keeps them and drops y_x^4.

    Note what this says about where a wave's energy is. It is not the displacement that stores
    energy but the *slope* — a stretch of string lifted bodily and held flat stores nothing,
    however high it is held. On a travelling sine the steepest points are the zero crossings,
    which is where both densities peak, and the crests are momentarily empty.
    """
    slope = np.asarray(dydx, dtype=float)
    if tension <= 0:
        raise ValueError("tension must be positive")
    return 0.5 * float(tension) * slope**2


def energy_flux(
    dydx: np.ndarray | float, dydt: np.ndarray | float, tension: float
) -> np.ndarray | float:
    """Power crossing a point of the string, toward +x, P = -T (dy/dx)(dy/dt) [W].

    Cut the string at x. The left piece holds the right one up, pulling it along the string's
    own direction with tension T, whose transverse component is -T y_x for small slopes. That
    force acts on a point moving at y_t, and force times velocity is the rate the left piece
    does work on the right: the energy per second handed across the cut.

    The sign is the direction, and both signs occur. A right-moving wave has y_t = -v y_x, so
    P = T v y_x^2 >= 0 — energy always flows the way the wave goes, whether the string is
    rising or falling there. A left-mover has y_t = +v y_x and P <= 0. On a standing wave the
    flux reverses twice a cycle and averages to zero everywhere: the energy sloshes between
    neighbouring quarter-wavelengths and none of it goes anywhere.

    Together with `kinetic_density` and `potential_density` this satisfies the course's first
    local conservation law, du/dt + dP/dx = 0, with u = u_K + u_P.
    """
    slope = np.asarray(dydx, dtype=float)
    velocity = np.asarray(dydt, dtype=float)
    if tension <= 0:
        raise ValueError("tension must be positive")
    return -float(tension) * slope * velocity


def total_energy(
    y: np.ndarray,
    dydt: np.ndarray,
    dx: float,
    tension: float,
    mu: float | np.ndarray,
) -> float | np.ndarray:
    """Kinetic plus potential energy of the whole string [J].

        E = sum_i (1/2) mu_i w_i (dy_i/dt)^2 + sum_cells (1/2) T ((y_{i+1} - y_i) / dx)^2 dx,

    with trapezoid weights w_i: dx inside, dx/2 at the two end points. Both sums are the
    continuum integrals of (1/2) mu y_t^2 and (1/2) T y_x^2, discretised the way the solver
    discretises the string — the kinetic term at the grid points, where the masses are, and the
    potential term on the cells between them, where the springs are. That pairing is what makes
    this the quantity `simulate_string` keeps: its error then oscillates, bounded and second
    order in dt, rather than drifting.

    `y` and `dydt` may be single snapshots or whole histories of shape (n_samples, N); the
    result is a float or an array of one energy per sample. `mu` may vary along the string.
    """
    single = np.ndim(y) == 1
    displacement = np.atleast_2d(np.asarray(y, dtype=float))
    velocity = np.atleast_2d(np.asarray(dydt, dtype=float))
    if displacement.shape != velocity.shape:
        raise ValueError("y and dydt must have the same shape")
    if displacement.ndim != 2 or displacement.shape[-1] < 2:
        raise ValueError("y must be a grid of at least two points, or a history of them")
    if dx <= 0:
        raise ValueError("dx must be positive")
    if tension <= 0:
        raise ValueError("tension must be positive")

    points = displacement.shape[-1]
    density = np.broadcast_to(np.asarray(mu, dtype=float), (points,))
    weights = np.full(points, float(dx))
    weights[[0, -1]] = 0.5 * dx

    kinetic = 0.5 * np.sum(density * weights * velocity**2, axis=-1)
    potential = 0.5 * tension * np.sum(np.diff(displacement, axis=-1) ** 2, axis=-1) / dx
    energy = kinetic + potential
    return float(energy[0]) if single else energy


def sinusoidal_mean_power(amplitude: float, omega: float, tension: float, mu: float) -> float:
    """Average power a travelling sine carries along the string, (1/2) mu v omega^2 A^2 [W].

    For y = Re[A e^{i(kx - omega t)}] the flux is P = T v y_x^2 = mu v omega^2 A^2 cos^2(...),
    and the mean of cos^2 over a cycle is 1/2. Every factor earns its place: doubling the
    amplitude quadruples the power, and so does doubling the frequency, because the flux goes
    as the square of the transverse velocity A omega. Sending a wave twice as fast for a given
    shape — a tighter string — costs power in proportion to v.

    Written with the impedance Z = sqrt(T mu) = mu v this is (1/2) Z (A omega)^2: an amplitude
    times a property of the medium, the form module 10 generalises and every later part of the
    course reuses, down to a laser beam's intensity being proportional to the square of its
    field.
    """
    if omega < 0:
        raise ValueError("omega must be non-negative")
    speed = wave_speed(tension, mu)
    return 0.5 * float(mu) * speed * float(omega) ** 2 * float(amplitude) ** 2
