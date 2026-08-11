"""Render the demonstration animations for module 05 (work and thermodynamic paths).

Same approach as the module 04 renderer: animations come from `thermolab` itself, are written as
MP4 by `_common.save`, and contain no words, so one file serves both language sites and the
explanation stays in translated page prose.

Run:  uv run python media/render/render_paths.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, save  # noqa: E402
from thermolab import paths  # noqa: E402

N_PARTICLES = 1000
TEMPERATURE = 300.0
V1, V2 = 1.0e-3, 2.0e-3
P1 = paths.ideal_gas_pressure(N_PARTICLES, TEMPERATURE, V1)
P2 = paths.ideal_gas_pressure(N_PARTICLES, TEMPERATURE, V2)


def render_two_routes(n_frames: int = 180) -> None:
    """Two routes traced out side by side, with the accumulating work shown as it grows.

    Both journeys start and finish at the same points, and the running totals separate as they
    go — which is the module's whole argument, made without a word of text.
    """
    isotherm = paths.isothermal_path(N_PARTICLES, TEMPERATURE, V1, V2, n_points=n_frames)
    two_leg = paths.join(
        paths.isobaric_path(P1, V1, V2, n_points=n_frames // 2),
        paths.isochoric_path(V2, P1, P2, n_points=n_frames // 2 + 1),
    )

    def partial_work(route: paths.Path, fraction: float) -> float:
        """Work accumulated along the first `fraction` of a route's sample points."""
        cut = max(2, int(fraction * route.volumes.size))
        return paths.work_on_gas(route.volumes[:cut], route.pressures[:cut])

    routes = [(isotherm, "#2563eb"), (two_leg, "#d97706")]
    fractions = np.linspace(0.02, 1.0, n_frames)
    works = [[partial_work(route, f) for f in fractions] for route, _ in routes]

    fig, (plane, bars) = plt.subplots(1, 2, figsize=(9, 3.8), dpi=DPI)

    plane.plot([V1 * 1e3, V2 * 1e3], [P1, P2], "ko", ms=7, zorder=5)
    plane.set_xlim(0.9 * V1 * 1e3, 1.05 * V2 * 1e3)
    plane.set_ylim(0, 1.15 * P1)
    plane.set_xlabel("volume (L)")
    plane.set_ylabel("pressure (Pa)")
    curves = [plane.plot([], [], lw=2.2, color=colour)[0] for _, colour in routes]

    bars.set_xlim(-0.6, 1.6)
    bars.set_ylim(min(min(w) for w in works) * 1.15, 0)
    bars.set_xticks([0, 1])
    bars.set_xticklabels(["", ""])
    bars.set_ylabel("work done on the gas (J)")
    rectangles = bars.bar([0, 1], [0, 0], width=0.55, color=[c for _, c in routes])

    fig.tight_layout()

    def update(frame: int):
        for curve, (route, _) in zip(curves, routes, strict=True):
            cut = max(2, int(fractions[frame] * route.volumes.size))
            curve.set_data(route.volumes[:cut] * 1e3, route.pressures[:cut])
        for rectangle, series in zip(rectangles, works, strict=True):
            rectangle.set_height(series[frame])
        return [*curves, *rectangles]

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "paths-two-routes")
    plt.close(fig)


def render_cycle(n_frames: int = 180) -> None:
    """A rectangular cycle traced repeatedly, with the enclosed area filling in.

    The state returns to where it began every lap; the shaded area does not vanish. That gap
    is the net work, and it is what an engine sells.
    """
    cycle = paths.join(
        paths.isobaric_path(P1, V1, V2, n_points=n_frames // 4),
        paths.isochoric_path(V2, P1, P2, n_points=n_frames // 4 + 1),
        paths.isobaric_path(P2, V2, V1, n_points=n_frames // 4 + 1),
        paths.isochoric_path(V1, P2, P1, n_points=n_frames // 4 + 1),
    )

    fig, ax = plt.subplots(figsize=(5.2, 4.0), dpi=DPI)
    ax.set_xlim(0.9 * V1 * 1e3, 1.08 * V2 * 1e3)
    ax.set_ylim(0.85 * P2, 1.12 * P1)
    ax.set_xlabel("volume (L)")
    ax.set_ylabel("pressure (Pa)")
    (curve,) = ax.plot([], [], lw=2.2, color="#7c3aed")
    (marker,) = ax.plot([], [], "o", ms=9, color="#4c1d95")
    shading = [ax.fill_between([], [], alpha=0.0)]
    fig.tight_layout()

    total = cycle.volumes.size
    steps = np.linspace(2, total, n_frames).astype(int)

    def update(frame: int):
        cut = steps[frame]
        volumes, pressures = cycle.volumes[:cut], cycle.pressures[:cut]
        curve.set_data(volumes * 1e3, pressures)
        marker.set_data([volumes[-1] * 1e3], [pressures[-1]])
        shading[0].remove()
        shading[0] = ax.fill(volumes * 1e3, pressures, alpha=0.18, color="#7c3aed")[0]
        return curve, marker, shading[0]

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "paths-cycle")
    plt.close(fig)


def main() -> None:
    render_two_routes()
    render_cycle()


if __name__ == "__main__":
    main()
