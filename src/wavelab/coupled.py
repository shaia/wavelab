"""Coupled oscillators — masses joined by springs, in the site picture and the mode picture.

MODEL SPECIFICATION
    System:        N point masses on a line joined by linear springs, described by a mass
                   matrix M and a stiffness matrix K; the observables are displacements,
                   velocities, and the energy attributed to each site or to each mode
    Dynamics:      M x'' + K x = 0, solved exactly by modal decomposition and independently
                   by velocity-Verlet integration — discover before diagonalizing
    Boundary:      fixed walls, free ends, or a periodic ring, chosen by whichever builder
                   assembled the matrices
    Ensemble:      a single deterministic trajectory per choice of initial conditions; noise
                   only via `wavelab.measurement`, randomness only from a seeded generator
    Ignored:       damping, driving, spring masses, nonlinearity, and the distinction between
                   transverse and longitudinal motion — one polarization, one dimension
    Valid when:    M is symmetric positive definite and K symmetric positive semi-definite
                   (linear springs, small displacements), and the time step stays well below
                   the period of the fastest mode
    Failure modes: matrices that are not symmetric; the zero modes of a free or periodic
                   chain misread as an error; amplitudes large enough for nonlinearity to
                   couple the modes, at which point superposition itself fails

Two pictures of one motion run through this file. In the *site* picture the coordinates are the
displacements of individual masses, energy sloshes between them, and nothing is conserved
except the total. In the *mode* picture the coordinates are combinations that oscillate
independently, each at its own frequency, each holding its energy forever. The whole content of
a coupled system is that the second picture exists.

The eigenproblem is the generalized one, K a = omega^2 M a, and it is solved in plain NumPy: a
Cholesky factorization M = L L^T turns it into the ordinary symmetric problem for
L^-1 K L^-T, whose eigenvectors carry back to M-orthonormal mode shapes. No SciPy, so this runs
unchanged in the browser kernel the laboratories use.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# A frequency below this fraction of the fastest one is a zero mode rather than a slow
# oscillation, and has to be evolved as `q0 + qdot0 t` instead of as a cosine. Free and
# periodic chains have genuine zero modes — the whole system translating, costing nothing —
# and `normal_mode_solve` hands them back near 1e-8 rather than at 0, because a square root
# turns an eigenvalue's rounding error into a much larger relative one. The slowest *real*
# mode of an N-mass chain sits near pi/N of the fastest, so any threshold between those two
# does; 1e-6 is far from both.
ZERO_MODE_RELATIVE_TOLERANCE = 1e-6


@dataclass(frozen=True)
class CoupledTrajectory:
    """A numerically integrated trajectory of a coupled system, initial state included.

    `times[0] == 0`; `positions[i]` and `velocities[i]` are the full state vectors at
    `times[i]`, so both arrays have shape (n_steps + 1, N).
    """

    times: np.ndarray
    positions: np.ndarray
    velocities: np.ndarray


@dataclass(frozen=True)
class Modes:
    """The normal modes of a system: frequencies ascending, shapes as columns.

    `shapes[:, p]` is the pattern of displacement belonging to `frequencies[p]`, normalised so
    that `shapes.T @ mass_matrix @ shapes` is the identity. The mass matrix is kept because
    projecting a state onto these shapes needs it.
    """

    frequencies: np.ndarray
    shapes: np.ndarray
    mass_matrix: np.ndarray


def two_mass_matrices(
    mass: float, stiffness: float, coupling: float, detune: float = 0.0
) -> tuple[np.ndarray, np.ndarray]:
    """Mass and stiffness matrices of two masses anchored by springs and joined by a third.

    Each mass is held to a wall by a spring of stiffness `stiffness` and to its neighbour by
    one of stiffness `coupling`, so

        K = [[k + k_c, -k_c], [-k_c, k(1 + detune) + k_c]],   M = m * identity.

    The off-diagonal entries are what make the equations coupled: without `coupling` the matrix
    is diagonal and the two masses never learn of each other's existence.

    `detune` scales the *second* mass's anchor stiffness only, breaking the symmetry between
    the two oscillators. At zero it is the identical pair the module studies; swept through
    zero it traces an avoided crossing, the two frequencies approaching and turning away
    without ever meeting.
    """
    if mass <= 0:
        raise ValueError("mass must be positive")
    if stiffness <= 0:
        raise ValueError("stiffness must be positive")
    if coupling < 0:
        raise ValueError("coupling must be non-negative")
    if detune <= -1.0:
        raise ValueError("detune must exceed -1 — the second anchor spring cannot go slack")

    mass_matrix = mass * np.eye(2)
    stiffness_matrix = np.array(
        [
            [stiffness + coupling, -coupling],
            [-coupling, stiffness * (1.0 + detune) + coupling],
        ]
    )
    return mass_matrix, stiffness_matrix


def chain_matrices(
    n: int, mass: float, stiffness: float, boundary: str = "fixed"
) -> tuple[np.ndarray, np.ndarray]:
    """Mass and stiffness matrices of `n` equal masses in a row on identical springs.

    This is the two-mass system with the "two" taken out. Every mass is pulled back towards
    its neighbours and nothing else, so `K` is tridiagonal: a mass can only feel what it is
    tied to, and the width of the band is the range of the interaction. That single fact —
    each row of `K` reading `-k, 2k, -k` — is what turns into a second derivative when the
    masses are packed close enough together, and with it into the wave equation.

    `boundary` chooses what happens at the ends, and the choice changes the physics rather
    than merely tidying an edge case:

    - `"fixed"` puts a wall beyond each end mass, so there are `n + 1` springs holding `n`
      masses. Every mode costs energy, and the spectrum is the closed form
      `chain_mode_frequencies` gives.
    - `"free"` removes those two walls, leaving `n - 1` springs. The chain can now drift
      bodily without stretching anything, which is a genuine zero-frequency mode — momentum
      conservation showing up as an eigenvalue.
    - `"periodic"` joins the last mass back to the first, making a ring of `n` masses and `n`
      springs. It also has the translation zero mode, and its other modes come in
      equal-frequency pairs, because a ring has no preferred direction to travel round.

    The single fixed mass is the smallest useful case: two walls, two springs, and a
    frequency of `sqrt(2 k_s / m)` rather than `sqrt(k_s / m)`, because both springs resist.
    """
    if n < 1:
        raise ValueError("a chain needs at least one mass")
    if mass <= 0:
        raise ValueError("mass must be positive")
    if stiffness <= 0:
        raise ValueError("stiffness must be positive")
    if boundary not in ("fixed", "free", "periodic"):
        raise ValueError(f"boundary must be 'fixed', 'free' or 'periodic', not {boundary!r}")
    if boundary != "fixed" and n < 2:
        raise ValueError(f"a {boundary} chain needs at least two masses")

    stiffness_matrix = np.zeros((n, n))
    neighbours = np.arange(n - 1)
    stiffness_matrix[neighbours, neighbours + 1] = -stiffness
    stiffness_matrix[neighbours + 1, neighbours] = -stiffness
    if boundary == "periodic":
        stiffness_matrix[0, -1] -= stiffness
        stiffness_matrix[-1, 0] -= stiffness

    # Each diagonal entry is the total stiffness felt by that mass, which is the sum of the
    # springs attached to it. Reading it off the off-diagonals means the two end conventions
    # need no separate arithmetic: a wall is simply a bond whose other end never moves.
    stiffness_matrix[np.diag_indices(n)] = -stiffness_matrix.sum(axis=1)
    if boundary == "fixed":
        stiffness_matrix[0, 0] += stiffness
        stiffness_matrix[-1, -1] += stiffness

    return mass * np.eye(n), stiffness_matrix


def normal_mode_solve(mass_matrix: np.ndarray, stiffness_matrix: np.ndarray) -> Modes:
    """Solve K a = omega^2 M a for every mode: frequencies ascending, M-orthonormal shapes.

    A Cholesky factorization M = L L^T reduces the generalized problem to the ordinary
    symmetric one for A = L^-1 K L^-T, whose eigenvectors u give mode shapes a = L^-T u. That
    route is used rather than a general eigensolver because A is symmetric by construction, so
    the frequencies come out real and the shapes orthogonal without either having to be hoped
    for. A is symmetrised explicitly before the eigensolve: it is symmetric in exact
    arithmetic, and rounding is not permitted to make it otherwise.

    Two details of the numerics are visible to callers:

    Eigenvalues are clipped at zero before the square root. A free or periodic chain has a
    genuine zero mode — the whole system translating, costing no energy — and its eigenvalue
    lands within rounding of zero on either side. Without the clip a tiny negative value would
    produce a nan; with it the frequency comes out near 1e-8 rather than exactly 0, because a
    square root turns an eigenvalue's absolute error into a much larger relative one. Test a
    zero mode against a small tolerance, never against equality.

    Mode shape signs are fixed so the largest-magnitude entry of each column is positive.
    Eigenvectors are only defined up to sign, and the underlying routine's choice is arbitrary
    but not random: without this the symmetric mode of an identical pair comes back as
    (-1, -1), which is the same physical motion drawn upside down and a nuisance in every plot
    and every test.
    """
    M = np.asarray(mass_matrix, dtype=float)
    K = np.asarray(stiffness_matrix, dtype=float)
    if M.ndim != 2 or M.shape[0] != M.shape[1]:
        raise ValueError("mass matrix must be square")
    if K.shape != M.shape:
        raise ValueError("stiffness matrix must have the same shape as the mass matrix")
    if not np.allclose(M, M.T):
        raise ValueError("mass matrix must be symmetric")
    if not np.allclose(K, K.T):
        raise ValueError("stiffness matrix must be symmetric")

    try:
        factor = np.linalg.cholesky(M)
    except np.linalg.LinAlgError as error:
        raise ValueError("mass matrix must be positive definite") from error

    inverse = np.linalg.inv(factor)
    reduced = inverse @ K @ inverse.T
    eigenvalues, vectors = np.linalg.eigh(0.5 * (reduced + reduced.T))
    frequencies = np.sqrt(np.clip(eigenvalues, 0.0, None))
    shapes = inverse.T @ vectors

    for column in shapes.T:
        dominant = column[np.argmax(np.abs(column))]
        if dominant < 0:
            column *= -1.0

    return Modes(frequencies=frequencies, shapes=shapes, mass_matrix=M)


def mode_coordinates(
    modes: Modes, x0: np.ndarray, v0: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Project a state onto the normal modes, as `(q, qdot)`.

    The shapes are orthonormal with respect to M rather than to the ordinary dot product, so
    the projection carries the mass matrix with it: q = shapes^T M x. Physically, this is the
    question "how much of each independent motion is present?", and the answer is what turns a
    tangle of coupled coordinates into a list of separate oscillators.

    `x0` and `v0` may be single state vectors or whole trajectories of shape (n_samples, N),
    exactly as `site_energies` accepts; the result carries the same leading shape. Watching
    the modal coordinates along a trajectory is how a page shows that they do not move.
    """
    shapes = modes.shapes
    weighted = shapes.T @ modes.mass_matrix
    single = np.ndim(x0) == 1
    positions = np.atleast_2d(np.asarray(x0, dtype=float))
    velocities = np.atleast_2d(np.asarray(v0, dtype=float))
    if positions.shape != velocities.shape:
        raise ValueError("x0 and v0 must have the same shape")
    if positions.ndim != 2 or positions.shape[-1] != shapes.shape[0]:
        raise ValueError("x0 and v0 must be state vectors matching the number of masses")
    q = positions @ weighted.T
    qdot = velocities @ weighted.T
    return (q[0], qdot[0]) if single else (q, qdot)


def evolve(modes: Modes, x0: np.ndarray, v0: np.ndarray, t: np.ndarray) -> np.ndarray:
    """The exact motion at time(s) `t`, assembled mode by mode rather than stepped.

    Project the starting state onto the modes, let each modal coordinate run as the
    independent module-01 oscillator it is, and add the results back up:

        x_j(t) = sum_p a_p(j) [ q_p(0) cos(omega_p t) + (qdot_p(0) / omega_p) sin(omega_p t) ].

    Nothing here is an approximation and nothing accumulates: the state at t = 10^6 seconds
    costs exactly what the state at t = 1 costs, and is exactly as accurate. That is the
    practical dividend of the whole change of basis, and the reason a hundred-mass chain can
    be animated without integrating anything. `simulate_coupled` remains the honest check —
    it steps the coupled equations and has never heard of a mode — and the two agreeing to
    integrator tolerance is what licenses this shortcut.

    A zero mode has no frequency to oscillate at and drifts instead: `q_p(0) + qdot_p(0) t`,
    the free chain sliding along at constant speed. Taking the cosine formula's limit would
    divide by zero; this branch is that limit taken by hand.

    `t` may be a scalar or an array; the result is a state vector or an array of shape
    (len(t), N) to match.
    """
    q0, qdot0 = mode_coordinates(modes, x0, v0)
    times = np.atleast_1d(np.asarray(t, dtype=float))
    omega = modes.frequencies

    fastest = float(np.max(omega)) if omega.size else 0.0
    moving = omega > ZERO_MODE_RELATIVE_TOLERANCE * fastest
    q = np.empty((times.size, omega.size))
    phase = np.outer(times, omega[moving])
    q[:, moving] = q0[moving] * np.cos(phase) + (qdot0[moving] / omega[moving]) * np.sin(phase)
    q[:, ~moving] = q0[~moving] + np.outer(times, qdot0[~moving])

    positions = q @ modes.shapes.T
    return positions[0] if np.ndim(t) == 0 else positions


def modal_energies(modes: Modes, x0: np.ndarray, v0: np.ndarray) -> np.ndarray:
    """Energy held by each normal mode, `(qdot^2 + omega^2 q^2) / 2` [J].

    Each modal coordinate is an independent module-01 oscillator, so its energy is the
    familiar one and — this is the contract the conservation tests check — it is constant in
    time. Site energies are not; the difference between those two statements is what a normal
    mode *is*.

    A zero mode contributes only its kinetic term, which is correct: a freely translating
    system stores no potential energy in doing so.

    Like `site_energies`, this accepts single state vectors or whole trajectories of shape
    (n_samples, N) and returns the matching leading shape — which is what lets a page put the
    two pictures side by side over the same run: bars that slosh, and bars that do not.
    """
    q, qdot = mode_coordinates(modes, x0, v0)
    return 0.5 * (qdot**2 + modes.frequencies**2 * q**2)


def site_energies(
    mass_matrix: np.ndarray,
    stiffness_matrix: np.ndarray,
    positions: np.ndarray,
    velocities: np.ndarray,
) -> np.ndarray:
    """Energy attributed to each mass, along a whole trajectory [J].

    Kinetic energy belongs to a mass unambiguously. Spring energy does not — it lives in the
    bond, not at either end — so each spring's share is split half and half between the two
    masses it joins, and an anchor spring gives its whole energy to the mass it holds. The
    convention is a choice, and it is made here so that the site energies sum to the true total
    energy exactly, whatever the motion. Anything else would leave the pictures disagreeing
    about how much energy the system has.

    `positions` and `velocities` may be single state vectors or whole trajectories of shape
    (n_samples, N); the result carries the same leading shape.
    """
    M = np.asarray(mass_matrix, dtype=float)
    K = np.asarray(stiffness_matrix, dtype=float)
    single = np.ndim(positions) == 1
    x = np.atleast_2d(np.asarray(positions, dtype=float))
    v = np.atleast_2d(np.asarray(velocities, dtype=float))
    if x.shape != v.shape:
        raise ValueError("positions and velocities must have the same shape")
    if x.shape[-1] != M.shape[0]:
        raise ValueError("state vectors must match the number of masses")

    # Off-diagonal K[i, j] = -k_ij is the spring joining i and j; its energy is shared. What is
    # left on the diagonal once every bond has been accounted for is the anchor to the wall.
    energy = 0.5 * (v**2) * np.diag(M)
    n = M.shape[0]
    anchor = np.diag(K).copy()
    for i in range(n):
        for j in range(i + 1, n):
            bond = -K[i, j]
            if bond == 0.0:
                continue
            stored = 0.5 * bond * (x[:, i] - x[:, j]) ** 2
            energy[:, i] += 0.5 * stored
            energy[:, j] += 0.5 * stored
            anchor[i] -= bond
            anchor[j] -= bond
    energy += 0.5 * anchor * x**2

    return energy[0] if single else energy


def exchange_time(omega_a: float, omega_b: float) -> float:
    """How long two coupled oscillators take to hand their energy over and get it back [s].

    T_ex = 2 pi / |omega_a - omega_b|. Starting one oscillator of an identical pair excites
    both modes equally, and what follows is module 00's beat between them: the energy is fully
    transferred after half this time and fully returned after all of it. The splitting alone
    sets the tempo — the mode frequencies themselves are irrelevant, which is why a slow, clean
    exchange is the signature of weak coupling.
    """
    gap = abs(float(omega_a) - float(omega_b))
    if gap == 0.0:
        raise ValueError("degenerate frequencies never exchange — the splitting is zero")
    return 2.0 * np.pi / gap


def simulate_coupled(
    mass_matrix: np.ndarray,
    stiffness_matrix: np.ndarray,
    x0: np.ndarray,
    v0: np.ndarray,
    dt: float,
    n_steps: int,
) -> CoupledTrajectory:
    """Integrate M x'' + K x = 0 by velocity Verlet, knowing nothing about modes.

    The same kick-drift-kick scheme `oscillators.simulate` uses, promoted to vectors: the
    acceleration is a = -M^-1 K x, with M^-1 K formed once rather than solved for at every
    step. Being symplectic, it keeps the energy error bounded rather than letting it drift,
    which is what makes it trustworthy over the many exchange periods this module's questions
    require.

    This function is deliberately ignorant of the modal decomposition. When a page claims that
    the pair has two special motions, that claim is checked against an integrator with no
    notion of what a mode is — otherwise the check would assume what it set out to test.
    """
    M = np.asarray(mass_matrix, dtype=float)
    K = np.asarray(stiffness_matrix, dtype=float)
    if dt <= 0:
        raise ValueError("dt must be positive")
    if n_steps < 1:
        raise ValueError("n_steps must be at least one")

    x = np.array(x0, dtype=float)
    v = np.array(v0, dtype=float)
    if x.shape != (M.shape[0],) or v.shape != x.shape:
        raise ValueError("x0 and v0 must be vectors matching the number of masses")

    dynamics = np.linalg.solve(M, K)
    positions = np.empty((n_steps + 1, x.size))
    velocities = np.empty_like(positions)
    positions[0] = x
    velocities[0] = v

    acceleration = -dynamics @ x
    for step in range(n_steps):
        v = v + 0.5 * dt * acceleration
        x = x + dt * v
        acceleration = -dynamics @ x
        v = v + 0.5 * dt * acceleration
        positions[step + 1] = x
        velocities[step + 1] = v

    return CoupledTrajectory(
        times=np.arange(n_steps + 1) * dt, positions=positions, velocities=velocities
    )


def chain_mode_frequencies(n: int, mass: float, stiffness: float) -> np.ndarray:
    """The `n` mode frequencies of a fixed-end chain in closed form [rad/s], ascending.

        omega_p = 2 sqrt(k_s / m) sin( p pi / (2(N + 1)) ),   p = 1 .. N.

    This is the reference the numerical solver is held against, and it says three things at
    once. There are exactly `n` of them, one per mass, so the mode count is the degree-of-
    freedom count and not a coincidence. They are bounded: the sine cannot exceed one, so no
    chain of any length oscillates faster than `2 sqrt(k_s/m)`, which is the arrangement with
    every mass in antiphase with both its neighbours — there is nothing faster available.
    And the low ones are nearly evenly spaced, `omega_p ~ p`, which is what a plucked string
    sounding one note with harmonic overtones requires.
    """
    if n < 1:
        raise ValueError("a chain needs at least one mass")
    if mass <= 0 or stiffness <= 0:
        raise ValueError("mass and stiffness must be positive")
    p = np.arange(1, n + 1)
    return 2.0 * np.sqrt(stiffness / mass) * np.sin(p * np.pi / (2.0 * (n + 1)))


def chain_mode_shapes(n: int) -> np.ndarray:
    """The `n` mode shapes of a fixed-end chain, as orthonormal columns.

        a_p(j) ~ sin( p pi j / (N + 1) ),   j = 1 .. N,

    which is a sine wave sampled at the masses' positions — the standing wave a string will
    have in the continuum limit, read off at N points. Mode `p` has `p - 1` interior nodes,
    so the shapes can be sketched before anything is computed: more zero crossings, higher
    frequency, always in that order.

    Columns are normalised to unit length, which is `M`-orthonormality for unit masses;
    `normal_mode_solve` on a chain of mass `m` returns these divided by `sqrt(m)`, since its
    normalisation carries the mass matrix.

    Signs are the sine's own — `a_p(1) = sin(p pi/(N + 1))` is positive for every `p`, so no
    convention has to be imposed here. `normal_mode_solve` imposes a different one, making the
    *largest* entry positive, so its columns agree with these up to an overall sign per column
    and sometimes differ (mode 3 of a 3-chain, for one). That is not a disagreement about
    physics: a mode shape reversed is the same motion started half a period later, and nothing
    observable distinguishes them. Compare shapes up to sign, or compare `|a|`.

    The shapes do not depend on the mass or the stiffness at all, only on `n`. Changing
    either rescales every frequency together and leaves the patterns untouched, because the
    pattern is fixed by the geometry of the chain and the two ends holding it.
    """
    if n < 1:
        raise ValueError("a chain needs at least one mass")
    site = np.arange(1, n + 1)
    mode = np.arange(1, n + 1)
    return np.sqrt(2.0 / (n + 1)) * np.sin(np.outer(site, mode) * np.pi / (n + 1))


def chain_dispersion(
    wavenumber: np.ndarray, spacing: float, mass: float, stiffness: float
) -> np.ndarray:
    """The chain's dispersion relation [rad/s] — the course's first, and the model for the rest.

        omega(k) = 2 sqrt(k_s / m) |sin(k a / 2)|.

    A dispersion relation answers "how fast does a wave of this wavelength oscillate?", and
    every wave-carrying system in the rest of the course has one. This one has the two
    features to recognise elsewhere. At long wavelengths, `k a << 1`, the sine is its own
    argument and `omega = (a sqrt(k_s/m)) k`: strictly proportional, so every long wave
    travels at the same speed `c = a sqrt(k_s/m)` and a pulse built from them keeps its shape.
    That regime is where the chain behaves like a string. Approaching `k = pi/a` the curve
    flattens onto its maximum, neighbouring masses reach exact antiphase, and the chain
    refuses to carry anything faster — a cutoff imposed by the fact that the medium is made
    of discrete pieces at all.

    `wavenumber` beyond the band edge is not an error and not new physics: `k` and
    `k + 2 pi/a` sample the masses at identical displacements, so the formula repeats. There
    is no way to tell the two waves apart by looking at the chain, which is aliasing arriving
    a course ahead of schedule.
    """
    if spacing <= 0:
        raise ValueError("spacing must be positive")
    if mass <= 0 or stiffness <= 0:
        raise ValueError("mass and stiffness must be positive")
    k = np.asarray(wavenumber, dtype=float)
    return 2.0 * np.sqrt(stiffness / mass) * np.abs(np.sin(0.5 * k * spacing))


def chain_continuum_frequencies(n: int, mass: float, stiffness: float) -> np.ndarray:
    """The string frequencies the chain's low modes converge to [rad/s], ascending.

        omega_p^inf = p pi sqrt(k_s / m) / (N + 1) = p pi c / L,

    holding the total length `L = (N + 1) a` fixed while the masses are made smaller and more
    numerous. These are evenly spaced, `omega_p` exactly proportional to `p`, which is what a
    musical instrument needs and what the discrete chain only approximately delivers.

    The comparison is the point of the function, so its limits matter. Expanding
    `sin x = x - x^3/6` in `chain_mode_frequencies` gives a relative error of about
    `(p pi)^2 / (24 (N + 1)^2)`: second order in `1/N`, and growing as `p^2`. The continuum
    is therefore reached from the bottom of the band upwards — mode 1 is accurate long before
    mode 20 is — and the modes near `p = N` never converge at all, however large `N` grows.
    A string is what a chain looks like to a long wave, not what a chain is.
    """
    if n < 1:
        raise ValueError("a chain needs at least one mass")
    if mass <= 0 or stiffness <= 0:
        raise ValueError("mass and stiffness must be positive")
    p = np.arange(1, n + 1)
    return p * np.pi * np.sqrt(stiffness / mass) / (n + 1)
