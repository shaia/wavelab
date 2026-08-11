"""Render the demonstration animations for module 00 (phasors).

Animations are produced from `wavelab` itself, so what a student watches is the same model
they can read, run and test — never a hand-drawn impression of it.

Output is MP4, written by `_common.save`; see that module for why, and for the constraints the
format brings. The animations carry no words, so the same file serves both language sites; the
caption that explains each one is ordinary translated page prose rather than a subtitle track
that could silently drift from the text around it.

The arrows rotate CLOCKWISE — the course phase convention made visible. If an update ever
makes them turn the other way, the convention has been broken somewhere.

Run:  uv run python media/render/render_phasors.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, FPS, save  # noqa: E402
from wavelab import phasors  # noqa: E402

BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#059669"


def _arrow_artist(ax, color):
    quiver = ax.quiver(
        [0.0], [0.0], [0.0], [0.0],
        angles="xy", scale_units="xy", scale=1.0,
        color=color, width=0.012,
    )
    return quiver


def render_superposition(n_frames: int = 300) -> None:
    """Two rotating phasors tip-to-tail beside the three real signals they project.

    The sum arrow rotates rigidly with its parts — same frequency — so its projection is
    again a cosine; only its length depends on the phase difference.
    """
    omega = 2.0 * np.pi / 3.0  # one turn every 3 s
    duration = n_frames / FPS
    times = np.linspace(0.0, duration, n_frames)

    z1 = phasors.phasor(1.0, 0.0)
    z2 = phasors.phasor(0.7, 2.0)
    z_sum = z1 + z2
    rot1 = phasors.evaluate(z1, omega, times)
    rot2 = phasors.evaluate(z2, omega, times)
    rot_sum = phasors.evaluate(z_sum, omega, times)

    fig, (left, right) = plt.subplots(
        1, 2, figsize=(8.5, 3.6), dpi=DPI, gridspec_kw={"width_ratios": [1.0, 1.6]}
    )

    reach = abs(z_sum) * 1.15
    left.set_xlim(-reach, reach)
    left.set_ylim(-reach, reach)
    left.set_aspect("equal")
    left.axhline(0.0, color="0.85", lw=0.8, zorder=0)
    left.axvline(0.0, color="0.85", lw=0.8, zorder=0)
    left.set_xlabel("Re")
    left.set_ylabel("Im")
    circle = plt.Circle((0, 0), abs(z_sum), fill=False, color="0.9", lw=0.8, zorder=0)
    left.add_patch(circle)
    arrow1 = _arrow_artist(left, BLUE)
    arrow2 = _arrow_artist(left, ORANGE)
    arrow_sum = _arrow_artist(left, GREEN)

    right.set_xlim(0.0, duration)
    right.set_ylim(-reach, reach)
    right.set_xlabel("t (s)")
    right.set_ylabel("Re")
    (trace1,) = right.plot([], [], lw=1.0, color=BLUE, alpha=0.8)
    (trace2,) = right.plot([], [], lw=1.0, color=ORANGE, alpha=0.8)
    (trace_sum,) = right.plot([], [], lw=1.8, color=GREEN)
    fig.tight_layout()

    def update(frame: int):
        a, b, s = rot1[frame], rot2[frame], rot_sum[frame]
        arrow1.set_UVC([a.real], [a.imag])
        arrow2.set_offsets([[a.real, a.imag]])
        arrow2.set_UVC([b.real], [b.imag])
        arrow_sum.set_UVC([s.real], [s.imag])
        upto = slice(0, frame + 1)
        trace1.set_data(times[upto], rot1[upto].real)
        trace2.set_data(times[upto], rot2[upto].real)
        trace_sum.set_data(times[upto], rot_sum[upto].real)
        return arrow1, arrow2, arrow_sum, trace1, trace2, trace_sum

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "phasor-superposition")


def render_beats(n_frames: int = 300) -> None:
    """Two equal amplitudes at nearby frequencies: counter-turning arrows in the mean
    rotating frame, beside the pulsing sum they project.

    In the frame rotating at the mean frequency the two phasors turn slowly in opposite
    senses; their sum stretches and collapses along the real axis at the half-difference
    frequency, and the projected intensity pulses at the full difference.
    """
    f1, f2 = 1.0, 1.2  # Hz — beat period 5 s, two full beats in one loop
    omega1, omega2 = 2.0 * np.pi * f1, 2.0 * np.pi * f2
    half_delta = 0.5 * (omega1 - omega2)
    amplitude = 0.6
    duration = n_frames / FPS
    times = np.linspace(0.0, duration, n_frames)

    frame1 = amplitude * np.exp(-1j * half_delta * times)
    frame2 = amplitude * np.exp(+1j * half_delta * times)
    frame_sum = frame1 + frame2
    signal = phasors.beat_signal(amplitude, amplitude, omega1, omega2, times)
    envelope = 2.0 * amplitude * np.cos(half_delta * times)

    fig, (left, right) = plt.subplots(
        1, 2, figsize=(8.5, 3.6), dpi=DPI, gridspec_kw={"width_ratios": [1.0, 1.6]}
    )

    reach = 2.0 * amplitude * 1.15
    left.set_xlim(-reach, reach)
    left.set_ylim(-reach, reach)
    left.set_aspect("equal")
    left.axhline(0.0, color="0.85", lw=0.8, zorder=0)
    left.axvline(0.0, color="0.85", lw=0.8, zorder=0)
    left.set_xlabel("Re")
    left.set_ylabel("Im")
    arrow1 = _arrow_artist(left, BLUE)
    arrow2 = _arrow_artist(left, ORANGE)
    arrow_sum = _arrow_artist(left, GREEN)

    right.set_xlim(0.0, duration)
    right.set_ylim(-reach, reach)
    right.set_xlabel("t (s)")
    right.set_ylabel("signal")
    right.plot(times, envelope, color="0.75", lw=1.0, ls="--")
    right.plot(times, -envelope, color="0.75", lw=1.0, ls="--")
    (trace,) = right.plot([], [], lw=1.4, color=GREEN)
    fig.tight_layout()

    def update(frame: int):
        a, b, s = frame1[frame], frame2[frame], frame_sum[frame]
        arrow1.set_UVC([a.real], [a.imag])
        arrow2.set_offsets([[a.real, a.imag]])
        arrow2.set_UVC([b.real], [b.imag])
        arrow_sum.set_UVC([s.real], [s.imag])
        upto = slice(0, frame + 1)
        trace.set_data(times[upto], signal[upto])
        return arrow1, arrow2, arrow_sum, trace

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "beats")


if __name__ == "__main__":
    render_superposition()
    render_beats()
