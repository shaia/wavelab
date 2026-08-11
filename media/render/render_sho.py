"""Render the demonstration animations for module 01 (the simple harmonic oscillator).

Animations are produced from `wavelab` itself, so what a student watches is the same model
they can read, run and test — never a hand-drawn impression of it.

Output is MP4, written by `_common.save`; see that module for why, and for the constraints the
format brings. The animations carry no words, so the same file serves both language sites; the
caption that explains each one is ordinary translated page prose rather than a subtitle track
that could silently drift from the text around it.

Run:  uv run python media/render/render_sho.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, FPS, save  # noqa: E402
from wavelab import oscillators  # noqa: E402

BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#059669"

MASS = 0.5
STIFFNESS = 8.0
OMEGA0 = oscillators.natural_frequency(MASS, STIFFNESS)


def _spring_points(x_mass: float, x_wall: float = -0.18, n_coils: int = 8) -> np.ndarray:
    """A zigzag spring from the wall to the mass, as an (N, 2) array of xy points."""
    n_points = 2 * n_coils + 2
    xs = np.linspace(x_wall, x_mass, n_points)
    ys = np.zeros(n_points)
    ys[1:-1] = 0.02 * np.where(np.arange(1, n_points - 1) % 2 == 0, 1.0, -1.0)
    return np.column_stack([xs, ys])


def render_portrait(n_frames: int = 300) -> None:
    """The mass on its spring beside x(t), v(t), and the energy exchange.

    The middle panel shows velocity leading position by a quarter period; the right panel
    shows the energies trading twice per cycle under a flat total.
    """
    x0, v0 = 0.1, 0.0
    duration = n_frames / FPS
    times = np.linspace(0.0, duration, n_frames)
    x = oscillators.position(times, MASS, STIFFNESS, x0, v0)
    v = oscillators.velocity(times, MASS, STIFFNESS, x0, v0)
    kinetic, potential, total = oscillators.energies(x, v, MASS, STIFFNESS)

    fig, (left, middle, right) = plt.subplots(
        1, 3, figsize=(9.6, 3.2), dpi=DPI, gridspec_kw={"width_ratios": [1.0, 1.7, 0.7]}
    )

    left.set_xlim(-0.2, 0.2)
    left.set_ylim(-0.1, 0.1)
    left.set_aspect("equal")
    left.set_xlabel("x (m)")
    left.set_yticks([])
    left.axvline(-0.18, color="0.3", lw=3.0)
    left.axvline(0.0, color="0.85", lw=0.8, ls="--")
    (spring_line,) = left.plot([], [], color="0.4", lw=1.2)
    (mass_dot,) = left.plot([], [], marker="s", markersize=16, color=BLUE)

    middle.set_xlim(0.0, duration)
    span = 1.1 * max(np.max(np.abs(x)), np.max(np.abs(v)) / OMEGA0)
    middle.set_ylim(-span, span)
    middle.set_xlabel("t (s)")
    (x_trace,) = middle.plot([], [], lw=1.6, color=BLUE, label="x")
    (v_trace,) = middle.plot([], [], lw=1.2, color=ORANGE, label="v/$\\omega_0$")
    middle.legend(loc="upper right", fontsize=8, frameon=False)

    right.set_xlim(-0.6, 2.6)
    right.set_ylim(0.0, 1.25 * total[0])
    right.set_xticks([0, 1, 2])
    right.set_xticklabels(["K", "U", "E"])
    right.set_yticks([])
    bars = right.bar([0, 1, 2], [0.0, 0.0, total[0]], color=[ORANGE, BLUE, GREEN], width=0.6)
    right.axhline(total[0], color="0.6", lw=0.8, ls="--")
    fig.tight_layout()

    def update(frame: int):
        spring = _spring_points(x[frame] - 0.02)
        spring_line.set_data(spring[:, 0], spring[:, 1])
        mass_dot.set_data([x[frame]], [0.0])
        upto = slice(0, frame + 1)
        x_trace.set_data(times[upto], x[upto])
        v_trace.set_data(times[upto], v[upto] / OMEGA0)
        bars[0].set_height(kinetic[frame])
        bars[1].set_height(potential[frame])
        bars[2].set_height(total[frame])
        return spring_line, mass_dot, x_trace, v_trace, *bars

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "sho-portrait")


def render_phase_space(n_frames: int = 300) -> None:
    """Two release amplitudes traced simultaneously in phase space.

    The orbits are similar ellipses; the two moving points stay exactly in step — the
    visual form of amplitude-independent period.
    """
    amplitudes = (0.06, 0.12)
    duration = n_frames / FPS
    times = np.linspace(0.0, duration, n_frames)

    trajectories = []
    for amplitude in amplitudes:
        x = oscillators.position(times, MASS, STIFFNESS, amplitude, 0.0)
        v = oscillators.velocity(times, MASS, STIFFNESS, amplitude, 0.0)
        trajectories.append((x, v))

    fig, (left, right) = plt.subplots(
        1, 2, figsize=(8.5, 3.6), dpi=DPI, gridspec_kw={"width_ratios": [1.5, 1.0]}
    )

    left.set_xlim(0.0, duration)
    left.set_ylim(-0.14, 0.14)
    left.set_xlabel("t (s)")
    left.set_ylabel("x (m)")
    time_traces = [
        left.plot([], [], lw=1.4, color=color)[0] for color in (BLUE, ORANGE)
    ]

    right.set_xlim(-0.14, 0.14)
    right.set_ylim(-0.6, 0.6)
    right.set_xlabel("x (m)")
    right.set_ylabel("v (m/s)")
    right.axhline(0.0, color="0.85", lw=0.8, zorder=0)
    right.axvline(0.0, color="0.85", lw=0.8, zorder=0)
    for (x, v), color in zip(trajectories, (BLUE, ORANGE), strict=True):
        right.plot(x, v, color=color, lw=0.8, alpha=0.35)
    dots = [
        right.plot([], [], marker="o", markersize=7, color=color)[0]
        for color in (BLUE, ORANGE)
    ]
    fig.tight_layout()

    def update(frame: int):
        upto = slice(0, frame + 1)
        artists = []
        for (x, v), trace, dot in zip(trajectories, time_traces, dots, strict=True):
            trace.set_data(times[upto], x[upto])
            dot.set_data([x[frame]], [v[frame]])
            artists.extend([trace, dot])
        return tuple(artists)

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "sho-phase-space")


if __name__ == "__main__":
    render_portrait()
    render_phase_space()
