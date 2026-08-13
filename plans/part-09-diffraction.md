# Part IX — Diffraction — Implementation Plan

> **Master plan:** §16 (Part IX). **Modules:** `28-huygens`, `29-fraunhofer`, `30-apertures`, `31-gratings`, `32-fresnel-diffraction`. **Status:** planned.
> Canonical numbering, invariants, and conflict log: [README.md](README.md).

## 1. Part overview and narrative arc

Diffraction is where the course's two halves fuse. Since `00-phasors` the course has run on
one arithmetic — oscillations add as arrows — and since `03-fourier-series` /
`04-fourier-transform` on one analysis — any signal is a sum of harmonics. Until now those
were two skills. In this part they become **one subject**: an aperture is a *continuum* of
secondary sources, the tip-to-tail polygon of arrows becomes an integral, and computing the
arrow sum for every direction at once *is* a Fourier transform. That sentence is a verbatim
promise from the built `00-phasors` page's transfer section; this part exists to keep it.
The master plan calls Part IX "one of the centerpiece sections of the course" (§16),
dedicates §30 to its textbook strategy and §31 to its pedagogical bet — that a student who
already owns $\operatorname{rect} \leftrightarrow \operatorname{sinc}$ should meet
single-slit diffraction as **recognition, not derivation**. Module 29 is built around that
moment; everything before it earns it, everything after it spends it.

The module order walks the two textbook routes of master plan §30 and shows they are the
same road. Module 28 is the **Hecht route**: Huygens–Fresnel wavelets summed numerically —
phasor polygons drawn over real geometry — *before any formula exists*. Its historical
centerpiece is the Poisson–Arago spot: Poisson derived the absurd bright spot behind a disk
to *refute* wave theory, Arago measured it, and the falsifying prediction confirmed instead
— the cleanest epistemology lesson the course owns, and one the student *simulates*.
Module 29 is the **Goodman route**: in the far field the wavelet integral collapses to
$U(\theta) \propto \mathcal{F}\{A(x)\}$, and the Part-0 pair zoo turns into light on a
screen. Module 30 makes the convolution theorem visible — the finite-width double slit is a
two-delta comb convolved with a rect, so its pattern is
$\cos^2 \times \operatorname{sinc}^2$, interference structure under a diffraction envelope,
with **missing orders** as a designed lab discovery — then the circular aperture delivers
the Airy pattern and the Rayleigh criterion. Module 31 industrialises the sum: $N$ slits,
sharpening as $1/N$, resolving power $R = mN$, and a virtual grating spectrometer seeding
capstone §35.3. Module 32 closes the ring: the angular-spectrum propagator — FFT, multiply
by $e^{\ii k_z z}$, inverse FFT — is *exact* scalar propagation at any distance and the
part's computational deliverable. With it the student watches one pattern morph from
aperture shadow through Fresnel ripples to far-field $\operatorname{sinc}^2$ as $z$ grows,
the Fresnel number $N_F = a^2/(\lambda z)$ narrating — and re-derives 28's Poisson spot by
an entirely different method, which agrees.

Relative to master plan §16 this plan deepens: 9.1 gains numerical-wavelets-first
discipline, Fresnel zones, and the Poisson–Arago simulation with its epistemology box;
9.2 + 9.3 gain the honest Fraunhofer condition (a Fresnel-number inequality, not "far
away"), the claimed registry misconception `narrow-slit-narrow-pattern` with a measured
$\Delta\theta \propto 1/a$ falsifier, and the uncertainty-principle reading of
slit-vs-spread (the Part-0 bandwidth theorem in space); 9.4 + 9.5 gain missing orders,
real-number Rayleigh applications (eye, Hubble, radio dish, §26.4's 10-mm telescope), and a
noisy two-point-resolution measurement; 9.6 gains the finite-vs-infinite phasor-sum
parallel with `26-fabry-perot`, the measured $1/N$ sharpening, the sodium-doublet
spectrometer lab, and the CD/DVD track-pitch experiment; 9.7 gains the angular-spectrum
method (Goodman's, in place of direct Fresnel-integral quadrature), explicit sampling
constraints as hard validity conditions, knife-edge/Cornu validation, and the
arbitrary-aperture draw/upload playground of master plan §30.

Seeds planted forward: the Airy disk of 30 **is** the point-spread function that
`40-psf-otf` will convolve scenes with — Part XI's imaging theory is this part plus a lens;
`39-fourier-lens` relocates 29's far field to a focal plane; `43-gaussian-beams` inherits
the confinement-spread law as beam divergence; `50-holography` records what this part
computes; `53-computational-imaging` inverts it. Capstones §35.1, §35.3, and §35.5 all
stand on `diffraction.py`. Backward, the part pays three standing debts: `00-phasors`'
polygon promise (28), part-08's deferred finite-width double slit (30 — the handoff logged
in part-08 §8), and `04-fourier-transform`'s pair zoo, finally drawn in light.

## 2. Position in the course

- **Requires:**
  - `00-phasors`: the superposition theorem, tip-to-tail addition (`phasors.superpose`,
    `phasors.resultant`), the random-phase walk (`phasors.random_phasor_sum`) — 28's
    wavelet polygon and 32's speckle test both trace to it.
  - `04-fourier-transform`: the pair zoo — `fourier.rect_pulse` ↔ `fourier.sinc_spectrum`,
    `fourier.gaussian_pulse` ↔ `fourier.gaussian_spectrum` — the convolution theorem
    (`fourier.convolve`), scaled FFTs (`fourier.spectrum`, forward sign
    $e^{-\ii\omega t}$), and the bandwidth theorem via `fourier.rms_widths`; 32's
    propagator generalises `spectrum` to two spatial dimensions.
  - `23-interference`: the two-beam law and Young geometry (`interference.young_pattern`,
    `interference.fringe_spacing`, `interference.two_beam_intensity`) — 30's cos² factor
    *is* Young's pattern, cited not re-derived.
  - `26-fabry-perot`: the infinite geometric phasor sum (`interference.airy_transmission`,
    `interference.finesse`) — 31's finite $N$-slit sum is its sibling.
  - `17-refraction`: the phase-matching argument (equal $\omega$, $k_\parallel$ — part-06
    flags it "reused verbatim in 31"); a periodic structure absorbs $k_\parallel$ in lumps
    of $2\pi/d$, which *is* the grating equation.
  - `19-evanescent`: the imaginary-$k_z$ decaying branch and `interfaces.penetration_depth`
    — 32's evanescent angular-spectrum components are the same mathematics, cited by name.
  - `15-em-energy`: intensity as cycle-averaged flux, $I \propto |\hat{U}|^2$;
    `16-light-in-matter`: $\lambda/n$ for immersed-system questions.
- **Feeds:**
  - `38-spatial-frequencies` / `39-fourier-lens` / `40-psf-otf` / `41-imaging-coherence` /
    `42-4f-processor`: Part XI is this part plus lenses — 29's transform relation becomes
    the focal-plane theorem, 30's Airy disk the PSF, 32's propagator the imaging engine
    (parallel part; referenced by module id only).
  - `43-gaussian-beams`: divergence $\theta \approx \lambda/(\pi w_0)$ is 29's
    confinement-spread law for a Gaussian aperture.
  - `50-holography` / `53-computational-imaging`: recording and inverting diffraction.
  - Capstones §35.1, §35.3, §35.5 (see §6).
- **Explicitly not assumed:** vector diffraction or polarization (scalar theory
  throughout, said in every model spec); Kirchhoff/Rayleigh–Sommerfeld rigour (cited as
  the resolution of 28's honesty gaps, never derived); lenses and imaging (Part X/XI —
  every pattern here lives on a physical screen at distance $z$); the "spatial frequency"
  *vocabulary* (Part XI's; here $k_x = k\sin\theta$ is just a direction); Bessel-function
  theory (the $J_1$ result stated honestly, derived only in 30's advanced); partial
  coherence (fully coherent illumination; one sentence per module points to
  `27-coherence`).

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|
| `28-huygens` | `content/en/diffraction/28-huygens.md` | Huygens–Fresnel: diffraction from wavelets | 9.1 | Hecht, Diffraction — preliminary considerations & Huygens–Fresnel principle | planned |
| `29-fraunhofer` | `content/en/diffraction/29-fraunhofer.md` | Fraunhofer diffraction: the far field is a Fourier transform | 9.2 + 9.3 | Hecht, Fraunhofer diffraction — single slit; Goodman, Fourier-transform view (the §30 bridge) | planned |
| `30-apertures` | `content/en/diffraction/30-apertures.md` | Apertures: envelopes, the Airy pattern, and resolution | 9.4 + 9.5 | Hecht, Fraunhofer diffraction — double slit, circular apertures, resolution | planned |
| `31-gratings` | `content/en/diffraction/31-gratings.md` | Diffraction gratings and spectroscopy | 9.6 | Hecht, Fraunhofer diffraction — many slits & gratings | planned |
| `32-fresnel-diffraction` | `content/en/diffraction/32-fresnel-diffraction.md` | Fresnel diffraction: propagating the near field | 9.7 | Hecht, Fresnel diffraction; Goodman, angular-spectrum propagation | planned |

## 4. Shared infrastructure for this part

**`src/wavelab` — existing used:** `phasors.superpose` / `resultant` (28's polygons),
`phasors.random_phasor_sum` (32's speckle seed test); `fourier.spectrum` (sign and scaling
precedent for the spatial FFT), `fourier.rect_pulse` / `sinc_spectrum` / `gaussian_pulse` /
`gaussian_spectrum` (29's zoo overlays), `fourier.convolve` (30's convolution-theorem
demo), `fourier.rms_widths` (29's uncertainty product in space);
`interference.young_pattern` / `fringe_spacing` / `two_beam_intensity` (30's cos² factor),
`interference.airy_transmission` / `finesse` (31's comparison);
`interfaces.penetration_depth` / `evanescent_field` (32's evanescent cross-check, by name —
owned by part-06); `measurement.add_noise` / `fit_cosine` (all five labs);
`validation.scaling_exponent` / `convergence_study` / `seed_study` / `relative_error`.

**`src/wavelab` — new: `diffraction.py`** (introduced and owned by this part; README
ownership table — serves 28–32, FFT Fraunhofer + angular-spectrum propagator, and the
course's first 2-D FFT machinery, built on `fourier.py`'s conventions). Docstring model
spec:

- **System:** scalar monochromatic optical fields — complex amplitudes sampled on 1-D or
  2-D grids — passing through planar apertures and propagating through free space to
  screens or later planes.
- **Dynamics:** stationary propagation only; the time factor $e^{-\ii\omega t}$ is divided
  out and fields evolve in $z$, not $t$ (propagator phase $e^{\ii k_z z}$).
- **Boundary:** apertures are infinitely thin transmission masks in one plane (Kirchhoff
  screen idealisation); the surrounding screen is perfectly opaque; free space homogeneous
  beyond the mask.
- **Ensemble:** deterministic and fully coherent; callers add noise via
  `wavelab.measurement`; partial coherence belongs to `interference.py` / part XI.
- **Ignored:** polarization and all vector effects (scalar approximation); exact boundary
  fields inside the aperture (transmission-mask model); backward-propagating waves;
  material dispersion.
- **Valid when:** feature sizes ≳ $\lambda$ (scalar theory's honest edge); angles where
  the chosen tier applies — angular spectrum exact for any $z$, Fresnel paraxial,
  Fraunhofer additionally $N_F \ll 1$; grids satisfy `propagation_sampling_ok`.
- **Failure modes:** sub-wavelength features trusted quantitatively (vector regime);
  Fraunhofer formulas at $N_F \gtrsim 1$; aliased quadratic phase read as physics (rings
  that move with grid size); wraparound ghosts from missing zero padding; the growing
  evanescent branch.

Function-level sketch (signatures + contracts; the four **course-fixed** shared names —
`fraunhofer_pattern`, `angular_spectrum_propagate`, `airy_radius`, `rayleigh_criterion` —
are cited by parts X–XII and must not drift):

```python
# aperture builders — sampled transmission in [0, 1] on the caller's grid
slit(x, a) -> A                          # rect(x/a): 1 for |x| <= a/2, else 0
double_slit(x, a, d) -> A                # two width-a slits at centers ±d/2 — the part-08 handoff object
circular(x, y, diameter) -> A            # 2-D: 1 inside the disk (meshgrid convention)
disk(x, y, diameter) -> A                # opaque disk, 1 - circular — the Poisson–Arago obstacle
grating(x, d, n_slits, a) -> A           # n_slits width-a slits at pitch d (truncated comb ⊗ rect)
from_image(image, extent) -> (A, dx)     # grayscale array/file -> transmission mask + grid step (32's playground)

# far field and analytic references
fraunhofer_pattern(aperture, dx, lam, z) -> (coords, U)
                                         # far-field complex amplitude via zero-padded FFT of the sampled
                                         # aperture; spatial kernel e^{-i k_x x} (the fourier.spectrum sign);
                                         # returns screen coordinates at distance z (angles for z=None);
                                         # 1-D and 2-D; intensity is |U|^2
sinc_intensity(theta, a, lam) -> I       # I0 sinc^2(pi a sin(theta)/lam), sinc(x) = sin(x)/x — the analytic slit
double_slit_intensity(theta, a, d, lam) -> I
                                         # cos^2(pi d sin(theta)/lam) * sinc^2(pi a sin(theta)/lam) — 30's law
n_slit_intensity(theta, d, a, lam, n) -> I
                                         # [sin(n delta/2)/sin(delta/2)]^2 * envelope, delta = 2 pi d sin(theta)/lam;
                                         # n=2 reduces to double_slit_intensity exactly
airy_pattern(theta, lam, diameter) -> I  # I0 [2 J1(v)/v]^2, v = pi D sin(theta)/lam; J1 via scipy.special
airy_radius(lam, diameter, focal_or_distance) -> r
                                         # first-zero radius on a screen: 1.22 lam/D * distance (small angle)
rayleigh_criterion(lam, diameter) -> theta
                                         # 1.22 lam / D [rad] — the angular resolution limit

# gratings
grating_orders(d, lam) -> (m, theta)     # all propagating orders |m| <= d/lam with their angles
angular_dispersion(d, m, theta) -> dth_dlam    # m / (d cos(theta)) [rad/m]
resolving_power(m, n_slits) -> R         # m * N = lambda / Delta lambda (Rayleigh-resolved doublet)

# propagation
fresnel_number(a, lam, z) -> NF          # a^2/(lam z), a = half-width or radius; the regime classifier
wavelet_sum(src_x, src_amp, obs_x, z, lam) -> U
                                         # direct Huygens sum of sampled secondary wavelets e^{i k r}/sqrt(r)
                                         # (2-D line-aperture geometry; obliquity documented) — 28's engine,
                                         # transparent and O(N_src * N_obs)
angular_spectrum_propagate(field, dx, lam, z) -> field_z
                                         # exact scalar propagator: FFT -> multiply exp(i k_z z) with
                                         # k_z = sqrt(k^2 - k_x^2 [- k_y^2]), evanescent branch
                                         # k_z = i sqrt(k_x^2 + k_y^2 - k^2) (decaying, never growing) ->
                                         # inverse FFT; zero-padded; 1-D and 2-D; refuses grids that fail
                                         # propagation_sampling_ok
propagation_sampling_ok(n_grid, dx, lam, z) -> bool
                                         # 32's hard constraints: transfer-function phase unaliased across
                                         # the band, >= 2x zero padding against wraparound
fresnel_integrals(w) -> (C, S)           # C(w), S(w) — the Cornu spiral's coordinates (quadrature, vectorized)
knife_edge_intensity(x, lam, z) -> I     # analytic Fresnel edge: I/I0 = ((C+1/2)^2 + (S+1/2)^2)/2,
                                         # w = x sqrt(2/(lam z)); the propagator's validation target
```

Convention notes carried in the docstring: $\operatorname{sinc}(x) = \sin x / x$
(unnormalised, matching `fourier.sinc_spectrum` and Hecht's $\beta$ notation —
`numpy.sinc` is the *normalised* $\sin(\pi x)/(\pi x)$ and is never used directly);
propagator phase $e^{\ii k_z z}$ under $e^{-\ii\omega t}$ so forward waves are
$e^{\ii(k_z z - \omega t)}$ and the evanescent branch decays.

**`tests/physics/` additions:**

- *limits:* `fraunhofer_pattern(slit(...))` ≡ `sinc_intensity` after padding (`<1e-10`);
  `fraunhofer_pattern(circular(...))` zeros at $1.220,\ 2.233,\ 3.238\ \lambda/D$ (the
  $J_1$ zeros $3.832, 7.016, 10.174$ over $\pi$); `n_slit_intensity(n=2)` ≡
  `double_slit_intensity`, whose cos² factor ≡ `interference.young_pattern`'s fringes
  under a flat envelope; `angular_spectrum_propagate(field, dx, lam, 0)` ≡ identity;
  angular spectrum at $N_F < 10^{-2}$ ≡ `fraunhofer_pattern` (rescaled);
  `grating_orders` count = $2\lfloor d/\lambda\rfloor + 1$.
- *convergence:* `angular_spectrum_propagate` vs `knife_edge_intensity` — max error falls
  under grid refinement at the documented rate (`validation.convergence_study`);
  `wavelet_sum` → Fraunhofer as wavelet density grows (error vs $N_{\rm src}$ measured);
  paraxial (Fresnel) transfer function vs exact $k_z$ — error grows as $\theta^2$.
- *conservation:* Parseval through `angular_spectrum_propagate` — energy in propagating
  components exactly conserved at every $z$ (evanescent caveat: energy in $|k_x| > k$
  components decays; the test documents the split rather than pretending totals survive
  sub-$\lambda$ features); screen-integrated far-field intensity = transmitted aperture
  energy (Parseval on `fraunhofer_pattern`).
- *scaling:* fitted $\Delta\theta \propto a^{\alpha}$, $\alpha = -1$, via
  `validation.scaling_exponent` (the `narrow-slit-narrow-pattern` falsifier as a test);
  `airy_radius` exponents $+1$ in $\lambda$, $-1$ in $D$; grating principal-maximum FWHM
  $\propto 1/N$ fit.
- *seeds:* two-point-resolution ensembles (30's lab) reproducible per seed, statistics
  stable to $1/\sqrt{M}$; a random-phase screen propagated by the angular spectrum
  develops fully-developed speckle with contrast → 1 (the `00-phasors` random walk in
  2-D, seeded).
- *dimensions:* `rayleigh_criterion` in rad, `airy_radius` in m, `angular_dispersion` in
  rad/m, `fresnel_number` dimensionless — against the `units` registry.

**Shared media:** one script `media/render/render_diffraction.py` produces all Part IX
MP4s (shot lists in §5); the near→far morph (shot i) is the part's signature animation,
precomputed. **Glossary themes:** wavelet/diffraction vocabulary (28), far-field (29),
resolution (30), grating (31), propagation (32) — per-module lists in §5. "Airy" names two
unrelated objects in the course glossary (part-08's `airy-function`, Fabry–Pérot; this
part's `airy-pattern`, circular aperture — both after G. B. Airy); both entries carry a
one-line disambiguation.

## 5. Module specifications

### 5.1 `28-huygens` — Huygens–Fresnel: diffraction from wavelets

- **Identity and scope:** master-plan notebook 9.1. Diffraction from secondary-wavelet
  intuition — **numerical wavelet superposition before any formula**; Fresnel zones; the
  Poisson–Arago spot simulated and boxed as epistemology. Deferred: the far-field
  transform relation → `29-fraunhofer`; the FFT propagator's pedagogy →
  `32-fresnel-diffraction` (this module's Poisson-spot *rendering* uses
  `angular_spectrum_propagate` behind the scenes; its in-page numerics use the
  transparent `wavelet_sum`); Kirchhoff's derivation → cited, never taught.
- **Prerequisites:** `00-phasors` (tip-to-tail polygon, superposition theorem);
  `08-wave-equation` (spherical/cylindrical spreading); `15-em-energy`
  ($I \propto |\hat{U}|^2$).
- **Learning objectives:**
  - `OBJ-28-1` — State the Huygens-Fresnel principle: every point of a wavefront acts as
    a source of secondary wavelets, and the field beyond is their coherent phasor sum.
  - `OBJ-28-2` — Compute a diffracted field numerically by summing sampled wavelet
    phasors over an aperture, and read the sum as module 00's tip-to-tail polygon made
    spatial.
  - `OBJ-28-3` — Predict qualitatively how shadow sharpness depends on a/lambda and
    state in what limit ray-optics shadows are recovered.
  - `OBJ-28-4` — Use Fresnel half-period zones to predict on-axis intensity behind
    circular apertures and disks, including the bright Poisson-Arago spot.
  - `OBJ-28-5` — Identify the model's honest gaps (no backward wave, obliquity factor
    inserted by hand) as assumptions resolved by Kirchhoff's theory, and recount the
    Poisson-Arago episode as a falsifying prediction that confirmed wave optics.
- **Mathematical background:** has — phasor sums, $e^{\ii(kr-\omega t)}/r$ spherical
  waves; introduced here — discretising a continuous source distribution and trusting
  the sum only after a density-convergence check (the course's first "integral as limit
  of arrows", done honestly).
- **Physical intuition goals:** (1) every shadow edge is soft at the wavelength scale —
  razor blades have fringes; (2) whether an obstacle "blocks" light is a question about
  $a/\lambda$, not opacity; (3) the exact centre of a circular shadow is *bright* —
  symmetry makes all edge wavelets agree in phase; (4) ray optics is what wavelet sums
  look like as $\lambda \to 0$.
- **Section skeleton seeds:**
  - *puzzle:* sound bends around a doorway; light appears not to — yet the darkest place
    behind a coin, its exact shadow centre, is *bright*. (Boxed: if light is a wave like
    sound, why are shadows sharp at all — and if they are, what is a bright spot doing in
    the middle of one?) The 1818 story opens in two sentences, paid off in derive/verify.
  - *predict:* (1) a slit much wider than $\lambda$ narrows: does the transmitted patch
    first narrow or first widen? (plants 29's crossover) (2) behind an opaque disk, is
    the on-axis point darker or brighter than the surrounding shadow? (targets
    `obstacle-only-darkens`) (3) do Huygens wavelets radiate backwards — and if so, why
    is there no backward wave? (4) double $\lambda$ at fixed geometry: edge fringes
    spread or tighten?
  - *explore:* **wavelet builder** — an aperture sampled by $N$ secondary sources
    (density slider), draggable observation point; panels: geometry with wavelet arcs,
    the tip-to-tail polygon at the chosen point (module 00's picture with geometry-set
    phases), screen intensity assembled point by point; presets: slit, edge, disk
    (on-axis cut), circular aperture; $a$, $\lambda$, $z$ sliders.
  - *derive:* the principle stated (its two honesty gaps flagged immediately) → the
    discrete wavelet sum and its polygon reading (arrows aligned straight-through,
    curled off-axis) → Fresnel half-period zones → alternating series, on-axis amplitude
    ≈ half the first zone → circular aperture: $1$ zone bright, $2$ dark (measured in
    explore) → the **disk**: all edge wavelets equidistant from the axis → in phase →
    the bright spot, as bright as the unobstructed axis — Poisson's reductio, Arago's
    measurement → ray limit as $\lambda \to 0$ (stationary phase qualitatively;
    `33-fermat` teaser).
  - *verify:* `wavelet_sum` density-convergence study (`numerical-observation` box: the
    sum *is* an integral once wavelets are ≲ λ/4 apart — measured, with the fitted
    rate); one-zone vs two-zone on-axis ratio; the Poisson-spot axial intensity equals
    the unobstructed value (cross-checked in module 32 by `angular_spectrum_propagate` —
    flagged as a coming attraction).
  - *transfer:* `29-fraunhofer` (this sum, far away, is a Fourier transform — next
    page's first sentence); `32-fresnel-diffraction` (this sum, done with FFTs, at any
    distance); `33-fermat` (stationary phase → rays); zone plates (problem set + X-ray
    optics sentence); acoustics and radio (hearing around corners: $a/\lambda$); back to
    `00-phasors` (the polygon promise kept).
  - *quiz:* zone-counting numeric; disk-centre MC (registry distractor); backward-wave
    MC; $a/\lambda$ ranking MC; polygon-reading item.
  - *explain:* why the bright spot is *not* paradoxical once you believe in wavelets;
    why sound and light behave differently at a doorway; what was at stake for Poisson,
    and why a confirmed absurd prediction is *strong* evidence.
  - *advanced:* the obliquity factor $(1 + \cos\theta)/2$ and where it comes from
    (Kirchhoff's integral quoted, one paragraph); why the naive picture over-counts by
    a factor and phase ($e^{-\ii\pi/2}/\lambda$ — stated, "Kirchhoff pays this debt",
    Goodman citation); zone-plate focal lengths.
- **Core derivations:** (1) discrete wavelet sum
  $U(P) \propto \sum_j A_j\,e^{\ii k r_j}/\sqrt{r_j}$ (sampled line aperture,
  cylindrical spreading; 3-D $1/r$ form stated), convention-compliant; (2) zones:
  $r_m = z + m\lambda/2$ → ring radii $\rho_m = \sqrt{m\lambda z}$ (paraxial), equal
  areas $\pi\lambda z$ → alternating series
  $U \propto U_1 - U_2 + U_3 - \cdots \approx U_1/2$; (3) the disk: a disk of $p$ zones
  removes the first $p$ terms, remainder $\approx U_{p+1}/2$ — same magnitude, hence the
  bright spot; (4) ray recovery: $\rho_1 = \sqrt{\lambda z} \to 0$ as $\lambda \to 0$ —
  the pencil of relevant wavelets collapses to the line of sight.
- **Model specification draft:** System — a monochromatic scalar field crossing a thin
  planar mask; sampled secondary sources on the open part; observables are screen
  intensities from their coherent sum. Dynamics — stationary; propagation as phasor
  accumulation $e^{\ii k r}$. Boundary — Kirchhoff screen: field = 1 in the opening, 0
  on the screen (`model-assumption`, wrong within ~λ of edges). Ensemble —
  deterministic, fully coherent. Ignored — polarization; backward wavelets; obliquity
  beyond the quoted factor; edge currents. Valid when — features ≳ λ; observation many λ
  from the mask. Failure modes — trusting sub-wavelength features; reading an
  un-converged discrete sum as physics; expecting energy conservation at large angles
  without obliquity.
- **Epistemic classification:** the Huygens–Fresnel principle — `model-assumption` at
  this level ("Kirchhoff derives it from the wave equation; we cite, not derive"); "no
  backward wave" — `open-question` *at this module's level*, resolution named
  (Kirchhoff's obliquity factor) — an honesty box closed by a citation; zone arithmetic
  — `theorem` (given the principle); wavelet-density convergence —
  `numerical-observation`; **Arago's bright spot** — `empirical-law` box carrying the
  epistemology paragraph: *a theory earns trust when its strangest prediction, derived
  by an opponent to kill it, is measured* (the part's centerpiece box, cited from §6).
- **Misconceptions:** NEW **`obstacle-only-darkens`** — "Putting an obstacle into a beam
  can only ever reduce the light at any point behind it." Falsifying experiment:
  simulate the opaque disk's shadow (`wavelet_sum` on-axis profile); the axial point is
  as bright as with *no disk at all*, and near-shadow fringes exceed the uniform
  intensity. Distractor: quiz option "every point behind the disk receives less light
  than without the disk".
- **Glossary terms:** `diffraction` (עקיפה), `huygens-principle` (עקרון הויגנס),
  `secondary-wavelet` (גלון משני — translator to confirm; `he_reject` candidate:
  גל משני), `wavefront` (cited, deposited by `14-em-waves`), `fresnel-zone` (אזור פרנל), `poisson-spot`
  (כתם פואסון), `obliquity-factor` (גורם הטיה — translator to decide), `zone-plate`
  (לוחית אזורים — advanced).
- **Interactive controls and simulations:** wavelet builder (aperture preset,
  $N_{\rm src}$ 10–2000, $a$ 5–200 µm, $\lambda$ 400–700 nm, $z$ 1 mm–1 m, draggable
  observation point); zone viewer (zones coloured by sign, per-zone open/blocked toggle
  — a proto zone plate); Poisson-spot explorer (disk diameter, $z$, axial + transverse
  cuts).
- **Virtual lab outline** (`notebooks/en/labs/28-huygens.ipynb`): (1) polygon play —
  watch arrows close into a circle off-axis; (2) convergence: error vs wavelet density,
  log-log fit; (3) zones: open 1, 2, 3 zones, tabulate on-axis intensity vs the
  alternating series; (4) *measurement:* the Poisson spot — 2-mm disk at $z = 1$ m,
  633 nm; measure spot intensity vs unobstructed axis (ratio 1.0), add pixel noise
  (`measurement.add_noise`), report the ratio ± uncertainty across seeds; (5) open the
  sealed box: rerun (4) with the imported angular-spectrum propagator — two methods, one
  answer, door to 32.
- **Real-experiment counterpart:** a ball bearing or BB glued to a microscope slide,
  laser pointer expanded through a lens or pinhole, shadow on a wall at 2–3 m:
  photograph the bright spot; import an intensity row and compare the axial ratio.
  Cheap, spectacular, and the exact 1818 apparatus.
- **Media assets** (`render_diffraction.py`): (a) wavelet polygon: observation point
  sweeping the screen while arrows curl, pattern assembling underneath; (b) Poisson-spot
  buildup: shadow computed zone ring by zone ring, spot emerging last. Language-neutral.
- **Quiz bank outline:** `Q-28-1` MC — disk centre bright/dark (OBJ-28-4, distractor
  `obstacle-only-darkens`); `Q-28-2` numeric — zone radius $\sqrt{m\lambda z}$
  (OBJ-28-4); `Q-28-3` MC — which screen point a closed polygon corresponds to
  (OBJ-28-2); `Q-28-4` MC — doorway sound vs light (OBJ-28-3); `Q-28-5` MC — the
  backward-wave question and what resolves it (OBJ-28-5); `Q-28-6` free — the
  Poisson–Arago story in four sentences: prediction, intent, measurement, lesson
  (OBJ-28-5); `Q-28-7` numeric — 1-zone vs 2-zone aperture intensity ratio (OBJ-28-1,
  OBJ-28-4).
- **Problem set outline:** analytical — zone areas equal (paraxial proof); zone-plate
  focal length $f = \rho_1^2/\lambda$; the straight-edge half-shadow $I = I_0/4$ from
  half the wavelets removed (bridge to 32). Computational — `wavelet_sum` convergence
  rate; build and focus a zone-plate mask. Challenge — obliquity on/off at large
  angles: measure where the naive sum's energy bookkeeping fails.
- **Runtime budget:** direct sums ≤ $2000 \times 2000$ source–observation pairs (~4·10⁶
  complex exponentials) — about a second in Pyodide; explore presets capped at
  $N_{\rm src} = 500$ for live sliders; Poisson 2-D renders precomputed (MP4), lab uses
  1-D cuts only.
- **Validation gates:** standard set (README) with `--module 28-huygens`; plus the
  wavelet-convergence and Poisson-ratio tests of §4 land with this module.
- **Open questions for the author:** whether the 1818 narrative opens the puzzle or the
  derive section (recommendation: two sentences in puzzle, full story with the
  `empirical-law` box in derive — the spot must be simulated before the history lands);
  whether the zone viewer doubles as a zone-plate builder in core (recommendation:
  problem set — core keeps one idea).

### 5.2 `29-fraunhofer` — Fraunhofer diffraction: the far field is a Fourier transform

- **Identity and scope:** master-plan notebooks 9.2 + 9.3, merged (precedent:
  `02-damped-driven` ← 1.2 + 1.3): the transform relation *and* its first payoff — the
  single slit — are one lesson; splitting them would put the punchline in a different
  module from the joke (§31: the pattern "should appear as a natural consequence rather
  than an isolated formula"). Deferred: compound apertures and the convolution theorem →
  `30-apertures`; $N$ slits → `31-gratings`; validity beyond $N_F \ll 1$ →
  `32-fresnel-diffraction`; the lens-brings-the-far-field-near theorem →
  `39-fourier-lens` (id reference; parallel part).
- **Prerequisites:** `28-huygens` (the wavelet sum whose far-field limit this is);
  `04-fourier-transform` (rect ↔ sinc via `fourier.rect_pulse` / `sinc_spectrum`;
  bandwidth theorem, `fourier.rms_widths`); `23-interference` (path-difference
  geometry); `15-em-energy`.
- **Learning objectives:**
  - `OBJ-29-1` — Compute the Fresnel number N_F = a^2/(lambda z) and state the
    Fraunhofer condition N_F << 1 as the regime where aperture-internal quadratic phase
    is negligible.
  - `OBJ-29-2` — Derive U(theta) proportional to the Fourier transform of the aperture
    function A(x), evaluated at k_x = k sin(theta), from the path-difference phase of
    each aperture point.
  - `OBJ-29-3` — Write down the single-slit pattern I(theta) = I0 sinc^2(pi a
    sin(theta)/lambda) directly from the rect <-> sinc pair, and locate its zeros at
    sin(theta) = m lambda / a.
  - `OBJ-29-4` — Measure the scaling of the central-lobe width with slit width
    (Delta theta proportional to 1/a) from simulated patterns, and explain physically
    why a narrower slit produces a wider pattern.
  - `OBJ-29-5` — Read confinement vs angular spread as the bandwidth theorem in space:
    Delta x Delta k_x >= 1/2 with Delta x set by the aperture — the module-04
    inequality in its second costume.
  - `OBJ-29-6` — Compute far-field patterns of arbitrary 1-D apertures with
    fraunhofer_pattern and check them against analytic references.
- **Mathematical background:** has — the 1-D transform and pair zoo, phasor integrals;
  introduced here — the *spatial* transform (the course's first: part-00 §8 reserved
  space for this moment) and the map $k_x = k\sin\theta$ from directions to frequencies.
- **Physical intuition goals:** (1) narrower slit, wider pattern — confinement costs
  angular spread, *always*; (2) the far field of an aperture is its spectrum — sharp
  edges ring (sinc lobes), smooth apertures don't (Gaussian); (3) doubling $\lambda$
  doubles the pattern — the screen is drawn in units of $\lambda/a$; (4) "far" is not a
  distance but the dimensionless statement $N_F \ll 1$.
- **Section skeleton seeds:**
  - *puzzle:* close a slit slowly in laser light. The transmitted stripe first narrows —
    obeying geometry — then, past a certain width, turns around and *widens*, sprouting
    side lobes. (Boxed: what sets the turnaround width, and why does light punish
    confinement with spread?) The misconception staged as hardware.
  - *predict:* (1) halve the slit width: central lobe halves or doubles? (targets
    `narrow-slit-narrow-pattern`) (2) can any side lobe beat $\theta = 0$? (3) red →
    blue at fixed slit: pattern grows or shrinks? (4) a soft-edged (Gaussian) opening of
    similar size: do the side lobes survive?
  - *explore:* **the slit-width slider as centrepiece** — live far field with measured
    central-lobe width $\Delta\theta$ plotted against $a$ on a log-log inset (the
    falsifier drawn in real time); aperture selector (rect / Gaussian / triangle, each
    with its module-04 partner overlaid); $\lambda$ slider; $N_F$ readout with a "you
    are in the far field" indicator.
  - *derive:* start from 28's wavelet sum → far-field reduction, quadratic remainder
    kept in view → **the honest condition**: its phase is negligible iff
    $N_F = a^2/(\lambda z) \ll 1$ (boxed `approximation`; "far" quantified, not
    gestured) → the surviving linear phase gives $U(\theta) \propto \mathcal{F}\{A\}$ at
    $k_x = k\sin\theta$ (course forward sign — `fourier.spectrum`'s kernel, now in
    space) → **the recognition moment**: $A = \operatorname{rect}(x/a)$ and the answer
    is *already known* — the module-04 zoo card is pasted, not re-derived → zeros,
    central width, side lobes → the uncertainty reading: $\Delta x \sim a$ ⇒
    $\Delta\theta \sim \lambda/a$ — `fourier.rms_widths` in space, module 04's theorem,
    no new proof.
  - *verify:* `fraunhofer_pattern(slit)` vs `sinc_intensity` to $10^{-10}$; the log-log
    fit $\Delta\theta \propto a^{-1.00}$ (`numerical-observation` box with the fitted
    exponent — the registry falsifier as a measurement); Gaussian aperture: no zeros
    (zoo pair #2 in light); Parseval: screen energy = aperture energy.
  - *transfer:* `30-apertures` (two of these slits, and circles); `31-gratings` (many);
    `32-fresnel-diffraction` ($N_F \gtrsim 1$: what was dropped, restored);
    `39-fourier-lens` (a lens moves this screen to its focal plane — id reference);
    `43-gaussian-beams` (the Gaussian aperture's spread is beam divergence);
    `04-fourier-transform` backward (the zoo's third life); `17-refraction`
    ($k_x = k\sin\theta$ is the same $k_\parallel$ bookkeeping).
  - *quiz:* slit-narrowing MC (registry distractor); zero-position numeric;
    wavelength-scaling MC; $N_F$ classification numeric; uncertainty-reading free item.
  - *explain:* why "the far field is the aperture's spectrum" is the same sentence as
    module 04's "a pulse's spectrum widens as it shortens"; why side lobes are the
    slit's sharp edges talking; what exactly is *approximated* in Fraunhofer
    diffraction and who pays when $N_F \to 1$.
  - *advanced:* apodization — soft-edged apertures as window functions (module 04's Hann
    window, spatially: resolution vs side-lobe suppression; pupil teaser for
    `37-aberrations` / Part XI); Babinet's principle (complementary screens give
    identical patterns off-axis — the hair-measurement licence), stated and simulated.
- **Core derivations:** (1) far-field reduction with explicit remainder:
  $k\,\frac{x^2}{2z}\big|_{x = a/2} = \frac{\pi}{4} N_F$ — small iff $N_F \ll 1$;
  (2) $U(\theta) \propto \mathcal{F}\{A\}(k\sin\theta)$, kernel $e^{-\ii k_x x}$;
  (3) the slit:
  $I(\theta) = I_0 \operatorname{sinc}^2\!\big(\tfrac{\pi a \sin\theta}{\lambda}\big)$,
  $\operatorname{sinc}(x) = \sin x/x$, zeros $\sin\theta = m\lambda/a$ ($m \ne 0$),
  side-lobe heights $4.7\%, 1.6\%, \dots$; (4) RMS confinement–spread product, quoting
  module 04's theorem with $x \leftrightarrow t$, $k_x \leftrightarrow \omega$.
- **Model specification draft:** System — a thin planar aperture $A(x)$ under coherent
  plane-wave illumination; observable is far-field intensity vs angle (or screen
  position at $z$). Dynamics — stationary; propagation enters only as the linear phase.
  Boundary — Kirchhoff mask (inherited from 28); screen at $N_F \ll 1$. Ensemble —
  deterministic, fully coherent. Ignored — quadratic (Fresnel) phase; polarization;
  obliquity (small angles). Valid when — $N_F \ll 1$ and $\sin\theta$ small; features
  ≳ λ. Failure modes — Fraunhofer at $N_F \gtrsim 1$ (32 shows how it fails);
  large-angle patterns without obliquity; screen coordinates read as angles beyond the
  small-angle map.
- **Epistemic classification:** far-field transform relation — `theorem` (given 28's
  principle); Fraunhofer condition — `approximation` (boxed, $N_F$ edge); the slit
  pattern — `theorem` *by recognition* (the box cites module 04's pair, per §31);
  measured $\Delta\theta$ exponent — `numerical-observation`; confinement–spread law —
  `theorem` (module 04's, cited).
- **Misconceptions:** claims **`narrow-slit-narrow-pattern`** (README conflict log
  re-points it here from `09-diffraction`; the one-line `assigned_module` edit lands
  with this module). Falsifying experiment: the slit-width slider with live measured
  $\Delta\theta$, then the lab's log-log fit $\Delta\theta \propto a^{-1}$ — the pattern
  demonstrably *widens* as the slit narrows, with a measured exponent, not a slogan.
  Distractor: quiz option "halving the slit width halves the width of the central
  bright band".
- **Glossary terms:** `fraunhofer-diffraction` (עקיפת פראונהופר), `far-field`
  (שדה רחוק), `fresnel-number` (מספר פרנל), `aperture-function` (פונקציית מפתח;
  `he_reject` candidate: צמצם — translator to decide between מפתח and צמצם
  course-wide), `sinc-function` (פונקציית sinc — transliteration likely), `side-lobe`
  (אונה צדדית), `apodization` (אפודיזציה — advanced), `babinet-principle`
  (עקרון בבינה — advanced; translator to confirm spelling).
- **Interactive controls and simulations:** the slit-width centrepiece ($a$ 2–200 µm log
  slider, $\lambda$ 400–700 nm, $z$ 0.1–5 m with live $N_F$; measured-width inset);
  aperture selector with zoo overlays; angle↔screen-position toggle (the small-angle
  map made explicit).
- **Virtual lab outline** (`notebooks/en/labs/29-fraunhofer.ipynb`): (1) crossover hunt:
  sweep $a$ downward, record patch width, find the geometric → diffractive turnaround
  (at $a \sim \sqrt{\lambda z}$, i.e. $N_F \sim 1$ — a discovery that seeds 32);
  (2) *measurement* (the registry falsifier): patterns at 8 slit widths with pixel noise
  (`measurement.add_noise`), extract widths, log-log fit → $\alpha = -1.00 \pm$
  uncertainty via `validation.scaling_exponent`; (3) zoo in light: three apertures vs
  their module-04 partners; (4) *measurement:* unknown-slit width from zero positions,
  report $a \pm \sigma$ — then measure a human hair the same way (Babinet) against a
  micrometer value.
- **Real-experiment counterpart:** laser pointer + adjustable slit (two razor blades, or
  a vernier caliper's jaws): photograph patterns at several gaps, import intensity rows,
  redo the $\Delta\theta$–$a$ fit on real data; a human hair across the beam for the
  Babinet measurement (compare 60–100 µm).
- **Media assets** (`render_diffraction.py`): (c) the crossover: slit closing while the
  far-field stripe narrows, stalls, and blooms into sinc lobes; (d) aperture–pattern
  pairs morphing (rect→Gaussian→triangle) with transforms tracking. Language-neutral.
- **Quiz bank outline:** `Q-29-1` MC — halve the slit: central lobe (OBJ-29-3,
  OBJ-29-4, distractor `narrow-slit-narrow-pattern`); `Q-29-2` numeric — first-zero
  angle for $a = 50$ µm, $\lambda = 633$ nm (OBJ-29-3); `Q-29-3` numeric — classify a
  geometry by $N_F$ (OBJ-29-1); `Q-29-4` MC — red vs blue pattern size (OBJ-29-3);
  `Q-29-5` MC — Gaussian-aperture side lobes (OBJ-29-2, OBJ-29-6); `Q-29-6` free —
  state the transform relation and what each symbol means physically (OBJ-29-2);
  `Q-29-7` free — the bandwidth theorem in both costumes, two sentences (OBJ-29-5).
- **Problem set outline:** analytical — double-width slit at $\theta = 0$ (quadruples:
  amplitude vs energy bookkeeping); triangle aperture via rect∗rect (30 teaser); RMS
  width of the sinc (second moment diverges — honest subtlety, back to 04's RMS
  caveats). Computational — side-lobe suppression vs apodization strength; crossover
  point vs $\lambda$. Challenge — Babinet from Parseval: prove complementary screens
  agree off-axis, verify with slit vs strip.
- **Runtime budget:** 1-D FFTs ≤ $2^{14}$ with ×4 zero padding — milliseconds; the
  eight-width lab loop trivial; nothing 2-D in this module.
- **Validation gates:** standard set with `--module 29-fraunhofer`; plus the slit-limit,
  Parseval, and $\Delta\theta$-scaling tests of §4; apply the README conflict-log
  re-pointing `narrow-slit-narrow-pattern` → `29-fraunhofer` (status → `addressed` when
  the quiz distractor exists).
- **Open questions for the author:** primary notation $k_x$ vs $\sin\theta$
  (recommendation: derive in $\sin\theta$, box both; Part XI upgrades $k_x$ to "spatial
  frequency"); whether Babinet lives in advanced or core (recommendation: advanced, but
  the hair measurement stays in the lab).

### 5.3 `30-apertures` — Apertures: envelopes, the Airy pattern, and resolution

- **Identity and scope:** master-plan notebooks 9.4 + 9.5, merged: both are "the
  transform of a compound aperture" — the convolution theorem made visible; splitting
  them would teach one theorem twice. **This module receives the part-08 handoff**:
  `23-interference` modelled slits as ideal line sources and deferred the finite-width
  envelope here (part-08 §5.1 and §8; honoured in this module's first section, logged
  in §8 below). Deferred from here: $N > 2$ slits → `31-gratings`; the PSF/OTF
  formalism the Airy disk seeds → `40-psf-otf` (id reference; parallel part); aberrated
  pupils → `37-aberrations`.
- **Prerequisites:** `29-fraunhofer` (transform relation, sinc envelope);
  `23-interference` (`interference.young_pattern` — the cos² factor, cited);
  `04-fourier-transform` (convolution theorem, `fourier.convolve`); `28-huygens`
  (wavelet picture for the circular-symmetry argument).
- **Learning objectives:**
  - `OBJ-30-1` — Write the finite-width double slit as a convolution (two-delta comb
    convolved with rect) and derive I(theta) = cos^2(pi d sin(theta)/lambda) *
    sinc^2(pi a sin(theta)/lambda) by the convolution theorem.
  - `OBJ-30-2` — Predict missing orders when d/a is an integer, identify them in
    patterns, and recover the slit-to-separation ratio from which orders vanish.
  - `OBJ-30-3` — State the circular-aperture Airy pattern I = I0 [2 J1(v)/v]^2 with
    v = pi D sin(theta)/lambda and its first zero at sin(theta) = 1.22 lambda/D.
  - `OBJ-30-4` — Apply the Rayleigh criterion theta_min = 1.22 lambda/D with real
    numbers: eye pupil, Hubble, a radio dish, and a 10-mm telescope.
  - `OBJ-30-5` — Measure a two-point resolution limit from noisy simulated images, with
    uncertainty, and compare it with the Rayleigh prediction.
  - `OBJ-30-6` — Identify the Airy disk as the point-spread function of a
    diffraction-limited imager and predict how image blur scales with lambda and D.
- **Mathematical background:** has — convolution theorem, sinc envelope, 2-D FFT
  mechanics (`fraunhofer_pattern`); introduced here — the comb ⊗ shape decomposition of
  compound apertures; $J_1$ *used*, first zeros quoted ($3.832, 7.016, 10.174$), origin
  deferred to advanced.
- **Physical intuition goals:** (1) structure at *large* scale $d$ makes *fine* fringes,
  at *small* scale $a$ the *broad* envelope — big↔small, always; (2) an interference
  order can be exactly extinguished by an envelope zero — patterns multiply; (3) every
  telescope draws stars as Airy disks — the aperture is stamped on the sky;
  (4) magnification enlarges the blur with the image — only aperture buys resolution.
- **Section skeleton seeds:**
  - *puzzle:* Young's experiment with *real* slits: orders $m = 0, 1, 2$ are there,
    $m = 3$ is *gone*, $m = 4$ is back. (Boxed: who stole order 3 — and what does the
    theft reveal about the slits?) The handoff stated in one sentence: module 23
    promised this envelope; here it is.
  - *predict:* (1) slits get *wider* at fixed $d$: do fringes move? does the envelope?
    (2) can a fringe order vanish entirely — what must $d/a$ be? (3) a star through a
    bigger telescope: smaller or bigger dot? (4) will more eyepiece magnification split
    a close double star? (targets `resolution-improves-with-magnification`)
  - *explore:* double-slit dashboard — $a$, $d$, $\lambda$ sliders with cos² fringes,
    sinc² envelope, and their product drawn separately; live counter of extinguished
    orders; **2-D aperture gallery** (square, circle, triangle, two circles) via
    `fraunhofer_pattern`; **two-point resolution game**: two Airy sources, separation
    slider, "resolved?" judgement vs the Rayleigh line.
  - *derive:* $A(x) = [\delta(x - d/2) + \delta(x + d/2)] \ast \operatorname{rect}(x/a)$
    → transform = product (module 04's theorem, cited) →
    $I = I_0\cos^2(\cdot)\,\operatorname{sinc}^2(\cdot)$ — 23's fringes under 29's
    envelope, both cited → missing orders: order $m$ ($\sin\theta = m\lambda/d$) dies on
    an envelope zero ($\sin\theta = p\lambda/a$) — integer $d/a = n$ kills orders
    $n, 2n, 3n, \dots$ → circular aperture: radial symmetry → Hankel transform (named,
    not developed) → **the Bessel result, stated honestly**: $I = I_0[2J_1(v)/v]^2$,
    first zero $v = 3.832 = 1.22\pi$ → $\sin\theta = 1.22\lambda/D$ (boxed `theorem`,
    "derived in advanced"; 83.8% of the energy in the central disk) → Rayleigh
    criterion: maximum on first zero, $\theta_{\min} = 1.22\lambda/D$ (boxed
    `definition` — a *convention*, said so; sub-Rayleigh left to
    `53-computational-imaging`) → the numbers table: eye ($D \approx 3$ mm, 550 nm →
    $2.2\times10^{-4}$ rad ≈ 46″ — about 1′ with real optics), Hubble ($2.4$ m →
    $0.058″$), a 100-m radio dish at 21 cm → $2.6\times10^{-3}$ rad ≈ 0.15° (why radio
    interferometry exists — `27-coherence`'s VLBI sentence recalled), the §26.4 10-mm
    telescope → $6.7\times10^{-5}$ rad ≈ 14″ (full open investigation in the problem set
    and §6) → **the PSF sentence**: a lens images a point to this pattern; the Airy disk
    *is* the point-spread function, and `40-psf-otf` will convolve every scene with it
    (said in exactly those words).
  - *verify:* `fraunhofer_pattern(double_slit)` vs `double_slit_intensity` and vs
    `interference.young_pattern` × `sinc_intensity` (the handoff verified in code);
    missing orders at $d/a = 3$ exact; `fraunhofer_pattern(circular)` zeros at
    $1.220, 2.233, 3.238\,\lambda/D$ (`numerical-observation` box); encircled energy
    83.8%.
  - *transfer:* `31-gratings` (same comb ⊗ rect, longer comb); `40-psf-otf` (the PSF
    door, id reference); `37-aberrations` (real pupils fall short of Airy);
    `41-imaging-coherence` (coherent vs incoherent pairs resolve differently — one
    sentence); `27-coherence` backward (the stellar interferometer measured what a
    single dish could not); `53-computational-imaging` (the criterion is a convention,
    not a wall).
  - *quiz:* missing-order numeric; envelope vs fringe scaling MC; Rayleigh numerics
    (Hubble, eye); magnification MC (registry distractor); PSF-sentence free item.
  - *explain:* how to measure $d$ *and* $a$ from a photograph of the pattern alone; why
    "bigger telescope" means "sharper star", in wavelet language; what the Rayleigh
    criterion does *not* claim.
  - *advanced:* the Airy derivation — 2-D transform in polars, $J_0$ integral
    representation, $\int v' J_0 = v J_1$, first zeros; aperture-synthesis teaser (two
    small dishes far apart beat one big dish — door to `41-imaging-coherence`); annular
    apertures (central obstruction sharpens the core, feeds the side lobes — every
    reflector telescope).
- **Core derivations:** (1) comb ⊗ rect and the product law (formulas as in seeds,
  convention-compliant); (2) missing-order condition $d/a = m/p$, integer case boxed;
  (3) Airy: stated form, zeros, encircled energy; derivation in advanced; (4) Rayleigh
  with the worked numbers table (four rows, plus arcsecond conversions); (5) PSF
  preview: image = scene ∗ Airy (one line, `40-psf-otf`'s opening claim, planted).
- **Model specification draft:** System — compound planar apertures (double slit;
  circular pupil) under coherent plane-wave illumination; observables are far-field
  patterns and two-point-source images. Dynamics — stationary. Boundary — Kirchhoff
  mask; $N_F \ll 1$; for the resolution lab, two mutually *incoherent* point sources
  (intensities add, per `27-coherence`). Ensemble — deterministic apart from seeded lab
  noise. Ignored — polarization; aberrations (perfect pupil); obliquity. Valid when —
  29's conditions; source pair incoherent for the resolution question. Failure modes —
  adding amplitudes of incoherent stars; reading the Rayleigh convention as a physical
  cutoff; expecting magnification to beat aperture.
- **Epistemic classification:** product law — `theorem` (convolution theorem cited);
  missing orders — `theorem`; Airy pattern — `theorem` stated with proof deferred
  (honest box: "the Bessel integral is in advanced; the zeros you can *measure* now");
  measured zeros — `numerical-observation`; Rayleigh criterion — `definition` (a
  convention, boxed as such); "incoherent point pair" — `model-assumption`.
- **Misconceptions:** NEW **`resolution-improves-with-magnification`** — "More
  magnification always reveals more detail." Falsifying experiment: the two-point lab
  renders an unresolved pair at the diffraction limit, then digitally magnifies ×2, ×4,
  ×8 — the blur enlarges with the image and the pair never separates; only the aperture
  slider splits it. Distractor: quiz option "a higher-power eyepiece will split the
  double star". (Missing orders stays a quiz item and lab discovery, not a registry
  entry — a surprise, not a stable wrong model.)
- **Glossary terms:** `airy-pattern` (תבנית איירי — disambiguated from part-08's
  `airy-function`), `airy-disk` (דיסקת איירי), `diffraction-envelope` (מעטפת עקיפה),
  `missing-orders` (סדרים חסרים), `rayleigh-criterion` (קריטריון ריילי),
  `angular-resolution` (הפרדה זוויתית), `diffraction-limited` (מוגבל־עקיפה — translator
  to confirm hyphenation). The `point-spread-function` key is *deferred* to
  `40-psf-otf` (previewed in prose here; the glossary key belongs to its owner).
- **Interactive controls and simulations:** double-slit dashboard ($a$ 5–100 µm, $d$
  20–500 µm with $d \ge a$ enforced, $\lambda$; separate cos²/sinc²/product traces;
  order counter); 2-D gallery (five presets, log-intensity toggle); resolution game
  ($D$, separation, $\lambda$, noise level; blind "resolved?" scoring against the
  Rayleigh line).
- **Virtual lab outline** (`notebooks/en/labs/30-apertures.ipynb`): (1) envelope
  dissection: vary $a$ at fixed $d$, then $d$ at fixed $a$ — attribute each feature to
  its scale; (2) *discovery:* sweep $d/a$ and watch order 3 die and revive; recover
  $d/a$ from which orders vanish; (3) Airy: radial profile from a 2-D
  `fraunhofer_pattern`, locate zeros, compare $J_1$; (4) *measurement* (centrepiece):
  two incoherent Airy sources with noise (`measurement.add_noise`, seeded), step
  separation downward, judge resolved/not by a fixed dip criterion across seeds →
  measured $\theta_{\min} \pm \sigma$ vs $1.22\lambda/D$; (5) magnification postscript:
  enlarge an unresolved frame — the registry falsifier, one cell.
- **Real-experiment counterpart:** double-slit slide (or foil with two scored lines) in
  a laser beam — photograph, find the missing order, recover $d/a$; a pinhole in
  aluminium foil against a distant LED for Airy rings; the streetlight-through-umbrella
  cross as the 2-D gallery in the street.
- **Media assets** (`render_diffraction.py`): (e) envelope theft: $d/a$ sweeping through
  3 while order 3 fades and returns; (f) Airy buildup: aperture $D$ growing, disk
  shrinking, two stars separating past the Rayleigh line. Language-neutral.
- **Quiz bank outline:** `Q-30-1` numeric — which orders vanish for $d/a = 3$
  (OBJ-30-2); `Q-30-2` MC — widen slits at fixed $d$: fringes vs envelope (OBJ-30-1);
  `Q-30-3` numeric — Hubble's $\theta_{\min}$ at 550 nm (OBJ-30-4); `Q-30-4` MC —
  magnification vs resolution (OBJ-30-4, OBJ-30-6, distractor
  `resolution-improves-with-magnification`); `Q-30-5` numeric — first Airy zero for the
  10-mm telescope (OBJ-30-3, OBJ-30-4); `Q-30-6` MC — read $d/a$ from a pattern with
  orders 4, 8 missing (OBJ-30-2); `Q-30-7` free — the Airy disk as PSF: what will
  module 40 convolve, and with what (OBJ-30-6); `Q-30-8` free — design: laser, double
  slit, screen — extract both $d$ and $a$ (OBJ-30-1, OBJ-30-5).
- **Problem set outline:** analytical — three-slit pattern by phasors (23's problem
  upgraded with envelope; 31 warm-up); order-1/order-0 intensity ratio vs $d/a$;
  annular aperture on-axis field. Computational — **the §26.4 open investigation,
  verbatim**: the 10-mm telescope across wavelength — analytic + computational
  (fit $\theta_{\min}(\lambda)$, exponent $+1$, from simulated star pairs) + the
  physics explained; encircled-energy curve. Challenge — two *coherent* point sources
  vs incoherent: the resolution answer changes with relative phase (door to
  `41-imaging-coherence`).
- **Runtime budget:** 1-D products trivial; 2-D gallery and Airy at $512^2$ grids with
  ×2 padding — ≲ 1 s per shot in Pyodide; resolution lab ≤ 32 seeds × $256^2$ frames —
  a few seconds once; nothing exceeds $1024^2$.
- **Validation gates:** standard set with `--module 30-apertures`; plus the double-slit
  product identity, Airy-zero, and encircled-energy tests of §4.
- **Open questions for the author:** whether the resolution game runs before or after
  the criterion is taught (recommendation: before — let them *invent* a criterion, then
  name it); whether the numbers table adds a James Webb row (6.5 m but mid-IR: bigger
  mirror, longer wavelength, comparable $\theta_{\min}$; recommendation: yes — the
  punchline that $\lambda/D$ is a *ratio*).

### 5.4 `31-gratings` — Diffraction gratings and spectroscopy

- **Identity and scope:** master-plan notebook 9.6. Orders, angular dispersion, the
  $N$-slit sum, $1/N$ sharpening, resolving power $R = mN$ derived *and measured*; the
  virtual grating spectrometer (capstone §35.3's seed); CD/DVD pitch measurement.
  Deferred: spectrometer system design (detector sampling, range trades) → capstone
  §35.3; blazed-grating efficiency theory → advanced, qualitative only; X-ray/crystal
  diffraction → one transfer sentence.
- **Prerequisites:** `30-apertures` (comb ⊗ rect, envelope, missing orders);
  `17-refraction` (phase matching / $k_\parallel$ — "reused verbatim" per part-06);
  `26-fabry-perot` (`interference.airy_transmission`, `interference.finesse`);
  `23-interference` ($N = 2$ base case); `27-coherence` (linewidth vocabulary).
- **Learning objectives:**
  - `OBJ-31-1` — Derive the grating equation d sin(theta) = m lambda by phase matching,
    and restate it as k_parallel conservation modulo the grating's 2 pi / d.
  - `OBJ-31-2` — Derive the N-slit intensity [sin(N delta/2)/sin(delta/2)]^2 times the
    single-slit envelope by summing the finite geometric phasor series, and reduce it
    to the double slit at N = 2.
  - `OBJ-31-3` — Predict and measure that principal maxima stay fixed in angle and
    sharpen as Delta theta proportional to 1/N as slits are added at fixed pitch.
  - `OBJ-31-4` — Compute the angular dispersion d theta/d lambda = m/(d cos theta) and
    use it to lay out a spectrometer geometry.
  - `OBJ-31-5` — Derive and measure the chromatic resolving power
    R = lambda/Delta lambda = m N (sodium doublet resolved or not, vs N and m).
  - `OBJ-31-6` — Measure a track pitch from laser diffraction angles (CD vs DVD) with
    propagated uncertainty.
- **Mathematical background:** has — finite geometric series of phasors (00; 24 and 26
  summed the same series to $N$ and to $\infty$); introduced here — the
  $\sin(N\delta/2)/\sin(\delta/2)$ structure and its limits; reciprocal-lattice-lite
  ($2\pi/d$ lumps) language.
- **Physical intuition goals:** (1) principal maxima sit where *neighbouring* slits
  agree — more slits cannot move them, only enforce them more strictly; (2) $N$ phasors
  align on a maximum ($I \propto N^2$), curl closed slightly off it ($1/N$ width) —
  00's arithmetic with a budget; (3) dispersion is geometry: higher order and finer
  pitch buy more angle per nanometre; (4) resolution counts *illuminated* slits — a
  wide beam on a fine grating is a big $R$.
- **Section skeleton seeds:**
  - *puzzle:* a CD held to sunlight throws rainbows; so does a DVD — but *wider*.
    Neither contains pigment, and a laser bounced off each gives clean dots at
    different angles. (Boxed: what is the disc doing to the light, and what do the dot
    angles measure about the disc — to a tenth of a micron?)
  - *predict:* (1) more slits at the same spacing: do the bright directions move?
    (targets `more-slits-tighter-fringes`) (2) do they get brighter, sharper, both?
    (3) red vs blue: which diffracts to larger angles? (opposite to a prism!) (4) a
    DVD's pitch is half a CD's — first-order dot at larger or smaller angle?
  - *explore:* $N$-slit dashboard — $N$ 2–200 (log), $d$, $a$, $\lambda$; panels: the
    phasor polygon at a chosen angle (aligned ↔ closed), $I(\theta)$ with
    principal/secondary maxima and the sinc² envelope, width readout tracking $1/N$;
    **two-line source toggle** (sodium doublet) with a "resolved?" indicator — the
    spectrometer game begins here.
  - *derive:* phase matching: successive slits add path $d\sin\theta$; all agree iff
    $d\sin\theta = m\lambda$ (cite 17's argument: a functional identity forces equal
    $\omega$ and $k_\parallel$ up to the grating's $2\pi/d$ lumps — the interface's
    conservation law with a reciprocal kick) → the finite sum
    $U \propto \sum_{j=0}^{N-1} e^{\ii j\delta}$, $\delta = 2\pi d\sin\theta/\lambda$ →
    closed form →
    $I = I_0\big[\tfrac{\sin(N\delta/2)}{\sin(\delta/2)}\big]^2
    \operatorname{sinc}^2(\pi a\sin\theta/\lambda)$ → **the Fabry–Pérot parallel,
    staged**: 26 summed the *infinite* geometric series and got `airy_transmission`; 31
    sums the *finite* one — two instruments, one arithmetic, two cutoffs (side-by-side
    box tabulated under core derivations) → principal maxima $I \propto N^2$ at
    $\delta = 2\pi m$; first zero at $\Delta(\sin\theta) = \lambda/(Nd)$ → width
    $\propto 1/N$; $N - 2$ secondary maxima between orders → angular dispersion
    $d\theta/d\lambda = m/(d\cos\theta)$ → resolving power: Rayleigh applied to two
    wavelengths in order $m$ → $R = \lambda/\Delta\lambda = mN$ (boxed `theorem`) →
    worked target: the sodium doublet, $\Delta\lambda = 0.6$ nm at 589 nm →
    $R \approx 982$ → first order needs $N \gtrsim 10^3$ illuminated lines.
  - *verify:* `n_slit_intensity(n=2)` ≡ `double_slit_intensity`; peak height $N^2$ and
    fitted width exponent $-1$ in $N$ (`numerical-observation`); `grating_orders` vs
    the $|m| \le d/\lambda$ count (DVD at 650 nm: only $m = 0, \pm1$ propagate — the
    missing second order is *evanescent*, one sentence citing `19-evanescent`);
    resolving-power criterion reproduced numerically at $R = mN$ within one part in
    $N$.
  - *transfer:* capstone §35.3 (this lab grows into the full spectrometer design);
    `26-fabry-perot` backward (finite vs infinite; for $R \sim 10^6$ the étalon wins —
    one sentence why); `17-refraction` backward ($k_\parallel$ ledger closed);
    `03-fourier-series` (a periodic structure has a discrete angular spectrum);
    crystallography — Bragg is a 3-D grating (one sentence); spectrometers and telecom
    WDM demux as engineering payoffs.
  - *quiz:* more-slits MC (registry distractor); grating-equation numerics (CD/DVD);
    dispersion numeric; $R = mN$ design numeric; prism-vs-grating colour-order MC.
  - *explain:* why adding slits sharpens but does not move the maxima, with phasor
    polygons; why a grating disperses red *more* while a prism disperses blue more;
    what limits how fine a doublet your grating splits — and what you would change
    first.
  - *advanced:* blazed gratings — tilt each groove's facet so the *envelope* maximum
    (which normally wastes light on $m = 0$) is steered onto a chosen order: the
    comb ⊗ rect picture with the rect's phase ramped; efficiency qualitative; echelle
    mention (high $m$, crossed disperser).
- **Core derivations:** as in seeds, convention-compliant ($e^{\ii j\delta}$ under
  $e^{-\ii\omega t}$); the 26-parallel box tabulates: series length ($N$ vs ∞),
  weighting (equal vs $R^m$), peak shape ($\sin N/\sin$ vs Lorentzian), sharpness
  driver ($N$ vs finesse), resolving power ($mN$ vs $m\mathcal{F}$ — same *form*,
  cited to 26's `OBJ-26-5`).
- **Model specification draft:** System — $N$ identical parallel slits at pitch $d$
  (transmission-grating idealisation) under coherent plane-wave illumination;
  observables are far-field intensity, order angles, line separability. Dynamics —
  stationary. Boundary — Kirchhoff mask; $N_F \ll 1$; uniform illumination over
  exactly $N$ slits. Ensemble — deterministic; lab noise seeded. Ignored —
  groove-profile efficiency (blaze in advanced); polarization dependence of real
  gratings (one honesty sentence); reflection geometry (transmission taught; CD/DVD
  mapped onto it). Valid when — 29's far-field conditions; illumination spatially
  coherent across the $N$ slits (`27-coherence` caveat, one sentence). Failure modes —
  counting ruled instead of *illuminated* lines in $R = mN$; orders beyond
  $|m| \le d/\lambda$; blaming the grating for source-linewidth limits.
- **Epistemic classification:** grating equation — `theorem` (phase matching); $N$-slit
  sum and $1/N$ width — `theorem`; measured width exponent and $N^2$ peaks —
  `numerical-observation`; $R = mN$ — `theorem` (Rayleigh convention inherited from
  30, flagged); "uniform coherent illumination of exactly $N$ slits" —
  `model-assumption`; blaze efficiency — `empirical-law`-level engineering in
  advanced.
- **Misconceptions:** NEW **`more-slits-tighter-fringes`** — "Adding more slits at the
  same spacing squeezes the bright fringes closer together." Falsifying experiment:
  the $N$ slider at fixed $d$ — principal-maxima angles measurably fixed (the grating
  equation contains no $N$) while their width collapses as the fitted $1/N$; the
  polygon panel shows *why*. Distractor: quiz option "with 100 slits the maxima are
  50× closer together than with 2".
- **Glossary terms:** `diffraction-grating` (סריג עקיפה), `diffraction-order`
  (סדר עקיפה), `grating-equation` (משוואת הסריג), `angular-dispersion`
  (נפיצה זוויתית), `principal-maximum` (מקסימום ראשי), `secondary-maximum`
  (מקסימום משני), `blazed-grating` (סריג מולהב — translator to decide; `he_reject`
  candidate: סריג משופע), `grating-pitch` (מחזור סריג). Reuses part-08's
  `resolving-power` key (deposited by 26) — no new deposit, noted for `check_parity`.
- **Interactive controls and simulations:** $N$-slit dashboard (see explore); **virtual
  grating spectrometer** — source menu (HeNe, sodium doublet, unknown two-line, white
  light), pitch and illuminated width (hence $N$), order selector, detector sweep with
  resolution readout — the instrument the lab drives and §35.3 industrialises; CD/DVD
  mode with reflection-geometry sketch and measured dot angles.
- **Virtual lab outline** (`notebooks/en/labs/31-gratings.ipynb`): (1) $N$-sweep:
  peak height and width vs $N$, fit exponents ($+2$, $-1$) via
  `validation.scaling_exponent`; (2) *calibration:* HeNe line calibrates the angle axis
  against the grating equation; (3) *measurement* (the capstone seed): the sodium
  doublet at $m = 1$ with $N = 300, 600, 1200$ — unresolved, marginal, resolved; then
  $m = 2$, $N = 600$; tabulate against $R = mN$, report $\Delta\lambda \pm \sigma$
  where resolved (noise via `measurement.add_noise`); (4) *measurement:* CD/DVD —
  synthetic dot-angle data with jig tolerance, extract pitch: CD 1.6 µm
  ($\sin\theta = 0.41$, $\theta \approx 24°$ at 650 nm), DVD 0.74 µm
  ($\sin\theta = 0.88$, $\theta \approx 61°$; $m = 2$ evanescent) — both pitches ±
  uncertainty; (5) blaze demo (advanced): ramp the intra-slit phase, watch the envelope
  slide onto $m = 1$.
- **Real-experiment counterpart:** the module's centrepiece — laser pointer, a CD and a
  DVD, a wall and a tape measure: measure first-order angles, recover both pitches,
  compare with the 1.6 µm / 0.74 µm specifications; import the angles into the lab's
  uncertainty pipeline. (A 1000-lines/mm grating card, if available, adds $m = \pm1$
  symmetry checks.)
- **Media assets** (`render_diffraction.py`): (g) $N$ ramping 2 → 100 at fixed $d$:
  maxima frozen in place, sharpening, secondary maxima rippling between;
  (h) spectrometer sweep: the doublet's combs sliding apart as $m$ increases,
  merging/splitting at the $R = mN$ boundary. Language-neutral.
- **Quiz bank outline:** `Q-31-1` MC — effect of adding slits at fixed $d$ (OBJ-31-2,
  OBJ-31-3, distractor `more-slits-tighter-fringes`); `Q-31-2` numeric — CD pitch from
  a measured first-order angle (OBJ-31-1, OBJ-31-6); `Q-31-3` numeric — dispersion at
  given $d, m, \theta$ (OBJ-31-4); `Q-31-4` numeric — lines needed to resolve the
  sodium doublet at $m = 1$ (OBJ-31-5); `Q-31-5` MC — why the DVD has no second order
  (OBJ-31-1); `Q-31-6` MC — grating vs prism colour order (OBJ-31-4); `Q-31-7` free —
  the 26-parallel: same series, two instruments (OBJ-31-2).
- **Problem set outline:** analytical — secondary-maxima heights (~$1/N^2$ of
  principal); order overlap ($m = 2$ blue meets $m = 1$ red — the free-spectral-range
  idea, 26 echo); $R = mN$ from the width formula. Computational — spectrometer design
  brief: resolve a stated doublet within a footprint — choose $d$, $N$, $m$; grating
  with random line-position jitter (ghost/grass study, seeded). Challenge — blazed
  grating: implement the phase-ramped comb ⊗ rect, maximise order-1 efficiency vs
  blaze angle.
- **Runtime budget:** analytic formulas and 1-D FFTs ≤ $2^{14}$; $N \le 2000$ in
  direct sums; spectrometer sweeps ≤ 200 angles × 4 sources — all sub-second.
- **Validation gates:** standard set with `--module 31-gratings`; plus the $N = 2$
  reduction, order-count, and $1/N$-scaling tests of §4.
- **Open questions for the author:** whether the CD/DVD reflection-geometry mapping is
  a boxed aside or woven into derive (recommendation: boxed aside — the transmission
  form carries the theory); whether the order-overlap / free-spectral-range problem is
  promoted into core (recommendation: problem set — core already carries two
  instrument comparisons).

### 5.5 `32-fresnel-diffraction` — Fresnel diffraction: propagating the near field

- **Identity and scope:** master-plan notebook 9.7. The near field and the
  **angular-spectrum propagator** as the part's computational deliverable: decompose,
  multiply by $e^{\ii k_z z}$, recompose — exact scalar propagation at any distance;
  the near→far transition watched against the Fresnel number; validation against
  analytic Fresnel integrals (knife edge; Cornu spiral in advanced); sampling criteria
  as hard constraints; the arbitrary-aperture draw/upload playground (master plan §30)
  as the lab finale. Deferred: lenses in the propagation path → Part X/XI; holographic
  reconstruction → `50-holography`; inverse problems → `53-computational-imaging`.
- **Prerequisites:** `29-fraunhofer` (the far-field limit contained as a special case;
  $N_F$); `28-huygens` (the wavelet sum reorganised; the Poisson spot to re-derive);
  `04-fourier-transform` (`fourier.spectrum` conventions, sampling/aliasing/Nyquist —
  reused, not re-taught); `19-evanescent` (the imaginary-$k_z$ decaying branch,
  `interfaces.penetration_depth` — *the same mathematics*, cited); `13-dispersion`
  (phase accumulated per component — one-sentence analogy).
- **Learning objectives:**
  - `OBJ-32-1` — Decompose a monochromatic field in a plane into plane waves by FFT and
    interpret each (k_x, k_z) component as a propagation direction.
  - `OBJ-32-2` — Propagate exactly by multiplying each component by exp(i k_z z) with
    k_z = sqrt(k^2 - k_x^2), taking the decaying branch k_z = i sqrt(k_x^2 - k^2) for
    k_x > k, and state why those components die.
  - `OBJ-32-3` — Classify propagation regimes by the Fresnel number and locate the
    geometric-shadow -> Fresnel-ripple -> Fraunhofer transition in propagated data.
  - `OBJ-32-4` — Validate the numerical propagator against the analytic knife-edge
    solution and quantify the error and its convergence under grid refinement.
  - `OBJ-32-5` — State and apply the sampling constraints of FFT propagation
    (transfer-phase aliasing, zero padding) as hard validity conditions, and recognize
    their violation in artefacts.
  - `OBJ-32-6` — Compute the diffraction pattern of an arbitrary drawn or uploaded
    aperture at any chosen distance.
- **Mathematical background:** has — FFT mechanics, sampling and aliasing (04), complex
  square roots with a chosen branch (19); introduced here — the transfer-function view
  of propagation (free space is an LTI system in $x$, in module-05 vocabulary);
  discretisation error as a *physics* concern with named symptoms.
- **Physical intuition goals:** (1) free space is a filter: it delays every plane wave
  by its own phase and *deletes* the sub-wavelength ones — why no lens images below ~λ
  (door to Part XI; `19-evanescent` backward); (2) close behind an aperture the field
  still ripples — the geometric shadow is a fiction at every distance, decreasingly bad
  as $N_F$ grows; (3) one aperture, one knob ($z$): shadow → ripples → sinc²,
  continuously — Fraunhofer is not different physics, it is far away; (4) a numerical
  grid is an instrument with a validity range, like any lab instrument.
- **Section skeleton seeds:**
  - *puzzle:* module 29 computed the slit pattern "far away" — but a camera 2 mm behind
    the slit sees neither a clean shadow nor sinc lobes: it sees ripples that *change
    with every millimetre*. (Boxed: what does the field look like at *every* distance —
    and is there one method that is simply correct, near or far?) Secondary hook: the
    answer will independently settle whether 28's Poisson spot was real.
  - *predict:* (1) just behind a wide slit ($N_F \gg 1$): sharp-edged shadow, or
    already fringed? (targets `near-field-is-geometric-shadow`) (2) as $z$ grows, does
    the pattern change smoothly or switch regimes abruptly? (3) an aperture with
    0.1 µm features in 633 nm light: do those features reach any screen? (4) the FFT
    grid is made twice as coarse: can the *physics* output change?
  - *explore:* **the z-slider** — one aperture (slit / edge / disk / double slit /
    drawn), field propagated live to any $z$, with $N_F$ readout and a regime banner
    (shadow / Fresnel / Fraunhofer); the part's signature animation runs here as a
    scrubbable movie: shadow morphing through ripples to sinc² as $z$ grows;
    **angular-spectrum inspector**: $|F(k_x)|$ beside the field, evanescent band shaded
    and visibly dying with $z$; an "undersample" toggle that shows aliasing artefacts
    and names them.
  - *derive:* any field in the $z = 0$ plane = superposition of plane waves (FFT —
    module 04's theorem in space) → each component satisfies Helmholtz with
    $k_z = \sqrt{k^2 - k_x^2}$ → propagation = phase factor $e^{\ii k_z z}$ per
    component ($e^{\ii(k_z z - \omega t)}$, course convention) → for $|k_x| > k$:
    $k_z = \ii\sqrt{k_x^2 - k^2}$, the **decaying branch** — cite `19-evanescent` in
    exactly these words: *the same imaginary $k_z$, the same chosen branch, the same
    physics — features finer than λ do not propagate, they cling*
    (`interfaces.penetration_depth` as the quantitative crosslink) → the algorithm
    boxed: FFT → multiply → inverse FFT; exact within scalar theory → the ladder
    descended honestly: paraxial $k_z \approx k - k_x^2/(2k)$ gives **Fresnel**;
    dropping aperture-internal quadratic phase ($N_F \ll 1$) gives **Fraunhofer** — 29
    recovered as the bottom rung → the knife edge worked analytically:
    $I/I_0 = \tfrac12[(C(w) + \tfrac12)^2 + (S(w) + \tfrac12)^2]$,
    $w = x\sqrt{2/(\lambda z)}$ — $I_0/4$ at the geometric edge, first fringe
    overshooting to $\approx 1.37\,I_0$ (numbers the propagator must and does hit) →
    **sampling as physics**: the transfer phase must change by $< \pi$ between grid
    samples (else the quadratic phase aliases — rings that move with the grid), and
    the convolution wraps unless padded ×2 — hard constraints enforced by
    `propagation_sampling_ok`, rule of thumb $z \lesssim N\,\Delta x^2/\lambda$
    derived in one line.
  - *verify:* propagator vs `knife_edge_intensity` — max error and its convergence
    under grid refinement (`numerical-observation` box with the measured rate);
    $z \to 0$ identity; $N_F < 10^{-2}$ limit ≡ `fraunhofer_pattern`; propagating-band
    energy conserved at every $z$ (Parseval, evanescent split documented); **the
    Poisson spot re-derived**: `angular_spectrum_propagate` behind 28's disk reproduces
    the unit axial ratio — two independent methods, one answer, boxed as the part's
    internal consistency check.
  - *transfer:* Part XI wholesale — `38-spatial-frequencies` names what the inspector
    showed, `39-fourier-lens` puts a lens in this pipeline, `40-psf-otf` and
    `42-4f-processor` run on this propagator (id references); `50-holography`
    (propagate *backward*: $z < 0$ works — one astonishing sentence); `19-evanescent`
    backward (near-field optics: the clinging fields *can* be reached — NSOM, one
    sentence); `43-gaussian-beams` (a Gaussian propagated by this code stays Gaussian —
    the lab checks it); capstones §35.1/§35.5.
  - *quiz:* regime-classification numeric ($N_F$); evanescent-cutoff numeric;
    knife-edge value-at-edge MC; sampling-violation diagnosis MC; backward-propagation
    free item.
  - *explain:* why "the shadow region" is never dark-with-a-sharp-edge at any distance;
    why free space is a low-pass filter and what exactly it cuts; why a numerical
    result can be *wrong* while looking plausible — and which two checks catch it
    (analytic limit + grid refinement: the `validation` culture, named).
  - *advanced:* the **Cornu spiral** — plot $(C(w), S(w))$: the knife-edge field is a
    chord of a double spiral, and the spiral *is* module 00's tip-to-tail polygon for a
    continuum of wavelets, curled by quadratic phase (the part's two bookend pictures
    joined); fringe positions read off the spiral; transfer-function vs
    impulse-response implementations of Fresnel propagation and when each samples well
    (the classic numerical-optics trade); off-axis/tilted-plane propagation as
    literature pointers.
- **Core derivations:** (1) the angular-spectrum theorem (decompose–multiply–
  recompose), branch choice boxed; (2) the paraxial ladder with explicit error terms
  ($\theta^2$ paraxial; $\pi N_F/4$ Fraunhofer — 29's number recalled); (3) knife edge
  via Fresnel integrals with the stated values ($I_0/4$; $1.37 I_0$); (4) sampling
  constraints from the phase-increment argument; (5) the free-space transfer function
  as the convolution theorem's payoff: propagation in $x$-space is convolution with a
  chirp — `fourier.convolve`'s contract, in space.
- **Model specification draft:** System — a monochromatic scalar field sampled on a
  uniform 1-D or 2-D grid in a source plane, propagated through vacuum to parallel
  planes. Dynamics — stationary; evolution in $z$ via the exact transfer factor.
  Boundary — the computational window: implicitly periodic (the FFT's fiction,
  inherited from 04's DFT honesty), mitigated by zero padding; apertures as thin masks.
  Ensemble — deterministic; the speckle seed test is the one stochastic use. Ignored —
  polarization; backward waves ($+z$ only in core); media other than uniform index.
  Valid when — features ≳ λ for quantitative results; `propagation_sampling_ok` passes;
  window padded so wraparound stays below tolerance. Failure modes — aliased quadratic
  phase read as fringes; wraparound ghosts; trusting evanescent-band content at
  $z > 0$; comparing patterns across grids without refinement checks.
- **Epistemic classification:** angular-spectrum propagation — `theorem` (exact within
  scalar theory; the module's spine); paraxial/Fraunhofer rungs — `approximation`
  (each with its boxed edge); knife-edge overshoot and convergence rate —
  `numerical-observation`; thin-mask aperture and the periodic window —
  `model-assumption`; sub-λ imaging impossibility *for propagating fields* — `theorem`
  with an `open-question` pointer (near-field methods; `19-evanescent` backward).
- **Misconceptions:** NEW **`near-field-is-geometric-shadow`** — "Close behind an
  aperture the light is just the geometric shadow; diffraction only appears far away."
  Falsifying experiment: propagate a wide slit to $N_F = 100$: edge fringes are
  already there (the knife-edge overshoot to $1.37 I_0$ sits within microns of the
  edge), and the z-slider shows ripples at *every* $z$ — the shadow never was clean.
  Distractor: quiz option "for $N_F \gg 1$ the screen shows a sharp-edged copy of the
  aperture with no fringes".
- **Glossary terms:** `fresnel-diffraction` (עקיפת פרנל), `near-field` (שדה קרוב),
  `angular-spectrum` (ספקטרום זוויתי), `plane-wave-decomposition`
  (פירוק לגלים מישוריים), `transfer-function` (פונקציית תמסורת — translator to
  confirm), `knife-edge-diffraction` (עקיפת קצה סכין), `cornu-spiral`
  (ספירלת קורנו), `geometric-shadow` (צל גאומטרי). Reuses `evanescent-wave` (part-06)
  and module 04's sampling vocabulary — no re-deposit, noted for `check_parity`.
- **Interactive controls and simulations:** the z-slider rig (aperture preset + drawn
  mask; $z$ log slider 0.1 mm–10 m; $N_F$ readout; regime banner); angular-spectrum
  inspector (evanescent band shaded, live decay); undersample toggle (artefact
  literacy); **aperture playground** — paint tool on a $512^2$ canvas + image upload
  (`from_image`), propagate anywhere — master plan §30's aperture list (slit, double
  slit, square, circle, triangle, grating, arbitrary drawing, uploaded image) in one
  widget.
- **Virtual lab outline** (`notebooks/en/labs/32-fresnel-diffraction.ipynb`): (1) knife
  edge: propagate, overlay `knife_edge_intensity`, measure max error; refine the grid
  ×2, ×4, log convergence (the `validation.convergence_study` culture as a lab
  exercise); (2) *measurement:* the near→far transition — central-lobe width vs $z$
  for a fixed slit; identify the $N_F \sim 1$ crossover; fit the far-field asymptote
  against 29's fit; (3) Poisson closure: re-derive 28's spot with the propagator,
  report the axial ratio ± numerical error — the two-method box completed by the
  student; (4) break it on purpose: violate `propagation_sampling_ok`, catalogue the
  artefacts (aliased rings, wraparound ghosts) — instrument literacy as a deliverable;
  (5) *finale:* the aperture playground — draw an initial, upload a logo, propagate to
  three distances, annotate which regime each shows (open exploration credit).
- **Real-experiment counterpart:** laser pointer + razor blade: photograph the shadow
  edge at 0.5–2 m — the Fresnel fringes on the bright side are visible in a phone
  photo; import an intensity row and overlay `knife_edge_intensity` scaled to the
  geometry (one free parameter: overall intensity). The cheapest quantitative
  Fresnel-diffraction measurement there is.
- **Media assets** (`render_diffraction.py`): (i) **the part's signature shot** —
  single slit, camera plane sweeping $z$ over four decades: shadow → ripples → sinc²,
  with an $N_F$ dial spinning down (numeric dial, language-neutral); (j) Cornu spiral
  tracing the knife-edge profile — chord sweeping as the observation point crosses the
  edge.
- **Quiz bank outline:** `Q-32-1` MC — field just behind a wide slit (OBJ-32-3,
  distractor `near-field-is-geometric-shadow`); `Q-32-2` numeric — evanescent or
  propagating for given feature size and λ (OBJ-32-2); `Q-32-3` numeric — classify
  three $(a, z)$ geometries by $N_F$ (OBJ-32-3); `Q-32-4` MC — intensity exactly at
  the geometric edge (OBJ-32-4); `Q-32-5` MC — a propagated pattern changes when the
  grid is coarsened: physics or artefact, and which check decides (OBJ-32-5);
  `Q-32-6` free — the algorithm in three sentences: decompose, delay, recompose — and
  why it is exact (OBJ-32-1, OBJ-32-2); `Q-32-7` free — what free space filters out
  and what that implies for the smallest detail any far screen can show (OBJ-32-2,
  OBJ-32-6).
- **Problem set outline:** analytical — on-axis intensity behind a circular aperture
  vs $z$ (oscillating between $0$ and $4I_0$ — zones revisited exactly); the paraxial
  error bound; derive the $z \lesssim N\Delta x^2/\lambda$ sampling rule.
  Computational — Talbot carpet: propagate a grating, find the self-imaging distance
  $z_T = 2d^2/\lambda$ (a spectacular free discovery); Gaussian self-similarity check
  (43 teaser). Challenge — backward propagation: reconstruct the aperture from a far
  pattern's full complex field; then magnitude only — meet the phase problem
  (`ft-discards-time`'s spatial twin, cited; door to `53-computational-imaging`).
- **Runtime budget:** the hard budget of the part — live 2-D FFTs capped at $1024^2$
  including padding (≈ 0.5–2 s per shot in Pyodide; the z-slider updates on release,
  not drag); playground canvas $512^2$ (padded $1024^2$); the signature near→far
  animation and any heavier shot precomputed by `render_diffraction.py` and shipped as
  MP4; 1-D studies at $2^{14}$ samples — milliseconds.
- **Validation gates:** standard set with `--module 32-fresnel-diffraction`; plus §4's
  knife-edge convergence, $z \to 0$ / Fraunhofer limits, Parseval, and speckle-seed
  tests — this module lands the propagator's full guarantee set, cited by parts X–XII.
- **Open questions for the author:** whether the Talbot carpet is promoted from
  problem set to explore preset (recommendation: problem set first build — gorgeous
  but optional); whether the playground ships an upload-size guard (recommendation:
  yes — downsample to $512^2$ on import, stated in the UI); whether backward
  propagation appears in core transfer or only the challenge (recommendation: one
  transfer sentence; `50-holography` owns it).

## 6. Part-level assessment and capstone hooks

- **Capstones fed:** §35.3 (grating spectrometer) is seeded directly by 31's virtual
  spectrometer lab — the capstone adds detector sampling, wavelength range, and trade
  studies to an instrument already driven; §35.1 (computational telescope) consumes
  30's Airy-disk-as-PSF and 32's propagator, Part XI supplying the imaging chain;
  §35.5 (4-f processor) runs on 29's transform relation and 32's propagation code;
  §35.2 (virtual optical bench) lists Fresnel and Fraunhofer propagation among its
  models — both are `diffraction.py` calls.
- **Cross-module synthesis problems** (live with the part, not one module): (a) *the
  Poisson dossier* — predict the spot by zones (28), compute it by wavelet quadrature
  (28) and by angular spectrum (32), measure it with a ball bearing (28's real
  experiment), and write the epistemology paragraph: one phenomenon, three
  derivations, one measurement; (b) *two roads, one pattern* — compute one aperture by
  Hecht's route (wavelet sum) and Goodman's route (`fraunhofer_pattern`), quantify the
  agreement and state each method's validity domain — master plan §30's textbook
  transition as an exercise; (c) *the §26.4 open investigation in full* — the 10-mm
  telescope across wavelength, analytic + computational + experimental-reasoning
  writeup; (d) *resolve it twice* — the sodium doublet with 31's grating and 26's
  Fabry–Pérot: compare $R = mN$ against $R = m\mathcal{F}$, cost out both instruments
  (bridges part VIII, closes the finite/infinite-sum arc).
- **Exam themes:** regime classification by $N_F$ under time pressure; pair-zoo pattern
  sketching (aperture given, pattern sketched, and the reverse); missing-order and
  $d/a$ forensics; Rayleigh and $R = mN$ design numerics with order-of-magnitude
  sanity checks; "which method computes this correctly" (wavelet / Fraunhofer /
  angular spectrum — validity-domain judgement).

## 7. Build order and validation gates

Build order `28 → 29 → 30 → 31 → 32` — teaching order and dependency order aligned: 28
supplies the principle and the transparent summation engine; 29 takes its far-field
limit and must exist before any envelope talk; 30 needs 29's envelope and 23's fringes
(part-08 built first — the handoff lands cleanly); 31 needs 30's comb ⊗ rect; 32 needs
29's limit to have something to transcend, and closes the part by re-deriving 28's
centerpiece.

With `28-huygens`: create `content/en/diffraction/`, land **`diffraction.py` in full
skeleton** — the file-level model spec plus `wavelet_sum`, the aperture builders,
`fresnel_number`, *and* a working `angular_spectrum_propagate` (28's Poisson-spot media
render and lab cell (5) need it; its *pedagogy* waits for 32 — ownership and spec live
in this plan either way, single-owner rule intact) — with 28's §4 tests
(wavelet convergence, Poisson ratio); deposit 28's glossary terms; add NEW registry
entry `obstacle-only-darkens`. With `29-fraunhofer`: `fraunhofer_pattern`,
`sinc_intensity`, the slit-limit/Parseval/scaling tests; apply the README conflict-log
re-pointing `narrow-slit-narrow-pattern` → `29-fraunhofer` (one-line `assigned_module`
edit; status → `addressed` when `Q-29-1` exists); the built `00-phasors` page's
"module 9" prose drift (README conflict log) becomes fixable now — apply with this
module. With `30-apertures`: `double_slit_intensity`, `airy_pattern`, `airy_radius`,
`rayleigh_criterion`, their tests, NEW entry `resolution-improves-with-magnification`.
With `31-gratings`: `n_slit_intensity`, `grating_orders`, `angular_dispersion`,
`resolving_power`, tests, NEW entry `more-slits-tighter-fringes` (31 deposits no
`resolving-power` glossary key — part-08/26 owns it). With `32-fresnel-diffraction`:
`propagation_sampling_ok`, `fresnel_integrals`, `knife_edge_intensity`, `from_image`,
and the propagator's full §4 guarantee set (knife-edge convergence, limits, Parseval,
speckle seeds) — these must land *with* 32, since parts X–XII cite them by name; NEW
entry `near-field-is-geometric-shadow`. All NEW registry entries land status `pending`,
flipped to `addressed` with their quiz distractors.

Per module: the standard four gates (README). Additionally: the four
course-fixed signatures (`fraunhofer_pattern`, `angular_spectrum_propagate`,
`airy_radius`, `rayleigh_criterion`) are frozen API — any change requires
re-coordination with parts X–XII, and the physics tests double as their contract
tests.

## 8. Deviations from the master plan

- **Merge (9.2 + 9.3 → `29-fraunhofer`):** the far-field transform relation and the
  single slit are one lesson — §31 demands sinc² arrive as *recognition* of the
  module-04 pair, which requires the relation and its payoff on one page. Precedent:
  `02-damped-driven` ← 1.2 + 1.3. Canonical per README module map.
- **Merge (9.4 + 9.5 → `30-apertures`):** both notebooks are the convolution theorem
  made visible (compound aperture → product of transforms); the double slit's envelope
  and the Airy pattern share one lab pattern and one derivation engine. Canonical per
  README module map.
- **Part-08 handoff landed:** the finite-slit-width double slit (master plan 9.4's
  core), deferred by `23-interference` (part-08 §5.1 and §8), is owned here by
  `30-apertures` — honoured explicitly in 30's identity, puzzle, and verify (the cos²
  factor *cited* from `interference.young_pattern`, never re-derived).
- **Registry re-pointing:** `narrow-slit-narrow-pattern` moves `09-diffraction` →
  `29-fraunhofer` per the README conflict log; the one-line edit lands with 29 (§7).
- **Method choice for 9.7:** the master plan says "numerically propagate fields
  between planes"; this plan fixes the method as the **angular-spectrum propagator**
  (Goodman) rather than direct Fresnel-integral quadrature — exact within scalar
  theory, one code path for all regimes, and the Fraunhofer limit falls out of it.
  Direct quadrature survives as 28's pedagogical `wavelet_sum`.
- **Additions beyond the master plan:** the Poisson–Arago spot as simulated historical
  centerpiece with an epistemology box (9.1 says only "secondary-wavelet intuition");
  the honest Fraunhofer condition as a Fresnel-number inequality, threaded through
  29–32; missing orders as designed discovery; the real-number Rayleigh table
  including §26.4's 10-mm telescope; the finite-vs-infinite phasor-sum parallel with
  `26-fabry-perot`; the CD/DVD track-pitch experiment; the sodium-doublet spectrometer
  lab as capstone §35.3's seed; sampling constraints as hard validity conditions with
  `propagation_sampling_ok`; Babinet, blazed gratings, the Cornu spiral, and the
  Talbot carpet in advanced/problems; four NEW registry misconceptions plus the
  claimed re-pointing.
- **Terminology:** $\operatorname{sinc}(x) = \sin x/x$ (unnormalised) is fixed
  course-wide, matching `fourier.sinc_spectrum` and Hecht's $\beta$ notation; the
  `numpy.sinc` normalisation trap is documented in `diffraction.py`'s docstring.
  "Airy pattern" (this part) vs "Airy function" (part-08's Fabry–Pérot) are distinct
  glossary entries with mutual disambiguation. "Spatial frequency" as a *term* is
  withheld until `38-spatial-frequencies` — here $k_x = k\sin\theta$ is a direction.
- **Convention note:** all seeded formulas carry the course phase convention
  ($e^{\ii(kx-\omega t)}$, time factor $e^{-\ii\omega t}$, propagator phase
  $e^{\ii k_z z}$ with the decaying evanescent branch, spatial transform kernel
  $e^{-\ii k_x x}$ matching `fourier.spectrum`'s forward sign) — where Hecht's
  $e^{\ii(\omega t - kx)}$ pages are companion reading, the conventions page is the
  arbiter, as everywhere in the course.
