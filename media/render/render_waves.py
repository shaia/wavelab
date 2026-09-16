"""Render the demonstration animations for Part III (the wave equation, energy, impedance).

Animations are produced from `wavelab` itself, so what a student watches is the same model
they can read, run and test — never a hand-drawn impression of it. Every string shown here is
integrated by `waves.simulate_string`, whose convergence on d'Alembert's exact solution is
tested before anything is rendered (tests/physics/test_convergence.py).

Output is MP4, written by `_common.save`; see that module for why, and for the constraints the
format brings. The animations carry no words, so the same file serves both language sites; the
caption that explains each one is ordinary translated page prose.

Displacements are drawn in millimetres on strings metres long, so every pulse on screen is
hundreds of times steeper than the string it depicts. The model's small-slope assumption holds
for the string; the picture is exaggerated vertically, and the axis units say by how much.

Run:  uv run python media/render/render_waves.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, save  # noqa: E402
from wavelab import waves  # noqa: E402

BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#059669"
GREY = "0.55"

TENSION = 4.0  # N
MU = 0.01  # kg/m
SPEED = waves.wave_speed(TENSION, MU)  # 20 m/s
MM = 1e3  # metres to millimetres, for display only


# ---------------------------------------------------------------------------
# Module 08: the wave equation
# ---------------------------------------------------------------------------

LENGTH = 4.0
CELLS = 1600
DX = LENGTH / CELLS
X = np.arange(CELLS + 1) * DX


def _draw_string_axes(axis, span_mm: float) -> None:
    """Limits, walls and rest line for a panel showing the whole string."""
    axis.set_xlim(-0.04 * LENGTH, 1.04 * LENGTH)
    axis.set_ylim(-span_mm, span_mm)
    axis.set_xlabel("x (m)")
    axis.set_ylabel("y (mm)")
    axis.axhline(0.0, color="0.9", lw=0.8)
    for wall in (0.0, LENGTH):
        axis.plot([wall], [0.0], marker="|", markersize=18, color="0.3", mew=3)


def render_pulse_speck(n_frames: int = 300, save_every: int = 7) -> None:
    """A pulse runs the length of the string; a marked speck goes up, comes down, stays put.

    The falsifier for `wave-carries-medium`. The speck is one grid point, drawn in orange with
    a faint trail of everywhere it has been, and the trail is a vertical line: the speck rises
    as the front of the pulse arrives, falls as the back leaves, and is exactly where it
    started once the pulse has gone on. The lower panel records its height against time, which
    begins and ends at zero. Whatever crossed the string, none of the string went with it.

    Honesty about the model belongs in the caption rather than the picture: the ideal string
    moves only transversely by assumption, so the vertical trail is built in. What is not built
    in is that the speck *returns* — a displacement that stayed behind would need energy the
    pulse carried away.
    """
    width = 0.15
    start = 0.7

    def pulse(s: np.ndarray) -> np.ndarray:
        return 0.01 * np.exp(-(((s - start) / width) ** 2))

    def slope(s: np.ndarray) -> np.ndarray:
        return -2.0 * (s - start) / width**2 * pulse(s)

    dt = 0.5 * DX / SPEED
    # A right-mover starts with y_t = -v y_x; the pulse then runs 2.6 m without dispersing
    # visibly, sixty grid points to a width.
    run = waves.simulate_string(
        pulse(X), -SPEED * slope(X), DX, dt, TENSION, MU, (n_frames - 1) * save_every,
        save_every=save_every,
    )
    speck = int(round(2.0 / DX))
    height = run.y[:, speck] * MM

    fig, (string_axis, trace_axis) = plt.subplots(
        2, 1, figsize=(9.0, 4.6), dpi=DPI, gridspec_kw={"height_ratios": [1.5, 1.0]}
    )
    _draw_string_axes(string_axis, 14.0)
    string_axis.set_ylim(-3.0, 13.0)
    string_axis.axvline(X[speck], color="0.88", lw=0.8, ls="--")
    (line,) = string_axis.plot([], [], color=BLUE, lw=1.6)
    (trail,) = string_axis.plot([], [], color=ORANGE, lw=3.0, alpha=0.35, solid_capstyle="round")
    (dot,) = string_axis.plot([], [], marker="o", markersize=8, color=ORANGE)

    trace_axis.set_xlim(0.0, run.times[-1])
    trace_axis.set_ylim(-2.0, 12.0)
    trace_axis.set_xlabel("t (s)")
    trace_axis.set_ylabel("speck y (mm)")
    trace_axis.axhline(0.0, color="0.85", lw=0.8)
    (trace,) = trace_axis.plot([], [], color=ORANGE, lw=1.6)
    fig.tight_layout()

    def update(frame: int):
        line.set_data(X, run.y[frame] * MM)
        seen = height[: frame + 1]
        trail.set_data([X[speck], X[speck]], [min(0.0, seen.min()), max(0.0, seen.max())])
        dot.set_data([X[speck]], [height[frame]])
        trace.set_data(run.times[: frame + 1], seen)
        return line, trail, dot, trace

    print(f"[render] pulse and speck: speck peaks at {height.max():.2f} mm and ends at "
          f"{height[-1]:.1e} mm; string clear of the walls to "
          f"{max(abs(run.y[:, 1]).max(), abs(run.y[:, -2]).max()) * MM:.1e} mm")
    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "wave-pulse-speck")


def render_pluck_split(hold: int = 30, save_every: int = 2, n_steps: int = 560) -> None:
    """A triangle released from rest becomes two triangles of half the height, running apart.

    Underneath the string, translucent fills draw d'Alembert's two halves, y0(x - vt)/2 in blue
    and y0(x + vt)/2 in orange. At the first frame they lie on top of each other and the string
    is their sum, twice the height of either; as they slide apart the string follows the sum,
    and each separated pulse keeps the colour of the direction it is travelling. That is the
    argument for why the pluck *must* split, shown rather than stated: a string released from
    rest has no velocity to prefer either direction, so each gets half.

    Fills rather than lines, because a line drawing either half lies exactly under the string
    wherever the halves no longer overlap, and all that stays visible is its flat stretch at
    zero — under the *other* pulse.

    The run is at the magic step S = 1, where a pluck is transported exactly (the convergence
    tests pin it to 1e-14), so the triangle's corners stay sharp. At any S < 1 they would shed
    a small wake of grid-dispersion ripples, which is a fact about the computer the shot has no
    reason to show.
    """
    centre, half_width, peak = 2.0, 0.4, 0.01

    def triangle(s: np.ndarray) -> np.ndarray:
        return peak * np.clip(1.0 - np.abs(s - centre) / half_width, 0.0, None)

    dt = waves.cfl_max_dt(DX, SPEED)
    run = waves.simulate_string(
        triangle(X), np.zeros_like(X), DX, dt, TENSION, MU, n_steps, save_every=save_every
    )
    exact = waves.dalembert_solution(triangle, SPEED, X, run.times)
    frames = [0] * hold + list(range(run.times.size))

    fig, axis = plt.subplots(figsize=(9.0, 3.0), dpi=DPI)
    _draw_string_axes(axis, 12.5)
    axis.set_ylim(-2.0, 12.5)
    axis.plot(X, triangle(X) * MM, color="0.8", lw=1.0, ls=":")
    (line,) = axis.plot([], [], color="0.15", lw=1.8, zorder=3)
    halves = []
    fig.tight_layout()

    def update(frame: int):
        step = frames[frame]
        t = run.times[step]
        for fill in halves:
            fill.remove()
        halves[:] = [
            axis.fill_between(X, 0.5 * triangle(X - sign * SPEED * t) * MM, color=colour,
                              alpha=0.3, lw=0.0, zorder=2)
            for sign, colour in ((1.0, BLUE), (-1.0, ORANGE))
        ]
        line.set_data(X, run.y[step] * MM)
        return line, *halves

    error = np.max(np.abs(run.y - exact)) / peak
    print(f"[render] pluck split over {run.times[-1] * SPEED:.2f} m of travel; "
          f"solver vs d'Alembert {error:.1e} of the height")
    save(FuncAnimation(fig, update, frames=len(frames), blit=False), fig, "wave-pluck-split")


def _top_mode_amplitude(y: np.ndarray) -> np.ndarray:
    """Amplitude of the shortest wave a fixed-end grid holds, per saved step.

    That mode is y_i = (-1)^(i+1) sin(pi i / N) — neighbouring points in antiphase under a
    half-sine envelope — and it is the one the instability amplifies fastest. Projecting onto
    it separates the instability from the pulse, whose own content up there is e^(-986) of
    its height: invisible in the string, it is plain on a logarithmic axis.
    """
    cells = y.shape[-1] - 1
    i = np.arange(cells + 1)
    mode = (-1.0) ** (i + 1) * np.sin(np.pi * i / cells)
    return np.abs(y @ mode) * 2.0 / cells


def render_cfl_blowup(n_steps: int = 150, frames_per_step: int = 2) -> None:
    """The same pluck at S = 0.99 and S = 1.01: one splits and travels, the other is destroyed.

    For a hundred steps the two runs look identical, which is the unsettling part. The damage
    is growing the whole time, from rounding error, in the shortest wave the grid can hold —
    the bottom panel tracks it on a logarithmic axis, where the S = 1.01 run climbs a straight
    line of slope log10(1.327) per step, von Neumann's growth factor, while the S = 0.99 run
    sits on the rounding floor. At step 137 the sawtooth reaches the pulse's own size and the
    string panel is overwhelmed within a dozen steps.

    Nothing physical happened: the string is stable at every S. What failed is a scheme asked
    to move information further than one grid spacing per step.
    """
    cells = 400
    dx = 1.0 / cells
    x = np.arange(cells + 1) * dx
    amplitude = 0.01
    pluck = amplitude * np.exp(-(((x - 0.5) / 0.05) ** 2))

    runs = {
        courant: waves.simulate_string(
            pluck, np.zeros_like(x), dx, courant * dx / SPEED, TENSION, MU, n_steps,
            allow_unstable=True,
        )
        for courant in (0.99, 1.01)
    }
    growth = {courant: _top_mode_amplitude(run.y) / amplitude for courant, run in runs.items()}
    # Drawn as the largest value reached so far. At the rounding floor the projection lands
    # exactly on zero every few steps, and a log axis turns each of those into a spike down to
    # its bottom edge; the running maximum is the same statement — "it never got bigger than
    # this" — without the comb.
    reached = {courant: np.maximum.accumulate(values) for courant, values in growth.items()}

    fig, axes = plt.subplots(
        3, 1, figsize=(8.4, 6.0), dpi=DPI, gridspec_kw={"height_ratios": [1.0, 1.0, 1.1]}
    )
    lines = {}
    for axis, courant, colour in ((axes[0], 0.99, BLUE), (axes[1], 1.01, ORANGE)):
        axis.set_xlim(0.0, 1.0)
        axis.set_ylim(-12.0, 12.0)
        axis.set_ylabel("y (mm)")
        axis.axhline(0.0, color="0.9", lw=0.8)
        axis.text(0.99, 0.82, f"S = {courant}", transform=axis.transAxes, ha="right",
                  fontsize=10, color=colour)
        (lines[courant],) = axis.plot([], [], color=colour, lw=1.3)
    axes[0].set_xticklabels([])
    axes[1].set_xlabel("x (m)")

    log_axis = axes[2]
    log_axis.set_xlim(0, n_steps)
    log_axis.set_yscale("log")
    log_axis.set_ylim(1e-18, 1e2)
    log_axis.set_yticks([1e-15, 1e-10, 1e-5, 1.0])
    log_axis.set_xlabel("step")
    log_axis.set_ylabel("sawtooth / pulse")
    log_axis.axhline(1.0, color="0.85", lw=0.8, ls="--")
    traces = {
        courant: log_axis.plot([], [], color=colour, lw=1.5)[0]
        for courant, colour in ((0.99, BLUE), (1.01, ORANGE))
    }
    fig.tight_layout()

    steps = np.arange(n_steps + 1)
    frames = np.repeat(steps, frames_per_step)

    def update(frame: int):
        step = frames[frame]
        for courant, run in runs.items():
            lines[courant].set_data(x, run.y[step] * MM)
            traces[courant].set_data(steps[: step + 1], reached[courant][: step + 1])
        return (*lines.values(), *traces.values())

    rising = (growth[1.01] > 1e-12) & (growth[1.01] < 1e-2)
    slope = np.exp(np.polyfit(steps[rising], np.log(growth[1.01][rising]), 1)[0])
    b = 2.0 * 1.01**2 - 1.0
    print(f"[render] CFL: sawtooth grows by {slope:.4f} per step at S = 1.01 "
          f"(von Neumann {b + np.sqrt(b * b - 1.0):.4f}); reaches the pulse at step "
          f"{int(np.argmax(growth[1.01] > 1.0))}; S = 0.99 stays below "
          f"{growth[0.99].max():.1e}")
    save(FuncAnimation(fig, update, frames=frames.size, blit=False), fig, "wave-cfl-blowup")


if __name__ == "__main__":
    render_pulse_speck()
    render_pluck_split()
    render_cfl_blowup()
