# Part <PP> — <Title> — Implementation Plan

> **Master plan:** §<n> (Part <roman>). **Modules:** `<id-list>`. **Status:** <planned / partial / built>.
> Canonical numbering, invariants, and conflict log: [README.md](README.md).

<!--
This template folds the master plan's §42 twenty-field notebook spec into the repo's
module contract. Every part plan follows this skeleton with these exact top-level
headings. Per-module blocks (§5) repeat once per module. Modules that already exist in
content/ get an "as-built" spec: what the page actually does, plus a gap list.
Formulas must be seeded pre-compliant with the course phase convention — see README
invariant 1 — using the myst.yml macros \ii, \Real, \Imag, \wnat.
-->

## 1. Part overview and narrative arc

3–6 paragraphs. This is the enhancement layer over the master plan: the part's
through-line as a story, why the modules come in this order, what this plan deepens or
adds relative to the master plan's section, which earlier ideas get their payoff here, and
which later modules this part plants seeds for.

## 2. Position in the course

- **Requires:** module ids + the *specific results* assumed (not "knows Fourier" but
  "uses the rect ↔ sinc pair from 04").
- **Feeds:** later module ids + what they consume from here.
- **Explicitly not assumed:** common over-assumptions to keep out of the prose.

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|

Textbook companions by chapter *topic*, never number (editions differ): Georgi / MIT /
French for parts 0–IV, Hecht (+ Griffiths for field derivations) for V–X, Goodman for XI,
Saleh & Teich / Siegman for XII+.

## 4. Shared infrastructure for this part

- **`src/wavelab` — existing used:** which functions from which modules.
- **`src/wavelab` — new:** file(s) this part introduces or extends (must match the README
  ownership table), with a function-level sketch — signature + one-line contract each.
  Include the 7-bullet model-spec docstring header for a new file.
- **`tests/physics/` additions:** one line per test, filed under the six categories
  (conservation / convergence / dimensions / limits / scaling / seeds).
- **Shared media assets** and **glossary themes** for the part.

## 5. Module specifications

### 5.<k> `<NN-slug>` — <Title>

- **Identity and scope** — master-plan notebooks covered; what is deliberately deferred
  and to which module.
- **Prerequisites** — module ids + the specific results used.
- **Learning objectives** — `OBJ-<NN>-1..K`, testable phrasing, ASCII math (these go into
  frontmatter verbatim).
- **Mathematical background** — already has / introduced here.
- **Physical intuition goals** — 2–4 "student can predict without algebra" statements.
- **Section skeleton seeds** — one or two bullets per mandatory section:
  - *puzzle:* the hook phenomenon and the boxed question.
  - *predict:* the 3–4 commit-first questions (at least one targeting a misconception).
  - *explore:* the lab's interactive controls — parameters, ranges, what updates live.
  - *derive:* the derivation route (see core derivations).
  - *verify:* which numerical checks, which becomes a `numerical-observation` admonition.
  - *transfer:* the 3–5 transfer targets (forward/backward module links).
  - *quiz:* themes the quiz bank must cover.
  - *explain:* the in-your-own-words questions.
  - *advanced (optional):* what it contains, and the "safe to skip" boundary.
- **Core derivations** — ordered: starting point → route → result. Key formulas written
  out, convention-compliant.
- **Model specification draft** — the 7 bullets: System / Dynamics / Boundary / Ensemble /
  Ignored / Valid when / Failure modes.
- **Epistemic classification** — the module's key claims, each tagged
  `definition | empirical-law | theorem | model-assumption | approximation |
  numerical-observation | open-question` (at least one admonition is mandatory in the
  page; list which claims get boxes).
- **Misconceptions** — registry ids addressed here (falsifying experiment + quiz
  distractor), and NEW entries as: id · statement · falsifying experiment · distractor.
- **Glossary terms** — key / en / suggested he / `he_reject` candidates.
- **Interactive controls and simulations** — beyond the explore bullets: each simulation,
  its parameters and ranges, what it renders.
- **Virtual lab outline** — `notebooks/en/labs/<NN-slug>.ipynb` cell-by-cell sketch:
  apparatus, measured quantities, synthetic-noise model (via `wavelab.measurement`),
  fit + uncertainty analysis, the "measurement culture" result (value ± error).
- **Real-experiment counterpart** — cheap physical pairing + how data imports into the
  lab notebook (or "none practical" with a sentence why).
- **Media assets** — `media/render/render_<topic>.py`: MP4 shot list, language-neutral
  (no text burned into frames).
- **Quiz bank outline** — `Q-<NN>-1..M`: per question, type (multiple-choice / numeric /
  free), objectives covered, misconception distractor if any. Every `OBJ-<NN>-K` covered
  at least once.
- **Problem set outline** — `<NN-slug>-problems.md`: analytical / computational /
  challenge problems, one-line statements, objective tags.
- **Runtime budget** — JupyterLite/Pyodide cost notes: grid and FFT sizes, animation
  frame counts, target "runs in seconds in the browser".
- **Validation gates** — the per-module commands (README bottom) + anything extra.
- **Open questions for the author** — decisions deliberately left to content-writing time.

## 6. Part-level assessment and capstone hooks

Which §35 capstones this part feeds and with what; cross-module synthesis problems that
belong to the part rather than a single module; exam-style themes.

## 7. Build order and validation gates

Module build order within the part, with one sentence of rationale; the per-module gate
commands; anything that must land in `glossary/terms.yml` or
`assessment/misconceptions.yml` alongside the first module.

## 8. Deviations from the master plan

Explicit log: merges, resequencing, scope changes, terminology changes — one line of
rationale each. Empty section allowed but must be present.
