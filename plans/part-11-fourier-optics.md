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
`numerical-aperture` is expected from part-10 (36's instrument vocabulary); if absent
when this part builds first, module 39 deposits it (coordination note, precedent:
part-01's `bandwidth`).

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

<!-- CHUNK-BREAK -->
