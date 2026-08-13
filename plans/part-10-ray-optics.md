# Part X — Geometrical Optics — Implementation Plan

> **Master plan:** §17 (Part X). **Modules:** `33-fermat`, `34-lenses`, `35-abcd-matrices`, `36-instruments`, `37-aberrations`. **Status:** planned.
> Canonical numbering, invariants, and conflict log: [README.md](README.md).

## 1. Part overview and narrative arc

Part X is the course's deliberate inversion of the traditional optics syllabus. A
conventional course *starts* with rays and asks students to accept them; this course has
spent nine parts building wave optics, and now **derives rays from it** — geometrical
optics enters as an approximation, presented as such, exactly as master plan §17 insists.
The part opens with an honesty box (an `approximation` admonition, the first thing the
reader meets): a ray is not a thing light *is*, it is where the phasor sum over
neighbouring paths is *stationary*. Fermat's principle **is** stationary phase — paths
near the stationary one add in phase, like module `00-phasors`' aligned arrows, while all
others wind into cancelling spirals, the same cancellation `32-fresnel-diffraction` drew
as the Cornu spiral and `28-huygens` built the wavelet sum from. The λ → 0 (eikonal)
limit is named, its validity boundary stated, and the whole part lives knowingly inside
that boundary. This framing is the plan's single largest enhancement over a traditional
treatment, and it is structural, not decorative: **rays are earned, not assumed**.

The arc is a nesting of models, each deriving the next and each measured against its
parent. Module 33 derives ray optics from wave optics (stationarity of optical path
length), and kills the "least time" teleology properly — reflection off a plane mirror is
a genuine minimum, but a mirror curved more tightly than the tangent ellipse makes the
physical path a local *maximum* of the very same functional, so "light seeks the fastest
route" dies as a mechanism and survives only as a slogan. Module 34 derives the paraxial
model from exact rays — one spherical surface, done honestly with small angles, then
mirrors and thin lenses as corollaries — and fixes the course's ray-optics sign
convention once, in a boxed table, never to be re-litigated. Module 35 compresses the
paraxial model into the course's **second operator formalism**: ray state $(y, \theta)$,
elements as $2\times2$ matrices, systems as ordered products — the exact grammar of
`21-jones-calculus`, and the plan says so out loud, in the same words part-07 used for
Jones ("states are vectors, elements are operators, cascades are ordered products, and
order matters"). Module 36 spends the formalism: camera, magnifier, microscope, telescope,
each an ABCD design exercise — with **empty magnification** as the honesty centerpiece,
where the part's ray designs are cross-checked against Part IX's diffraction limit and
found wanting. Module 37 closes the loop from inside: exact ray tracing (full Snell per
surface) is turned against the paraxial model that was derived from it, and the
discrepancies — spherical aberration, coma, astigmatism, chromatic aberration — are
*measured*, spot diagram by spot diagram, the way a lens designer measures them.

So the part opens by deriving its own domain of validity and closes by measuring where it
breaks — twice: 36 measures ray optics against wave optics (diffraction wins at the
focus), 37 measures paraxial optics against exact rays (the third-order terms win at the
aperture edge). Two ideas run the whole length. First, **optical path length is
accumulated phase** ($\varphi = k_0 \cdot \mathrm{OPL}$): imaging works because a lens
equalises OPLs from object point to image point, and aberrations are nothing but the
failure of that equalisation — which is exactly the wavefront-error currency that
`40-psf-otf` converts into point-spread functions. Second, the **operator grammar**: the
same six matrix functions specced here propagate Gaussian beams via the $q$-parameter in
`43-gaussian-beams` and decide cavity stability in `44-resonators` — part-12 cites this
part's function names verbatim, so §4's names are frozen on merge.

Hecht is the companion text throughout (topic references, never chapter numbers), with
Feynman's lifeguard story told — and then told *honestly* — in 33.

## 2. Position in the course

- **Requires:**
  - `00-phasors`: coherent vs random-phase addition — aligned arrows dominate a sum;
    the arrow arithmetic that stationary phase runs on.
  - `28-huygens`: every point on a wavefront radiates a wavelet; the ray is a bookkeeping
    device for where the wavelet sum survives.
  - `32-fresnel-diffraction`: the Cornu-spiral picture — contributions far from
    stationarity curl up and cancel; 33 cites it as the rigorous version of its opening
    argument.
  - `17-refraction`: `interfaces.snell_angle` (complex-safe Snell) and the phase-matching
    derivation; 17 promised the full variational route to Snell as "the third
    derivation" — 33 delivers it.
  - `16-light-in-matter`: index as medium response; $v = c/n$, $\lambda = \lambda_0/n$ —
    the physical content of "optical" in optical path length; `em.sellmeier` and
    `em.refractive_index` supply $n(\lambda)$ for 37's chromatic aberration.
  - `14-em-waves`: plane waves and $\mathbf{k}$; rays are normals to wavefronts.
  - `21-jones-calculus`: the operator grammar — state vector, operator, ordered product
    in meeting order — learned once there, reused verbatim in 35.
  - `30-apertures`: the dictated results `airy_radius` and `rayleigh_criterion` — 36's
    empty-magnification cross-check and the floor under every "perfect focus" claim.
- **Feeds:**
  - `38-spatial-frequencies`–`42-4f-processor`: the paraxial imaging skeleton (conjugate
    planes, focal planes, magnification) that Fourier optics dresses in amplitude and
    phase; `39-fourier-lens` puts the transform in 35's focal plane; `40-psf-otf` turns
    37's OPL error into the PSF.
  - `43-gaussian-beams`: the same ABCD matrices propagate the complex $q$-parameter —
    part-12 consumes `free_space`, `thin_lens`, `mirror`, `refraction_flat`,
    `refraction_spherical`, `cascade` by exact name.
  - `44-resonators`: cavity stability as a condition on the round-trip ABCD matrix
    (planted as a one-line trailer in 35's advanced section).
  - Capstones §35.1 (computational telescope) and §35.2 (virtual optical bench) — see §6.
- **Explicitly not assumed:** amplitude transport along rays (intensity via ray density
  is gestured at, never developed); wave-aberration theory (Zernike polynomials appear
  in one research box, the machinery belongs to `40-psf-otf`); skew rays and 3-D
  tracing (meridional plane only — §8); thick-lens principal-plane machinery in core
  (advanced box in 35 — §8); radiometry/photometry beyond the $1/N^2$ brightness
  argument; any Gaussian-beam content (the matrices are handed to part-12, not used on
  beams here).

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|
| `33-fermat` | `content/en/ray-optics/33-fermat.md` | Fermat's principle: rays from stationary phase | 10.1 | Hecht, propagation of light — Fermat's principle; Feynman QED lifeguard (popular aside) | planned |
| `34-lenses` | `content/en/ray-optics/34-lenses.md` | Spherical surfaces, mirrors, and thin lenses | 10.2 | Hecht, geometrical optics — refraction at spherical surfaces, thin lenses, mirrors | planned |
| `35-abcd-matrices` | `content/en/ray-optics/35-abcd-matrices.md` | Ray-transfer matrices: the second operator formalism | 10.3 | Hecht, geometrical optics — analytical ray tracing / matrix methods | planned |
| `36-instruments` | `content/en/ray-optics/36-instruments.md` | Optical instruments by design | 10.4 | Hecht, optical instruments — camera, magnifier, microscope, telescope | planned |
| `37-aberrations` | `content/en/ray-optics/37-aberrations.md` | Aberrations: where the paraxial model breaks | 10.5 | Hecht, more on geometrical optics — Seidel aberrations, chromatic aberration | planned |

## 4. Shared infrastructure for this part

**`src/wavelab` — existing used:** `interfaces.snell_angle` (37's exact tracer refracts
with it at every surface; owned by part-06), `interfaces.critical_angle` (exact-trace TIR
guard); `em.sellmeier` and `em.refractive_index` (37's $n(\lambda)$; owned by part-05);
`diffraction.airy_radius`, `diffraction.rayleigh_criterion` (36's empty-magnification
cross-check; dictated names, owned by part-09); `phasors.superpose` (33's path-arrow
sums; owned by part-00); `measurement.add_noise` + fit helpers (noisy conjugate data,
spot-metric uncertainty); `validation.scaling_exponent`, `validation.convergence_study`,
`validation.seed_study`, `validation.relative_error`.

**`src/wavelab` — new: `rayoptics.py`** (introduced and owned by this part; README
ownership table; part-12 cites the six matrix-builder names verbatim — frozen on merge).
Docstring model spec:

- **System:** meridional rays in axially symmetric optical systems — ray state
  $(y, \theta)$ at a reference plane, with $\theta$ the slope $dy/dz$; paraxial elements
  as $2\times2$ real ray-transfer matrices; exact tracing over ordered lists of spherical
  surfaces.
- **Dynamics:** none integrated — straight-line propagation between surfaces; refraction
  and reflection applied algebraically at each surface (paraxial: matrix products;
  exact: `interfaces.snell_angle` per surface, sines not slopes).
- **Boundary:** sequential surfaces on a single optical axis; apertures as hard stops on
  $|y|$; mirrors handled in the unfolded convention (propagation always "forward").
- **Ensemble:** deterministic; ray bundles are caller-built fans; noise enters only via
  `wavelab.measurement` in the labs.
- **Ignored:** amplitude, phase, polarization, and diffraction — rays carry direction
  only, wave optics owns everything else; skew rays (meridional plane only — the
  restriction is honest and logged); Fresnel losses and ghost reflections (belong to
  `interfaces.py`); scattering.
- **Valid when:** every feature is many wavelengths across (the λ → 0 limit); paraxial
  functions additionally require $|\theta| \ll 1$ and $|y| \ll |R|$.
- **Failure modes:** paraxial matrices trusted at large aperture (that *is* spherical
  aberration — 37 measures it); ray results read at foci, caustics, or edges where
  diffraction rules (the real spot floor is `airy_radius`); sign errors from mixing
  conventions (Hecht only, 34's box); mirror matrices used without unfolding.

Function-level sketch (signatures + contracts). The six matrix builders and `cascade`
are the **dictated shared names** part-12 consumes:

```python
free_space(d) -> M                    # [[1, d], [0, 1]]; det = 1
thin_lens(f) -> M                     # [[1, 0], [-1/f, 1]]; det = 1
mirror(R) -> M                        # [[1, 0], [2/R, 1]] in the unfolded convention;
                                      #   f = -R/2 (Hecht sign: concave mirror R < 0, f > 0)
refraction_flat(n1, n2) -> M          # [[1, 0], [0, n1/n2]]; det = n1/n2
refraction_spherical(n1, n2, R) -> M  # [[1, 0], [-(n2 - n1)/(n2 R), n1/n2]]; det = n1/n2;
                                      #   R -> inf reproduces refraction_flat exactly
cascade(*matrices) -> M               # arguments in the order light MEETS the elements;
                                      #   returns M_N @ ... @ M_1 — deliberate namespaced
                                      #   coexistence with polarization.cascade: same
                                      #   operator grammar, same meeting-order contract
Ray(y, theta)                         # dataclass: meridional ray state; theta = dy/dz [rad]
trace_paraxial(system, ray) -> Ray    # applies the (list of) matrices, returning the final
                                      #   state (and intermediates when given the list)
trace_exact(surfaces, ray) -> path    # sequential exact meridional trace; full Snell via
                                      #   interfaces.snell_angle at each spherical surface;
                                      #   returns the (z, y) polyline + final ray; flags TIR
image_distance(system) -> d           # distance past the exit plane where the extended
                                      #   matrix has B = 0 (image plane); inf if afocal
system_focal_length(system) -> f      # f = -1/C for equal outer media; inf when C = 0
lensmaker(n, R1, R2, n_medium=1.0) -> f   # thin-lens focal length; immersion via n_medium
two_lens(f1, f2, d) -> system         # cascade(thin_lens(f1), free_space(d), thin_lens(f2));
                                      #   the generic instrument chassis (telescope: d = f1 + f2)
spot_diagram(surfaces, rays, plane=None) -> heights
                                      # transverse intercepts of an exact-traced fan at the
                                      #   image plane (default: paraxial image plane); 2-D spot
                                      #   synthesised by revolution for on-axis bundles,
                                      #   labelled "tangential fan" off-axis (meridional-only)
longitudinal_aberration(surfaces, heights) -> dz
                                      # axis crossings of exact rays minus the paraxial focus
chromatic_focus_shift(n_of_lam, R1, R2, lams) -> f_of_lam
                                      # lensmaker evaluated on n(lambda); callers build
                                      #   n_of_lam from em.sellmeier
abbe_number(n_of_lam) -> V            # V_d = (n_d - 1)/(n_F - n_C) at 587.6/486.1/656.3 nm
```

**`tests/physics/` additions:**

- *limits:* two spherical surfaces collapse to the thin lens — element-wise agreement of
  `cascade(refraction_spherical(1, n, R1), free_space(t), refraction_spherical(n, 1, R2))`
  with `thin_lens(lensmaker(n, R1, R2))` as $t \to 0$; `refraction_spherical(n1, n2, R)`
  → `refraction_flat(n1, n2)` as $R \to \infty$; `trace_exact` → `trace_paraxial`
  point-by-point as launch angle → 0; `image_distance` of a bare thin lens reproduces
  $1/s_o + 1/s_i = 1/f$ over a conjugate grid.
- *conservation:* $\det M = n_1/n_2$ for every element builder; $\det$ of `cascade`
  equals $n_{\text{in}}/n_{\text{out}}$ through randomly generated stacks
  (hypothesis-driven); afocal two-lens systems satisfy $A\,D = 1$ in air.
- *convergence:* transverse ray aberration of a single spherical surface scales as $h^3$
  (fitted exponent 3.0 via `convergence_study`) and longitudinal as $h^2$ — the
  exact-to-paraxial error order that names "third-order aberrations";
  `chromatic_focus_shift` linear in $\Delta n$ for small $\Delta n$.
- *scaling:* transverse magnification $m = -s_i/s_o$ measured from traced conjugates;
  longitudinal magnification of a short axial segment fits $m_L = m^2$ (exponent 2.00
  via `scaling_exponent`); `lensmaker` $f$ linear in $R$ at fixed shape.
- *seeds:* `spot_diagram` RMS radius of a seeded noisy bundle exactly reproducible;
  best-focus location from noisy fans scatters as $1/\sqrt{M}$ across $M$ seeds via
  `seed_study`.
- *dimensions:* $d$, $R$, $f$ in meters against the `units` registry; $\theta$
  dimensionless (rad); optical power in diopters (1/m).

**Shared media:** one render script `media/render/render_rayoptics.py` produces all Part
X MP4s (shot lists in §5). **Glossary themes:** variational vocabulary (33), imaging
vocabulary + the sign convention (34), matrix-optics vocabulary (35), instrument
vocabulary (36), aberration vocabulary (37). `fermats-principle` (part-06), `wavefront`
(part-05), `dispersion` (part-04) are cited, never re-deposited.

## 5. Module specifications

### 5.1 `33-fermat` — Fermat's principle: rays from stationary phase

- **Identity and scope:** master-plan notebook 10.1. Optical path length, Fermat as
  stationarity (not minimality), reflection and refraction derived variationally, the
  maximum case, equal-OPL imaging as the bridge to 34. This module owns the variational
  machinery that `17-refraction` deliberately deferred ("a taste here, the meal there").
  Deferred from here: the eikonal equation derivation (advanced box only, stated not
  proved); amplitude transport (out of the course's core entirely).
- **Prerequisites:** `00-phasors` (aligned arrows dominate; random phases cancel);
  `28-huygens` (wavelet sum); `32-fresnel-diffraction` (Cornu-spiral cancellation — the
  rigorous form of this module's opening argument); `17-refraction` (`snell_angle`,
  phase matching, and the promised third derivation); `16-light-in-matter` ($v = c/n$).
- **Learning objectives:**
  - `OBJ-33-1` — Define optical path length OPL = integral of n ds (= n L in uniform
    media), and relate it to accumulated phase phi = k0 * OPL and travel time t = OPL/c.
  - `OBJ-33-2` — State Fermat's principle as stationarity of the OPL, and justify it by
    stationary phase: paths near a stationary path add in phase, all others cancel.
  - `OBJ-33-3` — Derive the law of reflection and Snell's law from stationarity of the
    OPL, identifying which stationary point each is.
  - `OBJ-33-4` — Exhibit a reflection geometry (mirror curved inside the tangent
    ellipse) in which the physical path is a local maximum of the OPL, and use it to
    refute "light always takes the fastest path".
  - `OBJ-33-5` — Explain why a converging lens can image at all: every ray from object
    point to image point accumulates the same OPL, glass thickness compensating
    geometric length.
- **Mathematical background:** has — one-variable stationarity ($dT/dx = 0$, from 17),
  phasor sums, path geometry; introduced here — a functional (number from a *path*),
  stationarity of a functional explored numerically, never with Euler–Lagrange (named
  in advanced as the road not taken).
- **Physical intuition goals:** (1) predict, for any source–mirror–receiver sketch,
  *where* the reflection point sits, by sliding a trial point and feeling the OPL
  flatten; (2) say why "the path where the time is flattest" beats "the fastest path"
  as a description — and produce the counterexample; (3) rank paths by how much they
  contribute to the field, using the half-wavelength criterion; (4) explain a mirage
  and a lens with the same sentence (light concentrates where OPLs agree).
- **Section skeleton seeds:**
  - *puzzle:* aim a laser at a mirror so the spot hits a target: one angle works —
    yet `28-huygens` said every point of the mirror radiates wavelets everywhere. Boxed
    question: if light explores *every* path, why do we see exactly *one* — and what
    singles it out? (The part-opening `approximation` honesty box sits immediately
    above this puzzle: geometrical optics as the λ → 0, stationary-phase limit of
    everything since Part IX.)
  - *predict:* (1) does light from A to B via a mirror take the *shortest* mirror path?
    the *fastest*? always? (targets NEW `light-takes-fastest-path`); (2) drag the
    reflection point off the equal-angle position — does total path length increase or
    decrease? For a *curved* mirror too?; (3) which paths matter to the field: only the
    stationary one, those within about half a wavelength of it in OPL, or all equally?;
    (4) two rays leave one object point through different parts of a lens and meet at
    the image — which one arrived "first"?
  - *explore:* path explorer — source, receiver, one interface (mirror or refracting
    boundary); drag the intermediate point, live readouts of geometric length, OPL,
    travel time, and *accumulated phase*; a phasor strip beneath (module 00's arrows,
    one per trial path in a bundle) showing alignment at stationarity; mirror-curvature
    slider morphing plane → ellipse-tangent → tighter-than-ellipse, with the OPL curve
    flipping minimum → flat → maximum while the physical ray never moves.
  - *derive:* OPL and phase ($\varphi = k_0\,\mathrm{OPL}$, from
    $\psi = \Real[A\,e^{\ii(kx - \omega t)}]$ with $k = n k_0$) → stationary phase:
    bundle the paths, sum the arrows, paths within $\sim\lambda/2$ of stationarity add
    coherently (cite 00's $N$ vs $\sqrt{N}$, 32's spiral) → reflection from
    $d(\mathrm{OPL})/dx = 0$: equal angles, and a *minimum* for the plane mirror →
    Snell from stationarity (the third derivation, 17's promise redeemed) → the ellipse
    argument: all focus-to-focus paths via the ellipse are equal-OPL (definition of the
    ellipse); a mirror tangent inside it makes the physical path a maximum → imaging as
    equal OPL: the marginal ray's longer geometric path through thin glass equals the
    axial ray's shorter path through thick glass — 34's lens, pre-derived.
  - *verify:* stationary point of the numerical OPL curve matches
    `interfaces.snell_angle` to $10^{-10}$ (extends 17's check to curved interfaces);
    phasor-bundle sum: resultant amplitude vs bundle-truncation radius plateaus once
    paths differing by $> \lambda/2$ are included (`numerical-observation` box —
    "the first Fresnel zone carries the field"); curvature sweep: sign of the OPL
    second derivative flips exactly at the ellipse tangent curvature while the
    equal-angle ray persists.
  - *transfer:* mirages and gradient-index optics ($n$ varying continuously — 17's
    advanced invariant, now variational); the equal-OPL condition returns as 34's
    imaging and 37's aberration currency (unequal OPLs = blur); `40-psf-otf` converts
    residual OPL spread to the PSF; Feynman's path-integral quantum mechanics — the
    same arrow sum with action in place of OPL (one advanced sentence).
  - *quiz:* stationarity vs minimality MC (the maximum case); OPL/phase numerics;
    which-paths-contribute MC; mirror-geometry numeric; lens equal-OPL conceptual.
  - *explain:* rewrite "light takes the fastest path" so it is true — and say what the
    lifeguard story gets right (the trade-off) and wrong (the optimisation); why the
    ellipse mirror makes *every* path equally good and what that does to focusing;
    where the "decision" happens if light has no intent.
  - *advanced:* the eikonal limit stated — substitute
    $\psi = a\,e^{\ii k_0 S}$ into the wave equation, keep leading order in $1/k_0$:
    $|\nabla S|^2 = n^2$, rays are the integral curves of $\nabla S$ — the formal
    version of everything above, with its failure points named (foci, caustics, edges:
    exactly Part IX's territory and 37's caustic). Safe to skip; nothing later depends
    on it.
- **Core derivations:** (1) OPL: $\mathrm{OPL} = \int n\,ds$; phase
  $\varphi = k_0\,\mathrm{OPL}$; time $t = \mathrm{OPL}/c$ — three readings of one
  number. (2) stationary phase: total field
  $\propto \sum_{\text{paths}} e^{\ii k_0 L_j}$; where $dL/d(\text{path}) = 0$
  neighbouring arrows align, elsewhere they wind — a curvature argument, quantified by
  the $\lambda/2$ half-zone criterion. (3) reflection:
  $L(x) = \sqrt{h_1^2 + x^2} + \sqrt{h_2^2 + (d - x)^2}$; $L'(x) = 0$ gives
  $\sin\theta_i = \sin\theta_r$, and $L'' > 0$: a minimum. (4) refraction:
  $\mathrm{OPL}(x) = n_1\sqrt{h_1^2 + x^2} + n_2\sqrt{h_2^2 + (d - x)^2}$;
  $d(\mathrm{OPL})/dx = 0$ gives $n_1\sin\theta_1 = n_2\sin\theta_2$ — 17's $T(x)$
  scaled by $c$, now read as phase stationarity. (5) the maximum: focus-to-focus
  reflections off an ellipse all satisfy $r_1 + r_2 = 2a$ (equal OPL, degenerate
  stationarity); for a mirror tangent at the same point but curved inside the ellipse,
  the physical path is a strict local maximum — computed and plotted. (6) imaging:
  equal-OPL from object to image through every lens zone; solved for the required
  thickness profile → a spherical-cap profile in the paraxial limit, previewing 34.
- **Model specification draft:** System — a point source, a receiver, and one
  reflecting or refracting boundary in 2-D; the object of study is the OPL functional
  over one-bounce paths. Dynamics — none; paths are geometric trials, fields enter only
  as attached phasors $e^{\ii k_0 L}$. Boundary — perfect mirrors and sharp index
  steps; media uniform between them. Ensemble — deterministic; the phasor-bundle
  experiment sums a deterministic fan. Ignored — amplitudes (all trial arrows unit
  length), obliquity factors, multiple bounces, polarization. Valid when — geometry is
  many wavelengths across, so the half-zone bundle is narrow compared to the apparatus.
  Failure modes — reading "stationary" as "minimum"; treating the ray as a physical
  filament; using the picture where zones are not small (edges, foci — Part IX rules
  there).
- **Epistemic classification:** Fermat stationarity — `theorem` (given the wave model;
  the stationary-phase argument is the proof sketch); the λ → 0 framing —
  `approximation` (the part-opening box; mandatory admonition satisfied and then some);
  half-zone dominance plateau — `numerical-observation`; "light explores all paths" —
  `model-assumption` of the phasor-sum picture, flagged as the course's chosen
  language; equal-OPL imaging — `theorem`.
- **Misconceptions:** NEW `light-takes-fastest-path` — "Light always takes the path of
  least time." Falsifying experiment: the path explorer's curvature sweep — for a
  mirror curved inside the tangent ellipse, the measured OPL of the physical
  (equal-angle) path is a local *maximum*: every neighbouring trial path is faster,
  yet the ray is where it is. Distractor: quiz option "the reflected ray always marks
  the minimum-time route". The *teleology* ("light chooses") is handled in predict/
  explain prose, as part-06 §8 ruled — the registry entry carries only the falsifiable
  minimality claim.
- **Glossary terms:** `optical-path-length` (cited, deposited by `23-interference`) · `stationary-phase`
  (פאזה סטציונרית — translator to confirm; `he_reject` candidate: פאזה נייחת) ·
  `variational-principle` (עקרון וריאציוני) · `ray` (קרן) · `eikonal` (איקונל —
  transliteration, translator to confirm). `fermats-principle` cited from part-06's
  deposit, not re-added.
- **Interactive controls and simulations:** path explorer (drag point; OPL/time/phase
  readouts; phasor strip); curvature-sweep mirror (plane ↔ ellipse ↔ tighter);
  refraction variant with $n_1, n_2$ sliders; bundle-width control for the phasor sum
  (how many trial paths, how wide).
- **Virtual lab outline** (`notebooks/en/labs/33-fermat.ipynb`): (1) path explorer —
  find the reflection stationary point by hand, compare to equal angles; (2) refraction
  — locate stationarity, verify against `interfaces.snell_angle` ($10^{-10}$);
  (3) phasor-bundle sum via `phasors.superpose` — resultant vs bundle width, find the
  $\lambda/2$ plateau; (4) curvature sweep — plot $\mathrm{OPL}''$ at the stationary
  point vs mirror curvature, find the sign flip at the ellipse tangent;
  (5) *measurement culture:* locate the stationary point from a *noisy* sampled OPL
  curve (`measurement.add_noise`), report its position ± uncertainty across seeds and
  compare with the Snell prediction.
- **Real-experiment counterpart:** laser pointer, plane mirror, protractor paper —
  verify equal angles to a degree; string-and-two-pins ellipse drawing to make
  "equal path length from focus to focus" tactile. The stationary-*phase* content has
  no cheap physical counterpart — stated honestly; the interference machinery lives in
  Parts VIII–IX.
- **Media assets** (`render_rayoptics.py`): (a) path-bundle phasor sum — fan of paths
  A→mirror→B, each with its arrow; arrows align near the equal-angle path, wind far
  from it; the resultant grows only from the aligned bundle; (b) curvature morph — the
  mirror bends through the tangent-ellipse curvature; the OPL-vs-trial-point curve
  flips minimum → flat → maximum while the drawn ray stays fixed. Language-neutral, no
  burned-in text.
- **Quiz bank outline:** `Q-33-1` MC — is the reflected path always fastest
  (OBJ-33-4, distractor `light-takes-fastest-path`); `Q-33-2` numeric — OPL and phase
  through layered media (OBJ-33-1); `Q-33-3` MC — which trial paths contribute to the
  field (OBJ-33-2); `Q-33-4` numeric — stationary point of a two-medium crossing
  (OBJ-33-3); `Q-33-5` MC — equal-OPL reading of a lens (OBJ-33-5); `Q-33-6` free —
  state Fermat's principle without teleology and without "minimum" (OBJ-33-2,
  OBJ-33-4).
- **Problem set outline:** analytical — apparent depth via stationarity; the parabolic
  mirror focuses parallel rays exactly (equal-OPL proof); ellipse degenerate case.
  Computational — mirage from $n(y)$ by direct OPL stationarity over polyline paths,
  compared with 17's ray-invariant. Challenge — anticipate the zone plate: block the
  *non*-aligned half-zones on a straight path and show the field at B grows
  (back-reference `32-fresnel-diffraction`).
- **Runtime budget:** $10^4$-point OPL scans and few-hundred-arrow phasor sums —
  trivial in Pyodide; curvature sweep precomputed as MP4 (b).
- **Validation gates:** standard four (README) with `--module 33-fermat`.
- **Open questions for the author:** does the part-opening `approximation` box live
  above 33's puzzle (recommendation: yes, it is the part's front door) or duplicated in
  the part landing page? Does the eikonal box show the substitution or only the result
  (recommendation: result plus one line of where it comes from)?

### 5.2 `34-lenses` — Spherical surfaces, mirrors, and thin lenses

- **Identity and scope:** master-plan notebook 10.2. Paraxial refraction at one
  spherical surface, derived; mirrors and thin lenses as corollaries; focal length,
  conjugates, magnification; the **sign convention fixed once** in a boxed table
  (Hecht's, named); lensmaker's equation; ray diagrams the student builds; the
  half-covered-lens experiment. Deferred: matrix packaging (35), instruments (36),
  everything beyond paraxial (37), thick lenses (35 advanced, §8).
- **Prerequisites:** `33-fermat` (equal-OPL imaging — the "why" this module's algebra
  serves); `17-refraction` (Snell; `snell_angle` for the verify section);
  `16-light-in-matter` ($n$); `30-apertures` (for the transfer bullet only:
  `airy_radius` as the floor under "point image").
- **Learning objectives:**
  - `OBJ-34-1` — Derive the paraxial single-surface equation
    n1/s_o + n2/s_i = (n2 - n1)/R from Snell's law with small angles, and state the
    validity condition (small theta, y << R).
  - `OBJ-34-2` — Apply the course (Hecht) sign convention to assign signs to s_o, s_i,
    R, f, and m in any single-element layout, for lenses and for mirrors, without
    mixing conventions.
  - `OBJ-34-3` — Locate and classify images (real/virtual, upright/inverted,
    enlarged/reduced) with 1/s_o + 1/s_i = 1/f and m = -s_i/s_o, including virtual
    objects and virtual images.
  - `OBJ-34-4` — Compute thin-lens focal lengths from the lensmaker's equation
    1/f = (n/n_m - 1)(1/R1 - 1/R2) and predict the effect of immersion (n_m > 1).
  - `OBJ-34-5` — Construct the three principal rays for a lens or mirror and read
    image position and magnification from the diagram.
  - `OBJ-34-6` — Predict that covering part of a lens aperture leaves the image whole
    but dimmer, and explain why every image point receives rays from the entire
    aperture.
- **Mathematical background:** has — Snell, small-angle expansions, similar triangles;
  introduced here — the discipline of a *signed* geometry (the sign table as an
  algebra, not a mnemonic); conjugate variables ($s_o \leftrightarrow s_i$ symmetry).
- **Physical intuition goals:** (1) given any object position against a known lens,
  sketch the image's side, orientation, and rough size before computing; (2) know what
  happens to the image as the object crosses the focal point (real → virtual flip,
  and the magnification blow-up between); (3) predict the half-covered-lens outcome
  and defend it with a ray diagram; (4) say why immersing a lens in water weakens it.
- **Section skeleton seeds:**
  - *puzzle:* hold a magnifier at arm's length toward a window: on a paper behind it,
    the window appears — upside down, small, and *sharp*. Cover the top half of the
    lens with a post-it. Boxed question: what does the paper show now — the bottom half
    of the window, the whole window dimmer, or a blur? (Answer withheld; the predict
    section forces commitment.)
  - *predict:* (1) the post-it question (targets NEW `half-lens-half-image`);
    (2) object inside the focal length — where is the image, and can you catch it on
    paper?; (3) a lens is moved from air into water — does $f$ grow, shrink, or hold?;
    (4) two convex surfaces vs plano-convex of equal $|R|$ budget — which is stronger?
  - *explore:* imaging bench — one spherical surface, mirror, or thin lens; object
    slider (from $\infty$ to inside $f$), live ray diagram with the three principal
    rays drawn, image marker with real/virtual and $m$ readouts; **build-a-diagram
    mode**: the student places the three rays by hand (snap-assisted) and the bench
    scores the construction before revealing; aperture shade slider (cover 0–90% of
    the lens; watch image brightness fall, sharpness and completeness hold).
  - *derive:* single spherical surface: Snell → small angles → the $n_1/s_o + n_2/s_i$
    equation, with the equal-OPL route (33) shown as the two-line alternative → sign
    convention boxed table (below) → mirror as the same geometry
    ($1/s_o + 1/s_i = -2/R = 1/f$) → thin lens: two surfaces back-to-back, inner
    image as outer object → lensmaker → conjugates and $m = -s_i/s_o$ → the
    Newtonian form $x_o x_i = f^2$ (stated; derived in problems).
  - *verify:* paraxial single-surface prediction vs `trace_exact` at shrinking angles
    (agreement → 0 as $\theta^3$ — quoting the §4 convergence test, and *previewing
    37*: the disagreement at finite aperture is not a bug); half-covered lens
    simulated: exact fan with the top half of the aperture stopped — every image
    point still forms, at reduced ray count (`numerical-observation` box: "image
    intensity scales with open aperture area; image *extent* does not");
    conjugate-pair scan fits $1/s_i$ vs $1/s_o$ to slope $-1$, intercept $1/f$.
  - *transfer:* aperture ↔ brightness ↔ resolution — the shade slider returns as the
    camera stop (36) and as the PSF width (`30-apertures` now, `40-psf-otf` later:
    a *smaller* aperture means a *wider* diffraction spot); virtual images run the
    magnifier (36); the sign table is 35's matrix bookkeeping; unequal OPLs at finite
    aperture are 37's subject.
  - *quiz:* sign-assignment drills; image classification; lensmaker numerics;
    the post-it MC; immersion MC.
  - *explain:* why the image inverts (in terms of rays crossing, not "lenses invert");
    why there is no image on paper when the object sits inside $f$ — and what the eye
    sees instead; talk a photographer out of "my cracked lens will photograph half the
    scene".
  - *advanced:* the aplanatic points of a sphere (one perfect conjugate pair exists
    even non-paraxially — a teaser that 37's pessimism has exceptions); Fresnel lenses
    (the equal-OPL profile collapsed into zones). Safe to skip.
- **Core derivations:** (1) single surface: rays from axial object point through a
  spherical cap; Snell $n_1\sin\theta_1 = n_2\sin\theta_2$ with
  $\sin\theta \approx \theta$ and exterior-angle bookkeeping gives
  $\dfrac{n_1}{s_o} + \dfrac{n_2}{s_i} = \dfrac{n_2 - n_1}{R}$ — every symbol signed
  per the table. (2) equal-OPL route: impose $n_1\ell_o + n_2\ell_i$ constant across
  zones, expand to second order in $y$ — same equation, 33's currency. (3) mirror:
  reflection as $n_2 = -n_1$ in the same algebra, or directly:
  $1/s_o + 1/s_i = -2/R \equiv 1/f$, $f = -R/2$ (concave: $R < 0$, $f > 0$).
  (4) thin lens in medium $n_m$: chain two surfaces, drop the thickness:
  $\dfrac{1}{f} = \Big(\dfrac{n}{n_m} - 1\Big)\Big(\dfrac{1}{R_1} - \dfrac{1}{R_2}\Big)$,
  and $1/s_o + 1/s_i = 1/f$. (5) magnification: chief-ray similar triangles →
  $m = -s_i/s_o$; two-point axial object → $m_L = m^2$ (stated; measured in the §4
  scaling test; consumed by 36's depth-of-field discussion).
- **Sign convention (pinned; stated once, here — Hecht's, named):** light travels left
  → right; distances measured from the vertex.

  | Quantity | Positive when | Note |
  |---|---|---|
  | $s_o$ | object left of vertex | real object |
  | $s_i$ (lens/surface) | image right of vertex | real image |
  | $s_i$ (mirror) | image left of mirror | real image on the incoming side |
  | $R$ | centre of curvature right of vertex | concave mirror: $R<0$, $f = -R/2 > 0$ |
  | $f$ | converging | diverging lens: $f < 0$ |
  | $y$, $m$ | above axis / upright | $m = -s_i/s_o$ |
  | $\theta$ | slope $dy/dz$ rising | the 35 state convention, set here |

  The box carries the sentence "this table is the *only* sign convention in the
  course; other texts differ, and mixing is the classic ray-optics failure mode", and
  cross-links `content/en/conventions.md`, which gains a matching ray-optics entry at
  build time (§7) — the same pattern as part-07's handedness box. Modules 35–37 refer
  to the table; they never restate it.
- **Model specification draft:** System — a single refracting spherical surface,
  mirror, or thin lens on one axis; point and extended objects; observables are image
  location, orientation, size. Dynamics — none; algebraic conjugate relations from
  paraxial Snell. Boundary — one element, unbounded aperture unless the shade is set;
  media uniform on each side. Ensemble — deterministic; the conjugate-measurement lab
  adds seeded distance noise. Ignored — thickness (thin-lens limit), aberrations
  (angles kept small by construction), diffraction (image "points" are geometric),
  Fresnel losses. Valid when — $|\theta| \ll 1$, $|y| \ll |R|$, aperture small against
  conjugate distances. Failure modes — sign mixing; paraxial formulas at wide aperture
  (37); trusting a geometric point focus below the `airy_radius` floor.
- **Epistemic classification:** single-surface equation, lensmaker, $m = -s_i/s_o$ —
  `theorem` (given paraxial Snell); the small-angle step — `approximation` (boxed,
  with the $\theta^3$ error order stated — 37's seed); the sign table —
  `definition`; the half-lens measured outcome — `numerical-observation`; "a lens
  images a point to a point" — `model-assumption` flagged with the diffraction floor.
- **Misconceptions:** NEW `half-lens-half-image` — "Covering half a lens produces half
  an image." Falsifying experiment: the exact-trace fan with 50% aperture stop —
  every image point persists at reduced intensity, measured; real counterpart: the
  post-it on the magnifier while imaging a window onto paper — the full window stays,
  dimmer. Root repair: every image point receives rays from the *whole* aperture;
  the lens is not a pixel-wise mapper. Distractor: "the top half of the scene
  disappears from the image". Forward links: the same open-aperture area controls
  brightness (36's f-number) and, inverted, the diffraction PSF width
  (`30-apertures`, `40-psf-otf`); 37 closes the circle when stopping down *improves*
  sharpness — for the aberration reason, not the pixel reason.
- **Glossary terms:** `focal-length` (מרחק מוקד) · `thin-lens` (עדשה דקה) ·
  `real-image` (דמות ממשית) · `virtual-image` (דמות מדומה) · `magnification` (הגדלה) ·
  `conjugate-points` (נקודות מצומדות — translator to confirm) · `sign-convention`
  (מוסכמת סימנים) · `lensmakers-equation` (משוואת יוצר העדשות — translator to
  confirm) · `optical-axis` (ציר אופטי) · `paraxial` (פרקסיאלי — transliteration;
  `he_reject` candidate: צמוד-ציר).
- **Interactive controls and simulations:** imaging bench (element type, $R_1, R_2$,
  $n$, object slider, aperture shade 0–90%, principal rays toggle);
  build-a-diagram scored mode; conjugate scanner (sweep $s_o$, plot $s_i$ and $m$
  live — the hyperbola with its $f$ asymptotes drawn).
- **Virtual lab outline** (`notebooks/en/labs/34-lenses.ipynb`): (1) bench play —
  find the real→virtual flip; (2) build-a-diagram for three canonical cases (outside
  $2f$, between $f$ and $2f$, inside $f$), scored; (3) the post-it experiment
  simulated — aperture fraction sweep, plot image intensity (∝ open area) and image
  extent (flat); (4) conjugate scan → linear fit of $1/s_i$ vs $1/s_o$;
  (5) *measurement culture:* an "unknown" lens — noisy conjugate pairs via
  `measurement.add_noise`, fit → $f$ ± uncertainty; cross-check with a lensmaker
  computation from its stated $R_1, R_2, n$.
- **Real-experiment counterpart:** magnifier + window + paper: measure $s_o$
  (large), $s_i$ with a ruler → $f$; then the post-it half-cover — full image,
  visibly dimmer. Data import: table of $(s_o, s_i)$ pairs into lab cell (5). Cost:
  one magnifying glass.
- **Media assets** (`render_rayoptics.py`): (c) single-surface imaging — wavefronts
  refracting at a spherical cap, rays drawn as their normals, converging to the
  conjugate point (the 33 → 34 bridge visualised); (d) conjugate sweep — object
  sliding in from far away; image marker racing out, blowing up at $f$, flipping to
  virtual; aperture shade dropping late in the shot: image dims, never crops.
  Language-neutral.
- **Quiz bank outline:** `Q-34-1` MC — the post-it outcome (OBJ-34-6, distractor
  `half-lens-half-image`); `Q-34-2` numeric — image location/classification chain
  (OBJ-34-3); `Q-34-3` numeric — lensmaker with immersion (OBJ-34-4); `Q-34-4` MC —
  sign assignment in a mirror layout (OBJ-34-2); `Q-34-5` MC — ray-diagram reading
  (OBJ-34-5); `Q-34-6` numeric — single-surface equation with signed $R$
  (OBJ-34-1); `Q-34-7` free — why every image point needs the whole aperture
  (OBJ-34-6).
- **Problem set outline:** analytical — Newtonian form $x_o x_i = f^2$; two-lens
  contact power addition (35's teaser); mirror-lens equivalence table; minimum
  object–image throw $4f$. Computational — conjugate scan for a *thick* element via
  `trace_exact`, watch the thin-lens fit degrade with thickness (35-advanced teaser).
  Challenge — derive the aplanatic points of a single sphere and verify with
  `trace_exact` that they image without spherical aberration (37 foreshadowed).
- **Runtime budget:** closed forms plus ≤ $10^3$-ray exact fans — trivial in Pyodide.
- **Validation gates:** standard four with `--module 34-lenses`; the conventions.md
  ray-optics sign entry lands with this module (§7).
- **Open questions for the author:** does build-a-diagram scoring live on the page
  (JS) or lab-only (recommendation: lab-only; page shows a static scored example)?
  Mirror content depth — full parallel treatment or lens-first with a mirror
  subsection (recommendation: lens-first; mirrors as the $n_2 = -n_1$ corollary plus
  their own diagram set)?

### 5.3 `35-abcd-matrices` — Ray-transfer matrices: the second operator formalism

- **Identity and scope:** master-plan notebook 10.3. Ray state $(y, \theta)$; elements
  as $2\times2$ matrices; systems as ordered products built interactively; imaging
  condition $B = 0$; system focal length; determinant conservation. **This module is,
  and says out loud that it is, the course's second operator formalism** — Jones
  calculus (`21-jones-calculus`) was the first, and the page opens by quoting that
  module's own framing: states are vectors, elements are operators, cascades are
  ordered products, and order matters. Deferred: Gaussian-beam propagation (the
  matrices are built *for* `43-gaussian-beams` too — the forward seed is explicit —
  but no beam appears here); resonator stability (44, one-line trailer); thick-lens
  principal planes (advanced box, §8).
- **Prerequisites:** `34-lenses` (paraxial relations the matrices encode; the sign
  table); `21-jones-calculus` (the operator grammar, meeting-order products,
  non-commutativity as a designed experiment — this module re-runs that playbook on
  rays); `17-refraction` (paraxial Snell inside the interface matrices).
- **Learning objectives:**
  - `OBJ-35-1` — Represent a meridional paraxial ray as the state (y, theta) and an
    optical element as a 2x2 ray-transfer matrix, and state the structural parallel
    with Jones calculus explicitly.
  - `OBJ-35-2` — Derive the free-space, thin-lens, spherical-interface, flat-interface,
    and mirror matrices from geometry and paraxial Snell.
  - `OBJ-35-3` — Compute a compound system matrix as an ordered product (rightmost
    factor acts first), and exhibit two elements whose two orderings give measurably
    different ray outputs.
  - `OBJ-35-4` — State and apply the imaging condition B = 0; recover the thin-lens
    equation from cascade(free_space(s_o), thin_lens(f), free_space(s_i)) and read
    m = A at the image plane.
  - `OBJ-35-5` — Extract the system focal length f = -1/C, recognize afocal systems by
    C = 0, and use det M = n1/n2 as a conservation check on any cascade.
  - `OBJ-35-6` — Predict how two separated thin lenses combine,
    P = P1 + P2 - d P1 P2, and locate the separation d = f1 + f2 where the pair turns
    afocal.
- **Mathematical background:** has — $2\times 2$ products (21), paraxial relations
  (34); introduced here — phase-space thinking (the ray as a *point* in $(y, \theta)$
  and elements as linear maps of that plane); determinant as the map's area factor.
- **Physical intuition goals:** (1) narrate what each matrix does in words ("free
  space shears — height changes, angle doesn't"; "a lens kinks — angle changes,
  height doesn't"); (2) predict lens-then-gap vs gap-then-lens outputs without
  multiplying; (3) read a system matrix at sight: $B = 0$ image plane, $C = 0$
  telescope, $A$ the magnification when imaging; (4) know that separating two lenses
  *weakens* then *unmakes* their combined power — and where the telescope hides in
  that statement.
- **Section skeleton seeds:**
  - *puzzle:* two identical thin lenses. Held in contact they magnify like a single
    lens of twice the power; pulled apart, the combination weakens, and at one special
    separation it stops focusing entirely — parallel light in, parallel light out.
    Boxed question: what single object describes "this whole train of optics" the way
    one Jones matrix described a train of polarizers — and what does its algebra say
    about order and about that special separation?
  - *predict:* (1) lens then 10 cm of air, vs 10 cm of air then lens — same downstream
    ray? (reinforces `optical-elements-commute`, owned by 21 — now for rays);
    (2) two $f = 10$ cm lenses in contact — combined focal length?; separated by 5 cm?
    (targets NEW `lens-powers-always-add`); (3) what happens at separation
    $d = f_1 + f_2$?; (4) a system's matrix has $B = 0$ — what is physically true of
    the two planes it connects?
  - *explore:* **build-a-system sandbox** — drag elements (lens, gap, flat interface,
    spherical interface, mirror) onto a rail; per-element parameter sliders; live
    system matrix with $A, B, C, D$ readouts and det check; a fan of input rays traced
    through both real space and $(y, \theta)$ phase space side by side; badges light
    up when $B = 0$ (imaging) or $C = 0$ (afocal); drag-to-reorder with an output-ray
    diff view (21's bench playbook, re-run on rays).
  - *derive:* the state and the convention (slope $\theta$, 34's table) → free space
    by similar triangles → thin lens from $1/s_o + 1/s_i = 1/f$ (kink) → flat and
    spherical interfaces from paraxial Snell → mirror in the unfolded convention →
    cascade in meeting order, rightmost first (same contract as
    `polarization.cascade` — the namespaced twins are shown side by side in one
    figure) → non-commutativity computed for the puzzle pair → $B = 0$ imaging and
    $m = A$; thin-lens equation recovered → $f = -1/C$, afocal $C = 0$, two-lens
    power formula → $\det M = n_1/n_2$ and what it conserves (Lagrange invariant
    named in one sentence, derived in advanced).
  - *verify:* every element matrix vs a first-principles two-ray construction
    (heights/angles from 34's algebra); cascade of the two-surface lens →
    `thin_lens(lensmaker(...))` as thickness → 0 (§4 limit test, quoted);
    determinant $n_1/n_2$ through a random ten-element stack
    (`numerical-observation` box); the two orderings of lens+gap measured — output
    states differ by exactly the computed commutator's action.
  - *transfer:* **the same matrices propagate Gaussian beams**: 43 will fold
    $(y, \theta)$ into one complex $q$ and reuse `cascade` unchanged — the forward
    seed is stated with the function names; cavity round trips and stability (44,
    trailer: $|A + D| \le 2$); Jones ↔ ABCD as the course's operator-grammar pair
    (52 adds the third speaker); 36 consumes the formalism wholesale next module.
  - *quiz:* matrix identification; ordering MC; $B = 0$ reading; two-lens power
    numeric; determinant conceptual.
  - *explain:* why the rightmost matrix acts first, told to someone who has seen 21
    (and the one-sentence version for someone who hasn't); what $B = 0$ *means*
    physically, without the word "matrix"; why pulling lenses apart weakens them —
    where does the power "go"?
  - *advanced:* thick elements and principal planes — the system matrix factorised as
    gap · thin-lens · gap, making any paraxial black box an "effective thin lens plus
    two reference planes" (the honest home of thick-lens optics in this course, §8);
    the Lagrange/Smith–Helmholtz invariant $n y \theta$ from the determinant; one
    sentence on symplectic structure (why $2\times2$ with unit-ish det, and why the
    same shape recurs from beams to accelerator optics). Safe to skip.
- **Core derivations:** (1) free space $d$:
  $y_2 = y_1 + d\,\theta_1$, $\theta_2 = \theta_1$ →
  $M = \begin{pmatrix}1 & d\\ 0 & 1\end{pmatrix}$. (2) thin lens: $y_2 = y_1$,
  $\theta_2 = \theta_1 - y_1/f$ → $\begin{pmatrix}1 & 0\\ -1/f & 1\end{pmatrix}$.
  (3) spherical interface: paraxial Snell $n_1(\theta_1 + y/R) = n_2(\theta_2 + y/R)$
  → $\begin{pmatrix}1 & 0\\ -(n_2 - n_1)/(n_2 R) & n_1/n_2\end{pmatrix}$; flat
  interface as $R \to \infty$: $\operatorname{diag}(1, n_1/n_2)$. (4) mirror
  (unfolded): $\begin{pmatrix}1 & 0\\ 2/R & 1\end{pmatrix}$, $f = -R/2$ — signs per
  34's table. (5) imaging: $M = \text{cascade}(\text{free\_space}(s_o),
  \text{thin\_lens}(f), \text{free\_space}(s_i))$ has
  $B = s_o + s_i - s_o s_i/f$; $B = 0 \Leftrightarrow 1/s_o + 1/s_i = 1/f$, and then
  $A = 1 - s_i/f = -s_i/s_o = m$; $D = 1 - s_o/f$ is the angular magnification,
  $AD = \det = 1$ in air — magnify size, demagnify angles, the invariant at work.
  (6) two lenses: $C = -(1/f_1 + 1/f_2 - d/f_1 f_2)$, i.e.
  $P = P_1 + P_2 - d\,P_1 P_2$; $P = 0$ at $d = f_1 + f_2$ — the telescope, one
  module early, discovered as an algebraic accident and named in 36.
  (7) non-commutativity: $\text{free\_space}(d)\,\text{thin\_lens}(f) \ne
  \text{thin\_lens}(f)\,\text{free\_space}(d)$; the difference acts measurably on any
  ray with $\theta_1 \ne 0$ — computed for the puzzle, measured in the sandbox.
- **Model specification draft:** System — meridional paraxial rays as $(y, \theta)$
  states crossing a sequence of ideal elements on one axis; observables are output
  states and derived system constants ($f$, image planes, $m$). Dynamics — linear
  maps applied in meeting order; nothing integrated. Boundary — elements thin (or
  unfolded), apertures ignored except as stated stops; outer media declared.
  Ensemble — deterministic; lab noise via `wavelab.measurement` only. Ignored —
  everything the file-level spec ignores, plus aberrations by construction (matrices
  *are* the paraxial truth; their failure is 37's content). Valid when — paraxial
  limits hold for every element and every ray traced. Failure modes — meeting order
  reversed (reading order); mirror matrix without unfolding; trusting $m = A$ off the
  $B = 0$ plane; power-addition applied to separated lenses.
- **Epistemic classification:** each element matrix and every cascade identity —
  `theorem` (given the paraxial model); the paraxial model itself —
  `approximation` (inherited from 34's box, cited not restated);
  $\det M = n_1/n_2$ — `theorem`, its numerical ten-element check —
  `numerical-observation`; "one matrix fully describes a paraxial system" —
  `model-assumption` (breaks precisely where 37 begins); "the same algebra will
  propagate Gaussian beams" — stated as a forward `theorem` pointer owned by 43.
- **Misconceptions:**
  - NEW `lens-powers-always-add` — "The powers of stacked lenses add, regardless of
    separation." Falsifying experiment: the sandbox separation sweep — measured
    system power falls from $P_1 + P_2$ along $P_1 + P_2 - d P_1 P_2$, hitting zero
    at $d = f_1 + f_2$ (parallel in, parallel out, on screen); real counterpart: two
    magnifiers on a ruler focusing sunlight — the combined focal point recedes as
    they separate. Distractor: "two $f = 10$ cm lenses 5 cm apart ≡ one $f = 5$ cm
    lens".
  - Reinforces `optical-elements-commute` (registry, owned by `21-jones-calculus`):
    the ordering experiment re-run on rays, plus a quiz distractor — no re-point, the
    ray case cites 21's entry.
- **Glossary terms:** `ray-transfer-matrix` (מטריצת מעבר קרן — translator to
  confirm) · `abcd-matrix` (מטריצת ABCD) · `optical-power` (כוח שבירה) · `diopter`
  (דיופטר) · `afocal` (אפוקלי — transliteration; `he_reject` candidate: חסר-מוקד) ·
  `principal-plane` (מישור ראשי) · `phase-space` (מרחב פאזה — dedupe if an earlier
  part deposited it).
- **Interactive controls and simulations:** build-a-system sandbox (rail, element
  palette, parameter sliders, live $ABCD$ + det readout, badges, reorder-diff); the
  phase-space twin view (input fan as a segment in $(y, \theta)$, sheared/kinked by
  each element — watching free space shear and lenses rotate the fan is the module's
  best picture); "matrix inspector" showing the running product term by term (21's
  inspector, reskinned).
- **Virtual lab outline** (`notebooks/en/labs/35-abcd-matrices.ipynb`): (1) element
  bestiary — verify each matrix by tracing two independent rays and solving for
  $A, B, C, D$; (2) the ordering experiment — lens+gap both ways, record output
  states, compare with the computed products (`numerical-observation`); (3) imaging
  hunt — slide an image plane until $B = 0$, read $m = A$, check against 34's bench;
  (4) separation sweep — measure $P(d)$ for two lenses, fit the line in $d$, extract
  $P_1 P_2$ from the slope, find the afocal zero; (5) determinant audit — build five
  random stacks with mixed media, verify $\det = n_{\text{in}}/n_{\text{out}}$;
  (6) *measurement culture:* a sealed "mystery box" system (hidden element list) —
  determine its $ABCD$ from four noisy ray measurements
  (`measurement.add_noise`), report $f = -1/C$ ± uncertainty, and state whether it
  images or is afocal.
- **Real-experiment counterpart:** two cheap lenses on a printed ruler: combined
  focal length vs separation by focusing a distant lamp — a hand-measured $P(d)$
  line; at $d \approx f_1 + f_2$, no focus exists and the pair becomes a (Keplerian)
  peephole telescope — 36's opening, discovered on the living-room floor. Data
  import: $(d, f_{\text{combo}})$ CSV into lab cell (4).
- **Media assets** (`render_rayoptics.py`): (e) phase-space twin — a ray fan crossing
  lens · gap · lens, real space above, $(y, \theta)$ plane below; shears and kinks
  visibly compose into the system map; (f) ordering swap — the same input fan through
  lens-then-gap and gap-then-lens, outputs diverging side by side.
  Language-neutral.
- **Quiz bank outline:** `Q-35-1` MC — identify the element from its matrix
  (OBJ-35-2); `Q-35-2` MC — do lens and gap commute (OBJ-35-3, distractor from
  `optical-elements-commute`); `Q-35-3` numeric — two-lens power at separation
  (OBJ-35-6, distractor `lens-powers-always-add`); `Q-35-4` numeric — cascade a
  three-element system, find the image plane (OBJ-35-4); `Q-35-5` MC — what $B = 0$
  and $C = 0$ each mean (OBJ-35-4, OBJ-35-5); `Q-35-6` numeric — det check to catch
  a corrupted cascade (OBJ-35-5); `Q-35-7` free — the Jones ↔ ABCD parallel in ≤ 4
  sentences (OBJ-35-1).
- **Problem set outline:** analytical — derive the mirror matrix and the equivalence
  "cavity round trip = periodic lens guide"; principal planes of a thick lens from
  its matrix; prove $\det = n_1/n_2$ for the general cascade by induction.
  Computational — matrix-fit an "unknown" black box from ray data (conditioning of
  the four-ray solve); reproduce 34's conjugate hyperbola entirely from `cascade`.
  Challenge — the $|A + D| \le 2$ stability criterion for a two-mirror cavity,
  derived from eigenvalues and verified by iterating `cascade` round trips (44's
  trailer, done honestly).
- **Runtime budget:** $2\times2$ real products, fans ≤ $10^3$ rays — negligible;
  phase-space animation ≤ 60 frames, pre-rendered.
- **Validation gates:** standard four with `--module 35-abcd-matrices`; the
  `rayoptics.py` matrix-core tests (§4 limits/conservation) land with this module —
  36, 37, and part-12 cite them; **the six dictated names freeze on this module's
  merge** (§7).
- **Open questions for the author:** does the phase-space view appear on the page or
  lab-only (recommendation: one static page figure, live in lab)? Mirror unfolding —
  full subsection or advanced note (recommendation: full subsection; 44 depends on
  the convention being solid)? Show the Jones/ABCD twin-cascade figure in core
  (recommendation: yes — it is the part's thesis in one image)?

### 5.4 `36-instruments` — Optical instruments by design

- **Identity and scope:** master-plan notebook 10.4 (order refined, §8): camera,
  magnifier, microscope, telescope — each an ABCD design exercise plus a built ray
  diagram, in single-lens → two-lens order. **Empty magnification is the honesty
  centerpiece**: every design is cross-checked against the Part IX diffraction limit
  (`diffraction.airy_radius`, `diffraction.rayleigh_criterion` — dictated names), and
  the master plan's §26.4 open investigation (the 10-mm telescope) lands here as the
  lab's finale. Deferred: aberration budgets (37), eye physiology beyond the near
  point (out of course), photometry beyond $1/N^2$.
- **Prerequisites:** `34-lenses` (conjugates, virtual images, $m$); `35-abcd-matrices`
  (`two_lens`, afocal $C = 0$, $m = A$); `30-apertures` (`airy_radius`,
  `rayleigh_criterion`); `27-coherence` is *not* needed — incoherent point sources
  suffice throughout.
- **Learning objectives:**
  - `OBJ-36-1` — Model a camera as a single-lens imager: relate f-number N = f/D to
    image brightness (proportional to 1/N^2) and, qualitatively, to depth of field.
  - `OBJ-36-2` — Compute the angular magnification of a magnifier,
    M = 25 cm / f for the image at infinity and M = 1 + 25 cm / f at the near point,
    and explain why "angular" is the honest currency for instruments feeding an eye.
  - `OBJ-36-3` — Design a compound microscope as an ABCD cascade and verify
    M = -(L / f_obj)(25 cm / f_eye) with tube length L.
  - `OBJ-36-4` — Design an afocal telescope (C = 0 at d = f_obj + f_eye), verify the
    angular magnification M = -f_obj / f_eye, and state the aperture's double role:
    light bucket and resolution limit.
  - `OBJ-36-5` — Compute an instrument's diffraction-limited angular resolution from
    rayleigh_criterion, derive the empty-magnification threshold (magnification beyond
    which no new detail appears), and apply it to a given design.
  - `OBJ-36-6` — Carry out the 10-mm-telescope investigation: determine how resolving
    capability changes with wavelength, verify analytically and computationally, and
    explain the physics.
- **Mathematical background:** has — the full 34/35 toolkit; introduced here —
  angular magnification as a ratio of *angles at the eye* (a new comparison standard:
  the 25 cm near point as reference); order-of-magnitude design reasoning.
- **Physical intuition goals:** (1) say which instrument is "a lens making a real
  image", "a lens making a virtual image", and "two of those in series" — and never
  confuse magnifier with microscope again; (2) rank two telescopes by resolving
  power *from aperture alone*; (3) predict that doubling eyepiece power doubles
  image scale but, past the useful threshold, reveals nothing; (4) explain why
  astronomers buy aperture, not magnification.
- **Section skeleton seeds:**
  - *puzzle:* a market stall sells two telescopes: "500×!!" with a 50 mm aperture,
    and a plain 150 mm instrument advertising only "75×". Boxed question: which shows
    more detail on the Moon — and what, physically, does the extra magnification of
    the first one magnify? Secondary hook: your phone's digital zoom — pinch-zooming
    *after* the photo never adds detail; why?
  - *predict:* (1) the stall question (targets NEW `magnification-reveals-detail`);
    (2) halve a camera's f-number — what happens to exposure time?; (3) a magnifier
    of $f = 5$ cm — how many times "bigger" does it show a stamp, and bigger than
    *what*?; (4) for the 10-mm telescope, does red or blue light resolve finer
    detail?
  - *explore:* instrument workbench — presets (camera / magnifier / microscope /
    telescope) built from `two_lens` and stops on the 35 sandbox rail; per-preset
    live readouts ($N$, $M_{\text{ang}}$, $C$, exit rays); a **detail meter**: a
    simulated double star / line-pair target rendered through the design with the
    diffraction blur from `airy_radius` overlaid, so cranking magnification visibly
    enlarges blur, not detail; wavelength slider for the resolution experiments.
  - *derive:* camera: single-lens imaging + stop; irradiance ∝ aperture area /
    image area → $1/N^2$; depth of field qualitatively via 34's $m_L = m^2$
    (defocus grows twice as fast in image space as in angle) → magnifier: virtual
    image, angular gain vs the 25 cm reference; both formulas → microscope:
    objective forms a real magnified intermediate ($m_{\text{obj}} = -L/f_{obj}$),
    eyepiece magnifies it as a magnifier; cascade verified $B = 0$ then afocal
    viewing → telescope: afocal cascade at $d = f_{obj} + f_{eye}$ (35's algebraic
    accident, now named), $M = -f_{obj}/f_{eye} = D$ of the system matrix; aperture
    as light bucket (flux ∝ $D^2$) → the diffraction ceiling:
    $\theta_{\min} = $ `rayleigh_criterion`$(\lambda, D)$; useful magnification
    $M_{\max} \sim \theta_{\text{eye}}/\theta_{\min}$ (with
    $\theta_{\text{eye}} \approx 1'$), the empty-magnification threshold — beyond
    it, the eyepiece magnifies the Airy blob.
  - *verify:* microscope and telescope cascade matrices hit the closed-form $M$
    (limit checks quoted from §4); afocal check $C = 0$ at the designed separation;
    the detail meter measured: fitted resolvable line-pair spacing vs magnification
    flattens exactly at the computed $M_{\max}$ (`numerical-observation` box —
    "magnification beyond ~1–2× per millimetre of aperture is empty");
    $\theta_{\min} \propto \lambda/D$ fitted exponents (1.00, −1.00).
  - *transfer:* the camera stop is 34's aperture shade wearing engineering units —
    and 37 will *want* stopping down for sharpness; `40-psf-otf` upgrades the detail
    meter to the full PSF/MTF story; `41-imaging-coherence` revisits resolution with
    coherence honesty; capstone §35.1 builds the computational telescope from this
    module's design plus 37's aberrations.
  - *quiz:* f-number numerics; magnifier/microscope/telescope $M$ numerics; the
    stall MC; empty-magnification threshold numeric; light-bucket conceptual.
  - *explain:* to the market-stall customer — what "500×" does and does not buy;
    why a microscope needs *two* stages when a magnifier is one lens; why "digital
    zoom" is empty magnification by construction; what a big telescope mirror is
    *for*, in one sentence each for brightness and resolution.
  - *advanced:* exit pupil and eye relief from the system matrix (where the eye
    goes, and why $M_{\max}$ is also "exit pupil ≈ eye pupil"); Galilean vs
    Keplerian telescopes (negative eyepiece, upright image, no intermediate focus).
    Safe to skip.
- **Core derivations:** (1) camera exposure: image irradiance
  $\propto (D/f)^2 = 1/N^2$ for extended scenes — one stop = factor 2 in $N^2$.
  (2) magnifier: unaided angle $y/25\,\mathrm{cm}$; aided (image at $\infty$)
  $y/f$; ratio $M = 25\,\mathrm{cm}/f$; near-point variant $1 + 25\,\mathrm{cm}/f$.
  (3) microscope: $M = m_{\text{obj}} \times M_{\text{eye}}
  = -(L/f_{obj})(25\,\mathrm{cm}/f_{eye})$; cascade check via
  `two_lens(f_obj, f_eye, f_obj + L + f_eye)` layout. (4) telescope:
  `two_lens(f_obj, f_eye, f_obj + f_eye)` gives
  $M_{\text{sys}} = \begin{pmatrix}-f_{eye}/f_{obj} & f_{obj}+f_{eye}\\
  0 & -f_{obj}/f_{eye}\end{pmatrix}$: $C = 0$, angular magnification
  $D = -f_{obj}/f_{eye}$, $AD = 1$ (35's invariant: wider beam → shallower angles —
  why the light bucket also *steadies* the image). (5) resolution:
  $\theta_{\min} = 1.22\,\lambda/D$ via `rayleigh_criterion` (result *cited* from
  30, with its Airy provenance — never re-derived here);
  $M_{\max} \approx \theta_{\text{eye}}\,D/(1.22\,\lambda)$ — for
  $\lambda = 550$ nm, roughly $1.5\times$ per millimetre of aperture; the 50 mm
  "500×" stall telescope is ~7× over budget. (6) the 10-mm telescope:
  $\theta_{\min}(550\,\text{nm}) \approx 6.7\times10^{-5}$ rad ≈ 14″; blue improves
  it, red worsens it, linearly in $\lambda$.
- **Model specification draft:** System — two-lens (or one-lens) paraxial
  instruments with a circular aperture stop, feeding an ideal eye with a 25 cm near
  point and ~1′ acuity; observables are angular magnification, image brightness
  scaling, and resolvable detail. Dynamics — 35's matrix maps; diffraction enters
  only as the imported Airy blur at the image. Boundary — stops are hard circles;
  eye at the designed exit position. Ensemble — deterministic; detail-meter
  measurements add seeded detector noise. Ignored — aberrations (37), eye
  accommodation range beyond the near point, sky background, atmospheric seeing
  (named in the lab as the real-world ceiling above 10 mm... honest one-liner).
  Valid when — paraxial designs, stop diameters ≫ λ, incoherent targets. Failure
  modes — magnification quoted without aperture context; resolution claims below
  the Airy floor; comparing instrument $M$ to transverse $m$ (different
  currencies).
- **Epistemic classification:** all $M$ formulas — `theorem` (given the paraxial
  model); $\theta_{\text{eye}} \approx 1'$ — `empirical-law`; the
  $\theta_{\min} = 1.22\lambda/D$ input — cited `theorem` owned by 30; the measured
  flattening of the detail curve — `numerical-observation`; "the eye tolerates the
  near-point convention" — `model-assumption` (stated once); "how far can
  computational post-processing push below the classical limit?" —
  `open-question` pointer to `53-computational-imaging`.
- **Misconceptions:** NEW `magnification-reveals-detail` — "More magnification always
  shows more detail." Falsifying experiment: the detail meter — a double star at the
  10-mm telescope's limit, eyepiece power swept ×2, ×4, ×8 past $M_{\max}$: the blobs
  grow, their separation-to-blur ratio never improves; measured resolvable spacing
  flattens at the diffraction value from `rayleigh_criterion`. Real counterpart:
  pinch-zooming a phone photo of a distant sign. Distractor: "a 500× eyepiece on a
  50 mm telescope resolves 500×-finer detail than the eye".
- **Glossary terms:** `f-number` (מספר-f) · `depth-of-field` (עומק שדה) ·
  `angular-magnification` (הגדלה זוויתית) · `near-point` (נקודה קרובה) ·
  `objective-lens` (עדשה עצמית — translator to decide vs אובייקטיב) · `eyepiece`
  (עינית) · `empty-magnification` (הגדלה ריקה — translator to confirm) ·
  `light-gathering-power` (כושר איסוף אור) · `exit-pupil` (אישון יציאה) ·
  `numerical-aperture` (מפתח מספרי — deposited here; modules 39 and 47 cite and
  extend the same key).
- **Interactive controls and simulations:** instrument workbench (presets, stops,
  live badges and readouts); detail meter (target type: double star / line pairs;
  magnification and λ sliders; Airy-blur overlay toggle); exposure sandbox
  ($N$ vs required exposure time at fixed noise).
- **Virtual lab outline** (`notebooks/en/labs/36-instruments.ipynb`): (1) build all
  four instruments from `two_lens` + stops; verify $M$ and badges against closed
  forms; (2) camera: measure image brightness vs $N$ across stops, fit the $-2$
  exponent; (3) empty magnification: detail meter sweep, extract the flattening
  point, compare to $M_{\max}$; (4) **open investigation (master plan §26.4), the
  lab's finale:** the 10-mm telescope — how does resolving capability change with
  wavelength? Student designs the measurement (simulated double stars across
  400–700 nm via the Airy blur), fits $\theta_{\min}(\lambda)$, verifies
  $1.22\lambda/D$ analytically, and writes the explanation; deliverable is a short
  lab report, not a filled blank; (5) *measurement culture:* $\theta_{\min}$ at
  550 nm reported ± uncertainty from noisy detail-meter data across seeds.
- **Real-experiment counterpart:** the two-lens Keplerian telescope from 35's
  ruler experiment, now aimed at a distant brick wall — count courses per view
  width, measure $M$ against the naked eye, compare to $-f_1/f_2$; phone digital
  zoom on a distant printed test pattern (empty magnification, physically); a
  10 mm aperture mask over a camera lens photographing a line-pair target —
  resolution with and without the mask. CSV/photo import into lab cells (3)–(5).
- **Media assets** (`render_rayoptics.py`): (g) telescope afocal geometry —
  parallel bundle in at angle $\theta$, parallel out at $M\theta$, beam compressed
  $D \to D/|M|$ (the $AD = 1$ trade drawn); (h) empty magnification — zooming into
  an Airy-blurred double star: blobs swell, never separate; beside it the larger
  aperture resolving them at the *same* magnification. Language-neutral.
- **Quiz bank outline:** `Q-36-1` MC — the market-stall telescopes (OBJ-36-4,
  OBJ-36-5, distractor `magnification-reveals-detail`); `Q-36-2` numeric — exposure
  change across f-stops (OBJ-36-1); `Q-36-3` numeric — magnifier $M$ both
  conventions (OBJ-36-2); `Q-36-4` numeric — microscope design to a target $M$
  (OBJ-36-3); `Q-36-5` numeric — telescope $M$ and beam compression (OBJ-36-4);
  `Q-36-6` numeric — $M_{\max}$ and $\theta_{\min}(\lambda)$ for a given aperture
  (OBJ-36-5, OBJ-36-6); `Q-36-7` free — aperture's two jobs, one sentence each
  (OBJ-36-4).
- **Problem set outline:** analytical — Galilean telescope $M$ and length; exit
  pupil position/size from the system matrix; near-point vs infinity magnifier
  derivations. Computational — design a microscope to resolve 2 μm at the eye
  given $\theta_{\text{eye}}$, then check the objective's NA honestly against
  `rayleigh_criterion` (discover that the *objective aperture*, not the eyepiece,
  is the budget). Challenge — the §26.4 investigation extended: add atmospheric
  seeing as a fixed 1″ blur and find the aperture beyond which it, not
  diffraction, rules (why 10 mm is safe and 1 m is not).
- **Runtime budget:** matrix algebra trivial; detail-meter renders ≤ $512^2$ with
  precomputed Airy kernels — ≤ 1 s in Pyodide per update.
- **Validation gates:** standard four with `--module 36-instruments`.
- **Open questions for the author:** does the eye model (25 cm, 1′) get its own
  boxed mini-spec (recommendation: yes, `model-assumption` box — it is the
  module's hidden apparatus)? Detail meter on the page (static pair of frames) vs
  lab-only live (recommendation: static pair on page — it *is* the misconception
  falsifier, worth front-loading)?

### 5.5 `37-aberrations` — Aberrations: where the paraxial model breaks

- **Identity and scope:** master-plan notebook 10.5. The truth the paraxial model
  hid, measured: exact ray tracing (full Snell per surface via
  `interfaces.snell_angle`) against the paraxial prediction; spherical aberration
  (marginal vs paraxial focus, the caustic); coma and astigmatism from off-axis
  fans; chromatic aberration from $n(\lambda)$ (`em.sellmeier`) with a
  student-designed crown+flint achromatic doublet; stopping down as the
  brightness-for-sharpness trade (closing 34's aperture circle); spot-diagram
  metrics with noise as measurement culture. Zernike polynomials and adaptive
  optics appear in a research-connection box (JWST), machinery deferred to
  `40-psf-otf`. Deferred: full Seidel theory (named, not developed); skew-ray coma
  shapes (§8).
- **Prerequisites:** `34-lenses` (paraxial predictions, the `approximation` box
  whose bill now comes due); `35-abcd-matrices` (`trace_paraxial` as the reference
  ruler); `17-refraction` (`snell_angle`); `16-light-in-matter` + part-05's
  `em.sellmeier` / `em.refractive_index` ($n(\lambda)$, glass data);
  `13-dispersion` (why $n$ varies at all — cited in one line).
- **Learning objectives:**
  - `OBJ-37-1` — Explain aberrations as the measured discrepancy between exact ray
    tracing and the paraxial model, and attribute them to the next term of
    sin(theta) = theta - theta^3/6 + ...
  - `OBJ-37-2` — Measure spherical aberration for a given lens: marginal vs
    paraxial focus, longitudinal shift proportional to h^2 and transverse blur to
    h^3, and identify the caustic.
  - `OBJ-37-3` — Identify coma and astigmatism in off-axis exact-trace fans and
    spot diagrams, and state which field angle and aperture each grows with.
  - `OBJ-37-4` — Compute chromatic focal shift from n(lambda) via the Sellmeier
    relation, define the Abbe number V = (n_d - 1)/(n_F - n_C), and design an
    achromatic crown+flint contact doublet from P1/V1 + P2/V2 = 0.
  - `OBJ-37-5` — Predict the effect of stopping down on each aberration and on
    image brightness, and choose an aperture that meets a stated blur budget.
  - `OBJ-37-6` — Report an RMS spot radius with uncertainty from noisy traced data
    and use it to compare two designs quantitatively.
- **Mathematical background:** has — exact Snell, matrices, series expansions;
  introduced here — the aberration bookkeeping mindset (blur budgets, metrics on
  ray bundles: RMS spot radius); reading a spot diagram / ray-fan plot.
- **Physical intuition goals:** (1) predict which way spherical aberration pushes
  the marginal focus for a plano-convex lens — and which orientation of that lens
  is better; (2) look at a spot diagram and name the aberration (circular halo =
  spherical, comet = coma, cross/line pair = astigmatism, colour fringe =
  chromatic); (3) know that stopping down kills $h^3$ blur fast but costs $h^2$
  light — and where the diffraction floor stops the game; (4) explain why a
  *perfectly manufactured* spherical lens still cannot focus perfectly.
- **Section skeleton seeds:**
  - *puzzle:* the coffee-cup caustic — sunlight off the cup's inner wall draws a
    bright cusped curve, not a point. The cup is a perfectly good circular mirror;
    34 promised a focus. Boxed question: the paraxial model was *derived*, not
    guessed — so what exactly did we throw away, and how big is the bill?
  - *predict:* (1) a flawlessly made spherical lens, monochromatic light, tiny
    source — perfect point image? (targets NEW `aberrations-need-imperfection`);
    (2) rays through the lens edge vs centre — same focal point, edge focuses
    shorter, or longer?; (3) does stopping down help chromatic aberration the way
    it helps spherical?; (4) blue and red through one lens — which focuses
    closer?
  - *explore:* aberration bench — a lens (or 34's bench elements) traced two ways
    at once: paraxial rays ghosted, exact rays solid; aperture-height slider
    growing the fan; field-angle slider tilting the bundle off axis; screen
    slider sweeping through focus with a live spot diagram and RMS readout; a λ
    slider (with `em.sellmeier` glass presets) splitting the trace into colours;
    a stop slider re-running 34's shade with the sharpness meter now *improving*.
  - *derive:* the bill: $\sin\theta = \theta - \theta^3/6 + \dots$ — paraxial kept
    the first term; the $\theta^3$ term is "third-order aberration", Seidel's five
    named in one table (spherical, coma, astigmatism, field curvature,
    distortion; the course measures the first three plus chromatic) → spherical
    aberration: exact trace of an on-axis fan; axis crossings march with $h^2$
    (longitudinal), blur with $h^3$ (transverse); marginal vs paraxial focus,
    best-focus circle of least confusion; the caustic as the envelope of exact
    rays (33's advanced warning made visible) → coma and astigmatism: off-axis
    fans; tangential vs sagittal focus split (astigmatism) and the asymmetric
    flare (coma), delivered as spot diagrams — the professional's tool, stated as
    such → chromatic: lensmaker with $n(\lambda)$; $f(\lambda)$ falls toward
    blue; longitudinal chromatic shift; Abbe number; the doublet condition
    $P_1/V_1 + P_2/V_2 = 0$ solved for crown+flint, student picks the powers →
    stopping down: each blur's aperture scaling vs the $1/N^2$ light bill and the
    `airy_radius` floor — the three-way trade that *is* lens design.
  - *verify:* transverse aberration fitted exponent 3.0, longitudinal 2.0 (§4
    convergence tests quoted; `numerical-observation` box); `trace_exact` →
    `trace_paraxial` as the fan narrows (the part's opening promise, closed
    numerically); doublet: measured focal shift across 486–656 nm collapses by
    >10× vs the singlet (`numerical-observation`); plano-convex orientation
    experiment — curved side toward the distant object roughly halves the RMS
    spot.
  - *transfer:* unequal OPLs are wavefront error — `40-psf-otf` converts exactly
    this into PSF/OTF (Zernike named as its language); stopping down closes 34's
    aperture story — brightness (34/36) vs sharpness (37) vs diffraction (30):
    three modules, one slider; `43-gaussian-beams` inherits clean paraxial
    matrices *because* laser beams live near-axis; capstone §35.1 budgets
    aberrations against the atmosphere.
  - *quiz:* name-the-aberration from spot diagrams; $h$-scaling numerics;
    chromatic shift numeric; doublet design numeric; stop-down conceptual.
  - *explain:* to a lens buyer — why "aspheric" costs more and what it buys; why
    the caustic is not a manufacturing defect; why stopping down sharpens *and*
    darkens, and what sets the sweet spot; why achromats use two glasses instead
    of "better" glass.
  - *advanced (research-connection box):* Zernike polynomials as the orthogonal
    alphabet of wavefront error (defocus, astigmatism, coma, spherical as its
    first letters — machinery in `40-psf-otf`); adaptive optics — measure the
    error, bend a mirror against it, kilohertz-fast; JWST's segmented primary
    phased to tens of nanometres — aberration correction as *the* enabling
    technology of modern astronomy. Safe to skip; nothing later depends on it.
- **Core derivations:** (1) the error term: exact vs paraxial Snell differ at
  $O(\theta^3)$; for a single surface the transverse ray aberration at the
  paraxial focus $\propto h^3$, longitudinal $\propto h^2$ — derived by expanding
  the exact trace one order past 34. (2) marginal vs paraxial focus and the circle
  of least confusion located from the traced caustic envelope. (3) coma /
  astigmatism operationally: tangential fan at field angle $\phi$; focus split
  $\Delta z_{ta}$ grows as $\phi^2$, comatic asymmetry as $h^2\phi$ — measured
  scalings, with the Seidel provenance named but not derived. (4) chromatic:
  $\dfrac{1}{f(\lambda)} = \big(n(\lambda) - 1\big)\Big(\dfrac{1}{R_1} -
  \dfrac{1}{R_2}\Big)$ with $n(\lambda)$ = `em.sellmeier`; fractional focal spread
  F-to-C $\approx 1/V$; doublet: $P = P_1 + P_2$ with
  $P_1/V_1 + P_2/V_2 = 0$ → crown positive, flint negative, net positive power
  with $df/d\lambda \approx 0$ at the design pair (worked for BK7 + F2-class
  values via `abbe_number`). (5) the trade: blur$_{\text{sph}} \propto (D/2)^3$,
  flux $\propto D^2$, Airy floor $\propto 1/D$ — the optimal stop exists and the
  student finds it numerically.
- **Model specification draft:** System — a small stack of spherical surfaces
  (singlet, then doublet) traced two ways: paraxial matrices and exact meridional
  rays; observables are focus positions, spot diagrams, RMS radii, $f(\lambda)$.
  Dynamics — sequential exact refraction via `interfaces.snell_angle`; no waves.
  Boundary — surfaces spherical and perfectly made (the point!); hard circular
  stop; meridional plane only. Ensemble — deterministic traces; measurement cells
  add seeded ray-height and detector noise. Ignored — diffraction at the spot
  scale (quoted as the floor, not computed here); skew rays (sagittal behaviour
  approximated, labelled); surface errors and tolerances; ghost images. Valid
  when — geometric blur ≫ `airy_radius` (else Part XI's regime); glasses inside
  their Sellmeier windows. Failure modes — reading spot structure below the
  diffraction floor as real; comparing spot metrics across different focal
  planes; the meridional model quoted for full coma shapes.
- **Epistemic classification:** the $h^2$/$h^3$ scalings and the doublet
  condition — `theorem` (given exact ray model); measured exponents and the
  doublet's >10× collapse — `numerical-observation`; Sellmeier coefficients —
  `empirical-law` (part-05's deposit, cited); "spherical surfaces are what you
  can polish" — `empirical-law` (one manufacturing sentence); "aberration-free
  spherical imaging is impossible in general" — `theorem` stated with the
  aplanatic-point exception (34's problem set) footnoted; "how well can
  computation undo a *known* aberration?" — `open-question` pointer to
  `53-computational-imaging`.
- **Misconceptions:** NEW `aberrations-need-imperfection` — "Aberrations come from
  manufacturing flaws; a perfect spherical lens would image perfectly."
  Falsifying experiment: `trace_exact` through a *mathematically exact* sphere —
  the marginal-focus march and the caustic appear anyway, and the measured
  $h^3$ blur matches the third-order prediction; the sphere is the wrong shape,
  not a bad copy of the right one. Real counterpart: the coffee-cup caustic —
  no cup is at fault. Distractor: "with monochromatic light and a flawless
  spherical lens, the image of a point is a point".
- **Glossary terms:** `aberration` (אברציה — translator to decide vs עיוות) ·
  `spherical-aberration` (אברציה כדורית) · `coma` (קומה) · `astigmatism`
  (אסטיגמטיזם) · `chromatic-aberration` (אברציה כרומטית) · `achromatic-doublet`
  (צמד אכרומטי — translator to confirm) · `caustic` (קאוסטיקה) · `spot-diagram`
  (דיאגרמת כתם — translator to confirm) · `abbe-number` (מספר אבה) ·
  `marginal-ray` (קרן שולית) · `adaptive-optics` (אופטיקה אדפטיבית).
- **Interactive controls and simulations:** aberration bench (aperture height,
  field angle, screen position, λ with glass presets, stop slider; ghosted
  paraxial vs solid exact rays; live spot diagram + RMS readout); doublet
  designer (pick crown/flint from a small glass table, slide the power split,
  watch $f(\lambda)$ flatten); caustic explorer (screen sweep through the cusp).
- **Virtual lab outline** (`notebooks/en/labs/37-aberrations.ipynb`):
  (1) exact-vs-paraxial warm-up — shrink the fan, watch the models converge
  (the part's thesis, measured); (2) spherical aberration — axis-crossing vs $h$,
  fit the $h^2$ law; locate marginal, paraxial, and best focus; render the
  caustic; (3) orientation experiment — plano-convex both ways, RMS spot
  comparison; (4) off-axis — tangential fans at three field angles, spot
  diagrams, name the aberrations; (5) chromatic — $f(\lambda)$ for a BK7
  singlet via `chromatic_focus_shift`; then **design the achromat**: choose
  powers from $P_1/V_1 + P_2/V_2 = 0$, re-trace, quantify the collapse;
  (6) stop-down study — RMS spot and flux vs stop diameter with the
  `airy_radius` floor overlaid; find the sweet spot; (7) *measurement culture:*
  RMS spot radius of the final doublet at best focus, ± uncertainty across
  seeded noisy bundles (`validation.seed_study`), compared against the singlet
  as a defensible "×N better" claim.
- **Real-experiment counterpart:** the coffee-cup (or wedding-ring) caustic on
  a sunny table — photograph and compare with the traced envelope's cusp shape;
  chromatic fringing — photograph a black-white edge through a cheap magnifier
  at full aperture (colour fringe) and through a small paper stop (fringe
  shrinks); photo import into lab cells (2)/(5). Cost: sunlight and a cup.
- **Media assets** (`render_rayoptics.py`): (i) fan growing at fixed lens —
  exact rays peeling away from the ghosted paraxial focus, caustic condensing,
  screen sweep showing the circle of least confusion; (j) white-light fan —
  colour-split foci strung along the axis; the doublet snapping them together
  as the second element fades in. Language-neutral.
- **Quiz bank outline:** `Q-37-1` MC — perfect sphere, perfect image?
  (OBJ-37-1, distractor `aberrations-need-imperfection`); `Q-37-2` MC — name
  the aberration from four spot diagrams (OBJ-37-3); `Q-37-3` numeric —
  longitudinal SA scaling from two measured heights (OBJ-37-2); `Q-37-4`
  numeric — chromatic focal spread from Sellmeier values (OBJ-37-4); `Q-37-5`
  numeric — doublet power split for a target $f$ (OBJ-37-4); `Q-37-6` MC —
  which aberrations does stopping down help, and what does it cost
  (OBJ-37-5); `Q-37-7` free — explain to a photographer why f/8 is sharper
  than f/2 *and* than f/22 on a cheap lens (OBJ-37-5, `half-lens-half-image`
  circle closed).
- **Problem set outline:** analytical — third-order transverse aberration of a
  single surface (the honest expansion); doublet condition from
  $d(P_1 + P_2)/d\lambda = 0$; best-focus location minimising RMS blur for an
  $h^3$ fan. Computational — Coddington-style lens bending: sweep the shape
  factor of a singlet at fixed power, find minimum-SA bending; tolerance the
  doublet (how wrong can the flint power be for a 2× budget?). Challenge —
  build `spot_diagram` output into a merit function and let
  `scipy.optimize` design the doublet — then compare with the analytic
  $P/V$ answer (a first taste of real lens design).
- **Runtime budget:** exact traces ≤ $10^4$ rays × ≤ 4 surfaces — well under a
  second in Pyodide; caustic renders ≤ $10^3$ rays; optimisation challenge ≤
  a few hundred merit evaluations.
- **Validation gates:** standard four with `--module 37-aberrations`; the
  exact-trace §4 tests (convergence/seeds) land with this module.
- **Open questions for the author:** does field curvature/distortion get one
  illustrated paragraph or a bare table row (recommendation: one paragraph,
  no lab); JWST box with or without the segmented-phasing figure
  (recommendation: with — it is the part's best "why this matters" image);
  glass table size in the doublet designer (recommendation: 4 glasses — two
  crowns, two flints — enough for real choice, small enough to reason about).

## 6. Part-level assessment and capstone hooks

- **Capstone §35.1 (Computational Telescope)** is this part's direct heir: 36
  supplies the design (aperture, focal lengths, magnification budget, empty-
  magnification ceiling), 37 the aberration budget and spot metrics, part-09's
  `diffraction` names the floor. The capstone adds detectors and image
  processing on top — the rayoptics layer is finished here.
- **Capstone §35.2 (Virtual Optical Bench)** gains its geometry engine: the 35
  sandbox *is* the bench's ray layer, as part-07's §28 bench is its polarization
  layer — the twin `cascade`s meet in one instrument, and the capstone's UI
  should expose them as siblings.
- **Capstone §35.5 (Fourier-Optics Image Processor)** consumes 35's focal-plane
  bookkeeping (where the transform plane *is*) en route to part-11.
- Cross-module synthesis problems (filed with 37's problem set): (a) **design a
  camera** end-to-end — focal length from conjugates (34), two-element layout
  (35), f-number for a stated exposure (36), then measure its spherical +
  chromatic blur and stop it down to a stated budget (37) — one problem
  touching every module; (b) Fermat ↔ ABCD consistency: show the equal-OPL
  condition and $B = 0$ select the same image plane for a thin lens (33 + 35);
  (c) "the honest spec sheet": given a rival catalogue's telescope listing,
  identify every claim that violates the diffraction limit or the aberration
  scalings (36 + 37 + 30's names).
- Exam themes: sign-convention drills under time pressure; matrix products in
  meeting order; instrument design numerics; name-the-aberration from spot
  diagrams; one essay from the approximation-hierarchy thread (waves → rays →
  paraxial, and what each step buys and costs).

## 7. Build order and validation gates

Build order `33 → 34 → 35 → 36 → 37` — teaching order and dependency order
coincide: 34's derivations lean on 33's equal-OPL result, 35 packages 34's
algebra, 36 spends 35's formalism, 37 turns 35's exact tracer against 34's
model. `rayoptics.py`'s matrix core (§4 limits/conservation tests) lands with
35; the exact-trace tests (convergence/seeds) land with 37. **The six dictated
names (`free_space`, `thin_lens`, `mirror`, `refraction_flat`,
`refraction_spherical`, `cascade`) freeze when 35 merges** — part-12's plan
cites them verbatim for the $q$-parameter, and renames after that point are
breaking changes across plans.

With `33-fermat`: add NEW registry entry `light-takes-fastest-path`
(`assessment/misconceptions.yml`, status `addressed` once page + quiz land);
deposit 33's glossary terms (`fermats-principle` is part-06's deposit — cite,
never re-add). With `34-lenses`: add `half-lens-half-image`; add the ray-optics
sign-convention entry to `content/en/conventions.md` (one boxed subsection
cross-linked from 34's table — the course states the convention exactly once,
the same pattern as part-07's handedness entry). With `35-abcd-matrices`: add
`lens-powers-always-add` (the ray-side reinforcement of
`optical-elements-commute` cites part-07's entry, no re-point). With
`36-instruments`: add `magnification-reveals-detail`. With `37-aberrations`:
add `aberrations-need-imperfection`.

Per module: the standard four gates (README, bottom). Additionally for this
part: 36's detail meter and 37's stop-down study import `diffraction.airy_radius`
/ `diffraction.rayleigh_criterion` — build coordination with part-09's modules
is required before 36 merges (the names are dictated precisely so the two parts
can build in parallel).

## 8. Deviations from the master plan

- **Approximation-first made structural:** master plan §17 asks that geometrical
  optics be "presented as an approximation to wave optics"; this plan makes the
  demand load-bearing — the part opens with the `approximation` honesty box,
  33 derives rays from stationary phase, and 36/37 measure the model's edges.
  Nothing in the part asserts a ray without its provenance.
- **Fermat as the full variational module:** per part-06 §8's split, 17 kept
  only a taste ($dT/dx$); 33 owns stationarity proper, the maximum case, and
  equal-OPL imaging — content the master plan's one-line 10.1 does not mention.
- **Sign convention pinned to Hecht, named:** the master plan lists "sign
  conventions" as a topic without choosing one. This plan adopts Hecht's,
  states it once in 34's boxed table, mirrors it into
  `content/en/conventions.md`, and forbids restatement elsewhere.
- **Meridional-plane-only tracing (scope decision):** `trace_exact` and
  `spot_diagram` work in the meridional plane; skew rays are out of scope for
  the core course. On-axis spots are exact by revolution; off-axis output is
  labelled "tangential fan" honestly. Full 3-D coma shapes are sacrificed —
  logged as the price of a library a student can read in one sitting.
- **Thick lenses deferred to an advanced box (scope decision):** principal
  planes appear only as 35's matrix-factorisation advanced material; no core
  content or later plan depends on thick-lens formulas.
- **Instrument order refined:** master plan 10.4 lists camera, microscope,
  telescope, magnifier; this plan teaches camera → magnifier → microscope →
  telescope (single-lens instruments before two-lens compounds, with the
  magnifier as the microscope's second stage).
- **Empty magnification and §26.4 placed:** the master plan's open
  investigation (10-mm telescope) and the diffraction cross-check are not in
  its Part X section at all; this plan lands both in 36 as the honesty
  centerpiece, using part-09's dictated names.
- **Aberrations quantified:** master plan 10.5 says "explore"; this plan
  commits to measured scalings ($h^2$/$h^3$), spot-diagram metrics with
  uncertainty, a designed achromatic doublet, and the stop-down trade — plus
  the Zernike/JWST research box. "Optional advanced ray tracing" from the
  master plan is promoted to the module's spine (`trace_exact`).
- **Namespaced `cascade` twins:** `rayoptics.cascade` deliberately shares its
  name and meeting-order contract with `polarization.cascade` — same operator
  grammar, disambiguated by module namespace; flagged here so the collision is
  read as design, not accident.
- **Five NEW misconceptions added** (`light-takes-fastest-path`,
  `half-lens-half-image`, `lens-powers-always-add`,
  `magnification-reveals-detail`, `aberrations-need-imperfection`); no
  existing registry entry is re-pointed to this part.
