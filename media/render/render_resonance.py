"""Render the demonstration animations for module 02 (damping, resonance, and Q).

Animations are produced from `wavelab` itself, so what a student watches is the same model
they can read, run and test — never a hand-drawn impression of it.

Output is MP4, written by `_common.save`; see that module for why, and for the constraints the
format brings. The animations carry no words, so the same file serves both language sites; the
caption that explains each one is ordinary translated page prose rather than a subtitle track
that could silently drift from the text around it.

Run:  uv run python media/render/render_resonance.py
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


def render_regimes(n_frames: int = 300) -> None:
    """One oscillator released from rest, again and again, as the damping is swept.

    The sweep runs continuously across the critical value rather than showing three separate
    cases, because the three "regimes" are one function: nothing discontinuous happens as the
    ringing dies out, it simply runs out of cycles. The phase-space panel makes the same point
    geometrically — module 01's closed ellipse unwinding into a spiral and then into a curve
    that never completes a turn.
    """
    times = np.linspace(0.0, 6.0 * PERIOD, 900)
    # Logarithmic in gamma / (2 omega0), so equal frames are equal *fractional* changes in
    # damping; a linear sweep spends almost all its frames in the overdamped tail.
    ratios = np.geomspace(0.03, 3.0, n_frames)
    dampings = ratios * CRITICAL_DAMPING

    fig, (left, right) = plt.subplots(
        1, 2, figsize=(9.2, 3.6), dpi=DPI, gridspec_kw={"width_ratios": [1.6, 1.0]}
    )

    left.set_xlim(0.0, times[-1])
    left.set_ylim(-0.12, 0.12)
    left.set_xlabel("t (s)")
    left.set_ylabel("x (m)")
    left.axhline(0.0, color="0.85", lw=0.8, zorder=0)
    (trace,) = left.plot([], [], lw=1.6, color=BLUE)
    (envelope_upper,) = left.plot([], [], lw=0.9, ls="--", color=GREY)
    (envelope_lower,) = left.plot([], [], lw=0.9, ls="--", color=GREY)

    right.set_xlim(-0.12, 0.12)
    right.set_ylim(-0.5, 0.5)
    right.set_xlabel("x (m)")
    right.set_ylabel("v (m/s)")
    right.axhline(0.0, color="0.85", lw=0.8, zorder=0)
    right.axvline(0.0, color="0.85", lw=0.8, zorder=0)
    (orbit,) = right.plot([], [], lw=1.1, color=ORANGE)
    (endpoint,) = right.plot([], [], marker="o", markersize=6, color=ORANGE)

    # A damping gauge along the top: one moving marker on a bar whose midpoint is critical.
    gauge = fig.add_axes((0.08, 0.90, 0.84, 0.035))
    gauge.set_xlim(np.log10(ratios[0]), np.log10(ratios[-1]))
    gauge.set_ylim(0.0, 1.0)
    gauge.set_xticks([np.log10(ratios[0]), 0.0, np.log10(ratios[-1])])
    gauge.set_xticklabels(["", "", ""])
    gauge.set_yticks([])
    gauge.axvline(0.0, color=GREEN, lw=1.6)  # gamma = 2 omega0, the critical boundary
    (marker,) = gauge.plot([], [], marker="v", markersize=8, color=BLUE)
    fig.subplots_adjust(top=0.84)

    def update(frame: int):
        damping = dampings[frame]
        gamma = oscillators.damping_rate(MASS, damping)
        x = oscillators.damped_position(times, MASS, STIFFNESS, damping, 0.1, 0.0)
        v = np.gradient(x, times)
        decay = 0.1 * np.exp(-gamma * times / 2.0)

        trace.set_data(times, x)
        envelope_upper.set_data(times, decay)
        envelope_lower.set_data(times, -decay)
        orbit.set_data(x, v)
        endpoint.set_data([x[-1]], [v[-1]])
        marker.set_data([np.log10(ratios[frame])], [0.5])
        return trace, envelope_upper, envelope_lower, orbit, endpoint, marker

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "resonance-regimes")


def render_sweep(n_frames: int = 300) -> None:
    """A drive slowly ramped through resonance, with the response curve drawn as it is measured.

    Left: the steady-state motion at the current drive frequency, with the drive itself behind
    it, so the lag can be *seen* rotating from zero through a quarter cycle to a half. Right:
    the amplitude and lag curves, filled in point by point as the ramp passes over them — the
    resonance curve as a measurement rather than as a formula. The marker on the amplitude
    panel and the vertical line at the peak sit at different frequencies on purpose: that gap
    is the misconception this module exists to kill.
    """
    # Q = 2. Deliberately low: at the Q ~ 20 of a nice-looking resonance the peak sits
    # 0.06% below omega0 and the two vertical lines land on the same pixel, which would make
    # the figure quietly argue for the misconception the module is here to break. At Q = 2
    # the gap is 6.5% of omega0 and unmistakable, and the response still rises by a clear
    # factor of Q over its static value.
    damping = 1.0
    q = oscillators.quality_factor(MASS, STIFFNESS, damping)
    peak = oscillators.resonance_peak_omega(MASS, STIFFNESS, damping)

    drives = np.linspace(0.25 * OMEGA0, 1.9 * OMEGA0, n_frames)
    response = oscillators.steady_state_response(drives, MASS, STIFFNESS, damping, 1.0)
    amplitude = np.abs(response)
    lag = np.angle(response)
    window = np.linspace(0.0, 3.0 * PERIOD, 600)

    fig, (motion, curves) = plt.subplots(
        1, 2, figsize=(9.6, 3.8), dpi=DPI, gridspec_kw={"width_ratios": [1.2, 1.0]}
    )

    motion.set_xlim(0.0, window[-1])
    motion.set_ylim(-1.15 * amplitude.max(), 1.15 * amplitude.max())
    motion.set_xlabel("t (s)")
    motion.set_ylabel("x (m)   /   F (arb.)")
    motion.axhline(0.0, color="0.85", lw=0.8, zorder=0)
    (drive_trace,) = motion.plot([], [], lw=1.1, color=GREY)
    (motion_trace,) = motion.plot([], [], lw=1.8, color=BLUE)

    curves.set_xlim(drives[0] / OMEGA0, drives[-1] / OMEGA0)
    curves.set_ylim(0.0, 1.15 * amplitude.max())
    curves.set_xlabel(r"$\omega / \omega_0$")
    curves.set_ylabel("|X| (m)", color=BLUE)
    curves.axvline(1.0, color=GREY, lw=0.9, ls=":")
    curves.axvline(peak / OMEGA0, color=GREEN, lw=1.2, ls="--")
    (amplitude_trace,) = curves.plot([], [], lw=1.8, color=BLUE)
    (amplitude_dot,) = curves.plot([], [], marker="o", markersize=6, color=BLUE)

    phase_axis = curves.twinx()
    phase_axis.set_ylim(0.0, np.pi)
    phase_axis.set_yticks([0.0, np.pi / 2.0, np.pi])
    phase_axis.set_yticklabels(["0", "π/2", "π"])
    phase_axis.set_ylabel("lag", color=ORANGE)
    (phase_trace,) = phase_axis.plot([], [], lw=1.4, color=ORANGE)
    (phase_dot,) = phase_axis.plot([], [], marker="o", markersize=5, color=ORANGE)
    fig.tight_layout()

    def update(frame: int):
        omega = drives[frame]
        # The steady state only: this animation is about the response curve, and the transient
        # is module 02's *other* figure. Re[X e^{-i omega t}] = |X| cos(omega t - arg X).
        motion_trace.set_data(window, amplitude[frame] * np.cos(omega * window - lag[frame]))
        drive_trace.set_data(window, 0.35 * amplitude.max() * np.cos(omega * window))
        upto = slice(0, frame + 1)
        amplitude_trace.set_data(drives[upto] / OMEGA0, amplitude[upto])
        amplitude_dot.set_data([omega / OMEGA0], [amplitude[frame]])
        phase_trace.set_data(drives[upto] / OMEGA0, lag[upto])
        phase_dot.set_data([omega / OMEGA0], [lag[frame]])
        return (
            motion_trace,
            drive_trace,
            amplitude_trace,
            amplitude_dot,
            phase_trace,
            phase_dot,
        )

    print(f"[render] sweep at Q = {q:.2f}, peak at {peak / OMEGA0:.4f} omega0")
    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "resonance-sweep")


if __name__ == "__main__":
    render_regimes()
    render_sweep()
