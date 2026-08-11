"""Render the demonstration animations for module 04 (the microscopic origin of pressure).

Animations are produced from `thermolab` itself, so what a student watches is the same model
they can read, run and test — never a hand-drawn impression of it.

Output is MP4, written by `_common.save`; see that module for why, and for the constraints the
format brings. The animations carry no words, so the same file serves both language sites; the
caption that explains each one is ordinary translated page prose rather than a subtitle track
that could silently drift from the text around it.

Run:  uv run python media/render/render_pressure.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, save  # noqa: E402
from thermolab import kinetics  # noqa: E402

ARGON_MASS = 39.948 * 1.66053906660e-27
BOX = (1e-6, 1e-6)
AREA = float(np.prod(BOX))


def render_impacts_to_pressure(n_particles: int = 60, n_frames: int = 300) -> None:
    """Particles bouncing beside the running average of the pressure they produce.

    The point of the pairing: the left panel never settles down, and the right panel does.
    """
    rng = np.random.default_rng(12)
    state = kinetics.initialise_gas(n_particles, BOX, 300.0, ARGON_MASS, rng)
    dt = kinetics.max_stable_dt(state)
    steps_per_frame = 12

    positions = [state.positions.copy()]
    impulses: list[float] = []
    current = state
    for _ in range(n_frames):
        run = kinetics.simulate(current, dt=dt, n_steps=steps_per_frame)
        current = run.final_state
        positions.append(current.positions.copy())
        impulses.append(float(run.impulses.sum()))

    frame_time = dt * steps_per_frame
    times = np.arange(1, n_frames + 1) * frame_time
    running = np.cumsum(impulses) / (times * state.wall_measure)
    predicted = kinetics.ideal_gas_pressure(n_particles, 300.0, AREA)

    fig, (left, right) = plt.subplots(1, 2, figsize=(8.5, 3.6), dpi=DPI)
    micron = 1e6

    dots = left.scatter([], [], s=14, color="#2563eb")
    left.set_xlim(0, BOX[0] * micron)
    left.set_ylim(0, BOX[1] * micron)
    left.set_xlabel("x (μm)")
    left.set_ylabel("y (μm)")
    left.set_title(f"{n_particles} particles, 300 K")

    (trace,) = right.plot([], [], lw=1.4, color="#2563eb")
    right.axhline(predicted, color="crimson", ls="--", lw=1.2)
    right.set_xlim(0, times[-1] * 1e9)
    right.set_ylim(0, 2.2 * predicted)
    right.set_xlabel("time (ns)")
    right.set_ylabel("pressure (N/m)")
    right.set_title("running average vs $N k_B T / V$")
    fig.tight_layout()

    def update(frame: int):
        dots.set_offsets(positions[frame] * micron)
        trace.set_data(times[:frame] * 1e9, running[:frame])
        return dots, trace

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "pressure-impacts")
    plt.close(fig)


def render_fluctuations_shrink(n_frames: int = 180) -> None:
    """The same measurement at three particle numbers, on a shared fractional scale.

    Plotting P/P_predicted rather than P is what makes the comparison honest: the three runs
    have wildly different pressures, and only the *relative* spread is being compared.
    """
    rng = np.random.default_rng(5)
    sizes = (20, 200, 2000)
    steps_per_frame = 12

    traces = []
    for n_particles in sizes:
        state = kinetics.initialise_gas(n_particles, BOX, 300.0, ARGON_MASS, rng)
        dt = kinetics.max_stable_dt(state)
        impulses: list[float] = []
        current = state
        for _ in range(n_frames):
            run = kinetics.simulate(current, dt=dt, n_steps=steps_per_frame)
            current = run.final_state
            impulses.append(float(run.impulses.sum()))
        times = np.arange(1, n_frames + 1) * dt * steps_per_frame
        running = np.cumsum(impulses) / (times * state.wall_measure)
        traces.append(
            (times * 1e9, running / kinetics.ideal_gas_pressure(n_particles, 300.0, AREA))
        )

    fig, axes = plt.subplots(1, 3, figsize=(9.5, 3.0), dpi=DPI, sharey=True)
    lines = []
    for ax, n_particles, (t, _) in zip(axes, sizes, traces, strict=True):
        (line,) = ax.plot([], [], lw=1.2, color="#2563eb")
        ax.axhline(1.0, color="crimson", ls="--", lw=1.0)
        ax.set_xlim(0, t[-1])
        ax.set_ylim(0.4, 1.6)
        ax.set_title(f"N = {n_particles}")
        ax.set_xlabel("time (ns)")
        lines.append(line)
    axes[0].set_ylabel("measured / predicted")
    fig.tight_layout()

    def update(frame: int):
        for line, (t, y) in zip(lines, traces, strict=True):
            line.set_data(t[:frame], y[:frame])
        return lines

    save(
        FuncAnimation(fig, update, frames=n_frames, blit=False),
        fig,
        "pressure-fluctuations",
    )
    plt.close(fig)


def main() -> None:
    render_impacts_to_pressure()
    render_fluctuations_shrink()


if __name__ == "__main__":
    main()
