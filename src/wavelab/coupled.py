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
    """
    shapes = modes.shapes
    weighted = shapes.T @ modes.mass_matrix
    positions = np.asarray(x0, dtype=float)
    velocities = np.asarray(v0, dtype=float)
    if positions.shape != (shapes.shape[0],) or velocities.shape != positions.shape:
        raise ValueError("x0 and v0 must be vectors matching the number of masses")
    return weighted @ positions, weighted @ velocities


def modal_energies(modes: Modes, x0: np.ndarray, v0: np.ndarray) -> np.ndarray:
    """Energy held by each normal mode, `(qdot^2 + omega^2 q^2) / 2` [J].

    Each modal coordinate is an independent module-01 oscillator, so its energy is the
    familiar one and — this is the contract the conservation tests check — it is constant in
    time. Site energies are not; the difference between those two statements is what a normal
    mode *is*.

    A zero mode contributes only its kinetic term, which is correct: a freely translating
    system stores no potential energy in doing so.
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
