"""Lab-notebook lint: the JupyterLite bootstrap cell no other check can see.

Every notebook under `notebooks/<lang>/labs/` runs in two places. On this machine `wavelab`
and its dependencies are already importable, so the bootstrap cell does nothing and nbmake is
green whatever it contains. In the browser that cell is the only thing that puts the course
package and the pure-Python libraries into the Pyodide kernel — and if it is wrong, the
laboratory is dead for every student while the whole local pipeline still passes.

That asymmetry is why this file exists. It has already caught the real thing: a notebook whose
bootstrap was typed from memory rather than copied installed `wavelab` *with* its dependency
graph, which sends micropip to PyPI for NumPy and matplotlib, neither of which has a
WebAssembly wheel.

The opposite mistake shipped in every laboratory before this file looked for it: with the
dependency graph switched off, nothing asked for SciPy at all. The kernel loads a Pyodide
package unprompted only when the text of the cell being run imports it. A notebook's own
`import numpy` is seen; the `import scipy` inside `wavelab.measurement` is not, so
`from wavelab import ...` died in the browser with "No module named 'scipy'" while nbmake
stayed green.

The check is on *requirements*, not on bytes. Comparing against `00-phasors.ipynb` verbatim
would fail on a reformat and would have to be rewritten every time a dependency is added; what
actually matters is that every dependency of `wavelab` is requested by name, the compiled ones
Pyodide ships and the pure-Python ones it does not, and that `wavelab` itself is installed
without its dependency graph.

Run standalone (`python scripts/check_notebooks.py`) or import `check()`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _findings import Finding, report  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

# Compiled packages `wavelab` imports. Pyodide ships them but loads one only when the text of
# the cell being run imports it, and it cannot see imports inside `wavelab`. matplotlib is not
# listed because `wavelab` never imports it; the notebooks that plot import it themselves.
REQUIRED_FROM_PYODIDE = ("numpy", "scipy")

# Pure-Python packages Pyodide does not ship. `wavelab` itself is handled separately,
# because the thing that matters about it is the absence of its dependency graph.
REQUIRED_PURE_PYTHON = ("pint", "ipywidgets", "jupyterquiz")
PACKAGE = "wavelab"


def iter_lab_notebooks(root: Path) -> list[Path]:
    """Every authored laboratory notebook, in both languages."""
    notebooks: list[Path] = []
    for lang in ("en", "he"):
        labs = root / "notebooks" / lang / "labs"
        if not labs.exists():
            continue
        notebooks.extend(
            sorted(p for p in labs.rglob("*.ipynb") if ".ipynb_checkpoints" not in p.parts)
        )
    return notebooks


def first_code_cell(notebook: dict) -> str | None:
    for cell in notebook.get("cells") or []:
        if cell.get("cell_type") == "code":
            return "".join(cell.get("source") or [])
    return None


def check_bootstrap(path: Path, source: str | None) -> list[Finding]:
    if source is None:
        return [Finding(path, None, "error", "notebook has no code cells")]

    if "piplite" not in source:
        return [
            Finding(
                path,
                None,
                "error",
                "first code cell is not the JupyterLite bootstrap — copy it from "
                "notebooks/en/labs/00-phasors.ipynb (cell id 'piplite-bootstrap'); "
                "nbmake cannot see this, but the browser can",
            )
        ]

    findings: list[Finding] = []

    unrequested = [name for name in REQUIRED_FROM_PYODIDE if f'"{name}"' not in source]
    if unrequested:
        findings.append(
            Finding(
                path,
                None,
                "error",
                f"bootstrap does not request {', '.join(unrequested)} — Pyodide loads a package "
                "only when the running cell's own text imports it, so the imports inside "
                f"{PACKAGE} fail in the browser with ModuleNotFoundError",
            )
        )

    missing = [name for name in REQUIRED_PURE_PYTHON if f'"{name}"' not in source]
    if missing:
        findings.append(
            Finding(
                path,
                None,
                "error",
                f"bootstrap does not install {', '.join(missing)} — Pyodide does not ship "
                f"{'them' if len(missing) > 1 else 'it'}, so the notebook dies in the browser",
            )
        )

    if "deps=False" not in source:
        findings.append(
            Finding(
                path,
                None,
                "error",
                f"bootstrap must install {PACKAGE} with deps=False; installing its dependency "
                "graph sends micropip to PyPI for NumPy/SciPy/matplotlib, which have no "
                "WebAssembly wheels",
            )
        )

    return findings


def check(root: Path = ROOT) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_lab_notebooks(root):
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(Finding(path, None, "error", f"unreadable notebook: {exc}"))
            continue
        findings.extend(check_bootstrap(path, first_code_cell(notebook)))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)
    findings = check()
    return report(findings, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
