# ThermoLab — Explore, Derive and Simulate Thermal Physics

An interactive, bilingual (English / עברית) computational textbook and virtual laboratory for
university-level thermal and statistical physics. Not a tutorial: a full learning environment
meant to take a student from zero to exam-ready at the level of leading university courses,
at the depth of a good book on the subject — plus everything interactive computing adds:
live simulations, laboratories, quizzes, exams and demonstration videos.

The guiding question, everywhere:

> **How does predictable macroscopic behaviour emerge from uncertain microscopic behaviour?**

## What's here

| Piece | Where | What it is |
| --- | --- | --- |
| Course text (EN) | `content/en/` | MyST Markdown site — the source of truth |
| Course text (HE) | `content/he/` | Full Hebrew mirror (RTL), kept in lockstep by tooling |
| Laboratories | `notebooks/{en,he}/labs/` | Interactive Jupyter notebooks (ipywidgets) |
| Physics engine | `src/thermolab/` | Plain, readable, vectorized NumPy — every model the course uses |
| Assessment | `assessment/` | Quiz banks (YAML, bilingual), exam-style problems, misconception registry |
| Animations | `media/render/` → `content/*/media/` | Simulation-rendered MP4 demonstrations, language-neutral, embedded in both site copies |
| Validation | `tests/`, `scripts/` | The scientific-accuracy framework, mechanized (see below) |
| Instructor material | `instructor/` | Worked solutions and marking rubrics — never deployed |

## Quickstart

Requirements: [uv](https://docs.astral.sh/uv/) and Node.js ≥ 18.

```powershell
uv sync                                   # Python 3.12 env with all deps
npm install                               # mystmd (site builder)

uv run pytest                             # physics test suite
uv run python scripts/validate_all.py     # every validation layer
.\build.ps1 -Serve                        # complete build -> _site/, then serve it
                                          # (bash: ./build.sh --serve)

uv run jupyter lab                        # work with the lab notebooks
```

`build.ps1` (PowerShell) and `build.sh` (bash) are the same wrapper and take the same options
under each shell's spelling. Either one runs every generation step in order — stylesheets,
quizzes, animations, both MyST projects, then the JupyterLite app — and reports a per-stage
summary. Useful flags: `-NoMedia` / `--no-media` (skip the slow animation render),
`-NoLite` / `--no-lite`, `-Port <n>` / `--port <n>`.

The interactive laboratories are served from `_site/lite/`, so they only work in a build of
the whole site. `npx myst start` previews a single language and has no `/lite` route: the
laboratory links on module pages return "Document Not Found" there by design.

## Publishing

`.github/workflows/pages.yml` publishes the site to GitHub Pages on every push to `master`;
pull requests run the same build and validation without deploying. Nothing is committed by the
workflow — the whole site is rebuilt from source each time, because the animations, the
generated quiz includes and the JupyterLite bundle are all gitignored.

The site is served under a path prefix on a project Pages site
(`https://<user>.github.io/<repo>/`). `actions/configure-pages` reports that prefix and the
workflow passes it to the build, which turns it into `BASE_URL=<prefix>/<lang>` for each MyST
project. Reproduce the deployed layout locally with `.\build.ps1 -BasePath /<repo>`
(`./build.sh --base-path /<repo>`) — note the result must then be served *from* that path, not
from the root. Moving to a custom domain later needs no change here: the reported prefix
becomes `/` and the build falls back to root-relative output.

Two things make the browser laboratories work once published, and both are easy to break:

- Pyodide has no access to this repository, so `scripts/build_site.py` builds the `thermolab`
  wheel into `dist/` and JupyterLite's `PipliteAddon` indexes it into the bundle. The first
  cell of every laboratory notebook installs it — with `deps=False`, because Pyodide supplies
  its own older builds of NumPy, SciPy and matplotlib. The wheel's `requires-python` upper
  bound must admit the CPython that Pyodide runs (3.14 today).
- MyST rewrites the `/lite/…` laboratory links into `<prefix>/<lang>/lite/…`, where no bundle
  exists. The build writes a relative redirect at that address rather than duplicating the
  70 MB bundle per language. `verify_lite` fails the build if a laboratory link, its notebook
  or the wheel is missing, so neither can regress silently.

One-time setup on a fresh fork: repo Settings → Pages → Source = **GitHub Actions**.

Other tools you will reach for while authoring:

```powershell
uv run python scripts/render_quizzes.py   # quiz banks -> site pages + notebook JSON
uv run python scripts/sync_notebooks.py   # copy EN code cells into the HE notebooks
uv run python scripts/stamp_hashes.py     # mark a finished translation as up to date
uv run python media/render/render_pressure.py   # regenerate a module's animations
```

On Windows, `uv` may not be on PATH; call it as `& "$env:USERPROFILE\.local\bin\uv.exe"`.

Live-preview a single language while writing: `cd content/en && npx myst start`.

## Quality: the scientific-accuracy framework

Every module passes six automated physics-test categories (dimensional consistency,
conservation, analytic limits, large-N scaling, numerical convergence, seed independence),
notebook execution in both languages, content lint (structure, model-spec blocks, fixed sign
convention `dU = δQ + δW_on`, epistemic labeling), assessment lint (answer keys, objective and
misconception coverage), and EN↔HE parity (tree, equation identity, notebook code-cell
identity, glossary consistency) — plus a human/assisted review pass. See `.claude/CLAUDE.md`
for the full conventions.

## Bilingual design

English is the authoring language; Hebrew is a first-class mirror, not an afterthought:
per-file `en_source_hash` staleness tracking, a canonical physics glossary
(`glossary/terms.yml`), byte-identical equations and code cells across languages, and an
RTL-aware build. `translation-pending.txt` must be empty for any release.

## Course map

Module 0 (orientation & prerequisites from zero) → 12 core modules (equilibrium, equations of
state, probability, kinetic theory, first law, processes, second law, entropy, fundamental
relation, potentials, ensembles, partition functions) → 6 advanced modules (chemical potential,
phase equilibrium, phase transitions, radiation & solids, quantum statistics, fluctuations &
transport). Currently built: orientation, the microscopic origin of pressure, work &
thermodynamic paths, and entropy & multiplicity — plus two reference pages, the course
conventions and a mathematics refresher.
