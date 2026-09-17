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


# ---------------------------------------------------------------------------
# Module 09: wave energy
# ---------------------------------------------------------------------------

# A 40 Hz, half-metre wave, used by every shot below so the three can be read against each
# other. The train shots run on a long string with a windowed wave far from both ends; the
# standing shot needs a string whose length is a whole number of half wavelengths.
ENERGY_WAVELENGTH = 0.5
ENERGY_K = 2.0 * np.pi / ENERGY_WAVELENGTH
ENERGY_OMEGA = SPEED * ENERGY_K
ENERGY_PERIOD = 2.0 * np.pi / ENERGY_OMEGA
ENERGY_AMPLITUDE = 0.002
MJ = 1e3  # joules per metre to millijoules per metre, and watts to milliwatts


def _windowed_train(x: np.ndarray, flat: tuple[float, float]) -> np.ndarray:
    """A sine with raised-cosine shoulders, flat between `flat`, zero outside it.

    A travelling sine cannot live on a string with fixed ends — it would have to move them — so
    every train here is windowed and kept clear of both walls. Inside the flat stretch it is an
    unmodulated sine, which is what the shots look at.
    """
    low, high = flat
    shoulder = 4.0 * ENERGY_WAVELENGTH
    ramp = np.clip((x - (low - shoulder)) / shoulder, 0.0, 1.0) * np.clip(
        ((high + shoulder) - x) / shoulder, 0.0, 1.0
    )
    return ENERGY_AMPLITUDE * np.sin(ENERGY_K * x) * 0.5 * (1.0 - np.cos(np.pi * ramp))


def _frame_step(dx: float, periods: float, frames: int) -> tuple[float, int]:
    """A stable time step that lands a saved sample on every frame, and how many steps that is.

    The animation wants `frames` samples spanning `periods` cycles, which on these grids is a
    much longer interval than the Courant limit allows in one step. So the step is that interval
    divided by the smallest `save_every` that brings it under `cfl_max_dt`, and the solver is
    asked to keep every `save_every`-th step: the frames then sit exactly one cycle apart at the
    end of the loop, which is what makes it repeat seamlessly.
    """
    interval = periods * ENERGY_PERIOD / frames
    save_every = int(np.ceil(interval / waves.cfl_max_dt(dx, SPEED)))
    return interval / save_every, save_every


def _run_train(length: float, cells: int, flat: tuple[float, float], periods: float,
               frames: int) -> tuple[waves.StringEvolution, float]:
    """Launch a right-moving train and keep exactly `frames` samples spanning `periods` cycles."""
    dx = length / cells
    x = np.arange(cells + 1) * dx
    y0 = _windowed_train(x, flat)
    dt, save_every = _frame_step(dx, periods, frames)
    run = waves.simulate_string(
        y0, -SPEED * np.gradient(y0, dx), dx, dt, TENSION, MU, frames * save_every,
        save_every=save_every,
    )
    return run, dx


def render_energy_paint(periods: float = 2.0, frames: int = 96) -> None:
    """A travelling sine over its own energy density: the crests are the empty places.

    The falsifier for `energy-peaks-at-crests`. The upper panel is the string, with a marker
    riding a crest and another riding the zero crossing a quarter wavelength behind it; the
    lower panel is the energy density at the same instant, filled. The crest marker sits in the
    trough of the energy and the zero-crossing marker sits on its peak, and both stay there for
    the whole animation, because the pattern and its energy travel together at v.

    Energy is stored by the slope and by the transverse speed, and a crest has neither: the
    string there is momentarily flat and momentarily at rest, the two halves of u_K and u_P
    vanishing at once. Measured on the grid, the density at the crests is 1.5e-4 of the density
    at the zero crossings.

    The loop is a whole number of periods, so it repeats seamlessly, and the window is a metre
    of string far inside the train's flat stretch — what is drawn is an unmodulated sine.
    """
    length, cells = 12.0, 4800
    run, dx = _run_train(length, cells, (1.0, 9.0), periods, frames)
    x = run.x
    view = (x >= 4.0) & (x <= 5.0)

    slope = np.gradient(run.y, dx, axis=1)
    density = waves.kinetic_density(run.dydt, MU) + waves.potential_density(slope, TENSION)
    # The crest that sits at 4.25 m in the first frame, and the zero crossing a quarter
    # wavelength behind it; both are carried along at v by construction, not by searching.
    crest0 = 4.0 + 0.25 * ENERGY_WAVELENGTH
    zero0 = crest0 - 0.25 * ENERGY_WAVELENGTH

    fig, (string_axis, energy_axis) = plt.subplots(
        2, 1, figsize=(8.4, 4.4), dpi=DPI, sharex=True,
        gridspec_kw={"height_ratios": [1.0, 1.0]},
    )
    string_axis.set_xlim(4.0, 5.0)
    string_axis.set_ylim(-3.0, 3.0)
    string_axis.set_ylabel("y (mm)")
    string_axis.axhline(0.0, color="0.9", lw=0.8)
    (wave_line,) = string_axis.plot([], [], color="0.15", lw=1.6)
    (crest_dot,) = string_axis.plot([], [], marker="o", ms=9, color=ORANGE, zorder=4)
    (zero_dot,) = string_axis.plot([], [], marker="o", ms=9, color=GREEN, zorder=4)

    energy_axis.set_xlim(4.0, 5.0)
    energy_axis.set_ylim(0.0, 1.15 * float(density[:, view].max()) * MJ)
    energy_axis.set_xlabel("x (m)")
    energy_axis.set_ylabel("u (mJ/m)")
    (energy_line,) = energy_axis.plot([], [], color=BLUE, lw=1.4)
    fills: list = []
    guides = [
        energy_axis.axvline(crest0, color=ORANGE, lw=1.2, ls="--"),
        energy_axis.axvline(zero0, color=GREEN, lw=1.2, ls="--"),
    ]
    fig.tight_layout()

    def update(frame: int):
        travelled = SPEED * run.times[frame]
        crest = 4.0 + (crest0 - 4.0 + travelled) % ENERGY_WAVELENGTH
        zero = 4.0 + (zero0 - 4.0 + travelled) % ENERGY_WAVELENGTH
        wave_line.set_data(x[view], run.y[frame, view] * MM)
        crest_dot.set_data([crest], [np.interp(crest, x, run.y[frame]) * MM])
        zero_dot.set_data([zero], [np.interp(zero, x, run.y[frame]) * MM])
        energy_line.set_data(x[view], density[frame, view] * MJ)
        for fill in fills:
            fill.remove()
        fills[:] = [
            energy_axis.fill_between(
                x[view], density[frame, view] * MJ, color=BLUE, alpha=0.22, lw=0.0
            )
        ]
        guides[0].set_xdata([crest, crest])
        guides[1].set_xdata([zero, zero])
        return wave_line, crest_dot, zero_dot, energy_line, *fills, *guides

    # The two markers, followed frame by frame: the energy they stand on, relative to the
    # largest energy anywhere in the window at that instant.
    crests = 4.0 + (crest0 - 4.0 + SPEED * run.times) % ENERGY_WAVELENGTH
    zeros = 4.0 + (zero0 - 4.0 + SPEED * run.times) % ENERGY_WAVELENGTH
    at_crest = np.array([np.interp(c, x, row) for c, row in zip(crests, density, strict=True)])
    at_zero = np.array([np.interp(z, x, row) for z, row in zip(zeros, density, strict=True)])
    print(f"[render] energy paint: over every frame, u at the crest is at most "
          f"{(at_crest / at_zero).max():.1e} of u at the zero crossing a quarter wavelength "
          f"behind it; peak u {density[:, view].max() * MJ:.3f} mJ/m")
    save(FuncAnimation(fig, update, frames=frames, blit=False), fig, "wave-energy-paint")


def render_energy_densities(n_frames: int = 250, save_every: int = 12) -> None:
    """One hump of string, two humps of energy — and the two densities lying on top of each other.

    A Gaussian pulse travels; beneath it, u_P is drawn thick and pale and u_K thin and dark on
    top of it. They coincide everywhere, at every frame, to 1.1e-4 of the peak: a travelling
    wave carries equal kinetic and potential energy at every single point, not merely on
    average. The oscillator of module 01 does this only in a time average, trading one for the
    other twice a cycle; the wave has every element a little behind its neighbour, so the trade
    happens across the string instead of across the cycle.

    The shape of the energy is the second lesson and the one that surprises. A single-humped
    pulse carries a double-humped energy, because both densities go as the square of the slope
    and the slope is zero at the top. The grey fill is the total density and the dotted curve on
    it is the flux divided by v, which lands on the fill to 2.2e-8 of the peak: the energy moves
    at exactly the speed the pattern does.
    """
    width, start = 0.12, 0.45
    length, cells = 4.0, 2000
    dx = length / cells
    x = np.arange(cells + 1) * dx

    def pulse(s: np.ndarray) -> np.ndarray:
        return 0.008 * np.exp(-(((s - start) / width) ** 2))

    slope0 = -2.0 * (x - start) / width**2 * pulse(x)
    dt = 0.5 * dx / SPEED
    run = waves.simulate_string(
        pulse(x), -SPEED * slope0, dx, dt, TENSION, MU, (n_frames - 1) * save_every,
        save_every=save_every,
    )
    slope = np.gradient(run.y, dx, axis=1)
    kinetic = waves.kinetic_density(run.dydt, MU)
    potential = waves.potential_density(slope, TENSION)
    flux = waves.energy_flux(slope, run.dydt, TENSION)

    fig, (string_axis, energy_axis) = plt.subplots(
        2, 1, figsize=(9.0, 4.8), dpi=DPI, sharex=True,
        gridspec_kw={"height_ratios": [1.0, 1.2]},
    )
    string_axis.set_xlim(0.0, length)
    string_axis.set_ylim(-1.5, 9.5)
    string_axis.set_ylabel("y (mm)")
    string_axis.axhline(0.0, color="0.9", lw=0.8)
    (wave_line,) = string_axis.plot([], [], color="0.15", lw=1.6)

    energy_axis.set_xlim(0.0, length)
    energy_axis.set_ylim(0.0, 1.15 * float((kinetic + potential).max()) * MJ)
    energy_axis.set_xlabel("x (m)")
    energy_axis.set_ylabel("u (mJ/m)")
    (potential_line,) = energy_axis.plot([], [], color=ORANGE, lw=5.0, alpha=0.5)
    (kinetic_line,) = energy_axis.plot([], [], color=BLUE, lw=1.5)
    (transport_line,) = energy_axis.plot([], [], color=GREEN, lw=1.6, ls=":")
    totals: list = []
    fig.tight_layout()

    def update(frame: int):
        wave_line.set_data(x, run.y[frame] * MM)
        potential_line.set_data(x, potential[frame] * MJ)
        kinetic_line.set_data(x, kinetic[frame] * MJ)
        transport_line.set_data(x, flux[frame] / SPEED * MJ)
        for patch in totals:
            patch.remove()
        totals[:] = [
            energy_axis.fill_between(
                x, (kinetic[frame] + potential[frame]) * MJ, color="0.55", alpha=0.25, lw=0.0
            )
        ]
        return wave_line, potential_line, kinetic_line, transport_line, *totals

    peak = float((kinetic + potential).max())
    gap = float(np.max(np.abs(kinetic - potential))) / peak
    print(f"[render] energy densities: u_K and u_P agree to {gap:.1e} of the peak; "
          f"P/v vs u_K + u_P to "
          f"{float(np.max(np.abs(flux / SPEED - kinetic - potential))) / peak:.1e}")
    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "wave-energy-densities")


def render_energy_transport(periods: float = 3.0, frames: int = 150) -> None:
    """Two waves of the same amplitude and frequency: one delivers energy, one only lends it.

    The upper string is a right-moving train, the lower a standing mode of a fixed string, and
    each carries a gate — a point where the flux is read. The bottom panel plots what the two
    gates see. The travelling wave's flux never goes below zero: energy crosses that point and
    keeps going, twice per cycle in pulses, always forwards. The standing wave's flux swings
    symmetrically about zero, spending exactly as long carrying energy one way as the other,
    and over any whole cycle delivering nothing at all.

    Both fluxes oscillate at twice the wave's frequency, and the standing wave's peak is a
    quarter of the travelling wave's at the same amplitude, so the two sit on one axis without
    any scaling. That is the shot's argument: nothing is small here, and nothing is averaged
    away by drawing. The standing wave moves as much energy about as the travelling one — it
    just puts it all back.
    """
    train, train_dx = _run_train(12.0, 4800, (1.0, 9.0), periods, frames)
    train_gate = int(round(5.0 / train_dx))
    train_slope = np.gradient(train.y, train_dx, axis=1)[:, train_gate]
    train_flux = waves.energy_flux(train_slope, train.dydt[:, train_gate], TENSION)

    # A whole number of half wavelengths between the walls, so the mode fits exactly. The gate
    # sits an eighth of a wavelength from a node, where the standing wave's flux
    # T A^2 k omega sin(2kx) sin(2 omega t) / 4 is largest — a quarter of the travelling
    # wave's peak at the same amplitude, which is the honest ratio and not a drawing choice.
    modes, standing_length = 4, 2.0 * ENERGY_WAVELENGTH
    standing_cells = 800
    standing_dx = standing_length / standing_cells
    sx = np.arange(standing_cells + 1) * standing_dx
    standing_dt, standing_save = _frame_step(standing_dx, periods, frames)
    standing = waves.simulate_string(
        ENERGY_AMPLITUDE * np.sin(modes * np.pi * sx / standing_length), np.zeros_like(sx),
        standing_dx, standing_dt, TENSION, MU, frames * standing_save,
        save_every=standing_save,
    )
    standing_gate = int(round((0.625 * ENERGY_WAVELENGTH) / standing_dx))
    standing_slope = np.gradient(standing.y, standing_dx, axis=1)[:, standing_gate]
    standing_flux = waves.energy_flux(standing_slope, standing.dydt[:, standing_gate], TENSION)

    fig, axes = plt.subplots(
        3, 1, figsize=(8.4, 6.2), dpi=DPI, gridspec_kw={"height_ratios": [1.0, 1.0, 1.3]}
    )
    view = (train.x >= 4.5) & (train.x <= 5.5)
    for axis in axes[:2]:
        axis.set_ylim(-3.0, 3.0)
        axis.set_ylabel("y (mm)")
        axis.axhline(0.0, color="0.9", lw=0.8)
        axis.tick_params(labelsize=8)
    # The upper panel is a metre-wide window on a twelve-metre string; the lower is a whole
    # string between two walls, drawn with the wall marks the module 08 shots use, so the two
    # x axes are not mistaken for the same stretch of anything.
    axes[0].set_xlim(4.5, 5.5)
    axes[1].set_xlim(-0.02 * standing_length, 1.02 * standing_length)
    for wall in (0.0, standing_length):
        axes[1].plot([wall], [0.0], marker="|", markersize=16, color="0.3", mew=3)
    (train_line,) = axes[0].plot([], [], color=BLUE, lw=1.6)
    (standing_line,) = axes[1].plot([], [], color=ORANGE, lw=1.6)
    axes[0].axvline(train.x[train_gate], color="0.7", lw=1.0, ls="--")
    axes[1].axvline(sx[standing_gate], color="0.7", lw=1.0, ls="--")
    (train_dot,) = axes[0].plot([], [], marker="o", ms=7, color=BLUE, zorder=4)
    (standing_dot,) = axes[1].plot([], [], marker="o", ms=7, color=ORANGE, zorder=4)

    flux_axis = axes[2]
    limit = 1.15 * max(np.abs(train_flux).max(), np.abs(standing_flux).max()) * MJ
    flux_axis.set_xlim(0.0, train.times[-1] * 1e3)
    flux_axis.set_ylim(-limit, limit)
    flux_axis.set_xlabel("t (ms)")
    flux_axis.set_ylabel("P at the gate (mW)")
    flux_axis.axhline(0.0, color="0.4", lw=1.0)
    (train_trace,) = flux_axis.plot([], [], color=BLUE, lw=1.6)
    (standing_trace,) = flux_axis.plot([], [], color=ORANGE, lw=1.6)
    traces: list = []
    fig.tight_layout()

    def update(frame: int):
        train_line.set_data(train.x[view], train.y[frame, view] * MM)
        standing_line.set_data(sx, standing.y[frame] * MM)
        train_dot.set_data([train.x[train_gate]], [train.y[frame, train_gate] * MM])
        standing_dot.set_data([sx[standing_gate]], [standing.y[frame, standing_gate] * MM])
        ms = train.times[: frame + 1] * 1e3
        train_trace.set_data(ms, train_flux[: frame + 1] * MJ)
        standing_trace.set_data(ms, standing_flux[: frame + 1] * MJ)
        for patch in traces:
            patch.remove()
        traces[:] = [
            flux_axis.fill_between(ms, values[: frame + 1] * MJ, color=colour, alpha=0.2, lw=0.0)
            for values, colour in ((train_flux, BLUE), (standing_flux, ORANGE))
        ]
        return train_line, standing_line, train_dot, standing_dot, train_trace, standing_trace

    net = np.trapezoid(standing_flux, standing.times) / np.trapezoid(
        np.abs(standing_flux), standing.times
    )
    print(f"[render] transport: travelling flux stays above "
          f"{train_flux.min() / train_flux.max():+.1e} of its peak; standing flux nets "
          f"{net:+.1e} of what it moved, peak ratio "
          f"{np.abs(standing_flux).max() / train_flux.max():.2f}")
    save(FuncAnimation(fig, update, frames=frames, blit=False), fig, "wave-energy-transport")


if __name__ == "__main__":
    render_pulse_speck()
    render_pluck_split()
    render_cfl_blowup()
    render_energy_paint()
    render_energy_densities()
    render_energy_transport()
