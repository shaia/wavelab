"""Render the demonstration animations for module 00 (orientation).

Animations are produced from `thermolab` itself, so what a student watches is the same model
they can read, run and test — never a hand-drawn impression of it.

Output is MP4, written by `_common.save`; see that module for why, and for the constraints the
format brings. The animations carry no words, so the same file serves both language sites; the
caption that explains each one is ordinary translated page prose rather than a subtitle track
that could silently drift from the text around it.

Deliberately absent: any histogram, density curve or fitted bell. This module derives how
*wide* the scatter of an average is and says nothing about its shape — the shape is module 3's
result, and drawing it here would give the answer away before the argument exists.

Run:  uv run python media/render/render_orientation.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, save  # noqa: E402
from thermolab import sampling  # noqa: E402

BLUE = "#2563eb"
RED = "crimson"


def render_running_average(n_rolls: int = 600) -> None:
    """Individual rolls beside the running average of the same sequence.

    The pairing is the whole module in one picture, and it is deliberately built like
    `pressure-impacts.gif`: the left panel never settles, the right panel does. Module 4 will
    show the identical contrast with molecules instead of dice.
    """
    rng = np.random.default_rng(20)
    rolls = sampling.roll_dice(n_rolls, rng)
    curve = sampling.running_average(rolls)
    trials = np.arange(1, n_rolls + 1)
    mean = sampling.die_mean()

    fig, (left, right) = plt.subplots(1, 2, figsize=(8.5, 3.6), dpi=DPI)

    dots = left.scatter([], [], s=16, color=BLUE, alpha=0.65)
    left.axhline(mean, color=RED, ls="--", lw=1.2)
    left.set_xlim(0, n_rolls)
    left.set_ylim(0.3, 6.7)
    left.set_yticks(range(1, 7))
    left.set_xlabel("roll number")
    left.set_ylabel("face shown")

    (trace,) = right.plot([], [], lw=1.4, color=BLUE)
    right.axhline(mean, color=RED, ls="--", lw=1.2)
    right.set_xlim(0, n_rolls)
    right.set_ylim(1.0, 6.0)
    right.set_xlabel("rolls averaged, $N$")
    right.set_ylabel("average so far")
    fig.tight_layout()

    def update(frame: int):
        k = frame + 1
        dots.set_offsets(np.column_stack((trials[:k], rolls[:k])))
        trace.set_data(trials[:k], curve[:k])
        return dots, trace

    save(FuncAnimation(fig, update, frames=n_rolls, blit=False), fig, "running-average")
    plt.close(fig)


def render_spread_shrinks(n_experiments: int = 240) -> None:
    """The same experiment repeated at three values of N, one dot per completed experiment.

    Each dot is one finished "average N dice" experiment, so the vertical extent of a column
    of dots *is* the reproducibility of a single measurement. Shown on a shared axis, the
    three columns narrow visibly — the N^(-1/2) law before any algebra.
    """
    rng = np.random.default_rng(7)
    sizes = (10, 100, 1000)
    columns = [sampling.sample_averages(n, n_experiments, rng) for n in sizes]
    mean = sampling.die_mean()
    trials = np.arange(1, n_experiments + 1)

    fig, axes = plt.subplots(1, 3, figsize=(9.5, 3.2), dpi=DPI, sharey=True)
    clouds = []
    for ax, n_per_sample in zip(axes, sizes, strict=True):
        cloud = ax.scatter([], [], s=12, color=BLUE, alpha=0.6)
        ax.axhline(mean, color=RED, ls="--", lw=1.1)
        ax.set_xlim(0, n_experiments)
        ax.set_ylim(2.3, 4.7)
        ax.set_title(f"$N = {n_per_sample}$")
        ax.set_xlabel("experiment number")
        clouds.append(cloud)
    axes[0].set_ylabel("average of $N$ dice")
    fig.tight_layout()

    def update(frame: int):
        k = frame + 1
        for cloud, averages in zip(clouds, columns, strict=True):
            cloud.set_offsets(np.column_stack((trials[:k], averages[:k])))
        return clouds

    save(
        FuncAnimation(fig, update, frames=n_experiments, blit=False),
        fig,
        "spread-shrinks",
    )
    plt.close(fig)


def main() -> None:
    render_running_average()
    render_spread_shrinks()


if __name__ == "__main__":
    main()
