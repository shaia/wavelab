# Part 0 — Mathematical and Computational Foundations — Implementation Plan

> **Master plan:** §7 (Part 0). **Modules:** `00-phasors`, `03-fourier-series`, `04-fourier-transform`. **Status:** partial — `00-phasors` built.
> Canonical numbering, invariants, and conflict log: [README.md](README.md).

## 1. Part overview and narrative arc

Part 0 builds the course's mathematical language: complex amplitudes for single
oscillations, Fourier series for periodic signals, and the Fourier transform for
everything else. The master plan treats these as three preliminary notebooks; this plan's
refinement is to treat them as three *physical* modules with their own puzzles, labs, and
measurements — and to weave them into the oscillations arc rather than front-loading them
as mathematics (the sequencing argument is in §8).

The through-line is a single escalating claim: **any signal is a sum of rotating arrows.**
Module 00 establishes the arrow itself — one frequency, one complex amplitude — and
already extracts physics from pure arithmetic: interference, beats, and the $\sqrt{N}$
random walk that separates a light bulb from a laser. Module 03 makes the sum countable:
a periodic signal is a comb of harmonics, and *which* harmonics, with *what* weights, is
answerable by symmetry before any integral is computed. Module 04 makes the sum
continuous, and adds the two theorems the rest of the course runs on: the convolution
theorem (module 05's impulse response, module 40's point spread function, module 29's
double slit) and the bandwidth theorem $\Delta t\,\Delta\omega \ge \tfrac12$ (module 27's
coherence length, module 43's beam divergence — the same inequality in three costumes).

Two enhancements run through the whole part. First, the **transform-pair zoo** —
$\operatorname{rect} \leftrightarrow \operatorname{sinc}$, Gaussian ↔ Gaussian,
decaying exponential ↔ Lorentzian, comb ↔ comb — is introduced as a set of *visual
reflexes*, drawn identically every time they recur (the master plan's §22 "three
synchronized representations" and §31's insistence that diffraction should feel like a
Fourier pair already known). Second, the **DFT/FFT bridge** is treated as first-class
physics, not numerics: every later laboratory computes spectra of sampled, noisy data, so
sampling, aliasing, Nyquist, and leakage are taught here once, with measurements, and
never re-derived.

Because the course convention puts the time factor at $e^{-\ii\omega t}$ while the
forward transform carries $e^{-\ii\omega t}$ as well (the `numpy.fft` sign — see
`src/wavelab/constants.py`), the phasor of module 00 lives in the *negative*-frequency
half of a numerical spectrum. That is not a nuisance to hide but a fact to teach: it is
the analytic-signal idea previewed in 00's advanced section, and module 04 closes it.

## 2. Position in the course

- **Requires:**
  - `00-phasors`: nothing — the course entry point.
  - `03-fourier-series`: `00-phasors` (phasor addition, the superposition theorem for one
    frequency); `02-damped-driven` (the Lorentzian response curve and the meaning of
    steady state — the module's driving application).
  - `04-fourier-transform`: `03-fourier-series` (coefficients, orthogonality, the
    $T \to \infty$ limit is taken literally).
- **Feeds (selection — this part feeds everything):**
  - `05-impulse-response`: convolution theorem, $\hat{G}(\omega)$ as complex response.
  - `11-standing-waves`: mode decomposition = Fourier series on a finite string.
  - `12-wave-packets` / `13-dispersion`: packets as $A(k)$ superpositions; bandwidth
    theorem → spreading.
  - `27-coherence`: Wiener–Khinchin; coherence time as $1/\Delta\omega$.
  - `29-fraunhofer` and all of parts IX/XI: diffraction as the transform of the aperture;
    the pair zoo becomes hardware.
- **Explicitly not assumed:** convergence theory beyond piecewise-smooth signals;
  distribution theory (delta functions are used operationally, flagged as such); any wave
  or spatial concept — Part 0 is strictly signals in time, so that space enters
  only once, properly, in Part III.

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|
| `00-phasors` | `content/en/foundations/00-phasors.md` | Phasors: the language of waves | 0.1 | Georgi, harmonic oscillation & complex notation; French, superposition | **built** |
| `03-fourier-series` | `content/en/foundations/03-fourier-series.md` | Fourier series: periodic signals as harmonic sums | 0.2 | Georgi, Fourier series; MIT 8.03 Fourier lectures | planned |
| `04-fourier-transform` | `content/en/foundations/04-fourier-transform.md` | The Fourier transform and convolution | 0.3 | Georgi, Fourier integrals; Goodman, Fourier analysis background (preview) | planned |

## 4. Shared infrastructure for this part

**`src/wavelab` — existing used:** `phasors.real_signal`, `phasors.superpose` (00, and
the epicycle view in 03); `oscillators.steady_state_response` (03's driven application —
exact name per `oscillators.py` as built in part-01's plan); `measurement` (noisy-signal
experiments in both new labs); `validation` (convergence and Parseval checks).

**`src/wavelab` — new: `fourier.py`** (introduced and owned by this part; README
ownership table). Docstring model spec:

- **System:** real time-signals — periodic (coefficient arrays) or sampled aperiodic
  (arrays at spacing `dt`) — and their complex spectra.
- **Dynamics:** none; analysis and synthesis of given signals.
- **Boundary:** periodic signals repeat exactly; sampled signals are treated by the DFT
  as one period of a periodic signal — that fiction is the module's central caveat.
- **Ensemble:** deterministic; callers add noise via `wavelab.measurement`.
- **Ignored:** distribution-theory rigour; convergence beyond piecewise-smooth.
- **Valid when:** bandwidth below Nyquist (`|omega| < pi/dt`); windows long against
  signal features.
- **Failure modes:** aliasing, leakage read as physics, magnitude-only reconstruction.

Function-level sketch (signatures + contracts):

```python
fourier_coefficients(samples, n_max) -> c        # c[-n_max..n_max] by trapezoid integral over one period
partial_sum(c, omega0, t) -> x                   # synthesis sum, real output for conjugate-symmetric c
square_coefficients(n_max) / triangle_coefficients / sawtooth_coefficients / pulse_train_coefficients(duty, n_max)
                                                 # closed forms, the reference the numerics are tested against
spectrum(samples, dt) -> (omega, F)              # scaled, fftshifted FFT; forward sign e^{-i omega t}
inverse_spectrum(F, dt) -> samples               # round-trips spectrum() to machine precision
rect_pulse(t, width) / sinc_spectrum(omega, width)
gaussian_pulse(t, sigma) / gaussian_spectrum(omega, sigma)
exp_decay(t, tau) / lorentzian_spectrum(omega, tau)
                                                 # the analytic pair zoo, for overlaying on FFT output
convolve(f, g, dt) -> h                          # numerical convolution normalised so spectrum(h) = spectrum(f)*spectrum(g)
gibbs_overshoot(n_max) -> float                  # measured max overshoot of the square partial sum
rms_widths(samples, dt) -> (dt_rms, domega_rms)  # RMS duration and bandwidth for the uncertainty product
```

**`tests/physics/` additions:**

- *limits:* `spectrum(rect_pulse)` matches `sinc_spectrum` (zero-padded, `<1e-10`);
  Gaussian pair likewise; `exp_decay` → Lorentzian half-width $1/\tau$.
- *convergence:* square-wave partial-sum $L^2$ error $\propto N^{-1/2}$, triangle
  $\propto N^{-3/2}$ (smoothness ↔ decay); `gibbs_overshoot(N)` → 8.95% constant in $N$.
- *conservation:* Parseval both discrete (`sum |c_n|^2` = mean square) and sampled
  (energy in time = energy in spectrum / $2\pi$).
- *scaling:* time-scaling theorem $f(at) \leftrightarrow F(\omega/a)/|a|$; the
  uncertainty product from `rms_widths` invariant under time scaling.
- *dimensions:* `spectrum` frequency axis in rad/s against `units` registry.
- *seeds:* averaged periodogram noise floor $\propto 1/\sqrt{M}$ over $M$ seeded
  realisations.

**Shared media:** one render script `media/render/render_fourier.py` produces the MP4s of
both new modules (shot lists in §5). **Glossary themes:** harmonic analysis vocabulary
(§5 per module) — first real waves/optics deposits into `glossary/terms.yml`.

## 5. Module specifications

### 5.1 `00-phasors` — Phasors: the language of waves (as built)

**As-built summary.** The page exists and passes the content lints: noise-cancelling
headphones puzzle; four commit-first predictions (including the violinists' $N$ vs $N^2$);
two referenced animations; full model spec; derivations covering Euler representation,
the one-frequency superposition theorem (boxed `theorem`), the interference law
$A^2 = A_1^2 + A_2^2 + 2A_1A_2\cos\delta$, beats, and the random-phase walk
$\langle|\sum e^{-\ii\varphi_k}|^2\rangle = N$; a four-check verify section with a
`numerical-observation` box (fitted exponent $p = 0.52$); transfer bullets to
interference, diffraction, coherence, AC circuits, quantum amplitudes; an advanced
section on energy bookkeeping, the rotating frame, and negative frequencies. Objectives
`OBJ-00-1..5` as in the frontmatter. Registry entries `superposition-always-adds` and
`phase-is-unphysical` are assigned here with `status: addressed`.

**Gap list (work this plan tracks; no content rewrite needed):**

1. `media/render/render_phasors.py` does not exist — the page references
   `../media/phasor-superposition.mp4` and `../media/beats.mp4`. Shot list implied by the
   captions: (a) two same-frequency phasors tip-to-tail + projection, $\delta$ sweep;
   (b) rotating-frame beats + pulsing envelope.
2. `notebooks/en/labs/00-phasors.ipynb` does not exist — the page links it, and
   `build_site.verify_lite` fails the full build until it lands. Lab outline: phasor
   sandbox (per-arrow length/angle sliders) → $\delta$ sweep with resultant-length
   readout → 1% detuning in the rotating frame → $N$ random phasors with re-roll and
   RMS-vs-$N$ fit (the $p \approx 0.5$ measurement quoted by the page).
3. `assessment/quizzes/00-phasors.{en,he}.yml` do not exist though the page includes
   `../_generated/quiz-00-phasors.md`, and the two `addressed` registry entries need
   their distractors to actually exist. Outline: `Q-00-1` interference-law numeric
   (OBJ-00-2); `Q-00-2` largest/smallest resultant MC (OBJ-00-2, distractor from
   `superposition-always-adds`); `Q-00-3` beats MC (OBJ-00-3); `Q-00-4` violinists MC
   (OBJ-00-4); `Q-00-5` convention MC (OBJ-00-5); `Q-00-6` measurable-phase MC
   (OBJ-00-1, distractor from `phase-is-unphysical`).
4. No HE mirror (`content/he/foundations/`) and no glossary deposits (phasor,
   superposition, beat, coherent/incoherent, phase). `check_parity` gates a release
   until mirrored or listed in `translation-pending.txt`.
5. Prose drift ("module 8", "module 9", "module 1.3") — README conflict log; fix when
   the referenced modules exist.

**Validation gates:** standard per-module set once 1–4 land.

### 5.2 `03-fourier-series` — Fourier series: periodic signals as harmonic sums

- **Identity and scope:** master-plan notebook 0.2. Periodic signals only; the
  $T \to \infty$ limit is deliberately deferred to `04-fourier-transform`.
- **Prerequisites:** `00-phasors` (arrows, one-frequency theorem); `02-damped-driven`
  (Lorentzian response, steady state) — see §8 for the ordering.
- **Learning objectives:**
  - `OBJ-03-1` — Compute Fourier coefficients c_n = (1/T) integral of f(t) e^(i n omega0 t) dt
    via orthogonality, and interpret |c_n| and arg(c_n) as the amplitude and phase of the
    nth harmonic's phasor.
  - `OBJ-03-2` — Predict from symmetry which harmonics a waveform contains (odd/even,
    half-wave symmetry) before computing any integral.
  - `OBJ-03-3` — Relate smoothness to coefficient decay (jump -> 1/n, corner -> 1/n^2)
    and identify the Gibbs overshoot as a fixed property of partial sums at jumps.
  - `OBJ-03-4` — Predict the steady-state response of a damped driven oscillator to a
    periodic non-sinusoidal drive by weighting each harmonic with the Lorentzian response.
  - `OBJ-03-5` — Convert between time-domain and spectrum descriptions of square,
    triangle, sawtooth, and pulse-train signals.
- **Mathematical background:** has — complex arithmetic, phasors, integration by parts;
  introduced here — orthogonality as "inner product of exponentials", the notion of a
  basis of functions.
- **Physical intuition goals:** (1) a periodic signal *is* its harmonic recipe — timbre
  is spectrum; (2) sharp features cost high harmonics; (3) a linear resonator is a
  harmonic *selector* — it answers a square-wave drive at whichever of the drive's
  harmonics it can hear; (4) more terms ≠ better everywhere.
- **Section skeleton seeds:**
  - *puzzle:* a resonator tuned to 300 Hz responds strongly to a 100 Hz square-wave
    drive — where does it find 300 Hz in a 100 Hz signal? (Boxed question: what *is* the
    frequency content of a non-sinusoidal periodic signal?) Secondary hook: violin and
    flute play the same A, and no one confuses them.
  - *predict:* (1) does the 300 Hz resonator respond to the 100 Hz square drive? To a
    100 Hz *sine* drive? (2) how many sine terms until a square wave is "perfect"?
    (3) zooming in at the jump as terms are added — does the wiggle shrink to zero?
    (targets `more-terms-always-converge`) (4) triangle vs square: which needs fewer
    terms, and why?
  - *explore:* harmonic mixer — sliders for $|c_n|$, $\arg c_n$ of the first ~10
    harmonics; waveform presets (square/triangle/sawtooth/pulse train) with an $N$
    slider; epicycle view (harmonic phasors tip-to-tail, the module-00 picture animated);
    live spectrum panel beside the waveform (the course's dual-view motif, first
    appearance).
  - *derive:* orthogonality → coefficient formula → symmetry rules → worked square wave
    → decay-rate table → Gibbs (stated, measured, explained qualitatively) → driven
    oscillator by superposition of harmonic responses.
  - *verify:* closed-form coefficients vs `fourier_coefficients` numerics; $L^2$
    convergence rates by smoothness class; Gibbs overshoot constant at 8.95%
    (`numerical-observation` box); square-driven oscillator: harmonic-sum prediction vs
    direct velocity-Verlet integration.
  - *transfer:* string modes (11) — same sum with $\sin k_n x$ shapes; why AC power
    engineering speaks of harmonics; audio synthesis and timbre; the comb spectrum as a
    future diffraction grating (31).
  - *quiz:* symmetry → harmonic content; decay-rate reasoning; Gibbs (distractor);
    resonator-as-selector numeric.
  - *explain:* why a clarinet and a violin at the same pitch differ; why "the square
    wave contains 300 Hz" is a physical statement, not a mathematical trick; what the
    9% overshoot does *not* mean.
  - *advanced:* mean-square vs pointwise convergence; Fejér/Cesàro smoothing as the fix
    for Gibbs; the harmonic phasor is $2c_n^*$ — the negative-index half of the sum is
    module 00's "analytic signal", closed properly in 04.
- **Core derivations:** (1) orthogonality
  $\tfrac1T\int_T e^{\ii(n-m)\omega_0 t}\,dt = \delta_{nm}$ → $c_n$; (2) square wave:
  $c_n = 2/(\ii\pi n)$ for odd $n$, zero even — odd harmonics with $1/n$ decay;
  (3) integration by parts: each degree of smoothness buys one power of $1/n$;
  (4) driven response $x(t) = \sum_n c_n\,\hat{H}(n\omega_0)\,e^{-\ii n\omega_0 t}$ with
  $\hat{H}$ the module-02 Lorentzian <!-- author note: synthesis sums carry
  $e^{+\ii n\omega_0 t}$ under the course convention when written index-up; write real
  forms or carry a sign-convention-exception comment where the lint objects -->.
- **Model specification draft:** System — a periodic real signal of period $T$
  represented by coefficients $\{c_n\}$; observables are partial sums and harmonic
  amplitudes. Dynamics — none; when driving the module-02 oscillator, each harmonic
  drives independently by linearity. Boundary — exact periodicity; one period carries
  everything. Ensemble — deterministic; the lab's extraction experiment adds seeded
  Gaussian noise. Ignored — transients (steady state only); convergence pathologies
  beyond piecewise-smooth. Valid when — the signal is periodic and piecewise smooth, and
  partial sums are read with Gibbs in mind. Failure modes — treating the overshoot as
  refinable error; applying the series to aperiodic signals; summing harmonic responses
  through a nonlinearity.
- **Epistemic classification:** orthogonality/coefficient formula — `theorem`;
  smoothness↔decay — `theorem` (proof sketch); Gibbs overshoot value — stated as
  `theorem`, measured as `numerical-observation`; "each harmonic drives independently" —
  `model-assumption` (linearity).
- **Misconceptions:** NEW `more-terms-always-converge` — "Adding more Fourier terms makes
  the approximation better everywhere." Falsifying experiment: zoom on the square-wave
  jump while raising $N$; the overshoot rides in toward the jump but its *height* stays
  at 9%, measured by `gibbs_overshoot`. Distractor: quiz option claiming the wiggle
  vanishes for large enough $N$.
- **Glossary terms:** `harmonic` (he: הרמוניה — translator to confirm physics usage),
  `fundamental-frequency` (תדר יסוד), `spectrum` (ספקטרום), `partial-sum` (סכום חלקי),
  `gibbs-phenomenon` (תופעת גיבס), `orthogonality` (אורתוגונליות; `he_reject` candidate:
  ניצבות in this context), `timbre` (גוון צליל).
- **Interactive controls and simulations:** harmonic mixer ($|c_n|$, phase, $N \le 32$);
  epicycle animation; preset waveforms; square-wave-driven oscillator with resonator
  frequency slider sweeping across the harmonic comb.
- **Virtual lab outline** (`notebooks/en/labs/03-fourier-series.ipynb`): (1) mixer +
  epicycles; (2) reconstruct the four presets, measure $L^2$ error vs $N$, log-log fit
  of the decay rate; (3) Gibbs zoom, overshoot vs $N$ plot; (4) drive the oscillator
  with a square wave, sweep $\omega_0^{\text{res}}$, find response peaks at odd
  harmonics, compare peak heights to $|c_n \hat{H}(n\omega_0)|$; (5) *measurement:*
  extract $|c_1|, |c_3|, |c_5|$ from a noisy sampled square wave via the coefficient
  integrals, report value ± uncertainty across seeds.
- **Real-experiment counterpart:** record a sustained instrument note (or a signal
  generator through a phone) as WAV; import; extract harmonic amplitudes; compare two
  instruments at the same pitch. Import path: `scipy.io.wavfile` → NumPy array cell.
- **Media assets** (`render_fourier.py`): (a) square-wave build-up $N = 1, 3, 5, 9, 33$
  with epicycle arrows tracing the waveform; (b) Gibbs zoom sequence. Language-neutral,
  no burned-in text.
- **Quiz bank outline:** `Q-03-1` MC symmetry → which harmonics (OBJ-03-2); `Q-03-2` MC
  Gibbs (OBJ-03-3, distractor `more-terms-always-converge`); `Q-03-3` numeric — decay
  exponent from a smoothness statement (OBJ-03-3); `Q-03-4` numeric — resonator response
  to square drive (OBJ-03-4); `Q-03-5` MC time↔spectrum matching (OBJ-03-5); `Q-03-6`
  free — interpret $|c_n|$, $\arg c_n$ (OBJ-03-1).
- **Problem set outline:** analytical — coefficients of sawtooth and pulse train
  (duty-cycle dependence); half-wave symmetry proof; Parseval for the square wave
  ($\sum 1/n^2$ odd = $\pi^2/8$). Computational — decay-rate measurement for a smoothed
  square (corner-rounding parameter); resonator bank as a "Fourier analyser".
  Challenge — Fejér sums kill Gibbs: prove positivity of the kernel, verify numerically.
- **Runtime budget:** partial sums ≤ 32 harmonics on ≤ 4096-point grids; oscillator
  integrations ≤ 100 periods. Trivial in Pyodide.
- **Validation gates:** standard set (README) with `--module 03-fourier-series`.
- **Open questions for the author:** whether the epicycle view belongs in `explore` or
  as the page's first figure; whether to include a one-cell audio player (browser
  `Audio`) for the mixer output — pedagogically strong, but adds a JupyterLite audio
  dependency to check.

### 5.3 `04-fourier-transform` — The Fourier transform and convolution

- **Identity and scope:** master-plan notebook 0.3. Aperiodic signals, the pair zoo,
  convolution, the bandwidth theorem, and the DFT/FFT bridge. Time signals only —
  spatial transforms wait for Part IX where they arrive as diffraction.
- **Prerequisites:** `03-fourier-series` (coefficients; the $T\to\infty$ limit is taken
  explicitly); `00-phasors` (analytic-signal preview closed here).
- **Learning objectives:**
  - `OBJ-04-1` — State the transform pair F(omega) = integral f(t) e^(-i omega t) dt and
    f(t) = (1/2 pi) integral F(omega) e^(i omega t) d omega, derive it as the T -> infinity
    limit of the series, and state where the course phasor lands in the spectrum.
  - `OBJ-04-2` — Use the pair zoo (rect<->sinc, Gauss<->Gauss, exponential<->Lorentzian,
    comb<->comb) to sketch spectra without integration.
  - `OBJ-04-3` — State and apply the convolution theorem in both directions.
  - `OBJ-04-4` — Use Delta t times Delta omega >= 1/2 to estimate bandwidth from duration
    and vice versa, and name the equality case.
  - `OBJ-04-5` — Compute a correctly scaled spectrum of sampled data with the FFT and
    diagnose aliasing, leakage, and the effect of zero-padding.
  - `OBJ-04-6` — Explain what the complex phase of a spectrum carries, and why
    magnitude-only reconstruction fails.
- **Mathematical background:** has — series, orthogonality, complex integration at the
  completing-the-square level; introduced here — delta function (operationally), RMS
  width as a moment.
- **Physical intuition goals:** (1) short ↔ wide is a law, not a tendency; (2) smooth ↔
  compact spectrum, sharp ↔ extended; (3) convolution is "smear one signal with the
  other" and multiplication in the other domain; (4) a sampled signal only pretends to
  be continuous — above Nyquist it lies.
- **Section skeleton seeds:**
  - *puzzle:* what frequency is a hand-clap? A whistle has a pitch; a clap has none —
    yet a microphone + FFT shows the clap *has* every frequency at once. (Boxed: what is
    the frequency content of something that never repeats?) Hook 2: tuning a radio —
    hundreds of stations share one air.
  - *predict:* (1) halve a pulse's duration — its spectrum gets wider/narrower/unchanged?
    (2) can two different signals have the same magnitude spectrum? (targets
    `ft-discards-time`) (3) a 60 Hz sine sampled at 100 Hz — what frequency does the
    data show? (4) is there a signal both short in time and narrow in frequency?
  - *explore:* pulse sculptor — shape (rect/Gauss/exponential/chirp), duration and
    centre sliders, live dual panel $f(t)$ ↔ $|F(\omega)|$ with the analytic pair
    overlaid; sampling toggle exposing Nyquist and fold-back; convolution sandbox
    (pick $f$, $g$, watch $f*g$ and the spectral product).
  - *derive:* $T\to\infty$ limit → transform pair (forward sign $e^{-\ii\omega t}$, the
    `numpy.fft` sign; the $1/2\pi$ on the inverse) → where the phasor lives: for
    $x(t) = \Real[\hat{x}e^{-\ii\omega_0 t}]$ the spectrum holds $\pi\hat{x}$ at
    $-\omega_0$ and $\pi\hat{x}^*$ at $+\omega_0$; the analytic signal keeps the
    clockwise half → the four zoo pairs, each derived once → convolution theorem →
    Parseval → bandwidth theorem via RMS widths, Gaussian equality → DFT as sampled
    transform: comb multiplication in time = periodisation in frequency, hence aliasing;
    finite window = convolution with a sinc, hence leakage.
  - *verify:* zoo pairs — FFT vs closed forms; round-trip `inverse_spectrum(spectrum(f))`
    to machine precision; convolution theorem numerically; uncertainty product across
    shapes, minimised by the Gaussian (`numerical-observation`); aliasing — a swept tone
    folds at exactly $\omega_{\text{Nyq}}$.
  - *transfer:* impulse response (05) — the transform of the Green function is *the*
    frequency response; wave packets (12) — same theorem with $x$ and $k$; coherence
    (27) — spectral width sets fringe survival; diffraction (29) — the zoo drawn on a
    screen in light; every later lab's spectrum panel — this module's `spectrum()` call.
  - *quiz:* pair-zoo matching; bandwidth numeric; aliasing numeric; phase-information MC.
  - *explain:* why "what frequency is a clap" is ill-posed and what question replaces
    it; why a piano note's attack matters to its sound though the magnitude spectrum of
    the sustain barely shows it; explain aliasing to a film-maker (wagon wheels).
  - *advanced:* the analytic signal and single-sideband representation, closing 00's
    negative-frequency thread; windows (Hann) as leakage control and the
    resolution/leakage trade; a first look at the spectrogram — trading $\Delta t$
    against $\Delta\omega$ inside one picture.
- **Core derivations:** as in the seeds; each zoo pair gets the honest two-line
  integral: rect by direct integration → $\operatorname{sinc}$; Gaussian by completing
  the square; one-sided exponential $e^{-t/\tau}\Theta(t)$ → Lorentzian
  $1/(1/\tau - \ii\omega)$ — the same curve as module 02's resonance and, later, the
  linewidth of module 27 and the cavity line of 26; comb → comb stated with the
  periodisation proof sketched.
- **Model specification draft:** System — square-integrable real signals and their
  complex spectra; numerically, $N$ samples at spacing $\Delta t$. Dynamics — none; a
  change of representation (convolution models LTI action when used). Boundary — signals
  decay or are windowed; the DFT imposes periodicity on the window, silently. Ensemble —
  deterministic; seeded noise in measurement cells. Ignored — distribution rigour;
  convergence pathologies. Valid when — content below Nyquist; window long against
  features. Failure modes — aliasing; leakage read as physics; magnitude-only thinking;
  forgetting the $1/2\pi$ or the sign of the forward transform.
- **Epistemic classification:** transform pair and convolution theorem — `theorem`;
  bandwidth theorem — `theorem` (RMS proof in advanced, statement in core); "sampled
  signal represents the continuous one" — `model-assumption` with Nyquist as its
  validity edge; measured uncertainty products — `numerical-observation`; "is there a
  best window?" — `open-question` pointer.
- **Misconceptions:** NEW `ft-discards-time` — "The Fourier transform throws away the
  time information in a signal." Falsifier: reconstruct from the full complex spectrum
  (exact) vs from magnitude alone (garbage); a chirp and a pulse with identical
  magnitude spectra, visibly different. Distractor: quiz option "two signals with the
  same magnitude spectrum are the same signal". NEW `negative-frequency-unphysical` —
  "Negative frequencies are a mathematical artifact with no physical content."
  Falsifier: the phasor of a real cosine demonstrably occupies both half-axes
  (`spectrum` of $\cos$), and suppressing one half changes the signal into its analytic
  form — a different, complex signal. Distractor: "the negative-frequency half of an
  FFT is redundant noise the code should discard".
- **Glossary terms:** `fourier-transform` (התמרת פורייה), `bandwidth` (cited, deposited
  by `02-damped-driven` — 02 precedes 04 in teaching order),
  `convolution` (קונבולוציה; `he_reject` candidate: עירוב), `sampling` (דגימה),
  `nyquist-frequency` (תדר נייקוויסט), `aliasing` (כיווץ תדרים? translator to decide —
  transliteration אליאסינג common), `spectral-leakage` (זליגה ספקטרלית),
  `analytic-signal` (אות אנליטי).
- **Interactive controls and simulations:** pulse sculptor (shape, $\sigma$/width,
  chirp rate); sampling panel ($\Delta t$, $N$, window on/off); convolution sandbox;
  uncertainty-product meter (live $\Delta t_{\text{rms}}\cdot\Delta\omega_{\text{rms}}$
  readout with the $\tfrac12$ line drawn).
- **Virtual lab outline** (`notebooks/en/labs/04-fourier-transform.ipynb`): (1) zoo
  gallery, FFT vs analytic overlay; (2) uncertainty products across shapes, table +
  Gaussian minimum; (3) aliasing: sweep a tone through Nyquist, plot apparent vs true
  frequency (the folding diagram measured, not asserted); (4) leakage and the Hann
  window; (5) convolution theorem check; (6) *measurement:* given a noisy two-tone
  signal with nearby frequencies, resolve them — discover the window-length /
  resolution trade, report both frequencies ± uncertainty.
- **Real-experiment counterpart:** phone-microphone clap vs whistle spectra (WAV
  import); optional strobe/wagon-wheel video for aliasing.
- **Media assets** (`render_fourier.py`): (c) pulse narrowing ↔ spectrum widening,
  side-by-side, uncertainty product overlaid as a shaded box; (d) aliasing wagon-wheel:
  rotating marker sampled below its rotation rate.
- **Quiz bank outline:** `Q-04-1` MC zoo matching (OBJ-04-2); `Q-04-2` numeric bandwidth
  from duration (OBJ-04-4); `Q-04-3` numeric aliasing fold (OBJ-04-5); `Q-04-4` MC phase
  information (OBJ-04-6, distractor `ft-discards-time`); `Q-04-5` MC negative
  frequencies (OBJ-04-1, distractor `negative-frequency-unphysical`); `Q-04-6` free —
  convolution theorem in words with an example (OBJ-04-3).
- **Problem set outline:** analytical — derive the Gaussian pair; scaling and shift
  theorems; Lorentzian width ↔ decay time; Parseval application. Computational —
  build a numerical uncertainty-product minimiser over a parametrised pulse family;
  measure leakage vs window choice. Challenge — sampling theorem reconstruction:
  implement sinc interpolation and find where it breaks.
- **Runtime budget:** FFTs ≤ $2^{14}$ points, convolutions via FFT — all sub-second in
  Pyodide; the two-tone measurement uses ≤ $2^{16}$ once, still fine.
- **Validation gates:** standard set with `--module 04-fourier-transform`.
- **Open questions for the author:** how much of the DFT bridge belongs in core vs
  advanced (recommendation: comb/periodisation picture in core, windows in advanced);
  whether `spectrum()` should return two-sided (honest, matches the convention
  discussion) or fold to one-sided for display (recommendation: two-sided return,
  one-sided display helper in the lab only).

## 6. Part-level assessment and capstone hooks

- Every later laboratory's spectrum panel is this part's deliverable: `spectrum()` +
  the pair zoo are the course's shared visual language (master plan §22).
- Capstone §35.3 (grating spectrometer) and §35.5 (4-f image processor) consume the
  FFT bridge directly; §35.1 (computational telescope) consumes the 2-D generalisation
  built in part-09/11 on top of `fourier.py`.
- Cross-module synthesis problem (lives with part-01 problem sets once 05 exists):
  drive the damped oscillator with a noisy square wave, predict the response spectrum
  from $c_n \times$ Lorentzian, verify by FFT — one problem touching 00–05.
- Exam themes: pair-zoo sketching under time pressure; symmetry → harmonic content;
  bandwidth estimates with order-of-magnitude answers.

## 7. Build order and validation gates

Build `03-fourier-series` first, then `04-fourier-transform` (04 opens with 03's
$T\to\infty$ limit). Both follow `02-damped-driven` (part-01) in teaching order, and 03's
driven application needs 02's `steady_state_response` in `src/wavelab/oscillators.py` —
so the concrete build sequence across parts is: `02` → `03` → `04` → `05`.

With the first of these modules, deposit into `glossary/terms.yml` the §5 term lists and
add the two/three NEW misconception entries to `assessment/misconceptions.yml`
(`more-terms-always-converge`, `ft-discards-time`, `negative-frequency-unphysical`),
status `pending` until the pages address them. Registry re-pointings per README conflict
log happen with the affected modules, not here.

Per module: the standard four gates (README). Additionally for this part: the
`fourier.py` test additions (§4) must land *with* 03/04, since later parts' plans cite
those guarantees.

## 8. Deviations from the master plan

- **Resequencing (the just-in-time decision, user-approved):** master plan §7 places all
  three foundation notebooks before oscillations. This plan teaches 00 first but moves
  Fourier series to position 03 (after the driven oscillator) and the transform to 04
  (before impulse response). Rationale: Fourier series acquires a physical engine — the
  resonator-as-harmonic-selector — instead of being unmotivated mathematics; the
  transform lands immediately before the module that consumes it (05, convolution =
  impulse response); §31's requirement (Fourier before diffraction) is honoured with
  five parts to spare. Cost: none to ids (ids are opaque; TOC order governs).
- **Scope split:** spatial Fourier analysis (2-D transforms, spatial frequency) is
  *not* previewed here; it enters at part-09/11 where light performs it. The master
  plan's 0.3 "signature dual-view motif" is adopted, but in time/frequency only.
- **Notation:** series and transform are written in the course phase convention
  (forward $e^{-\ii\omega t}$, $1/2\pi$ on the inverse, `numpy.fft` sign — see
  `constants.py`), which reverses the sign convention shown in master plan §7's series
  formula. Synthesis-direction exponentials ($e^{+\ii\omega t}$) appearing index-up in
  content will carry the lint exception comment where required.
- **Additions beyond the master plan:** the DFT/FFT bridge as first-class content; the
  bandwidth theorem stated and measured here (the master plan first implies it at
  coherence); the transform-pair zoo as a recurring visual motif; three new registry
  misconceptions; the negative-frequency/analytic-signal thread closed explicitly.
