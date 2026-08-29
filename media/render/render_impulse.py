"""Render the demonstration animations for module 05 (impulse response and convolution).

Animations are produced from `wavelab` itself, so what a student watches is the same model
they can read, run and test — never a hand-drawn impression of it.

Output is MP4, written by `_common.save`; see that module for why, and for the constraints the
format brings. The animations carry no words, so the same file serves both language sites; the
caption that explains each one is ordinary translated page prose rather than a subtitle track
that could silently drift from the text around it.

Run:  uv run python media/render/render_impulse.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, save  # noqa: E402
from wavelab import oscillators  # noqa: E402

BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#059669"
GREY = "0.55"

MASS = 0.5
STIFFNESS = 8.0
OMEGA0 = oscillators.natural_frequency(MASS, STIFFNESS)
PERIOD = 2.0 * np.pi / OMEGA0
CRITICAL_DAMPING = 2.0 * np.sqrt(MASS * STIFFNESS)


def render_convolution(n_frames: int = 300) -> None:
    """Kicks arriving one at a time, each spawning a ringdown, the ringdowns summing.

    This is the module's central claim made visible: the oscillator answers every kick the
    same way, and the motion under an arbitrary force is nothing but those answers added up.
    A playhead sweeps the record so that each faint curve *begins* where its kick lands —
    which is causality drawn rather than asserted, since no faint curve exists to the left of
    the arrow that created it.

    Kick signs are mixed on purpose. A demonstration in which every contribution adds would
    teach that superposition means growth; here the third and fourth kicks partly cancel what
    the second one built, which is the same arithmetic and the more honest picture.
    """
    # Q = 4: long enough that a kick still rings when the next arrives — so the curves have
    # something to superpose — and short enough that each ringdown visibly belongs to its own
    # arrow rather than smearing across the whole record.
    damping = 0.5
    span = 9.0 * PERIOD
    times = np.linspace(0.0, span, 1200)

    rng = np.random.default_rng(11)
    kick_times = np.sort(rng.uniform(0.4 * PERIOD, 6.2 * PERIOD, 5))
    strengths = rng.choice([-1.0, 1.0], 5) * rng.uniform(0.6, 1.0, 5)

    # Every kick's contribution over the whole record, computed once: G(t - t_i) is zero
    # before t_i by construction, so the causal masking below is the library's, not the
    # script's.
    contributions = np.array(
        [
            strength * oscillators.impulse_response(times - t0, MASS, STIFFNESS, damping)
            for t0, strength in zip(kick_times, strengths, strict=True)
        ]
    )
    total = contributions.sum(axis=0)
    reach = 1.25 * np.max(np.abs(total))

    fig, (force_axis, motion) = plt.subplots(
        2, 1, figsize=(9.2, 4.4), dpi=DPI, sharex=True, gridspec_kw={"height_ratios": [1.0, 2.4]}
    )

    force_axis.set_xlim(0.0, span)
    force_axis.set_ylim(-1.25, 1.25)
    force_axis.set_ylabel("F (arb.)")
    force_axis.axhline(0.0, color="0.85", lw=0.8, zorder=0)
    arrows = [
        force_axis.annotate(
            "",
            xy=(t0, strength),
            xytext=(t0, 0.0),
            arrowprops={"arrowstyle": "-|>", "color": ORANGE, "lw": 1.6},
        )
        for t0, strength in zip(kick_times, strengths, strict=True)
    ]

    motion.set_xlim(0.0, span)
    motion.set_ylim(-reach, reach)
    motion.set_xlabel("t (s)")
    motion.set_ylabel("x (m)")
    motion.axhline(0.0, color="0.85", lw=0.8, zorder=0)
    faint = [motion.plot([], [], lw=1.0, color=GREY, alpha=0.75)[0] for _ in kick_times]
    (bold,) = motion.plot([], [], lw=2.0, color=BLUE)
    playhead = motion.axvline(0.0, color=GREEN, lw=1.0, ls=":")
    fig.tight_layout()

    def update(frame: int):
        now = span * (frame + 1) / n_frames
        upto = times <= now
        fired = kick_times <= now

        for arrow, has_fired in zip(arrows, fired, strict=True):
            arrow.set_visible(bool(has_fired))
        for curve, contribution, has_fired in zip(faint, contributions, fired, strict=True):
            if has_fired:
                curve.set_data(times[upto], contribution[upto])
            else:
                curve.set_data([], [])
        if fired.any():
            bold.set_data(times[upto], contributions[fired].sum(axis=0)[upto])
        else:
            bold.set_data([], [])
        playhead.set_xdata([now, now])
        return (*arrows, *faint, bold, playhead)

    print(f"[render] convolution at Q = {oscillators.quality_factor(MASS, STIFFNESS, damping):.2f}")
    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "impulse-convolution")


def render_step_overshoot(n_frames: int = 300) -> None:
    """A constant force switched on, answered by four oscillators of different Q.

    The force has no features at all after the switch-on, and the responses ring anyway: the
    falsifier for the belief that a linear system's displacement follows the shape of what
    pushed it. All four curves end at the same place, F0/k, so the only thing separating them
    is how they get there — 85% above the final value at Q = 10, 44% at Q = 2, 16% at Q = 1,
    and not at all once damping is critical.

    Drawn progressively rather than shown finished, because the overshoot is an event in time;
    a static plot of the same four curves lets a reader take the peak for the destination.
    """
    dampings = (CRITICAL_DAMPING, 2.0, 1.0, 0.2)
    colours = (GREY, GREEN, ORANGE, BLUE)
    span = 14.0 * PERIOD
    times = np.linspace(0.0, span, 1600)
    final = 1.0 / STIFFNESS

    responses = [oscillators.step_response(times, MASS, STIFFNESS, b, 1.0) for b in dampings]

    fig, (force_axis, axis) = plt.subplots(
        2, 1, figsize=(9.2, 4.4), dpi=DPI, sharex=True, gridspec_kw={"height_ratios": [1.0, 2.6]}
    )

    # The force panel is what makes this a falsifier rather than a gallery of curves: it has
    # exactly one feature, at t = 0, and everything below it rings for twenty seconds.
    force_axis.set_xlim(0.0, span)
    force_axis.set_ylim(-0.15, 1.35)
    force_axis.set_ylabel("F (arb.)")
    force_axis.axhline(0.0, color="0.85", lw=0.8, zorder=0)
    (force_trace,) = force_axis.plot([], [], lw=1.8, color=ORANGE)

    axis.set_xlim(0.0, span)
    axis.set_ylim(0.0, 1.15 * max(r.max() for r in responses))
    axis.set_xlabel("t (s)")
    axis.set_ylabel("x (m)")
    axis.axhline(final, color="0.8", lw=1.0, ls="--", zorder=0)
    traces = [axis.plot([], [], lw=1.8, color=c)[0] for c in colours]
    peaks = [axis.plot([], [], marker="o", markersize=5, color=c)[0] for c in colours]
    fig.tight_layout()

    def update(frame: int):
        upto = slice(0, int(len(times) * (frame + 1) / n_frames))
        force_trace.set_data(times[upto], np.ones(len(times))[upto])
        for trace, peak, response in zip(traces, peaks, responses, strict=True):
            shown = response[upto]
            trace.set_data(times[upto], shown)
            # The marker appears only once a curve has actually turned over, so it reads as a
            # maximum rather than as the leading edge of the line.
            crest = int(np.argmax(shown)) if shown.size else 0
            if shown.size and crest < shown.size - 1 and shown[crest] > final:
                peak.set_data([times[crest]], [shown[crest]])
        return (force_trace, *traces, *peaks)

    for damping, response in zip(dampings, responses, strict=True):
        q = oscillators.quality_factor(MASS, STIFFNESS, damping)
        overshoot = 100.0 * (response.max() / final - 1.0)
        print(f"[render] step at Q = {q:5.2f}: overshoot {overshoot:5.1f}%")
    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "impulse-step-overshoot")


if __name__ == "__main__":
    render_convolution()
    render_step_overshoot()
