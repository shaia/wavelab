"""Render the demonstration animations for modules 03 and 04 (Fourier series and transform).

Animations are produced from `wavelab` itself, so what a student watches is the same model
they can read, run and test — never a hand-drawn impression of it.

Output is MP4, written by `_common.save`; see that module for why, and for the constraints the
format brings. The animations carry no words, so the same file serves both language sites; the
caption that explains each one is ordinary translated page prose rather than a subtitle track
that could silently drift from the text around it.

One script covers both modules because they share a subject and, in `fourier.py`, a source of
truth; the four shots divide two to a page.

Run:  uv run python media/render/render_fourier.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, save  # noqa: E402
from wavelab import fourier  # noqa: E402

BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#059669"
GREY = "0.55"

OMEGA0 = 1.0
PERIOD = 2.0 * np.pi / OMEGA0


def _harmonic_arrows(coefficients: np.ndarray, phase: float) -> np.ndarray:
    """Successive tip positions of the harmonic phasors laid tip-to-tail at one instant.

    Arrow n is 2i conj(c_n) e^{-i n omega0 t}: module 00's phasor for harmonic n, turned a
    quarter turn so that the *height* of the running tip is the signal rather than its width.
    The rotation is common to every arrow, so it is a choice of which projection to read and
    not a change to any harmonic's phase relative to the others. Rotation stays clockwise,
    which is the course convention and what module 00's animation already showed.
    """
    n_max = (coefficients.size - 1) // 2
    orders = np.arange(1, n_max + 1)
    amplitudes = 2j * np.conj(coefficients[n_max + orders])
    steps = amplitudes * np.exp(-1j * orders * OMEGA0 * phase)
    return np.concatenate([[0.0 + 0.0j], np.cumsum(steps)])


def render_square_buildup(n_frames: int = 450) -> None:
    """A square wave assembling itself out of rotating arrows, one harmonic count at a time.

    The animation holds each of N = 1, 3, 5, 9, 33 for exactly one period, so the number of
    arrows changes but the sweep never does: what the eye compares between stages is the shape
    being traced, not the speed of the tracing. Arrow lengths come from `square_coefficients`
    rather than being set by hand, which is what makes the 1/n decay visible as geometry — the
    ninth arrow is a ninth of the first.

    The vertical limits are fixed with headroom above 1 on purpose. Autoscaling each stage
    would hide the overshoot that appears the moment there is more than one arrow, and this
    animation would then quietly argue for the misconception module 03 exists to break.
    """
    stages = [1, 3, 5, 9, 33]
    frames_per_stage = n_frames // len(stages)
    coefficient_sets = [fourier.square_coefficients(n) for n in stages]

    fig, (left, right) = plt.subplots(
        1, 2, figsize=(9.6, 4.0), dpi=DPI, gridspec_kw={"width_ratios": [1.0, 1.5]}
    )

    # The chain can stretch to sum(4/(pi n)) over the odd n it carries — about 2.76 at N = 33,
    # when every arrow lines up near the jump. Limits are set from that, not from the signal's
    # own range, or the arrows would run off the panel exactly where the lesson is.
    left.set_xlim(-2.95, 2.95)
    left.set_ylim(-2.95, 2.95)
    left.set_aspect("equal")
    left.set_xticks([])
    left.set_yticks([])
    left.axhline(0.0, color="0.9", lw=0.8, zorder=0)
    left.axvline(0.0, color="0.9", lw=0.8, zorder=0)
    (orbit,) = left.plot([], [], lw=1.0, color=GREY, alpha=0.55)
    (chain,) = left.plot([], [], lw=1.3, color=BLUE, marker="o", markersize=2.6)
    (tip,) = left.plot([], [], marker="o", markersize=7, color=ORANGE)

    right.set_xlim(0.0, PERIOD)
    right.set_ylim(-1.5, 1.5)
    right.set_xlabel("t (s)")
    right.set_ylabel("f(t)")
    right.axhline(0.0, color="0.9", lw=0.8, zorder=0)
    right.axhline(1.0, color=GREEN, lw=0.9, ls="--")
    right.axhline(-1.0, color=GREEN, lw=0.9, ls="--")
    (trace,) = right.plot([], [], lw=1.6, color=BLUE)
    (marker,) = right.plot([], [], marker="o", markersize=6, color=ORANGE)
    (connector,) = right.plot([], [], lw=0.8, ls=":", color=ORANGE)
    fig.tight_layout()

    # The closed curve each arrow chain traces over one period, precomputed per stage so the
    # shape the tip is drawing is visible from the first frame rather than emerging from it.
    orbits = [
        np.array([_harmonic_arrows(c, p)[-1] for p in np.linspace(0.0, PERIOD, 400)])
        for c in coefficient_sets
    ]

    def update(frame: int):
        stage = min(frame // frames_per_stage, len(stages) - 1)
        within = frame - stage * frames_per_stage
        phase = PERIOD * within / frames_per_stage
        coefficients = coefficient_sets[stage]

        vertices = _harmonic_arrows(coefficients, phase)
        orbit.set_data(orbits[stage].real, orbits[stage].imag)
        chain.set_data(vertices.real, vertices.imag)
        tip.set_data([vertices[-1].real], [vertices[-1].imag])

        history = np.linspace(0.0, phase, max(within + 1, 2))
        trace.set_data(history, fourier.partial_sum(coefficients, OMEGA0, history))
        height = float(vertices[-1].imag)
        marker.set_data([phase], [height])
        connector.set_data([0.0, phase], [height, height])
        return orbit, chain, tip, trace, marker, connector

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "fourier-square-buildup")


def render_gibbs_zoom(n_frames: int = 300) -> None:
    """The overshoot at a jump, first as terms are added and then under magnification.

    The two halves change one thing each, which is the whole design. Frames 0-149 hold the
    window still and raise N: the ripples crowd toward the discontinuity and the first horn
    slides in with them, but its height stays on the drawn line. Frames 150-299 freeze N and
    magnify the window twentyfold: the same structure reappears at every scale, still on the
    line. Sweeping both at once would let the eye attribute the constancy to either.

    Vertical limits never move. A zoom that rescaled the vertical axis would make the overshoot
    appear to grow or shrink for reasons that have nothing to do with the mathematics.
    """
    orders = [5, 9, 17, 31]
    hold_frames = n_frames // 2
    overshoot = 1.0 + 2.0 * fourier.gibbs_overshoot(orders[-1])

    fig, ax = plt.subplots(figsize=(8.4, 4.0), dpi=DPI)
    ax.set_ylim(-0.35, 1.35)
    ax.set_xlabel("t (s)")
    ax.set_ylabel("f(t)")
    ax.axhline(1.0, color="0.9", lw=0.8, zorder=0)
    ax.axhline(overshoot, color=GREEN, lw=1.1, ls="--")
    ax.axvline(0.0, color=GREY, lw=0.9)
    (curve,) = ax.plot([], [], lw=1.6, color=BLUE)
    fig.tight_layout()

    def update(frame: int):
        if frame < hold_frames:
            order = orders[min(frame * len(orders) // hold_frames, len(orders) - 1)]
            half_width = 0.55 * PERIOD
        else:
            order = orders[-1]
            fraction = (frame - hold_frames) / max(hold_frames - 1, 1)
            half_width = 0.55 * PERIOD * float(20.0**-fraction)

        times = np.linspace(-half_width, half_width, 4001)
        coefficients = fourier.square_coefficients(order)
        curve.set_data(times, fourier.partial_sum(coefficients, OMEGA0, times))
        ax.set_xlim(-half_width, half_width)
        return (curve,)

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "fourier-gibbs-zoom")


def render_uncertainty(n_frames: int = 300) -> None:
    """A Gaussian pulse squeezed in time while its spectrum widens by the reciprocal factor.

    Both panels keep fixed limits for the whole sweep, which is the only way the trade reads as
    a trade: if either axis rescaled itself, narrowing in time would stop looking like widening
    in frequency and start looking like nothing at all. The shaded bands are the RMS widths
    `rms_widths` actually returns, and the gauge across the top carries their product against
    the theoretical floor of one half. The marker never leaves the line — that is the theorem.

    The sweep is geometric in sigma so that equal frames are equal fractional changes; a linear
    sweep spends most of its time at the wide end where nothing much happens.
    """
    sigmas = np.geomspace(0.75, 0.12, n_frames // 2)
    sigmas = np.concatenate([sigmas, sigmas[::-1]])
    dt = 0.01
    times = (np.arange(4096) - 2048) * dt

    fig, (gauge, left, right) = plt.subplots(
        3, 1, figsize=(8.0, 5.2), dpi=DPI, gridspec_kw={"height_ratios": [0.28, 1.0, 1.0]}
    )

    gauge.set_xlim(0.0, 1.0)
    gauge.set_ylim(-1.0, 1.0)
    gauge.set_yticks([])
    gauge.set_xticks([0.5])
    gauge.set_xticklabels(["1/2"])
    gauge.axvline(0.5, color=GREEN, lw=1.4)
    gauge.set_xlabel("dt_rms x domega_rms")
    (product_marker,) = gauge.plot([], [], marker="o", markersize=8, color=ORANGE)

    left.set_xlim(-3.0, 3.0)
    left.set_ylim(0.0, 1.15)
    left.set_xlabel("t (s)")
    left.set_ylabel("f(t)")
    (pulse_curve,) = left.plot([], [], lw=1.6, color=BLUE)
    duration_band = left.axvspan(-1.0, 1.0, color=BLUE, alpha=0.13)

    right.set_xlim(-30.0, 30.0)
    right.set_ylim(0.0, 2.1)
    right.set_xlabel("omega (rad/s)")
    right.set_ylabel("|F(omega)|")
    (spectrum_curve,) = right.plot([], [], lw=1.6, color=ORANGE)
    bandwidth_band = right.axvspan(-1.0, 1.0, color=ORANGE, alpha=0.13)
    fig.tight_layout()

    def update(frame: int):
        sigma = float(sigmas[frame])
        pulse = fourier.gaussian_pulse(times, sigma)
        omega, transform = fourier.spectrum(pulse, dt)
        duration, bandwidth = fourier.rms_widths(pulse, dt)

        pulse_curve.set_data(times, pulse)
        spectrum_curve.set_data(omega, np.abs(transform))
        _span(duration_band, duration)
        _span(bandwidth_band, bandwidth)
        product_marker.set_data([duration * bandwidth], [0.0])
        return pulse_curve, spectrum_curve, duration_band, bandwidth_band, product_marker

    save(FuncAnimation(fig, update, frames=sigmas.size, blit=False), fig, "fourier-uncertainty")


def _span(band, half_width: float) -> None:
    """Recentre an `axvspan` rectangle to cover plus and minus `half_width`."""
    band.set_x(-half_width)
    band.set_width(2.0 * half_width)


def render_aliasing_wheel(n_frames: int = 360) -> None:
    """A wheel filmed by a strobe: the wagon-wheel effect, with the fold diagram it draws.

    The true rotation ramps from rest to twice the strobe rate. The strobed marker tracks it,
    slows, freezes when the two rates match, and then runs backwards — and every strobe flash
    adds a point to the right-hand panel, so the folding diagram is *measured by the wheel*
    rather than asserted beside it.

    The on-screen rotation is deliberately kept far below the video's own 30 frames per second.
    A faster wheel would alias against the encoded frame rate as well as against the strobe,
    and the animation would be demonstrating its own artefact instead of the physics.
    """
    strobe_rate = 1.4
    times = np.arange(n_frames) / 30.0
    true_rates = np.linspace(0.0, 2.0 * strobe_rate, n_frames)
    # Angle is the integral of a linearly ramped rate, so the wheel never jumps.
    angles = 2.0 * np.pi * (true_rates * times / 2.0)

    fig, (left, right) = plt.subplots(
        1, 2, figsize=(9.4, 4.0), dpi=DPI, gridspec_kw={"width_ratios": [1.0, 1.3]}
    )

    left.set_xlim(-1.35, 1.35)
    left.set_ylim(-1.35, 1.35)
    left.set_aspect("equal")
    left.set_xticks([])
    left.set_yticks([])
    rim = np.linspace(0.0, 2.0 * np.pi, 200)
    left.plot(np.cos(rim), np.sin(rim), lw=1.2, color=GREY)
    (spoke,) = left.plot([], [], lw=1.4, color=BLUE)
    (true_dot,) = left.plot([], [], marker="o", markersize=8, color=BLUE)
    (strobed_dot,) = left.plot([], [], marker="o", markersize=11, color=ORANGE, alpha=0.9)

    right.set_xlim(0.0, 2.0 * strobe_rate)
    right.set_ylim(-strobe_rate / 2.0 * 1.2, strobe_rate / 2.0 * 1.2)
    right.set_xlabel("true rotation rate (rev/s)")
    right.set_ylabel("apparent rate (rev/s)")
    right.axhline(0.0, color="0.9", lw=0.8, zorder=0)
    right.axvline(strobe_rate / 2.0, color=GREEN, lw=1.0, ls="--")
    (fold_trace,) = right.plot([], [], lw=0.0, marker="o", markersize=2.6, color=ORANGE)
    fig.tight_layout()

    flash_period = 1.0 / strobe_rate
    measured_true: list[float] = []
    measured_apparent: list[float] = []
    last_flash = [-1.0]
    held_angle = [0.0]

    def update(frame: int):
        now = times[frame]
        angle = angles[frame]
        spoke.set_data([0.0, np.cos(angle)], [0.0, np.sin(angle)])
        true_dot.set_data([np.cos(angle)], [np.sin(angle)])

        if now - last_flash[0] >= flash_period:
            last_flash[0] = now
            held_angle[0] = angle
            rate = float(true_rates[frame])
            apparent = (rate + strobe_rate / 2.0) % strobe_rate - strobe_rate / 2.0
            measured_true.append(rate)
            measured_apparent.append(apparent)
            fold_trace.set_data(measured_true, measured_apparent)

        held = held_angle[0]
        strobed_dot.set_data([np.cos(held)], [np.sin(held)])
        return spoke, true_dot, strobed_dot, fold_trace

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "fourier-aliasing-wheel")


if __name__ == "__main__":
    render_square_buildup()
    render_gibbs_zoom()
    render_uncertainty()
    render_aliasing_wheel()
