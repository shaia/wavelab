# WaveLab course plans

This folder is the notebook-by-notebook implementation layer the master plan calls for in
its §42: one detailed plan per curriculum part, converting the curriculum in
`../waves_optics_interactive_course_master_plan.md` into buildable module specifications.
Plans are where content is **enhanced and refined** beyond the master plan — narrative
arcs, cross-module payoffs, misconceptions with falsifying experiments, library sketches —
before any content file is written.

A plan is a *design artifact*, not content: nothing in this folder is linted or deployed.
But every formula seeded here must already obey the course conventions (below) so it can be
pasted into `content/` untouched.

## Files

| File | Master plan | Modules |
|---|---|---|
| `_template.md` | — | the part-plan skeleton all plans follow |
| `part-00-foundations.md` | §7 (Part 0) | 00, 03, 04 |
| `part-01-oscillations.md` | §8 (Part I) | 01, 02, 05 |
| `part-02-normal-modes.md` | §9 (Part II) | 06, 07 |
| `part-03-waves.md` | §10 (Part III) | 08, 09, 10 |
| `part-04-fourier-waves.md` | §11 (Part IV) | 11, 12, 13 |
| `part-05-em-waves.md` | §12 (Part V) | 14, 15, 16 |
| `part-06-interfaces.md` | §13 (Part VI) | 17, 18, 19 |
| `part-07-polarization.md` | §14 (Part VII) | 20, 21, 22 |
| `part-08-interference.md` | §15 (Part VIII) | 23–27 |
| `part-09-diffraction.md` | §16 (Part IX) | 28–32 |
| `part-10-ray-optics.md` | §17 (Part X) | 33–37 |
| `part-11-fourier-optics.md` | §18 (Part XI) | 38–42 |
| `part-12-photonics.md` | §19 (Part XII) | 43–47 |
| `part-13-advanced.md` | §20 (electives) | 50+ |

The `part-PP` prefix is a **curriculum-part** number. Module ids `NN-slug` are a separate,
course-wide counter (below). The two never coincide on purpose — a part number names a
folder of the curriculum, a module id names one content page and its artifact family.

## Canonical module map

Flat course-wide two-digit ids, assigned in teaching order. A module covers one or two
master-plan notebooks (the `X.Y` numbers). Ids are opaque identifiers — the site's teaching
order is set by the TOC in `content/en/myst.yml`, not by filename sort — so the sequence
can be rearranged later without renaming anything. Ids `48–49` are insertion slack;
electives start at `50`.

| Part | `content/en/` dir | Modules (id ← master-plan notebooks) |
|---|---|---|
| 0 Foundations | `foundations/` | `00-phasors` ← 0.1 **(built)** · `03-fourier-series` ← 0.2 **(built)** · `04-fourier-transform` ← 0.3 **(built)** |
| I Oscillations | `oscillations/` | `01-sho` ← 1.1 **(built)** · `02-damped-driven` ← 1.2 + 1.3 **(built)** · `05-impulse-response` ← 1.4 **(built)** |
| II Normal modes | `normal-modes/` | `06-coupled` ← 2.1 · `07-normal-modes` ← 2.2 + 2.3 |
| III Waves | `waves/` | `08-wave-equation` ← 3.1 + 3.2 · `09-wave-energy` ← 3.3 · `10-impedance` ← 3.4 |
| IV Fourier waves | `fourier-waves/` | `11-standing-waves` ← 4.1 + 4.2 · `12-wave-packets` ← 4.3 · `13-dispersion` ← 4.4 |
| V EM waves | `em-waves/` | `14-em-waves` ← 5.1 + 5.2 · `15-em-energy` ← 5.3 · `16-light-in-matter` ← 5.4 |
| VI Interfaces | `interfaces/` | `17-refraction` ← 6.1 · `18-fresnel` ← 6.2 + 6.3 · `19-evanescent` ← 6.4 |
| VII Polarization | `polarization/` | `20-polarization` ← 7.1 + 7.2 · `21-jones-calculus` ← 7.3 · `22-stokes-poincare` ← 7.4 |
| VIII Interference | `interference/` | `23-interference` ← 8.1 + 8.2 · `24-thin-films` ← 8.3 · `25-michelson` ← 8.4 · `26-fabry-perot` ← 8.5 · `27-coherence` ← 8.6 |
| IX Diffraction | `diffraction/` | `28-huygens` ← 9.1 · `29-fraunhofer` ← 9.2 + 9.3 · `30-apertures` ← 9.4 + 9.5 · `31-gratings` ← 9.6 · `32-fresnel-diffraction` ← 9.7 |
| X Ray optics | `ray-optics/` | `33-fermat` ← 10.1 · `34-lenses` ← 10.2 · `35-abcd-matrices` ← 10.3 · `36-instruments` ← 10.4 · `37-aberrations` ← 10.5 |
| XI Fourier optics | `fourier-optics/` | `38-spatial-frequencies` ← 11.1 · `39-fourier-lens` ← 11.2 · `40-psf-otf` ← 11.3 + 11.4 · `41-imaging-coherence` ← 11.5 · `42-4f-processor` ← 11.6 |
| XII Photonics | `photonics/` | `43-gaussian-beams` ← 12.1 + 12.2 · `44-resonators` ← 12.3 · `45-lasers` ← 12.4 · `46-waveguides` ← 12.5 · `47-fibers` ← 12.6 |
| XIII Advanced | `advanced/` | `50-holography` · `51-nonlinear-optics` · `52-quantum-optics` · `53-computational-imaging` · `54-photonic-crystals` · `55-ultrafast` (+ stubs for the remaining §20 topics) |

### Teaching order

Teaching order equals id order: `00 → 01 → 02 → 03 → 04 → 05 → 06 → …`. The deliberate
deviation from the master plan is that the two Fourier modules of Part 0 are taught
**just-in-time inside the oscillations arc** — Fourier series (03) is motivated by the
driven oscillator's periodic forcing (02), and the Fourier transform (04) feeds directly
into impulse response (05). Master plan §31 wants Fourier "before diffraction"; this
sequence honours that with room to spare while giving the mathematics a physical engine.
The full argument lives in `part-00-foundations.md` §8.

## Cross-plan invariants

Every plan (and the content built from it) must respect these; the verification pass
checks them across the folder.

1. **Phase convention** (`src/wavelab/constants.py`, `content/en/conventions.md`): phasor
   $A e^{-\ii\varphi}$, time factor $e^{-\ii\omega t}$, travelling wave
   $\psi = \Real[A\,e^{\ii(kx-\omega t)}]$, complex index $n + \ii\kappa$. The content lint
   rejects $e^{j(\omega t - kx)}$ and $n - \ii\kappa$; legitimate exceptions carry
   `<!-- sign-convention-exception -->`. Plans seed formulas pre-compliant, using the
   project math macros `\ii`, `\Real`, `\Imag`, `\wnat` (defined in `content/en/myst.yml`).
2. **Module contract** (`scripts/check_modelspec.py`): section order
   `puzzle → predict → explore → derive → verify → transfer → quiz → explain`
   (+ optional trailing `advanced`), each labelled `(NN-slug-<suffix>)=`; a
   7-bullet Model specification (System / Dynamics / Boundary / Ensemble / Ignored /
   Valid when / Failure modes); at least one epistemic admonition
   (`definition`, `empirical-law`, `theorem`, `model-assumption`, `approximation`,
   `numerical-observation`, `open-question`); frontmatter objectives `OBJ-NN-K` with
   ASCII math in their text.
3. **Notebooks never re-implement physics.** All physics lives in `src/wavelab/`; labs and
   render scripts orchestrate it. Each library function is specified in exactly **one**
   plan's §4 (single-owner rule; ownership table below).
4. **Glossary is the sole EN↔HE terminology source** (`glossary/terms.yml`). Plans list
   new terms as key / en / suggested he / `he_reject` candidates; suggested Hebrew is a
   *proposal* for the translator, never applied directly.
5. **Misconception registry** (`assessment/misconceptions.yml`) entries are design
   requirements: the assigned module must stage a falsifying experiment and a quiz
   distractor built on the wrong model. Plans may add entries; every pending entry's
   `assigned_module` already names the module that will address it (conflict log below).
6. **Artifact family per module** (join key `NN-slug`): content page + `-problems.md`,
   quiz banks `assessment/quizzes/NN-slug.{en,he}.yml` (every objective covered, per-choice
   feedback), lab `notebooks/{en,he}/labs/NN-slug.ipynb`, quiz JSON
   `notebooks/{en,he}/_quiz/NN-slug.json`, media `media/render/render_<topic>.py`, HE
   mirror page with `en_source_hash`, glossary entries.

## `src/wavelab/` ownership

Existing: `constants`, `units`, `phasors` (module 00), `fourier` (03–04), `oscillators` (01–02, 05 — extended by
02 with `steady_state_response`, `resonance_peak_omega`, `power_absorbed` and the three
`q_from_*` estimators, and by 05 with `impulse_response`, `step_response`,
`convolution_response` and a fourth estimator `q_from_linewidth`),
`measurement` (shared: noise, fitting, uncertainty), `validation` (shared: conservation /
analytic-limit / convergence / seed checks).

| New file | Introduced by | Extended by | Serves modules |
|---|---|---|---|
| `fourier.py` | part-00 | — | 03, 04 — and every later FFT-using lab **(built)** |
| `coupled.py` | part-02 | — | 06, 07 |
| `waves.py` | part-03 | part-04 | 08–13 |
| `em.py` | part-05 | — | 14–16 |
| `interfaces.py` | part-06 | — | 17–19 |
| `polarization.py` | part-07 | — | 20–22 |
| `interference.py` | part-08 | — | 23–27 (incl. thin-film reflectance → colour pipeline) |
| `diffraction.py` | part-09 | — | 28–32 (FFT Fraunhofer + angular-spectrum propagator) |
| `rayoptics.py` | part-10 | — | 33–37 |
| `imaging.py` | part-11 | — | 38–42 |
| `gaussian.py` | part-12 | — | 43, 44 |
| `photonics.py` | part-12 | — | 45–47 |

"Introduced by" owns the file's docstring model spec; "extended by" plans spec only their
own additional functions. A function referenced by several plans is *defined* (signature +
contract) in exactly one.

One cross-part extension has happened so far: part-00 added `oscillators.simulate_forced`
(a sampled arbitrary drive) to part-01's file, because module 03 has to check its harmonic-sum
prediction against an integration that knows nothing about harmonics and `simulate` drives with
a cosine only. Recorded in `part-00-foundations.md` §5.4.

## Conflict log

Inconsistencies between the master plan, the repo, and this map, with the resolution
applied to each. All three groups below are **resolved in the files** — this log is the
record of what changed and why, not a to-do list.

**Registry `assigned_module` re-pointings** — applied to `assessment/misconceptions.yml`.
The pending entries had been forward-declared against module ids that this map never
assigns; each now names the module whose plan actually stages its falsifying experiment.
`status` stays `pending` until that module is built.

| Misconception id | Was | Now |
|---|---|---|
| `resonance-peak-at-omega0` | `02-damped-driven` | unchanged — module built, now `addressed` |
| `wave-carries-medium` | `04-waves` | `08-wave-equation` |
| `packet-at-phase-velocity` | `05-fourier` | `12-wave-packets` |
| `frequency-changes-in-medium` | `06-em-waves` | `16-light-in-matter` |
| `third-polarizer-only-dims` | `07-polarization` | `20-polarization` |
| `interference-destroys-energy` | `08-interference` | `23-interference` |
| `narrow-slit-narrow-pattern` | `09-diffraction` | `29-fraunhofer` |

**Prose drift in built modules** — applied to the content pages in both languages, with
`en_source_hash` re-stamped for the three affected Hebrew mirrors. Forward references are
plain prose (`module 23`), not links: the targets do not exist yet, and a link would break
the build. Convert them to links as each module lands.

| Page | Was | Now |
|---|---|---|
| `00-phasors.md` | module 8 (interference law, energy bookkeeping) | module 23 |
| `00-phasors.md` | module 8 (coherence bullet) | module 27 |
| `00-phasors.md` | module 9 (diffraction bullet) | module 29 |
| `00-phasors.md` | module 1.3 (driven oscillator) | module 02 |
| `00-phasors-problems.md` | module 8 (speckle) | module 41 |
| `00-phasors-problems.md` | module 9 (grating) | module 31 |
| `01-sho.md` | module 02 (coupled oscillators) | module 06 |
| `01-sho.md` | modules 02–03 (normal modes) | modules 06–07 |
| `01-sho.md` | module 20 (nonlinear optics) | module 51 |

The last two rows of `00-phasors-problems.md` were not in the original log — speckle
belongs to `41-imaging-coherence` and the phasor-polygon problem anticipates
`31-gratings`, not the generic "diffraction" module. `00-phasors.md`'s "module 04"
reference was already correct.

**Master-plan internal inconsistencies** — applied to
`../waves_optics_interactive_course_master_plan.md`:

- §6's part table contradicted the document's own section headings from Part V onward
  (it merged electromagnetic waves with interfaces, shifting every later part by one).
  The table now matches the headings, which are canonical.
- §6 estimated "35–45 notebooks" while §7–§19 enumerate 60. The table now carries the
  real per-part counts, summing to 60, and the surrounding prose states the 48-core-module
  grouping (a module covers one or two notebooks; precedent: `02-damped-driven` ← 1.2 + 1.3).
- §33's proposed repository layout (`00_foundations/`, `waves_optics/`) never matched the
  built repo. It now documents the actual `physics_lab/wavelab/` tree with the hyphenated
  part directories this map uses.

**Cross-plan glossary-key ownership** (verification pass; owner = earliest depositing
module in teaching order, all other plans cite):

- `bandwidth` → `02-damped-driven` (04 cites).
- `dispersion-relation` → `07-normal-modes` (13 cites; 13 still deposits `dispersion`).
- `wavefront` → `14-em-waves` (17, 28 cite; part-03 never deposited it).
- `optical-path-length` → `23-interference` (33 cites).
- `numerical-aperture` → `36-instruments` (39 and 47 cite and extend the same key).
- `adaptive-optics` → `37-aberrations` (53 cites).
- `chirp` → `13-dispersion` (55 cites).
- Part-13's nonlinear key renamed `nonlinear-phase-matching` — a concept distinct from
  `17-refraction`'s kinematic `phase-matching`; both keys stand.

## Status

| Part | Plan | Modules built |
|---|---|---|
| 00 Foundations | written | `00-phasors`, `03-fourier-series`, `04-fourier-transform` — **complete** |
| 01 Oscillations | written | `01-sho`, `02-damped-driven`, `05-impulse-response` — **complete** |
| 02 Normal modes | written | — |
| 03 Waves | written | — |
| 04 Fourier waves | written | — |
| 05 EM waves | written | — |
| 06 Interfaces | written | — |
| 07 Polarization | written | — |
| 08 Interference | written | — |
| 09 Diffraction | written | — |
| 10 Ray optics | written | — |
| 11 Fourier optics | written | — |
| 12 Photonics | written | — |
| 13 Advanced | written | — |

## Validation gates (per module, when built)

```sh
uv run python scripts/check_modelspec.py --module <NN-slug>
uv run python scripts/check_assessment.py --module <NN-slug>
uv run pytest tests/physics -k <topic>
uv run python scripts/validate_all.py   # full gate before merge
```
