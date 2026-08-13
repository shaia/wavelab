# Part XI — Fourier Optics and Imaging — Implementation Plan

> **Master plan:** §18 (Part XI). **Modules:** `38-spatial-frequencies`, `39-fourier-lens`, `40-psf-otf`, `41-imaging-coherence`, `42-4f-processor`. **Status:** planned.
> Canonical numbering, invariants, and conflict log: [README.md](README.md).

## 1. Part overview and narrative arc

Part XI is where the course closes the loop it opened in module `00-phasors`. The
escalating claim of Part 0 — *any signal is a sum of rotating arrows* — has climbed from
arrows (00) to signals (03, 04) to waves (Part III) to light (Parts V–IX). Here it reaches
its final costume: **an image is a sum of spatial Fourier components, and a lens is the
machine that computes the sum.** Nothing in this part is new mathematics. The 2-D
transform is `04-fourier-transform` with two axes; the point spread function is
`05-impulse-response`'s Green function with $t \to (x,y)$; the coherent/incoherent
boundary is `27-coherence` moved from the source to the image plane; the Airy pattern is
`30-apertures` read as a transfer function. What *is* new is the realisation that light
performs this mathematics physically — the back focal plane of a lens is a place you can
put your finger, and what lives there is a Fourier transform.

This is also where the textbook baton passes: Hecht's Fourier-optics chapter bridges into
Goodman, who is the companion for all five modules (per-module chapter topics in §3, per
master plan §18 and §30). The course convention stays fixed — $e^{\ii(kx-\omega t)}$,
time factor $e^{-\ii\omega t}$ — and Goodman is read through the standing $j
\leftrightarrow -\ii$ dictionary of `content/en/conventions.md`; §5.2 flags the one place
(quadratic phases and transform kernels under an engineering $e^{+j\omega t}$ time
factor) where a careless mixture flips a sign and silently conjugates every spectrum.

The five modules run as one argument. **38** establishes that a picture *is* a spectrum:
2-D transforms, spatial frequency in cycles/mm with gratings as the pure tones
(`31-gratings` in reverse), orientation as direction in the transform plane, pixels as
spatial sampling with moiré as `04`'s aliasing photographed. **39** is the part's
conceptual event: the lens as an *analog Fourier computer*, derived Goodman's way —
Fresnel-propagate $f$ → quadratic lens phase → $f$, watch the quadratic phases cancel
exactly, leaving the pure transform with scaling $\nu = x/(\lambda f)$ — and read
historically through Abbe's theory of the microscope. **40** keeps the promise
`05-impulse-response` made in its transfer section, loudly: imaging is convolution, the
PSF is the optical Green function, the OTF is $\hat{H}$ with two axes, and resolution is
a frequency response you can *measure* from noisy bar-target data. **41** does the
coherent/incoherent split honestly — linear in field vs linear in intensity, pupil vs
pupil-autocorrelation, ringing vs 2× cutoff — and crowns it with speckle, whose
statistics are module 00's random walk verbatim. **42** is the course's summit lab: the
4-f processor, where the student reaches into a physical Fourier plane with a mask and
edits an image's spectrum by hand — Abbe–Porter's 1906 grid experiment, Zernike's
phase-contrast Nobel trick, low-pass, high-pass, and directional filtering, all in one
apparatus.

The part plants seeds deliberately: capstone §35.1 (computational telescope) is module 40
scaled up — scene → aperture → PSF → sensor with aberrations and noise; capstone §35.5
(Fourier-optics image processor) *is* module 42 scaled up, and both plans say so in
content. `50-holography` inherits the Fourier-plane field (record it, don't just
intensity-detect it); `53-computational-imaging` inherits deconvolution where module 40's
MTF nulls make it hurt; `43-gaussian-beams` inherits the quadratic-phase reflexes of 39.
Every formalism the course has built — phasors, Fourier pairs, convolution, LTI response,
coherence, diffraction — is used *simultaneously* here. That is the pedagogical point:
Part XI is not another topic; it is the course, integrated.

## 2. Position in the course

- **Requires:**
  - `04-fourier-transform`: the pair zoo (rect ↔ sinc, Gauss ↔ Gauss, comb ↔ comb),
    the convolution theorem in both directions, `fourier.spectrum` scaling discipline,
    aliasing/Nyquist (module 38 replays it in space), and the `ft-discards-time` lesson
    (module 38 restages it as phase-vs-magnitude in images).
  - `05-impulse-response`: the LTI bridge — $G(t)$, $x = G*F$, $\hat{G} = \hat{H}$, and
    its transfer-section promise "$G$ is the point spread function of time, $\hat{H}$
    the OTF; imaging is this module with $t \to (x,y)$" — module 40 is that sentence
    made a module. The $\hat{G} \leftrightarrow \hat{H}$ identity test of part-01 §4 is
    cited as the LTI-bridge guarantee.
  - `29-fraunhofer` / `30-apertures` / `31-gratings` (dictated names only):
    `diffraction.fraunhofer_pattern` (far field = 2-D transform of the aperture),
    `diffraction.airy_radius` and `diffraction.rayleigh_criterion` (module 40's
    clear-pupil limits), the grating-equation dots (modules 38/39 reuse "a grating is a
    single spatial frequency"), `diffraction.angular_spectrum_propagate` (module 39's
    numerical engine; `32-fresnel-diffraction` context).
  - `27-coherence`: visibility, $\gamma(\tau)$, Wiener–Khinchin,
    `interference.degree_of_coherence`, `interference.partial_coherence_source`, and
    the deferred promise "van Cittert–Zernike as an imaging theorem →
    `41-imaging-coherence`" — module 41 collects it.
  - `34-lenses` / `35-abcd-matrices` / `36-instruments` (part-10): image formation,
    conjugates, `rayoptics.thin_lens` / `free_space` / `cascade` (dictated names; 39's
    ray-picture cross-check), numerical aperture and the microscope layout;
    `37-aberrations`: wavefront error and the Zernike research-connection trailer whose
    machinery lands in module 40.
  - `00-phasors` / `03-fourier-series`: `phasors.random_phasor_sum` and the $\sqrt{N}$
    random walk (41's speckle statistics); `fourier.gibbs_overshoot` and the 8.95%
    overshoot (41's coherent edge ringing is Gibbs in space).
- **Feeds:**
  - `43-gaussian-beams`: quadratic phases as the natural habitat of beams; the Fourier
    plane as the far field brought close.
  - `50-holography`: recording the Fourier-plane *field* (amplitude and phase), not its
    intensity; the VanderLugt correlator (42's advanced box) is its front door.
  - `53-computational-imaging`: deconvolution against the measured MTF; where OTF nulls
    (40's defocus experiment) make inversion ill-posed — 05's deconvolution wreckage,
    now in space.
  - Capstones §35.1 (computational telescope — direct consumer of 40's PSF/OTF chain
    plus 37's aberrations), §35.5 (4-f image processor — module 42 scaled up), §35.2
    (virtual optical bench — 39's propagate–lens–propagate chain as one of its engines).
- **Explicitly not assumed:** Fresnel-integral evaluation beyond what
  `angular_spectrum_propagate` encapsulates (32's machinery is called, not re-derived);
  vector diffraction and high-NA corrections (scalar throughout, flagged in every model
  spec); partial-coherence *calculus* (mutual coherence propagation / TCC — 41 keeps
  partial coherence qualitative, §8); photon statistics (`52-quantum-optics`);
  statistical-optics formalism beyond the single-point speckle distribution.

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|
| `38-spatial-frequencies` | `content/en/fourier-optics/38-spatial-frequencies.md` | Spatial frequencies: a picture is a spectrum | 11.1 | Goodman, 2-D signal analysis; Hecht, Fourier-optics introduction | planned |
| `39-fourier-lens` | `content/en/fourier-optics/39-fourier-lens.md` | The lens as an analog Fourier computer | 11.2 | Goodman, wave-optics analysis of coherent systems (Fourier-transforming property of a lens); Hecht, lens-transform sections | planned |
| `40-psf-otf` | `content/en/fourier-optics/40-psf-otf.md` | PSF and OTF: resolution as frequency response | 11.3 + 11.4 | Goodman, frequency analysis of imaging systems; Hecht, resolution & imagery | planned |
| `41-imaging-coherence` | `content/en/fourier-optics/41-imaging-coherence.md` | Coherent and incoherent imaging — and speckle | 11.5 | Goodman, coherent vs incoherent frequency response; Goodman, speckle statistics (statistical-optics companion) | planned |
| `42-4f-processor` | `content/en/fourier-optics/42-4f-processor.md` | The 4-f processor and spatial filtering | 11.6 | Goodman, analog optical information processing; Hecht, optical data processing | planned |

## 4. Shared infrastructure for this part

**`src/wavelab` — existing used:** `diffraction.fraunhofer_pattern`,
`diffraction.angular_spectrum_propagate`, `diffraction.airy_radius`,
`diffraction.rayleigh_criterion` (dictated names, owned by part-09 — 39's propagation
engine and 40's clear-pupil limits); `rayoptics.thin_lens`, `rayoptics.free_space`,
`rayoptics.cascade` (dictated names, owned by part-10 — 39's and 42's ray-picture
cross-checks); `fourier.spectrum` / `rect_pulse` / `sinc_spectrum` /
`gaussian_pulse` / `gaussian_spectrum` (1-D separable cross-checks of the 2-D wrappers),
`fourier.gibbs_overshoot` (41's edge-ringing comparison); `oscillators.impulse_response`
(40's side-by-side time/space LTI figure — by name only, owned by part-01);
`phasors.random_phasor_sum` (41's speckle statistics precedent);
`interference.degree_of_coherence`, `interference.partial_coherence_source`,
`interference.visibility` (41's partial-coherence bridge); `measurement.add_noise` +
fit helpers (bar-target/edge MTF measurement, all labs); `validation.scaling_exponent`,
`convergence_study`, `seed_study`, `relative_error`.

**`src/wavelab` — new: `imaging.py`** (introduced and owned by this part; README
ownership table — serves 38–42). **Design decision (logged in §8): all 2-D transform
machinery lives here.** `fourier.py` remains 1-D and untouched; the 2-D wrappers below
are the single home for centred, physically scaled 2-D FFTs, and part-13's
`53-computational-imaging` builds on them. Docstring model spec:

- **System:** scalar monochromatic optical fields on uniform 2-D grids — object
  transparencies, pupils, PSFs, and images — with physical sampling `dx` [m] and
  spatial-frequency axes in cycles/m.
- **Dynamics:** none integrated — Fourier-domain propagation and thin-element phase
  screens; imaging as convolution (field or intensity per coherence state).
- **Boundary:** grids are finite and periodic under the FFT (wrap-around is the standing
  caveat); pupils and masks are hard-edged arrays; elements are thin (a single complex
  transmittance per plane).
- **Ensemble:** deterministic by default; speckle and rough surfaces via seeded
  random-phase screens; noise only via `wavelab.measurement`.
- **Ignored:** polarization and vector diffraction; energy lost outside the grid;
  multiple reflections between elements; anything non-monochromatic unless the caller
  loops wavelengths; quantum statistics.
- **Valid when:** paraxial (angles small, $\mathrm{NA} \lesssim 0.3$ for quantitative
  claims); features ≥ a few grid samples and grids ≥ a few features (guard band against
  wrap-around); scalar approximation valid (features ≫ λ where amplitudes are read
  literally).
- **Failure modes:** aliasing/wrap-around read as physics (thin bright frame at the grid
  edge); mixing the coherent and incoherent pipelines (fields convolved where
  intensities are required, or vice versa); trusting paraxial quadratic phases at high
  NA; single speckle realisations read as ensemble averages.

Function-level sketch (signatures + contracts):

```python
fft2_centered(field, dx) -> (nu_x, nu_y, F)   # centred 2-D FT; axes in cycles/m; Parseval-preserving
                                              #   scaling (F carries dx*dx); forward kernel matches
                                              #   fourier.spectrum's sign convention, axis by axis
ifft2_centered(F, dnu) -> (x, y, field)       # inverse; round-trips fft2_centered to machine precision
lens_phase(x, y, f, lam) -> t                 # thin-lens transmittance exp(-i k (x^2+y^2)/(2 f));
                                              #   converging for f > 0 under the course e^{+i k z} forward phase
fourier_plane_field(obj, dx, f, lam) -> (u, v, U)
                                              # front-focal-plane object -> back-focal-plane field via
                                              #   f -> lens_phase -> f with angular_spectrum_propagate;
                                              #   equals fft2_centered up to the constant 1/(i lam f),
                                              #   with u = lam * f * nu_x (the scaling law, tested)
pupil_disk(n, dx, radius) -> P                # circular pupil array, 1 inside, 0 outside; the clear aperture
zernike_phase(n_rad, m_azi, npix) -> W        # Zernike polynomial on the unit disk (OSA/ANSI normalised);
                                              #   defocus is (2, 0) — the machinery 37's trailer deferred here
psf_from_pupil(pupil, dx, lam, f) -> (x, y, psf)
                                              # coherent amplitude PSF h = scaled FT of pupil; returns
                                              #   |h|^2 normalised to unit volume (intensity PSF)
amplitude_psf(pupil, dx, lam, f) -> (x, y, h) # the complex h itself (41's coherent pipeline needs the field)
otf_from_psf(psf) -> (nu_x, nu_y, otf)        # normalised FT of the intensity PSF; otf[0,0] == 1 exactly
mtf(otf) -> M                                 # |otf|; the measurable modulus
image_coherent(obj, pupil, dx, lam, f) -> img # field pipeline: (E_obj * h), intensity taken LAST; obj is
                                              #   complex transmittance (phase objects welcome)
image_incoherent(obj, psf) -> img             # intensity pipeline: I_obj convolved with psf via FFT;
                                              #   energy-conserving for unit-volume psf
speckle_field(n, dx, grain, seed) -> E        # unit-mean-intensity fully developed speckle: random-phase
                                              #   screen low-pass filtered to grain size; seeded
speckle_contrast(I) -> C                      # std(I)/mean(I); -> 1 for fully developed speckle
four_f_process(obj, mask, dx, lam, f) -> (img, U_fourier)
                                              # object -> lens -> Fourier plane -> mask -> lens -> image;
                                              #   returns the (inverted) image and the pre-mask Fourier field;
                                              #   mask == 1 reproduces the object flipped, energy conserved
lowpass_mask(n, dnu, cutoff) -> mask          # circular pass-band, 1 inside cutoff [cycles/m]
highpass_mask(n, dnu, cutoff) -> mask         # 1 - lowpass_mask; blocks DC by construction
directional_mask(n, dnu, angle, halfwidth) -> mask
                                              # angular wedge pass-band (+ its mirror); Abbe-Porter's slit
phase_dot(n, dnu, radius, phase=np.pi/2) -> mask
                                              # complex mask: exp(i*phase) inside radius, 1 outside —
                                              #   Zernike's phase-contrast plate (attenuation optional arg)
bar_target(n, dx, periods) -> obj             # three-bar resolution target at given spatial periods [m]
spoke_target(n, dx, n_spokes) -> obj          # Siemens star; radius sweeps all spatial frequencies at once
edge_target(n, dx, angle=5.0) -> obj          # slanted-edge target for the ESF -> LSF -> MTF chain
```

**`tests/physics/` additions:**

- *limits:* `psf_from_pupil(pupil_disk(...))` first dark ring at
  `diffraction.airy_radius` and radial profile matching
  `diffraction.fraunhofer_pattern` of the same disk (the clear-pupil PSF *is* the Airy
  pattern — cross-owner agreement, `<1e-8`); `otf_from_psf` gives `otf[0,0] == 1`
  exactly for any normalised PSF; 1-D slit pupil → triangle MTF $1 - |\nu|/(2\nu_0)$;
  measured incoherent cutoff = 2× the coherent cutoff of the same pupil (the module-41
  boundary as a test); `four_f_process(obj, mask=1)` returns the object rotated 180°
  to machine precision; `zernike_phase` orthogonality on the disk (`<1e-3` on a
  512-grid); separable-object `fft2_centered` = outer product of two
  `fourier.spectrum` calls.
- *conservation:* Parseval through `fft2_centered`/`ifft2_centered` (energy in the
  field = energy in the spectrum, both round-trip); energy through a lossless 4-f
  (`mask == 1`) conserved to `<1e-10`; `image_incoherent` conserves total intensity
  for unit-volume PSFs.
- *convergence:* PSF and MTF under grid refinement (256 → 512 → 1024) converge with
  the expected order via `validation.convergence_study`; `fourier_plane_field` vs
  direct `fft2_centered` agreement improves as the guard band grows (wrap-around
  quantified, not hidden).
- *scaling:* fitted exponents via `validation.scaling_exponent`: PSF width $\propto
  \lambda$ (+1), $\propto 1/D$ (−1), Fourier-plane feature position $\propto f$ (+1)
  — the $\nu = x/(\lambda f)$ law measured, not assumed.
- *seeds:* `speckle_field` intensity histogram fits the exponential
  $P(I) = e^{-I/\langle I\rangle}/\langle I\rangle$ (KS-test pass across seeds);
  `speckle_contrast` → 1 within $1/\sqrt{M}$ over $M$ realisations; exact
  reproducibility per seed.
- *dimensions:* `fft2_centered` axes in cycles/m against the `units` registry;
  `airy_radius` consistency check carries meters end-to-end; `lens_phase`
  dimensionless transmittance.

**Shared media:** one render script `media/render/render_fourier_optics.py` produces
all Part XI MP4s (shot lists in §5). **Glossary themes:** spatial-spectrum vocabulary
(38), lens-transform vocabulary (39), transfer-function vocabulary (40), imaging-
coherence vocabulary (41), filtering vocabulary (42) — per-module lists in §5.
`numerical-aperture` is cited from `36-instruments` (part-10's deposit); module 39
adds the imaging usage to the same key.

## 5. Module specifications

### 5.1 `38-spatial-frequencies` — Spatial frequencies: a picture is a spectrum

- **Identity and scope:** master-plan notebook 11.1. Images as superpositions of spatial
  Fourier components: the 2-D transform, spatial frequency in cycles/mm, orientation ↔
  direction in the transform plane, phase vs magnitude, pixels as spatial sampling with
  moiré as aliasing. Purely computational — no lens yet; the *optical* transform is
  deliberately deferred to `39-fourier-lens`, filtering consequences to `42-4f-processor`.
- **Prerequisites:** `04-fourier-transform` (transform pair, pair zoo, convolution
  theorem, aliasing/Nyquist — all replayed with two axes); `31-gratings` (the grating
  equation and its dot pattern — this module reads a grating as a single spatial
  frequency); `00-phasors` (a 2-D Fourier component is a phasor field
  $e^{\ii 2\pi(\nu_x x + \nu_y y)}$ — arrows tiled over a plane).
- **Learning objectives:**
  - `OBJ-38-1` — Define spatial frequency in cycles/mm, identify a sinusoidal grating of
    period d as the pure tone nu = 1/d, and locate it as a symmetric point pair at
    radius nu and the grating's orientation angle in the 2-D transform plane.
  - `OBJ-38-2` — Decompose and resynthesize an image with the 2-D Fourier transform,
    predicting which visual features (smooth shading, edges, texture, orientation) live
    at which radii and angles of |F(nu_x, nu_y)|.
  - `OBJ-38-3` — Demonstrate that spectral phase, not magnitude, carries an image's
    structure, by reconstructing from each alone and by swapping phase and magnitude
    between two images.
  - `OBJ-38-4` — Treat a pixel grid as 2-D sampling: state the Nyquist frequency
    1/(2 dx) per axis, predict when a fine pattern aliases into moire, and compute the
    false frequency it folds to.
  - `OBJ-38-5` — Apply the 2-D pair zoo (rect <-> 2-D sinc, Gaussian <-> Gaussian,
    disk <-> Airy-like ring pattern, comb <-> comb) and the rotation and separability
    theorems to sketch transforms without computing.
- **Mathematical background:** has — 1-D transform pair, convolution theorem, sampling
  (04); introduced here — the 2-D transform as two nested 1-D transforms
  (separability), the rotation theorem (rotate the image, the spectrum rotates with
  it), polar reading of $(\nu_x, \nu_y)$ as (how fine, which way).
- **Physical intuition goals:** (1) point at any image region and say where its energy
  sits in the transform plane — smooth sky at the centre, brick texture in a mid-radius
  cluster, sharp edge as a streak *perpendicular* to itself; (2) know without computing
  that killing the spectrum's centre leaves an outline sketch and killing its rim
  leaves a blur; (3) expect a striped shirt on a television to writhe with moiré, and
  say which way the false stripes tilt; (4) trust phase over magnitude — a spectrum's
  magnitude is a texture inventory, its phase is the picture.
- **Section skeleton seeds:**
  - *puzzle:* photograph a laptop screen with a phone: broad dark bands crawl across
    the picture that neither the screen nor the eye contains. Where is that pattern —
    in the screen, the camera, or the mathematics between them? (Boxed: what is the
    "frequency" of a *picture*, and what plays the role of Nyquist when the signal is
    made of pixels instead of samples in time?)
  - *predict:* (1) a vertical grating's transform: points along which axis? (2) two
    images: your face and white noise, magnitudes swapped, phases kept — which
    reconstruction shows the face? (restages `ft-discards-time` in space; expect the
    magnitude vote); (3) rotate the image 30° — what happens to its spectrum?
    (4) delete a 3-pixel dot at the spectrum's centre — a dot disappears from the
    image, the whole image dims, or something else? (targets NEW
    `spectrum-maps-image-locations`).
  - *explore:* **spectrum playground** — choose an image (built-ins: portrait, brick
    texture, `bar_target`, `spoke_target`, a hand-drawn canvas per master plan §30);
    live $|F|$ panel (log display, stated as such) via `fft2_centered`; brush to zero
    or keep spectral regions with instant `ifft2_centered` resynthesis; grating
    composer — stack up to 8 oriented sinusoids with sliders for $\nu$, angle,
    amplitude, phase and watch image and spectrum build together; **phase/magnitude
    lab** — the two-image swap as a one-click experiment; sampling panel — resample
    the image at coarser `dx`, watch fine patterns fold into moiré with the folded
    frequency predicted live.
  - *derive:* 1-D pair with $x$ in place of $t$ (nothing new, said explicitly — space
    has no arrow of time, so no causality baggage) → 2-D by separability →
    $F(\nu_x,\nu_y) = \iint f(x,y)\, e^{-\ii 2\pi(\nu_x x + \nu_y y)}\,dx\,dy$ with
    the inverse carrying $e^{+\ii 2\pi(\cdot)}$ <!-- sign-convention-exception on the
    synthesis kernel, as in 04 --> → a single oriented sinusoid ↔ a conjugate point
    pair (the grating as pure tone; `31-gratings` said the same thing with light) →
    rotation and similarity theorems → the 2-D pair zoo, each drawn: rect ↔ 2-D sinc
    (the crossed streaks), disk ↔ the ring pattern that module 40 will name as Airy,
    Gaussian ↔ Gaussian, 2-D comb ↔ comb (the pixel grid's own spectrum) → edges:
    a step along one direction decays as $1/\nu$ *perpendicular* to itself — why edges
    are streaks and why sharpness is expensive (03's smoothness ↔ decay, now with
    orientation) → sampling: multiply by the pixel comb, spectrum periodises,
    overlap = aliasing = moiré; the photographed screen worked as a worked example.
  - *verify:* separable products against two `fourier.spectrum` calls; rotation
    theorem measured (rotate, transform, compare); Parseval through `fft2_centered`
    (§4 conservation test in view); the phase/magnitude swap quantified — correlation
    of each reconstruction with each parent (`numerical-observation`: the
    phase-parent wins by an order of magnitude); moiré frequency vs the fold formula
    across a sweep of grating pitches.
  - *transfer:* `39-fourier-lens` — everything this module did with `fft2_centered`,
    a lens does with glass, at the speed of light; `40-psf-otf` — blur will be
    *described* in this plane; `42-4f-processor` — the brush-to-kill experiment will
    be rebuilt with a physical mask; `04-fourier-transform` backward — same theorems,
    same zoo, same aliasing, new axes; image compression (JPEG lives in exactly this
    plane — one honest paragraph); crystallography teaser: an X-ray pattern is a
    $|F|^2$ with the phase lost — the phase problem is `ft-discards-time` as a Nobel
    industry.
  - *quiz:* grating ↔ spectrum matching; phase-vs-magnitude MC (distractor from the
    swap); moiré fold numeric; zoo sketching MC; edge-orientation MC.
  - *explain:* why a checked shirt misbehaves on television; what the centre of the
    transform plane "sees" of the image; to a photographer — what sharpening does in
    this plane and why it amplifies noise; why the transform of *any* real image has
    point symmetry.
  - *advanced:* discrete geometry of the 2-D DFT — wrap-around, the guard band, and
    why `imaging.py` documents the thin bright frame failure mode; windowing in 2-D;
    a first look at radial power spectra and the $1/\nu^2$-ish statistics of natural
    images (why "natural images are mostly smooth" is a measurable claim,
    `numerical-observation`).
- **Core derivations:** (1) separability:
  $e^{-\ii 2\pi(\nu_x x + \nu_y y)} = e^{-\ii 2\pi\nu_x x}\,e^{-\ii 2\pi\nu_y y}$, so
  the 2-D transform is 1-D transforms along rows then columns — the implementation
  *is* the theorem (`fft2_centered` docstring cites it). (2) Oriented sinusoid
  $\cos[2\pi\nu_0(x\cos\theta + y\sin\theta)]$ ↔ $\tfrac12[\delta_{+} + \delta_{-}]$
  at radius $\nu_0$, angle $\theta$ — the grating as pure tone, boxed. (3) Rotation
  theorem by substitution. (4) Disk of diameter $D$ ↔ ring-lobed pattern with first
  zero at $\nu \approx 1.22/D$ — stated, plotted, and cross-checked against
  `diffraction.fraunhofer_pattern`; named "Airy" with a forward pointer to 40.
  (5) Sampling: $f_s = f \cdot \mathrm{comb}_{dx}$ ⇒ $F_s = F * \mathrm{comb}_{1/dx}$;
  fold formula $\nu_{\text{seen}} = |\nu - m/dx|$ minimised over integer $m$ — the
  moiré band spacing and tilt of the puzzle computed.
- **Model specification draft:** System — real or complex 2-D arrays as ideal
  transparencies on a uniform grid `dx`; observables are the array, its centred
  spectrum, and resyntheses. Dynamics — none; a change of representation. Boundary —
  the FFT's silent periodicity (the standing caveat, stated in-page). Ensemble —
  deterministic; the noise-image experiments use seeded fields. Ignored — light
  entirely (no propagation, no λ) — this module is mathematics wearing image clothes;
  display gamma and colour (grayscale only). Valid when — features ≥ a few samples and
  ≪ the grid; intensity treated as a linear quantity. Failure modes — aliasing read as
  image content; log-display magnitudes read as energy fractions; phase discarded by
  careless `abs()`.
- **Epistemic classification:** separability, rotation theorem, sampling theorem —
  `theorem`; "phase carries the picture" — `numerical-observation` (measured
  correlations; the general claim is heuristic and said so); "natural-image spectra
  fall roughly as a power law" — `empirical-law` (advanced); the pixel-comb model of a
  sensor — `model-assumption` (real sensors integrate over the pixel — one honest
  sentence, finite-aperture sampling deferred).
- **Misconceptions:** cites `ft-discards-time` (owned by 04) — restaged spatially by
  the phase/magnitude swap; the registry entry gains a cross-reference note, not a
  re-pointing. NEW **`spectrum-maps-image-locations`** — "Each point of the 2-D
  spectrum corresponds to a location in the image, so editing a spectral point edits
  one spot of the picture." Falsifying experiment: zero a single off-centre spectral
  point — a *global* sinusoidal ripple changes across the whole image, no spot
  appears or disappears; conversely, occlude one corner of the image and watch every
  spectral value change. Distractor: quiz option "removing the bright centre of the
  spectrum cuts a hole in the middle of the picture".
- **Glossary terms:** `spatial-frequency` (תדר מרחבי), `transform-plane` (מישור
  ההתמרה — translator to confirm vs מישור פורייה, coordinated with 39's
  `fourier-plane`), `spectral-phase` (מופע ספקטרלי), `moire` (מוארה; `he_reject`
  candidate: דוגמת סריג), `nyquist-frequency` cited (part-00 deposit), `sampling`
  cited (part-00 deposit), `separability` (פריקות — translator to decide),
  `dc-component` (רכיב ממוצע — translator to decide; `he_reject`: רכיב DC).
- **Interactive controls and simulations:** spectrum playground (image chooser +
  draw canvas; spectral brush radius/shape; keep/kill toggle; log/linear display);
  grating composer (≤ 8 components; $\nu \in [0.5, 64]$ cycles/image, angle 0–180°,
  amplitude, phase); phase/magnitude lab (image pair chooser, swap/isolate buttons,
  correlation readouts); sampling panel (`dx` decimation 1–8×, predicted vs measured
  moiré overlay).
- **Virtual lab outline** (`notebooks/en/labs/38-spatial-frequencies.ipynb`):
  (1) pure tones — compose gratings, locate their spectral points, verify radius =
  1/period and angle = orientation; (2) zoo gallery — rect/disk/Gaussian/comb
  transforms vs analytic overlays; (3) surgery — kill centre, kill rim, kill one
  angle band; describe each result before running (predictions logged);
  (4) phase/magnitude swap with correlation table (`numerical-observation` data);
  (5) *measurement:* sample a known grating at decreasing resolution, measure the
  moiré frequency vs the fold formula across pitches, fit and report; (6) real-data
  import: the student's own screen photograph — locate the moiré pair in its
  spectrum, infer the screen's pixel pitch ± uncertainty from it (measurement
  culture with a phone).
- **Real-experiment counterpart:** photograph a laptop/TV screen at several
  distances (the puzzle's own data); optionally a woven chair or window screen
  through the phone — import, transform, find the fabric's spectral points. Cost:
  a phone.
- **Media assets** (`render_fourier_optics.py`): (a) an image assembling itself
  from its Fourier components, lowest radius outward — sinusoid tiles washing in
  until the portrait snaps into recognisability; (b) moiré morph — a grating
  resampled at a sliding pitch, spectrum panels showing the replicas marching into
  overlap. Language-neutral, no burned-in text.
- **Quiz bank outline:** `Q-38-1` MC — grating orientation/period ↔ spectral pair
  (OBJ-38-1); `Q-38-2` MC — which surgery produced which image (OBJ-38-2); `Q-38-3`
  MC — phase/magnitude swap outcome (OBJ-38-3; distractor cites `ft-discards-time`);
  `Q-38-4` numeric — folded moiré frequency from pitch and `dx` (OBJ-38-4);
  `Q-38-5` MC — spectral-point surgery (OBJ-38-2; distractor
  `spectrum-maps-image-locations`); `Q-38-6` free — sketch and justify the transform
  of a tilted rect (OBJ-38-5).
- **Problem set outline:** analytical — rotation and similarity theorems from the
  definition; transform of an oriented cosine grating with phase; the 2-D comb pair
  and the fold formula. Computational — radial power spectrum of three image
  classes (portrait, texture, noise) with fitted slopes; anti-aliasing by pre-blur:
  choose the mildest Gaussian that kills a given moiré. Challenge — implement a
  crude "phase-retrieval by alternating projections" toy (Gerchberg–Saxton, 20
  lines) and watch it sometimes work — the crystallographer's phase problem made
  tangible.
- **Runtime budget:** all interactions on 256² grids (one FFT ≈ ms in Pyodide);
  labs up to 512²; the assembly animation pre-rendered. Comfortably in-browser.
- **Validation gates:** standard four with `--module 38-spatial-frequencies`; plus
  the §4 separability, rotation, and Parseval tests landing with this module.
- **Open questions for the author:** built-in portrait choice (needs a
  public-domain, culture-neutral image; a synthetic face avoids licensing);
  whether the drawing canvas ships in v1 (recommendation: yes — master plan §30
  asks for it and it is the stickiest control); log-display floor for $|F|$
  (recommendation: fixed −60 dB with the choice stated in the caption).

### 5.2 `39-fourier-lens` — The lens as an analog Fourier computer

- **Identity and scope:** master-plan notebook 11.2. The Fourier-transforming property
  of a single lens: derivation by quadratic-phase cancellation, the scaling law
  $\nu = x/(\lambda f)$, shift invariance of the Fourier-plane intensity, and Abbe's
  two-stage theory of image formation. Deferred: what happens *after* the Fourier
  plane (a second lens and a mask) → `42-4f-processor`; the system-level transfer
  function → `40-psf-otf`; recording the Fourier-plane field → `50-holography`.
- **Prerequisites:** `38-spatial-frequencies` (the 2-D transform and the grating as
  pure tone); `32-fresnel-diffraction` context via
  `diffraction.angular_spectrum_propagate` (dictated name — the numerical propagator
  is called, never re-derived); `34-lenses` / `35-abcd-matrices`
  (`rayoptics.thin_lens`, `free_space`, `cascade` — the ray cross-check);
  `31-gratings` (the order equation this module's dots must reproduce).
- **Learning objectives:**
  - `OBJ-39-1` — State and apply the Fourier-transforming property: for an object in
    the front focal plane, the back-focal-plane field is the 2-D Fourier transform of
    the object with spatial frequency mapped to position by nu_x = x / (lambda f),
    and compute where a given object feature lands.
  - `OBJ-39-2` — Derive the property by propagating focal distance -> lens phase ->
    focal distance and showing the quadratic phases cancel exactly; state what
    survives when the object is *not* in the front focal plane (same intensity, extra
    quadratic phase on the field).
  - `OBJ-39-3` — Predict the back-focal-plane pattern of gratings and apertures
    (grating of period d -> conjugate dot pair at x = +/- lambda f / d) and show the
    dots obey module 31's grating equation in the small-angle limit.
  - `OBJ-39-4` — Explain Abbe's two-stage picture of imaging (object -> spectrum in
    the pupil -> image) and estimate the finest resolvable grating period
    d_min ~ lambda / NA from which diffraction orders the pupil admits.
  - `OBJ-39-5` — Demonstrate shift invariance: translating the object leaves the
    Fourier-plane *intensity* fixed and adds only a linear phase to the field, and
    explain why this is the convolution theorem's shift rule performed by glass.
- **Mathematical background:** has — 2-D transform and theorems (38), Fresnel/angular
  spectrum propagation as a callable black box (32), thin-lens phase from ray optics
  (34); introduced here — the quadratic-phase cancellation argument; reading a
  physical plane as a frequency axis (the $\nu = x/(\lambda f)$ dictionary).
- **Physical intuition goals:** (1) the back focal plane is *the far field brought
  close* — every direction becomes a place; (2) finer object detail lands farther
  off-axis — "the pupil's edge is where sharpness lives"; (3) moving the object
  sideways moves the image but not the transform — the spectrum has no position;
  (4) a longer focal length spreads the same spectrum over more millimetres —
  $f$ is the zoom knob of the transform plane.
- **Section skeleton seeds:**
  - *puzzle:* shine a laser through a fine mesh and put a lens behind it: on a card
    at one special distance, the mesh vanishes and a crisp lattice of *dots* appears
    — geometry the mesh itself nowhere contains. Move the mesh sideways; the dots do
    not move. (Boxed: what is the lens computing, and why does the answer not care
    where the object is?)
  - *predict:* (1) double the grating period — do the dots move in or out? (2) slide
    the mesh sideways — do the dots slide too? (targets NEW `fourier-plane-is-image`)
    (3) replace the mesh by a smaller mesh of the same pitch — do the dots move?
    (4) is the dot pattern an *image* of anything? What happens to it as the object
    is slowly defocused from the front focal plane?
  - *explore:* **virtual transform bench** — object chooser (grating, mesh, disk,
    portrait, `spoke_target`); sliders $f$ (50–500 mm), $\lambda$ (450–650 nm),
    grating period, object lateral shift; three synchronized panes: object, exact
    back-focal-plane intensity via `fourier_plane_field`, and the pure
    `fft2_centered` prediction overlaid — with a live residual meter showing the two
    agree; a "move the object" button that leaves the middle pane conspicuously
    still while a phase-view toggle shows the linear phase ramping.
  - *derive:* thin lens as phase screen $t = e^{-\ii k(x^2+y^2)/(2f)}$ (34's
    lensmaker made wavy; sign per the course $e^{+\ii kz}$ forward phase) → Fresnel
    quadratic phase over distance $f$ → the three quadratic phases cancel
    identically → $U_f(u,v) = \dfrac{1}{\ii\lambda f}\,
    \iint U_o(x,y)\, e^{-\ii 2\pi (xu + yv)/(\lambda f)}\,dx\,dy$ — the forward
    transform with $\nu_x = u/(\lambda f)$, the constant $1/(\ii\lambda f)$ kept
    honestly → grating check: period $d$ → dots at $u = \pm\lambda f/d$, matching
    $\sin\theta = \lambda/d$ small-angle (31's equation recovered) → object at
    distance $z \ne f$: the transform survives with an extra quadratic phase
    $e^{\ii k(1 - z/f)(u^2+v^2)/(2f)}$ — invisible to intensity, fatal to holography
    (forward pointer to 50) → shift theorem performed by glass → Abbe: imaging is
    transform-then-transform; the pupil truncates the spectrum between the stages,
    so a grating images only if its first orders fit through: $d_{\min} \approx
    \lambda/\mathrm{NA}$ (coherent axial illumination; the factor-2 refinement is
    41's).
  - *verify:* `fourier_plane_field` vs `fft2_centered` to the documented guard-band
    accuracy (§4 convergence test in view); dot position vs $\lambda f/d$ across a
    sweep — fitted exponents $+1, +1, -1$ in $(\lambda, f, d)$ via
    `validation.scaling_exponent` (`numerical-observation` box); shift invariance —
    $|U_f|$ unchanged to machine precision under object translation while the field
    phase ramps linearly; ray cross-check — `rayoptics.cascade(free_space(f),
    thin_lens(f), free_space(f))` maps input *angle* to output *height* with the
    same $\lambda$-free scaling (the ABCD matrix has $B = f$, $A = 0$: angle-to-
    position, the geometric shadow of the transform).
  - *transfer:* `40-psf-otf` — put the *pupil* where this module put its card, and
    the truncated spectrum becomes a transfer function; `42-4f-processor` — a second
    lens undoes the transform, so a mask between them edits the spectrum;
    `38-spatial-frequencies` backward — the playground's brush becomes a physical
    object; `31-gratings` backward — spectrometers park a detector in exactly this
    plane; `50-holography` — the field here is worth recording, not just detecting;
    optical computing — correlation at the speed of light (42's advanced box).
  - *quiz:* dot-position numeric; shift-invariance MC (registry distractor);
    which-plane-is-the-transform MC; Abbe $d_{\min}$ numeric; scaling-law reasoning.
  - *explain:* why the transform plane has no memory of where the object sits, in
    terms of what a lens does to plane waves; why finer detail sits farther out; to
    a microscopist — what Abbe meant by "the image is formed twice"; why the dots
    at the mesh experiment are sharp even though the mesh is illuminated everywhere.
  - *advanced:* the exact quadratic-phase bookkeeping for object planes $z \ne f$
    (the formula derived, not just stated); the transform's space-bandwidth budget —
    how many resolvable spots a lens of given NA and field can deliver (the number
    that prices real optical processors); oblique illumination doubling Abbe's
    resolution (trailer for 41's incoherent factor 2).
- **Core derivations:** (1) lens phase from optical path through a thin lens:
  $t(x,y) = e^{-\ii k (x^2+y^2)/(2f)}$ — one line from 34's sag formula, sign fixed
  by the course convention (a converging lens *advances* the marginal ray's phase
  toward the axis so plane waves curve inward). (2) The f–lens–f chain with Fresnel
  kernels $e^{+\ii k (x^2+y^2)/(2z)}$: the object-side, lens, and image-side
  quadratic phases cancel term by term, leaving the pure kernel
  $e^{-\ii 2\pi(xu+yv)/(\lambda f)}$ and the prefactor $1/(\ii\lambda f)$ — done
  once in full, then delegated to `fourier_plane_field` for all numerics. (3) The
  grating dot pair and the 31 consistency check. (4) The $z \ne f$ quadratic
  residual $e^{\ii k(1-z/f)(u^2+v^2)/(2f)}$. (5) Abbe's $d_{\min} = \lambda/\mathrm{NA}$
  by asking which conjugate dot pairs the pupil admits.
- **Model specification draft:** System — a monochromatic scalar field passing one
  thin ideal lens between two free-space stretches; observables are the complex
  field and intensity in the back focal plane. Dynamics — angular-spectrum
  propagation plus one multiplicative phase screen. Boundary — finite periodic grids
  (the §4 guard-band caveat); the lens is infinite in aperture unless a pupil array
  is supplied. Ensemble — deterministic. Ignored — aberrations (37's subject; the
  lens phase is exactly quadratic), reflection losses, polarization, finite lens
  aperture in core (introduced as *the* topic of 40). Valid when — paraxial
  (quadratic phases honest, $\mathrm{NA} \lesssim 0.3$); object features ≥ a few
  grid samples; grid guard band ≥ the object's diffraction spread. Failure modes —
  reading the Fourier plane as an image; trusting the scaling law far off axis;
  wrap-around bleeding into the transform corners; forgetting the $1/(\ii\lambda f)$
  when energies are compared.
- **Epistemic classification:** the Fourier-transforming property — `theorem`
  (derived by cancellation, within the paraxial model); paraxial/thin-lens phase —
  `approximation` (boxed with its NA validity edge); the measured $(λ, f, d)$
  scaling exponents — `numerical-observation`; Abbe's two-stage picture —
  `theorem` at this level (its coherent-illumination scope stated, refined in 41);
  "the lens computes at light speed" — prose, kept honest (the computation is the
  propagation; the lens only cancels phases).
- **Misconceptions:** NEW **`fourier-plane-is-image`** — "The pattern in the back
  focal plane is a small image of the object." Falsifying experiment: translate the
  object laterally — the Fourier-plane *intensity* does not move (measured to
  machine precision via `fourier_plane_field`), while any image would translate;
  a grating object produces dots that look nothing like the grating, at positions
  set by its *period*, not its outline. Distractor: quiz option "sliding the mesh
  sideways slides the dot pattern by the magnification times the shift".
- **Glossary terms:** `fourier-plane` (מישור פורייה — coordinate with 38's
  `transform-plane` key: 38 deposits the mathematical term, 39 the optical),
  `back-focal-plane` (מישור המוקד האחורי), `abbe-theory` (תורת ההדמיה של אבה —
  translator to confirm), `quadratic-phase` (מופע ריבועי), `space-bandwidth-product`
  (מכפלת מרחב–רוחב־פס — translator to decide; advanced), `angular-spectrum` cited
  (deposited by `32-fresnel-diffraction`, part-09).
- **Interactive controls and simulations:** the virtual transform bench (see
  *explore*); Abbe order-picker — a pupil-radius slider that admits 0, 1, 2, …
  conjugate order pairs of a grating object with the *image* (computed by a second
  transform) shown live: the grating snaps into existence exactly when the first
  pair enters (a designed discovery for 42's masks); ray/wave split view — the same
  f–lens–f chain traced by `rayoptics.cascade` rays above and by fields below.
- **Virtual lab outline** (`notebooks/en/labs/39-fourier-lens.ipynb`): (1) bench
  play — gratings, meshes, the portrait; log predictions; (2) *measurement:* dot
  positions vs $d$, $f$, $\lambda$ across sweeps with pixel noise
  (`measurement.add_noise`), log-log fits of all three exponents ± uncertainty;
  (3) shift-invariance experiment — object translation sweep, plot
  $\max |\Delta|U_f||$ (machine zero) and the fitted linear phase slope vs shift;
  (4) the $z \ne f$ study — intensity unchanged, phase curvature measured against
  the residual formula; (5) Abbe order-picker quantified: image contrast vs number
  of admitted order pairs; $d_{\min}$ vs pupil radius fitted against
  $\lambda/\mathrm{NA}$.
- **Real-experiment counterpart:** laser pointer + a fine mesh (sieve, woven
  screen, or fabric) + any magnifier or camera lens: photograph the dot lattice on
  a card at the focal distance, with a ruler in frame; import, measure dot spacing,
  infer the mesh pitch ± uncertainty and check against a direct photo of the mesh.
  Cost: a few dollars beyond the part's laser pointer.
- **Media assets** (`render_fourier_optics.py`): (c) the f–lens–f morph — a wave
  field crossing the lens, quadratic phase fronts visibly straightening into the
  transform plane, the grating's dots condensing; (d) shift-invariance shot —
  object sliding, image plane (from a second lens) sliding with it, Fourier plane
  rock still. Language-neutral.
- **Quiz bank outline:** `Q-39-1` numeric — dot position for given $d$, $f$,
  $\lambda$ (OBJ-39-1, OBJ-39-3); `Q-39-2` MC — object translated: what moves?
  (OBJ-39-5; distractor `fourier-plane-is-image`); `Q-39-3` MC — double the period:
  dots in or out (OBJ-39-1); `Q-39-4` numeric — Abbe $d_{\min}$ for a given NA and
  $\lambda$ (OBJ-39-4); `Q-39-5` MC — object moved out of the front focal plane:
  what changes in the back focal plane (OBJ-39-2); `Q-39-6` free — derive the dot
  positions from the grating equation and from the transform picture, and show they
  agree (OBJ-39-2, OBJ-39-3).
- **Problem set outline:** analytical — carry the three quadratic phases through
  the f–lens–f chain and watch them cancel (guided); the $z \ne f$ residual phase;
  two thin lenses back to back as one transform at effective $f$. Computational —
  space-bandwidth census: resolvable spots vs NA and field for three real lenses;
  reproduce the mesh photo's dot lattice from a photographed mesh. Challenge —
  cylindrical lens: a 1-D transform along one axis only — predict and verify the
  anamorphic Fourier plane of a crossed grid.
- **Runtime budget:** bench interactions on 256² grids with two
  `angular_spectrum_propagate` calls per update — a few ms each in Pyodide; lab
  sweeps ≤ 40 configurations at 512²; animations pre-rendered. In-browser
  comfortable.
- **Validation gates:** standard four with `--module 39-fourier-lens`; plus the §4
  `fourier_plane_field`-vs-`fft2_centered` convergence test and the scaling-exponent
  tests landing with this module.
- **Open questions for the author:** whether the $1/(\ii\lambda f)$ prefactor is
  carried in every displayed formula or once in a box (recommendation: box once,
  cite thereafter — the lint's sign checks apply either way); whether the Abbe
  order-picker lives here or is deferred wholly to 42 (recommendation: here as a
  discovery, rebuilt in 42 as an instrument); mesh vs grating as the puzzle object
  (recommendation: mesh — the 2-D dot lattice is more arresting than a dot row).

### 5.3 `40-psf-otf` — PSF and OTF: resolution as frequency response

- **Identity and scope:** master-plan notebooks 11.3 + 11.4, **merged** (§8): the PSF
  and the OTF are one Fourier pair — a PSF notebook without its transform repeats
  `05-impulse-response`'s mistake of splitting $G$ from $\hat{H}$. Covers: PSF from
  the pupil, imaging as convolution, OTF/MTF, cutoff and two-point resolution,
  defocus and contrast reversal, and the measured slanted-edge MTF. Deferred: the
  coherent/incoherent split → `41-imaging-coherence` (this module is incoherent
  throughout, stated in the model spec); aberrations beyond defocus → `37-aberrations`
  backward and capstone §35.1; deconvolution → `53-computational-imaging`.
- **Prerequisites:** `39-fourier-lens` (pupil-plane spectrum truncation);
  `05-impulse-response` (the LTI bridge, quoted verbatim); `30-apertures`
  (`diffraction.airy_radius`, `diffraction.rayleigh_criterion` — dictated names);
  `04-fourier-transform` (convolution theorem); `36-instruments` (NA, and the
  registry's `magnification-reveals-detail`, reinforced here with a distractor).
- **Learning objectives:**
  - `OBJ-40-1` — Define the PSF as the image of a point source, compute it as the
    scaled transform of the pupil, and verify that a clear circular pupil gives the
    Airy pattern with first dark ring at 1.22 lambda f / D.
  - `OBJ-40-2` — Model imaging as convolution, image = object (*) PSF, state the
    isoplanatism assumption that licenses it, and connect it word for word to module
    05's G and convolution_response.
  - `OBJ-40-3` — Define OTF = normalized FT of the intensity PSF and MTF = |OTF|,
    state OTF(0) = 1, and compute the clear-pupil MTF with its cutoff
    nu_c = D / (lambda f) = 2 NA / lambda.
  - `OBJ-40-4` — Predict two-point and bar-target resolvability from the MTF, use
    rayleigh_criterion as its classical shorthand, and explain why resolution is a
    contrast threshold, not a cliff.
  - `OBJ-40-5` — Add defocus as the Zernike (2,0) pupil phase, predict the MTF's
    collapse and nulls, and demonstrate spurious resolution (contrast reversal past
    a null).
  - `OBJ-40-6` — Measure an MTF from noisy synthetic data by the slanted-edge chain
    ESF -> LSF -> MTF, with an uncertainty estimate.
- **Mathematical background:** has — 2-D pairs (38), lens transform (39), LTI
  formalism (05); introduced here — autocorrelation of a pupil as a transfer
  function (stated for the incoherent case, derived properly in 41); the
  ESF→LSF→MTF differentiation chain; Zernike defocus as the lowest interesting
  pupil aberration.
- **Physical intuition goals:** (1) every camera is a low-pass filter; the only
  question is its cutoff and its roll-off; (2) doubling the aperture halves the PSF
  and doubles the cutoff — resolution is bought in the pupil, not at the sensor;
  (3) blur never adds signal beyond the cutoff: zero times anything is zero;
  (4) a defocused image can *reverse* contrast — bar targets with black and white
  swapped are the fingerprint of an MTF null, not of a broken camera.
- **Section skeleton seeds:**
  - *puzzle:* two photographs of the same star field, same exposure: the cheap wide
    lens shows every star as a soft blob; the telescope shows rings around each.
    Neither shows a point. (Boxed: what does a *perfect* imaging system do to a
    point of light — and if even perfection blurs, what number honestly describes
    "sharpness"?)
  - *predict:* (1) a perfect lens images a star as — a point, a blob, or rings?
    (targets NEW `smaller-aperture-sharper-image` via its companion: what sets the
    blob size?) (2) stop the aperture down to half — does the image get sharper or
    softer? (3) can any amount of magnification reveal detail the MTF has cut off?
    (reinforces `magnification-reveals-detail`, part-10 registry) (4) defocus a bar
    target slowly — do the bars fade out once, or can they vanish and *come back*?
  - *explore:* **PSF/MTF workbench** — pupil builder (`pupil_disk` radius slider,
    annulus toggle, `zernike_phase(2,0)` defocus slider); three synchronized panes
    per master plan §22: pupil (with phase as colour), PSF (log/linear zoom,
    `airy_radius` ring overlaid), MTF radial profile (cutoff marked, Rayleigh-
    contrast line drawn); an imaging pane applying the current PSF to a chooseable
    object (`bar_target`, `spoke_target`, portrait) via `image_incoherent` — the
    spoke target makes the MTF *visible* as a grey ring whose radius shrinks as
    defocus grows.
  - *derive:* point source → pupil-plane field = constant → image-plane amplitude =
    scaled pupil transform (39's machinery pointed backward) → intensity PSF
    $|h|^2$; clear disk → Airy, first zero at $1.22\lambda f/D$
    (`diffraction.airy_radius` cited, cross-owner agreement tested) →
    isoplanatism + linearity in intensity → image = object $*$ PSF — **the module-05
    sentence kept**: "$G$ is the point spread function of time, $\hat{H}$ the OTF;
    imaging is this module with $t \to (x,y)$", now with the arrow reversed →
    OTF = $\widehat{\mathrm{PSF}}$, normalised; MTF = $|{\rm OTF}|$ → clear-pupil
    MTF = autocorrelation of the disk (the chat function), cutoff $\nu_c =
    D/(\lambda f)$ — stated here as a computed fact, *derived* as pupil
    autocorrelation in 41 → two-point resolution: Rayleigh's 26.4% dip as a
    historical contrast threshold; the MTF view replaces the cliff with a curve →
    defocus: $W_{2,0}$ pupil phase, MTF collapse, nulls, and contrast reversal
    past each null (spurious resolution shown on the spoke target) → the
    slanted-edge method: ESF from an `edge_target` image, differentiate to LSF,
    transform to MTF — the practitioner's chain, done with noise.
  - *verify:* PSF-vs-`fraunhofer_pattern` and `airy_radius` cross-owner tests (§4
    *limits* in view); `otf_from_psf`[0,0] $= 1$ exactly; slit pupil → triangle
    MTF matching $1 - |\nu|/(2\nu_0)$; measured cutoff vs $D/(\lambda f)$ across a
    pupil sweep (fitted exponents +1, −1 — `numerical-observation` box);
    slanted-edge MTF vs the direct `mtf(otf_from_psf(...))` on the same system
    within the noise-set uncertainty.
  - *transfer:* `41-imaging-coherence` — the same pupil, coherent rules: cutoff
    halves and amplitudes, not intensities, convolve; `53-computational-imaging` —
    dividing by the MTF where it is small is 05's deconvolution wreckage in space
    (nulls make it impossible, not just hard); capstone §35.1 — scene → pupil →
    PSF → sensor is this module industrialised; `37-aberrations` backward — every
    Seidel term is a pupil phase like defocus, and the Zernike machinery deferred
    from 37's trailer now exists; astronomy — star tests, why telescope reviews
    print MTF curves; photography — why lens tests shoot slanted edges.
  - *quiz:* Airy-radius numeric; convolution-model MC; cutoff numeric; aperture
    halved MC (registry distractor); contrast-reversal MC; magnification
    distractor item.
  - *explain:* why "how many megapixels" is the wrong first question about a
    camera; the MTF to a photographer in three sentences, no formulas; why a
    perfect lens still blurs (where the information went); what an MTF null means
    for recovering the scene — and why no algorithm crosses zero.
  - *advanced:* the incoherent OTF as pupil autocorrelation — stated and computed
    here, derived in 41 (the forward pointer is explicit); apodisation — soft
    pupils trade cutoff for sidelobe suppression (Gaussian pupil → ringless PSF);
    annular pupils — sharper core, taller sidelobes (why telescopes with big
    secondaries still resolve); sampling the PSF: matching $\mathrm{px} \le
    \lambda f / (2D)$ — the sensor-side Nyquist condition closing 38's loop.
- **Core derivations:** (1) amplitude PSF $h = $ scaled FT of the pupil (one line
  given 39); intensity PSF $= |h|^2$, unit-normalised. (2) Clear disk → Airy;
  $r_1 = 1.22\,\lambda f/D$ (cited, not re-derived — `30-apertures` owns the
  Bessel integral). (3) Linearity + isoplanatism ⇒ image $= I_{\rm obj} * \mathrm{PSF}$
  — assumptions boxed. (4) OTF $= \widehat{\mathrm{PSF}}/\widehat{\mathrm{PSF}}(0)$;
  slit-pupil triangle MTF computed in full as the 1-D worked example; disk-pupil
  chat function quoted with its cutoff $\nu_c = D/(\lambda f)$. (5) Defocus
  $W(\rho) = W_{20}\,(2\rho^2 - 1)$ via `zernike_phase(2, 0)`; MTF nulls and the
  sign flip of the OTF between them (contrast reversal = negative OTF, made
  visible). (6) ESF → LSF (derivative) → MTF (transform), with the noise-
  amplification of differentiation handled by the fit, not hidden.
- **Model specification draft:** System — one incoherently illuminated, isoplanatic,
  monochromatic imaging system reduced to its exit pupil (amplitude and phase over
  a disk); observables are PSF, OTF/MTF, and images of test objects. Dynamics —
  none; pupil → PSF by transform, imaging by convolution. Boundary — finite grids
  (§4 caveat); pupils hard-edged unless apodised. Ensemble — deterministic; sensor
  noise via `wavelab.measurement` in the labs. Ignored — coherence effects (41),
  field-dependent aberrations (isoplanatism boxed), chromatic effects unless λ is
  looped, sensor pixel integration (one honest sentence, as in 38). Valid when —
  paraxial NA; object features within the isoplanatic patch; intensities add
  (source incoherent — the standing assumption this module inherits and 41
  interrogates). Failure modes — comparing PSFs of different normalisation;
  reading spurious resolution as detail; dividing by MTF near nulls; pupil phase
  wrapped without unwrapping at large defocus.
- **Epistemic classification:** PSF-from-pupil and OTF pair — `theorem` (given 39
  and the convolution theorem); isoplanatism + incoherent linearity —
  `model-assumption` (the boxed one); Airy radius and Rayleigh criterion —
  `theorem` / `definition` respectively (cited from 30); measured cutoff scaling
  and the slanted-edge agreement — `numerical-observation`; "resolution is a
  contrast threshold" — `definition`-level framing, said explicitly.
- **Misconceptions:** NEW **`smaller-aperture-sharper-image`** — "Stopping a lens
  down always makes the image sharper, because a smaller hole selects straighter
  rays." Falsifying experiment: pupil-radius sweep with `psf_from_pupil` — PSF
  width fitted $\propto 1/D$, MTF cutoff $\propto D$; halving the aperture
  demonstrably *halves* the resolving power of the aberration-free system (an
  honest aside notes that real lenses at full aperture are aberration-limited —
  part-10's story — which is why the folk rule half-works). Distractor: quiz
  option "the smaller stop passes only near-axial rays, so the image is always
  sharper". Also reinforces `magnification-reveals-detail` (owned by part-10,
  module 36) with a quiz distractor here — empty magnification is an MTF fact.
- **Glossary terms:** `point-spread-function` (פונקציית פיזור נקודה),
  `optical-transfer-function` (פונקציית תמסורת אופטית — translator to align with
  05's `frequency-response` תגובת תדר), `modulation-transfer-function` (פונקציית
  תמסורת אפנון; `he_reject` candidate: MTF כתעתיק), `cutoff-frequency` cited
  (part-02 deposit — the optical usage added to the same key), `defocus`
  (חוסר מיקוד; `he_reject` candidate: דפוקוס), `zernike-polynomial` (פולינום
  זרניקה), `spurious-resolution` (הפרדה מדומה — translator to confirm),
  `slanted-edge-method` (שיטת הקצה המוטה — translator to decide).
- **Interactive controls and simulations:** the PSF/MTF workbench (see *explore*);
  two-point resolver — separation slider over the live PSF with the intensity
  profile and its dip percentage read out, Rayleigh's 26.4% marked; defocus
  theatre — spoke target under increasing $W_{20}$, the grey ring walking inward
  and bars flipping past each null; aperture-sweep strip: PSF thumbnails at
  $D, D/2, D/4$ side by side (the misconception's falsifier as a picture).
- **Virtual lab outline** (`notebooks/en/labs/40-psf-otf.ipynb`): (1) workbench
  play; Airy ring against `airy_radius`; (2) *measurement:* two-point resolution —
  noisy double-star frames across separations (`measurement.add_noise`), dip-based
  resolvability threshold vs `rayleigh_criterion`, reported ± uncertainty;
  (3) MTF from bar targets: contrast vs frequency across a `bar_target` ladder,
  overlaid on `mtf(otf_from_psf(...))`; (4) defocus study: MTF nulls located,
  contrast reversal photographed, null positions vs $W_{20}$ fitted; (5) *the
  slanted-edge measurement:* `edge_target` image with noise → ESF → LSF → MTF ±
  spread across seeds (`validation.seed_study`), compared with the direct
  computation — the practitioner's method validated end to end.
- **Real-experiment counterpart:** photograph a printed slanted-edge target (one
  sheet, any laser printer) with a phone at fixed distance; import the raw image,
  run the module's own ESF → LSF → MTF chain on real data; report the phone
  camera's MTF50 ± uncertainty. A distant streetlight at night is a free point
  source for a qualitative PSF (defocus rings included).
- **Media assets** (`render_fourier_optics.py`): (e) aperture sweep — pupil
  shrinking, PSF blooming, MTF curve retracting, spoke-target image degrading, all
  four panes locked in step; (f) defocus theatre — $W_{20}$ ramp with bars flipping
  black-for-white past each MTF null. Language-neutral.
- **Quiz bank outline:** `Q-40-1` numeric — Airy radius for given $D$, $f$,
  $\lambda$ (OBJ-40-1); `Q-40-2` MC — what a perfect lens does to a point
  (OBJ-40-1); `Q-40-3` MC — aperture halved: PSF and cutoff (OBJ-40-3; distractor
  `smaller-aperture-sharper-image`); `Q-40-4` MC — can magnification beat the MTF
  (OBJ-40-4; distractor from `magnification-reveals-detail`); `Q-40-5` numeric —
  cutoff frequency and finest resolvable bar period (OBJ-40-3, OBJ-40-4);
  `Q-40-6` MC — bars reappear inverted under defocus: why (OBJ-40-5); `Q-40-7`
  free — describe the slanted-edge chain and why the edge is slanted
  (OBJ-40-6).
- **Problem set outline:** analytical — slit-pupil triangle MTF from the
  autocorrelation; annular-pupil MTF and its enhanced mid-band dip; prove
  OTF(0) = 1 from PSF normalisation. Computational — apodisation study: Gaussian
  vs hard pupil, ringing vs cutoff; sensor-matching: choose pixel pitch for a
  given $f/\#$ and λ (38's Nyquist closing). Challenge — reconstruct a defocused
  image by MTF division, watch the nulls destroy it, regularise crudely, and
  write three sentences on why `53-computational-imaging` exists.
- **Runtime budget:** pupils/PSFs at 256²–512², a handful of FFTs per
  interaction — ms-scale; the seed-study slanted-edge cell ≤ 64 realisations at
  512² — a few seconds, the module's heaviest cell. In-browser comfortable.
- **Validation gates:** standard four with `--module 40-psf-otf`; plus the §4
  cross-owner Airy tests, triangle-MTF limit, cutoff-scaling, and `zernike_phase`
  orthogonality tests landing with this module.
- **Open questions for the author:** whether contrast reversal is core or
  advanced (recommendation: core — it is the most memorable evidence that
  imaging is frequency response); whether the Rayleigh criterion gets a
  `definition` box or lives inside the MTF discussion (recommendation: box — the
  term is exam-canonical); how much of 37's Zernike vocabulary to import beyond
  (2,0) (recommendation: none — defocus only, the rest stays with 37 and §35.1).

### 5.4 `41-imaging-coherence` — Coherent and incoherent imaging — and speckle

- **Identity and scope:** master-plan notebook 11.5. The field-vs-intensity split:
  coherent imaging as amplitude convolution with the pupil as transfer function,
  incoherent imaging as intensity convolution with the pupil *autocorrelation* as
  OTF, the factor-2 cutoff comparison, coherent artifacts (edge ringing, two-point
  phase dependence), and speckle as the part's statistical crown. Collects
  part-08's deferred promise: van Cittert–Zernike *as an imaging idea* lands here
  (kept at the visibility level of 27; the propagation calculus stays out, §8).
  Deferred: photon statistics → `52-quantum-optics`; holographic recording of
  coherent fields → `50-holography`; partial-coherence calculus (TCC) → out of
  course scope (§8).
- **Prerequisites:** `40-psf-otf` (PSF/OTF machinery, `amplitude_psf` vs
  `psf_from_pupil`); `27-coherence` (visibility, `degree_of_coherence`,
  `partial_coherence_source`, the source gallery); `00-phasors`
  (`random_phasor_sum` — speckle is its 2-D field version); `03-fourier-series`
  (`gibbs_overshoot` — coherent edge ringing is Gibbs in space);
  `23-interference` (adding fields vs adding intensities — the part-08 failure
  mode, now the *subject*).
- **Learning objectives:**
  - `OBJ-41-1` — Decide from the illumination whether a system is linear in field
    or linear in intensity, and write the correct imaging pipeline for each
    (convolve amplitudes then square, vs square then convolve).
  - `OBJ-41-2` — State that the coherent transfer function is the pupil itself
    with cutoff NA/lambda, while the incoherent OTF is the pupil autocorrelation
    with cutoff 2 NA/lambda, and explain why the factor 2 does not mean
    "incoherent is twice as sharp".
  - `OBJ-41-3` — Predict coherent artifacts: edge ringing and overshoot at sharp
    boundaries, and the dependence of two-point resolvability on the points'
    relative phase (in phase: worse than incoherent; antiphase: better).
  - `OBJ-41-4` — Derive the first-order statistics of fully developed speckle
    (exponential intensity distribution, unit contrast) from the random phasor
    walk, and compute the characteristic grain size ~ lambda z / D from the
    illuminated aperture.
  - `OBJ-41-5` — Use fringe-visibility reasoning (module 27's gamma) to place a
    real source between the coherent and incoherent limits, and predict which
    limit a laser, an LED, and a sunlit scene each approach in an imaging system.
- **Mathematical background:** has — amplitude vs intensity PSFs (40), coherence
  functions (27), the random walk (00); introduced here — pupil autocorrelation
  as a derived object (the 40 statement earns its proof); ensemble reasoning over
  *images* (speckle realisations vs the smooth incoherent limit).
- **Physical intuition goals:** (1) laser light makes everything look
  crystalline and *grainy* at once — the grain is in the light, not the object;
  (2) coherent edges ring — the 9% overshoot follows light around; (3) two
  stars vs two laser spots: the same separation can be resolvable in one and
  not the other; (4) sunlight through a camera is incoherent *because* the sun
  is an extended thermal source — 27's source gallery decides the pipeline.
- **Section skeleton seeds:**
  - *puzzle:* point a laser at a white wall and look: the spot seethes with a
    fine granular sparkle that moves when *you* move, and no camera focus makes
    it go away. Photograph the same wall in sunlight: perfectly smooth. Same
    wall, same eye. (Boxed: where does the grain live — in the wall, in the eye,
    or in the light — and why does sunlight not have it?)
  - *predict:* (1) the speckle grains: object texture, sensor noise, or
    interference? (2) is a laser-lit microscope image sharper than the same
    microscope with lamp light? (targets NEW `coherent-always-sharper`)
    (3) a razor edge imaged in laser light: clean step or ringing? (4) squint
    (shrink your pupil) at laser speckle — do the grains get bigger or smaller?
  - *explore:* **pipeline switchboard** — one object (edge, two points with a
    relative-phase dial, bar ladder, portrait-as-transparency), one pupil, two
    pipelines side by side: `image_coherent` (via `amplitude_psf`) vs
    `image_incoherent` (via `psf_from_pupil`), with their transfer functions
    (pupil vs its autocorrelation) plotted above each; the two-point phase dial
    is the module's designed discovery — sweep it and watch the coherent pair
    merge and split at fixed separation. **Speckle box:** `speckle_field` with
    aperture-size slider, live intensity histogram against the exponential,
    contrast readout, grain-size ruler.
  - *derive:* coherent: field at image = $E_{\rm obj} * h$ (isoplanatism as in
    40), intensity last ⇒ transfer function = pupil, cutoff $\mathrm{NA}/\lambda$
    → incoherent: uncorrelated object phases ⇒ cross terms average out
    (the same cross-term killing as 00's random walk and 27's Wiener–Khinchin
    proof — said so), intensity convolution survives ⇒ OTF =
    autocorrelation of the pupil (40's stated fact now derived), cutoff
    $2\mathrm{NA}/\lambda$ → why 2× is not "twice as sharp": amplitude vs
    intensity contrast at the old cutoff compared honestly → edge response:
    coherent step overshoot ≈ Gibbs (`gibbs_overshoot` cited; the transfer
    function is a hard cutoff, so the space-domain edge rings) → two points at
    separation $s$ with relative phase $\varphi$: intensity
    $|h_1 + e^{\ii\varphi}h_2|^2$ — in phase fills the dip, antiphase digs it
    (Rayleigh's criterion is *illumination-dependent*, the honest headline) →
    speckle: rough surface = random phasor field; at any image point the field
    is 00's $\sum e^{-\ii\varphi_k}$; Gaussian field ⇒ exponential intensity,
    contrast 1 (`speckle_contrast` → 1); grain size = the diffraction scale
    $\sim \lambda z/D$ of the illuminated patch (the speckle *is* a PSF-scale
    interference pattern) → partial coherence: 27's $|\gamma|$ interpolates the
    two-point fringe term; vCZ idea (source size → coherence area) quoted at
    27's level to place lamps and LEDs.
  - *verify:* incoherent OTF from `otf_from_psf` equals the pupil
    autocorrelation (the §4 limits test in view); measured coherent cutoff =
    half the incoherent cutoff on the same pupil (§4); coherent edge overshoot
    vs `gibbs_overshoot`'s 8.95% (`numerical-observation` box — agreement is
    approximate and its conditions stated); speckle histogram KS-test against
    the exponential across seeds (§4 seeds test); grain-size vs aperture fitted
    exponent −1.
  - *transfer:* `50-holography` — coherent imaging is a feature there: the
    field is the point; `53-computational-imaging` — speckle as noise floor
    and as *signal* (speckle imaging teaser); `27-coherence` backward — the
    source gallery now dictates an imaging pipeline; `52-quantum-optics` —
    intensity correlations of speckle, $g^{(2)}$, HBT; microscopy — why
    condenser design (Köhler, oblique) is coherence engineering, one honest
    paragraph; astronomy — speckle interferometry: the atmosphere's speckle
    beaten by statistics (research box).
  - *quiz:* pipeline choice MC; cutoff-factor MC (with the "twice as sharp"
    trap); two-point phase MC; speckle-statistics numeric; grain-size numeric
    (registry distractor on the squint question).
  - *explain:* why laser speckle follows your head; to a microscopist — when
    lamp light beats laser light and when it doesn't; why "what is the
    resolution of this microscope" needs the illumination specified; where the
    9% overshoot in a coherent edge image comes from, citing a module from
    Part 0.
  - *advanced:* speckle suppression by diversity — average $M$ independent
    speckle patterns (rotating diffuser), contrast $\propto 1/\sqrt{M}$
    (00's $\sqrt{N}$ again, third costume — measured); the mutual-coherence /
    TCC formalism named as the honest general machinery and *not* developed
    (`open-question`-flavoured pointer to Goodman's statistical optics);
    dark-field and oblique illumination as pupil engineering (bridge to 42's
    masks).
- **Core derivations:** (1) the two pipelines side by side, with the cross-term
  average $\langle e^{\ii(\varphi_k - \varphi_l)}\rangle = \delta_{kl}$ doing
  the incoherent work — one displayed equation each. (2) OTF =
  $\mathrm{autocorr}(P)/\mathrm{autocorr}(P)(0)$ derived from
  $\mathrm{PSF} = |h|^2$ and the convolution theorem — three lines given 40.
  (3) Two-point intensity $|h(x - s/2) + e^{\ii\varphi} h(x + s/2)|^2$ expanded;
  the $\varphi$-dependence displayed. (4) Speckle first-order statistics:
  complex Gaussian field from the CLT over surface phasors ⇒
  $P(I) = e^{-I/\bar I}/\bar I$; contrast $= 1$; grain size from the
  autocorrelation of the imaged field ≈ the diffraction limit of the
  illuminated aperture. (5) The $1/\sqrt{M}$ diversity law (advanced).
- **Model specification draft:** System — one isoplanatic imaging system under
  either fully coherent or fully incoherent scalar illumination (the two ideal
  limits; partial coherence enters only via 27's $|\gamma|$ in two-beam
  reasoning); objects are complex transmittances, possibly with rough
  (random-phase) surfaces. Dynamics — none; the two convolution pipelines.
  Boundary — finite grids (§4); pupils as in 40. Ensemble — central for
  speckle: seeded rough-surface realisations, ensemble claims labelled as
  such. Ignored — partial-coherence propagation (TCC), polarization (speckle
  depolarisation noted in one sentence), photon noise. Valid when — paraxial;
  illumination genuinely near one limit (laser vs thermal-extended; 27's
  gallery cited); rough surfaces rough on the λ scale for fully developed
  speckle. Failure modes — mixing pipelines (the part-08 failure mode
  promoted to the model spec); reading one speckle frame as an average;
  applying Rayleigh's incoherent criterion to coherent pairs; contrast
  claims from clipped detectors.
- **Epistemic classification:** the two pipelines and their transfer
  functions — `theorem` (given 40 + the cross-term average); "the
  illumination decides the pipeline" — `model-assumption` (the ideal-limit
  box, with 27's γ as the honest dial); speckle exponential statistics —
  `theorem` (CLT conditions stated) with the measured histogram a
  `numerical-observation`; Gibbs-overshoot correspondence —
  `numerical-observation` (conditions stated); TCC pointer — honest scope
  note (out of course).
- **Misconceptions:** NEW **`coherent-always-sharper`** — "Laser illumination
  gives sharper images because laser light is 'better' light." Falsifying
  experiment: same pupil, same object, both pipelines — the coherent cutoff
  is *half* the incoherent one, the coherent edge rings, and the two-point
  dial shows in-phase pairs blurring together at separations the incoherent
  system resolves; measured, plotted, and printed side by side. Distractor:
  quiz option "coherent light always resolves finer detail because it is more
  ordered". (The squint prediction doubles as the falsifier's kinesthetic
  twin: grains grow as the pupil shrinks — the grain is diffraction, not
  object.)
- **Glossary terms:** `coherent-imaging` (הדמיה קוהרנטית),
  `incoherent-imaging` (הדמיה בלתי־קוהרנטית), `speckle` (ספקל; `he_reject`
  candidate: נצנוץ), `speckle-contrast` (ניגודיות ספקל), `edge-ringing`
  (צלצול שפה — translator to confirm), `coherent-transfer-function`
  (פונקציית תמסורת קוהרנטית), `fully-developed-speckle` (ספקל מפותח במלואו —
  translator to decide).
- **Interactive controls and simulations:** the pipeline switchboard and
  speckle box (see *explore*); two-point phase dial (separation and $\varphi$
  sliders, dip-depth readout for both pipelines); diversity averager —
  $M$ slider stacking independent speckle frames with live contrast → the
  $1/\sqrt{M}$ curve tracing itself (advanced).
- **Virtual lab outline** (`notebooks/en/labs/41-imaging-coherence.ipynb`):
  (1) switchboard play — edge, bars, portrait through both pipelines;
  (2) *measurement:* cutoff comparison — bar-ladder contrast vs frequency
  under each pipeline, both cutoffs extracted ± uncertainty, ratio reported
  (target: 2.0); (3) two-point study: resolvable separation vs relative
  phase, the Rayleigh-is-illumination-dependent plot; (4) *speckle
  statistics:* `speckle_field` ensembles — histogram vs exponential, KS
  statistic across seeds, `speckle_contrast` → 1 ± $1/\sqrt{M}$; grain size
  vs aperture fit; (5) diversity: contrast vs $M$ on log-log, slope −1/2
  (`validation.scaling_exponent`) — 00's random walk measured for the third
  time in the course, and the lab says so.
- **Real-experiment counterpart:** a laser pointer on any matte wall:
  photograph speckle at several camera apertures (phone pro-mode or a paper
  iris), import, measure grain size vs aperture and intensity histogram —
  a genuinely quantitative statistical-optics experiment for the cost of a
  laser pointer. Sunlit-wall control frame for the incoherent comparison.
- **Media assets** (`render_fourier_optics.py`): (g) pipeline split-screen —
  one object, two pipelines, edge ringing and speckle appearing only on the
  coherent side; (h) speckle diversity — frames stacking, grain washing out,
  contrast meter falling as $1/\sqrt{M}$. Language-neutral.
- **Quiz bank outline:** `Q-41-1` MC — which pipeline for a sunlit scene /
  a laser-lit die / an LED close-up (OBJ-41-1, OBJ-41-5); `Q-41-2` MC —
  cutoff factor 2 and the "twice as sharp" trap (OBJ-41-2; distractor
  `coherent-always-sharper`); `Q-41-3` MC — two points in antiphase: better
  or worse than incoherent (OBJ-41-3); `Q-41-4` numeric — speckle contrast
  of fully developed speckle, and after averaging 16 frames (OBJ-41-4);
  `Q-41-5` numeric — grain size from aperture and distance (OBJ-41-4);
  `Q-41-6` free — why the grain follows the observer, in module-00
  vocabulary (OBJ-41-4).
- **Problem set outline:** analytical — derive the incoherent OTF as pupil
  autocorrelation; two-point intensity vs $\varphi$; exponential statistics
  from the complex-Gaussian assumption. Computational — coherent vs
  incoherent bar-ladder study across NA; speckle through the 40 workbench's
  defocus (does defocus change contrast? measure, explain). Challenge —
  polarisation diversity: sum two independent speckle intensities, show
  contrast $1/\sqrt2$, and connect to why matte metal speckles differently
  (one paragraph of honest hand-waving allowed, flagged as such).
- **Runtime budget:** double-pipeline updates = 4–6 FFTs at 256² — ms-scale;
  speckle ensembles $M \le 64$ at 256² — a few seconds, the heaviest cell;
  everything else trivial. In-browser comfortable.
- **Validation gates:** standard four with `--module 41-imaging-coherence`;
  plus the §4 coherent/incoherent cutoff test, speckle histogram and
  contrast seed tests landing with this module.
- **Open questions for the author:** whether vCZ appears by name or only as
  "27's source-size rule" (recommendation: by name, one sentence, since 27
  promised it forward); whether the two-point phase dial or the speckle box
  opens the module (recommendation: speckle opens — the puzzle is stronger —
  and the dial is the derive section's set piece); whether polarisation
  speckle diversity stays in the challenge problem only (recommendation:
  yes).

### 5.5 `42-4f-processor` — The 4-f processor and spatial filtering

- **Identity and scope:** master-plan notebook 11.6, the part's summit lab: object →
  lens → Fourier plane → mask → lens → image, with low-pass, high-pass, directional
  filtering and edge enhancement (the master plan's four operations delivered as
  mask families), Abbe–Porter's grid experiment re-enacted, and Zernike phase
  contrast as the crowning trick. Deferred: matched filtering / VanderLugt
  correlator → advanced box and `50-holography`; digital–optical hybrids →
  `53-computational-imaging`; capstone scale-up → §35.5 (stated in content).
- **Prerequisites:** `39-fourier-lens` (one transform stage; the Abbe order-picker);
  `38-spatial-frequencies` (the spectral brush this module makes physical, and its
  `spectrum-maps-image-locations` registry entry — re-falsified here with glass);
  `40-psf-otf` (masks reshape the transfer function); `41-imaging-coherence` (the
  processor runs coherent — its artifacts are now working conditions);
  `20-polarization`/`21-jones-calculus` not needed (scalar masks only, stated).
- **Learning objectives:**
  - `OBJ-42-1` — Assemble the 4-f chain and show that an empty Fourier plane
    returns the object exactly, inverted (magnification -1), with energy conserved.
  - `OBJ-42-2` — Design and apply low-pass, high-pass, and directional masks,
    predicting each filtered image before computing it, and explain edge
    enhancement as high-pass filtering.
  - `OBJ-42-3` — Reproduce the Abbe-Porter experiment: mask a crossed grid's
    spectrum down to one row of orders and predict which line family survives in
    the image.
  - `OBJ-42-4` — Explain Zernike phase contrast: for a weak phase object, a
    quarter-wave shift of the undiffracted order converts invisible phase
    modulation into visible intensity contrast, to first order in phi.
  - `OBJ-42-5` — Connect mask design to transfer-function shaping: state what a
    given mask does to the system's effective coherent transfer function and
    predict artifacts (ringing from hard mask edges) from Part 0 reflexes.
- **Mathematical background:** has — everything (this module deliberately adds no
  new mathematics; the point is that none is needed); introduced here — only the
  weak-phase expansion $e^{\ii\varphi} \approx 1 + \ii\varphi$ and its reading in
  the Fourier plane (DC carries the 1, sidebands carry the $\ii\varphi$).
- **Physical intuition goals:** (1) a mask in the Fourier plane edits *global*
  properties of the image — kill the centre and every smooth area darkens to its
  edges; (2) directions in the mask are orientations in the image — a slit passes
  one family of stripes; (3) a transparent object is invisible because its
  information hides in *phase*, exactly one quarter-turn out of reach — and a
  quarter-wave plate at one point of the Fourier plane turns it visible;
  (4) hard-edged masks ring — the processor obeys the same Fourier rules it
  exploits.
- **Section skeleton seeds:**
  - *puzzle:* Abbe and Porter, 1906: image a wire mesh through a microscope, slip
    a slit into a plane inside the instrument where only a row of dots lives —
    and the *horizontal* wires vanish from the image while nothing touched the
    image plane. (Boxed: how can blocking dots in one plane delete a whole family
    of wires in another — and what else can surgery in that plane do?)
  - *predict:* (1) empty Fourier plane — is the 4-f output identical to the
    object, or changed in one way? (2) pass only the vertical row of a mesh's
    dots — which wires survive? (3) block only the central dot of a portrait's
    spectrum — dark spot in the middle, uniform dimming, or something stranger?
    (re-falsifies `spectrum-maps-image-locations` physically) (4) a perfectly
    transparent oil smear on a slide: can *any* mask make it visible? (targets
    NEW `transparent-means-invisible`)
  - *explore:* **the processor bench** — object chooser (mesh, portrait,
    `spoke_target`, a pure phase object with a hidden message written in
    refractive index); live three-plane view (object / Fourier plane with the
    mask overlaid / image) via `four_f_process`; mask palette: `lowpass_mask`
    and `highpass_mask` with cutoff sliders, `directional_mask` with angle and
    width, `phase_dot` with radius and phase, freehand brush (38's playground
    brush, now physical); an energy meter summing each plane (conservation
    visible, absorption by masks honest).
  - *derive:* two transform stages in cascade: $\mathcal{F}\{\mathcal{F}\{f\}\}
    (x) \propto f(-x)$ — the inverted image, magnification −1, one line given 39
    → a mask $M(u,v)$ multiplies the spectrum ⇒ the output is
    $f * \widehat{M}$: **masking is convolution**, the processor is a
    programmable PSF (40 backward) → low-pass: blur with ringing (hard edge ⇒
    sinc-like kernel; Part-0 reflex); high-pass: DC gone ⇒ mean removed ⇒
    edges glow on darkness; directional: 38's oriented components isolated —
    Abbe–Porter worked as the canonical example (vertical row of dots ↔
    horizontal spatial frequencies ↔ the wires that vary vertically; the
    bookkeeping done carefully in one boxed figure) → phase objects:
    $t = e^{\ii\varphi} \approx 1 + \ii\varphi$; image intensity
    $\approx 1 + 2\,\Real[\ii\varphi] = 1$ — invisible; `phase_dot` shifts the
    DC by $\pi/2$: intensity $\approx 1 + 2\varphi$ — **phase becomes
    brightness**, Zernike's Nobel in four lines → mask edges ring (41's
    coherent artifacts are the working medium; hard vs apodised masks
    compared).
  - *verify:* empty-plane round trip = rotated object to machine precision
    (§4 limits test in view); energy conservation through unit mask (§4);
    Abbe–Porter prediction table vs computed images (every row/column mask
    case); phase-contrast linearity — output contrast vs $\varphi$ slope 2
    for small $\varphi$, departure quantified beyond
    (`numerical-observation` box); high-pass DC check — filtered image mean
    = 0 exactly.
  - *transfer:* `50-holography` — record the Fourier plane instead of masking
    it, and the mask becomes a *recorded field*: the VanderLugt correlator
    (advanced box here, front door there); `53-computational-imaging` — this
    bench in silicon: every convolutional layer is a bank of 4-f masks (one
    honest sentence on the analogy's limits); `35.5` capstone — this module
    scaled to a project, said in content; microscopy — phase contrast and
    dark field as clinical daily bread; `38-spatial-frequencies` backward —
    the playground was this bench's simulator all along.
  - *quiz:* inverted-image MC; mask-to-image matching; Abbe–Porter row/column
    item; phase-contrast mechanism MC (registry distractor); ringing-origin MC.
  - *explain:* the Abbe–Porter surprise to a friend, using 38's "spectrum has
    no location" language; why the phase object is invisible without the dot
    and visible with it; why every mask trades artifact for effect; what
    "programmable PSF" means and why it is the module's best summary.
  - *advanced:* the VanderLugt matched filter — correlate by masking with a
    conjugate spectrum; recognition as a bright dot; why it needs holography
    to build (the mask is complex-valued) — door to `50-holography`;
    dark-field as an extreme high-pass (block DC only) and its microscopy
    payoff; apodised masks — the engineering of gentle edges (Part-0 window
    functions, physically).
- **Core derivations:** (1) double transform ⇒ inversion; magnification −1.
  (2) mask multiplication ⇒ image-plane convolution with $\widehat{M}$ (the
  convolution theorem read backward — the course's most-used theorem used one
  last time). (3) the Abbe–Porter bookkeeping: mesh = vertical wires
  (varying along $x$: dots along $\nu_x$) + horizontal wires (dots along
  $\nu_y$); a horizontal-slit mask passing the $\nu_x$ row keeps the vertical
  wires — the figure that prevents the classic left/right error, drawn once,
  tested in the quiz. (4) weak-phase expansion and the $\pi/2$ dot:
  $I \approx 1 + 2\varphi(x,y)$; attenuating the dot boosts contrast (stated,
  optional arg in `phase_dot`). (5) hard-edge mask ⇒ sinc-kernel ringing with
  Gibbs-scale overshoot (03/41 cited).
- **Model specification draft:** System — the coherent 4-f chain: two ideal
  transform stages (39's model) with one thin complex mask in the shared
  focal plane; objects are complex transmittances. Dynamics — none beyond
  the two transforms and one multiplication. Boundary — finite grids (§4);
  masks are arrays, hard-edged unless apodised. Ensemble — deterministic;
  noise only via `wavelab.measurement` in labs. Ignored — lens apertures
  (pupils set to clear; 40 owns their effect), aberrations, reflection
  losses, polarization; partial coherence (the processor is a coherent
  instrument, 41's boxed assumption inherited). Valid when — paraxial;
  masks thin; object spectrum inside the grid's Nyquist disk with guard
  band. Failure modes — mask pixelation read as physics; wrap-around from
  aggressive high-pass; phase-contrast linearity trusted at large
  $\varphi$; forgetting the image inversion when comparing.
- **Epistemic classification:** inversion and mask-convolution duality —
  `theorem`; weak-phase contrast law — `approximation` (boxed with its
  $\varphi \ll 1$ edge); "the processor is a programmable PSF" —
  `definition`-level framing said explicitly; measured phase-contrast
  linearity range and Abbe–Porter table — `numerical-observation`;
  the coherent-instrument assumption — `model-assumption` (inherited from
  41, re-boxed here because the bench depends on it).
- **Misconceptions:** re-falsifies **`spectrum-maps-image-locations`**
  (owned by 38) with a physical mask — the registry entry's falsifier gains
  the optical staging, no re-pointing. NEW **`transparent-means-invisible`**
  — "A perfectly transparent object can never produce contrast in an
  image, whatever the instrument." Falsifying experiment: the hidden-message
  phase object images to uniform grey through the empty 4-f bench
  (measured: contrast < 10⁻⁶), then leaps into legibility when `phase_dot`
  is inserted — same object, same illumination, one quarter-wave dot;
  contrast vs $\varphi$ follows the predicted slope 2. Distractor: quiz
  option "if it absorbs nothing it must image to uniform brightness in any
  optical system".
- **Glossary terms:** `spatial-filtering` (סינון מרחבי), `4f-system`
  (מערכת 4f), `low-pass-filter` / `high-pass-filter` (מסנן מעביר־נמוכים /
  מעביר־גבוהים — coordinate with any EE deposits), `phase-contrast`
  (ניגודיות מופע), `dark-field` (שדה אפל), `abbe-porter-experiment`
  (ניסוי אבה–פורטר), `optical-correlator` (מתאם אופטי; `he_reject`
  candidate: קורלטור — advanced), `phase-object` (עצם מופע — translator to
  confirm).
- **Interactive controls and simulations:** the processor bench (see
  *explore*); Abbe–Porter theatre — mesh object with a rotatable slit mask
  and a prediction prompt before each release; phase-contrast reveal — the
  hidden message with dot radius/phase sliders and a contrast meter;
  apodisation A/B — hard vs Gaussian-edged low-pass side by side, ringing
  visible on one only.
- **Virtual lab outline** (`notebooks/en/labs/42-4f-processor.ipynb`):
  (1) empty-bench checks: inversion, energy, round trip; (2) mask gallery
  with predictions logged before each run (low, high, directional on the
  portrait and the mesh); (3) *Abbe–Porter measurement:* full row/column
  mask table on the mesh, each image classified, table vs prediction;
  (4) *phase-contrast measurement:* contrast vs $\varphi$ across seeds with
  detector noise (`measurement.add_noise`), fitted slope ± uncertainty vs
  the predicted 2; dot-attenuation bonus sweep; (5) design task: build the
  mildest mask that removes a specified halftone screen from a scanned
  image while keeping the portrait legible — the engineering finale (a
  §35.5 rehearsal, and the lab says so).
- **Real-experiment counterpart:** none practical at home as a true 4-f
  bench (two matched lenses on an optical rail exceed the course's
  kitchen-table budget); the honest pairing is the module's own puzzle
  heritage — a teaching-lab import cell for Abbe–Porter photographs
  (laser, mesh, two lenses, a slit cut in card) is provided for
  institutions that have a bench, and the phone-based 38 experiments
  remain the at-home spectral playground.
- **Media assets** (`render_fourier_optics.py`): (i) the money shot —
  camera tracking along the 4-f axis: object, dot lattice condensing,
  slit sliding in, wire family dissolving from the image; (j) phase-
  contrast reveal — invisible slide, dot dropping into the Fourier plane,
  message fading in. Language-neutral.
- **Quiz bank outline:** `Q-42-1` MC — empty-bench output vs object
  (OBJ-42-1); `Q-42-2` matching — four masks to four filtered images
  (OBJ-42-2); `Q-42-3` MC — Abbe–Porter: slit passes $\nu_x$ row, which
  wires survive (OBJ-42-3); `Q-42-4` MC — what the phase dot does and to
  which spectral component (OBJ-42-4; distractor
  `transparent-means-invisible`); `Q-42-5` MC — why the low-passed portrait
  shows fringes near edges (OBJ-42-5); `Q-42-6` free — explain "programmable
  PSF" and give one mask with its PSF (OBJ-42-2, OBJ-42-5).
- **Problem set outline:** analytical — double-transform inversion;
  weak-phase contrast with an attenuated dot (contrast $2\varphi/\sqrt{a}$
  for amplitude transmission $\sqrt{a}$); the directional mask's kernel.
  Computational — halftone-removal design task variants; dark-field vs
  phase-contrast on the same phase object (which sees what). Challenge —
  a toy VanderLugt: correlate a letter against a page using a complex mask
  built numerically (the hologram 50 will teach you to build physically);
  find the letter as a bright dot; break it by rotating the page 10°.
- **Runtime budget:** each bench update = 2 FFTs + 1 multiply at 256² —
  ms-scale; lab table runs ≤ 30 configurations at 512²; the correlator
  challenge ≤ 1024² once. In-browser comfortable.
- **Validation gates:** standard four with `--module 42-4f-processor`;
  plus the §4 empty-bench, energy-conservation, and mask tests landing
  with this module.
- **Open questions for the author:** hidden-message content for the phase
  object (needs to be language-neutral — recommendation: a simple icon,
  not text, per the media-asset rule's spirit); whether the freehand mask
  brush ships in v1 (recommendation: yes — it is 38's canvas re-used, and
  master plan §30 asks for manipulable filters); whether dark-field gets
  its own explore preset or stays in advanced (recommendation: preset —
  it is one click and lands the "extreme high-pass" point).

## 6. Part-level assessment and capstone hooks

- **Capstones fed, explicitly:** §35.5 (Fourier-optics image processor) *is*
  module 42 scaled to a project — the capstone brief should cite 42's bench and
  §5.5's design task as its seed; §35.1 (computational telescope) chains 40's
  pupil → PSF → sensor with 37's aberrations and 38's sampling — its noise
  budget uses `measurement` and its speckled long exposures use 41's ensembles;
  §35.2 (virtual optical bench) gains 39's f–lens–f chain as a propagation
  engine alongside part-10's ray engine.
- **Cross-module synthesis problems** (owned by the part, not one module):
  (a) *the camera datasheet* — from pupil diameter, focal length, λ, and pixel
  pitch, produce the full resolution story: Airy radius (40), MTF and cutoff
  (40), sensor Nyquist and aliasing risk (38), and the coherent caveat (41) —
  one problem, four modules; (b) *design the microscope illumination* — given a
  phase-rich specimen, choose between bright-field, oblique, dark-field, and
  phase contrast (39's Abbe picture + 41's coherence + 42's masks), and defend
  the choice in one paragraph; (c) *the phase problem* — 38's magnitude/phase
  swap, 42's inability to mask phase back into a lost spectrum, and a
  three-sentence bridge to holography (50) and crystallography.
- **Exam themes:** sketch the transform plane of a described image (and the
  image of a described mask); one-step numerics on $\nu = x/(\lambda f)$,
  Airy radius, and cutoff; pipeline choice with justification; predict-the-
  filtered-image items in the Abbe–Porter style; "what does this MTF curve
  forbid" reasoning.

## 7. Build order and validation gates

Build order `38 → 39 → 40 → 41 → 42` — teaching order and dependency order
coincide: 38 supplies the 2-D transform grammar and targets; 39 needs only 38
plus dictated part-09/10 names; 40 consumes 39's pupil-plane picture; 41
consumes 40's two PSFs; 42 consumes everything and must land last (its §5.5
design task is the part's exit exam). The part builds after part-09 and
part-10 (its §2 prerequisites are their built modules and dictated names);
`27-coherence` must exist for 41's bridge.

`imaging.py` lands incrementally with its owners: with 38 —
`fft2_centered`, `ifft2_centered`, `bar_target`, `spoke_target` plus the
separability/rotation/Parseval tests; with 39 — `lens_phase`,
`fourier_plane_field`, `pupil_disk` plus the convergence and scaling tests;
with 40 — `psf_from_pupil`, `otf_from_psf`, `mtf`, `zernike_phase`,
`edge_target` plus the cross-owner Airy tests (which require part-09's
`fraunhofer_pattern` and `airy_radius` to be importable — a hard sequencing
constraint, stated); with 41 — `amplitude_psf`, `image_coherent`,
`image_incoherent`, `speckle_field`, `speckle_contrast` plus the
cutoff-factor and speckle-statistics tests; with 42 — `four_f_process`,
`lowpass_mask`, `highpass_mask`, `directional_mask`, `phase_dot` plus the
empty-bench and energy tests. Later parts (13's `53-computational-imaging`,
capstones) may cite any of these names once merged.

Registry work: with 38, deposit NEW `spectrum-maps-image-locations`; with
39, NEW `fourier-plane-is-image`; with 40, NEW
`smaller-aperture-sharper-image`; with 41, NEW `coherent-always-sharper`;
with 42, NEW `transparent-means-invisible` — each `pending` until its page's
falsifier and distractor exist. No re-pointings belong to this part.
Glossary: each module deposits its §5 list; `numerical-aperture` is cited
from `36-instruments` (part-10) and `angular-spectrum` from
`32-fresnel-diffraction` (part-09) — neither is re-deposited here.

Per module: the standard four gates (README bottom) with the module id; the
§4 test additions must land *with* their functions, since §35.1/§35.5
capstone briefs will cite them as guarantees.

## 8. Deviations from the master plan

- **Merge (11.3 + 11.4 → `40-psf-otf`):** the PSF and the OTF are a Fourier
  pair; teaching them apart would re-enact the $G$-without-$\hat{H}$ split
  that `05-impulse-response` exists to prevent. Precedent:
  `02-damped-driven` ← 1.2 + 1.3 (README canonical map records the merge).
- **2-D transforms live in `imaging.py`:** the master plan implies a single
  Fourier toolkit; this plan keeps `fourier.py` strictly 1-D (part-00's
  ownership untouched) and gives the centred, physically scaled 2-D wrappers
  one home in `imaging.py`, where every consumer (38–42, part-13, capstones)
  lives downstream. Logged as a design decision in §4.
- **Speckle added (41):** master plan §18 does not mention speckle; this plan
  makes it 41's statistical crown because it is the course-wide payoff of
  `00-phasors`' random walk and the cheapest quantitative statistical-optics
  experiment available to a student with a laser pointer.
- **Partial-coherence calculus deferred out of course:** mutual-coherence
  propagation and the TCC are named honestly in 41 and not developed —
  Goodman's statistical-optics machinery exceeds the course's scope; 41
  interpolates the two ideal limits with 27's $|\gamma|$ and says so in a
  scope box. Van Cittert–Zernike appears as an idea (per part-08's deferral),
  not as a theorem with proof.
- **Scalar and paraxial throughout:** vector diffraction and high-NA imaging
  are excluded by every model spec in the part; quantitative claims are
  bounded at NA ≲ 0.3 and the boundary is stated where students will meet
  real microscopes.
- **Historical staging added:** Abbe's theory (39), Abbe–Porter 1906 (42),
  and Zernike's phase contrast (42) structure the narrative; the master plan
  lists operations, this plan hangs them on their discovery experiments.
- **Edge enhancement delivered as mask family:** master plan 11.6 lists
  "edge enhancement" as a separate operation; it is high-pass plus
  directional filtering in 42's mask palette, not a fifth mechanism — one
  line in content states this.
- **Convention note:** all seeded formulas carry the course phase convention
  ($e^{\ii(kx-\omega t)}$, $e^{-\ii\omega t}$; forward transform kernel
  $e^{-\ii 2\pi(\nu_x x + \nu_y y)}$ matching `fourier.spectrum` axis by
  axis); Goodman's engineering $e^{+j\omega t}$ pages are read through the
  standing $j \leftrightarrow -\ii$ dictionary of
  `content/en/conventions.md`, and §5.2 flags the quadratic-phase kernels as
  the one place a mixed convention silently conjugates every spectrum.
