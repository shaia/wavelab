# Part 4 — Standing Waves, Fourier Modes, and Dispersion — Implementation Plan

> **Master plan:** §11 (Part IV). **Modules:** `11-standing-waves`, `12-wave-packets`, `13-dispersion`. **Status:** planned.
> Canonical numbering, invariants, and conflict log: [README.md](README.md).

## 1. Part overview and narrative arc

Parts 0–III built three machines separately: a language for signals (phasors, Fourier series, the
transform and its pair zoo), a theory of oscillators with normal coordinates, and a wave equation
with travelling solutions, energy bookkeeping, and impedance. Part IV bolts them together —
**Fourier analysis stops being a description of signals and becomes the physics of how waves
actually move** — and after it the course can do optics, because every optics idea to come
(coherence, diffraction, fibers, resonators) is a wave whose spectral components are tracked
separately.

The arc runs from confinement to freedom. Module 11 confines the wave: boundary conditions turn the
continuum of travelling waves into a discrete ladder of standing modes, and the same standing wave
is derived twice — as two module-08 travelling waves superposed phasor-by-phasor at every point, and
as an eigenvalue problem where the boundaries quantize $k$ — with the two pictures reconciled
explicitly. A plucked string then makes module 03's payoff physical: decomposing the initial shape
into modes *is* a Fourier series on the $\sin(k_n x)$ basis, and each mode evolves as an independent
module-01 oscillator — part II's normal-coordinate lesson made continuous. Module 12 releases the
wave into an infinite medium and asks the part's sharpest question: when a packet of many
wavenumbers travels, *what* travels? The carrier moves at $v_p = \omega/k$, the envelope — which
carries energy and information — at $v_g = d\omega/dk$, and in a dispersive medium the two visibly
separate. Module 13 makes the dispersion relation itself the object of study: a museum of
$\omega(k)$ families, the analytic Gaussian-spreading law as the bandwidth theorem's dynamical
payoff, and a general FFT propagator evolving *any* packet under *any* $\omega(k)$.

Two enhancements run through the part: **musical acoustics as the laboratory** (pluck position
selecting harmonics, touch-harmonics, struck vs plucked strings — physics a guitarist already
knows, now derived) and **the spectral propagator as an instrument** — FFT → phase factor
$e^{-\ii\omega(k)t}$ → inverse FFT, introduced as *the* way linear waves are evolved and returning
as the angular-spectrum method (part IX), fiber propagation (47), and the 4-f processor (part XI).
The part also settles an energy account opened in module 09: a standing wave carries no net energy
flux, and a spreading pulse loses no energy at all, only rearranges its phases — theorems here,
measurements in the labs.

## 2. Position in the course

- **Requires:**
  - `11-standing-waves`: `08-wave-equation` ($f(x \mp vt)$, $v=\sqrt{T/\mu}$, linearity);
    `00-phasors` (pointwise phasor addition); `03-fourier-series` (coefficients by orthogonality,
    smoothness ↔ decay, Gibbs); `07-normal-modes` (normal coordinates; the chain's $N \to \infty$
    limit); `01-sho` (mode time dependence); `09-wave-energy` (energy density and flux evaluators).
  - `12-wave-packets`: `00-phasors` (beats identity with $kx-\omega t$ phases);
    `04-fourier-transform` ($A(k)$ superposition; `rms_widths`); `08-wave-equation`;
    `11-standing-waves` (contrast: confined modes vs free packets).
  - `13-dispersion`: `12-wave-packets` ($v_g$); `04-fourier-transform` (bandwidth theorem, Gaussian
    pair, FFT bridge); `07-normal-modes` (`coupled.chain_dispersion`).
- **Feeds:** `14-em-waves` (vacuum as the nondispersive case); `16-light-in-matter` (13's Lorentz
  sketch derived honestly); `27-coherence` (packet duration ↔ coherence time); `43-gaussian-beams`
  ($\sigma(t)$ is mathematically the Rayleigh-range law, $x \to z$); `46-waveguides` (the
  plasma-form $\omega^2 = \omega_c^2 + c^2k^2$ of 12's superluminal example); `47-fibers` (GVD
  pulse spreading; `propagate_dispersive` reused as-is).
- **Explicitly not assumed:** anything electromagnetic (media stay strings, water, abstract
  $\omega(k)$); absorption or complex $k$ (all $\omega$ real; evanescence waits for 19); 2-D/3-D
  waves; quantum mechanics (advanced aside only); nonlinearity (soliton trailer to 51).

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|
| `11-standing-waves` | `content/en/fourier-waves/11-standing-waves.md` | Standing waves: boundaries quantize | 4.1 + 4.2 | French, vibrating string & normal modes; Georgi, boundary conditions & Fourier on a string | planned |
| `12-wave-packets` | `content/en/fourier-waves/12-wave-packets.md` | Wave packets: phase and group velocity | 4.3 | Georgi, group velocity; MIT 8.03 dispersion lectures | planned |
| `13-dispersion` | `content/en/fourier-waves/13-dispersion.md` | Dispersion: how media sort waves | 4.4 | Georgi, dispersion; Hecht, dispersion in matter (preview only) | planned |

## 4. Shared infrastructure for this part

**`src/wavelab` — existing used:** `phasors.superpose` / `resultant` (11's pointwise picture);
`oscillators.position` / `energies` (each mode a module-01 oscillator); `fourier.spectrum` /
`inverse_spectrum`, `gaussian_pulse` / `gaussian_spectrum`, `rms_widths`; `measurement.add_noise` /
`fit_cosine`; `validation.seed_study` / `scaling_exponent` / `convergence_study`. From part-03's
`waves.py` core: the string FDTD solver, d'Alembert evaluator, and energy density / flux evaluators
(names per part-03 §4) — consumed, never re-specified here.

**`src/wavelab` — new: extension of `waves.py`** (README ownership: *introduced by* part-03,
*extended by* part-04). The single-owner split, stated explicitly: **part-03 owns** the file-level
docstring model spec, the string FDTD solver, d'Alembert solutions, energy densities and flux,
impedance/junction coefficients, and boundary handling. **This plan owns exactly**: standing-wave
mode functions and modal decomposition, packet construction, the dispersion-relation families, the
spectral propagator, group/phase velocity evaluators, and the envelope/centroid trackers. No
docstring is written here; part-04's functions conform to part-03's model spec and
`constants.SIGN_CONVENTION`.

Function-level sketch (signatures + contracts):

```python
mode_wavenumbers(n_modes, length, boundary) -> k      # k_n: "fixed-fixed" n pi/L, "fixed-free" (n-1/2) pi/L,
                                                      #   "free-free" n pi/L incl. n=0
mode_shape(x, n, length, boundary) -> phi             # normalized eigenfunction (sin/cos per boundary)
modal_decompose(psi0, x, length, n_modes, boundary) -> a   # inner products against mode_shape
modal_synthesize(a, x, t, length, v, boundary) -> psi # sum a_n phi_n(x) cos(omega_n t), omega_n = v k_n (pluck release)
modal_energies(a, k, v, mu) -> E_n                    # per-mode energy; each constant in time
pluck_shape(x, length, pluck_point, height) -> psi0   # triangular pluck; closed-form a_n are the test reference
gaussian_packet(x, k0, sigma, x0=0.0) -> psi          # complex e^{i k0 x} carrier under a Gaussian envelope
phase_velocity(omega_of_k, k) -> v_p                  # omega(k)/k
group_velocity(omega_of_k, k, dk=1e-4) -> v_g         # central-difference d omega/dk, O(dk^2) accurate
omega_nondispersive(k, v) -> omega                    # v |k|
omega_lattice(k, omega_max, a) -> omega               # thin wrapper citing coupled.chain_dispersion (part-02)
omega_deep_water(k, g=9.81) -> omega                  # sqrt(g |k|); v_g = v_p / 2 exactly
omega_material_sketch(k, omega0, omega_p) -> omega    # lossless Lorentz-oscillator sketch; TRAILER for 16
propagate_dispersive(psi0, dx, omega_of_k, t) -> psi  # fourier.spectrum -> e^{-i omega(k) t} ->
                                                      #   fourier.inverse_spectrum; sign bookkeeping internal
envelope(psi, dx) -> env                              # |analytic signal| (module-00/04 thread); |psi| if complex
envelope_centroid(x, psi) -> x_c                      # intensity-weighted mean position
envelope_rms_width(x, psi) -> sigma                   # RMS width of |psi|^2, the sigma(t) observable
track_envelope(psi0, dx, omega_of_k, times) -> (x_c, sigma)  # propagate + centroid + width per time
spreading_time(sigma0, omega_of_k, k0) -> tau         # 2 sigma0^2 / |omega''(k0)|, numerical second derivative
```

Sign contract for `propagate_dispersive`: the course expands fields in $e^{+\ii kx}$ while
`fourier.spectrum` applies the forward $e^{-\ii(\cdot)}$ sign; the propagator internalizes the
resulting $k \to -k$ flip so positive-$k$ content moves toward $+x$ (a test pins this).
`omega_of_k` is evaluated on signed $k$ and must be even; no symmetrizing is done.

**`tests/physics/` additions:**

- *conservation:* `modal_energies` each constant under `modal_synthesize`, their sum matching
  part-03's integrated energy density; norm $\int|\psi|^2 dx$ and $|A(k)|$ conserved under
  `propagate_dispersive` (Parseval + unimodular phase).
- *limits:* nondispersive propagation = rigid translation by $vt$, matching part-03's d'Alembert
  evaluator to $<10^{-10}$; `omega_lattice` → $vk$, $v = \omega_{\max}a/2$, as $ka \to 0$;
  deep-water `group_velocity` = `phase_velocity`/2; a two-mode standing wave equals two
  counter-propagating d'Alembert waves.
- *convergence:* modal truncation $L^2$ error of `pluck_shape` $\propto N^{-3/2}$ (corner → $1/n^2$
  coefficients, part-00's smoothness ladder); `group_velocity` error $\propto dk^2$.
- *scaling:* fitted $\sigma(t)$ of a propagated `gaussian_packet` under quadratic dispersion
  matches $\sigma_0\sqrt{1+(t/\tau)^2}$ with $\tau$ from `spreading_time`; late-time exponent
  $\to 1$ via `validation.scaling_exponent`.
- *seeds:* centroid-fit $v_g$ across seeded noisy realisations — mean within uncertainty of
  `group_velocity`, error $\propto 1/\sqrt{M}$.
- *dimensions:* all `omega_*` return rad/s for $k$ in rad/m against the `units` registry.

**Shared media:** one script `media/render/render_fourier_waves.py` renders all three modules' MP4s
(shot lists in §5). **Glossary themes:** standing-wave and musical vocabulary (11), packet
kinematics (12), dispersion (13).

## 5. Module specifications

### 5.1 `11-standing-waves` — Standing waves: boundaries quantize

- **Identity and scope:** master-plan notebooks 4.1 + 4.2 merged (§8). Confined 1-D waves only;
  stiff-string dispersion deferred to 13's problem set, driven string resonance to 26.
- **Prerequisites:** §2 list; load-bearing: 08's travelling solutions, 03's orthogonality and decay
  rates, 07's normal coordinates, 09's flux.
- **Learning objectives:**
  - `OBJ-11-1` — Derive the standing wave 2A sin(kx) sin(omega t) as the superposition of two
    counter-propagating travelling waves and read nodes and antinodes off the pointwise phasor sum.
  - `OBJ-11-2` — Impose fixed-fixed, fixed-free, and free-free boundary conditions and derive the
    allowed wavenumbers (k_n = n pi/L; (n - 1/2) pi/L; n pi/L) and mode shapes, explaining why
    boundaries make the spectrum discrete.
  - `OBJ-11-3` — Decompose an arbitrary initial shape into modes via a_n = <psi0, phi_n> and
    predict from the pluck position which harmonics are loud and which are absent.
  - `OBJ-11-4` — Evolve psi(x,t) = sum a_n phi_n(x) cos(omega_n t) and explain why each mode is an
    independent harmonic oscillator.
  - `OBJ-11-5` — Show that a standing wave's time-averaged energy flux is zero while energy
    oscillates between kinetic and potential within quarter-wavelength cells.
- **Mathematical background:** has — coefficients, orthogonality, 07's eigenvalue language;
  introduced — eigenfunctions of a continuous operator with boundary conditions.
- **Physical intuition goals:** (1) confinement ⇒ discreteness — the boundaries, not the string,
  know about integers; (2) pluck position is a graphic equalizer: a harmonic with a node at the
  pluck point is silent; (3) a standing wave is two travelling waves going nowhere together;
  (4) the flat instant is maximum motion, not zero energy.
- **Section skeleton seeds:**
  - *puzzle:* a guitar string can be bent into infinitely many shapes yet only sounds notes from
    one discrete series; touched at the midpoint, the note jumps an octave. Boxed: **who told the
    string about integers?**
  - *predict:* (1) pluck exactly at the midpoint — is the octave present? (2) two identical
    counter-propagating waves — does their sum travel? carry energy? (3) where do you pluck for the
    mellowest tone? (4) the string passes through flat — where is the energy? (targets
    `flat-string-no-energy`).
  - *explore:* boundary selector; mode slider $n \le 12$ with node markers; sum-view toggle (the
    two counter-propagating half-waves behind the standing wave); pluck-point slider with live
    modal bar chart $|a_n|$; per-mode audio toggle.
  - *derive:* superposition picture → eigenvalue picture → boxed reconciliation → decomposition →
    energy (route below).
  - *verify:* modal reconstruction vs part-03 FDTD; truncation error $\propto N^{-3/2}$
    (`numerical-observation`); modal energies constant; mean flux $\approx 0$ everywhere.
  - *transfer:* 07 backward (chain modes → string modes); 26 (cavity modes); 44 (laser
    resonators); guitar vs piano (pluck vs strike); microwave-oven hot spots as 3-D nodes.
  - *quiz:* counter-propagating picture; mode counting per boundary; pluck-position harmonic
    content; flat-instant energy.
  - *explain:* why discrete frequencies at all; why the midpoint touch makes an octave; where a
    standing wave's energy lives over one cycle.
  - *advanced:* the free-free $n=0$ translation mode; struck strings (velocity initial data,
    $\sin\omega_n t$ factors); Gibbs at the pluck corner as 03's phenomenon moved to space.
- **Core derivations:** (1) superposition:
  $\Real[A e^{\ii(kx-\omega t)}] - \Real[A e^{\ii(-kx-\omega t)}] = 2A\sin(kx)\sin(\omega t)$ — at
  each $x$ the two phasors add with relative phase $2kx$, giving the *standing* resultant
  $2A|\sin kx|$ (module-00 arithmetic at every point). (2) eigenvalue picture: separable solutions
  $\phi(x)\cos(\omega t)$ with $\phi(0)=\phi(L)=0$ force $\phi_n = \sin(k_n x)$, $k_n = n\pi/L$,
  $\omega_n = v k_n$; fixed-free and free-free by the same three lines. Reconciliation: each
  eigenmode *is* the two-wave superposition, the boundary supplying the reflected partner
  (part-03's $r=-1$ hard end). (3) decomposition:
  $a_n = \tfrac{2}{L}\int_0^L \psi_0(x)\sin(k_n x)\,dx$ — module 03's formula with $x$ for $t$; the
  triangular pluck at $x_p$ gives $a_n \propto \sin(n\pi x_p/L)/n^2$, so a node at the pluck point
  silences that harmonic. (4) evolution: $\ddot{a}_n = -\omega_n^2 a_n$ — part II's normal
  coordinates, now infinitely many. (5) energy: flux
  $P = -T\,\partial_x\psi\,\partial_t\psi \propto \sin(2kx)\sin(2\omega t)$ — zero on time average
  everywhere, identically zero at nodes: no net transport.
- **Model specification draft:** System — a uniform string of length $L$ on the eigenbasis of the
  chosen boundary conditions. Dynamics — the part-03 wave equation; in modal coordinates,
  independent module-01 oscillators. Boundary — fixed-fixed / fixed-free / free-free ends select
  the basis. Ensemble — deterministic; lab noise seeded. Ignored — stiffness, damping, nonlinearity
  of large plucks. Valid when — small displacements; initial data smooth enough for the truncated
  sum. Failure modes — truncation ringing at the pluck corner; one boundary's basis used for
  another; inharmonicity read as error.
- **Epistemic classification:** quantization by boundary conditions — `theorem`; equivalence of the
  two pictures — `theorem` (boxed); basis completeness — `theorem` (stated); zero mean flux —
  `theorem`, its check a `numerical-observation`; ideal flexible string — `model-assumption`;
  measured truncation rate — `numerical-observation`.
- **Misconceptions:** NEW `pluck-single-frequency` — "A plucked string vibrates at one frequency,
  its fundamental." Falsifier: FFT of a simulated (and recorded) pluck shows a harmonic comb whose
  weights move with pluck position. Distractor: "the motion is a sine at $f_1$". NEW
  `flat-string-no-energy` — "When the vibrating string passes through flat, its energy has
  momentarily vanished." Falsifier: part-03 energy densities at the flat instant — all kinetic,
  velocity field maximal. Distractor: "energy is zero twice per period".
- **Glossary terms:** `standing-wave` (גל עומד), `node` (צומת), `antinode` (בטן),
  `boundary-condition` (תנאי שפה), `overtone` (צליל עילי; `he_reject` candidate: אוברטון).
- **Interactive controls and simulations:** as in *explore*, plus a strike-vs-pluck toggle (initial
  velocity vs initial displacement) previewing the advanced section.
- **Virtual lab outline** (`notebooks/en/labs/11-standing-waves.ipynb`): (1) sum-view sandbox;
  (2) decompose plucks at several $x_p$, bar-chart $|a_n|$ vs closed form; (3) evolve with
  `modal_synthesize` vs part-03 FDTD, overlay; (4) FFT one point's motion → harmonic comb;
  (5) time-average part-03's flux at several stations → 0; (6) *measurement:* from noisy mode
  frequencies $f_n$ vs $n$, fit the wave speed $v \pm \sigma_v$, check $v = \sqrt{T/\mu}$.
- **Real-experiment counterpart:** guitar or rubber band + phone spectrogram: pluck at several
  positions, compare harmonic heights; touch-harmonic at the midpoint. WAV import as in 03.
- **Media assets** (`render_fourier_waves.py`): (a) two counter-propagating waves cross-fading into
  their standing sum, node markers appearing; (b) pluck decomposition: triangle morphing as modal
  bars accumulate, then modes evolving independently and re-summing.
- **Quiz bank outline:** `Q-11-1` MC counter-propagating sum (OBJ-11-1); `Q-11-2` numeric
  fixed-free mode frequency (OBJ-11-2); `Q-11-3` MC pluck position → harmonic content (OBJ-11-3,
  distractor `pluck-single-frequency`); `Q-11-4` numeric modal evolution at time $t$ (OBJ-11-4);
  `Q-11-5` MC flat-instant energy (OBJ-11-5, distractor `flat-string-no-energy`); `Q-11-6` free —
  why discrete frequencies (OBJ-11-2).
- **Problem set outline:** analytical — fixed-free ladder and the clarinet's missing even
  harmonics; derive the pluck $a_n$; Parseval → total pluck energy from `modal_energies`.
  Computational — design a pluck silencing the 7th harmonic; spectrogram with per-mode damping
  $\propto n^2$. Challenge — struck vs plucked: piano vs guitar spectra.
- **Runtime budget:** modal sums ≤ 64 modes on ≤ 2048-point grids; FDTD reuses part-03's budgeted
  solver; FFTs ≤ $2^{12}$. Sub-second in Pyodide.
- **Validation gates:** standard set (README) with `--module 11-standing-waves`.
- **Open questions for the author:** does free-free (needs a rod or air column as prop) stay in
  core or move to advanced; is per-mode audio worth the JupyterLite audio dependency (same question
  as module 03 — decide once).

### 5.2 `12-wave-packets` — Wave packets: phase and group velocity

- **Identity and scope:** master-plan notebook 4.3. Kinematics of narrowband packets in a given
  $\omega(k)$; the systematic $\omega(k)$ study and spreading are 13's. Superluminal $v_p$ appears
  as an open-question admonition only.
- **Prerequisites:** §2 list; load-bearing: 00's beats identity, 04's transform pair and
  `rms_widths`, 08's travelling waves.
- **Learning objectives:**
  - `OBJ-12-1` — Compute v_p = omega/k and v_g = d omega/dk for a given omega(k) and state which
    observable each velocity describes.
  - `OBJ-12-2` — Derive the two-wavenumber beat in space: superposing k0 +/- dk gives a carrier at
    (k0, omega0) under an envelope moving at d omega/d k.
  - `OBJ-12-3` — Construct a narrowband packet as a superposition of e^(i(kx - omega(k) t))
    components and show via omega(k) ~ omega0 + v_g (k - k0) that the envelope translates rigidly
    at v_g.
  - `OBJ-12-4` — Extract v_g from a noisy simulation by fitting the envelope centroid versus time,
    reporting value and uncertainty.
  - `OBJ-12-5` — Explain why a phase velocity above c does not violate relativity, and identify
    which velocity carries information.
- **Mathematical background:** has — beats, transform pairs, Taylor expansion; introduced —
  stationary-phase reasoning at picture level (honest asymptotics is a challenge problem).
- **Physical intuition goals:** (1) in a pond ring, crests are born at the rear, march through the
  group, and die at the front — the crest is not the wave; (2) the envelope is what energy and
  messages ride on; (3) narrower bandwidth ⇒ the envelope survives longer; (4) a marked crest
  cannot carry a mark: marking it *is* modulation, which moves at $v_g$.
- **Section skeleton seeds:**
  - *puzzle:* film a stone dropped in a pond in slow motion: individual crests overtake the ring
    and vanish at its leading edge while the ring lags. Boxed: **when a "wave" travels, what
    exactly is doing the travelling — and how fast?**
  - *predict:* (1) do the pond crests move faster, slower, or with the ring? (2) where $v_p > c$,
    can a message beat light? (targets `packet-at-phase-velocity`) (3) superpose $k_0 \pm \Delta k$:
    how fast does the envelope move? (4) halve a packet's bandwidth — does its envelope hold
    together longer or shorter?
  - *explore:* $\omega(k)$ family selector (the four §4 families); $k_0$, $\sigma$ sliders; a dot
    riveted to one carrier crest and a dot on the envelope centroid, each with a trail; live $v_p$,
    $v_g$ readouts with the chord-and-tangent construction on the curve.
  - *derive:* beats-in-space → general packet → Taylor argument (route below).
  - *verify:* crest-dot speed matches $\omega_0/k_0$, centroid speed matches $d\omega/dk$
    (`numerical-observation`); deep-water ratio $v_g/v_p = 0.500$ measured; nondispersive case: the
    dots never separate.
  - *transfer:* 13 (what the neglected quadratic term does); 27 (duration ↔ coherence time); 46
    (plasma-form $\omega(k)$ returns as waveguide dispersion); quantum matter waves (advanced
    aside); 47 (information rate vs dispersion).
  - *quiz:* $v_p$/$v_g$ computation; beat envelope speed; which velocity for energy and
    information; deep-water crest kinematics.
  - *explain:* narrate the pond-ring movie; why "the wave's speed" is two questions; why deep-water
    crests die at the front.
  - *advanced:* $\omega^2 = \omega_p^2 + c^2k^2$ (plasma / waveguide-to-be): $v_p v_g = c^2$, so
    $v_p > c$ always — with the open-question box on fronts and precursors; the free-particle
    Schrödinger packet as the same mathematics.
- **Core derivations:** (1) two-wavenumber beat (module 00's identity with $kx-\omega t$ phases):
  $\cos[(k_0{+}\Delta k)x - (\omega_0{+}\Delta\omega)t] +
  \cos[(k_0{-}\Delta k)x - (\omega_0{-}\Delta\omega)t] =
  2\cos(\Delta k\,x - \Delta\omega\,t)\cos(k_0 x - \omega_0 t)$ — carrier at $\omega_0/k_0$,
  envelope at $\Delta\omega/\Delta k \to d\omega/dk$. (2) general packet
  $\psi(x,t) = \tfrac{1}{2\pi}\int A(k)\,e^{\ii(kx - \omega(k)t)}\,dk$, $A(k)$ narrow about $k_0$;
  inserting $\omega(k) \approx \omega_0 + v_g(k-k_0)$ gives
  $\psi = e^{\ii(k_0x-\omega_0 t)}\,F(x - v_g t)$ — carrier at $v_p$ under a rigidly translating
  envelope; the dropped $\tfrac12\omega''(k-k_0)^2\,t$ term is 13's subject (`approximation` box:
  valid for $t \ll \tau$). (3) deep water: $\omega = \sqrt{g|k|}$ gives
  $v_g = \tfrac12\sqrt{g/k} = v_p/2$ — crests move at twice the group speed: born at the rear, die
  at the front.
- **Model specification draft:** System — a narrowband packet, envelope × carrier, in an infinite
  1-D medium with given real $\omega(k)$. Dynamics — each spectral component advances its phase at
  its own $\omega(k)$; linear, unitary. Boundary — infinite domain; numerically periodic (FFT
  wrap), window kept large. Ensemble — deterministic; seeded noise in measurement cells. Ignored —
  absorption, nonlinearity, reflections. Valid when — $\Delta k \ll k_0$ and $t \ll \tau$. Failure
  modes — broadband packets have no single $v_g$; wrap-around contamination; reading carrier phase
  as arrival of information.
- **Epistemic classification:** envelope-at-$v_g$ — `theorem` given the linearization, itself an
  `approximation` box; crest/centroid speed measurements — `numerical-observation`; "information
  cannot outrun $c$ even where $v_p > c$" — `open-question` admonition (fronts and precursors are
  beyond this course; seeds 46).
- **Misconceptions:** claims registry id `packet-at-phase-velocity` (README conflict log re-points
  it here from `05-fourier`; yml edit lands when the module is built). Falsifying experiment:
  animate a narrowband deep-water packet tracking BOTH a marked carrier crest and the envelope
  centroid — the dots visibly separate, the crest at $2v_g$ overtaking and dying at the front while
  the centroid fit yields $v_g$; the plasma run shows $v_p > c$ with the measured centroid still at
  $v_g < c$. Distractor: "the pulse arrives when its first crest arrives, at $\omega/k$".
- **Glossary terms:** `wave-packet` (חבילת גלים), `phase-velocity` (מהירות פאזה), `group-velocity`
  (מהירות חבורה), `carrier` (גל נושא), `envelope` (מעטפת).
- **Interactive controls and simulations:** as in *explore*, plus a "mark a crest" button riveting
  the tracker dot to the crest under the cursor.
- **Virtual lab outline** (`notebooks/en/labs/12-wave-packets.ipynb`): (1) build `gaussian_packet`,
  view $|A(k)|$ via `fourier.spectrum`; (2) propagate under each family, watch crest vs centroid;
  (3) *measurement:* `track_envelope` on a noisy deep-water packet, weighted fit of $x_c(t)$ →
  $v_g \pm \sigma$ vs `group_velocity`; crest fit → $v_p$; report the ratio $0.5 \pm \sigma$;
  (4) plasma family: tabulate $v_p > c$, $v_g < c$, $v_p v_g/c^2 \to 1$.
- **Real-experiment counterpart:** slow-motion phone video of a stone dropped in still water; track
  one crest vs the ring radius (ratio estimate; caveat — pond rings are broadband).
- **Media assets** (`render_fourier_waves.py`): (c) the signature deep-water shot — crest dot and
  centroid dot with trails, crests born at the rear, dying at the front; (d) the same packet under
  the nondispersive family, dots locked together.
- **Quiz bank outline:** `Q-12-1` numeric $v_p$, $v_g$ from a given $\omega(k)$ (OBJ-12-1);
  `Q-12-2` numeric beat envelope speed (OBJ-12-2); `Q-12-3` MC which velocity carries the message
  (OBJ-12-3/5, distractor `packet-at-phase-velocity`); `Q-12-4` MC deep-water crest kinematics
  (OBJ-12-1); `Q-12-5` numeric centroid-fit reading (OBJ-12-4); `Q-12-6` free — superluminal $v_p$
  vs relativity (OBJ-12-5).
- **Problem set outline:** analytical — $v_g$ for the four families; $v_p v_g = c^2$ for the plasma
  form; envelope translation from the Taylor argument. Computational — crest vs centroid tracking;
  $v_g(k_0)$ across the lattice zone, $v_g \to 0$ at the band edge (a standing wave — module 11
  reappears). Challenge — stationary phase: the late-time field at $x/t$ is dominated by $k^*$ with
  $v_g(k^*) = x/t$.
- **Runtime budget:** FFT grids ≤ $2^{12}$, ≤ 200 frames, ≤ 60 sample times; sub-second in Pyodide.
- **Validation gates:** standard set with `--module 12-wave-packets`; the §4 seeds test lands with
  this module.
- **Open questions for the author:** does the plasma family enter core (as the admonition's
  vehicle) or stay in advanced; how much stationary-phase language in core prose (recommendation:
  none — pictures only, mathematics in the challenge).

### 5.3 `13-dispersion` — Dispersion: how media sort waves

- **Identity and scope:** master-plan notebook 4.4. Real $\omega(k)$ only; absorption and complex
  index wait for 16, nonlinearity for 51. The Lorentz-material curve is a cited sketch (trailer for
  `16-light-in-matter`), never derived here.
- **Prerequisites:** `12-wave-packets` ($v_g$, packets); `04-fourier-transform` (bandwidth theorem,
  Gaussian pair, FFT bridge); `07-normal-modes` (`coupled.chain_dispersion`).
- **Learning objectives:**
  - `OBJ-13-1` — Classify a medium from its omega(k): compute v_p(k) and v_g(k) for the
    nondispersive, lattice, deep-water, and material-sketch families and read both off the curve as
    chord and tangent.
  - `OBJ-13-2` — Derive the Gaussian spreading law sigma(t) = sigma0 sqrt(1 + (t/tau)^2) with
    tau = 2 sigma0^2 / |omega''(k0)| from the quadratic spectral phase.
  - `OBJ-13-3` — Propagate an arbitrary packet under an arbitrary omega(k) by FFT -> multiply by
    e^(-i omega(k) t) -> inverse FFT, and justify each step.
  - `OBJ-13-4` — Apply the bandwidth theorem to spreading: shorter pulses have wider bands and
    spread faster; estimate spreading for a fiber-like medium from |omega''|.
  - `OBJ-13-5` — Verify that dispersion conserves the norm and the magnitude spectrum, and describe
    the resulting chirp: the pulse is rearranged, never dissipated.
- **Mathematical background:** has — Gaussian pair, completing the square, second-order Taylor;
  introduced — quadratic spectral phase as the whole story of spreading; local spatial frequency
  read off a chirped waveform.
- **Physical intuition goals:** (1) a dispersive medium is a sorting machine — each wavelength
  leaves at its own speed; (2) a click enters, a glissando exits; (3) the peak drops because the
  pulse spreads, not because anything is absorbed; (4) the shorter the pulse, the faster it falls
  apart — its own bandwidth is the enemy.
- **Section skeleton seeds:**
  - *puzzle:* lightning's radio click, after a trip along Earth's magnetic field lines, arrives as
    a descending whistle lasting a second — the "whistler". Boxed: **what property of a medium
    turns a click into a glissando — and can we read the medium off the glissando?**
  - *predict:* (1) does a sharp click exit a dispersive medium as a click? (2) the spreading
    pulse's peak falls — is energy being absorbed? (targets `spreading-is-damping`) (3) which
    spreads faster in the same fiber: a 1 ns or a 1 ps pulse? (4) in which museum medium does every
    wavelength travel at one speed?
  - *explore:* the dispersion museum — four $\omega(k)$ curves with a draggable $k_0$ showing chord
    ($v_p$) and tangent ($v_g$); a packet racing under each curve; $\sigma_0$ slider with live
    $\sigma(t)$ plot against the analytic law; chirp view coloring the waveform by local frequency.
  - *derive:* museum tour → quadratic-phase spreading law → the spectral propagator as an algorithm
    (route below).
  - *verify:* fitted $\sigma(t)$ vs the law, late-time exponent $\to 1$ (`numerical-observation`);
    norm and $|A(k)|$ conserved to machine precision; nondispersive run = rigid translation
    matching d'Alembert.
  - *transfer:* 16 (the material sketch derived honestly, with absorption); 43 ($\sigma(t)$ ↔ waist
    $w(z)$ — beam diffraction is the same mathematics); 47 (GVD and fiber bit-rate limits — $\tau$
    becomes the dispersion length); 27 (why broadband light has short coherence); 51 (solitons,
    one-line trailer).
  - *quiz:* classify-the-medium; $\tau$ and $\sigma(t)$ numerics; the propagator's three steps;
    peak-drop energetics.
  - *explain:* explain the whistler to a radio amateur; why the 1 ps pulse loses to the 1 ns pulse;
    what "dispersive" promises about a rainbow (forward pointer, no derivation).
  - *advanced:* the chirped Gaussian written out — local frequency linear in $x$, fast components
    at the front when $\omega'' > 0$; reconstructing $\omega(k)$ from arrival times (the whistler
    lab's inverse problem); free-particle quantum spreading.
- **Core derivations:** (1) museum: $\omega = v|k|$ (the only family with $v_g = v_p$ for all $k$);
  lattice $\omega(k) = \omega_{\max}|\sin(ka/2)|$ (cite `coupled.chain_dispersion` and 07's
  measurement; $v_g \to 0$ at the zone edge); deep water $\omega = \sqrt{g|k|}$; Lorentz sketch via
  $k = n(\omega)\,\omega/c$ with $n^2 = 1 + \omega_p^2/(\omega_0^2-\omega^2)$ quoted, flagged as
  16's subject. (2) spreading: `gaussian_packet` of RMS intensity width $\sigma_0$ has a Gaussian
  spectrum of width $1/(2\sigma_0)$; propagation multiplies by
  $e^{-\ii[\omega_0 + v_g(k-k_0) + \frac12\omega''(k-k_0)^2]\,t}$; completing the square gives
  $\sigma(t) = \sigma_0\sqrt{1 + (t/\tau)^2}$, $\tau = 2\sigma_0^2/|\omega''(k_0)|$ — the bandwidth
  theorem's dynamical payoff: $\sigma_0\downarrow$ ⇒ band $\uparrow$ ⇒ $\tau\downarrow$,
  quadratically. (3) the propagator: sample $\psi_0$ → `fourier.spectrum` → multiply
  $e^{-\ii\omega(k)t}$ → `fourier.inverse_spectrum`; exact for the discretized field,
  norm-conserving by Parseval + unimodularity; the algorithm *is* `propagate_dispersive`.
- **Model specification draft:** System — an arbitrary 1-D packet under an arbitrary real, even
  $\omega(k)$, evolved spectrally. Dynamics — exact linear evolution by phase multiplication per
  component. Boundary — periodic FFT domain standing in for infinite space. Ensemble —
  deterministic; seeded noise for the fits. Ignored — absorption ($\Imag\,\omega = 0$),
  nonlinearity; the analytic law ignores beyond-quadratic terms (the numerics keep all orders).
  Valid when — the packet stays inside the window at all sampled times; band below Nyquist. Failure
  modes — wrap-around re-entry; under-sampling a strongly chirped field; trusting the $\sigma(t)$
  law where cubic dispersion matters.
- **Epistemic classification:** $\sigma(t)$ law — `theorem` (Gaussian + quadratic $\omega$),
  validity edge stated; spectral propagation exact for the discretized system — `theorem`; the
  material curve — `model-assumption` (sketch; trailer to 16); fitted spreading exponent and
  $\tau$ — `numerical-observation`; "what ultimately limits how short a usable pulse can be" —
  `open-question` pointer toward 47 and 55.
- **Misconceptions:** NEW `spreading-is-damping` — "A spreading pulse is being damped; dispersion
  dissipates its energy." Falsifier: under `propagate_dispersive` the norm $\int|\psi|^2 dx$ and
  $|A(k)|$ are conserved to machine precision while the peak falls — only spectral *phases* change,
  and the chirp view shows where the energy went (sorted, not spent). Distractor: "the medium
  absorbs the high frequencies, so the peak decays".
- **Glossary terms:** `dispersion` (נפיצה; `he_reject` candidate: דיספרסיה), `dispersion-relation`
  (cited, deposited by `07-normal-modes`), `chirp` (צ'ירפ — translator to decide on a coinage),
  `group-velocity-dispersion` (נפיצת מהירות חבורה).
- **Interactive controls and simulations:** the museum (draggable $k_0$, chord-and-tangent
  overlay); the four-lane packet race; spreading explorer ($\sigma_0$, family, $k_0$; live
  $\sigma(t)$ vs law); chirp colormap view.
- **Virtual lab outline** (`notebooks/en/labs/13-dispersion.ipynb`): (1) museum tour — $v_p(k)$,
  $v_g(k)$ tables; (2) race identical packets across the four families; (3) *measurement 1:*
  `track_envelope` widths on a noisy run → fit $\sigma_0$, $\tau$ vs `spreading_time`, extract
  $|\omega''|$ ± uncertainty; (4) *measurement 2:* late-time log-log fit of $\sigma(t)$ → exponent
  $1.0 \pm \sigma$ via `validation.scaling_exponent`; (5) chirp: local frequency vs position;
  (6) whistler data: import a public VLF recording, spectrogram, fit arrival time
  $t(f) \propto 1/\sqrt{f}$, report the constant.
- **Real-experiment counterpart:** publicly available whistler VLF audio (university VLF archives)
  imported as WAV — real dispersed data, fitted in the lab's final cells. No bench apparatus
  practical for mechanical dispersion at home.
- **Media assets** (`render_fourier_waves.py`): (e) four-lane packet race under the four
  $\omega(k)$ curves; (f) Gaussian spreading with chirp coloring, the $\sigma(t)$ curve drawing
  itself alongside.
- **Quiz bank outline:** `Q-13-1` MC classify media from $\omega(k)$ plots (OBJ-13-1); `Q-13-2`
  numeric $\tau$ and $\sigma(t)$ (OBJ-13-2); `Q-13-3` MC order the propagator's steps (OBJ-13-3);
  `Q-13-4` numeric ns-vs-ps fiber spreading (OBJ-13-4); `Q-13-5` MC peak-drop energetics
  (OBJ-13-5, distractor `spreading-is-damping`); `Q-13-6` free — describe the chirp and its sign
  (OBJ-13-5).
- **Problem set outline:** analytical — derive $\sigma(t)$ by the Gaussian integral; whistler
  arrival-time law; lattice $v_g$ at the zone edge. Computational — reconstruct $\omega(k)$ from
  simulated arrival times (the inverse problem); two-media relay race. Challenge — stiff string
  $\omega_n = n\omega_1\sqrt{1 + Bn^2}$: connect 11's mode ladder to dispersion and explain why
  piano tuners stretch octaves.
- **Runtime budget:** FFT grids ≤ $2^{12}$ ($2^{13}$ once, whistler spectrogram); ≤ 200 frames;
  ≤ 100 sample times. Sub-second per cell in Pyodide.
- **Validation gates:** standard set with `--module 13-dispersion`; the §4 conservation and scaling
  tests land with this module at the latest.
- **Open questions for the author:** which VLF recording to bundle (license, size); is the material
  sketch the museum's core fourth exhibit or an advanced fifth (recommendation: core, one
  paragraph, heavy trailer framing); does the quantum aside survive review.

## 6. Part-level assessment and capstone hooks

- Capstone §35.4 (optical communication system) consumes this part directly:
  `propagate_dispersive` + `spreading_time` are the fiber-dispersion stage; 13's $|\omega''|$
  extraction lab is the capstone's calibration step.
- Capstone §35.2 (virtual optical bench) and part XI's 4-f processor inherit the
  spectral-propagation pattern that part IX's angular-spectrum propagator re-instantiates in space.
- Cross-module synthesis problem (lives with this part's problem sets): follow one guitar pluck end
  to end — decompose it (11), send the same shape down an effectively infinite string as a packet
  (12), add stiffness and watch harmonics drift and the packet chirp (13). One problem touching 03,
  07, 08, 11–13.
- Exam themes: chord-and-tangent readings of $\omega(k)$; pluck-position → spectrum reasoning;
  order-of-magnitude spreading estimates from bandwidth alone; "which velocity?" scenarios.

## 7. Build order and validation gates

Build `11-standing-waves` → `12-wave-packets` → `13-dispersion`. 11 must follow part-03's first
modules because it consumes the FDTD solver, the energy/flux evaluators, and `waves.py` itself
(part-03 introduces the file and its docstring); 12 needs only `fourier.py` plus this plan's
additions; 13 needs 12's $v_g$ on the page. Across parts: part-03 modules → `11` → `12` → `13`.

With `11-standing-waves`, deposit the §5 glossary lists and add the three NEW registry entries
(`pluck-single-frequency`, `flat-string-no-energy`, `spreading-is-damping`), status `pending` until
their pages address them. With `12-wave-packets`, apply the README conflict-log re-pointing of
`packet-at-phase-velocity` from `05-fourier` to `12-wave-packets` and flip it to `addressed` once
the falsifying animation and distractor exist.

Per module: the standard four gates (README). Additionally: the §4 `waves.py` extension tests land
*with* their consuming module (conservation + convergence with 11; limits + seeds with 12;
scaling + dimensions with 13 at the latest), since parts V and XII cite these guarantees.

## 8. Deviations from the master plan

- **Merge (4.1 + 4.2 → `11-standing-waves`):** boundary-condition quantization and modal
  decomposition are one lesson — first find the eigenbasis, then use it as coordinates; splitting
  them would strand 4.1 without a payoff. Precedent: `02-damped-driven` ← 1.2 + 1.3.
- **`waves.py` ownership split with part-03 (single-owner rule):** part-03 introduces the file and
  owns its docstring model spec, the FDTD solver, d'Alembert, energy densities/flux,
  impedance/junction coefficients, and boundary handling; this plan extends the same file and owns
  exactly the modal, packet, dispersion-family, spectral-propagator, velocity-evaluator, and
  envelope-tracker functions listed in §4. Every cross-referenced function is defined in exactly
  one plan.
- **Registry re-pointing claimed:** `packet-at-phase-velocity` is claimed by `12-wave-packets` per
  the README conflict log; the yml edit happens when the module is built (§7).
- **Additions beyond the master plan:** the two derivations of standing waves reconciled
  explicitly; the zero-energy-flux theorem as module 09's payoff; musical acoustics as 11's running
  laboratory; the analytic $\sigma(t)$ law with the bandwidth theorem as its engine (the master
  plan only asks to "simulate pulse broadening"); the whistler real-data lab; the superluminal
  open-question admonition seeding 46; three new registry misconceptions; the Lorentz material
  model demoted to an explicit trailer for 16 rather than a derived example.
