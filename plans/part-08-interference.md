# Part VIII — Interference and Coherence — Implementation Plan

> **Master plan:** §15 (Part VIII). **Modules:** `23-interference`, `24-thin-films`, `25-michelson`, `26-fabry-perot`, `27-coherence`. **Status:** planned.
> Canonical numbering, invariants, and conflict log: [README.md](README.md).

## 1. Part overview and narrative arc

Interference is where phase — carefully nurtured since `00-phasors` — becomes
**measurable** distance, wavelength, and spectrum. Until now phase has been a bookkeeping
coordinate; from module 23 on it is a readout: fringes convert nanometres of path into
countable stripes, film thickness into colour, mirror motion into a blinking detector, and
spectral structure into visibility. The part's organising claim is therefore that **every
module is an instrument**: Young's slits measure wavelength, a soap film measures its own
thickness, the Michelson measures displacement and coherence length, the Fabry–Pérot
resolves spectra, and the coherence module turns fringe contrast itself into a spectrometer.
This is the master plan's §29 "Hecht Interference as a Virtual Laboratory Family" made
literal — each module's lab is one of that family's benches, with synthetic noise and a
value ± uncertainty at the end (§23–§24 of the master plan).

The part's **signature structure** is that coherence is woven through from the start
instead of being quarantined in the final notebook. Module 23 introduces a *visibility
slider* — a partial-correlation factor $\gamma$ between the two sources — purely as a
phenomenon: drag it down and the fringes wash out. Modules 24–26 keep meeting the same
ghost (why the thick film loses its colours, why white-light fringes live only near zero
path difference, why the sodium lamp's fringes fade and revive). Module 27 then closes the
loop with the formalism: $\gamma(\tau)$, the Wiener–Khinchin theorem, and the Part-0
bandwidth theorem paying off as $\tau_c \approx 1/\Delta\omega$. The student meets partial
coherence four times as an experimental fact before meeting it once as a definition.

The mathematical through-line is the maturing of module 00's arrow arithmetic. Module 23 is
two arrows — the built `00-phasors` page promises that its interference law
$A^2 = A_1^2 + A_2^2 + 2A_1A_2\cos\delta$ "becomes module 8's central topic, when this same
formula reappears wearing its optics costume, $I = I_1 + I_2 + 2\sqrt{I_1 I_2}\cos\delta$"
— this part keeps that promise on its first page. Module 24 is two arrows with honest phase
bookkeeping (the $\pi$-shift trap) and, exactly, a geometric series of them. Module 26 sums
the *infinite* geometric series of phasors in closed form — the module-00 arithmetic
literally summed to closure — and finds the Airy function. Module 27 is the random-phase
walk of `00-phasors` promoted to a correlation function: the violinists finally get their
theory. The second promise kept from module 00 is **energy bookkeeping**: the re-pointed
registry entry `interference-destroys-energy` is claimed by 23, whose falsifying experiment
(screen-integrated intensity equals the incoherent total — energy is redistributed, never
destroyed) is also a `tests/physics` conservation test.

Relative to master plan §15 this plan deepens: 8.3's "perceived color" becomes a complete,
honest **colour pipeline** ($R(\lambda)$ → CIE 1931 colour-matching integration → sRGB
swatch) so soap-film and oil-slick colours are *predicted*, not described; 8.4 gains the
compensator plate, coherence-length measurement, FTIR spectroscopy as the
interferogram-is-autocorrelation payoff, and LIGO as the research connection; 8.5 gains the
Lorentzian lineshape (part-01's resonance curve in frequency space), photon lifetime,
cavity ringdown, and $Q$; 8.6 gains Wiener–Khinchin as the part's crowning theorem, the
stellar interferometer, and a table of real sources with honest coherence lengths. Seeds
planted forward: diffraction (Part IX) is interference of a *continuum* of sources — 23
states its point-slit idealisation explicitly and hands the finite-width envelope to
`30-apertures`; the Fabry–Pérot returns with gain as a laser (`44-resonators`,
`45-lasers`); the quarter-wave stack trailered in 24 becomes dielectric mirrors and
photonic crystals; holography (`50-holography`) is interference *recorded*; partial
coherence returns in imaging (`41-imaging-coherence`) and photon statistics
(`52-quantum-optics`).

## 2. Position in the course

- **Requires:**
  - `00-phasors`: the one-frequency superposition theorem, the interference law
    $A^2 = A_1^2 + A_2^2 + 2A_1A_2\cos\delta$, `phasors.superpose` / `resultant`, and the
    random-walk result via `phasors.random_phasor_sum` ($\langle|\sum e^{-\ii\varphi_k}|^2\rangle = N$).
  - `04-fourier-transform`: `fourier.spectrum`, the pair zoo (`exp_decay` ↔
    `lorentzian_spectrum`, `gaussian_pulse` ↔ `gaussian_spectrum`), `rms_widths` and the
    bandwidth theorem $\Delta t\,\Delta\omega \ge \tfrac12$ — 27's engine.
  - `01-sho` / `02-damped-driven`: the Lorentzian response (`steady_state_response`) and
    $Q$ three ways (`q_from_bandwidth`, `q_from_ringdown`, `q_from_phase_slope`) — 26's
    linewidth/lifetime bridge.
  - `10-impedance`: junction algebra and quarter-wave matching teaser
    (`waves.impedance`, `waves.junction_coefficients`, `waves.power_coefficients`) — 24's
    algebra box.
  - `15-em-energy`: intensity as cycle-averaged Poynting flux, $I \propto |\hat{E}|^2$ —
    what "adding intensities" and "adding fields" each mean.
  - `16-light-in-matter`: wavelength $\lambda/n$ and phase accumulation $n k_0 x$ inside a
    medium; complex index $n + \ii\kappa$ notation.
  - `18-fresnel`: amplitude reflection/transmission coefficients and the phase-shift rules
    (external reflection carries $\pi$ at near-normal incidence) — 24's bookkeeping input.
- **Feeds:**
  - `29-fraunhofer` / `30-apertures` / `31-gratings`: two point sources → continuum;
    30 owns the finite-slit-width envelope 23 defers; 31 generalises 23 to $N$ slits.
  - `41-imaging-coherence`: van Cittert–Zernike in full; coherent vs incoherent imaging.
  - `44-resonators` / `45-lasers`: the Fabry–Pérot with curvature, stability, and gain;
    FSR returns as longitudinal-mode spacing; 27 explains why laser light is special.
  - `50-holography`: recording an interference pattern is the whole trick.
  - `52-quantum-optics`: $\gamma(\tau)$ → $g^{(2)}(\tau)$; Hanbury Brown–Twiss.
- **Explicitly not assumed:** any diffraction theory (no Huygens integral appears in this
  part — slits are ideal point/line sources); vector or polarization effects beyond the
  s/p Fresnel factors of 24; Gaussian beams; quantum descriptions of light; statistical
  optics beyond stationary ensembles.

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|
| `23-interference` | `content/en/interference/23-interference.md` | Two-wave interference and Young's double slit | 8.1 + 8.2 | Hecht, Interference — general treatment & wavefront-splitting (Young) | planned |
| `24-thin-films` | `content/en/interference/24-thin-films.md` | Thin-film interference and the colours of films | 8.3 | Hecht, Interference — amplitude-splitting: dielectric films | planned |
| `25-michelson` | `content/en/interference/25-michelson.md` | The Michelson interferometer as a measuring instrument | 8.4 | Hecht, Interference — amplitude-splitting interferometers | planned |
| `26-fabry-perot` | `content/en/interference/26-fabry-perot.md` | Fabry–Pérot: multiple-beam interference | 8.5 | Hecht, Interference — multiple-beam interference | planned |
| `27-coherence` | `content/en/interference/27-coherence.md` | Temporal and spatial coherence | 8.6 | Hecht, Basics of coherence theory; Michelson stellar interferometer | planned |

## 4. Shared infrastructure for this part

**`src/wavelab` — existing used:** `phasors.superpose` / `resultant` (23's arrow figures);
`phasors.random_phasor_sum` (27's ensemble machinery precedent); `fourier.spectrum` /
`inverse_spectrum` (25's FTIR, 27's Wiener–Khinchin numerics), `fourier.exp_decay` /
`lorentzian_spectrum` / `gaussian_pulse` / `gaussian_spectrum` (27's pair overlays),
`fourier.rms_widths` (27's $\tau_c\,\Delta\omega$ product); `oscillators.steady_state_response`,
`q_from_bandwidth`, `q_from_ringdown`, `q_from_phase_slope` (26's Lorentzian/Q bridge — by
name only, owned by part-01); `waves.impedance`, `waves.junction_coefficients`,
`waves.power_coefficients` (24's quarter-wave algebra box — by name only, owned by
part-03); the `interfaces.py` single-boundary amplitude-coefficient functions (24 composes
them into film products — by name per part-06's plan as built); `measurement.add_noise` /
`fit_cosine` (all five labs); `validation.scaling_exponent` / `convergence_study` /
`seed_study` / `relative_error`.

**`src/wavelab` — new: `interference.py`** (introduced and owned by this part; README
ownership table — serves 23–27 including the thin-film → colour pipeline). Docstring
model spec:

- **System:** scalar quasi-monochromatic optical fields as complex amplitudes —
  superposed at screens and detectors, multiply reflected in plane-parallel films and
  cavities — plus their spectra and correlation functions.
- **Dynamics:** none — stationary superposition; time enters only as propagation delay
  and through statistical correlation of ensemble members.
- **Boundary:** films and cavities are infinite plane-parallel layers; slits are ideal
  point/line sources (finite width belongs to `diffraction.py`); screens sit in the
  small-angle far field.
- **Ensemble:** deterministic by default; partial coherence via an analytic $|\gamma|$
  factor or seeded random-phase-drift field ensembles.
- **Ignored:** diffraction envelopes; vector effects beyond s/p Fresnel factors;
  absorption unless a complex index is supplied; nonlinearity; quantum statistics.
- **Valid when:** angles are small where the small-angle forms are used; fields are
  quasi-monochromatic (bandwidth ≪ centre frequency); detectors average many optical
  cycles.
- **Failure modes:** adding intensities where fields are required (or fields where the
  sources are uncorrelated); dropped or double-counted reflection $\pi$ shifts;
  small-angle fringe formulas applied at large angles; a single speckle realisation read
  as an ensemble average.

Function-level sketch (signatures + contracts):

```python
two_beam_intensity(I1, I2, delta, gamma=1.0) -> I    # I1+I2+2*sqrt(I1*I2)*gamma*cos(delta); gamma in [0,1]
path_difference(d, L, y) -> Delta                    # exact two-point geometry; documents Delta ~ d*y/L small-angle
fringe_spacing(lam, d, L) -> dy                      # lam*L/d
young_pattern(lam, d, L, y, gamma=1.0) -> I          # point-slit screen intensity; the five-panel engine
thin_film_amplitude(n1, n2, n3, d, lam, theta=0.0, pol="s") -> r
                                                     # complex: (r12 + r23 e^{2i beta})/(1 + r12 r23 e^{2i beta}),
                                                     # beta = 2 pi n2 d cos(theta_t)/lam; Fresnel signs carry the pi shifts
thin_film_reflectance(n1, n2, n3, d, lam, theta=0.0, pol="s") -> R   # |r|^2; R + T = 1 for real indices
reflected_spectrum(stack, lam_array, theta=0.0, pol="s") -> R_array  # vectorized over wavelength; stack=(indices, thicknesses)
transfer_matrix_stack(ns, ds, lam, theta=0.0, pol="s") -> (r, t)     # 2x2 characteristic matrices; multilayers (advanced)
ar_coating_design(n1, n3, lam0) -> (n2, d)           # sqrt(n1*n3), lam0/(4*n2); exact null guaranteed by construction
cie_color(spectrum, lam_array, illuminant="D65") -> (r, g, b)
                                                     # CIE 1931 2-deg CMFs x D65 -> XYZ -> linear sRGB matrix -> gamma, clipped
michelson_intensity(delta_d, lam, coherence_len=np.inf) -> I
                                                     # (I0/2)(1 + |gamma| cos(4 pi delta_d / lam)); |gamma| from coherence_len
fringe_count(delta_d, lam) -> N                      # 2*delta_d/lam
airy_coefficient(R) -> F                             # 4R/(1-R)^2 (coefficient of finesse; not the finesse)
airy_transmission(delta, R) -> T                     # 1/(1 + F sin^2(delta/2)); lossless symmetric cavity
finesse(R) -> float                                  # pi*sqrt(R)/(1-R) = FSR/FWHM
fsr(L, n=1.0) -> dnu                                 # c/(2*n*L) [Hz]
fp_linewidth(L, R, n=1.0) -> dnu                     # fsr/finesse [Hz]
fp_spectrum(lam_array, L, R, n=1.0) -> T_array       # Airy comb sampled at given wavelengths
visibility(I) -> V                                   # (Imax - Imin)/(Imax + Imin) from a fringe trace
degree_of_coherence(S, omega) -> (tau, gamma)        # normalized FT of the spectral density (Wiener-Khinchin),
                                                     # via the fourier.spectrum FFT machinery; gamma(0) == 1
coherence_time(S, omega) -> tau_c                    # RMS width of |gamma|; consistent with ~1/Delta_omega
coherence_length(S, omega) -> ell_c                  # c * coherence_time
partial_coherence_source(bandwidth, n_samples, dt, seed) -> E
                                                     # complex field with random-phase drift (phase diffusion ->
                                                     # Lorentzian line of the given width); seeded, ensemble-ready
```

The CIE 1931 2° colour-matching functions and the D65 illuminant ship as **package data**
(`src/wavelab/data/cie_1931_2deg.csv`, `src/wavelab/data/d65.csv`, 5 nm tabulation from
the public CIE tables) — `cie_color` documents the data provenance and the sRGB gamut
clipping honestly rather than hiding either.

**`tests/physics/` additions:**

- *conservation:* screen-integrated `young_pattern` energy over many fringes equals two
  incoherent sources (the `interference-destroys-energy` falsifier as a test, any
  $\gamma$); $R + T = 1$ for lossless films across $\lambda$, $\theta$, both
  polarizations; Airy $R_{\text{cav}} + T_{\text{cav}} = 1$ across $\delta$.
- *limits:* $R \to 0$: `airy_transmission` flat at 1; `degree_of_coherence` gives
  $\gamma(0) = 1$; `ar_coating_design` output nulls `thin_film_reflectance` at
  $\lambda_0$ exactly; $\gamma = 0$ reduces `two_beam_intensity` to $I_1 + I_2$;
  $d \to 0$ film → bare 1|3 interface coefficients; `michelson_intensity` with infinite
  coherence length → unit-visibility cosine; Lorentzian $S$ →
  $|\gamma| = e^{-|\tau|/\tau_c}$ against `fourier.exp_decay`.
- *scaling:* fitted fringe-spacing exponents $+1$ in $\lambda$ and $L$, $-1$ in $d$ via
  `scaling_exponent` (the $\Delta y = \lambda L/d$ law measured, not assumed).
- *convergence:* finite $N$-bounce phasor sum → `airy_transmission` as $N$ grows, error
  $\propto R^N$; `transfer_matrix_stack` for a single film ≡ `thin_film_amplitude`.
- *seeds:* ensemble visibility of `partial_coherence_source` reproducible per seed and
  matching analytic $|\gamma|$ within $1/\sqrt{M}$ across $M$ realisations.
- *dimensions:* `fsr` / `fp_linewidth` in Hz, `coherence_length` in m, against `units`.

**Shared media:** one script `media/render/render_interference.py` produces all Part VIII
MP4s (shot lists in §5). **Glossary themes:** interference vocabulary (23–24), instrument
vocabulary (25–26), coherence vocabulary (27) — per-module lists in §5.

## 5. Module specifications

### 5.1 `23-interference` — Two-wave interference and Young's double slit

- **Identity and scope:** master-plan notebooks 8.1 + 8.2, merged (precedent:
  `02-damped-driven` ← 1.2 + 1.3): the two-beam law *is* Young's screen read pointwise —
  splitting them would teach the same formula twice. Deferred: finite slit width and the
  diffraction envelope → `30-apertures` (stated in the page, logged in §8); $N$ slits →
  `31-gratings`; coherence formalism → `27-coherence`.
- **Prerequisites:** `00-phasors` (interference law, superposition theorem);
  `15-em-energy` ($I \propto |\hat{E}|^2$, cycle averaging); `16-light-in-matter`
  ($\lambda/n$, for the water-immersion question).
- **Learning objectives:**
  - `OBJ-23-1` — Derive I = I1 + I2 + 2 sqrt(I1 I2) cos delta from phasor addition and
    time-averaging, and map it onto the module-00 law A^2 = A1^2 + A2^2 + 2 A1 A2 cos delta.
  - `OBJ-23-2` — Compute the path difference d sin theta ~ d y / L and phase difference
    delta = 2 pi d y / (lambda L) for a double slit, and predict fringe positions.
  - `OBJ-23-3` — Use the fringe spacing Delta y = lambda L / d to measure a wavelength
    from a fringe pattern, with uncertainty.
  - `OBJ-23-4` — Show by integration that interference redistributes energy across the
    screen without changing the total, for any phase and any degree of correlation.
  - `OBJ-23-5` — Predict qualitatively how fringe contrast degrades as the two sources
    decorrelate (gamma slider), and state that the quantitative theory arrives in module 27.
  - `OBJ-23-6` — State the small-angle, far-field, point-slit assumptions and identify
    when each fails.
- **Mathematical background:** has — phasor arithmetic, time averages; introduced here —
  optical path difference as geometry, the far-field/small-angle expansion
  $\sqrt{L^2 + (y \pm d/2)^2}$ to first order.
- **Physical intuition goals:** (1) bright fringes are $4I_0$, not $2I_0$ — and dark
  fringes pay for them; (2) fringe spacing grows with $\lambda$ and $L$, shrinks with
  $d$ — a fringe pattern is a wavelength ruler; (3) no correlation, no fringes: two
  flashlights give a smooth wall; (4) immersing the apparatus in water squeezes the
  fringes by $n$.
- **Section skeleton seeds:**
  - *puzzle:* point two identical coherent sources at a wall: at the centre line you get
    *four* times one source's intensity, and a hand's width away, zero. (Boxed: where
    does the extra light at the bright fringes come from, and what happened to the light
    at the dark ones?) Secondary hook: two flashlights show nothing — yet Young did this
    with sunlight in 1803. What did he know that the flashlights don't?
  - *predict:* (1) two equal in-phase beams: centre intensity $2I_0$ or $4I_0$? (2) is
    total screen energy changed by interference? (targets
    `interference-destroys-energy`) (3) double the slit separation — fringe spacing
    doubles or halves? (4) two *independent* lasers — fringes or not?
  - *explore:* the master plan's **five synchronized panels** (its 8.2 display list):
    (i) optical geometry with the two paths drawn, (ii) path difference vs $y$,
    (iii) phase difference vs $y$, (iv) phasor addition at the chosen screen point,
    (v) screen intensity — sliders $\lambda$, $d$, $L$, screen-point marker $y$, plus the
    **$\gamma$ visibility slider** (partially correlated sources → fringes wash out; the
    part's signature thread starts here). Two-beam sandbox: $I_1$, $I_2$, $\delta$,
    $\gamma$ with live $I$ readout.
  - *derive:* field superposition → time-averaged intensity → the interference law (the
    module-00 formula in its optics costume — quoted, with $A^2 \leftrightarrow 2I$) →
    slit geometry → $\Delta = d\sin\theta \approx dy/L$ → fringe positions and
    $\Delta y = \lambda L/d$ → visibility $V = 2\sqrt{I_1 I_2}/(I_1 + I_2)$ for unequal
    beams → the $\gamma$ factor inserted phenomenologically → the energy integral.
  - *verify:* `young_pattern` small-angle vs exact `path_difference` geometry (when the
    approximation cracks); screen-integrated energy = incoherent total
    (`numerical-observation` box); fitted fringe-spacing exponents $(+1, +1, -1)$ in
    $(\lambda, L, d)$.
  - *transfer:* `24-thin-films` (same $\delta$, now set by film thickness);
    `25-michelson` / `26-fabry-perot` (the law industrialised); `27-coherence` (the
    $\gamma$ slider gets its theory); `29-fraunhofer` / `30-apertures` (continuum of
    sources; the envelope this module owes); `31-gratings` ($N$ slits); back to
    `00-phasors` (promise kept); single photons interfere with themselves — one sentence,
    door to `52-quantum-optics`.
  - *quiz:* $4I_0$ numeric; fringe-spacing numeric; inverse-$d$ MC; energy MC
    (registry distractor); water-immersion MC; visibility-slider reading.
  - *explain:* where the dark fringes' energy went (and why "destroyed" is wrong); why
    two flashlights show no fringes; why a fringe pattern is a wavelength ruler; what
    "small-angle" silently assumed.
  - *advanced:* the deeper energy cut — the radiation-load story of `00-phasors`'
    advanced section (sources coupled by their fields emit differently; link back
    explicitly); exact near-field hyperbolae vs the far-field pattern — where the
    Fraunhofer-like picture honestly ends.
- **Core derivations:** (1) $E = \Real[(\hat{E}_1 + \hat{E}_2)e^{-\ii\omega t}]$ →
  $I = I_1 + I_2 + 2\sqrt{I_1 I_2}\cos\delta$ (with the $\gamma$-generalised form
  $I = I_1 + I_2 + 2\sqrt{I_1 I_2}\,\gamma\cos\delta$ stated, derived in 27);
  (2) geometry: $\Delta = d\sin\theta \approx dy/L$, $\delta = k\Delta = 2\pi dy/(\lambda L)$,
  maxima at $y_m = m\lambda L/d$, so $\Delta y = \lambda L/d$;
  (3) energy: $\overline{I(y)} = I_1 + I_2$ once $\cos\delta$ averages out over whole
  fringes — redistribution, not destruction.
- **Model specification draft:** System — two quasi-monochromatic point/line sources and
  a distant screen; observable is cycle-averaged intensity vs position. Dynamics — none;
  stationary superposition. Boundary — screen in the small-angle far field; slits ideal
  (no width). Ensemble — deterministic at $\gamma = 1$; the slider mixes in an
  uncorrelated ensemble fraction. Ignored — diffraction envelope, polarization, source
  depletion. Valid when — $d, y \ll L$; bandwidth ≪ centre frequency; detector averages
  many cycles. Failure modes — adding intensities of correlated sources or fields of
  uncorrelated ones; using $\Delta y = \lambda L/d$ at large angles; forgetting the
  envelope exists (it does — module 30).
- **Epistemic classification:** interference law — `theorem` (from module 00's boxed
  theorem + time averaging); $\Delta y = \lambda L/d$ — `approximation` (small-angle,
  boxed with its validity edge); energy redistribution — `theorem`, its numerical check a
  `numerical-observation`; "point slits" — `model-assumption` (the honesty box pointing
  to `30-apertures`).
- **Misconceptions:** claims **`interference-destroys-energy`** (README conflict log
  re-points it here from `08-interference`; the one-line `assigned_module` edit lands
  with this module). Falsifying experiment: integrate $I(y)$ across the screen at
  $\gamma = 1$ and $\gamma = 0$ — equal totals to numerical precision; energy is
  *redistributed* from dark to bright fringes, never destroyed (the `00-phasors` advanced
  radiation-load story is the deeper cut, linked). Distractor: quiz option "at a dark
  fringe the two waves' energies cancel and are lost".
- **Glossary terms:** `interference` (התאבכות), `constructive-interference` (התאבכות
  בונה), `destructive-interference` (התאבכות הורסת), `fringe` (פס התאבכות),
  `fringe-spacing` (מרווח פסים), `path-difference` (הפרש דרכים; `he_reject` candidate:
  הפרש מהלך — translator to decide), `optical-path-length` (דרך אופטית),
  `double-slit` (שני סדקים).
- **Interactive controls and simulations:** five-panel Young ($\lambda$ 380–780 nm, $d$
  0.05–2 mm, $L$ 0.2–5 m, $y$ marker, $\gamma$ 0–1); two-beam sandbox; energy-integral
  bar (coherent vs incoherent totals side by side, live).
- **Virtual lab outline** (`notebooks/en/labs/23-interference.ipynb`): (1) five-panel
  exploration, log predictions; (2) *measurement* (master plan §23 "Double slit →
  wavelength"): synthetic fringe photo of an unknown laser with pixel noise and slit-jig
  tolerance (`measurement.add_noise`), locate maxima / fit the pattern, extract
  $\lambda \pm \sigma$ propagating the $d$ and $L$ uncertainties; (3) energy audit:
  numerically integrate $I(y)$ vs $\gamma$; (4) $\gamma$ ensemble: build the washout
  from explicit random relative phases, connecting slider to average.
- **Real-experiment counterpart:** laser pointer + double-slit slide (or two scored
  lines in foil): photograph fringes on a wall with a ruler in frame; import the photo's
  intensity row, repeat the lab's fit on real data.
- **Media assets** (`render_interference.py`): (a) five-panel Young animation sweeping
  $d$ — fringes tighten as arrows at the marked point rotate; (b) $\gamma$ washout
  sweep at fixed geometry. Language-neutral.
- **Quiz bank outline:** `Q-23-1` numeric — centre intensity of two equal coherent beams
  (OBJ-23-1); `Q-23-2` numeric — $\lambda$ from a fringe photo's spacing (OBJ-23-2,
  OBJ-23-3); `Q-23-3` MC — double $d$, what happens to $\Delta y$ (OBJ-23-2); `Q-23-4`
  MC — total screen energy with/without interference (OBJ-23-4, distractor
  `interference-destroys-energy`); `Q-23-5` MC — apparatus immersed in water (OBJ-23-2);
  `Q-23-6` MC — $\gamma$ slider at 0.5: fringe contrast (OBJ-23-5); `Q-23-7` free —
  which assumptions produced $\Delta y = \lambda L/d$ (OBJ-23-6).
- **Problem set outline:** analytical — three-slit phasor pattern (prelude to 31);
  visibility vs $I_1/I_2$ curve; fringe shift from a thin plate over one slit
  (bridge to 24). Computational — exact vs small-angle pattern error map over $(y, L)$;
  wavelength fit with bootstrapped uncertainty. Challenge — two detuned sources: show
  fringes *drift* at the beat frequency and time-average to zero (why "independent
  lasers" is subtle; door to 27).
- **Runtime budget:** 1-D screens ≤ 4096 points, ensemble ≤ 64 members — trivial in
  Pyodide.
- **Validation gates:** standard set with `--module 23-interference`; plus the energy
  conservation test and fringe-scaling test of §4 land with this module.
- **Open questions for the author:** whether the five panels live as one figure with
  tabs or a vertical stack (recommendation: stack, master plan §22's synchronized-view
  spirit); whether the two-flashlight hook opens the page or the transfer section
  (recommendation: open — it plants 27 early).

### 5.2 `24-thin-films` — Thin-film interference and the colours of films

- **Identity and scope:** master-plan notebook 8.3. Single film between two semi-infinite media, exact
  amplitude sum, colour pipeline, AR coating; multilayer stacks appear only as the
  advanced trailer. Deferred: dielectric-mirror design and photonic bandgaps →
  `44-resonators` / `54-photonic-crystals`; wedge films / Newton's rings → problem set.
- **Prerequisites:** `23-interference` (two-beam law); `18-fresnel` (amplitude
  coefficients and the phase-shift rules — external reflection carries $\pi$);
  `16-light-in-matter` ($\lambda/n$, phase $n k_0 d$); `10-impedance` (quarter-wave
  matching teaser and junction algebra, for the algebra box).
- **Learning objectives:**
  - `OBJ-24-1` — Compute the optical path difference 2 n2 d cos(theta_t) and the total
    phase difference between the first two reflected waves, including reflection phase
    shifts, and decide which reflections carry pi for a given stack ordering.
  - `OBJ-24-2` — Predict interference maxima and minima for both orderings
    (n1 < n2 < n3 vs n1 < n2 > n3) and explain why the conditions swap.
  - `OBJ-24-3` — Compute the exact reflectance R(lambda, theta) of a single film from the
    geometric series of Fresnel products, and state when the two-beam approximation is adequate.
  - `OBJ-24-4` — Predict the perceived colour of a film from its reflectance spectrum via
    CIE colour-matching integration, and explain why the colour shifts with angle and thickness.
  - `OBJ-24-5` — Design a quarter-wave antireflection coating (n2 = sqrt(n1 n3),
    d = lambda0 / (4 n2)) and map the design onto quarter-wave impedance matching on a string.
  - `OBJ-24-6` — (advanced) Compose multilayer stacks with 2x2 transfer matrices and
    explain qualitatively how a quarter-wave stack becomes a high reflector.
- **Mathematical background:** has — Fresnel coefficients, geometric series (00's beam
  arithmetic); introduced here — phase thickness $\beta = 2\pi n_2 d\cos\theta_t/\lambda$,
  the CIE integration as three weighted inner products, $2\times2$ transfer matrices
  (advanced).
- **Physical intuition goals:** (1) a film about as thick as a wavelength is a
  wavelength-selective mirror — colour without pigment; (2) the thinnest film is *dark*
  in reflection (the $\pi$ shift alone survives); (3) tilting shifts colours toward blue
  (shorter effective $\Lambda$... larger $\cos\theta_t$ reduces the OPD); (4) whatever
  reflection removes, transmission keeps — reflected and transmitted colours are
  complementary.
- **Section skeleton seeds:**
  - *puzzle:* a soap bubble and an oil slick contain no dye, yet blaze with colour — and
    a draining soap film turns *black* just before it pops. (Boxed: where does colour
    come from in a colourless film, and why is the thinnest film dark rather than
    bright?) The black film is the $\pi$-shift smoking gun.
  - *predict:* (1) soap film drains to $d \ll \lambda$: bright or dark in reflection?
    (targets the $\pi$ bookkeeping) (2) a $\lambda/4$ MgF$_2$ layer on glass: reflected
    green gets stronger or weaker? (3) walk around the oil slick — do the colours move?
    (4) is the film's transmitted colour the same as its reflected colour? (targets
    `film-color-is-pigment`)
  - *explore:* stack builder — $n_1, n_2, n_3$ (0.05 steps), $d$ 0–2000 nm, $\theta$
    0–80°, s/p, $\lambda$ slider; live panels: the two reflected phasors tip-to-tail
    (with the $\pi$ flips visible as arrow reversals), $R(\lambda)$ spectrum, **reflected
    and transmitted colour swatches** side by side; presets: soap film in air, oil on
    water, MgF$_2$ on glass.
  - *derive:* two-reflection geometry → $\Lambda = 2n_2 d\cos\theta_t$ → the $\pi$
    decision table from the Fresnel signs (cite `18-fresnel`'s rules: $r < 0$ exactly
    when the far side is denser, near normal incidence) → maxima/minima by stack
    ordering → the exact sum: geometric series of internal bounces →
    $r = (r_{12} + r_{23}e^{2\ii\beta})/(1 + r_{12}r_{23}e^{2\ii\beta})$ → $R + T = 1$
    → the colour pipeline → AR coating: $r_{12} = r_{23}$ needs $n_2 = \sqrt{n_1 n_3}$,
    $\beta = \pi/2$ makes the arrows antiparallel and equal → the algebra box.
  - *verify:* two-beam approximation vs exact $R$ across $r$ magnitudes (good below
    $R \approx 0.1$, `numerical-observation`); $R + T = 1$ sweep over $(\lambda,\theta)$,
    both polarizations; `ar_coating_design` null at $\lambda_0$ exact;
    `transfer_matrix_stack` ≡ `thin_film_amplitude` for one layer.
  - *transfer:* `26-fabry-perot` (same series, mirrors instead of a film — high-$R$
    limit); `44-resonators` / `54-photonic-crystals` (quarter-wave stacks); `10-impedance`
    backward (the unification); camera lenses and eyeglasses (why coated optics look
    faintly purple); butterfly wings and beetle shells — structural colour; oil-slick
    thickness gauging in engineering.
  - *quiz:* the black-film question; **the "which reflection gets the $\pi$" decision as
    its own item** (the classic trap); AR numeric; complementarity MC (registry
    distractor); angle-shift MC.
  - *explain:* why the drained film is black, in three sentences, without formulas; how
    you could measure a soap film's thickness with a lamp and a spectrometer; what the
    coating on your glasses is *doing*, told as an impedance story.
  - *advanced:* $2\times2$ transfer matrices — one matrix per layer, multiply, read
    $r, t$; a $(HL)^m$ quarter-wave stack's reflectance grows toward 1 (computed, not
    proved) — the dielectric mirrors that `26-fabry-perot` and `44-resonators` will
    assume. Safe to skip: nothing in 25–27 core needs matrices.
- **Core derivations:** (1) OPD with the tangent-plane construction:
  $\Lambda = 2n_2 d\cos\theta_t$ (the classic wrong answer $2n_2 d/\cos\theta_t$
  discussed); (2) total phase
  $\delta = 4\pi n_2 d\cos\theta_t/\lambda + \Delta\varphi_{\text{refl}}$ with
  $\Delta\varphi_{\text{refl}} \in \{0, \pi\}$ from the Fresnel signs — condition table
  for both orderings; (3) exact single-film sum (geometric series, quotable convergence
  since $|r_{12}r_{23}| < 1$); (4) colour pipeline:
  $X = \int R(\lambda)S_{D65}(\lambda)\bar{x}(\lambda)\,d\lambda$ (and $Y, Z$) → linear
  sRGB matrix → gamma encode → clip, with the gamut honesty note; (5) AR design and the
  impedance parallel: light's wave impedance in a medium is $Z_0/n$, so
  $r = (n_1 - n_2)/(n_1 + n_2)$ *is* `waves.junction_coefficients` with $Z \to 1/n$, and
  $n_2 = \sqrt{n_1 n_3}$ *is* the string's $Z = \sqrt{Z_1 Z_3}$ quarter-wave transformer
  — same algebra box, side by side (`waves.impedance`, `waves.power_coefficients` cited
  for the string column).
- **Model specification draft:** System — one homogeneous film between two semi-infinite
  media, plane-wave illumination; observables are $R$, $T$, spectra, colour coordinates.
  Dynamics — none; stationary multiple reflection. Boundary — infinite plane-parallel
  interfaces; smooth on the scale of $\lambda$. Ensemble — deterministic; illuminant
  enters only through the colour integral. Ignored — absorption unless complex $n$
  given; film-thickness gradients (wedge fringes live in the problem set); roughness and
  scattering. Valid when — $d$ within an order of magnitude of $\lambda$ for visible
  colour effects; indices weakly dispersive across the band (or supplied per
  wavelength). Failure modes — dropped/double $\pi$; two-beam approximation trusted at
  high $R$; colour read as pigment; sRGB clipping mistaken for physics.
- **Epistemic classification:** OPD formula and $\pi$-shift rules — `theorem` (from the
  Fresnel signs, cited); exact film sum — `theorem`; colour-matching functions —
  `empirical-law` (boxed: CIE 1931 is measured human physiology, not physics of light);
  two-beam adequacy threshold — `numerical-observation`; "smooth infinite film" —
  `model-assumption`.
- **Misconceptions:** NEW **`film-color-is-pigment`** — "Thin-film colours come from
  selective absorption, like a dye." Falsifying experiment: the lab computes reflected
  *and* transmitted swatches and verifies $R + T = 1$ at every wavelength — nothing is
  absorbed, the two colours are complementary; tilting the film shifts the colour, which
  no pigment does. Distractor: quiz option "the soap solution absorbs the missing
  colours". (The which-reflection-$\pi$ trap is deliberately a quiz item, `Q-24-2`, not
  a registry entry — it is an error pattern, not a stable wrong model.)
- **Glossary terms:** `thin-film-interference` (התאבכות בשכבה דקה),
  `anti-reflection-coating` (ציפוי מונע החזרה), `phase-thickness` (עובי מופע — translator
  to confirm), `iridescence` (ססגוניות; `he_reject` candidate: אירידסצנציה),
  `chromaticity` (כרומטיות), `transfer-matrix` (מטריצת מעבר), `structural-color`
  (צבע מבני).
- **Interactive controls and simulations:** stack builder as in *explore*; draining-film
  timeline (thickness ramps down, colour strip accrues — the bubble's life story);
  AR-coating designer: pick $n_1, n_3, \lambda_0$, see the null appear and the residual
  $R(\lambda)$ curve.
- **Virtual lab outline** (`notebooks/en/labs/24-thin-films.ipynb`): (1) stack-builder
  play + prediction checks; (2) *measurement* (master plan §23 "Thin film → optical
  thickness"): synthetic reflectance spectrum of an unknown film with noise, extract
  $n_2 d$ from the fringe period in $1/\lambda$ (an FFT via `fourier.spectrum` — the
  spectral fringes are literally a frequency), report $n_2 d \pm \sigma$; (3) draining
  soap film: spectrum + colour trajectory vs time, compare with the photographed colour
  sequence of a real bubble; (4) design task: AR coat a lens for 550 nm, then compute
  how much the null degrades for ±5% thickness error (tolerance analysis).
- **Real-experiment counterpart:** soap film on a dark mug or bubble wand, oil drop on
  wet asphalt — photograph in daylight, import an RGB row, compare the colour *sequence*
  vs thickness with the predicted strip (colour order is fit-free evidence).
- **Media assets** (`render_interference.py`): (c) draining film: colour strip and
  $R(\lambda)$ evolving together as $d$ shrinks, ending black; (d) the two reflected
  arrows vs $d$ at fixed $\lambda$, $\pi$ flips marked by arrow reversal.
- **Quiz bank outline:** `Q-24-1` MC — black film (OBJ-24-1); `Q-24-2` MC — which
  reflection carries $\pi$ in air|film|glass vs air|film|air (OBJ-24-1, the trap item);
  `Q-24-3` MC — maxima condition swap between orderings (OBJ-24-2); `Q-24-4` numeric —
  MgF$_2$ ($n = 1.38$) on glass at 550 nm: $d \approx 100$ nm (OBJ-24-5); `Q-24-5` MC —
  transmitted vs reflected colour (OBJ-24-4, distractor `film-color-is-pigment`);
  `Q-24-6` numeric — first-order bright thickness of a soap film at given $\lambda$,
  $\theta$ (OBJ-24-2, OBJ-24-3); `Q-24-7` free — the impedance-matching parallel in
  words (OBJ-24-5).
- **Problem set outline:** analytical — Newton's rings radii; wedge-film fringe spacing;
  show $r_{12} = r_{23}$ ⇔ $n_2 = \sqrt{n_1 n_3}$; two-beam vs exact $R$ at the AR
  point. Computational — broadband AR: minimise average $R$ over the visible with a
  two-layer coating (a first taste of optimisation); reproduce an oil-slick photo's
  palette. Challenge — transfer-matrix $(HL)^5$ mirror: compute $R(\lambda)$, find the
  stop band, and check against `26-fabry-perot`'s needed mirror.
- **Runtime budget:** spectra at ~400 wavelengths × slider updates — trivial; CIE
  integration is three dot products; transfer matrices ≤ 20 layers. All sub-second.
- **Validation gates:** standard set with `--module 24-thin-films`; plus the
  $R + T = 1$, AR-null, and matrix-consistency tests of §4.
- **Open questions for the author:** whether dispersion $n_2(\lambda)$ enters the core
  colour pipeline or stays a lab option (recommendation: constant $n$ in core, flagged
  as `model-assumption`; dispersive soap preset in the lab); whether the colour swatch
  needs a gamut-warning indicator when clipping activates (recommendation: yes, small
  dot — honesty is the pipeline's point).

### 5.3 `25-michelson` — The Michelson interferometer as a measuring instrument

- **Identity and scope:** master-plan notebook 8.4. The Michelson as an *instrument*,
  not a diagram: fringe counting → wavelength, white-light fringes → coherence length,
  FTIR → spectra. Deferred: quantitative Wiener–Khinchin → `27-coherence`;
  Twyman–Green/optical testing and Mach–Zehnder → mention only; LIGO's cavity tricks →
  `26-fabry-perot` and the research box.
- **Prerequisites:** `23-interference` (two-beam law, visibility phenomenon);
  `04-fourier-transform` (`fourier.spectrum` for the FTIR cell); `16-light-in-matter`
  (glass adds optical path — the compensator's reason).
- **Learning objectives:**
  - `OBJ-25-1` — Trace both arms and derive I(Delta d) = (I0/2)(1 + cos(4 pi Delta d / lambda))
    for a monochromatic source, identifying the factor 2 from the folded path.
  - `OBJ-25-2` — Measure a wavelength by fringe counting, N = 2 Delta d / lambda, with an
    uncertainty budget including miscount and mirror drift.
  - `OBJ-25-3` — Explain the compensator plate: equal glass in both arms makes the zero
    path difference common to all wavelengths.
  - `OBJ-25-4` — Locate white-light fringes near zero path difference and use the fringe
    packet's width to estimate the source's coherence length.
  - `OBJ-25-5` — Explain qualitatively why the interferogram is the field autocorrelation
    and why its Fourier transform is the source spectrum (FTIR).
- **Mathematical background:** has — two-beam law, FFT; introduced here — the delay
  variable $\tau = 2\Delta d/c$ as the instrument's native coordinate; spectral
  superposition of fringe patterns (an integral over $\omega$, done numerically before
  27 does it formally).
- **Physical intuition goals:** (1) the mirror moves $\lambda/2$ per fringe — the
  factor-2 reflex; (2) a fringe counter is a ruler with $\sim$300 nm ticks; (3) each
  wavelength writes its own cosine — only at $\Delta d = 0$ do they all agree (white-light
  fringe packet); (4) the broader the spectrum, the narrower the packet — the bandwidth
  theorem seen in hardware.
- **Section skeleton seeds:**
  - *puzzle:* Michelson sold the metre in wavelengths of cadmium light in 1892 — with
    mirrors, a lamp, and his eyes he measured lengths to parts in $10^8$. Today the same
    layout (plus module 26's cavities) detects mirror motions of $10^{-18}$ m. (Boxed:
    how does *counting fringes* turn light itself into a length standard?)
  - *predict:* (1) move the mirror by $\lambda/2$ — how many fringes pass? (the folded
    path) (2) replace the laser with white light: fringes everywhere, nowhere, or
    somewhere special? (targets `laser-needed-for-interference`) (3) slide a glass plate
    into one arm — what happens to the fringes and where did zero go? (4) with a sodium
    lamp the fringes fade, then *revive* as the mirror moves on — what could cause that?
    (the doublet; 27 teaser)
  - *explore:* **virtual bench**: mirror position with nm-step buttons and a µm drive,
    source selector (HeNe / sodium doublet / LED / white light), live detector trace
    $I$ vs $\Delta d$, running fringe counter, compensator toggle, glass-plate insertion;
    the student *drives the instrument* — nothing updates except through the bench.
  - *derive:* beam-splitter amplitude split → recombination → $\delta = 2k\Delta d$ →
    $I(\Delta d)$ → fringe counting $N = 2\Delta d/\lambda$ → polychromatic source: each
    $\omega$ adds its own cosine, so $I(\Delta d) - \bar{I} \propto \Real\,\gamma(\tau)$
    with $\tau = 2\Delta d/c$ — envelope = fringe visibility, packet width =
    coherence length → compensator (dispersion balance) → FTIR: Fourier-transform the
    interferogram, get $S(\omega)$ — Wiener–Khinchin *previewed, kept qualitative*, the
    theorem itself is 27's (`theorem` box lives there; here an `empirical-law`-of-the-lab
    style demonstration).
  - *verify:* `michelson_intensity` ≡ `two_beam_intensity` under the arm mapping; fringe
    count integer consistency across a sweep; sodium-doublet visibility revival period
    $\Delta(\Delta d) = \lambda^2/(2\Delta\lambda)$ measured vs formula
    (`numerical-observation`); FTIR round trip: `fourier.spectrum` of the synthetic
    interferogram recovers the source lines.
  - *transfer:* `26-fabry-perot` (multiple-beam sharpening; LIGO's arm cavities);
    `27-coherence` (the envelope becomes $|\gamma(\tau)|$, the revival becomes beats of
    two lines); `04-fourier-transform` backward (the FFT earns a salary); FTIR
    spectrometers in every chemistry lab; optical coherence tomography — medical imaging
    that *ranges* tissue by coherence gating; LIGO (research box).
  - *quiz:* factor-2 numeric; fringe-count wavelength numeric; compensator MC;
    white-light MC (registry distractor); sodium-revival MC.
  - *explain:* why white-light fringes exist only near zero path difference; what the
    compensator compensates, precisely; how you would tell a friend the interferogram
    "contains" the spectrum.
  - *advanced:* the LIGO research box with honest ballparks — arms $L = 4$ km, strain
    $h \sim 10^{-21}$ → $\Delta L \sim 4\times10^{-18}$ m ($\sim10^{-3}$ proton radii);
    the gap between one fringe ($\sim10^{-7}$ m) and that number is closed by arm
    cavities (module 26, $\sim$300 bounces), watts→kilowatts of circulating power
    against shot noise $\propto 1/\sqrt{P}$, and seismic isolation — each factor named,
    none derived; explicitly order-of-magnitude.
- **Core derivations:** (1) $I(\Delta d) = \tfrac{I_0}{2}[1 + \cos(2k\Delta d)]$
  (lossless 50:50 splitter; the other half exits the input port — energy audit in a
  footnote box); (2) $N = 2\Delta d/\lambda$ and its inversion with uncertainty
  ($\sigma_\lambda/\lambda = \sqrt{(\sigma_{\Delta d}/\Delta d)^2 + (1/N)^2}$ for a
  ±1-count error); (3) polychromatic superposition
  $I(\Delta d) = \int S(\omega)\,\tfrac12[1 + \cos(2\omega\Delta d/c)]\,d\omega$ →
  envelope/packet; (4) sodium doublet: two cosines beat, visibility period
  $\lambda^2/(2\Delta\lambda)$.
- **Model specification draft:** System — two-arm amplitude-splitting interferometer:
  ideal 50:50 splitter, movable mirror, detector reading cycle-averaged intensity vs
  $\Delta d$. Dynamics — none; quasi-static mirror motion. Boundary — plane mirrors,
  perfect alignment (a single fringe fills the field; alignment fringes are a lab
  aside). Ensemble — deterministic per source spectrum; drift noise added via
  `wavelab.measurement`. Ignored — splitter dispersion (delegated to the compensator),
  polarization, beam divergence, mirror figure. Valid when — path differences within
  the source coherence length for fringe work; detector slow against optical cycles.
  Failure modes — forgetting the folded-path factor 2; counting fringes with a drifting
  zero; trusting fringes beyond $\ell_c$; reading the input-port return as lost energy.
- **Epistemic classification:** $I(\Delta d)$ law — `theorem` (two-beam law applied);
  fringe-count inversion — `definition`-level metrology plus uncertainty
  (`approximation` for the drift model); interferogram → spectrum — stated as
  *demonstrated* here (`numerical-observation` on the FTIR cell), *proved* in 27;
  "ideal 50:50 splitter" — `model-assumption`.
- **Misconceptions:** NEW **`laser-needed-for-interference`** — "Interference fringes
  require laser light." Falsifying experiment: the bench's white-light source shows
  clear (coloured, few) fringes once $|2\Delta d| < \ell_c$ — and Young's 1803
  experiment predates the laser by 157 years; the laser buys coherence *length*, not
  interference *permission*. Distractor: quiz option "with a lamp instead of a laser
  the detector shows no modulation at any mirror position".
- **Glossary terms:** `interferometer` (אינטרפרומטר; `he_reject` candidate: מד־התאבכות
  — translator to decide), `beam-splitter` (מפצל אלומה), `compensator-plate`
  (לוח פיצוי), `zero-path-difference` (הפרש דרכים אפס), `interferogram`
  (אינטרפרוגרמה), `fourier-transform-spectroscopy` (ספקטרוסקופיית התמרת פורייה),
  `fringe-counting` (ספירת פסים).
- **Interactive controls and simulations:** the virtual bench (mirror nm-steps, source
  menu, compensator toggle, glass plate); packet explorer: source bandwidth slider vs
  fringe-packet width, side by side with the source's $S(\omega)$ (the bandwidth theorem
  as an instrument reading).
- **Virtual lab outline** (`notebooks/en/labs/25-michelson.ipynb`): (1) drive the bench,
  verify $\lambda/2$ per fringe; (2) *measurement* (master plan §23 "Michelson →
  wavelength/displacement"): sweep the mirror ~50 µm with synthetic mirror-drift noise
  (slow thermal ramp + jitter via `measurement.add_noise`), count fringes
  electronically, extract $\lambda \pm \sigma$ with the miscount/drift budget;
  (3) coherence length: switch to the LED, map visibility vs $\Delta d$, report
  $\ell_c$; (4) FTIR: record the sodium-doublet interferogram, `fourier.spectrum` it,
  report the doublet splitting ± uncertainty (compare 0.6 nm).
- **Real-experiment counterpart:** none practical at home — a stable Michelson needs
  vibration isolation a kitchen table cannot give; the lab instead ships an import cell
  for lecture-demo data (fringe video → intensity trace) so real fringe counting can be
  analysed when a teaching lab provides it.
- **Media assets** (`render_interference.py`): (e) fringes flowing past the detector as
  the mirror sweeps, counter incrementing (no burned-in text — counter is a tick
  strip); (f) white-light packet: source bandwidth widening while the fringe packet
  narrows around $\Delta d = 0$.
- **Quiz bank outline:** `Q-25-1` numeric — fringes per µm of mirror travel at 633 nm
  (OBJ-25-1); `Q-25-2` numeric — $\lambda$ from $N$ and $\Delta d$ with uncertainty
  (OBJ-25-2); `Q-25-3` MC — compensator's purpose (OBJ-25-3); `Q-25-4` MC — where
  white-light fringes appear (OBJ-25-4, distractor `laser-needed-for-interference`);
  `Q-25-5` MC — sodium fade-and-revive cause (OBJ-25-4, OBJ-25-5); `Q-25-6` free — why
  the interferogram's FT is the spectrum, in words (OBJ-25-5).
- **Problem set outline:** analytical — glass plate of thickness $t$, index $n$ in one
  arm: fringe shift count; visibility of a top-hat spectrum (sinc envelope — pair-zoo
  callback); doublet revival period derivation. Computational — fringe-counting
  wavelength measurement vs drift-rate sweep (when does the method break?); FTIR
  resolution vs scan length (the $\Delta\omega \sim 1/\tau_{\max}$ trade).
  Challenge — design a fringe-counting displacement gauge spec: given $\sigma_\lambda$
  and drift, what displacement uncertainty can 10 s of data buy?
- **Runtime budget:** traces ≤ $10^5$ points, FTIR FFTs ≤ $2^{16}$ — sub-second; the
  bench animation ≤ 60 frames per interaction.
- **Validation gates:** standard set with `--module 25-michelson`; plus the
  doublet-revival and `michelson_intensity` limit tests of §4.
- **Open questions for the author:** whether the LIGO box cites strain sensitivity as
  $10^{-21}$ flat or shows the noise-curve shape (recommendation: single number + one
  sentence that it is frequency-dependent); whether alignment fringes (tilted mirror →
  fringe field) merit an explore toggle or stay out (recommendation: out of core, lab
  aside — keeps the ideal-alignment model spec honest).

### 5.4 `26-fabry-perot` — Fabry–Pérot: multiple-beam interference

- **Identity and scope:** master-plan notebook 8.5. The plane-mirror étalon/cavity: Airy
  function, finesse, FSR, linewidth, resolving power, photon lifetime. Deferred: mirror
  curvature, transverse modes, stability → `44-resonators`; gain and threshold →
  `45-lasers`; Gaussian beams → `43-gaussian-beams`.
- **Prerequisites:** `23-interference` (two-beam law as the $N = 2$ special case);
  `24-thin-films` (the geometric series — same sum, higher $R$); `10-impedance` ("two
  junctions, many bounces" — its transfer bullet lands here); `02-damped-driven` (the
  Lorentzian and $Q$); `04-fourier-transform` (`lorentzian_spectrum` for the lineshape
  overlay).
- **Learning objectives:**
  - `OBJ-26-1` — Derive the Airy transmission T = 1/(1 + F sin^2(delta/2)) with
    F = 4R/(1 - R)^2 by summing the infinite geometric series of transmitted phasors.
  - `OBJ-26-2` — Compute finesse = pi sqrt(R)/(1 - R), free spectral range
    Delta nu = c/(2 n L), and linewidth delta nu = FSR/finesse, and predict how each
    responds to R and L.
  - `OBJ-26-3` — Explain physically why a lossless cavity of two highly reflective
    mirrors transmits T = 1 on resonance.
  - `OBJ-26-4` — Show that the near-resonance lineshape is Lorentzian and connect its
    width to the photon lifetime and the cavity Q.
  - `OBJ-26-5` — Resolve two nearby wavelengths with a scanning cavity and compute the
    chromatic resolving power lambda/Delta lambda = m * finesse.
  - `OBJ-26-6` — (advanced) Relate cavity ringdown decay time to linewidth,
    delta omega ~ 1/tau_p, and measure Q from the decay.
- **Mathematical background:** has — geometric series of phasors (00, 24), Lorentzian
  (02, 04); introduced here — round-trip phase $\delta = 4\pi n L\cos\theta/\lambda$ as
  the resonance variable; the comb-of-Lorentzians picture of a periodic resonator.
- **Physical intuition goals:** (1) two 99% mirrors at the right spacing pass 100% of
  the light — resonance is a conspiracy of phasors, not a leak; (2) raising $R$ makes
  peaks *narrower*, not shorter; (3) doubling $L$ halves the FSR (more resonances in the
  same band); (4) a sharper line means a longer-lived photon — linewidth is a lifetime
  in disguise.
- **Section skeleton seeds:**
  - *puzzle:* one mirror reflecting 99% transmits 1%. Add a *second* 99% mirror behind
    it — and at the right spacing the pair transmits **everything**. (Boxed: how can
    adding a nearly perfect mirror make the pair transparent?) — `two-mirrors-block-light`
    confronted in the first paragraph.
  - *predict:* (1) $T$ through two $R = 0.99$ mirrors at resonance: closer to $10^{-4}$
    or to 1? (targets `two-mirrors-block-light`) (2) raise $R$: do peaks get shorter,
    narrower, or both? (3) double $L$: what happens to the spacing between transmission
    peaks? (4) could this device distinguish 632.8 nm from 632.9 nm? What property
    decides?
  - *explore:* master plan §29's dials — $R$, $L$, $n$, $\lambda$ — with panels:
    circulating-phasor animation (transmitted arrows curling into a spiral off
    resonance, unrolling into a straight line *at* resonance — the geometric series
    drawn), $T(\nu)$ comb with FSR bracket, single-peak zoom with FWHM readout and
    Lorentzian overlay, two-line source overlay for the resolving game.
  - *derive:* transmitted amplitude series
    $E_t \propto t_1 t_2 e^{\ii\delta/2}\sum_{m\ge0}(r_1 r_2 e^{\ii\delta})^m$ — the
    module-00 arithmetic literally summed to closure → for symmetric lossless mirrors
    $T = 1/(1 + F\sin^2(\delta/2))$, $F = 4R/(1-R)^2$ → resonance condition
    $\delta = 2\pi m$ (standing-wave picture, `11-standing-waves` echo) → FSR
    $\Delta\nu = c/2nL$ → FWHM and finesse $\mathcal{F} = \pi\sqrt{R}/(1-R)$ →
    near-resonance expansion $\sin^2(\delta/2) \approx (\delta - 2\pi m)^2/4$ →
    **Lorentzian** — the same curve as `steady_state_response` squared and
    `lorentzian_spectrum`, now in optical frequency → photon lifetime
    $\tau_p = -t_{\text{rt}}/\ln(R_1R_2) \approx nL/[c(1-R)]$ → $\delta\nu = 1/(2\pi\tau_p)$
    consistency with FSR/$\mathcal{F}$ → $Q = \nu/\delta\nu = \omega\tau_p$ (huge:
    $\sim10^8$ for a modest cavity — compare module 02's tuning forks) → resolving
    power $\lambda/\Delta\lambda = m\mathcal{F}$.
  - *verify:* finite-sum convergence to Airy at rate $R^N$ (`numerical-observation`:
    fitted decay of the truncation error); peak $T = 1.000$ lossless at $R = 0.99$;
    FWHM vs $\mathcal{F}$ formula across $R$; Lorentzian fit residuals near resonance;
    $R_{\text{cav}} + T_{\text{cav}} = 1$ across $\delta$.
  - *transfer:* `44-resonators` (curved mirrors, stability, transverse modes — FSR
    returns as longitudinal-mode spacing); `45-lasers` (a laser is this cavity with
    gain: threshold = round-trip break-even); `24-thin-films` backward (same series,
    $R$ small vs large) and its quarter-wave stack as *the* way to make $R = 0.999$;
    `25-michelson` (LIGO's arm cavities close that box's gap); laser-line and
    etalon-based spectroscopy; `54-photonic-crystals` (many weak mirrors).
  - *quiz:* resonance-$T$ MC (registry distractor); finesse/FSR/linewidth numerics;
    peaks narrower-not-shorter MC; resolving-power design numeric.
  - *explain:* the two-mirror paradox to a friend, using arrows, in four sentences; why
    "narrower line" and "longer photon storage" are the same fact; what finesse *counts*
    (bounces, roughly — $\mathcal{F} \approx$ number of effective round trips).
  - *advanced:* cavity ringdown: switch the input off, watch $T$ decay as
    $e^{-t/\tau_p}$; extract $\tau_p$, hence $\delta\nu$ and $Q$ — the part-01 "Q three
    ways" reunion (`q_from_ringdown` on the decay, `q_from_bandwidth` on the Airy peak,
    `q_from_phase_slope` on the transmitted phase across resonance — three optics
    measurements, one number; functions cited by name, owned by part-01). Safe to skip:
    45 restates what it needs.
- **Core derivations:** as in the seeds; written with the course convention
  ($e^{\ii\delta}$ per round trip under $e^{-\ii\omega t}$), the series' closed form
  quotable in one line, and the lossless identity $T + R_{\text{cav}} = 1$ derived, not
  asserted. The Lorentzian connection made explicit:
  $T(\nu) \approx \dfrac{(\delta\nu/2)^2}{(\nu - \nu_m)^2 + (\delta\nu/2)^2}$ near
  $\nu_m$ — module 02's resonance curve in frequency space, third member of the
  Lorentzian family after 02 and 04 (27 adds the fourth).
- **Model specification draft:** System — two plane parallel mirrors (field reflectance
  $r$, lossless unless stated) enclosing index $n$, plane-wave illumination; observables
  $T$, $R_{\text{cav}}$, transmitted phase, ringdown. Dynamics — none in core; ringdown
  is the one transient (advanced). Boundary — infinite plane mirrors, perfect
  parallelism and alignment. Ensemble — deterministic. Ignored — mirror absorption and
  scatter (a loss note states where real cavities' $T_{\text{peak}} < 1$ goes),
  diffraction/walk-off, mirror curvature, gain. Valid when — beam diameter ≫ $\lambda$,
  alignment good to ≪ $\lambda$ across the beam, source linewidth ≪ FSR for clean
  scans. Failure modes — multiplying intensity transmittances ($T_1 T_2$ reasoning);
  treating finesse as fixed when $R$ disperses; reading real-cavity peak loss as an
  Airy failure rather than absorption.
- **Epistemic classification:** Airy formula, finesse, FSR, linewidth — `theorem`
  (series summed in view); $T = 1$ lossless on resonance — `theorem` with the loss
  caveat boxed as `model-assumption`; near-resonance Lorentzian — `approximation`
  (validity: $\mathcal{F} \gtrsim 10$); truncation-error decay $\propto R^N$ —
  `numerical-observation`; photon-lifetime linewidth identity — `theorem` at the
  course's level (exact only as $R \to 1$, stated).
- **Misconceptions:** NEW **`two-mirrors-block-light`** — "Two highly reflective
  mirrors in series transmit almost nothing (T = T1 x T2)." Falsifying experiment: the
  lab measures $T = 1.0$ at resonance for lossless $R = 0.99$ mirrors, and the
  phasor-curl animation shows *why* — the intracavity field builds until the leak
  through mirror 2 equals the input. Distractor: quiz option computing
  $T = 0.01 \times 0.01 = 10^{-4}$.
- **Glossary terms:** `fabry-perot` (פברי–פרו), `etalon` (אטלון), `airy-function`
  (פונקציית איירי), `finesse` (פינסה; `he_reject` candidate: חדות — translator to
  decide), `free-spectral-range` (תחום ספקטרלי חופשי), `linewidth` (רוחב קו),
  `resolving-power` (כושר הפרדה), `photon-lifetime` (זמן חיי פוטון), `cavity-ringdown`
  (דעיכת הד במהוד — translator to confirm).
- **Interactive controls and simulations:** the $R/L/n/\lambda$ dashboard as in
  *explore*; scanning-cavity mode: piezo ramp on $L$, detector trace vs time — the
  instrument every laser lab owns; ringdown mode (advanced): input chopped, log-scale
  decay with fitted $\tau_p$.
- **Virtual lab outline** (`notebooks/en/labs/26-fabry-perot.ipynb`): (1) dashboard
  play; the two-mirror paradox measured first; (2) *calibration:* scan $L$, identify
  FSR from peak spacing, calibrate the piezo axis; (3) *measurement* (master plan §23
  "Fabry–Pérot → finesse and FSR"): measure FWHM/finesse vs $R$ across a sweep,
  fit against $\pi\sqrt{R}/(1-R)$ with noise (`measurement.add_noise` on the detector);
  (4) *spectroscopy:* an unknown source with two lines ~0.1 nm apart — choose $L$ and
  $R$ to resolve them, report the splitting ± uncertainty (the design-your-instrument
  moment); (5) advanced: ringdown → $\tau_p$ → $\delta\nu$, cross-checked against (3).
- **Real-experiment counterpart:** none practical — supermirror cavities are not
  household items; the closest honest pairing is noticing étalon fringes in a window
  pane or camera sensor cover glass (a photo import shows the periodic-in-$1/\lambda$
  channel spectrum; one sentence connects it to `fp_spectrum` with low $R$).
- **Media assets** (`render_interference.py`): (g) phasor-curl: transmitted arrows
  spiralling shut as $\delta$ sweeps through resonance; (h) Airy comb morphing as $R$
  rises 0.2 → 0.97 — peaks sharpening at fixed height, FSR bracket steady.
- **Quiz bank outline:** `Q-26-1` MC — two-mirror resonance transmission (OBJ-26-3,
  distractor `two-mirrors-block-light`); `Q-26-2` numeric — finesse and linewidth for
  $R = 0.95$, $L = 5$ mm (OBJ-26-2); `Q-26-3` MC — effect of raising $R$ on peak
  height/width (OBJ-26-2); `Q-26-4` numeric — FSR for a given $L, n$, and the $L$ to
  resolve a stated doublet (OBJ-26-5); `Q-26-5` MC — Lorentzian lineshape provenance
  (OBJ-26-4); `Q-26-6` free — linewidth ↔ photon lifetime in words (OBJ-26-4,
  OBJ-26-6).
- **Problem set outline:** analytical — derive $\mathcal{F} = \pi\sqrt{R}/(1-R)$ from
  the FWHM condition; asymmetric mirrors $R_1 \ne R_2$: peak transmission
  $< 1$ (impedance mismatch — tie to 24's algebra box); étalon in a converging beam:
  ring pattern radii. Computational — truncation study $N$ bounces vs Airy;
  absorption's effect on peak $T$ (add $\kappa$); design a cavity to resolve the sodium
  doublet with margin. Challenge — pulse response: send a short pulse in, watch the
  ring-down train, connect the pulse-train FT to the Airy comb (pair-zoo full circle).
- **Runtime budget:** Airy evaluations trivial; finite sums ≤ 300 bounces; ringdown
  traces ≤ $10^5$ points; scanning animations ≤ 90 frames. All sub-second in Pyodide.
- **Validation gates:** standard set with `--module 26-fabry-perot`; plus the Airy
  limit/convergence/conservation tests of §4.
- **Open questions for the author:** whether the standing-wave (`11-standing-waves`)
  picture of resonance appears in core derive or transfer (recommendation: one
  sentence in derive — the travelling-series and standing-mode views are the same
  condition); whether absorption enters core or stays in problems (recommendation:
  problems — the core keeps the lossless `model-assumption` box sharp).

### 5.5 `27-coherence` — Temporal and spatial coherence

- **Identity and scope:** master-plan notebook 8.6, closing the thread the $\gamma$
  slider opened in 23: visibility quantified, $\gamma(\tau)$ defined, Wiener–Khinchin
  proved and measured, spatial coherence at the double-slit-with-extended-source level.
  Deferred: van Cittert–Zernike as an imaging theorem → `41-imaging-coherence`; photon
  statistics and $g^{(2)}$ → `52-quantum-optics`.
- **Prerequisites:** `23-interference` (the $\gamma$ slider phenomenon, visibility of
  unequal beams); `25-michelson` (envelope, sodium revival — data this module
  explains); `04-fourier-transform` (pair zoo, `rms_widths`, bandwidth theorem);
  `00-phasors` (`random_phasor_sum`, the violinists).
- **Learning objectives:**
  - `OBJ-27-1` — Compute fringe visibility V = (Imax - Imin)/(Imax + Imin) from a fringe
    trace and relate V = |gamma| for equal beams (and the general unequal-beam formula).
  - `OBJ-27-2` — Define the degree of coherence gamma(tau) as the normalized field
    autocorrelation and compute it from a spectrum via the Wiener-Khinchin theorem.
  - `OBJ-27-3` — Estimate coherence time as tau_c ~ 1/Delta omega and coherence length
    ell_c = c tau_c ~ lambda^2 / Delta lambda from spectral data — the Part-0 bandwidth
    theorem applied to light.
  - `OBJ-27-4` — Match lineshapes to coherence decays: Lorentzian spectrum <-> exponential
    |gamma|, Gaussian <-> Gaussian.
  - `OBJ-27-5` — Predict double-slit fringe washout for an extended source and estimate
    an unresolved source's angular size from the baseline where visibility vanishes.
  - `OBJ-27-6` — Rank common sources (sunlight, LED, sodium lamp, HeNe, single-mode
    laser) by coherence length with order-of-magnitude numbers.
- **Mathematical background:** has — FT pairs, RMS widths, autocorrelation as an
  integral, ensemble averages (00's random walk); introduced here — stationarity (time
  origin irrelevance) as the assumption that makes $\gamma(\tau)$ well defined; the
  normalized correlation function as a general tool.
- **Physical intuition goals:** (1) coherence is a *budget*, not a badge — every source
  has some $\tau_c$, and fringes survive while delays stay inside it; (2) the narrower
  the spectrum, the longer the coherence — one inequality, third costume; (3) an
  extended source is many independent point sources whose fringe patterns smear;
  (4) "incoherent" light differs from laser light the way 00's random-phase violinists
  differ from the marching band.
- **Section skeleton seeds:**
  - *puzzle:* Young made fringes with *sunlight* in 1803 — 157 years before the laser.
    Yet two flashlights a metre apart make none, and module 25's white-light fringes
    died a few microns from zero. (Boxed: what exactly does interference *require* of a
    source — and how much of it does sunlight have?)
  - *predict:* (1) sunlight through a pinhole onto a double slit: fringes or not?
    (2) as the Michelson arm lengthens, visibility drops: suddenly or gradually?
    (targets `coherence-is-binary`) (3) widen the source slit behind Young's pair: do
    fringes dim or blur? (4) which has the longer coherence length, a red LED or a
    sodium lamp — by roughly what factor?
  - *explore:* **coherence explorer** — spectrum builder (Lorentzian / Gaussian /
    doublet / comb presets, $\Delta\lambda$ slider) with three synchronized panels:
    $S(\omega)$, $|\gamma(\tau)|$ (live `degree_of_coherence` via FFT), and the
    resulting Michelson/Young fringe trace at an adjustable delay — 23's five-panel
    reflex extended to statistics. **Spatial panel:** source angular size $\theta_s$ vs
    slit separation $d$, live visibility readout, "measure the star" game.
  - *derive:* two beams with true fields → $I = I_1 + I_2 + 2\sqrt{I_1I_2}\,\Real\gamma(\tau)$
    — 23's phenomenological $\gamma$ now *derived* → visibility
    $V = 2\sqrt{I_1I_2}|\gamma|/(I_1 + I_2)$, $= |\gamma|$ for equal beams →
    $\gamma(\tau) = \langle \hat{E}^*(t)\hat{E}(t+\tau)\rangle/\langle|\hat{E}|^2\rangle$
    → **Wiener–Khinchin** (the part's crowning theorem, boxed):
    $\gamma(\tau) = \int S(\omega)e^{-\ii\omega\tau}d\omega \big/ \int S(\omega)d\omega$
    — proof at course level by writing the field as its Fourier decomposition and
    letting stationarity kill the cross terms, the same cross-term-vanishing arithmetic
    as 00's random walk → $\tau_c$ from the RMS width of $|\gamma|$
    (`fourier.rms_widths` on the correlation), $\tau_c \approx 1/\Delta\omega$, the
    **Part-0 bandwidth theorem payoff — said in exactly those words** →
    $\ell_c = c\tau_c \approx \lambda^2/\Delta\lambda$ → the pairs transposed:
    Lorentzian $S$ ↔ exponential $|\gamma|$ (`lorentzian_spectrum` ↔
    `exp_decay`, read the other way), Gaussian ↔ Gaussian → spatial coherence: each
    source point writes a displaced fringe pattern; smearing over a source of angular
    size $\theta_s$ gives $V = |\mathrm{sinc}|$-type falloff with first zero at
    $d \approx \lambda/\theta_s$ (the van Cittert–Zernike *idea*, kept at this level;
    the theorem proper is `41-imaging-coherence`'s) → Michelson's stellar
    interferometer: Betelgeuse 1920, $\theta \approx 0.047''$, first null near a 3 m
    baseline (uniform-disk $1.22\lambda/\theta$), measured on the 100-inch telescope's
    6 m outrigger.
  - *verify:* $\gamma(0) = 1$; `degree_of_coherence` of a Lorentzian $S$ overlays
    $e^{-|\tau|/\tau_c}$ (limits test in view); ensemble check: $M$ seeded
    `partial_coherence_source` realisations → measured $V$ vs analytic $|\gamma|$
    within $1/\sqrt{M}$ (`numerical-observation`); the sodium revival period from 25
    reproduced by a doublet spectrum; $\tau_c\,\Delta\omega$ of order 1 across preset
    shapes.
  - *transfer:* `25-michelson` backward (the envelope and the revival, now theorems);
    `41-imaging-coherence` (vCZ in full; coherent vs incoherent imaging);
    `45-lasers` (why laser light is different — the violinists' $N$ vs $N^2$ closed
    with vocabulary); `52-quantum-optics` (from $\gamma$ to $g^{(2)}$, Hanbury
    Brown–Twiss); radio astronomy and VLBI — interferometry across continents because
    correlation, not light, is transported; `22-stokes-poincare` (partial polarization
    is partial coherence between components — one-sentence bridge).
  - *quiz:* visibility numeric from a trace; lineshape-matching MC; coherence-length
    ranking MC (registry distractor); stellar-baseline numeric; washout-cause MC
    (spatial vs temporal — diagnose which killed the fringes).
  - *explain:* why "is this light coherent?" is a malformed question and what to ask
    instead; how a fringe visibility curve can *be* a spectrometer; why a pinhole
    rescued Young's sunlight but a filter would have helped too (the two coherences
    separated in words).
  - *advanced:* the analytic signal as the honest home of $\hat{E}(t)$ (00 → 04 thread
    closed for fields); Hanbury Brown–Twiss: intensity correlations survive where phase
    is scrambled — $g^{(2)}(\tau)$ teaser, door to `52-quantum-optics`; why two
    *independent* lasers can show transient fringes (fast detectors, finite $\tau_c$) —
    the resolution of 23's "independent lasers" prediction, with the ensemble average
    restored.
- **Core derivations:** as in the seeds; the Wiener–Khinchin box carries the
  stationarity assumption explicitly ($\langle\hat{E}^*(t)\hat{E}(t+\tau)\rangle$
  independent of $t$ — `model-assumption` feeding a `theorem`); the practical chain
  $\Delta\lambda \to \Delta\omega = 2\pi c\Delta\lambda/\lambda^2 \to \tau_c \to \ell_c$
  worked once with real numbers (LED: $\Delta\lambda = 30$ nm at 620 nm →
  $\ell_c \approx 13$ µm).
- **Model specification draft:** System — a stationary quasi-monochromatic scalar field
  described by its spectral density $S(\omega)$ or an ensemble of realisations;
  observables are visibilities and correlation functions. Dynamics — none beyond the
  statistical model (phase drift/diffusion in the synthetic source). Boundary — none;
  sources idealised as point (temporal part) or incoherently extended (spatial part).
  Ensemble — central: all coherence quantities are ensemble/time averages; seeded
  generators for realisations. Ignored — polarization (scalar), quantum statistics,
  non-stationary sources. Valid when — averaging time ≫ $\tau_c$; bandwidth ≪ centre
  frequency; source points mutually incoherent (spatial part). Failure modes — reading
  one realisation as the average; conflating spatial and temporal washout; applying
  $V = |\gamma|$ to unequal beams; trusting $\ell_c = \lambda^2/\Delta\lambda$ beyond
  order of magnitude for structured spectra (the doublet's revivals are the
  counterexample in view).
- **Epistemic classification:** Wiener–Khinchin — `theorem` (the part's crowning box);
  stationarity — `model-assumption`; $\tau_c \approx 1/\Delta\omega$ —
  `approximation` (order-of-magnitude, exact constants shape-dependent); ensemble
  visibility agreement — `numerical-observation`; source coherence-length table —
  `empirical-law` (measured, order-of-magnitude); "do two independent lasers
  interfere?" — resolved in advanced, with an `open-question` pointer to quantum
  descriptions (`52-quantum-optics`).
- **Misconceptions:** NEW **`coherence-is-binary`** — "Light is either coherent or
  incoherent; there is nothing in between." Falsifying experiment: the lab measures
  $V(\tau)$ decaying *continuously* from 1 to 0 as delay grows, for every source
  preset; the bandwidth slider interpolates smoothly between "laser-like" and
  "lamp-like" with no threshold anywhere. Distractor: quiz option "fringes vanish
  abruptly once the path difference exceeds one wavelength".
- **Glossary terms:** `coherence` (קוהרנטיות), `temporal-coherence` (קוהרנטיות
  זמנית), `spatial-coherence` (קוהרנטיות מרחבית), `coherence-time` (זמן קוהרנטיות),
  `coherence-length` (אורך קוהרנטיות), `degree-of-coherence` (דרגת קוהרנטיות),
  `fringe-visibility` (נראות פסים; `he_reject` candidate: חדות פסים),
  `wiener-khinchin-theorem` (משפט וינר–חינצ'ין), `extended-source` (מקור מורחב),
  `stellar-interferometry` (אינטרפרומטריה כוכבית).
- **Interactive controls and simulations:** the coherence explorer and spatial panel
  (see *explore*); **source gallery** — the honest table as an interactive: sunlight
  ($\ell_c \sim 1$ µm), white LED ($\sim 10$ µm), sodium lamp (doublet-limited
  $\sim 0.3$ mm revival structure; single Doppler-broadened line $\sim$ cm), multimode
  HeNe ($\sim 20$ cm), stabilised single-mode HeNe ($\sim 10^2$–$10^3$ m) — each row
  clickable, loading its spectrum into the explorer (numbers presented as
  order-of-magnitude, `empirical-law` box).
- **Virtual lab outline** (`notebooks/en/labs/27-coherence.ipynb`): (1) explorer play,
  lineshape ↔ decay matching; (2) *measurement* (the brief's centrepiece): generate
  partially coherent light with `partial_coherence_source` (random-phase-drift model —
  phase diffusion yielding a Lorentzian line; built on the ensemble machinery
  precedent of `phasors.random_phasor_sum`), run it through a simulated Michelson,
  measure $V$ vs delay across seeds, fit the exponential decay → $\tau_c \pm \sigma$;
  (3) cross-check: `fourier.spectrum` of the same field → $\Delta\nu$ → verify
  $\tau_c\,\Delta\omega \sim 1$; (4) spatial: double slit with an extended source,
  sweep $d$, find the visibility null, "measure" a synthetic star's angular diameter
  ± uncertainty (Michelson-1920 re-enacted); (5) the source gallery quantified: rank
  the presets by measured $\ell_c$, compare with the table.
- **Real-experiment counterpart:** double slit illuminated by a laser pointer vs an
  LED behind an adjustable foil pinhole: photograph both, import intensity rows,
  compare visibilities — the pinhole-size sweep is a real spatial-coherence
  measurement with household parts.
- **Media assets** (`render_interference.py`): (i) spectrum narrowing while
  $|\gamma(\tau)|$ stretches — the transform pair as a see-saw; (j) extended-source
  washout: fringe patterns from displaced source points stacking until the pattern
  greys out.
- **Quiz bank outline:** `Q-27-1` numeric — $V$ from $I_{\max}, I_{\min}$ (OBJ-27-1);
  `Q-27-2` MC — lineshape ↔ decay matching (OBJ-27-4); `Q-27-3` numeric — $\ell_c$
  from $\Delta\lambda$ for an LED (OBJ-27-3); `Q-27-4` MC — gradual vs abrupt
  visibility loss (OBJ-27-2, distractor `coherence-is-binary`); `Q-27-5` numeric —
  baseline for a stellar null given $\theta$ (OBJ-27-5); `Q-27-6` MC — source ranking
  by $\ell_c$ (OBJ-27-6); `Q-27-7` free — spatial vs temporal coherence: which
  experiment separates them (OBJ-27-2, OBJ-27-5).
- **Problem set outline:** analytical — $|\gamma|$ of a doublet (beats; recover 25's
  revival period); $|\gamma|$ of a top-hat spectrum (sinc — pair zoo); unequal-beam
  visibility formula. Computational — coherence of filtered white light vs filter
  width (design "how good a filter buys how many fringes"); phase-diffusion rate ↔
  measured linewidth study across seeds. Challenge — implement a two-point stellar
  interferometer simulation over a binary star: recover both separation and diameter
  from the visibility curve.
- **Runtime budget:** ensembles $M \le 64$ of $2^{14}$-sample fields with one FFT
  each — a few seconds in Pyodide, the part's heaviest cell; spatial panel analytic;
  everything else trivial.
- **Validation gates:** standard set with `--module 27-coherence`; plus the
  $\gamma(0) = 1$, Lorentzian↔exponential, and seeded-visibility tests of §4.
- **Open questions for the author:** whether Wiener–Khinchin's proof sketch lives in
  core derive or advanced (recommendation: core — it is three lines given 04, and it
  is the part's summit); whether the source table cites lab-condition caveats per row
  (recommendation: one shared footnote — the numbers are order-of-magnitude by design);
  whether HBT stays a teaser or gets a mini-simulation (recommendation: teaser only —
  `52-quantum-optics` owns it).

## 6. Part-level assessment and capstone hooks

- **Capstones fed:** §35.2 (virtual optical bench) consumes 25's bench pattern and the
  part's instrument culture wholesale; §35.3 (grating spectrometer) consumes resolving
  power and instrument-design reasoning from 26 (and inherits 27's linewidth
  vocabulary for what "resolved" means); §35.1 (computational telescope) consumes 27's
  spatial coherence via `41-imaging-coherence`; §35.4 (optical communication) consumes
  laser linewidth/coherence framing from 26–27.
- **Cross-module synthesis problems** (live with the part, not one module):
  (a) *characterise then resolve:* use the 25 FTIR bench to discover a source is a
  doublet, then design a 26 cavity to resolve it directly — one instrument hands off
  to the other; (b) *coat the interferometer:* apply 24's AR design to the Michelson's
  beam-splitter back face and compute the ghost-fringe suppression — 24 inside 25;
  (c) *the energy audit, part-wide:* verify no instrument in the family creates or
  destroys energy — screen integral (23), $R + T$ (24), the Michelson's second output
  port (25), $T + R_{\text{cav}}$ (26).
- **Exam themes:** $\pi$-shift bookkeeping under time pressure; instrument choice
  ("you must measure X — which bench and why"); order-of-magnitude coherence estimates
  from spectra; Airy/finesse numerics; visibility as data (read $V$, infer source).

## 7. Build order and validation gates

Build order `23 → 24 → 25 → 26 → 27`, teaching order and dependency order aligned: 23
is the grammar (and must exist before any $\gamma$ slider appears elsewhere); 24 needs
only 23 plus `18-fresnel`, and its geometric series is 26's warm-up; 25 needs 23 and
sets up the coherence-length data 27 explains; 26 needs 24's series and part-01's
Lorentzian/$Q$ kit; 27 closes the part and back-references 23's slider and 25's
envelopes, so it lands last.

With `23-interference`: create `content/en/interference/`, land `interference.py` with
its file-level model spec and the 23-scope functions plus their §4 tests (conservation
of screen energy, fringe-spacing scaling); apply the README conflict-log re-pointing
`interference-destroys-energy` → `23-interference` (one-line `assigned_module` edit,
status → `addressed` when the quiz distractor exists); deposit 23's glossary terms.
Each subsequent module lands its own functions + tests + glossary rows, and its NEW
registry entry alongside its falsifier: `film-color-is-pigment` (24),
`laser-needed-for-interference` (25), `two-mirrors-block-light` (26),
`coherence-is-binary` (27). The CIE package data ships with 24. The 00-phasors prose
drift ("module 8" → `23-interference` / `27-coherence`, per README conflict log)
becomes fixable when 23 and 27 exist — apply with 27.

Per module: the standard four gates (README). Additionally: `interference.py` tests
must land *with* their modules, since `29-fraunhofer`'s plan will cite the
`young_pattern` energy guarantee and `44-resonators` will cite the Airy limits.

## 8. Deviations from the master plan

- **Merge (8.1 + 8.2 → `23-interference`):** the two-beam law *is* Young's screen read
  pointwise; splitting them re-teaches one formula. Precedent: `02-damped-driven`
  ← 1.2 + 1.3. Canonical per README module map.
- **Finite-slit-width split:** master plan 9.4 (double slit with finite width) and any
  diffraction envelope are **deferred to `30-apertures`** — 23 models slits as ideal
  point/line sources, states the Fraunhofer-like small-angle assumptions explicitly,
  and links forward. Rationale: the envelope needs the single-slit transform (Part IX);
  teaching it here would smuggle in diffraction without its machinery.
- **Coherence woven, not appended:** the master plan confines coherence to 8.6; this
  plan threads a visibility slider from 23 and stages coherence phenomena in 24–26
  before 27 formalises them. Rationale: four encounters as fact make one encounter as
  definition stick.
- **Additions beyond the master plan:** the CIE colour pipeline with shipped
  colour-matching data (8.3 says only "perceived color"); compensator, FTIR, and the
  LIGO research box in 25; Lorentzian lineshape, photon lifetime, ringdown, and $Q$ in
  26; Wiener–Khinchin as a proved-and-measured theorem, the stellar interferometer,
  and the honest source table in 27; four NEW registry misconceptions plus the claimed
  re-pointing of `interference-destroys-energy`.
- **Terminology:** "visibility" is used phenomenologically from 23 and defined formally
  in 27 (glossary key `fringe-visibility` deposits with 27); "finesse" vs "coefficient
  of finesse" kept rigorously distinct in 26 (`finesse` vs `airy_coefficient`) because
  conflating $\mathcal{F}$ and $F$ is a standing student trap.
- **Convention note:** all seeded formulas carry the course phase convention
  ($e^{\ii(kx-\omega t)}$, $e^{-\ii\omega t}$, $n + \ii\kappa$; Wiener–Khinchin with
  $e^{-\ii\omega\tau}$, matching `fourier.spectrum`'s forward sign) — where Hecht's
  $e^{\ii(\omega t - kx)}$ pages are companion reading, the conventions page is the
  arbiter, as everywhere in the course.
