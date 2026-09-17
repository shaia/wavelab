# Part V — Electromagnetic Waves — Implementation Plan

> **Master plan:** §12 (Part V). **Modules:** `14-em-waves`, `15-em-energy`, `16-light-in-matter`. **Status:** planned.
> Canonical numbering, invariants, and conflict log: [README.md](README.md).

## 1. Part overview and narrative arc

Part V is the hinge of the course. Parts I–IV earned the wave equation *mechanically* — masses,
springs, tension over mass density, every term auditable by hand — and Part IV added the spectral
machinery for taking any wave apart. Part V opens with four equations from a different course
entirely, Maxwell's, and watches the same operator assemble itself out of a curl-of-curl identity:
$\nabla^2\mathbf{E} = \mu_0\epsilon_0\,\partial_t^2\mathbf{E}$. The speed that falls out is a
combination of two *electrical* constants — and it equals the measured speed of light. Light joins
the course not by announcement but by recognition: it solves an equation the student already knows
how to solve. Everything after is optics: this wave meeting geometry and matter.

The master plan calls $c = 1/\sqrt{\mu_0\epsilon_0}$ "a major conceptual event", and this plan
stages it as one — specifically, as a *measurement*. $\epsilon_0$ comes from charging a capacitor
in a basement, $\mu_0$ from forces between current-carrying coils; neither experiment involves
anything that shines. Combined they give $2.998\times10^8$ m/s — the number Fizeau's toothed wheel
was then producing for light (Weber and Kohlrausch's 1856 electrical ratio: $3.1\times10^8$ m/s).
Module 14's laboratory has the student *redo* this convergence with noisy synthetic capacitor and
coil data, propagating uncertainties into $c \pm \sigma$; a 2019 postscript notes that today the
SI inverts the logic — $c$ exact, $\mu_0$ measured (`constants.py`).

The three modules divide the physics as existence, bookkeeping, and matter. `14-em-waves` (5.1 +
5.2 merged, §8) derives the wave equation and reads the solution's geometry out of the same
equations: transversality from $\nabla\cdot\mathbf{E} = 0$, the
$\mathbf{E}\perp\mathbf{B}\perp\mathbf{k}$ triad and the amplitude lock $B_0 = E_0/c$ from
Faraday — derived, never asserted. `15-em-energy` does the accounting: Poynting's theorem and the
time average $\langle\cos^2\rangle = \tfrac12$ — named here, once, as *the workhorse identity*:
every interference and diffraction intensity formula in Parts VIII–XI is an amplitude squared
pushed through this average. `16-light-in-matter` is module 02 wearing electromagnetic clothes:
the bound electron is a damped driven oscillator forced by the wave's field, its response — the
very `oscillators.steady_state_response` of part-01 — becomes a susceptibility, and out come
$n(\omega)$ with the same Lorentzian resonance, absorption as $n + \ii\kappa$, Sellmeier in the
transparent window, and the registry's frequency misconception falsified by counting crests.

Objects planted earlier collect their payoff, and new seeds go in. The Lorentzian makes its third
appearance (02's resonance, 04's transform pair, 16's absorption line — later 26's Fabry–Pérot
line and 44's cavity mode); the dispersion language of 12/13 meets its first *material*
dispersion, redeeming the `waves.omega_material_sketch` trailer part-04 planted. Forward:
$n(\omega)$ manufactured here is the raw material of Part VI (Snell needs a number), thin-film
colours (24), chromatic aberration (37), and fiber dispersion (47); the transverse plane's two
dimensions seed Part VII; and the $E_0 \leftrightarrow$ irradiance calibration habit (sunlight
$\approx 870$ V/m) starts the practice of attaching magnitudes to field symbols.

## 2. Position in the course

- **Requires:**
  - `14-em-waves`: `08-wave-equation` (the 1-D wave equation, travelling solutions
    $e^{\ii(kx-\omega t)}$; the 3-D form as notational generalization); `13-dispersion`
    ($\omega(k)$ diagrams); `00-phasors` (complex representation, $e^{-\ii\omega t}$).
  - `15-em-energy`: `14-em-waves` (plane waves, the triad, $B = E/c$); `09-wave-energy` (string
    energy density and flux — the analogy upgraded: $P = -T\,y_x y_t \to \mathbf{S}$).
  - `16-light-in-matter`: `02-damped-driven` (`oscillators.steady_state_response`, the
    Lorentzian, $Q$, steady state as response at the drive frequency); `14`/`15` (plane waves;
    absorption as intensity decay); `12`/`13` (group velocity, `waves.group_velocity`, the
    material trailer); `04-fourier-transform` (the Lorentzian pair, recognized in $\chi''$).
- **Feeds:** `17-refraction` (the number $n$, the wavelength-shortening picture Snell is built
  from); `18-fresnel` ($I = \tfrac12 c\epsilon_0 n E_0^2$ for power coefficients);
  `19-evanescent` (the $n + \ii\kappa$ machinery with imaginary $k_z$); `20`–`22` (the
  transverse plane's two field dimensions); `23`–`32` (every intensity formula = amplitude
  squared through $\langle\cos^2\rangle = \tfrac12$); `24-thin-films` ($n(\lambda)$ → colour);
  `26-fabry-perot` / `44-resonators` (the Lorentzian line again); `37-aberrations` (chromatic
  aberration = Sellmeier in a lens); `47-fibers` (group index → pulse spreading).
- **Explicitly not assumed:** any prior exposure to *electromagnetic waves* — the student's EM
  course may have stopped at circuits and induction. What IS assumed from it, stated in the
  content: Maxwell's equations themselves (given empirical laws, the module's boxed
  `empirical-law`) and the vector-calculus identities
  ($\nabla\times(\nabla\times\mathbf{F}) = \nabla(\nabla\cdot\mathbf{F}) - \nabla^2\mathbf{F}$,
  quoted, not proven). NOT assumed: special relativity; photons; boundary-value
  electromagnetism (Part VI); anisotropic or magnetic media ($\mu = \mu_0$ throughout);
  local-field corrections.

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|
| `14-em-waves` | `content/en/em-waves/14-em-waves.md` | Maxwell's equations and the electromagnetic wave | 5.1 + 5.2 | Hecht, electromagnetic theory of light; Griffiths, EM waves in vacuum | planned |
| `15-em-energy` | `content/en/em-waves/15-em-energy.md` | Energy, irradiance, and the Poynting vector | 5.3 | Hecht, energy and momentum of light; Griffiths, Poynting's theorem | planned |
| `16-light-in-matter` | `content/en/em-waves/16-light-in-matter.md` | Light in matter: the refractive index | 5.4 | Hecht, dispersion; Griffiths, EM waves in matter, absorption and dispersion | planned |

## 4. Shared infrastructure for this part

**`src/wavelab` — existing used:** `constants.C_LIGHT` / `MU_0` / `EPS_0` / `SIGN_CONVENTION`
(14's verify section quotes the docstring); `oscillators.steady_state_response` (16's electron —
cited by name, owned by part-01) and `oscillators.power_absorbed` (shape comparison against
$\chi''$); `waves.group_velocity` / `propagate_dispersive` / `gaussian_packet` /
`omega_material_sketch` (16; names per parts 03/04); `fourier.lorentzian_spectrum`;
`measurement.add_noise` / `fit_cosine`; `validation.scaling_exponent` / `convergence_study` /
`seed_study` / `relative_error`.

**`src/wavelab` — new: `em.py`** (introduced and owned by this part; README ownership table;
serves 14–16 and is consumed, never extended, by later parts). Docstring model spec:

- **System:** monochromatic plane electromagnetic waves — $\mathbf{E}$ and $\mathbf{B}$ in vacuum
  and in linear, homogeneous, isotropic media described by a complex scalar susceptibility;
  observables: fields, energy densities, flux, irradiance, the complex index.
- **Dynamics:** Maxwell's equations reduced to plane-wave algebra — closed forms on grids, never
  a field solver (no FDTD; propagation through dispersion uses part-04's machinery).
- **Boundary:** unbounded homogeneous media only; interfaces belong to `interfaces.py` (part-06).
- **Ensemble:** deterministic; callers add noise via `wavelab.measurement`.
- **Ignored:** sources (how the wave was launched); magnetic response ($\mu = \mu_0$);
  anisotropy (part-07); nonlinearity; local-field corrections; the photon.
- **Valid when:** fields weak enough for linear response; medium homogeneous on the wavelength
  scale; single frequency, or narrow bands treated as packets on top of $n(\omega)$.
- **Failure modes:** dilute $n \approx 1 + \chi/2$ applied to dense media; Sellmeier evaluated
  inside an absorption band; intensity formulas fed a complex $n$; near-resonance $v_p > c$ read
  as a causality violation instead of a group-velocity conversation.

Function-level sketch (signatures + contracts):

```python
plane_wave_fields(r, t, e0, k_vec, omega, pol) -> (E, B)
                       # real E, B satisfying all four vacuum Maxwell equations; B = k_hat x E / c;
                       #   raises unless omega == c|k_vec| and pol is transverse to k_vec
poynting(E, B) -> S    # instantaneous S = E x B / mu0 [W/m^2], any matching shapes
energy_densities(E, B) -> (u_E, u_B)     # eps0 E^2/2 and B^2/(2 mu0); equal for a plane wave
intensity_from_amplitude(e0, n=1.0) -> I   # (1/2) c eps0 n e0^2 [W/m^2]; n real (transparent)
amplitude_from_intensity(intensity, n=1.0) -> e0   # inverse; the sunlight -> 870 V/m call
radiation_pressure(intensity, reflectivity=0.0) -> P   # (1 + R) I / c [Pa]
lorentz_susceptibility(omega, omega0, gamma, n_density) -> chi
                       # chi = omega_p^2/(omega0^2 - omega^2 - i gamma omega), omega_p^2 =
                       #   n_density e^2/(eps0 m_e) — implemented as (n_density e^2/eps0) times
                       #   oscillators.steady_state_response per unit force at the electron mass:
                       #   the susceptibility IS part-01's mechanical response, rescaled
refractive_index(omega, omega0, gamma, n_density) -> n_complex
                       # sqrt(1 + chi), branch with Im >= 0: n + i kappa under e^{-i omega t}
sellmeier(lam, b_coeffs, c_coeffs) -> n  # sqrt(1 + sum B_i lam^2/(lam^2 - C_i)); real n,
                       #   transparent regions only; raises inside any pole window
absorption_coefficient(kappa, lam_vac) -> alpha  # intensity 4 pi kappa / lam_vac [1/m];
                       #   Beer-Lambert I(z) = I(0) e^{-alpha z}
group_index(omega, n_of_omega, domega=1e-4) -> n_g  # n + omega dn/domega; v_g = c / n_g
```

**`tests/physics/` additions:**

- *dimensions:* `poynting` / `intensity_from_amplitude` in W/m², `radiation_pressure` in Pa,
  `absorption_coefficient` in 1/m, `group_index` dimensionless — against the `units` registry.
- *limits:* `refractive_index` → $1 + 0\ii$ as `n_density` → 0, $\kappa \to 0$ far below
  resonance; `sellmeier` vs the full lossless Lorentz form in the transparent window
  ($< 10^{-6}$); `group_index` → $n$ where dispersion is flat; $B_0/E_0 = 1/c$ to machine
  precision; the $\gamma \to 0$ limit of `refractive_index` reproduces the
  `waves.omega_material_sketch` branch point-for-point (part-04's trailer, pinned).
- *conservation:* time-averaged `poynting` of `plane_wave_fields` = `intensity_from_amplitude`
  = $c\,\times$ mean total `energy_densities` (energy-flux consistency, the part's headline
  test); Poynting-theorem residual $\partial_t u + \nabla\cdot\mathbf{S} = 0$ on the plane wave
  by finite differences; $u_E = u_B$ pointwise.
- *scaling:* $I \propto E_0^2$ with fitted exponent 2.00 via `validation.scaling_exponent`;
  $\alpha$ linear in $\kappa$; on-resonance $\kappa$ peak linear in `n_density` (dilute).
- *convergence:* Maxwell residuals of `plane_wave_fields` second order in the step;
  `group_index` error $\propto d\omega^2$; partial-period averages of $|\mathbf{S}|$ → the
  exact half as $1/N$ (whole periods: exact).
- *seeds:* the Sellmeier fit on seeded noisy $n(\lambda)$ data recovers the coefficients within
  reported uncertainty, scatter $\propto 1/\sqrt{M}$ via `validation.seed_study`.

**Shared media:** three scripts — `media/render/render_em_triad.py` (14),
`media/render/render_poynting.py` (15), `media/render/render_light_matter.py` (16); shot lists
in §5. **Glossary themes:** electromagnetic-wave vocabulary (14), radiometric energy vocabulary
(15), optical-materials vocabulary (16). `energy-density` / `energy-flux` (part-03) and
`dispersion` (part-04) are cited here, never re-deposited.

## 5. Module specifications

### 5.1 `14-em-waves` — Maxwell's equations and the electromagnetic wave

- **Identity and scope:** notebooks 5.1 + 5.2, merged (§8). Maxwell → wave equation → $c$;
  plane waves, transversality, the triad, phase fronts, the spectrum. Deferred: energy → `15`;
  media → `16`; boundaries → part-06; polarization states → part-07; how antennas launch waves
  → out of scope (qualitative Hertz material only).
- **Prerequisites:** `08-wave-equation` (the operator, travelling solutions); `13-dispersion`
  ($\omega(k)$ as an object); `00-phasors` (complex representation).
- **Learning objectives:**
  - `OBJ-14-1` — Derive the vacuum wave equation for E and B from Maxwell's equations via the
    curl-of-curl identity, and identify the wave speed as c = 1/sqrt(mu0 eps0).
  - `OBJ-14-2` — Compute c from tabletop values of mu0 and eps0, and explain why agreement with
    the measured speed of light identifies light as an electromagnetic wave.
  - `OBJ-14-3` — Show from div E = 0 that plane electromagnetic waves are transverse, and from
    Faraday's law that B = (k_hat x E)/c — a right-handed E, B, k triad with B0 = E0/c.
  - `OBJ-14-4` — Describe a plane wave by its phase fronts: planes of constant k . r - omega t,
    filling all space, advancing at c along k_hat, with omega = c |k|.
  - `OBJ-14-5` — Place radio, microwave, visible, and X-ray radiation on the one dispersion
    relation omega = c |k|, stating what varies across the spectrum and what never does.
- **Mathematical background:** has — div/curl, the quoted curl-of-curl identity, the 1-D wave
  equation, complex travelling waves; introduced here — the 3-D $\nabla^2$ acting
  componentwise, the wavevector as a genuinely 3-D object, phase fronts as level sets.
- **Physical intuition goals:** (1) nothing material waves — field values oscillate, at every
  point of the space the wave occupies; (2) the triad is rigid: two of
  $\{\mathbf{E}, \mathbf{B}, \mathbf{k}\}$ determine the third, and $B$ in tesla is $E$ in V/m
  divided by $3\times10^8$; (3) a detector *anywhere* on a phase plane reads the same signal;
  (4) radio and X-rays differ in one number only.
- **Section skeleton seeds:**
  - *puzzle:* two basement experiments — a capacitor gives $\epsilon_0$, coil forces give
    $\mu_0$; neither involves anything that shines. Combined: $2.998\times10^8$ m/s, the very
    number Fizeau's wheel was then measuring for light. Boxed: why should benchtop electricity
    know how fast light goes — coincidence, or identity?
  - *predict:* (1) a wave with no medium — what plays the string-displacement role? (2) is
    $\mathbf{E}$ along the travel direction (like sound) or across it (like the string)?
    (3) sunlight has $E_0 \sim 10^3$ V/m — is its $B_0$ huge, tiny, or middling as magnetic
    fields go? (4) a detector 1 m beside the "ray" drawn in every textbook figure — does it
    read zero? (targets NEW `em-wave-on-a-line`).
  - *explore:* 3-D visualizer — field arrows on a spatial *lattice*, not just along one axis;
    $\hat{\mathbf{k}}$ direction, $\lambda$, phase sliders; E/B/phase-plane toggles; a
    draggable probe reading $E(t)$ live anywhere — off-axis changes nothing. Second panel:
    "$c$ from constants" — dial $\mu_0$, $\epsilon_0$, watch the computed speed.
  - *derive:* Maxwell's vacuum equations stated (`empirical-law` box) → curl of Faraday +
    identity → wave equations, $c^2 = 1/\mu_0\epsilon_0$, numbers plugged → plane-wave ansatz
    → transversality → Faraday gives the triad and the lock → Ampère–Maxwell closes the loop,
    forcing $\omega = c|k|$ → phase fronts as moving planes.
  - *verify:* `plane_wave_fields` satisfies all four equations under numerical
    differentiation, residual second order (the `numerical-observation` box); $B_0/E_0 = 1/c$
    across random draws; computed $1/\sqrt{\texttt{MU\_0}\cdot\texttt{EPS\_0}}$ vs `C_LIGHT` —
    with the 2019-SI aside: in 1865 the left side predicted the measured right side; today $c$
    is exact and $\mu_0$ carries the uncertainty. Same equation, inverted roles.
  - *transfer:* Hertz 1887 — spark gap, standing waves across a room, node spacing →
    $\lambda$, known $f$ → speed $= c$: the prediction closed within a generation; the
    spectrum as one dispersion relation spanning 20 decades; `17-refraction` onward — optics
    is this wave meeting matter; $\mathbf{E}_0$'s two transverse dimensions → part-07.
  - *quiz:* triad geometry; $c$ from constants; why longitudinal plane waves are impossible;
    $B_0$ from $E_0$; the off-axis detector (distractor); what changes across the spectrum.
  - *explain:* what oscillates, without the word "ether"; name the equation that forbids the
    longitudinal option; explain to a 19th-century physicist why Weber–Kohlrausch's number
    settled what light is; what a phase front is and what moves at $c$.
  - *advanced:* near vs far field of an oscillating dipole — where the triad picture is
    honest; the ether that wasn't (one-paragraph Michelson–Morley culture note). Safe to skip.
- **Core derivations:** (1) $\nabla\times(\nabla\times\mathbf{E}) = -\nabla^2\mathbf{E}$ in
  vacuum and $= -\partial_t(\nabla\times\mathbf{B}) = -\mu_0\epsilon_0\,\partial_t^2\mathbf{E}$
  ⇒ $\nabla^2\mathbf{E} = \mu_0\epsilon_0\,\partial_t^2\mathbf{E}$, same for $\mathbf{B}$;
  $c = 1/\sqrt{\mu_0\epsilon_0} = 299\,792\,458$ m/s. (2) Ansatz
  $\mathbf{E} = \Real[\mathbf{E}_0\,e^{\ii(\mathbf{k}\cdot\mathbf{r} - \omega t)}]$:
  $\nabla\cdot\mathbf{E} = 0 \Rightarrow \mathbf{k}\cdot\mathbf{E}_0 = 0$ — no longitudinal
  component exists. (3) Faraday: $\ii\,\mathbf{k}\times\mathbf{E}_0 = \ii\,\omega\mathbf{B}_0
  \Rightarrow \mathbf{B}_0 = (\hat{\mathbf{k}}\times\mathbf{E}_0)/c$ — perpendicularity *and*
  the amplitude lock in one line. (4) Ampère–Maxwell on the ansatz ⇒ $\omega = c\,|k|$; phase
  fronts $\mathbf{k}\cdot\mathbf{r} - \omega t = \text{const}$ are planes
  $\perp \hat{\mathbf{k}}$ advancing at $\omega/|k| = c$.
- **Model specification draft:** System — $\mathbf{E}$ and $\mathbf{B}$ in a source-free
  vacuum region; observables: field components anywhere, phase-front geometry. Dynamics —
  Maxwell's four vacuum equations; plane-wave closed forms (no field solver). Boundary —
  unbounded vacuum, no charges or currents. Ensemble — deterministic. Ignored — sources and
  antennas; media; energy bookkeeping (next module); quantization. Valid when — the region is
  genuinely source-free and fields classical. Failure modes — asking what the wave "is made
  of" mechanically; treating drawn arrows as spatial displacements; expecting a rest frame.
- **Epistemic classification:** Maxwell's equations — `empirical-law` (THE boxed one: this
  module's given, as Hooke's law was 01's); wave equation + $c$, transversality, the triad,
  $\omega = c|k|$ — `theorem` (given Maxwell); "light *is* that wave" — `empirical-law` (the
  identification is experimental — Weber–Kohlrausch and Hertz, not mathematics; the page says
  so explicitly); Maxwell residuals — `numerical-observation`.
- **Misconceptions:** NEW `em-wave-on-a-line` — "An electromagnetic wave exists only along the
  line where the textbook draws its E and B arrows, which show something displacing sideways
  in space." Falsifier: render one plane wave on a 3-D lattice of probes — every point on a
  phase plane carries the identical field, a probe moved off the drawn axis reads the same
  $E(t)$, and nothing material is displaced (arrows are field *values*). Distractor:
  `Q-14-5`'s option that a detector beside the drawn ray reads nothing.
- **Glossary terms:** `electromagnetic-wave` (גל אלקטרומגנטי), `plane-wave` (גל מישורי),
  `wavefront` (חזית גל), `wave-vector` (וקטור גל — part-03's `wavenumber` is the scalar; this
  is the 3-D object), `transversality` (רוחביות — translator to confirm),
  `vacuum-permittivity` (מקדם החדירות החשמלית של הריק; `he_reject` candidate: מקדם דיאלקטרי),
  `vacuum-permeability` (מקדם החדירות המגנטית של הריק).
- **Interactive controls and simulations:** lattice visualizer ($\hat{\mathbf{k}}$ by two
  angles, $\lambda \in [0.5, 4]$ grid units, phase scrub; arrow lattice $\le 12^3$; toggles;
  probe with live $E(t)$ trace); "$c$ from constants" dial (log sliders, CODATA snap-to).
- **Virtual lab outline** (`notebooks/en/labs/14-em-waves.ipynb`): (1) build a plane wave with
  `plane_wave_fields`, probe random points, confirm equal fields on a phase plane; (2) Maxwell
  residuals by finite differences, order-2 convergence plot; (3) $B_0/E_0$ across random draws
  → $1/c$; (4) *measurement:* synthetic Weber–Kohlrausch — noisy capacitor data
  ($C = \epsilon_0 A/d$ with uncertain $A$, $d$, $Q$, $V$) and coil-force data →
  $\epsilon_0 \pm \sigma$, $\mu_0 \pm \sigma$ → propagated $c \pm \sigma$ vs `C_LIGHT` (the
  headline result); (5) Hertz cell: standing wave against a reflector, node spacing
  $\lambda/2$, known $f$ → $c$ by a second route.
- **Real-experiment counterpart:** the chocolate-bar microwave measurement — turntable out,
  heat until spots melt at the antinodes, spacing $\lambda/2 \approx 6$ cm, $f = 2.45$ GHz off
  the oven label → $c = 2f \times$ spacing to a few percent. Import: measured spacings typed
  into a notebook cell, uncertainty from spot-width spread.
- **Media assets** (`render_em_triad.py`): (a) the honest triad — a volume slab filled with E
  and B arrows on a lattice, phase planes gliding through, camera orbiting: the wave occupies
  *space*, not a line; an off-axis probe point pulsing in sync with an on-axis one; (b) Hertz
  visual — an oscillating dipole, field-line kinks detaching and propagating at one fixed
  speed. No burned-in text.
- **Quiz bank outline:** `Q-14-1` MC — $\mathbf{E} \parallel \hat{y}$, $\mathbf{k} \parallel
  \hat{z}$: direction of $\mathbf{B}$ (OBJ-14-3); `Q-14-2` numeric — $c$ from given $\mu_0$,
  $\epsilon_0$ (OBJ-14-1, OBJ-14-2); `Q-14-3` MC — which Maxwell equation forbids a
  longitudinal plane wave (OBJ-14-3); `Q-14-4` numeric — $B_0$ for $E_0 = 870$ V/m (OBJ-14-3);
  `Q-14-5` MC — the off-axis detector (OBJ-14-4; distractor `em-wave-on-a-line`); `Q-14-6` MC
  — radio vs X-ray: what changes, what doesn't (OBJ-14-5); `Q-14-7` free — the
  Weber–Kohlrausch argument in the student's own words (OBJ-14-2).
- **Problem set outline:** analytical — the $\mathbf{B}$ wave equation carried out; any
  $f(\mathbf{k}\cdot\mathbf{r} - \omega t)$ solves the wave equation iff $\omega = c|k|$; the
  triad's right-handedness from the derivation's signs. Computational — residual convergence
  order; two plane waves at an angle → map the stationary pattern (a trailer for 23).
  Challenge — the far field of an oscillating dipole from causality + transversality alone.
- **Runtime budget:** closed forms only; arrow lattice $\le 12^3$ per frame, $\le 300$ frames;
  residuals on $\le 64^3$ single-time grids evaluated once — seconds in Pyodide.
- **Validation gates:** standard set (README) with `--module 14-em-waves`; the
  `plane_wave_fields`, `energy_densities`, and Maxwell-residual tests (§4) land here.
- **Open questions for the author:** integral vs differential Maxwell as the starting
  statement (recommend differential, integral in a dropdown); how much Hertz in core vs
  advanced (recommend puzzle mention + transfer paragraph, apparatus in advanced); whether the
  "$c$ from constants" dial misleads (constants are not knobs — keep it, one caption sentence).

### 5.2 `15-em-energy` — Energy, irradiance, and the Poynting vector

- **Identity and scope:** notebook 5.3. Poynting's theorem, energy density and flux, time
  averages, irradiance ↔ amplitude, radiation pressure (advanced). Deferred: interference
  energy bookkeeping → `23`; power flow at boundaries → `18`; beam profiles → `43`; photon
  momentum beyond a one-line aside → out of scope.
- **Prerequisites:** `14-em-waves` (plane waves, triad, $B = E/c$); `09-wave-energy` (the
  string analogy being upgraded); `00-phasors` (amplitude squared vs intensity, $N$ vs $N^2$).
- **Learning objectives:**
  - `OBJ-15-1` — Derive Poynting's theorem from Maxwell's equations and interpret
    u = eps0 E^2/2 + B^2/(2 mu0) and S = E x B / mu0 as energy density and energy flux.
  - `OBJ-15-2` — Show that u_E = u_B for a plane wave and that S = c u k_hat instantaneously.
  - `OBJ-15-3` — Time-average with <cos^2> = 1/2 to obtain I = (1/2) c eps0 E0^2, and
    recognize this identity as the origin of the 1/2 in every later intensity formula.
  - `OBJ-15-4` — Convert both ways between irradiance and field amplitude, in vacuum and in a
    transparent medium (I = (1/2) c eps0 n E0^2), attaching correct magnitudes: sunlight at
    about 1 kW/m^2 corresponds to E0 of about 870 V/m and B0 of about 3 microtesla.
  - `OBJ-15-5` — Compute radiation pressure P = (1 + R) I / c on absorbing and reflecting
    surfaces and evaluate solar-sail-scale forces.
- **Mathematical background:** has — vector identities (one more quoted:
  $\nabla\cdot(\mathbf{E}\times\mathbf{B}) = \mathbf{B}\cdot\nabla\times\mathbf{E} -
  \mathbf{E}\cdot\nabla\times\mathbf{B}$), time averaging from part-01; introduced here —
  continuity equations as the universal bookkeeping form, momentum density (advanced).
- **Physical intuition goals:** (1) energy rides *in the fields*, half electric, half magnetic
  — exactly; (2) brightness is amplitude *squared*: doubling $E_0$ quadruples the light;
  (3) sunlight is about a kilovolt per metre and a toaster per towel — magnitudes a physicist
  carries; (4) light pushes, but gently: full sunlight on a palm is tens of nanonewtons.
- **Section skeleton seeds:**
  - *puzzle:* face the sun: every square metre of you intercepts about a kilowatt — yet
    nothing arrives. No mass, no medium, no current. Boxed: where is that energy between sun
    and skin, what carries it, and what does "bright" measure in the field's own units?
    Secondary hook: a 5 mW laser pointer out-brightens the sun per area — check it by the end.
  - *predict:* (1) double the field amplitude — brightness ×2 or ×4? (targets NEW
    `amplitude-doubles-intensity`); (2) sunlight's $E_0$: 0.01, 1, 1000, or $10^6$ V/m?
    (3) the energy split: mostly electric, mostly magnetic, or exactly even — given that
    $B_0 = E_0/c$ "looks tiny"? (4) can sunlight push a sheet of foil hard enough to matter?
  - *explore:* energy dashboard on a live plane wave — $u_E$, $u_B$, $|\mathbf{S}(z,t)|$
    pulsing at $2\omega$, the running average converging to $\tfrac12 c\epsilon_0 E_0^2$; an
    $E_0$ slider accumulating a log-log $(E_0, I)$ trace of slope 2; a calibration card
    cycling real sources (sunlight, laser pointer, phone screen, Wi-Fi at 1 m).
  - *derive:* Poynting's theorem — dot Faraday with $\mathbf{B}/\mu_0$, Ampère–Maxwell with
    $\epsilon_0\mathbf{E}$, subtract via the identity → $\partial_t u + \nabla\cdot\mathbf{S}
    = 0$ with $u$ and $\mathbf{S}$ *defined by the derivation*, not decreed → equipartition
    from $B = E/c$ → $\mathbf{S} = c\,u\,\hat{\mathbf{k}}$ → $\langle\cos^2\rangle = \tfrac12$
    — boxed as the workhorse identity, with the forward declaration to Parts VIII–XI →
    $I = \tfrac12 c\epsilon_0 E_0^2$; with an index $\tfrac12 c\epsilon_0 n E_0^2$ (stated; 18
    uses it) → calibration numbers → (advanced) momentum density and radiation pressure.
  - *verify:* whole-period average of $|\mathbf{S}|$ = exact half; partial-window convergence
    $\propto 1/N$; equipartition pointwise; the $E_0$ sweep — fitted exponent 2.00 (the
    `numerical-observation` box); Poynting-theorem residual on the plane wave.
  - *transfer:* `23`–`32` — say it explicitly: fringe formulas are amplitudes squared,
    time-averaged by *this* identity; `18-fresnel` — power coefficients need the $n$-weighted
    irradiance; inverse-square as flux conservation through spheres; laser-safety classes as
    irradiance culture; the solar constant and Earth's energy budget.
  - *quiz:* amplitude ↔ irradiance both ways; the ×4 question; energy split; $\mathbf{S}$
    direction; radiation-pressure numerics; the workhorse identity in words.
  - *explain:* why doubling amplitude quadruples brightness but doubling random-phase
    *sources* only doubles it (00's thread in energy units); why the magnetic half is not
    negligible though $B_0$ "is small"; what an irradiance detector averages, over what time;
    why the $\tfrac12$ will follow the course to its last module.
  - *advanced:* momentum density $\mathbf{g} = \mathbf{S}/c^2$ stated (stress-tensor proof
    deferred; plausibility via $p = E/c$ in one line); $P = (1+R)I/c$; solar-sail numbers — at
    1 AU ($I = 1361$ W/m²) a perfect 32 m² mirror feels 0.29 mN, and a 5 kg craft gains
    ~5 m/s per day, forever, on sunlight. Safe to skip.
- **Core derivations:** (1) $\partial_t[\tfrac{\epsilon_0}{2}E^2 + \tfrac{1}{2\mu_0}B^2] +
  \nabla\cdot[\tfrac{1}{\mu_0}\mathbf{E}\times\mathbf{B}] = 0$. (2) Equipartition:
  $u_B = B^2/2\mu_0 = E^2/(2\mu_0 c^2) = \tfrac{\epsilon_0}{2}E^2 = u_E$ — exact, from the
  amplitude lock. (3) $|\mathbf{S}| = EB/\mu_0 = c\,\epsilon_0 E^2 = c\,u$, direction
  $\hat{\mathbf{k}}$. (4) $\langle\cos^2(kz - \omega t)\rangle = \tfrac12$ ⇒
  $I = \tfrac12\,c\,\epsilon_0 E_0^2$; with an index, $\tfrac12\,c\,\epsilon_0\,n\,E_0^2$.
  (5) Calibration: $E_0 = \sqrt{2I/c\epsilon_0}$ — sunlight $10^3$ W/m² ⇒ $E_0 \approx 870$
  V/m, $B_0 \approx 2.9\ \mu$T; a 1 mW pointer in a 1 mm spot ⇒ $I \approx 1.3$ kW/m² — the
  keychain out-brightens the sun per area. (6) Pressure: absorbed $I/c$, mirrored $2I/c$;
  sunlight on a palm ≈ 30 nN.
- **Model specification draft:** System — energy, flux, and momentum bookkeeping of the vacuum
  plane wave; observables $u_E$, $u_B$, $\mathbf{S}$, $I$, pressure on test surfaces. Dynamics
  — Maxwell plus Poynting's theorem; averages over whole periods. Boundary — unbounded;
  detectors idealized as time-averagers slow against the period, fast against any envelope;
  test surfaces perfectly absorbing or reflecting. Ensemble — deterministic; noisy-detector
  cells via `wavelab.measurement`. Ignored — sources; media (beyond the stated $n$-weighted
  irradiance); quantization beyond one aside; detector spectral response. Valid when —
  averaging windows cover many periods (at optical frequencies, always). Failure modes —
  reading instantaneous $\mathbf{S}$ as measured brightness; the vacuum formula in a medium
  without $n$; adding *intensities* of coherent sources (23's error).
- **Epistemic classification:** Poynting's theorem — `theorem` (derived in full); the
  identification of $u$ and $\mathbf{S}$ as *the* density and flux — `model-assumption` (the
  boxed one: only the combination is fixed by Maxwell; the standard split is a choice, stated
  honestly); $\langle\cos^2\rangle = \tfrac12$ and equipartition — `theorem`; irradiance —
  `definition`; $\mathbf{g} = \mathbf{S}/c^2$ — `theorem`, stated with proof deferred; the
  fitted $I \propto E_0^{2.00}$ — `numerical-observation`.
- **Misconceptions:** NEW `amplitude-doubles-intensity` — "Doubling a wave's field amplitude
  doubles its brightness." Falsifier: sweep $E_0$ over a decade, measure the time-averaged
  $|\mathbf{S}|$, log-log slope $2.00 \pm$ uncertainty via `validation.scaling_exponent` —
  brightness quadruples. Distractor: `Q-15-2`'s "twice as bright". (Registry gains this id.)
- **Glossary terms:** `irradiance` (עוצמת קרינה — usage note: the course says "intensity"
  informally, `irradiance` in definitions; `he_reject` candidate: אינטנסיביות),
  `radiation-pressure` (לחץ קרינה). `poynting-vector` (וקטור פוינטינג) and `equipartition`
  (חלוקה שווה של אנרגיה — this plan's wording, taken as proposed) were deposited by
  `09-wave-energy`, the first module in teaching order whose prose needs them (part-03 §5.2,
  as-built deviation 2); this module cites both.
- **Interactive controls and simulations:** energy dashboard ($E_0$, $\lambda$,
  averaging-window sliders; four panels); calibration card (source presets, live
  $I \leftrightarrow E_0$); solar-sail toy (area, mass, reflectivity; velocity vs time against
  a gravity-only twin).
- **Virtual lab outline** (`notebooks/en/labs/15-em-energy.ipynb`): (1) watch
  $|\mathbf{S}(t)|$ pulse at $2\omega$, converge the running average to the exact half;
  (2) the $E_0$ sweep — slope $2.00 \pm \sigma$ (the falsifier as measurement);
  (3) equipartition cell, pointwise; (4) calibration table: sunlight, laser pointer, phone
  screen, Wi-Fi — compute $E_0$ for each and order them; (5) *measurement:* a chopped beam
  read by a noisy detector (seeded) — $I \pm \sigma$ propagated to $E_0 \pm \sigma$ via
  `amplitude_from_intensity`; (6) solar-sail integration, $\Delta v$/day vs the closed
  estimate.
- **Real-experiment counterpart:** a phone light-meter app (lux) on the sun, a lamp, and a
  laser spot — imported readings converted order-of-magnitude to W/m², with the
  photometric-vs-radiometric caveat in one honest sentence. The Crookes radiometer appears as
  a cautionary paragraph: it spins the wrong way (thermal creep, not radiation pressure).
- **Media assets** (`render_poynting.py`): (a) plane wave with $\mathbf{S}$ arrows pulsing at
  $2\omega$ beside a steady $\langle\mathbf{S}\rangle$ bar — instantaneous vs average in one
  shot; (b) solar sail: photon stream, slow velocity build against a gravity-only twin.
- **Quiz bank outline:** `Q-15-1` numeric — $E_0$ from sunlight's $I$ (OBJ-15-4); `Q-15-2` MC
  — doubling $E_0$ (OBJ-15-3; distractor `amplitude-doubles-intensity`); `Q-15-3` MC — the
  electric/magnetic split (OBJ-15-2); `Q-15-4` numeric — force of full sunlight on a given
  mirror (OBJ-15-5); `Q-15-5` MC — $\mathbf{S}$ direction from a field snapshot (OBJ-15-1);
  `Q-15-6` free — where the $\tfrac12$ comes from and where it reappears (OBJ-15-3).
- **Problem set outline:** analytical — Poynting's theorem with the
  $-\mathbf{J}\cdot\mathbf{E}$ source term restored; equipartition from the triad; averaging
  over non-integer periods (error vs window length); inverse-square from flux through spheres.
  Computational — detector-window study, error envelope $\propto 1/N$; sail trajectory vs
  loading. Challenge — comet tails: pressure vs gravity as a function of grain radius
  (gravity $\propto r^3$, pressure $\propto r^2$); find the blow-away size for icy grains.
- **Runtime budget:** closed forms on $\le 4096$-point grids; sail integration $\le 10^5$
  Euler steps once; dashboard $\le 300$ frames — all sub-second in Pyodide.
- **Validation gates:** standard set with `--module 15-em-energy`; the `poynting`,
  `intensity_from_amplitude` / `amplitude_from_intensity`, `radiation_pressure`, and
  energy-flux-consistency tests (§4) land here.
- **Open questions for the author:** the lux-vs-W/m² aside in core or advanced (recommend
  advanced — only the real-experiment cell needs it); whether the photon $p = E/c$ line stays
  (recommend yes, one sentence, no quantum detour); laser-pointer-vs-sunlight as hook or
  verify punchline (recommend hook — it makes the calibration table a payoff).

### 5.3 `16-light-in-matter` — Light in matter: the refractive index

- **Identity and scope:** notebook 5.4. The Lorentz-oscillator model: susceptibility, complex
  index $n + \ii\kappa$, absorption, normal and anomalous dispersion, Sellmeier/Cauchy, group
  index; frequency continuity at a boundary as kinematics. Deferred: reflection/transmission
  *amplitudes* → `18-fresnel`; Snell proper → `17-refraction`; scattering (blue sky) → one
  advanced paragraph; birefringence → part-07; gain media → `45-lasers`.
- **Prerequisites:** `02-damped-driven` (`oscillators.steady_state_response`, the Lorentzian,
  $Q$, steady state at the drive frequency); `14` / `15` (plane waves; intensity for
  Beer–Lambert); `12` / `13` (group velocity; the material trailer); `04` (the Lorentzian
  pair).
- **Learning objectives:**
  - `OBJ-16-1` — Model a bound electron as a damped driven oscillator forced by the wave's E
    field and derive chi(omega) = omega_p^2 / (omega0^2 - omega^2 - i gamma omega) with
    omega_p^2 = N e^2 / (eps0 m_e).
  - `OBJ-16-2` — Obtain the complex index n + i kappa from n^2 = 1 + chi, read off the phase
    velocity c/n and the attenuation, and explain why the plus sign is forced by the
    e^(-i omega t) convention.
  - `OBJ-16-3` — Identify normal and anomalous dispersion on an n(omega) curve and locate the
    absorption band of width gamma where kappa peaks.
  - `OBJ-16-4` — Show that frequency is continuous across a boundary while the wavelength
    shortens to lambda0/n, and refute "light changes frequency in glass" by
    crest-arrival-rate reasoning.
  - `OBJ-16-5` — Use the Sellmeier equation as the transparent-region limit of the Lorentz
    model and fit it to noisy n(lambda) data with uncertainties.
  - `OBJ-16-6` — Compute the group index n_g = n + omega dn/domega, and connect material
    dispersion to pulse spreading (modules 12-13) and fiber dispersion (module 47).
- **Mathematical background:** has — the complex driven-oscillator solution (02), principal
  complex square roots, the Lorentzian (02, 04); introduced here — a *complex* refractive
  index carrying propagation and decay in one object (02's "loss is the imaginary part", now
  in space instead of time), susceptibility as per-volume response.
- **Physical intuition goals:** (1) glass slows light because its electrons are driven *below*
  resonance and respond in phase — predictable from 02's phase curve before any algebra;
  (2) blue bends more than red because the visible sits below a UV resonance — and the
  student can say when the opposite ("anomalous") happens; (3) the crest arrival rate cannot
  change at a boundary — so colour is frequency, and a red fin looks grey at depth because of
  *absorption*; (4) X-rays see every electron as above-resonance: $n < 1$ — X-ray telescopes
  graze.
- **Section skeleton seeds:**
  - *puzzle:* a prism is colourless glass, yet it paints a spectrum — so $n$ depends on
    frequency; ten metres down, a red fin looks grey — so water eats red. Boxed: what,
    microscopically, does matter *do* to light that slows it, sorts it by colour, and
    swallows some of it — and can one model do all three? (The kept secret: module 02 with
    charge.)
  - *predict:* (1) light enters glass — which of {speed, wavelength, frequency, colour}
    change? commit each (targets registry `frequency-changes-in-medium`); (2) an electron
    bound at $\wnat$ driven far below — in phase or opposed, and what does that make $n$?
    (3) is $n$ always greater than 1? (the X-ray surprise); (4) blue bends more than red in
    every glass — law or habit?
  - *explore:* the Lorentz explorer — module 02's response explorer wearing EM clothes:
    sliders $\wnat$, $\gamma$, $N$; panels $\chi'$, $\chi''$, then $n(\omega)$,
    $\kappa(\omega)$ with normal/anomalous regions shaded live; a wavefront view — plane wave
    crossing into the medium, wavelength visibly shortening, a crest counter ticking at a
    probe on *each* side (the falsifier built into explore); Sellmeier playground — BK7 /
    fused silica / water presets, $n(\lambda)$ across the visible, live prism-deviation fan.
  - *derive:* bound electron: $m_e\ddot{x} + m_e\gamma\dot{x} + m_e\wnat^2 x = q_e E_0
    e^{-\ii\omega t}$ — module 02's equation with the force renamed; the displacement is
    `oscillators.steady_state_response` verbatim → $P = N q_e x = \epsilon_0\chi E$ →
    $\chi(\omega)$ → wave equation in the medium ⇒ $k = n\omega/c$, $n^2 = 1 + \chi$; dilute
    $n \approx 1 + \chi/2$ → the sign: with $e^{-\ii\omega t}$, $\Imag\chi > 0$, so the
    physical branch is $n + \ii\kappa$ with $\kappa > 0$ and the wave *decays* — the lint
    rejects $n - \ii\kappa$ because under this convention it would be gain; $e^{+\ii\omega t}$
    texts flip it, and the conversion is stated once → $\alpha = 4\pi\kappa/\lambda_0$,
    Beer–Lambert → reading the curve: normal-dispersion flanks, the $\gamma$-wide band where
    $\kappa$ is a Lorentzian (02's curve, third appearance) and $dn/d\omega < 0$ (anomalous),
    $n < 1$ above resonance → group index → frequency continuity: a linear medium in steady
    state answers *at the drive frequency* (02's lesson), and boundary matching at all times
    forces one $\omega$; $\lambda = \lambda_0/n$ → transparent limit: Sellmeier, then Cauchy.
  - *verify:* `refractive_index` vs `sellmeier` in the transparent window; $\kappa(\omega)$
    overlaid on the scaled module-02 `power_absorbed` curve — the same machine, measured; the
    crest-count experiment: frequencies equal to machine precision on both sides while the
    wavelength ratio fits $n$ (the `numerical-observation` box); `group_index` vs the arrival
    time of a `waves.gaussian_packet` sent through `waves.propagate_dispersive`; the
    $\gamma \to 0$ limit against `waves.omega_material_sketch` (part-04's trailer redeemed).
  - *transfer:* `17-refraction` — next module: Snell is wavelength-shortening plus geometry;
    `24-thin-films` — $n(\lambda)$ becomes colour; `26-fabry-perot` — the Lorentzian line yet
    again; `37-aberrations` — chromatic aberration is Sellmeier inside a lens; `47-fibers` —
    group index → pulse spreading and the telecom zero-dispersion window; `45-lasers` —
    pumped media flip the sign of $\kappa$: gain; backward to `13-dispersion` — the material
    $\omega(k)$ the sketch promised now exists, with loss.
  - *quiz:* what changes in glass (registry distractor); wavelength-in-medium numerics;
    reading $n$/$\kappa$ curves; penetration depth; whether $n$ is one number; group-index
    numerics; the sign of $\kappa$ under the course convention.
  - *explain:* why a linear medium cannot answer at a frequency it is not asked (and what
    "nonlinear optics" therefore means — one sentence, seed for `51-nonlinear-optics`); why
    colour does not change underwater though everything looks blue-green; the Lorentz
    dictionary in the student's own words; why $n - \ii\kappa$ is wrong *here* and right in
    an engineering text.
  - *advanced:* $v_p > c$ above resonance, $v_g > c$ inside the anomalous band — why neither
    carries a signal (front velocity, Sommerfeld–Brillouin pointer; 13's precedent, 19
    ahead); X-ray optics: $n < 1$, total external reflection, grazing telescopes; the same
    driven dipole *re-radiating* is scattering — blue sky and red sunset, $\omega^4$ stated
    not derived; local-field (Clausius–Mossotti) in one honest line: this model is dilute,
    glass is not, the shape survives anyway. Safe to skip.
- **Core derivations:** (1) $\chi(\omega) = \dfrac{\omega_p^2}{\wnat^2 - \omega^2 -
  \ii\gamma\omega}$, $\omega_p^2 = \dfrac{N q_e^2}{\epsilon_0 m_e}$ — the denominator is
  literally module 02's; the susceptibility is $(N q_e^2/\epsilon_0)$ times the mechanical
  response per unit force. (2) $n^2 = 1 + \chi$; dilute $n \approx 1 + \chi/2$, so
  $n - 1 \propto \chi'$ and $\kappa \propto \chi''$ — dispersion and absorption are the real
  and imaginary parts of one response. (3) $e^{\ii((n+\ii\kappa)\omega z/c - \omega t)} =
  e^{-\kappa\omega z/c}\,e^{\ii(n\omega z/c - \omega t)}$: phase velocity $c/n$, intensity
  decay $\alpha = 2\kappa\omega/c = 4\pi\kappa/\lambda_0$. (4) Near resonance
  $\chi'' \approx \dfrac{\omega_p^2}{2\wnat}\,\dfrac{\gamma/2}{(\omega - \wnat)^2 +
  (\gamma/2)^2}$ — the Lorentzian of FWHM $\gamma$, matching 02's power curve and 04's pair.
  (5) Frequency continuity: linear steady state answers at the drive frequency; matching at a
  boundary for all $t$ forces equal $\omega$; then $\lambda = \lambda_0/n$. (6) $n_g = n +
  \omega\,dn/d\omega$; in the normal window $n_g > n$ (pulses lag phase fronts); Sellmeier
  $n^2 = 1 + \sum_i B_i\lambda^2/(\lambda^2 - C_i)$ from real multi-resonance $\chi$ far from
  all poles; Cauchy $n \approx A + B/\lambda^2$ as its long-wavelength expansion.
- **Model specification draft:** System — a dilute medium of $N$ identical bound electrons
  per volume (resonance $\wnat$, damping $\gamma$) in a monochromatic plane wave; observables
  $\chi$, $n$, $\kappa$, $\alpha$, $n_g$. Dynamics — each electron a module-02 damped driven
  oscillator forced by the applied field (local = applied: dilute); response linear. Boundary
  — unbounded homogeneous medium; the interface enters only as the frequency-continuity
  argument, no amplitude matching (that is 18). Ensemble — deterministic; the Sellmeier lab
  adds seeded noise. Ignored — local-field corrections; magnetic response; multiple species
  beyond summed Sellmeier terms; nonlinearity; the quantum origin of $\wnat, \gamma$
  (empirical parameters here). Valid when — dilute or read qualitatively; fields weak.
  Failure modes — Sellmeier inside an absorption band (poles); quantitative claims for dense
  media; $v_p > c$ read as causality violation; oscillator parameters taken as literal
  mechanics (they encode quantum transitions, and the page says so).
- **Epistemic classification:** the bound-electron oscillator — `model-assumption` (THE boxed
  one: electrons are not on springs; the model is kept because the *shape* of $n(\omega)$ is
  right, and quantum mechanics later re-derives the same form with oscillator strengths);
  $n^2 = 1 + \chi$ — `theorem` (within the model plus Maxwell); frequency continuity —
  `theorem`; the $n + \ii\kappa$ sign under $e^{-\ii\omega t}$ — convention plus `theorem`;
  Sellmeier/Cauchy — `approximation` (boxed, validity window stated); measured crest-rate
  equality — `numerical-observation`; what sets a real atom's $\gamma$ — `open-question`
  pointer (radiative vs collisional; beyond the course).
- **Misconceptions:** registry `frequency-changes-in-medium` (pending; listed under the
  obsolete id `06-em-waves` — **re-pointed to this module and addressed here** per the README
  conflict log; the one-line `assigned_module` edit lands when this module is built).
  Falsifying experiment: simulated wavefronts crossing an air/glass interface with a crest
  counter on each side — the wavelength visibly shortens while the crest arrival rate at any
  fixed point is *identical* on both sides to machine precision; hence colour does not change
  underwater, and what looks like colour change is absorption. Distractor: `Q-16-1`'s option
  "the frequency drops by a factor $n$ inside the glass". NEW `index-is-one-number` — "A
  material's refractive index is a single fixed number." Falsifier: the Sellmeier lab's
  fitted BK7 curve — $n$ sweeps ~1.51 to ~1.53 across the visible, and the prism fan exists
  *because* no single number suffices; the same fit feeds 37's chromatic aberration.
  Distractor: `Q-16-5`'s "$n = 1.5$ for glass at every colour".
- **Glossary terms:** `refractive-index` (מקדם שבירה), `extinction-coefficient` (מקדם הכחדה —
  for $\kappa$), `susceptibility` (היענות חשמלית; `he_reject` candidate: סוספטיביליות),
  `plasma-frequency` (תדר הפלזמה), `absorption-coefficient` (מקדם בליעה),
  `anomalous-dispersion` (נפיצה אנומלית — `dispersion` itself is part-04's deposit, cited),
  `sellmeier-equation` (משוואת זלמאייר), `group-index` (מקדם שבירה קבוצתי).
- **Interactive controls and simulations:** Lorentz explorer ($\wnat$, $\gamma$, $N$ sliders;
  $\chi'/\chi''$ and $n/\kappa$ panels, shaded regimes); wavefront-crossing view (normal
  incidence, $n$ slider, twin crest counters, a $\kappa$ toggle adding visible decay);
  Sellmeier playground (material presets, wavelength band, prism fan); group-delay racer — a
  pulse and a phase-front marker racing through 1 m of glass, arrival clock in femtoseconds.
- **Virtual lab outline** (`notebooks/en/labs/16-light-in-matter.ipynb`): (1) sweep $\omega$
  across the resonance, record $\chi$, build $n + \ii\kappa$; overlay module 02's scaled
  response — the "same machine" cell; (2) the crest-count experiment: two probes, report
  $f_{\text{in}}/f_{\text{out}} = 1.0000 \pm \sigma$ and $\lambda_0/\lambda = n \pm \sigma$
  (the falsifier as a measurement); (3) absorption: propagate through $\kappa > 0$, fit the
  intensity decay, compare fitted $\alpha$ with $4\pi\kappa/\lambda_0$; (4) *measurement:*
  fit Sellmeier coefficients to seeded noisy BK7 $n(\lambda)$ data (`measurement.add_noise`),
  report $B_i, C_i \pm$ uncertainties with residuals (the measurement-culture headline), then
  compare a Cauchy fit's residuals; (5) group index: send a `waves.gaussian_packet` through
  the fitted glass via `waves.propagate_dispersive`, arrival vs $c/n_g$.
- **Real-experiment counterpart:** measure $n$ of water with a laser pointer and a
  rectangular tank: protractor angles in and out at several incidences, imported as a CSV of
  angle pairs → fitted $n \pm \sigma$. (Snell is *used* one module early as a black-box
  protractor fact, flagged as such — 17 derives it; noted in §8.)
- **Media assets** (`render_light_matter.py`): (a) the money shot — wavefronts crossing an
  air/glass interface: crests compress inside while probe dots on both sides blink in exact
  synchrony (frequency continuity made visible, no text needed); (b) white light through a
  Sellmeier prism — a fan of colours whose angular spread *is* the $n(\lambda)$ curve;
  (c) $n/\kappa$ curves morphing as $\gamma$ and $N$ sweep, the absorption band breathing.
- **Quiz bank outline:** `Q-16-1` MC — what changes entering glass (OBJ-16-4; distractor
  `frequency-changes-in-medium`); `Q-16-2` numeric — $\lambda$ in glass from $\lambda_0$, $n$
  (OBJ-16-4); `Q-16-3` MC — identify the anomalous region and absorption band on a plotted
  $n, \kappa$ pair (OBJ-16-3); `Q-16-4` numeric — penetration depth $1/\alpha$ from $\kappa$
  and $\lambda_0$ (OBJ-16-2); `Q-16-5` MC — is $n$ one number per material (OBJ-16-5;
  distractor `index-is-one-number`); `Q-16-6` numeric — $n_g$ from tabulated $n(\lambda)$
  (OBJ-16-6); `Q-16-7` MC — which sign of the imaginary part means absorption under
  $e^{-\ii\omega t}$, and what the other sign would mean (OBJ-16-2); `Q-16-8` free — the
  Lorentz dictionary: map module 02's symbols onto this module's, term by term (OBJ-16-1).
- **Problem set outline:** analytical — derive $\chi$ and the dilute $n \approx 1 + \chi/2$;
  $\chi''$ is a Lorentzian of FWHM $\gamma$ near resonance; Cauchy from a one-term Sellmeier;
  frequency continuity from boundary matching at all times. Computational — error map of the
  dilute approximation vs $N$ (where $\sqrt{1+\chi}$ and $1 + \chi/2$ part company);
  Sellmeier vs Cauchy residuals on one dataset. Challenge — a two-resonance glass (UV + IR):
  find the zero-dispersion wavelength where $dn_g/d\lambda = 0$, and connect it to why
  telecom fibers run near 1.3/1.55 μm (`47-fibers` seed).
- **Runtime budget:** closed-form $\chi$/$n$ on $\le 2048$-point frequency grids; wavefront
  animation on a $\le 4096$-point 1-D grid, $\le 300$ frames; Sellmeier least squares on ~50
  points; one `propagate_dispersive` call at $\le 2^{12}$ samples — all seconds in Pyodide.
- **Validation gates:** standard set with `--module 16-light-in-matter`; the
  `lorentz_susceptibility`, `refractive_index`, `sellmeier`, `absorption_coefficient`,
  `group_index` tests and the cross-part `omega_material_sketch` limit (§4) land here —
  part-06's plan will cite `refractive_index` as given.
- **Open questions for the author:** blue-sky scattering in transfer or advanced (recommend
  advanced — the $\omega^4$ is unearned in core); whether "plasma frequency" is named in core
  given the medium is glass (recommend yes, one sentence — 45/46 reuse it); whether the
  water-tank experiment's early use of Snell is acceptable (recommend yes with the black-box
  flag, since 17 follows immediately); crest counters in explore or verify only (recommend
  explore — predict question 1 should be checkable within a minute of opening the lab).

## 6. Part-level assessment and capstone hooks

- The part's durable deliverables: the triad picture (VI–VII), the workhorse identity
  $\langle\cos^2\rangle = \tfrac12$ with $I = \tfrac12 c\epsilon_0 n E_0^2$ (every intensity
  formula in VIII–XI), and `em.refractive_index` / `em.sellmeier` as the material database of
  parts VI, X, and XII.
- Capstone §35.4 (optical communication) consumes `group_index` and zero-dispersion reasoning
  directly; §35.3 (grating spectrometer) inherits the prism-vs-grating dispersion contrast (a
  designed exam theme); §35.1 (computational telescope) uses irradiance calibration in its
  signal budgets.
- Cross-module synthesis problem (lives with `16-light-in-matter-problems.md`): from two
  benchtop constants to a prism spectrum — compute $c$ from $\mu_0, \epsilon_0$ (14), convert
  a source's irradiance to $E_0$ (15), trace three wavelengths through a Sellmeier prism and
  predict the fan angles (16). One problem touching the whole part.
- Exam themes: triad quickies (given two of E/B/k, produce the third); order-of-magnitude
  $E_0$ from irradiance; reading $n/\kappa$ curves cold; sign-convention hygiene
  ($n + \ii\kappa$, $e^{-\ii\omega t}$) under time pressure; crest-counting in words.

## 7. Build order and validation gates

Build `14-em-waves` first (everything downstream consumes `plane_wave_fields` and the triad),
then `15-em-energy` (consumes 14; supplies intensity for 16's Beer–Lambert), then
`16-light-in-matter`. Cross-part dependencies: 16 requires part-01's `02-damped-driven` as
built (`oscillators.steady_state_response` is its engine) and part-04's
`waves.propagate_dispersive` / `gaussian_packet` / `omega_material_sketch` — all earlier in id
order, so the teaching sequence already guarantees the build sequence.

`em.py` lands in three stages, tests travelling with their module (§5 gates): with 14 —
`plane_wave_fields`, `energy_densities`, Maxwell residuals; with 15 — `poynting`,
`intensity_from_amplitude` / `amplitude_from_intensity`, `radiation_pressure`, energy-flux
consistency; with 16 — `lorentz_susceptibility`, `refractive_index`, `sellmeier`,
`absorption_coefficient`, `group_index`, the cross-part `omega_material_sketch` limit. The
file-level docstring model spec (§4) lands complete with 14.

Registry work: with 14, deposit NEW `em-wave-on-a-line`; with 15, NEW
`amplitude-doubles-intensity`; with 16, NEW `index-is-one-number` AND the conflict-log
re-pointing of `frequency-changes-in-medium` (`assigned_module: 06-em-waves` →
`16-light-in-matter`, flipped to `addressed` — the one-line edit the README defers to build
time). Glossary deposits per module (§5 lists); `energy-density`, `energy-flux`, and
`dispersion` are cited, not re-deposited.

Per module, the standard four gates (README): `check_modelspec.py`, `check_assessment.py`,
`pytest tests/physics -k <topic>`, `validate_all.py`.

## 8. Deviations from the master plan

- **Merge (5.1 + 5.2 → `14-em-waves`):** the derivation and the solution's geometry are one
  argument — transversality and the triad fall out of substituting the plane wave into the
  equations just derived, and separately 5.2 is a picture with no derivation to stand on. The
  canonical map reserves the merged id; precedent `02-damped-driven` (README).
- **Scope expansion of 5.3:** the master plan's four lines become a full module: Poynting's
  theorem derived (not quoted), $\langle\cos^2\rangle = \tfrac12$ named as the course-wide
  workhorse identity with its forward declaration to Parts VIII–XI, the irradiance ↔
  amplitude calibration culture (sunlight ≈ 870 V/m), radiation pressure with solar-sail
  numbers as advanced material.
- **Scope expansion of 5.4:** the master plan's five bullets become the full
  Lorentz-oscillator treatment: $\chi$ built on `oscillators.steady_state_response` (module
  02 re-costumed, stated explicitly), the $n + \ii\kappa$ sign argued from the
  $e^{-\ii\omega t}$ convention, Sellmeier/Cauchy with a fitting lab, group index bridging
  12/13 → 47, and the frequency falsifier as a designed experiment.
- **Staging of the conceptual event:** §12 asks that $c = 1/\sqrt{\mu_0\epsilon_0}$ be "a
  major conceptual event"; this plan implements that as a measurement-culture experiment
  (Weber–Kohlrausch redone with uncertainties) plus the 2019-SI role inversion, rather than
  as prose emphasis alone.
- **Additions beyond §12:** the Hertz verification as puzzle/transfer material with the
  microwave-chocolate real experiment; the honest volume-filling triad visualization and the
  NEW `em-wave-on-a-line` misconception it targets; two further NEW registry entries
  (`amplitude-doubles-intensity`, `index-is-one-number`); the registry re-pointing of
  `frequency-changes-in-medium` claimed by 16 (README conflict log executed at build time).
- **Terminology:** "irradiance" adopted for the precise quantity with "intensity" as the
  working word (Hecht's distinction), noted once in 15; SI units throughout ($\mu = \mu_0$;
  no Gaussian units anywhere, matching `constants.py`).
- **Sequencing note (minor):** 16's real-experiment pairing uses Snell's law one module
  before 17 derives it — flagged in content as a black-box instrument, deliberately, so the
  part ends with a real measured $n$ in hand as 17 opens.
