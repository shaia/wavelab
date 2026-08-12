# Part VII — Polarization — Implementation Plan

> **Master plan:** §14 (Part VII) + §28 (worked example: Hecht polarization as an interactive sequence). **Modules:** `20-polarization`, `21-jones-calculus`, `22-stokes-poincare`. **Status:** planned.
> Canonical numbering, invariants, and conflict log: [README.md](README.md).

## 1. Part overview and narrative arc

Part VII is where the **vector nature of light finally matters**. Everything so far —
strings, sound, even Part V's EM waves once transversality was established — treated the
wave as one number per point. Now the transverse plane opens up: the E-field is an arrow,
the arrow has a life of its own (linear, circular, elliptical), and that life is a new
physical degree of freedom with its own devices, algebra, and measurements. The
through-line: **the polarization state is a vector, optical elements are operators on it,
and measurement is projection** — the course's gentlest introduction to state-vector
thinking.

Module 20 builds the state. Two transverse components and a relative phase — $E_x$,
$E_y$, $\delta$ — and the tip of the real E-vector traces a Lissajous figure in the
transverse plane: the polarization ellipse. A polarizer is the simplest possible
measurement, Malus' law falls out of pure projection, and the centerpiece is the
**three-polarizer paradox**: crossed polarizers pass nothing, yet a *third* absorbing
element inserted between them at 45° brings the light back at $I_0/8$. That is registry
misconception `third-polarizer-only-dims`, claimed here — measurement-as-projection made
vivid, with the sequential Stern–Gerlach analogy as an advanced aside.

Module 21 is, and says out loud that it is, **the course's first operator formalism**:
states are 2-component complex vectors, elements are $2\times 2$ matrices, cascades are
ordered products, and order *matters* — non-commutativity is demonstrated on the bench,
not asserted. Waveplates are derived from birefringence
($\Gamma = 2\pi\,\Delta n\, d/\lambda_0$), and master plan §28's virtual bench — laser →
polarizer → QWP → HWP → analyzer → detector — is the laboratory's centerpiece, run in
predict-then-measure mode stage by stage. The same grammar returns as ABCD matrices for
rays (`35-abcd-matrices`) and, unchanged, as single-qubit gates (`52-quantum-optics`).

Module 22 confronts the formalism with its failure: **sunlight has no Jones vector** — a
single perfectly-defined field is always fully polarized. The repair is operational: four
Stokes parameters defined by six intensity measurements, a degree of polarization $p$,
and the Poincaré sphere — pure states on the surface, partial ones inside, waveplates as
rotations. The second deep lesson in state-thinking: when a description fails, enlarge
the state space and define the new one by what you can *measure*.

Seeds are planted deliberately: drifting-$\delta$ natural light is the embryo of
coherence (`27-coherence`), the operator grammar returns twice (35, 52), birefringent
colour feeds the thin-film colour pipeline (`24-thin-films`), Brewster glare links back
to `18-fresnel`. Relative to master plan §14 this plan merges 7.1+7.2, pins the
handedness convention §14 leaves silent (a notorious sign trap), elevates 7.4 from
"advanced extension" to a full advanced-track module, and confines the quantum
foreshadowing to clearly-bounded advanced boxes.

## 2. Position in the course

- **Requires:**
  - `14-em-waves`: plane waves $\mathbf{E} = \Real[\mathbf{E}_0 e^{\ii(kz-\omega t)}]$,
    transversality $\mathbf{E}\perp\mathbf{k}$, $\mathbf{B}$ slaved to $\mathbf{E}$ — the
    state is carried by $\mathbf{E}$ alone.
  - `15-em-energy`: the workhorse identity $I = \tfrac12 c\epsilon_0 n E_0^2$ and the
    $\langle\cos^2\rangle = \tfrac12$ average (fixed in `content/en/conventions.md`).
  - `00-phasors`: complex-amplitude arithmetic; only phase *differences* are measurable;
    random-phase ensembles (`phasors.random_phasor_sum` — reused by 22's ensemble).
  - `16-light-in-matter`: index as medium response — birefringence is "one $n$" upgraded
    to "$n$ depends on field direction".
  - `18-fresnel`: Brewster reflection yields fully s-polarized light — polarization by
    reflection as a *source*, and the physics of sunglasses vs glare.
- **Feeds:** `23-interference`–`26-fabry-perot` (fringe visibility needs matched
  polarizations; orthogonal polarizations do not interfere — stated here, exploited
  there); `24-thin-films` (tape colours = $\Gamma(\lambda)$ through part-08's
  reflectance-to-colour pipeline); `27-coherence` (degree of polarization *is* mutual
  coherence of $E_x$, $E_y$; $\delta$ drift becomes finite coherence time);
  `35-abcd-matrices` (identical operator grammar for rays); `47-fibers` (fiber
  birefringence, polarization-maintaining fiber); `51-nonlinear-optics` (birefringent
  phase matching); `52-quantum-optics` (polarization qubit; Jones matrices as gates;
  three polarizers as sequential measurement).
- **Explicitly not assumed:** crystal optics proper (index ellipsoid, walk-off —
  deferred entirely; waveplates taken as "cut with transverse axes"); coherence theory
  (27 builds *from* the seeds here); any quantum mechanics (advanced-boxed analogy
  only); optical angular momentum (one advanced sentence); Mueller calculus (named in
  22, developed nowhere in core).

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|
| `20-polarization` | `content/en/polarization/20-polarization.md` | Polarization states and Malus' law | 7.1 + 7.2 | Hecht, polarization chapter (states, polarizers, Malus); Griffiths, EM plane waves | planned |
| `21-jones-calculus` | `content/en/polarization/21-jones-calculus.md` | Jones calculus: states as vectors, elements as matrices | 7.3 | Hecht, polarization chapter (retarders, Jones treatment) | planned |
| `22-stokes-poincare` | `content/en/polarization/22-stokes-poincare.md` | Stokes parameters and the Poincaré sphere | 7.4 | Hecht, polarization chapter (Stokes parameters, partial polarization) | planned |

## 4. Shared infrastructure for this part

**`src/wavelab` — existing used:** `phasors.random_phasor_sum` (random-walk machinery
behind 22's unpolarized ensemble — cited by name, owned by part-00);
`measurement.add_noise` (detector noise on every bench reading); `measurement.fit_cosine`
(Malus data is a cosine in $2\theta$: fit $I = \tfrac{I_0}{2}[1+\cos 2\theta]$);
`validation.seed_study`, `validation.scaling_exponent` (the $p\to 0$ ensemble scaling),
`validation.relative_error`.

**`src/wavelab` — new: `polarization.py`** (introduced and owned by this part; README
ownership table). Docstring model spec:

- **System:** transverse plane waves along $+z$ as 2-component complex Jones vectors
  (fully polarized) or 4-component real Stokes vectors (any light); ideal elements as
  $2\times 2$ complex Jones matrices.
- **Dynamics:** none — elements act as linear instantaneous maps, applied by matrix
  multiplication in the order the light meets them.
- **Boundary:** monochromatic, paraxial, normal incidence on ideal aligned elements; no
  interface reflections, no multiple passes, no inter-element propagation phase.
- **Ensemble:** deterministic, except `unpolarized_ensemble`, whose members carry
  independent seeded random orientations and phases; ensemble Stokes vectors are member
  averages.
- **Ignored:** global optical phase (dropped); imperfect extinction and diattenuation;
  retardance dispersion beyond $\Gamma(\lambda)$; depolarization inside elements.
- **Valid when:** light is monochromatic and paraxial, elements ideal, detector averages
  over many cycles (and over the $\delta$ drift for ensemble quantities).
- **Failure modes:** partially polarized light forced into one Jones vector; handedness
  read in another text's convention; cascade matrices multiplied in reading order
  instead of meeting order; squaring complex components instead of $|\cdot|^2$.

Function-level sketch (signatures + contracts):

```python
ellipse_trace(Ex, Ey, delta, t) -> (x, y)        # tip of the real E-vector at z = 0; the polarization ellipse as a Lissajous trace
handedness(Ex, Ey, delta) -> int                 # +1 left, -1 right (receiver view), 0 linear; equals sign(sin delta) = -sign(S3)
jones_polarizer(theta) -> J                      # ideal linear polarizer, axis at theta; projection: J @ J = J, hermitian
jones_waveplate(retardance, theta) -> J          # lossless retarder Gamma, fast axis at theta; unitary, global phase dropped
jones_qwp(theta) / jones_hwp(theta) -> J         # conveniences: retardance pi/2 and pi
cascade(*matrices) -> J                          # arguments in the order light MEETS the elements; returns J_N @ ... @ J_1
intensity(jones_vector) -> float                 # |Ex|^2 + |Ey|^2 (relative units; caller applies 1/2 c eps0 n)
malus(I0, theta) -> float                        # I0 cos^2(theta) — the closed form the Jones route is tested against
stokes_from_jones(vec) -> S                      # (S0, S1, S2, S3); S3 = 2 Im(Ex Ey*) = I_R - I_L under the course convention
stokes_from_measurements(I_h, I_v, I_45, I_m45, I_r, I_l) -> S   # the six-detector operational definition
degree_of_polarization(S) -> float               # p = sqrt(S1^2 + S2^2 + S3^2) / S0
poincare_coords(S) -> (s1, s2, s3)               # (S1, S2, S3)/S0; on the unit sphere iff p = 1, strictly inside iff p < 1
unpolarized_ensemble(n, seed) -> (n, 2) array    # n Jones vectors, seeded random orientation and phase; ensemble p ~ n^(-1/2)
```

**`tests/physics/` additions:**

- *limits:* `intensity(jones_polarizer(t) @ e_x)` equals `malus(1, t)` on a fine angle
  grid (Malus from Jones at every angle, $<10^{-12}$); `cascade(qwp, qwp)` equals `hwp`
  up to global phase; $\Gamma\to 0$ waveplate → identity; `stokes_from_jones` of H, V,
  ±45°, L, R hits the six canonical Stokes vectors exactly.
- *conservation:* waveplates unitary — $S_0$ preserved for every input and axis angle;
  a polarizer never increases $S_0$; $p$ invariant under any waveplate.
- *dimensions:* $\Gamma = 2\pi\,\Delta n\, d/\lambda_0$ dimensionless when $d$,
  $\lambda_0$ carry `pint` lengths.
- *scaling:* scaling a Jones vector by $a$ scales all Stokes parameters by $a^2$, leaves
  $p$ and `poincare_coords` unchanged.
- *seeds:* `unpolarized_ensemble` degree of polarization fitted across seeds
  (`validation.scaling_exponent`) to $p \propto n^{-1/2}$ → 0; identical seeds
  reproduce identical ensembles.
- *convergence:* `stokes_from_measurements` on simulated six-detector data converges to
  the ensemble `stokes_from_jones` average as members grow; `ellipse_trace` closes over
  one period with enclosed area $\pi E_x E_y |\sin\delta|$.

**Shared media:** one render script `media/render/render_polarization.py` produces all
part MP4s (shot lists in §5). **Glossary themes:** state vocabulary (20),
device/operator vocabulary (21), partial-polarization vocabulary (22).

## 5. Module specifications

### 5.1 `20-polarization` — Polarization states and Malus' law

- **Identity and scope:** master-plan notebooks 7.1 + 7.2, merged (§8). States from
  $(E_x, E_y, \delta)$; handedness pinned; polarizer, analyzer, Malus; the
  three-polarizer experiment; unpolarized light introduced honestly. Deferred: matrix
  machinery (21), quantitative partial polarization (22), crystal optics (out of core).
- **Prerequisites:** `14-em-waves` (transversality); `15-em-energy`
  ($I = \tfrac12 c\epsilon_0 n E_0^2$, $\langle\cos^2\rangle = \tfrac12$); `00-phasors`
  (relative phase is physical); `18-fresnel` (Brewster source, for transfer).
- **Learning objectives:**
  - `OBJ-20-1` — Classify the polarization state (linear / circular / elliptical, with
    orientation and handedness) of E = Ex cos(kz - omega t) x + Ey cos(kz - omega t + delta) y
    directly from (Ex, Ey, delta).
  - `OBJ-20-2` — State the course handedness convention (receiver viewpoint, time factor
    e^(-i omega t)) and translate a handedness statement between the optics naming and
    the helicity / particle-physics naming.
  - `OBJ-20-3` — Predict transmitted intensity through a polarizer with Malus' law
    I = I0 cos^2(theta), including the factor-1/2 average for unpolarized input.
  - `OBJ-20-4` — Compute the transmission of a polarizer cascade by successive
    projection, and explain quantitatively why a 45-degree polarizer between crossed
    polarizers transmits I0/8 instead of zero.
  - `OBJ-20-5` — Distinguish polarized, partially polarized, and unpolarized light by
    the behaviour of delta over time, and describe what a rotating analyzer measures in
    each case.
- **Mathematical background:** has — phasors, trig identities, projections; introduced
  here — parametric curves (the Lissajous ellipse); orientation/ellipticity formulas
  (stated in core, derived in advanced).
- **Physical intuition goals:** (1) sketch the E-tip path for any $(E_x, E_y, \delta)$
  without algebra; (2) know what one polarizer does to unpolarized light (halves it)
  and to polarized light (projects it); (3) explain in words why the 45° polarizer
  "rescues" light — projection re-prepares the state; (4) know that a rotating
  analyzer *cannot* distinguish unpolarized from circular light.
- **Section skeleton seeds:**
  - *puzzle:* two crossed film polarizers: dark. Slide a third *between* them at 45°:
    light returns. Boxed question: how can inserting something that only ever absorbs
    light *increase* the transmitted light? Secondary hook: tilt your head 90° in
    polarized sunglasses facing an LCD — the screen goes black.
  - *predict:* (1) crossed pair, third inserted between at 45° — brighter, darker, or
    still dark? (targets `third-polarizer-only-dims`); (2) unpolarized light through
    one ideal polarizer — what fraction passes?; (3) $E_x = E_y$, $\delta = \pi/2$ —
    what path does the tip trace, which way does it turn?; (4) rotating analyzer in
    circular light — does the reading vary?
  - *explore:* state explorer — sliders $E_x, E_y \in [0,1]$, $\delta \in [-\pi,\pi]$;
    synchronized views (transverse ellipse trace with moving arrow, 3-D field helix,
    component traces, handedness readout); polarizer bench — source toggle (laser /
    unpolarized), up to four polarizers with angle sliders, live per-stage meters.
  - *derive:* transverse state → ellipse (eliminate $t$) → special cases → handedness
    convention box → Malus by projection → unpolarized $\langle\cos^2\rangle = \tfrac12$
    average → the three-polarizer stack by successive projection.
  - *verify:* `ellipse_trace` area against $\pi E_x E_y|\sin\delta|$; bench Malus sweep
    fit via `fit_cosine` at the double angle (fitted $\cos$-power = 2.00,
    `numerical-observation` box); triple stack measured at $I_0/8$, middle-angle sweep
    measured as $\tfrac{I_0}{8}\sin^2 2\theta_2$, maximum at 45°.
  - *transfer:* Brewster glare and sunglasses (`18-fresnel`); LCD screens as polarized
    emitters (the free lab kit); interference needs matched polarizations
    (`23-interference`); drifting $\delta$ seeds coherence (`27-coherence`);
    "state + projection" becomes the grammar of `21-jones-calculus`.
  - *quiz:* three-polarizer stack (conceptual + numeric); Malus numerics; state
    classification; handedness naming translation; unpolarized-vs-circular analyzer.
  - *explain:* why "the polarizer filters out the photons that don't fit" is the wrong
    picture and what replaces it; why unpolarized light still has a definite field
    direction at every instant; the head-tilt LCD blackout, for a phone-shop employee.
  - *advanced:* measurement-as-projection made explicit — the sequential Stern–Gerlach
    analogy (a 45° measurement re-prepares the state; quantum mechanics reuses the
    picture verbatim, `52-quantum-optics`); ellipse orientation/ellipticity derived;
    optical angular momentum in one sentence.
- **Core derivations:** (1) the state:
  $\mathbf{E}(z,t) = \Real\!\left[(E_x\,\hat{x} + E_y e^{\ii\delta}\,\hat{y})\,
  e^{\ii(kz-\omega t)}\right] = E_x\cos(kz-\omega t)\,\hat{x} +
  E_y\cos(kz-\omega t+\delta)\,\hat{y}$ — matching §14/§28's real form. (2) eliminate
  $t$ at $z=0$: $(X/E_x)^2 + (Y/E_y)^2 - 2(X/E_x)(Y/E_y)\cos\delta = \sin^2\delta$ —
  an ellipse; orientation $\tan 2\psi = 2E_xE_y\cos\delta/(E_x^2 - E_y^2)$; linear iff
  $\delta = 0, \pi$; circular iff $E_x = E_y$, $\delta = \pm\pi/2$. (3) handedness:
  for $\delta = +\pi/2$ the tip at $z=0$ is $(\cos\omega t, \sin\omega t)$ —
  counterclockwise as seen by the receiver — **left**-circular (box below). (4) Malus:
  projection $E_0\cos\theta$ → $I = I_0\cos^2\theta$; unpolarized input averages
  $\langle\cos^2\theta\rangle = \tfrac12$ over orientations — `15-em-energy`'s
  workhorse average, over *angle* this time. (5) the stack: $I_0 \to \tfrac{I_0}{2}
  \to \tfrac{I_0}{4} \to \tfrac{I_0}{8}$ through 0°/45°/90° — each stage projects, and
  the middle stage *rotates the surviving state*: the whole resolution of the paradox.
- **Handedness convention (pinned; stated once, here):** with time factor
  $e^{-\ii\omega t}$ and propagation along $+z$, the state $E_x = E_y$,
  $\delta = +\pi/2$ — Jones vector $(1, \ii)/\sqrt{2}$ — is **left-circular**: the
  *receiver*, looking back toward the source with the wave approaching, sees the tip
  rotate counterclockwise; $\delta = -\pi/2$ — $(1, -\ii)/\sqrt{2}$ — is
  **right-circular**. This is Hecht's convention, shared by all course texts. The
  trap, fixed in a `definition` box and never revisited: particle physics names by
  *helicity* — the left-circular beam above carries photon spin $+\hbar$ along $+z$
  and is what a particle physicist calls *right*-handed. Same beam, opposite word. The
  course always names from the receiver viewpoint; the box cites
  `content/en/conventions.md`, which gains a matching handedness entry at build time
  (§7).
- **Model specification draft:** System — one monochromatic transverse plane wave
  along $+z$, state $(E_x, E_y, \delta)$; observables are the tip trajectory and
  time-averaged intensities behind polarizers. Dynamics — free propagation plus ideal
  projection at each polarizer. Boundary — infinite uniform beam; polarizers thin,
  lossless in the pass axis, perfect extinction. Ensemble — deterministic for
  polarized light; unpolarized light is a seeded ensemble with drifting $\delta$ and
  orientation. Ignored — element reflection losses, finite extinction of real film,
  beam geometry, coherence between ensemble members. Valid when — detector averages
  many cycles (and, for unpolarized claims, many drift times). Failure modes —
  treating unpolarized light as "no field"; adding intensities of coherent
  same-polarization beams; reading handedness in another naming.
- **Epistemic classification:** ellipse equation, Malus — `theorem` (given the model);
  ideal polarizer — `model-assumption`; handedness naming — `definition` (the box);
  $I_0/8$ stack and fitted $\cos^2$ exponent — `numerical-observation`; "real film
  approaches ideal across the visible" — `empirical-law`.
- **Misconceptions:**
  - `third-polarizer-only-dims` (registry, re-pointed here per README conflict log;
    status → addressed when built) — "Inserting an extra polarizer can only ever
    reduce the transmitted light." Falsifying experiment: the virtual bench measures
    the 0°/90° stack at $I = 0$, then 0°/45°/90° at $I = I_0/8 > 0$, with the middle
    sweep $\tfrac{I_0}{8}\sin^2 2\theta_2$; real counterpart: the same with three
    film polarizers. Distractor: "the stack stays dark — a polarizer can only remove
    light".
  - NEW `unpolarized-means-no-field` — "Unpolarized light has no definite field
    direction at any instant." Falsifier: the lab's unpolarized source shows a
    perfectly definite ellipse at every instant, drifting on the slow ensemble
    timescale. Distractor: "at any given moment the E-vector of unpolarized light
    points nowhere / in all directions at once".
- **Glossary terms:** `polarization` (קיטוב) · `linear-polarization` (קיטוב קווי;
  `he_reject` candidate: קיטוב ליניארי) · `circular-polarization` (קיטוב מעגלי) ·
  `elliptical-polarization` (קיטוב אליפטי) · `handedness` (כיוון סיבוב — translator to
  confirm; `he_reject` candidate: ידיות) · `polarizer` (מקטב) · `analyzer` (מקטב בוחן —
  translator to decide vs אנלייזר) · `malus-law` (חוק מאלוס) · `unpolarized-light`
  (אור לא מקוטב; alternative: אור טבעי).
- **Interactive controls and simulations:** state explorer ($E_x$, $E_y$, $\delta$,
  speed; ellipse + helix + traces); polarizer bench (source toggle, 1–4 polarizers,
  per-stage meters); unpolarized mode with $\delta$-drift-rate slider (fast drift =
  light bulb, slow = "almost a laser" — the 27 teaser).
- **Virtual lab outline** (`notebooks/en/labs/20-polarization.ipynb`): (1) reproduce
  the six canonical states, record handedness; (2) Malus sweep with
  `measurement.add_noise`, fit via `fit_cosine` at $2\theta$, report $I_0$ ±
  uncertainty and the $\cos$-power; (3) the paradox — measure the crossed pair, insert
  the third, sweep its angle, fit $\sin^2 2\theta_2$, report the maximum ± error;
  (4) rotate an analyzer in ensemble light (flat $I_0/2$) and in circular light (also
  flat — the module's honest cliffhanger, resolved in 22); (5) *measurement culture:*
  triple-stack transmission = value ± error vs the $I_0/8$ prediction.
- **Real-experiment counterpart:** LCD/phone screen (polarized emitter) + film
  polarizer: rotate in 10° steps, log brightness with a light-meter app, import the
  angle–lux CSV, fit Malus; then the three-film-polarizer stack — qualitative return
  of light, relative-brightness estimate. Cost: three film polarizers.
- **Media assets** (`render_polarization.py`): (a) $\delta$-sweep morph — ellipse
  trace with rotating arrow beside the 3-D field helix, $\delta$ running $-\pi\to\pi$
  at fixed $E_x = E_y$; (b) three-polarizer bench — intensity bars as the middle
  polarizer rotates 0→90°, dark–bright–dark. Language-neutral, no burned-in text.
- **Quiz bank outline:** `Q-20-1` MC — crossed + inserted 45° outcome (OBJ-20-4,
  distractor `third-polarizer-only-dims`); `Q-20-2` numeric — triple stack at general
  middle angle (OBJ-20-4); `Q-20-3` numeric — Malus chain (OBJ-20-3); `Q-20-4` MC —
  classify state from $(E_x, E_y, \delta)$ (OBJ-20-1); `Q-20-5` MC — handedness
  translation optics ↔ helicity (OBJ-20-2); `Q-20-6` MC — rotating analyzer in
  unpolarized vs circular light (OBJ-20-5, distractor `unpolarized-means-no-field`);
  `Q-20-7` free — the paradox as projection in ≤ 4 sentences (OBJ-20-4).
- **Problem set outline:** analytical — derive the ellipse equation and orientation
  formula; the $N$-polarizer staircase and its $N\to\infty$ limit ("rotating light
  with absorbers", transmission → $\tfrac{I_0}{2}$); Brewster + Malus glare problem.
  Computational — optimal middle angle with lossy film; analyzer scan of a partially
  drifting ensemble. Challenge — prove a rotating analyzer cannot distinguish any two
  beams with equal time-averaged $I_H = I_V$ and $I_{45} = I_{-45}$ (phrased via time
  averages; 22's vocabulary not required).
- **Runtime budget:** ellipse traces ≤ 2000 points, bench closed-form, ensembles
  ≤ $10^4$ members — all sub-second in Pyodide.
- **Validation gates:** standard set (README) with `--module 20-polarization`; the
  registry re-point of `third-polarizer-only-dims` lands with this module (§7).
- **Open questions for the author:** does the 3-D helix earn a place on the page or
  stay lab-only (recommendation: ellipse + traces on page, helix in lab)? Does the
  Stern–Gerlach aside name quantum mechanics explicitly (recommendation: yes,
  advanced box only)?

### 5.2 `21-jones-calculus` — Jones calculus: states as vectors, elements as matrices

- **Identity and scope:** master-plan notebook 7.3. Jones vectors and matrices;
  polarizer, quarter- and half-wave plates from birefringence; rotation sandwich;
  cascades and non-commutativity; §28's bench as the lab centerpiece. Deferred:
  partial polarization (22), Mueller matrices (named in 22), crystal-optics origin of
  $\Delta n$ (out of core).
- **Prerequisites:** `20-polarization` (states, handedness box, Malus);
  `16-light-in-matter` (phase through index: $e^{\ii n k_0 d}$); `00-phasors`
  (complex arithmetic).
- **Learning objectives:**
  - `OBJ-21-1` — Write the normalized Jones vector of a given polarization state and
    compute relative intensity I = |Ex|^2 + |Ey|^2.
  - `OBJ-21-2` — Construct the Jones matrix of a polarizer or waveplate at angle theta
    with the rotation sandwich J(theta) = R(-theta) J0 R(theta).
  - `OBJ-21-3` — Compute retardance Gamma = 2 pi Delta-n d / lambda0 from birefringence
    and thickness, and design a quarter- or half-wave plate for a given wavelength.
  - `OBJ-21-4` — Predict the action of a QWP (linear at 45 degrees to the fast axis ->
    circular) and an HWP (reflects the polarization direction about the fast axis),
    including the handedness of the output.
  - `OBJ-21-5` — Compute cascade outputs E_out = J_N ... J_1 E_in in the order the
    light meets the elements, and exhibit two elements whose two orderings give
    measurably different outputs.
  - `OBJ-21-6` — Recover Malus' law from the Jones formalism and state the formalism's
    scope: fully polarized light only.
- **Mathematical background:** has — complex vectors, $2\times 2$ products, rotation
  matrices (from `07-normal-modes`); introduced here — operator thinking: state /
  operator / ordered product; unitary vs projection operators (named lightly, used
  concretely).
- **Physical intuition goals:** (1) predict the §28 bench output stage by stage
  without computing; (2) know *why* order matters — each element acts on whatever
  state reaches it; (3) say what a waveplate does physically (delays one axis) and why
  that changes the state without absorbing anything; (4) design "make me circular
  light" from a laser and a film drawer.
- **Section skeleton seeds:**
  - *puzzle:* laser → polarizer(0°) → QWP(45°) → analyzer(90°): light passes the
    crossed analyzer; remove the QWP: dark; swap polarizer and QWP: different again.
    Boxed question: what algebra predicts a chain of elements — and why does the
    *order* of two elements change the answer?
  - *predict:* (1) polarizer(0°) then QWP(45°) — same output as the reverse order?
    (targets NEW `optical-elements-commute`); (2) linear light at 45° to a QWP fast
    axis — what emerges?; (3) HWP at $\theta$ on horizontal light — output angle?;
    (4) double a QWP's thickness — what element is it now?
  - *explore:* the §28 virtual bench — laser (state presets), polarizer, QWP, HWP,
    analyzer, detector; every stage shows its output ellipse; **predict-then-measure
    mode** (commit the per-stage state, then reveal); drag-to-reorder elements;
    generic waveplate with a free $\Gamma$ slider and a $\lambda$ slider showing a
    real plate detune ($\Gamma \propto 1/\lambda$).
  - *derive:* Jones vectors (six canonical states tabulated) → polarizer at 0° as
    projection → rotation sandwich → polarizer at $\theta$ (Malus recovered) →
    waveplate from birefringence → QWP and HWP actions worked → non-commutativity
    computed for the puzzle pair.
  - *verify:* Malus-from-Jones at every angle (library limit test, quoted);
    `cascade(qwp, qwp)` = HWP up to global phase (`numerical-observation`); $S_0$
    conservation as the unitarity check; both orderings of polarizer(0°)+QWP(45°)
    measured — outputs differ in state *and* power.
  - *transfer:* ABCD ray matrices — same grammar, new vector (`35-abcd-matrices`);
    Jones matrices are single-qubit gates, HWP at 22.5° acts as a Hadamard
    (`52-quantum-optics`, advanced box); fiber birefringence (`47-fibers`);
    birefringent colour → thin-film colour pipeline (`24-thin-films`).
  - *quiz:* retardance design numeric; ordering MC; cascade numeric; HWP/QWP action
    MCs; meeting order vs reading order free response.
  - *explain:* how a waveplate changes the state without absorbing anything, without
    matrices; why $J_{pol}^2 = J_{pol}$ but $J_{wp}^2 \ne J_{wp}$, physically; explain
    to a photographer what a "circular polarizing filter" contains and why the order
    inside it matters (linear polarizer then QWP).
  - *advanced:* the qubit dictionary — Jones vectors as qubit states, waveplates as
    unitary gates, polarizers as projective measurements; eigenpolarizations — every
    lossless element has two states it merely phases; why "circular polarizer" sheets
    work one way round only.
- **Core derivations:** (1) canonical Jones vectors: H $(1,0)$; V $(0,1)$; ±45°
  $(1,\pm 1)/\sqrt2$; L $(1, \ii)/\sqrt2$; R $(1, -\ii)/\sqrt2$ — handedness per 20's
  box. (2) polarizer at $\theta$: $J_{pol}(\theta) = R(-\theta)\,
  \operatorname{diag}(1, 0)\, R(\theta)$, rows $(\cos^2\theta,\ \sin\theta\cos\theta)$
  and $(\sin\theta\cos\theta,\ \sin^2\theta)$, with $R(\theta)$ the frame rotation
  with rows $(\cos\theta,\ \sin\theta)$, $(-\sin\theta,\ \cos\theta)$. (3) waveplate,
  fast axis horizontal: each axis accumulates $e^{\ii n_{f,s} k_0 d}$; dropping the
  global phase, $J_{wp}(\Gamma, 0) = \operatorname{diag}(1, e^{\ii\Gamma})$ with
  $\Gamma = 2\pi\,\Delta n\, d/\lambda_0$, $\Delta n = n_s - n_f > 0$ — the *slow*
  axis gains the extra phase, sign forced by the course convention. (4) QWP at 45° on
  H: $(1,0) \mapsto \tfrac12(1+\ii,\, 1-\ii) \propto (1, -\ii)/\sqrt2$ —
  right-circular; the mirrored input gives left — output handedness depends on which
  side of the fast axis the input lies (quiz fodder, and the lab's cleanest
  handedness measurement). (5) HWP at $\theta$: rows $(\cos 2\theta,\ \sin 2\theta)$,
  $(\sin 2\theta,\ -\cos 2\theta)$ up to global phase — reflection about the fast
  axis; linear at $\alpha$ → linear at $2\theta - \alpha$. (6) non-commutativity
  worked: with H input, polarizer(0°) *then* QWP(45°) — the product
  $J_{qwp}(45^\circ) J_{pol}(0)$ — gives circular light at full intensity; the
  reversed order gives *linear* H at half intensity. Different state, different
  power; the bench confirms both numbers.
- **Model specification draft:** System — fully polarized monochromatic beams as
  Jones vectors; ideal thin elements as Jones matrices; observables are per-stage
  state and relative intensity. Dynamics — matrix multiplication in meeting order;
  free propagation contributes only global phase, dropped. Boundary — normal
  incidence, aligned ideal elements, no inter-element reflections. Ensemble —
  deterministic; detector noise via `wavelab.measurement` in the lab only. Ignored —
  retardance dispersion except where the $\Gamma(\lambda)$ slider makes it the point;
  element imperfections; beam geometry. Valid when — input fully polarized and
  monochromatic; elements thin and ideal. Failure modes — partial polarization pushed
  through a Jones vector (22's opening); matrices multiplied in reading order;
  global-phase differences mistaken for physics.
- **Epistemic classification:** rotation sandwich and every matrix identity —
  `theorem`; thin ideal normal-incidence elements — `model-assumption`;
  $\Gamma = 2\pi\Delta n d/\lambda_0$ — `theorem` given the plate model, tabulated
  $\Delta n$ values — `empirical-law`; QWP² = HWP and the two-orderings measurement —
  `numerical-observation`; "does the photon 'go through' the polarizer?" —
  `open-question` pointer to 52.
- **Misconceptions:** NEW `optical-elements-commute` — "Optical elements can be
  applied in any order; only which elements are present matters." Falsifying
  experiment: the bench measures both orderings of polarizer(0°) + QWP(45°) on the
  same input — different output states (circular vs linear) and powers (full vs
  half); real-kit counterpart: a camera "circular polarizer" (linear film + QWP)
  flipped front-to-back against an LCD. Distractor: "same output — matrix products
  don't care about order for lossless elements".
- **Glossary terms:** `jones-vector` (וקטור ג'ונס) · `jones-matrix` (מטריצת ג'ונס) ·
  `birefringence` (שבירה כפולה) · `fast-axis` (ציר מהיר) · `slow-axis` (ציר איטי) ·
  `retardance` (השהיית מופע — translator to confirm; `he_reject` candidate: פיגור) ·
  `waveplate` (לוחית גל) · `quarter-wave-plate` (לוחית רבע גל) · `half-wave-plate`
  (לוחית חצי גל) · `operator` (אופרטור).
- **Interactive controls and simulations:** the §28 bench (element list, angle
  sliders, drag-to-reorder, per-stage ellipses, predict-then-measure mode); generic
  waveplate with $\Gamma$ and $\lambda$ sliders; a "matrix inspector" showing the
  live cascade product.
- **Virtual lab outline** (`notebooks/en/labs/21-jones-calculus.ipynb`):
  (1) canonical states through single elements — verify the tabulated actions;
  (2) the full §28 chain laser → polarizer → QWP → HWP → analyzer → detector: predict
  the state at every stage on paper, then measure, and score the predictions;
  (3) the ordering experiment — both orderings of polarizer+QWP, record state and
  power (`numerical-observation`); (4) waveplate design — from quartz
  $\Delta n(\lambda)$ compute $d$ for a QWP at 633 nm, then *measure*
  $\Gamma(\lambda)$ over 500–700 nm (the chromatic-waveplate fact behind 24's tape
  colours); (5) *measurement culture:* extract $\Gamma$ of an "unknown" waveplate
  from analyzer sweeps, value ± error vs truth.
- **Real-experiment counterpart:** cellophane / sticky tape between crossed film
  polarizers — spectacular birefringent colours; layer count vs colour ($n$ layers
  step $\Gamma(\lambda)$ by a fixed $\Delta n\,d$ each); rotating the analyzer 90°
  swaps colours for complements. Photos import into the lab; a computed
  transmission-vs-$\lambda$ curve per layer count is compared qualitatively
  (quantitative colour arrives with `24-thin-films`).
- **Media assets** (`render_polarization.py`): (c) QWP action — linear field helix
  entering, circular helix leaving, fast/slow components separating in phase inside
  the plate; (d) HWP mirror-flip — input and output traces side by side while the
  plate angle sweeps.
- **Quiz bank outline:** `Q-21-1` numeric — QWP thickness from $\Delta n$, $\lambda$
  (OBJ-21-3); `Q-21-2` MC — do polarizer and QWP commute (OBJ-21-5, distractor
  `optical-elements-commute`); `Q-21-3` numeric — cascade output intensity
  (OBJ-21-5); `Q-21-4` MC — HWP on linear at $\alpha$ (OBJ-21-4); `Q-21-5` MC — QWP
  output handedness for inputs at ±45° (OBJ-21-4); `Q-21-6` numeric — Malus from a
  Jones product (OBJ-21-1, OBJ-21-2, OBJ-21-6); `Q-21-7` free — why the rightmost
  matrix acts first (OBJ-21-5).
- **Problem set outline:** analytical — derive $J_{hwp}(\theta)$ from the sandwich;
  eigenpolarizations of an arbitrary waveplate; lossless elements are unitary, ideal
  polarizers are projections. Computational — the elliptical-state factory
  (polarizer + QWP + HWP: show every fully polarized state is reachable); chromatic
  error of a real QWP across the visible. Challenge — the $N$-polarizer rotator of
  20's problem set in one line as a matrix-product limit; HWP at 22.5° as a Hadamard.
- **Runtime budget:** $2\times 2$ complex products and ≤ $10^3$-point sweeps —
  negligible; keep per-stage ellipse traces ≤ 400 points.
- **Validation gates:** standard set with `--module 21-jones-calculus`; the
  `polarization.py` limit/conservation tests (§4) land with this module — 22 cites
  them.
- **Open questions for the author:** matrix inspector numeric or symbolic
  (recommendation: numeric with a symbol toggle)? Qubit box here or only in 52
  (recommendation: two sentences here, full dictionary there)? "Circular polarizer"
  sheets in core or advanced (recommendation: advanced — a cascade-order payoff)?

### 5.3 `22-stokes-poincare` — Stokes parameters and the Poincaré sphere

- **Identity and scope:** master-plan notebook 7.4, elevated to a full advanced-track
  module (§8): Stokes parameters defined operationally, degree of polarization, the
  polarized + unpolarized decomposition, the Poincaré sphere with waveplate action as
  rotation. Mueller matrices *named* as the completion (matrices on Stokes vectors),
  deferred beyond the core. Advanced-track boundary: no core content in later parts
  depends on this module; `27-coherence` links to it from its own advanced material.
- **Prerequisites:** `20-polarization` (unpolarized light as $\delta$ drift; the
  analyzer's blindness to circular-vs-unpolarized); `21-jones-calculus` (Jones
  vectors; QWP action — the circular measurements need one); `00-phasors`
  (`random_phasor_sum`, ensemble averages).
- **Learning objectives:**
  - `OBJ-22-1` — Define S0, S1, S2, S3 operationally from six intensity measurements
    (S0 = IH + IV, S1 = IH - IV, S2 = I45 - Im45, S3 = IR - IL) and compute them from
    a Jones vector.
  - `OBJ-22-2` — Compute the degree of polarization p = sqrt(S1^2 + S2^2 + S3^2) / S0
    and decompose any beam uniquely into a fully polarized part plus an unpolarized
    part.
  - `OBJ-22-3` — Place a state on the Poincare sphere and read orientation,
    ellipticity, and handedness from its position (equator = linear, poles =
    circular).
  - `OBJ-22-4` — Describe waveplate action as a rotation of the Poincare sphere by
    Gamma about the equatorial point of its fast axis, and use it to predict QWP and
    HWP outputs geometrically.
  - `OBJ-22-5` — Explain why partially polarized light admits no Jones vector, and
    how an ensemble with drifting delta produces 0 < p < 1.
- **Mathematical background:** has — Jones algebra, ensemble averages, 3-D vectors;
  introduced here — double-angle sphere coordinates $(2\psi, 2\chi)$; a state space
  with a boundary (pure states on it, mixtures inside) — as geometry, not density
  matrices.
- **Physical intuition goals:** (1) name the six measurements that pin down any
  beam's polarization and carry them out; (2) say *why* a polarizer alone cannot
  distinguish circular from unpolarized, and which single element fixes it (a QWP);
  (3) see waveplates as rigid sphere rotations, polarizers as collapses onto a point;
  (4) read $p$ as "how repeatable the ellipse is", not "how strong the light is".
- **Section skeleton seeds:**
  - *puzzle:* 20 ended on a cliffhanger — a rotating analyzer reads flat in circular
    *and* in unpolarized light — and 21's formalism cannot even *write* sunlight.
    Boxed question: what numbers describe how polarized a beam is, and how do you
    measure them with a polarizer, a waveplate, and a power meter?
  - *predict:* (1) can some Jones vector represent sunlight? (targets NEW
    `every-beam-has-jones-vector`); (2) design a measurement distinguishing RCP from
    unpolarized using one polarizer and one QWP; (3) two equal-power beams, H and V,
    mutually incoherent — polarized or not?; (4) what does an HWP do to unpolarized
    light?
  - *explore:* the Stokes station — source mixer (pure state, or ensemble with $p$
    target, $\delta$-drift rate, member count) feeding six virtual detectors (H, V,
    ±45°, R, L); live Stokes bars, $p$ dial, 3-D Poincaré sphere with the state
    plotted inside or on the surface; QWP/HWP buttons drawing rotation trajectories.
  - *derive:* six measurements → Stokes definitions → from a Jones vector → ensemble
    averages and $S_0^2 \ge S_1^2+S_2^2+S_3^2$ → $p$ and the unique decomposition →
    the sphere and double angles → waveplates as rotations, HWP as half-turn → why
    the analyzer is blind to $S_3$ and a QWP converts $S_3$ into $S_1$ (the
    RCP-vs-unpolarized resolver).
  - *verify:* `stokes_from_measurements` round-trips `stokes_from_jones` for the six
    canonical states; ensemble $p \propto n^{-1/2}$ (`numerical-observation`, fitted
    exponent); waveplates preserve $S_0$ and $p$ and move the sphere point by exactly
    $\Gamma$ about the predicted axis; incoherent H+V measures $p = 0$ while
    *coherent* H+V measures $p = 1$ at 45° — the most instructive contrast in the
    part.
  - *transfer:* degree of polarization ↔ mutual coherence of the components —
    `27-coherence` builds fringe visibility the same way; Rayleigh sky polarization
    (the real experiment); polarimetry in astronomy and remote sensing; the Poincaré
    sphere *is* the Bloch sphere (`52-quantum-optics`); Mueller matrices as the
    operator completion (named, deferred).
  - *quiz:* six-measurement numerics; sphere-reading MCs; the RCP-vs-unpolarized
    design question; decomposition numeric.
  - *explain:* why "50% polarized" cannot be captured by any single field history;
    why the sphere's inside is not "weaker light" but "less repeatable light"; why a
    polarizing filter darkens blue sky most at 90° from the sun.
  - *advanced:* the coherency matrix $\langle E_i E_j^*\rangle$ with Stokes
    parameters as its four real coordinates — one page, bridging to 27's correlation
    functions and 52's density matrix; the Mueller matrix of a polarizer worked once,
    with the honest statement of what depolarizing elements would need.
- **Core derivations:** (1) operational: $S_0 = I_H + I_V$, $S_1 = I_H - I_V$,
  $S_2 = I_{45} - I_{-45}$, $S_3 = I_R - I_L$ — six measurements, four numbers, one
  redundancy ($S_0$ measured twice as a consistency check). (2) from a Jones vector:
  $S_0 = |E_x|^2 + |E_y|^2$, $S_1 = |E_x|^2 - |E_y|^2$, $S_2 = 2\Real(E_x E_y^*)$,
  $S_3 = 2\Imag(E_x E_y^*)$ — under the course time factor this gives $S_3 = +S_0$
  for right-circular $(1, -\ii)/\sqrt2$, consistent with $S_3 = I_R - I_L$; texts on
  the opposite time factor write the conjugate — same physics, flagged once (§8).
  (3) pure states satisfy $S_1^2 + S_2^2 + S_3^2 = S_0^2$ (identity); ensemble
  averages obey $\le$ (Cauchy–Schwarz) — fully polarized means the ellipse never
  drifts. (4) $p = \sqrt{S_1^2+S_2^2+S_3^2}/S_0$; decomposition
  $S = S^{(pol)} + S^{(unpol)}$ with $S^{(unpol)} = ((1-p)S_0, 0, 0, 0)$, unique.
  (5) sphere: $(s_1, s_2, s_3) = (S_1, S_2, S_3)/S_0$; a pure state sits at longitude
  $2\psi$, latitude $2\chi$; equator = linear, north pole = right-circular
  ($s_3 = +1$), south = left. (6) waveplate with fast axis at $\theta$: rotation by
  $\Gamma$ about the equatorial axis through longitude $2\theta$; its fixed points
  are its eigenpolarizations (21's advanced thread made geometric); HWP = half-turn.
  (7) unpolarized ensemble: independent drifting orientation and $\delta$ average
  $S_1, S_2, S_3$ all to zero — module 20's drift-rate slider made quantitative.
- **Model specification draft:** System — a beam described by ensemble-averaged
  intensity measurements, i.e. a Stokes 4-vector; pure states doubly described by
  Jones vectors. Dynamics — none for the beam; elements act on members as in 21, on
  Stokes vectors as sphere rotations (retarders) or projections (polarizers).
  Boundary — 21's ideal-element idealizations. Ensemble — the central object: seeded
  members with drifting orientation and $\delta$; measured Stokes values are member
  averages; detector noise via `wavelab.measurement`. Ignored — spectral structure of
  the drift (27's subject), depolarizing elements, Mueller machinery. Valid when —
  averaging time long against the drift time; elements non-depolarizing. Failure
  modes — assigning a Jones vector to $p < 1$ light; sphere points outside the unit
  ball (measurement error read as physics); confusing $p$ with intensity.
- **Epistemic classification:** Stokes-from-Jones relations and
  $S_0^2 \ge S_1^2+S_2^2+S_3^2$ — `theorem`; the six-measurement scheme —
  `definition`; the drift ensemble as a model of natural light — `model-assumption`;
  fitted $p \propto n^{-1/2}$ and the coherent-vs-incoherent H+V contrast —
  `numerical-observation`; Rayleigh sky pattern (max $p$ at 90° from the sun, real
  $p$ well below 1) — `empirical-law`; "what sets the drift timescale of real
  sources" — `open-question` pointer to `27-coherence`.
- **Misconceptions:** NEW `every-beam-has-jones-vector` — "Any beam of light can be
  written as some Jones vector if you are clever enough." Falsifying experiment: the
  Stokes station measures a $p = 0.5$ ensemble; students search the full
  $(E_x, E_y, \delta)$ space and verify no pure state reproduces the measured
  six-intensity table (every pure state gives $p = 1$); the ensemble does.
  Distractor: "sunlight is $(1, 1)/\sqrt2$, since it has equal H and V intensity".
- **Glossary terms:** `stokes-parameters` (פרמטרי סטוקס) · `degree-of-polarization`
  (דרגת קיטוב) · `poincare-sphere` (ספירת פואנקרה) · `partially-polarized-light`
  (אור מקוטב חלקית) · `ellipticity` (אליפטיות) · `mueller-matrix` (מטריצת מולר) ·
  `polarimetry` (פולרימטריה — translator to confirm transliteration).
- **Interactive controls and simulations:** Stokes station (source mixer, six
  detector readouts, Stokes bars, $p$ dial); Poincaré sphere 3-D view (orbit/zoom,
  trajectory trails, double-angle grid); "find the pure state" challenge mode for the
  misconception experiment.
- **Virtual lab outline** (`notebooks/en/labs/22-stokes-poincare.ipynb`): (1) measure
  the six intensities for the six canonical pure states, assemble Stokes vectors,
  check against `stokes_from_jones`; (2) the resolver — distinguish RCP from
  unpolarized with polarizer + QWP; (3) ensemble study — sweep drift rate, measure
  $p$; fit $p(n) \propto n^{-1/2}$ across seeds with `validation.scaling_exponent`;
  (4) sphere kinematics — QWP/HWP at several angles on a fixed state, plot
  trajectories, verify axis and angle; (5) *measurement culture:* a seeded "mystery
  beam" — report its full Stokes vector and $p$, each ± uncertainty from repeated
  noisy measurement.
- **Real-experiment counterpart:** sky polarimetry — film polarizer over a phone
  camera at fixed exposure; sweep orientation at several sky positions (90° from the
  sun vs near it); estimate linear degree of polarization
  $p_{lin} = (I_{max} - I_{min})/(I_{max} + I_{min})$; import the angle–brightness
  CSV; map $p_{lin}$ across the sky against the Rayleigh single-scattering pattern.
  Honest caveat stated: this measures *linear* DOP only — skylight's circular
  component is negligible, itself the interesting fact.
- **Media assets** (`render_polarization.py`): (e) Poincaré sphere — a state dragged
  by a rotating QWP then HWP, arcs traced on the sphere; (f) the dancing ellipse —
  an ensemble member's instantaneous ellipse drifting while the measured $p$ dial
  falls from 1 toward 0 as averaging lengthens.
- **Quiz bank outline:** `Q-22-1` numeric — Stokes vector and $p$ from six given
  intensities (OBJ-22-1, OBJ-22-2); `Q-22-2` MC — read state from a sphere position
  (OBJ-22-3); `Q-22-3` MC — which element distinguishes RCP from unpolarized
  (OBJ-22-1, OBJ-22-5); `Q-22-4` MC — can sunlight be a Jones vector (OBJ-22-5,
  distractor `every-beam-has-jones-vector`); `Q-22-5` numeric — polarized +
  unpolarized decomposition (OBJ-22-2); `Q-22-6` MC — sphere action of an HWP
  (OBJ-22-4); `Q-22-7` free — why $p$ measures repeatability, not strength
  (OBJ-22-5).
- **Problem set outline:** analytical — prove $S_0^2 = S_1^2+S_2^2+S_3^2$ for pure
  states and $\ge$ for mixtures; incoherent sums add Stokes vectors (and why);
  uniqueness of the decomposition. Computational — Stokes tomography with a single
  rotating QWP + fixed polarizer (the four-measurement classic; compare conditioning
  against the six-measurement scheme); simulate the sky map from single-scattering
  geometry. Challenge — the Mueller matrix of an ideal polarizer from projection on
  ensembles; retarder Mueller action as an $SO(3)$ rotation of $(S_1, S_2, S_3)$.
- **Runtime budget:** ensembles ≤ $10^4$ two-vectors; sphere as a static-refresh
  matplotlib 3-D plot (animations ≤ 60 frames, pre-rendered in media); sub-second in
  Pyodide.
- **Validation gates:** standard set with `--module 22-stokes-poincare`; the §4
  seeds/convergence tests land with this module.
- **Open questions for the author:** coherency-matrix page here or moved to
  `27-coherence` (recommendation: one paragraph here, machinery there)?
  Four-measurement rotating-QWP tomography in the lab core or as the computational
  problem (recommendation: six in core for clarity, four as the problem)? Sphere
  rendering library for JupyterLite (matplotlib 3-D suffices; avoid heavier deps)?

## 6. Part-level assessment and capstone hooks

- **Capstone §35.2 (Virtual Optical Bench)** consumes this part directly: its
  polarizer and waveplate stages *are* `jones_polarizer` / `jones_waveplate` /
  `cascade`, and the §28 bench built in 21 is a working prototype of that capstone's
  polarization layer. **Capstone §35.4 (Optical Communication System)** touches the
  part through fiber birefringence and polarization drift (via `47-fibers`).
- Cross-module synthesis problems (filed with 22's problem set): (a) full-chain
  design — deliver left-circular light of specified intensity from an unpolarized
  source with a minimal element list, then *verify* by measuring its Stokes vector
  (touches 20 + 21 + 22); (b) Brewster reflection (18) + Malus (20) + a camera filter
  cascade (21) — the polarization-and-glare problem; (c) why crossed polarizers leak
  in the real world — finite extinction + stray retardance, an uncertainty-budget
  exercise.
- Exam themes: state classification at sight; stack transmissions by projection;
  meeting-order matrix products; sphere reading; six-measurement Stokes arithmetic;
  one essay from the measurement-as-projection thread.

## 7. Build order and validation gates

Build order `20 → 21 → 22`, teaching order and dependency order coinciding: 21's bench
assumes 20's states and handedness box; 22 opens on the joint cliffhanger of 20
(analyzer blindness) and 21 (no Jones vector for sunlight). All three follow part-05's
`14-em-waves` / `15-em-energy` and part-06 in the TOC.

With `20-polarization`: re-point `third-polarizer-only-dims` from `07-polarization` to
`20-polarization` in `assessment/misconceptions.yml` (README conflict log; status →
`addressed` once page + quiz land); add NEW entries `unpolarized-means-no-field`
(addressed by 20), `optical-elements-commute` (pending until 21),
`every-beam-has-jones-vector` (pending until 22); deposit 20's glossary terms; add the
handedness entry to `content/en/conventions.md` (one boxed subsection, cross-linked
from 20's convention box — the course states handedness exactly once).

With `21-jones-calculus`: the `polarization.py` limit and conservation tests (§4) land
in `tests/physics/` — 22's claims cite them. With `22-stokes-poincare`: the seeds and
convergence tests land; mark the module advanced-track in the TOC
(`content/en/myst.yml`). Per module: the standard four gates (README, bottom).

## 8. Deviations from the master plan

- **Merge 7.1 + 7.2 → `20-polarization`:** Malus' law is a fifteen-minute payoff of
  the state picture, not a standalone notebook; merging puts the three-polarizer
  paradox in the same module as the states it interrogates (precedent:
  `02-damped-driven` ← 1.2 + 1.3).
- **Handedness convention pinned:** master plan §14 writes the field but never defines
  left/right circular. This plan fixes the receiver-viewpoint (Hecht) naming under
  the course time factor, adds the optics-vs-helicity naming-clash box, and adds the
  matching entry to `content/en/conventions.md` at build time.
- **Stokes spelling fixed:** $S_3 = 2\Imag(E_x E_y^*) = I_R - I_L$ is forced by the
  course phase convention; texts on the opposite time factor conjugate it. Stated
  once in 22 as a convention consequence, not a disagreement.
- **7.4 elevated:** from "advanced extension" bullet list to a full advanced-track
  module with an operational six-measurement definition, an ensemble lab, and a real
  experiment (sky polarimetry) — partial polarization is the course's bridge to
  coherence (27) and quantum state-thinking (52).
- **Additions beyond the master plan:** the three-polarizer paradox as centerpiece
  with a claimed registry misconception; non-commutativity as a designed experiment;
  predict-then-measure mode for the §28 bench; the drifting-$\delta$ model of natural
  light; three NEW misconception entries; quantum foreshadowing (Stern–Gerlach, qubit
  gates, Bloch = Poincaré) confined to advanced boxes; Mueller matrices named and
  deferred.
