# Part I — Oscillations — Implementation Plan

> **Master plan:** §8 (Part I). **Modules:** `01-sho`, `02-damped-driven`, `05-impulse-response`. **Status:** partial — `01-sho` and `02-damped-driven` built.
> Canonical numbering, invariants, and conflict log: [README.md](README.md).

## 1. Part overview and narrative arc

Part I is one equation explored in three passes. Everything lives inside
$m\ddot{x} + b\dot{x} + kx = F(t)$: **free** (module 01 — the parabola at the bottom of
every valley), **driven** ($F = F_0\cos\omega t$, module 02 — loss and forcing added,
resonance and the Lorentzian earned), **kicked** ($F$ arbitrary, module 05 — impulse
response and convolution turning the oscillator into the course's first linear
time-invariant system). By the end of 05 the student owns the *complete local theory of
linear response*: give me $G(t)$ — equivalently $\hat{H}(\omega)$ — and I will tell you
the motion under any force whatsoever. The rest of the course is this theory with space
added: $x(t)$ becomes $\psi(x,t)$, $\wnat$ a dispersion relation, $Q$ finesse and
linewidth, and $G(t)$ returns as the point spread function.

The enhancement over master plan §8 is threefold. Notebooks 1.2 and 1.3 are **merged**
into `02-damped-driven` (§8 below): free decay is the $F_0 = 0$ limit and the *transient*
of the driven solution — apart each half is thin; together, regimes and resonance fall
out of one complex-root analysis. The **complex-amplitude method is staged as module
00's payoff**: substitute $x = \Real[X e^{-\ii\omega t}]$, divide out the exponential,
and a differential equation collapses to one line of arrow arithmetic. And module 05
expands the master plan's four-line notebook 1.4 into the course's **LTI keystone**:
Green function, causality, $\hat{G} \leftrightarrow \hat{H}$, the mechanical–electrical
dictionary, with the forward link to imaging stated in the text, not left as folklore.

Two objects planted here recur for the rest of the course: the **Lorentzian** — universal
resonance shape in 02, transform of an exponential decay in 04, $|\hat{H}|$ from a single
kick in 05, later the Fabry–Pérot line (26), the absorption profile (16), the laser
cavity mode (44) — and **$Q$**, one number wearing three lab coats (energy decay per
radian, bandwidth $\wnat/\Delta\omega$, phase slope at resonance), later photon lifetime,
finesse, and linewidth. The teaching order interleaves Part 0 (`01 → 02 → 03 → 04 → 05`):
02 hands Fourier series its physical engine, 04 lands just before 05 consumes it; the
sequencing argument is owned by `part-00-foundations.md` §8.

## 2. Position in the course

- **Requires:**
  - `01-sho`: `00-phasors` — the arrow $A e^{-\ii\varphi}$, $\Real[\,\cdot\,]$ extraction.
  - `02-damped-driven`: `00-phasors` (complex arithmetic, one-frequency superposition);
    `01-sho` ($\wnat = \sqrt{k/m}$, energies, phase space, fit-and-report workflow).
  - `05-impulse-response`: `02-damped-driven` ($X$, $Q$, transient vs steady state);
    `04-fourier-transform` (convolution theorem, `fourier.spectrum`, the one-sided
    exponential ↔ Lorentzian pair, operational deltas); `00-phasors` (the
    negative-frequency thread, closed once more here).
- **Feeds:** `03-fourier-series` — `oscillators.steady_state_response` weights each
  harmonic of a periodic drive (part-00 §4 cites it by name; §4 below); `06-coupled` /
  `07-normal-modes` — coupled systems are two copies of this part; `10-impedance` —
  previewed in 02's advanced; `16-light-in-matter` — the Lorentz atom *is* module 02
  with charge; `26-fabry-perot` / `44-resonators` — linewidth, finesse, photon lifetime
  are $Q$ re-costumed; `40-psf-otf` — the LTI bridge, $G$ → PSF, $\hat{H}$ → OTF (05).
- **Explicitly not assumed:** Fourier methods anywhere in module 02 (it precedes 03/04 —
  all single-frequency phasor algebra); Laplace transforms (never used in the course);
  contour integration (the Green function comes from a physical argument, not residues);
  matrix eigentheory (waits for 06/07).

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|
| `01-sho` | `content/en/oscillations/01-sho.md` | The simple harmonic oscillator | 1.1 | Georgi, harmonic oscillation; French, SHM chapters | **built** |
| `02-damped-driven` | `content/en/oscillations/02-damped-driven.md` | Damping, resonance, and the quality factor | 1.2 + 1.3 | French, damped & forced vibrations; Georgi; MIT 8.03 resonance lectures | **built** |
| `05-impulse-response` | `content/en/oscillations/05-impulse-response.md` | Impulse response: the oscillator as a linear system | 1.4 | Georgi, LTI/Green-function treatment; MIT 8.03; Goodman, linear-systems preview | planned |

## 4. Shared infrastructure for this part

**`src/wavelab` — existing used:** `oscillators` as built for 01 (`natural_frequency`,
`amplitude_phase`, `position`, `velocity`, `energies`, `damping_rate`, `quality_factor`,
`damping_regime`, `damped_position`, `driven_amplitude`, `max_stable_dt`, `simulate` /
`Trajectory`); `phasors.phasor` / `evaluate` / `real_signal` (02's derivation figures);
`measurement.add_noise` / `fit_cosine` / `frequency_from_zero_crossings` (labs);
`validation.seed_study` / `convergence_study` / `scaling_exponent` / `relative_error`.
Module 05 additionally calls `fourier.convolve`, `fourier.spectrum`, `fourier.exp_decay`,
`fourier.lorentzian_spectrum` — by name only; `fourier.py` is owned by part-00.

**`src/wavelab` — extended: `oscillators.py`** (no new file; its model-spec docstring
exists as built and already covers driven dynamics). After this part the file serves 01,
02, and 05 — the README "Existing" annotation `oscillators (01–02)` gets its one-word
update when 05 lands. All additions below are defined here and nowhere else.
*Reconciliation for part-00:* part-00 §4 cites `oscillators.steady_state_response` for
module 03, deferring the exact name to this plan. The role exists as built in the
*scalar* `driven_amplitude`; this plan defines `steady_state_response` as its vectorized
counterpart (one shared closed form; a limits test pins scalar agreement), so part-00's
citation resolves exactly as written.

```python
steady_state_response(omega, mass, stiffness, damping, force_amplitude=1.0) -> np.ndarray
                       # complex X(omega) = (F0/m)/(omega0^2 - omega^2 - i gamma omega), vectorized
resonance_peak_omega(mass, stiffness, damping) -> float  # omega0 sqrt(1 - 1/(2Q^2)); 0.0 when Q <= 1/sqrt(2)
power_absorbed(omega, mass, stiffness, damping, force_amplitude) -> np.ndarray
                       # cycle-averaged (1/2) gamma m omega^2 |X|^2 [W]; peaks at omega0 exactly
q_from_ringdown(times, positions, threshold=0.1) -> float
                       # as built: Q = omega0/gamma, omega0 from omega_d^2 + gamma^2/4; envelope
                       # from RMS per half cycle, crossings hysteretic (see the as-built note)
q_from_bandwidth(omega, amplitude) -> float    # Q = omega_peak / width between |X|max/sqrt(2) crossings
q_from_phase_slope(omega, phase_lag) -> float  # Q = (omega0/2) d(phase_lag)/d(omega) at the pi/2 crossing;
                       # as built, obtained by fitting omega tan(phi - pi/2) vs omega^2, not by differencing
impulse_response(t, mass, stiffness, damping) -> np.ndarray  # G(t): damped_position(x0=0, v0=1/m), 0 for t<0
step_response(t, mass, stiffness, damping, force_amplitude) -> np.ndarray  # closed form; settles to F0/k
convolution_response(force, dt, mass, stiffness, damping) -> np.ndarray    # causal (G*F) via fourier.convolve
```

**`tests/physics/` additions:**

- *limits:* `steady_state_response` → $F_0/k$ at $\omega \to 0$, $-F_0/(m\omega^2)$ at
  $\omega \to \infty$, scalar agreement with `driven_amplitude`; `resonance_peak_omega`
  → $\wnat$ as damping → 0, 0.0 for $Q \le 1/\sqrt2$; `impulse_response` ≡
  `damped_position(x0{=}0, v0{=}1/m)` on $t \ge 0$; `step_response` → $F_0/k$;
  `spectrum(impulse_response)` ≡ conjugate unit-force response (the LTI-bridge identity).
- *conservation:* steady state — $\langle F\dot{x}\rangle$ = `power_absorbed` =
  $\langle \gamma m \dot{x}^2\rangle$; ringdown energy $\propto e^{-\gamma t}$.
- *convergence:* `simulate` past the transient → `steady_state_response` at
  $O(\Delta t^2)$; `convolution_response` vs `step_response` error $\propto \Delta t^2$.
- *dimensions:* `power_absorbed` in watts against `units`; `q_from_*` dimensionless.
- *scaling:* $Q$ invariant under $(m,k,b) \to (\alpha m, \alpha k, \alpha b)$; response
  curves collapse in $(\omega/\wnat,\ |X|k/F_0)$ at fixed $Q$; $\Delta\omega = \wnat/Q$.
- *seeds:* the three $Q$ extractors agree within uncertainty on one noisy dataset;
  `q_from_ringdown` scatter across $M$ seeds shrinks as $1/\sqrt{M}$.

**Shared media:** `media/render/render_resonance.py` (02) and
`media/render/render_impulse.py` (05); shot lists in §5; `render_sho.py` exists as built.
**Glossary themes:** damping-and-resonance vocabulary (02), linear-systems vocabulary
(05); the oscillation basics were deposited with 01.

## 5. Module specifications

### 5.1 `01-sho` — The simple harmonic oscillator (as built)

**As-built summary.** The page exists and passes the content lints: Galileo's
cathedral-lamp puzzle with the boxed amplitude-independence question; four commit-first
predictions; two animations (`sho-portrait.mp4`, `sho-phase-space.mp4`, rendered by
`media/render/render_sho.py`, present in `content/{en,he}/media/`); full 7-bullet model
spec; derivations covering the equation of motion (`empirical-law` box on Hooke),
amplitude/phase from initial conditions, the cancellation behind isochronism, energy
exchange at $2\wnat$ with the phase-space ellipse, and Taylor-expansion universality
(`approximation` box); a four-check verify section with a `numerical-observation` box on
the symplectic integrator's bounded energy error; transfer bullets (pendulum, LC circuit,
molecules, phonons/quantum) plus the `definition` box for natural frequency; quiz
include; four explain prompts; an advanced section on the pendulum period series,
anharmonicity, and phase-space tori. Objectives `OBJ-01-1..5` in frontmatter. The
artifact family is nearly complete: `01-sho-problems.md` (five objective-tagged
problems), `notebooks/en/labs/01-sho.ipynb`, `notebooks/en/_quiz/01-sho.json`,
`assessment/quizzes/01-sho.en.yml`.

**As-built quiz bank** (`Q-01-1..6`, every objective covered, per-choice feedback):
`Q-01-1` MC period vs amplitude (OBJ-01-3; distractor `amplitude-changes-period`);
`Q-01-2` MC period vs mass (OBJ-01-1, OBJ-01-3); `Q-01-3` MC fastest /
largest-acceleration points (OBJ-01-4; distractor `fastest-at-turning-points`); `Q-01-4`
MC energy over a cycle (OBJ-01-3, OBJ-01-4; distractor `energy-varies-over-cycle`);
`Q-01-5` numeric amplitude from a kick at equilibrium (OBJ-01-1, OBJ-01-2); `Q-01-6` MC
universality via Taylor expansion (OBJ-01-5). The three registry entries assigned here
are `addressed` with real distractors in place, verifiable by `check_assessment.py`.

**Gap list (work this plan tracks; no content rewrite needed):**

1. **HE mirror family missing entirely:** `content/he/oscillations/01-sho.md` and
   `01-sho-problems.md` (parked in `translation-pending.txt`, which must be empty for
   release), `assessment/quizzes/01-sho.he.yml`, `notebooks/he/labs/01-sho.ipynb`,
   `notebooks/he/_quiz/01-sho.json`, plus the `en_source_hash` stamp. `check_parity`
   gates a release until these land; the needed Hebrew terms are already in
   `glossary/terms.yml`.
2. **Prose drift** (README conflict log): "module 02 makes this literal" and
   "modules 02–03" → `06-coupled` / `07-normal-modes`; "module 20" →
   `51-nonlinear-optics`. Fix when those modules exist so the links can be made real.

**Validation gates:** standard per-module set; passing for the EN family, release
blocked on parity until gap 1 closes.

### 5.2 `02-damped-driven` — Damping, resonance, and the quality factor

- **Identity and scope:** notebooks 1.2 + 1.3, merged (§8). Free decay, the three
  damping regimes explored continuously, the driven steady state by complex amplitude,
  $Q$ three ways, the Lorentzian, transient + steady state. Deferred: periodic
  non-sinusoidal drive → `03-fourier-series`; arbitrary forcing → `05-impulse-response`;
  coupling → `06-coupled`; driven anharmonicity → `51-nonlinear-optics`.
- **Prerequisites:** `00-phasors` (complex arithmetic, the $e^{-\ii\omega t}$
  convention); `01-sho` ($\wnat$, energies, phase space, fit-and-report workflow).
- **Learning objectives:**
  - `OBJ-02-1` — Solve m x'' + b x' + k x = 0 in the underdamped, critical, and
    overdamped regimes, classify from gamma = b/m against gamma = 2 omega0, sketch each.
  - `OBJ-02-2` — Solve the driven oscillator by the complex-amplitude method — divide
    out e^(-i omega t) — obtaining X = (F0/m) / (omega0^2 - omega^2 - i gamma omega).
  - `OBJ-02-3` — Read amplitude/phase response curves: lag 0 -> pi/2 -> pi, peak at
    omega0 sqrt(1 - 1/(2 Q^2)) existing only for Q > 1/sqrt(2), |X(omega0)| = Q F0/k.
  - `OBJ-02-4` — Extract Q = omega0/gamma three equivalent ways: energy decay per radian
    of a ringdown, bandwidth Q = omega0/Delta omega, phase slope 2 Q/omega0 at resonance.
  - `OBJ-02-5` — Decompose driven motion into decaying transient plus steady state, and
    estimate the takeover time 2/gamma (about Q/pi periods).
  - `OBJ-02-6` — Identify the high-Q power response as a Lorentzian of FWHM gamma and
    transfer Q-and-bandwidth reasoning to cavities, atoms, and circuits.
- **Mathematical background:** has — complex exponentials, phasor division, quadratic
  roots; introduced — complex *frequency* (decay as $\Imag\,\Omega$), the Lorentzian.
- **Physical intuition goals:** (1) the lag without algebra — in phase slow, opposed
  fast, quarter behind at $\wnat$; (2) a struck high-$Q$ oscillator rings about $Q$
  cycles; (3) resonance is $Q$-fold amplification and takes about $Q$ cycles to build;
  (4) more damping: fewer ringdown cycles *and* wider resonance — one $\gamma$ behind both.
- **Section skeleton seeds:**
  - *puzzle:* a singer holds one note and the wine glass shatters; the same voice louder
    at another pitch does nothing. Boxed: why so violently frequency-dependent — what
    sets the deadly pitch, and how violent? Secondary hook: worn vs good shock absorbers.
  - *predict:* (1) far below $\wnat$ — in phase, opposed, or a quarter behind? (2) does
    the amplitude peak below, at, or above $\wnat$? (targets `resonance-peak-at-omega0`)
    (3) drive at exact $\wnat$ forever — unlimited growth? (targets
    `resonance-grows-forever`) (4) doubling damping — ringdown count and width?
  - *explore:* ringdown sandbox — damping slider sweeping $\gamma/2\wnat$ continuously
    0.05 → 3, live $x(t)$ + phase-space spiral; response explorer — the course's
    signature dual panel, $|X(\omega)|$ over $\varphi_{\text{lag}}(\omega)$, with $Q$
    slider, $\wnat$ line, peak marker, half-power band; transient viewer.
  - *derive:* complex-frequency ansatz → regimes → ringdown energy and $Q$ →
    complex-amplitude method (the phasor payoff) → amplitude and phase → peak position →
    three $Q$ extractions → power and the Lorentzian → steady + transient.
  - *verify:* `simulate` vs closed forms in all regimes; peak-position sweep at several
    $Q$ (the falsifier — the `numerical-observation` box); three $Q$ extractors agreeing
    on one dataset; power balance input = dissipated.
  - *transfer:* `03-fourier-series` — a periodic drive is a comb of harmonics, each
    weighted by this response; `16-light-in-matter` — the Lorentz atom's absorption
    line; `26-fabry-perot` / `44-resonators` — finesse and photon lifetime are $Q$; the
    series RLC circuit (dictionary completed in 05); the tuned mass damper.
  - *quiz:* regime classification; lag reasoning; peak-position and growth-at-resonance
    distractors; numeric $Q$ from bandwidth and ringdown; the three faces of $Q$.
  - *explain:* why swing-pushing works at one rhythm only; $Q$ in one sentence per face;
    why the peak sits *below* $\wnat$; where the dissipated energy goes (and why this
    model cannot answer).
  - *advanced:* displacement vs velocity vs power resonance — $\omega|X|$ peaks
    *exactly* at $\wnat$, previewing impedance (`10-impedance`); the $Q \le 1/\sqrt2$
    world: a peakless low-pass filter.
- **Core derivations:** (1) $x = \Real[C e^{-\ii\Omega t}]$ ⇒
  $\Omega^2 + \ii\gamma\Omega - \wnat^2 = 0$ ⇒ $\Omega = \pm\omega_d - \ii\gamma/2$,
  $\omega_d = \sqrt{\wnat^2 - \gamma^2/4}$ — *loss is the imaginary part of frequency*
  ($n + \ii\kappa$ in 16, cavity linewidth in 44); real forms per regime as in
  `damped_position`. (2) Driven: $X = (F_0/m)/(\wnat^2 - \omega^2 - \ii\gamma\omega)$,
  $\tan\varphi_{\text{lag}} = \gamma\omega/(\wnat^2 - \omega^2)$. (3) Peak: minimize the
  denominator's modulus ⇒ $\omega_{\text{peak}} = \wnat\sqrt{1 - 1/(2Q^2)}$, existing
  iff $Q > 1/\sqrt2$; at resonance $|X(\wnat)| = Q F_0/k$. (4) $Q$ three ways:
  $E \propto e^{-\gamma t}$ ⇒ $Q = \wnat/\gamma$; half-power width $\Delta\omega =
  \gamma$ ⇒ $Q = \wnat/\Delta\omega$; $d\varphi_{\text{lag}}/d\omega|_{\wnat} =
  2/\gamma = 2Q/\wnat$. (5) Power: $\langle P\rangle = \tfrac12\gamma m\omega^2|X|^2$,
  peaking exactly at $\wnat$; at high $Q$, $\langle P\rangle \approx
  \tfrac{F_0^2}{2m\gamma}\,(\gamma/2)^2 / \big[(\omega-\wnat)^2 + (\gamma/2)^2\big]$ —
  the Lorentzian. (6) Steady + transient on $2/\gamma$; from rest at resonance the
  envelope grows as $Q(F_0/k)(1 - e^{-\gamma t/2})$.
- **Model specification draft:** System — point mass, linear spring, linear velocity
  damping, sinusoidal force; observables: position, velocity, energies, mean power.
  Dynamics — $m\ddot{x} = -kx - b\dot{x} + F_0\cos\omega t$; closed forms where they
  exist, velocity Verlet elsewhere. Boundary — none spatially; the environment is a
  featureless energy sink. Ensemble — deterministic; noise only via `wavelab.measurement`.
  Ignored — microscopics of $b$; drive back-reaction; spring nonlinearity. Valid when —
  displacements linear, damping genuinely viscous, steady-state claims wait out the
  transient. Failure modes — dry friction; resonant amplitudes leaving the linear
  regime; transient data read as steady state; any question about the heat.
- **Epistemic classification:** viscous damping $F = -b\dot{x}$ — `model-assumption`
  (the boxed one); steady-plus-transient decomposition — `theorem`;
  $\omega_{\text{peak}}$ and the $Q$ equivalences — `theorem`; measured peak positions
  across $Q$ — `numerical-observation`; near-resonance Lorentzian — `approximation`;
  $Q$ — `definition`.
- **Misconceptions:** registry `resonance-peak-at-omega0` (pending → **addressed**
  here). Falsifier: amplitude-response sweeps at several damping values show the peak at
  $\wnat\sqrt{1 - 1/(2Q^2)}$ — below $\wnat$, farther as damping grows, absent for
  $Q < 1/\sqrt2$; plotted as $\omega_{\text{peak}}/\wnat$ vs $1/Q^2$ on the predicted
  line. Distractor: `Q-02-3`. NEW `resonance-grows-forever` — "Driving at resonance
  makes the amplitude grow without limit." Falsifier: integrate from rest at
  $\omega = \wnat$ with damping; the envelope saturates at $Q F_0/k$ after $\sim Q/\pi$
  periods — $Q$-fold amplification, not divergence. Distractor: `Q-02-4`.
- **Glossary terms:** `underdamped` (תת-ריסון), `overdamped` (ריסון-יתר),
  `critical-damping` (ריסון קריטי), `transient` (תגובת מעבר), `steady-state`
  (מצב מתמיד), `phase-lag` (פיגור מופע), `lorentzian` (לורנציאן), `ringdown`
  (דעיכה חופשית — translator to decide; `he_reject` candidate: רינגדאון), `bandwidth`
  (רוחב פס — deposited here; `04-fourier-transform` cites the same key).
- **Interactive controls and simulations:** ringdown morph ($\gamma/2\wnat \in
  [0.05, 3]$, log slider); response explorer ($Q \in [0.5, 50]$, $\omega/\wnat \in
  [0, 3]$; dual panel); transient viewer; $Q$-bench — one hidden oscillator, three tabs
  (ringdown / sweep / phase), each yielding a $Q$ estimate.
- **Virtual lab outline** (`notebooks/en/labs/02-damped-driven.ipynb`): (1) ringdowns
  across the regimes, $\omega_d$ vs $\sqrt{\wnat^2 - \gamma^2/4}$; (2) $Q$ via
  `q_from_ringdown`; (3) steady-state sweep at ~30 drive frequencies past the transient,
  amplitude and lag vs `steady_state_response`; (4) $Q$ from bandwidth and phase slope;
  all three as value ± uncertainty with mutual agreement (the measurement-culture
  result); (5) the peak-position experiment across damping values — the falsifying
  plot; (6) repeat (3) with `measurement.add_noise` under `validation.seed_study`.
- **Real-experiment counterpart:** a hacksaw blade or ruler clamped to a table edge with
  a phone (accelerometer app, e.g. phyphox) taped to the free end: record a ringdown,
  export CSV, import, fit $f_d$ and $\gamma$, report $Q$ ± uncertainty.
- **Media assets** (`render_resonance.py`): (a) one oscillator released repeatedly as
  damping sweeps through the regimes — trajectory + phase-space spiral; (b) drive
  frequency slowly ramped through resonance — amplitude envelope tracing $|X(\omega)|$
  on an adjacent panel, arrows showing the lag rotate 0 → $\pi/2$ → $\pi$. No text.
- **Quiz bank outline:** `Q-02-1` MC regime from $(m,k,b)$ (OBJ-02-1); `Q-02-2` MC lag
  at low/resonant/high drive (OBJ-02-2, OBJ-02-3); `Q-02-3` MC peak position (OBJ-02-3;
  distractor `resonance-peak-at-omega0`); `Q-02-4` MC exact-resonance driving forever
  (OBJ-02-5; distractor `resonance-grows-forever`); `Q-02-5` numeric $Q$ from FWHM
  (OBJ-02-4, OBJ-02-6); `Q-02-6` numeric ringdown cycles to $1/e$ given $Q$ (OBJ-02-1,
  OBJ-02-4); `Q-02-7` free — the three faces of $Q$ (OBJ-02-4, OBJ-02-6).
- **Problem set outline:** analytical — derive $\omega_{\text{peak}}$ and the
  $Q > 1/\sqrt2$ condition; energy per cycle → $Q = 2\pi E/\Delta E$; overdamped motion
  crosses zero at most once; series RLC ringdown $Q$. Computational — sweeps at
  $Q = 0.6$ and $Q = 3$: the peak's disappearance; build-up envelope vs
  $Q(F_0/k)(1-e^{-\gamma t/2})$. Challenge — shock-absorber design: choose $b$
  minimizing settling time to 1%; why slightly under critical wins.
- **Runtime budget:** closed forms carry the sweeps; Verlet only for transients and the
  lab sweep — ≈ $3\times10^5$ steps total, seconds in Pyodide; animations ≤ 300 frames.
- **Validation gates:** standard set with `--module 02-damped-driven`; the §4
  `steady_state_response` tests land with this module — part-00's module 03 cites them.
- **Open questions, as resolved when built:** the glass-shatter hook leads and the swing
  moved into *explain*; the velocity/power-resonance distinction lives in *advanced*, where
  it also carries the impedance preview; the laboratory's three $Q$ routes all interrogate
  one hidden oscillator, since "same number, three costumes" is the lesson.
- **As-built deviations from this section.** Three, each forced by the data rather than by
  taste. (1) `q_from_ringdown` returns $\wnat/\gamma$ with $\wnat$ reconstructed from
  $\omega_d^2 + \gamma^2/4$, not the shorthand $\omega_d/\gamma$ this section wrote: the
  shorthand is a percent low at $Q \sim 2$, inside the regime the module's own sweep
  explores. (2) The same function needed a hysteresis threshold and an RMS-per-half-cycle
  envelope to survive noisy data at all — naive crossing counting returned $Q \approx 1160$
  for a true $Q = 20$. (3) `q_from_phase_slope` fits the exactly-linear form
  $\omega\tan(\varphi - \pi/2)$ against $\omega^2$ rather than differencing the sweep;
  numerically differentiating measured phase put a 17% scatter on $Q$. All three are
  documented in the function docstrings and pinned by tests.

### 5.3 `05-impulse-response` — Impulse response: the oscillator as a linear system

- **Identity and scope:** notebook 1.4, expanded (§8). Green function $G(t)$, arbitrary
  forcing as convolution, $\hat{G}$ as the complex frequency response, causality, the
  mechanical–electrical dictionary. Deferred: spatial impulse response → `40-psf-otf`;
  deconvolution in earnest → `53-computational-imaging`; Green functions of wave
  equations → Part III and `28-huygens`.
- **Prerequisites:** `02-damped-driven` ($X$, $Q$, transient vs steady state);
  `04-fourier-transform` (convolution theorem, `fourier.spectrum`, exponential ↔
  Lorentzian pair, operational deltas); `01-sho` (a kick sets $v_0$); `00-phasors` (the
  two-sided spectrum of a real signal).
- **Learning objectives:**
  - `OBJ-05-1` — Define the impulse response G(t) as the motion after a unit impulse:
    G(t) = e^(-gamma t/2) sin(omega_d t) / (m omega_d) for t >= 0, zero before, and
    account for each feature (starts at zero, slope 1/m, rings at omega_d, decays at
    gamma/2).
  - `OBJ-05-2` — Predict the response to an arbitrary force as the convolution
    x(t) = (G*F)(t) = integral up to t of G(t - t') F(t') dt', read as a superposition
    of kicks, and evaluate it numerically for steps, ramps, and bursts.
  - `OBJ-05-3` — State that the Fourier transform of G is the complex frequency
    response H(omega) = (1/m) / (omega0^2 - omega^2 + i gamma omega), connect it to
    module 02's steady-state amplitude, and use x_hat = H F_hat.
  - `OBJ-05-4` — Use causality (G = 0 for t < 0) to constrain any response: nothing
    moves before the force starts, and x(t) cannot depend on F(t') for t' > t.
  - `OBJ-05-5` — Translate the oscillator into the series RLC circuit via m <-> L,
    b <-> R, k <-> 1/C (x <-> q, F <-> V), carrying G, Q, and H(omega) unchanged.
- **Mathematical background:** has — convolution theorem and pair zoo (04), complex
  response (02); introduced — the Green-function idea (named), the
  superposition-of-kicks limit, the two-sided spectrum of a causal signal.
- **Physical intuition goals:** (1) hit anything and it rings at *its own* frequency —
  the kick chooses amplitude, never pitch; (2) the response outlives the force: the
  oscillator *remembers being kicked* for $\sim 2/\gamma$; (3) slow forcing is tracked
  quasi-statically at $F/k$, fast wiggles average away; (4) one kick contains every
  frequency, so a single ringdown FFT reproduces module 02's whole resonance curve.
- **Section skeleton seeds:**
  - *puzzle:* strike a bell with wood, steel, or felt — loudness and brightness change,
    the pitch never does. Boxed: why can no mallet choose the note — and how can an
    engineer, hearing one strike, recover the *entire* resonance curve that module 02
    needed a frequency sweep to measure?
  - *predict:* (1) two identical kicks one period apart — bigger, cancelled, unchanged?
    at half a period? (2) a constant force switched on: smooth glide to $F_0/k$ or
    overshoot and ring? (targets `response-follows-force-shape`) (3) can the mass move
    before the kick — can $x(t)$ depend on the force's future? (4) a burst at $\wnat$
    of 3 cycles vs 30 — roughly what response ratio?
  - *explore:* kick sandbox — click the time axis to drop kicks; each spawns a faint
    ringdown, the bold curve is their sum (convolution made visible); forcing gallery —
    step, ramp, resonant and detuned bursts, seeded noise; three-spectra view —
    $|\hat{F}|$, $|\hat{H}|$, $|\hat{x}| = |\hat{H}||\hat{F}|$ side by side (the §22
    motif); RLC toggle relabelling axes ($x \to q$, $F \to V$).
  - *derive:* impulse $J$ → $v_0 = J/m$ → $G$ as unit-kick free decay → linearity +
    time invariance → force as a train of kicks → convolution with causal upper limit →
    $\hat{G}$ via the one-sided-exponential integral (04's pair) → identity with module
    02's $X$ → $\hat{x} = \hat{H}\hat{F}$ → step response → the RLC dictionary.
  - *verify:* `convolution_response` vs `simulate` for step, ramp, burst, noise (same
    trajectory at $O(\Delta t^2)$); `fourier.spectrum(impulse_response)` overlaid on
    the conjugate `steady_state_response` — the LTI bridge measured, the
    `numerical-observation` box; two-kick experiment (period-spaced doubles,
    half-period cancels); step overshoot vs closed form across $Q$.
  - *transfer:* `40-psf-otf` — **say it explicitly:** $G$ is the point spread function
    of time, $\hat{H}$ the OTF; imaging is this module with $t \to (x,y)$;
    `16-light-in-matter` — the atom as a kicked oscillator, its absorption line the
    $|\hat{H}|$ of the Lorentz model; `26-fabry-perot` / `44-resonators` — cavity
    ring-down as the optical kick experiment; `28-huygens` — secondary wavelets as
    spatial impulse responses; the RLC table as a standing invitation to electronics.
  - *quiz:* kick-timing interference; step-onset distractor; causality constraints;
    $\hat{G} \leftrightarrow$ Lorentzian identification; RLC numeric.
  - *explain:* why the bell's pitch ignores the mallet; what, physically, is the
    oscillator's "memory" and what sets its duration; convolution in words, no
    integral signs; what absurdity follows if $G(t) \ne 0$ for $t < 0$.
  - *advanced:* the name "Green function" and the ODE view
    $m\ddot{G} + b\dot{G} + kG = \delta(t)$; the anti-causal solution and why we
    discard it; deconvolution — noise exploding where $|\hat{H}|$ is small (bridge to 53).
- **Core derivations:** (1) a spike of impulse $J$ changes only the velocity,
  $v(0^+) = J/m$; hence
  $G(t) = \Theta(t)\,e^{-\gamma t/2}\sin(\omega_d t)/(m\,\omega_d)$ — precisely
  `damped_position` with $x_0 = 0$, $v_0 = 1/m$: *the impulse response is a free
  oscillation launched by a kick.* (2) Superposition of kicks:
  $x(t) = \int_{-\infty}^{t} G(t-t')F(t')\,dt' = (G*F)(t)$, upper limit $t$ by
  causality. (3) Under the course's forward transform,
  $\hat{G}(\omega) = (1/m)/(\wnat^2 - \omega^2 + \ii\gamma\omega)$, and the module-02
  amplitude is $X = F_0\,\hat{G}(-\omega_{\text{dr}}) = F_0\,\hat{G}(\omega_{\text{dr}})^{*}$:
  the phasor sits in the *negative*-frequency half of the spectrum, closing the thread
  part-00 opened <!-- author note: the sign of the i gamma omega term differs between
  spectrum-side H and phasor-side X; getting it wrong flips the lag -->.
  (4) Convolution theorem: $\hat{x} = \hat{G}\hat{F}$ — 02's sweep and 05's kick are
  one fact in two domains. (5) Step response by convolution:
  $x(t) = (F_0/k)\big[1 - e^{-\gamma t/2}\big(\cos\omega_d t +
  \tfrac{\gamma}{2\omega_d}\sin\omega_d t\big)\big]$, $t \ge 0$ — overshoot and ringing
  from a featureless force. (6) Dictionary: $L\ddot{q} + R\dot{q} + q/C = V(t)$ with
  $m \leftrightarrow L$, $b \leftrightarrow R$, $k \leftrightarrow 1/C$;
  $Q = \sqrt{L/C}/R$; same $G$, same Lorentzian.
- **Model specification draft:** System — the module-02 oscillator viewed as a map from
  force history to displacement history; observables are input–output pairs and their
  spectra. Dynamics — the same equation of motion; solutions represented as $G*F$.
  Boundary — at rest before the force begins (the causal condition selecting this $G$);
  environment sink as in 02. Ensemble — deterministic; noisy-force cells seeded via
  `wavelab.measurement`. Ignored — damping microscopics; any nonlinearity
  (superposition of kicks *is* linearity). Valid when — response linear, force bounded
  and starting at a finite time, sampling step well below $2\pi/\omega_d$ and the
  force's fastest feature. Failure modes — nonlinear springs (kicks stop superposing);
  discrete convolution above Nyquist; naive deconvolution amplifying noise.
- **Epistemic classification:** $G$ from linearity + the equation of motion —
  `theorem`; "any force is a limit of kick trains" — `theorem` (operational deltas
  flagged as in 04); the causal choice of Green function — `model-assumption` (the
  boxed one: anti-causal solutions exist and are discarded on physical grounds);
  measured $\hat{G} \leftrightarrow \hat{H}$ agreement — `numerical-observation`; the
  RLC correspondence — `theorem` (same equation, renamed symbols).
- **Misconceptions:** NEW `response-follows-force-shape` — "A linear system's
  displacement follows the shape of the force applied to it." Falsifier: a spike of
  force produces seconds of ringing (response outlives the force) and a constant step
  force overshoots and oscillates on its way to $F_0/k$ — both measured with
  `convolution_response` and `simulate` agreeing. Distractor: `Q-05-3`'s option that
  the mass glides monotonically to its new equilibrium. (Registry gains this id,
  pending → addressed when the module is built.)
- **Glossary terms:** `impulse-response` (תגובת מתקף — consistent with the deposited
  מתקף; translator to weigh the EE-standard תגובת הלם; `he_reject` candidate: תגובת
  אימפולס), `green-function` (פונקציית גרין), `causality` (סיבתיות),
  `linear-time-invariant` (מערכת ליניארית קבועה בזמן), `step-response` (תגובת מדרגה),
  `frequency-response` (תגובת תדר). `convolution` is listed by part-00 (04), cited only.
- **Interactive controls and simulations:** kick sandbox (kick times/strengths, $Q$
  slider); forcing gallery (preset, duration, detuning; $F(t)$ and $x(t)$ stacked);
  three-spectra view (live $|\hat{F}|$, $|\hat{H}|$, $|\hat{x}|$); RLC relabel toggle.
- **Virtual lab outline** (`notebooks/en/labs/05-impulse-response.ipynb`): (1) one
  kick — $\omega_d$, $\gamma$ from the ringdown; (2) FFT the ringdown via
  `fourier.spectrum`, overlay `fourier.lorentzian_spectrum` and the module-02 swept
  response: *the resonance curve from one kick*; (3) kick trains — period vs
  half-period spacing vs prediction; (4) `convolution_response` vs `simulate` for step,
  ramp, burst; overshoot vs $Q$; (5) *measurement:* noisy kick data across seeds —
  report $Q_{\text{kick}}$ (linewidth) and $Q_{\text{ring}}$ (envelope) as value ±
  uncertainty and test agreement (the module's punchline). **The envelope route must call
  `oscillators.q_from_ringdown`, not a fresh crossing counter written for this notebook.**
  That function grew a hysteresis threshold and an RMS-per-half-cycle envelope when 02 was
  built precisely because naive extraction returns $Q \approx 1160$ on a true $Q = 20$ once
  the tail decays into the noise (§5.2, as-built deviations). A broken estimator here does
  not read as a failed agreement test — it reads as a broken notebook, and it would break
  the one step the module is built around. **$Q_{\text{kick}}$ likewise comes from *fitting*
  `fourier.lorentzian_spectrum` to the ringdown spectrum, not from half-power crossings on
  raw FFT bins** — step (2) already overlays that curve, so this costs the lab nothing but
  turns an overlay into a measurement with an uncertainty step (5) can use. The reason is
  arithmetic, not noise: bin spacing $2\pi/T$ puts $\gamma T/2\pi = n/\pi$ bins across the
  FWHM for a record of $n$ amplitude e-folding times — $1.6$ bins at five — *independent of
  $Q$*, so the crossings are under-resolved before any noise arrives, and recording longer
  is not the escape it looks like ($10$ bins needs $31$ e-foldings, where the signal is
  $10^{-14}$ of its start). Zero-padding interpolates the lineshape and adds no information.
  Note that `q_from_bandwidth` will accept FFT bins and $|\hat{G}|$ without complaint, since
  both are just arrays: this is a trap, not a type error. Its contract assumes a *driven*
  sweep the experimenter can sample as finely as they like — a freedom module 02 had and a
  ringdown, whose bin spacing is set by the same $\gamma$ that sets its linewidth, does not.
- **Real-experiment counterpart:** strike a wine glass or tuning fork by a phone
  microphone; record WAV; import via `scipy.io.wavfile` (part-00's path); FFT the
  ring → $f_0$ and $Q$ from the linewidth, cross-checked against the audible decay
  time — the two-faces-of-$Q$ loop closed with real data.
- **Media assets** (`render_impulse.py`): (a) hammer flash → ringdown; then a train of
  randomly timed kicks, each spawning a faint ringdown, the faint curves summing into
  the bold response — convolution as superposition, the money shot; (b) step responses
  at several $Q$ side by side, overshoot growing with $Q$. No burned-in text.
- **Quiz bank outline:** `Q-05-1` MC what a harder mallet changes (OBJ-05-1); `Q-05-2`
  MC two kicks a half-period apart (OBJ-05-2); `Q-05-3` MC step-force onset (OBJ-05-2,
  OBJ-05-4; distractor `response-follows-force-shape`); `Q-05-4` MC which curve is
  $|\hat{G}|$, $Q$ read from a plotted linewidth (OBJ-05-3); `Q-05-5` MC which response
  features causality forbids (OBJ-05-4); `Q-05-6` numeric — $f_0$ and $Q$ of a series
  RLC from component values, mapped back to $(m,b,k)$ (OBJ-05-5).
- **Problem set outline:** analytical — step response by convolution; overshoot
  fraction vs $\gamma/2\wnat$; response to $F_0 e^{-t/\tau}\Theta(t)$ two ways —
  convolution and $\hat{H}\hat{F}$ — shown to agree. Computational — estimate $\hat{H}$
  from noisy kick data across seeds; compare $Q$ estimators. Challenge —
  deconvolution: recover $F$ from $x$ by spectral division, add noise, watch the
  wreckage, rescue with crude truncation; why `53-computational-imaging` needs better.
- **Runtime budget:** arrays ≤ $2^{14}$ samples; convolutions via `fourier.convolve`
  (FFT-based); a handful of FFTs per cell — sub-second in Pyodide.
- **Validation gates:** standard set with `--module 05-impulse-response`; the
  $\hat{G} \leftrightarrow \hat{H}$ identity test (§4 *limits*) must land with this
  module — part-11's plan will cite it as the LTI-bridge guarantee.
- **Open questions for the author:** whether the Green-function *name* leads or trails
  (recommend physics first, name in advanced); deconvolution teaser in advanced or
  deferred wholly to 53 (recommend one falling-apart demo, no theory); RLC toggle on
  the live sandbox vs a static figure.

## 6. Part-level assessment and capstone hooks

- The cross-module synthesis problem promised in part-00 §6 lands with this part, in
  `05-impulse-response-problems.md`: drive the damped oscillator with a noisy square
  wave; predict the response spectrum as $c_n \times$ Lorentzian (02 + 03), verify by
  FFT (04), re-derive as $\hat{G}\hat{F}$ (05) — one problem touching modules 00–05.
- Capstone §35.3 (grating spectrometer) reuses $Q$-and-bandwidth reasoning as resolving
  power; §35.4 (optical communication) consumes $\hat{H}$ thinking directly; §35.1
  (computational telescope) and §35.5 (4-f processor) inherit the LTI bridge through
  `40-psf-otf`, which 05 seeds.
- Exam themes: sketch $x(t)$ for a given regime; extract $Q$ three ways from supplied
  plots and reconcile; kick-timing reasoning without integrals; translate a mechanical
  spec sheet into RLC and back.

## 7. Build order and validation gates

Build `02-damped-driven` first: part-00's module 03 consumes
`oscillators.steady_state_response`, and the registry's pending oscillations entry
(`resonance-peak-at-omega0`) is addressed there. Then `05-impulse-response`, strictly
*after* part-00 builds 04 (05 consumes `fourier.convolve`, `fourier.spectrum`, and the
exponential ↔ Lorentzian pair). The cross-part sequence — agreed with part-00 §7 — is
`02 → 03 → 04 → 05`.

With `02-damped-driven` (**done**): the §5.2 glossary terms are deposited (`bandwidth`
among them, cited by part-00's 04); registry entry `resonance-grows-forever` added and
`resonance-peak-at-omega0` flipped to `addressed`; the `steady_state_response`,
`resonance_peak_omega`, `power_absorbed` and `q_from_*` tests have landed across all six
accuracy categories, and `media/render/render_resonance.py` renders the two animations.
With
`05-impulse-response`: deposit the §5.3 glossary terms; add NEW registry entry
`response-follows-force-shape`; land the `impulse_response`, `step_response`,
`convolution_response`, and $\hat{G}$-identity tests. Closing 01's gap list (§5.1, the
HE mirror family) can proceed in parallel and is required before any release.

Per module, the standard four gates (README): `check_modelspec.py`,
`check_assessment.py`, `pytest tests/physics -k <topic>`, `validate_all.py`.

## 8. Deviations from the master plan

- **Merge (1.2 + 1.3 → `02-damped-driven`):** free damped decay is the $F_0 = 0$ limit
  and the *transient* of the driven solution; regimes and the resonance curve fall out
  of one complex-root analysis, and separately each notebook is too thin to carry the
  module contract. The canonical map and the misconception registry already reserve the
  merged id; README notes the precedent.
- **Resequencing:** Fourier modules 03/04 are taught *between* 02 and 05 (just-in-time;
  decision owned by part-00 §8 — restated here only because this part's build order
  depends on it).
- **Scope expansion of 1.4:** the master plan gives notebook 1.4 four lines; this plan
  makes `05-impulse-response` the course's LTI keystone — Green function named,
  causality a boxed model assumption, $\hat{G} \leftrightarrow \hat{H}$ verified
  numerically, the RLC dictionary a transfer target, the forward link to `40-psf-otf`
  stated in content rather than implied.
- **Additions beyond §8:** the three-equivalent-ways treatment of $Q$; the
  displacement/velocity/power resonance-peak distinction (amplitude peaks below
  $\wnat$, power exactly at it); the Lorentzian named as the course-wide universal
  resonance shape with forward seeds (16, 26, 44); two NEW registry misconceptions
  (`resonance-grows-forever`, `response-follows-force-shape`).
- **Terminology:** the course fixes $\gamma \equiv b/m$ with amplitude decay
  $e^{-\gamma t/2}$ and $Q = \wnat/\gamma$ (as built in `oscillators.py`); several
  textbooks (French among them) use $\gamma = b/2m$. Content states the choice once, in
  02's derive section, and never mixes conventions.
