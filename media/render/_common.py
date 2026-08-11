"""Shared output plumbing for the demonstration renderers.

Every `render_<module>.py` builds a `FuncAnimation` from `thermolab` and hands it to `save()`
here. Before this module existed the same twenty lines were copy-pasted into all four scripts;
the MP4 writer needs enough setup that a fifth copy was not worth having.

WHY MP4 AND NOT GIF
    mystmd renders a `.mp4` in a `{figure}` directive through the book theme's own React
    component, which emits `<video autoplay muted loop playsinline>` — autoplaying, looping,
    no controls. That is byte-for-byte the playback a GIF gave us, at roughly a tenth of the
    size and in full colour instead of a 256-entry palette (the old GIFs were using 248-250 of
    those 256 entries, so line art and text were visibly quantized).

    Two constraints come with it. `.webm` is not supported by mystmd at all — the theme tests a
    literal `.endsWith(".mp4")` — and the theme drops the figure's `:alt:` text for video, so
    the descriptive wording lives in the visible caption instead.

WHY FFMPEG IS A DEV DEPENDENCY
    `imageio-ffmpeg` ships a static ffmpeg binary, so nothing has to be installed system-wide.
    It belongs in the `dev` group and must stay there: rendering happens at authoring time on
    this machine, never in the browser. Nothing under `src/thermolab/` or in any notebook
    imports `matplotlib.animation`, so Pyodide/JupyterLite never needs ffmpeg. Do not "fix"
    this by promoting the dependency.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.figure import Figure

ROOT = Path(__file__).resolve().parents[2]
LANGUAGES = ("en", "he")
SUFFIX = ".mp4"

# Playback and quality. FPS is 30 rather than the GIF era's 20 because particle motion reads as
# choppy below it; DPI is 150 so axis labels stay crisp on a high-density display. Note that
# raising FPS alone *shortens* an animation — frame counts in the render scripts are sized to
# these values, so changing one here means revisiting them.
FPS = 30
DPI = 150

# -tune animation is x264's preset for synthetic/flat-shaded content, which is exactly what a
# matplotlib figure is; measured on the hardest of these animations it saves ~6% over no tuning.
# crf 23 is x264's default and visually transparent for flat-shaded plots — crf 20 cost 15% more
# bytes for no visible gain. faststart moves the index to the front so playback can begin before
# the file has fully downloaded.
ENCODER_ARGS = ["-crf", "23", "-preset", "slow", "-tune", "animation", "-movflags", "+faststart"]


def ffmpeg_path() -> str:
    """The ffmpeg binary to encode with — the pinned wheel first, a system install second."""
    try:
        import imageio_ffmpeg
    except ImportError:
        pass
    else:
        return imageio_ffmpeg.get_ffmpeg_exe()

    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg

    raise RuntimeError(
        "No ffmpeg available. Install the pinned build with "
        "`uv add --group dev imageio-ffmpeg`, or put ffmpeg on PATH."
    )


def output_paths(name: str) -> list[Path]:
    """The same file in each language project — MyST resolves images inside its own tree."""
    return [ROOT / "content" / lang / "media" / f"{name}{SUFFIX}" for lang in LANGUAGES]


def snap_to_even_pixels(figure: Figure) -> None:
    """Grow the figure by at most a pixel each way so both dimensions are even.

    matplotlib forces `-pix_fmt yuv420p` for h264, and that pixel format cannot represent an odd
    width or height — chroma is subsampled 2x2. Five of this project's eight animations were
    odd-width under the old GIF settings (935 and 1045 px), so without this they simply fail to
    encode. Adjusting the figure is better than an ffmpeg `scale` filter, which would resample
    every frame to fix one pixel.
    """
    dpi = figure.dpi
    for _ in range(2):
        width, height = figure.canvas.get_width_height()
        if width % 2 == 0 and height % 2 == 0:
            return
        figure.set_size_inches(
            (width + width % 2) / dpi, (height + height % 2) / dpi, forward=True
        )
    width, height = figure.canvas.get_width_height()
    if width % 2 or height % 2:
        raise RuntimeError(f"could not reach even frame dimensions: {width}x{height}")


def save(animation: FuncAnimation, figure: Figure, name: str, fps: int = FPS) -> None:
    """Encode `animation` once and place an identical copy in every language tree.

    `figure` is passed explicitly rather than read off `animation._fig`, which is private API.
    """
    snap_to_even_pixels(figure)
    # FFMpegWriter.bin_path() reads this rcParam; setting it is the documented way to point
    # matplotlib at a specific binary, and it is idempotent.
    matplotlib.rcParams["animation.ffmpeg_path"] = ffmpeg_path()
    writer = FFMpegWriter(fps=fps, codec="h264", extra_args=ENCODER_ARGS)

    targets = output_paths(name)
    first = targets[0]
    first.parent.mkdir(parents=True, exist_ok=True)
    animation.save(first, writer=writer)
    for other in targets[1:]:
        other.parent.mkdir(parents=True, exist_ok=True)
        other.write_bytes(first.read_bytes())

    size_kb = first.stat().st_size / 1024
    listed = ", ".join(str(p.relative_to(ROOT)) for p in targets)
    print(f"[render] {name}{SUFFIX} ({size_kb:.0f} KB) -> {listed}")
