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


# ---------------------------------------------------------------------------
# Module 07: the chain
#
# Chains are drawn transversely — masses at fixed spacing along x, displaced up and down —
# while the model is one-dimensional and longitudinal. The two are the same equations, as the
# model specification says, and the transverse picture is the one in which a mode *looks* like
# the sine wave it is. Drawn longitudinally the shapes are a row of squares bunching up, which
# is honest and unreadable.
# ---------------------------------------------------------------------------

CHAIN_MASS = 0.5
CHAIN_STIFFNESS = 8.0
CHAIN_LENGTH = 1.0  # wall to wall, so the spacing is L/(N+1) whatever N is


def _chain_positions(n: int) -> np.ndarray:
    """Rest positions of `n` masses plus the two walls, evenly spaced across the length."""
    return np.linspace(0.0, CHAIN_LENGTH, n + 2)


def _draw_chain_axes(axis, span: float) -> None:
    """Walls, rest line and limits for a transverse chain panel."""
    axis.set_xlim(-0.03 * CHAIN_LENGTH, 1.03 * CHAIN_LENGTH)
    axis.set_ylim(-span, span)
    axis.set_xticks([])
    axis.set_yticks([])
    axis.axhline(0.0, color="0.9", lw=0.8)
    for wall in (0.0, CHAIN_LENGTH):
        axis.plot([wall], [0.0], marker="|", markersize=18, color="0.3", mew=3)


def _chain_artists(axis, colour: str = BLUE):
    """A line through the whole chain and markers on the masses only."""
    (thread,) = axis.plot([], [], color=GREY, lw=1.0)
    (beads,) = axis.plot([], [], marker="o", markersize=5, ls="none", color=colour)
    return thread, beads


def _place_chain(artists, rest: np.ndarray, displacement: np.ndarray) -> tuple:
    """Position a chain's artists; `displacement` covers the masses, the walls stay at zero."""
    thread, beads = artists
    y = np.concatenate([[0.0], displacement, [0.0]])
    thread.set_data(rest, y)
    beads.set_data(rest[1:-1], displacement)
    return thread, beads


def render_chain_modes(n_frames: int = 300, n: int = 5) -> None:
    """The five modes of a five-mass chain, each frozen into its own shape and its own rate.

    Frequency-ordered top to bottom, which is also node-ordered: mode p has p - 1 places where
    the chain stands still, and every extra node costs frequency. That correspondence is the
    thing to take away, because it lets a student sketch the shapes of a chain they have never
    computed — and it survives all the way to the modes of an optical cavity.

    Playback is slower than real time (about 0.45x) so the fastest mode is still watchable.
    All five run for the same physical duration, so what the eye compares is genuinely their
    rates: the top mode completes one and a half cycles while the bottom completes six.
    """
    modes = coupled.normal_mode_solve(*coupled.chain_matrices(n, CHAIN_MASS, CHAIN_STIFFNESS))
    duration = 1.5 * 2.0 * np.pi / modes.frequencies[0]
    times = np.linspace(0.0, duration, n_frames)
    rest = _chain_positions(n)
    amplitude = 0.7

    fig, axes = plt.subplots(n, 1, figsize=(6.4, 5.6), dpi=DPI)
    chains = []
    for p, axis in enumerate(axes):
        _draw_chain_axes(axis, 1.0)
        chains.append(_chain_artists(axis, BLUE if p % 2 == 0 else ORANGE))
        axis.set_ylabel(f"p = {p + 1}", fontsize=9, rotation=0, ha="right", va="center")
        axis.text(
            0.995, 0.06, f"{modes.frequencies[p]:.2f} rad/s",
            transform=axis.transAxes, ha="right", fontsize=8, color="0.45",
        )
    fig.tight_layout()

    # Each column is normalised to the same visible amplitude, so the panels compare shapes
    # rather than the solver's M-orthonormal scaling — and to `chain_mode_shapes`' sign, so a
    # mode whose largest entry happens to be negative is not drawn upside down.
    closed_form = coupled.chain_mode_shapes(n)
    patterns = [closed_form[:, p] / np.max(np.abs(closed_form[:, p])) for p in range(n)]

    def update(frame: int):
        artists = []
        for pattern, omega, chain in zip(patterns, modes.frequencies, chains, strict=True):
            swing = amplitude * np.cos(omega * times[frame])
            artists.extend(_place_chain(chain, rest, pattern * swing))
        return tuple(artists)

    print(f"[render] chain modes at {np.round(modes.frequencies, 3)} rad/s")
    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "chain-modes")


def render_chain_continuum(hold: int = 70) -> None:
    """Adding masses at fixed length: the lowest shape becomes a sine, the band fills in.

    Two things happen at once and the shot exists to show that they are the same thing. On the
    left the chain's slowest mode is drawn against the string's half-sine; at N = 2 it is a
    tent and by N = 50 the two are indistinguishable. On the right each chain drops its N modes
    onto the dispersion curve as dots, and as N grows the dots crowd in until they trace the
    sine they were always sitting on.

    Both panels are plotted in scaled units — displacement over its maximum, ka against
    omega/(2 sqrt(k_s/m)) — because the point is that the curve does not depend on N. Only
    which points of it a given chain is allowed to occupy does.
    """
    sizes = (2, 5, 10, 20, 50)
    fine = np.linspace(0.0, 1.0, 400)

    fig, (shape_axis, band_axis) = plt.subplots(1, 2, figsize=(9.6, 3.4), dpi=DPI)

    shape_axis.set_xlim(-0.02, 1.02)
    shape_axis.set_ylim(-0.15, 1.15)
    shape_axis.set_xlabel("position along the chain")
    shape_axis.set_ylabel("displacement (scaled)")
    shape_axis.plot(fine, np.sin(np.pi * fine), lw=1.2, ls="--", color=GREY)
    shape_thread, shape_beads = _chain_artists(shape_axis, BLUE)
    shape_thread.set_color(BLUE)
    size_label = shape_axis.text(0.03, 0.88, "", transform=shape_axis.transAxes, fontsize=11)

    band_axis.set_xlim(0.0, np.pi)
    band_axis.set_ylim(0.0, 1.08)
    band_axis.set_xlabel("k a (rad)")
    band_axis.set_ylabel("omega / 2 sqrt(k_s/m)")
    band_axis.set_xticks([0.0, np.pi / 2.0, np.pi])
    band_axis.set_xticklabels(["0", "pi/2", "pi"])
    band_axis.plot(fine * np.pi, np.abs(np.sin(0.5 * fine * np.pi)), lw=1.2, color=GREY)
    (dots,) = band_axis.plot([], [], marker="o", ms=4, ls="none", color=ORANGE)
    band_axis.axvline(np.pi, color="0.85", lw=0.8, ls=":")
    fig.tight_layout()

    # One frame list, built up front: each size contributes `hold` identical frames, so the
    # animation is a slide show of five chains rather than an interpolation between them —
    # there is nothing in between, since N is an integer.
    frames = []
    for n in sizes:
        spacing = CHAIN_LENGTH / (n + 1)
        rest = _chain_positions(n)
        shape = coupled.chain_mode_shapes(n)[:, 0]
        shape = shape / np.max(np.abs(shape))
        wavenumbers = np.arange(1, n + 1) * np.pi / CHAIN_LENGTH
        band = coupled.chain_dispersion(wavenumbers, spacing, CHAIN_MASS, CHAIN_STIFFNESS)
        ceiling = 2.0 * np.sqrt(CHAIN_STIFFNESS / CHAIN_MASS)
        frames.extend([(n, rest, shape, wavenumbers * spacing, band / ceiling)] * hold)

    def update(frame: int):
        n, rest, shape, ka, band = frames[frame]
        _place_chain((shape_thread, shape_beads), rest, shape)
        dots.set_data(ka, band)
        size_label.set_text(f"N = {n}")
        return shape_thread, shape_beads, dots, size_label

    errors = {
        n: abs(
            coupled.chain_mode_frequencies(n, CHAIN_MASS, CHAIN_STIFFNESS)[0]
            / coupled.chain_continuum_frequencies(n, CHAIN_MASS, CHAIN_STIFFNESS)[0]
            - 1.0
        )
        for n in sizes
    }
    print("[render] lowest-mode error vs the string: "
          + ", ".join(f"N={n}: {e:.2e}" for n, e in errors.items()))
    save(FuncAnimation(fig, update, frames=len(frames), blit=False), fig, "chain-continuum")


def render_chain_pluck(n_frames: int = 420, n: int = 20, substeps: int = 40) -> None:
    """A plucked chain, read twice: energy that travels, and energy that does not.

    This is module 06's site-versus-mode shot with twenty masses instead of two, and it is the
    falsifier for `modes-exchange-energy`. The middle bars are the twenty masses and they are
    never still. The right-hand bars are the twenty modes and they never move at all — for the
    whole run, at every step, while the chain visibly rings.

    As in module 06 the trajectory comes from the integrator rather than from `evolve`, and
    the substepping matters for the same reason: `evolve` would make the modal bars constant
    by construction, which is the one thing this shot must not assume. What it shows instead
    is twenty coupled equations, stepped in ignorance of any mode, producing twenty constants.
    """
    matrices = coupled.chain_matrices(n, CHAIN_MASS, CHAIN_STIFFNESS)
    modes = coupled.normal_mode_solve(*matrices)
    duration = 2.0 * 2.0 * np.pi / modes.frequencies[0]

    site = np.arange(1, n + 1)
    pluck = 0.35 * np.minimum(site, n + 1 - site) / ((n + 1) / 2.0)
    dt = duration / ((n_frames - 1) * substeps)
    fine = coupled.simulate_coupled(
        *matrices, pluck, np.zeros(n), dt, (n_frames - 1) * substeps
    )
    positions = fine.positions[::substeps]
    velocities = fine.velocities[::substeps]
    site_energy = coupled.site_energies(*matrices, positions, velocities)
    modal_energy = coupled.modal_energies(modes, positions, velocities)

    fig, (chain_axis, site_axis, mode_axis) = plt.subplots(
        1, 3, figsize=(11.2, 3.2), dpi=DPI, gridspec_kw={"width_ratios": [1.5, 1.0, 1.0]}
    )
    _draw_chain_axes(chain_axis, 0.45)
    chain = _chain_artists(chain_axis, BLUE)
    rest = _chain_positions(n)

    # Each panel is scaled to its own tallest bar. Scaling both to the total would flatten
    # twenty site bars into a smear, and scaling both to the modal maximum would flatten them
    # further still — a plucked chain puts 85% of its energy in the fundamental. The question
    # each panel answers is whether its own bars move, and that survives separate scales.
    for axis, label, energy in (
        (site_axis, "energy per mass", site_energy),
        (mode_axis, "energy per mode", modal_energy),
    ):
        axis.set_xlim(0.3, n + 0.7)
        axis.set_ylim(0.0, 1.12 * energy.max())
        axis.set_yticks([])
        axis.set_xticks([1, n // 2, n])
        axis.set_xlabel(label)
    site_bars = site_axis.bar(site, site_energy[0], color=ORANGE, width=0.75)
    mode_bars = mode_axis.bar(site, modal_energy[0], color=GREEN, width=0.75)

    # Dashes at the starting heights, so "the bars do not move" is something a viewer checks
    # rather than something the caption asserts. On the left they are left behind immediately.
    for axis, initial in ((site_axis, site_energy[0]), (mode_axis, modal_energy[0])):
        axis.hlines(initial, site - 0.42, site + 0.42, color="0.45", lw=0.9, ls="--")
    fig.tight_layout()

    def update(frame: int):
        _place_chain(chain, rest, positions[frame])
        for bar, value in zip(site_bars, site_energy[frame], strict=True):
            bar.set_height(value)
        for bar, value in zip(mode_bars, modal_energy[frame], strict=True):
            bar.set_height(value)
        return (*chain, *site_bars, *mode_bars)

    drift = np.max(np.abs(modal_energy - modal_energy[0])) / modal_energy[0].sum()
    shares = site_energy / site_energy.sum(axis=1, keepdims=True)
    print(f"[render] pluck: modal energies vary by {drift:.1e} of the total while the "
          f"widest site share swings by {np.ptp(shares, axis=0).max():.2f}")
    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "chain-pluck")


if __name__ == "__main__":
    render_exchange()
    render_modes()
    render_site_vs_mode()
    render_chain_modes()
    render_chain_continuum()
    render_chain_pluck()
