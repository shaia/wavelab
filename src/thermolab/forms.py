"""Differential forms in the plane: when does an integral depend on the path?

This module is pure mathematics — no gas, no energy, no units. It exists so that the
distinction the course leans on hardest can be met first as a fact about `M dx + N dy`,
before it arrives wearing physical clothes.

A form is *exact* when it is the total differential of some potential f, which happens exactly
when the mixed partials agree. An integral of an exact form depends only on its endpoints; an
integral of an inexact form depends on the route taken between them. `thermolab.paths` puts
this to work on the P-V plane, where the inexact form is the one whose integral is work.

Everything here is deterministic: no generator argument, and no model specification, because
nothing is being modelled.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

Field = Callable[[np.ndarray, np.ndarray], np.ndarray]


def line_integral(m: Field, n: Field, x: np.ndarray, y: np.ndarray) -> float:
    """Integrate M dx + N dy along the path sampled by the points (x, y).

    The path is taken to be the polyline through the sampled points and each segment is
    handled by the trapezoid rule, so the result converges to the true integral at second
    order in the sampling spacing. `m` and `n` must accept arrays and return arrays.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.shape != y.shape:
        raise ValueError("x and y must describe the same points")
    if x.ndim != 1 or x.size < 2:
        raise ValueError("a path needs at least two points")

    m_values = np.asarray(m(x, y), dtype=float)
    n_values = np.asarray(n(x, y), dtype=float)
    m_mid = 0.5 * (m_values[:-1] + m_values[1:])
    n_mid = 0.5 * (n_values[:-1] + n_values[1:])
    return float(np.sum(m_mid * np.diff(x) + n_mid * np.diff(y)))


def mixed_partials_gap(m: Field, n: Field, x: np.ndarray, y: np.ndarray,
                       h: float = 1e-5) -> np.ndarray:
    """The exactness test: dM/dy - dN/dx at each sampled point, by central differences.

    The gap vanishes everywhere for an exact form and is non-zero for an inexact one, so this
    decides path-independence without integrating anything. Central differences leave a
    truncation error of order h^2, which is why a "zero" here means "small compared with the
    scale of M and N", not a bit-exact zero.
    """
    x = np.atleast_1d(np.asarray(x, dtype=float))
    y = np.atleast_1d(np.asarray(y, dtype=float))
    if x.shape != y.shape:
        raise ValueError("x and y must describe the same points")
    if h <= 0:
        raise ValueError("h must be positive")

    dm_dy = (np.asarray(m(x, y + h)) - np.asarray(m(x, y - h))) / (2.0 * h)
    dn_dx = (np.asarray(n(x + h, y)) - np.asarray(n(x - h, y))) / (2.0 * h)
    return np.asarray(dm_dy - dn_dx, dtype=float)


def is_exact(m: Field, n: Field, x: np.ndarray, y: np.ndarray, tolerance: float = 1e-6) -> bool:
    """True when the mixed-partials gap is negligible at every sampled point.

    The verdict only covers the region actually sampled: a form can be exact on part of the
    plane and not on another, so pass points that cover the region you care about.
    """
    return bool(np.all(np.abs(mixed_partials_gap(m, n, x, y)) <= tolerance))
