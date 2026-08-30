"""Render the demonstration animations for Part II (coupled oscillators and normal modes).

Animations are produced from `wavelab` itself, so what a student watches is the same model
they can read, run and test — never a hand-drawn impression of it.

Output is MP4, written by `_common.save`; see that module for why, and for the constraints the
format brings. The animations carry no words, so the same file serves both language sites; the
caption that explains each one is ordinary translated page prose rather than a subtitle track
that could silently drift from the text around it.

Run:  uv run python media/render/render_normal_modes.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, save  # noqa: E402
from wavelab import coupled  # noqa: E402

BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#059669"
GREY = "0.55"

MASS = 0.5
STIFFNESS = 8.0
COUPLING = 0.05 * STIFFNESS  # weak: the exchange is slow, clean, and complete
REST = 0.55  # half the distance between the two masses at rest


def _spring_points(
    x_left: float, x_right: float, n_coils: int = 9, height: float = 0.045
) -> np.ndarray:
    """A zigzag spring between two points, as an (N, 2) array of xy points.

    The same device as `render_sho.py`'s wall-to-mass spring, generalised to run between two
    moving ends — which is what a coupling spring is.
    """
    n_points = 2 * n_coils + 2
    xs = np.linspace(x_left, x_right, n_points)
    ys = np.zeros(n_points)
    ys[1:-1] = height * np.where(np.arange(1, n_points - 1) % 2 == 0, 1.0, -1.0)
    return np.column_stack([xs, ys])


def _draw_bench(axis: float) -> None:
    """Walls, rest markers and the axis furniture shared by every physical panel."""
    axis.set_xlim(-1.0, 1.0)
    axis.set_ylim(-0.22, 0.22)
    axis.set_yticks([])
    axis.set_xlabel("x (m)")
    axis.axvline(-0.95, color="0.3", lw=3.0)
    axis.axvline(0.95, color="0.3", lw=3.0)
    for rest in (-REST, REST):
        axis.axvline(rest, color="0.88", lw=0.8, ls="--")


def _pair(axis, colours=(BLUE, ORANGE)):
    """Create the artists for two masses, two anchor springs and one coupling spring."""
    (left_anchor,) = axis.plot([], [], color="0.45", lw=1.1)
    (right_anchor,) = axis.plot([], [], color="0.45", lw=1.1)
    (coupler,) = axis.plot([], [], color=GREEN, lw=1.6)
    (first,) = axis.plot([], [], marker="s", markersize=15, color=colours[0])
    (second,) = axis.plot([], [], marker="s", markersize=15, color=colours[1])
    return left_anchor, right_anchor, coupler, first, second


def _place(artists, x1: float, x2: float) -> tuple:
    """Position the pair's artists for displacements `x1`, `x2` about their rest points."""
    left_anchor, right_anchor, coupler, first, second = artists
    a = -REST + x1
    b = REST + x2
    left_anchor.set_data(*_spring_points(-0.95, a - 0.03).T)
    right_anchor.set_data(*_spring_points(b + 0.03, 0.95).T)
    coupler.set_data(*_spring_points(a + 0.03, b - 0.03).T)
    first.set_data([a], [0.0])
    second.set_data([b], [0.0])
    return artists


def _start_one(duration: float, n_frames: int, substeps: int = 60):
    """The start-one experiment: matrices, modes, and a trajectory sampled for animation.

    The integration step is `substeps` times finer than the frame interval, and every
    `substeps`-th sample is kept. Integrating at frame resolution would put roughly twenty
    steps in the fast period, and velocity Verlet's energy error goes as (omega dt)^2: the
    modal energies would visibly wobble by a percent or so in the site-versus-mode shot, which
    exists precisely to show them not moving.
    """
    matrices = coupled.two_mass_matrices(MASS, STIFFNESS, COUPLING)
    modes = coupled.normal_mode_solve(*matrices)
    dt = duration / ((n_frames - 1) * substeps)
    fine = coupled.simulate_coupled(
        *matrices, [0.28, 0.0], [0.0, 0.0], dt, (n_frames - 1) * substeps
    )
    run = coupled.CoupledTrajectory(
        times=fine.times[::substeps],
        positions=fine.positions[::substeps],
        velocities=fine.velocities[::substeps],
    )
    energies = coupled.site_energies(*matrices, run.positions, run.velocities)
    return matrices, modes, run, energies


def render_exchange(n_frames: int = 420) -> None:
    """One pendulum started alone, handing its swing to the other and taking it back.

    The energy bars are the point of the shot. They pulse in antiphase beneath a dashed line
    at the constant total, so a viewer can see that the first mass does not slow down because
    something is draining it — the total never moves — but because the energy is *somewhere
    else*. That is the falsifier for `energy-stays-in-excited-pendulum`, and it is much more
    convincing watched than read.

    Coupling is weak on purpose. At k_c/k = 0.05 the transfer is essentially complete, which
    is the claim the module makes; at strong coupling a visible remainder stays behind and the
    animation would quietly argue against its own caption.
    """
    modes = coupled.normal_mode_solve(*coupled.two_mass_matrices(MASS, STIFFNESS, COUPLING))
    duration = coupled.exchange_time(*modes.frequencies)
    _, _, run, energies = _start_one(duration, n_frames)
    total = energies.sum(axis=1)

    fig, (bench, traces, bars_axis) = plt.subplots(
        1, 3, figsize=(10.4, 3.4), dpi=DPI, gridspec_kw={"width_ratios": [1.2, 1.6, 0.6]}
    )

    _draw_bench(bench)
    bench.set_aspect("equal")
    pair = _pair(bench)

    traces.set_xlim(0.0, duration)
    span = 1.15 * np.max(np.abs(run.positions))
    traces.set_ylim(-span, span)
    traces.set_xlabel("t (s)")
    traces.set_ylabel("displacement (m)")
    traces.axhline(0.0, color="0.85", lw=0.8)
    (trace1,) = traces.plot([], [], lw=1.4, color=BLUE)
    (trace2,) = traces.plot([], [], lw=1.4, color=ORANGE)

    bars_axis.set_xlim(-0.6, 1.6)
    bars_axis.set_ylim(0.0, 1.25 * total[0])
    bars_axis.set_xticks([0, 1])
    bars_axis.set_xticklabels(["1", "2"])
    bars_axis.set_yticks([])
    bars_axis.set_ylabel("energy (J)")
    bars = bars_axis.bar([0, 1], [energies[0, 0], energies[0, 1]], color=[BLUE, ORANGE], width=0.6)
    bars_axis.axhline(total[0], color="0.6", lw=0.8, ls="--")
    fig.tight_layout()

    def update(frame: int):
        _place(pair, run.positions[frame, 0], run.positions[frame, 1])
        upto = slice(0, frame + 1)
        trace1.set_data(run.times[upto], run.positions[upto, 0])
        trace2.set_data(run.times[upto], run.positions[upto, 1])
        bars[0].set_height(energies[frame, 0])
        bars[1].set_height(energies[frame, 1])
        return (*pair, trace1, trace2, *bars)

    share = energies[:, 0] / total
    print(f"[render] exchange over {duration:.1f} s; "
          f"mass 1 falls to {share.min():.1e} of the total")
    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "coupled-exchange")


def render_modes(n_frames: int = 300) -> None:
    """The two motions that refuse to trade, side by side and going nowhere.

    Started on either mode shape, the pair oscillates at one frequency for ever and the energy
    stays where it was put. The symmetric mode never stretches the coupling spring — watch it
    hold its length — which is why its frequency is the uncoupled one whatever the coupling.
    """
    matrices = coupled.two_mass_matrices(MASS, STIFFNESS, COUPLING)
    modes = coupled.normal_mode_solve(*matrices)
    duration = 6.0 * 2.0 * np.pi / modes.frequencies[0]
    times = np.linspace(0.0, duration, n_frames)
    amplitude = 0.28

    fig, axes = plt.subplots(2, 1, figsize=(9.0, 4.2), dpi=DPI)
    pairs = []
    for axis in axes:
        _draw_bench(axis)
        axis.set_aspect("equal")
        pairs.append(_pair(axis))
    axes[0].set_xlabel("")
    fig.tight_layout()

    # Columns of `shapes` are the two patterns; normalise each to the same visible amplitude
    # so the shot compares their *shapes* and not the solver's normalisation.
    patterns = [modes.shapes[:, p] / np.max(np.abs(modes.shapes[:, p])) for p in (0, 1)]

    def update(frame: int):
        artists = []
        for pattern, omega, pair in zip(patterns, modes.frequencies, pairs, strict=True):
            swing = amplitude * np.cos(omega * times[frame])
            artists.extend(_place(pair, pattern[0] * swing, pattern[1] * swing))
        return tuple(artists)

    print(f"[render] modes at {modes.frequencies[0]:.4f} and {modes.frequencies[1]:.4f} rad/s")
    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "coupled-modes")


def render_site_vs_mode(n_frames: int = 420) -> None:
    """One motion, two pictures: sloshing on the left, standing still on the right.

    The same trajectory drives both panels. In the site picture energy runs back and forth
    between the masses and nothing is constant. In the mode picture the two bars do not move
    at all. Neither picture is more true than the other; the mode picture is simply the one in
    which the answer is already a pair of numbers.

    This is the course's site/mode motif, and it returns for cavity modes and guided modes
    much later — worth recognising here, where it is still two masses on a bench.
    """
    pair_modes = coupled.normal_mode_solve(*coupled.two_mass_matrices(MASS, STIFFNESS, COUPLING))
    _, modes, run, energies = _start_one(
        coupled.exchange_time(*pair_modes.frequencies), n_frames
    )
    modal = np.array(
        [
            coupled.modal_energies(modes, x, v)
            for x, v in zip(run.positions, run.velocities, strict=True)
        ]
    )
    ceiling = 1.25 * max(energies.sum(axis=1)[0], modal[0].max())

    fig, (site_axis, mode_axis) = plt.subplots(1, 2, figsize=(8.4, 3.4), dpi=DPI)
    for axis, labels in ((site_axis, ["mass 1", "mass 2"]), (mode_axis, ["mode s", "mode a"])):
        axis.set_xlim(-0.6, 1.6)
        axis.set_ylim(0.0, ceiling)
        axis.set_xticks([0, 1])
        axis.set_xticklabels(labels)
        axis.set_yticks([])
    site_axis.set_ylabel("energy (J)")
    site_bars = site_axis.bar([0, 1], energies[0], color=[BLUE, ORANGE], width=0.6)
    mode_bars = mode_axis.bar([0, 1], modal[0], color=[GREEN, GREY], width=0.6)
    site_axis.axhline(energies.sum(axis=1)[0], color="0.6", lw=0.8, ls="--")
    mode_axis.axhline(energies.sum(axis=1)[0], color="0.6", lw=0.8, ls="--")
    fig.tight_layout()

    def update(frame: int):
        for bar, value in zip(site_bars, energies[frame], strict=True):
            bar.set_height(value)
        for bar, value in zip(mode_bars, modal[frame], strict=True):
            bar.set_height(value)
        return (*site_bars, *mode_bars)

    drift = np.max(np.abs(modal - modal[0])) / modal[0].sum()
    print(f"[render] site vs mode: modal energies vary by {drift:.1e} of the total")
    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "coupled-site-vs-mode")


if __name__ == "__main__":
    render_exchange()
    render_modes()
    render_site_vs_mode()
