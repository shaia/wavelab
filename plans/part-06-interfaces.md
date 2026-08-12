# Part VI — Reflection, Refraction, and Interfaces — Implementation Plan

> **Master plan:** §13 (Part VI). **Modules:** `17-refraction`, `18-fresnel`, `19-evanescent`. **Status:** planned.
> Canonical numbering, invariants, and conflict log: [README.md](README.md).

## 1. Part overview and narrative arc

Part VI is where the course's machinery first meets real optics. One planar boundary, one
set of boundary conditions — the fields must agree where the media meet — and the whole
of elementary optics falls out: the law of reflection, Snell's law, the Fresnel
amplitudes, the Brewster angle, total internal reflection, and the evanescent wave. The
tools sharpened earlier all get spent: 00's complex amplitudes, 10's impedance algebra,
14's plane waves and boundary conditions, 16's refractive index. The payoff: lake glare,
the 4% ghost in a shop window, the mirror above a diver's head, and the fingerprint
sensor on a phone all become *computable* from one matching condition.

The three modules escalate one derivation. `17-refraction` is the kinematics: which
directions the waves take, amplitudes deliberately unknown — Snell's law by three routes
ranked by depth: Huygens wavefront geometry (visual), phase matching (the deep one: the
fields must agree at every interface point at every instant, so $\omega$ and
$k_\parallel$ are conserved), and Fermat's stationary time (a trailer for `33-fermat`).
`18-fresnel` is the dynamics: continuity of tangential $E$ and $H$ fixes *how much*
reflects and transmits, and Brewster's angle appears as the zero of one curve.
`19-evanescent` is the analytic continuation: past the critical angle $\sin\theta_2 > 1$
forces $k_z$ imaginary, and the algebra — trusted rather than abandoned — predicts a
non-propagating field that tunnels across gaps. Nothing new is postulated after 17.

The plan's chief enhancement over master plan §13 is promoting **phase matching to the
part's organizing principle**, its forward links said out loud: it is why a periodic
interface diffracts into discrete orders (`31-gratings` adds $2\pi m/d$ to the matching
condition), why the matched $k_\parallel$ can exceed what medium 2 supports
(`19-evanescent`), and why frequency never changes in matter (`16-light-in-matter`,
re-derived at the boundary in one line). Second, notebooks 6.2 and 6.3 merge into
`18-fresnel` (§8): Brewster is a *feature of the Fresnel curves*, not a separate
subject. Third, a deliberate **conservation program**: $R + T = 1$ holds only with the
$n\cos\theta$ flux factors — a classic trap made into a verify check, a lab cell, and a
quiz item in 18, then re-audited in 19, where $R = 1$ exactly.

Two unifications give the part its spine: the normal-incidence Fresnel coefficient
$r = (n_1 - n_2)/(n_1 + n_2)$ is letter-for-letter the string-junction algebra of
`10-impedance` (`waves.junction_coefficients`), boxed side-by-side in 18; and the
evanescent decay $e^{-z/\delta}$ is `02-damped-driven`'s damped exponential in a spatial
costume. Per master plan §13 the part "should use Hecht heavily": §3 names each module's
Hecht companion topics, and the skeletons map onto §27's five-stage companion structure.
Seeds planted for later parts: the external/internal $\pi$ shift (`24-thin-films`);
$r, t$ as the letters of the Fabry–Pérot sum (`26-fabry-perot`); the s/p basis and the
Brewster polarizer (`20-polarization`); the TIR phase behind the Fresnel rhomb
(`21-jones-calculus`); evanescent cladding fields (`46-waveguides`, `47-fibers`).

## 2. Position in the course

- **Requires:**
  - `14-em-waves`: plane waves $\Real[\hat{E}\,e^{\ii(\mathbf{k}\cdot\mathbf{r}-\omega t)}]$;
    continuity of tangential $E$ and $H$ at a charge- and current-free boundary —
    assumed as a result here, derived there. Plane-wave field helpers from `em.py`
    (exact names per part-05's plan as built).
  - `16-light-in-matter`: $v = c/n$, $\lambda = \lambda_0/n$, frequency unchanged
    (registry id `frequency-changes-in-medium` owned there); complex index
    $n + \ii\kappa$ (this part's signatures are complex-ready, §4).
  - `10-impedance`: `junction_coefficients` / `power_coefficients` from `waves.py` and
    the mismatch intuition — reflection is what impedance discontinuity *does*.
  - `00-phasors`: complex-amplitude arithmetic; unimodular numbers as pure phase (TIR).
  - `02-damped-driven`: the decaying exponential $e^{-t/\tau}$, reused as $e^{-z/\delta}$.
- **Feeds:** `20-polarization` (the s/p basis, Brewster as polarizer); `24-thin-films`
  (amplitude coefficients, $\pi$-shift bookkeeping; the FTIR three-layer algebra as
  first transfer-matrix instance); `26-fabry-perot` ($r, t$ power the Airy sum);
  `31-gratings` ($k_\parallel$ conservation → order equation); `33-fermat` (owns the
  variational route trailered in 17); `46-waveguides` / `47-fibers` (TIR confinement,
  evanescent cladding tails, couplers).
- **Explicitly not assumed:** Jones matrices (21 — s and p are two scalar problems);
  coherence (27 — monochromatic sources only); multilayer interference (24 — the FTIR
  gap is tunneling, not fringes); absorption physics beyond accepting complex $n$ in
  signatures (metallic reflection is an aside; its physics is 16's); diffraction
  (interfaces are infinite planes).

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|
| `17-refraction` | `content/en/interfaces/17-refraction.md` | Refraction: three routes to Snell's law | 6.1 | Hecht, propagation of light — Huygens's principle, refraction, Fermat's principle | planned |
| `18-fresnel` | `content/en/interfaces/18-fresnel.md` | Fresnel equations and the Brewster angle | 6.2 + 6.3 | Hecht, electromagnetic theory of light — Fresnel equations, Brewster's law; Griffiths, EM waves in matter (derivation; sign caveat in §5.2) | planned |
| `19-evanescent` | `content/en/interfaces/19-evanescent.md` | Total internal reflection and evanescent waves | 6.4 | Hecht, total internal reflection, evanescent waves, frustrated TIR; Griffiths for the complex-wavevector treatment | planned |

## 4. Shared infrastructure for this part

**`src/wavelab` — existing used:** `waves.junction_coefficients`,
`waves.power_coefficients` (18's unification box and tests); plane-wave field builders
from `em.py` (exact names per part-05's plan as built); `phasors.real_signal`;
`measurement.add_noise` + fit helpers (Brewster hunt, decay fits);
`validation.scaling_exponent`, `validation.seed_study`.

**`src/wavelab` — new: `interfaces.py`** (introduced and owned by this part; README
ownership table). Docstring model spec:

- **System:** a monochromatic plane wave at a planar interface between homogeneous,
  isotropic, non-magnetic media of indices $n_1, n_2$ (either may be complex,
  $n + \ii\kappa$); observables are complex amplitude coefficients, power
  reflectance/transmittance, and evanescent field profiles.
- **Dynamics:** none integrated — algebraic solutions of Maxwell's boundary conditions
  (tangential $E$ and $H$ continuous) under the course convention $e^{-\ii\omega t}$.
- **Boundary:** one infinite plane at $z = 0$; `ftir_transmission` alone uses a
  three-layer stack (medium 1 / gap / medium 3) with two such planes.
- **Ensemble:** deterministic; callers add noise via `wavelab.measurement`.
- **Ignored:** roughness, magnetic response ($\mu = \mu_0$), nonlinearity, beam
  finiteness (Goos–Hänchen named, not computed); absorption only via complex $n$.
- **Valid when:** interface flat and clean on the wavelength scale; media linear and
  isotropic; steady-state monochromatic illumination.
- **Failure modes:** transmittance as $|t|^2$ without flux factors (breaks $R+T=1$);
  real-branch `arcsin` past critical (NaN where physics wants imaginary $k_z$); mixing
  $r_p$ sign conventions (Hecht vs Griffiths, §5.2); reading evanescent decay as
  absorption.

Function-level sketch (signatures + contracts):

```python
snell_angle(n1, n2, theta1) -> theta2      # complex-safe: real below critical, complex above;
                                           # branch chosen so the transmitted field decays
critical_angle(n1, n2) -> theta_c          # arcsin(n2/n1); ValueError if n1 <= n2 (no TIR)
brewster_angle(n1, n2) -> theta_B          # arctan(n2/n1)
fresnel_rs(n1, n2, theta1) -> r            # complex amplitude, s-pol, course (Hecht) convention
fresnel_ts(n1, n2, theta1) -> t            # s-pol transmission; t = 1 + r identically
fresnel_rp(n1, n2, theta1) -> r            # p-pol; Hecht sign: r_p(0) = -r_s(0)
fresnel_tp(n1, n2, theta1) -> t            # p-pol transmission
reflectance(n1, n2, theta1, pol) -> R      # |r|^2; pol in {"s","p"}; 1 above critical
transmittance(n1, n2, theta1, pol) -> T    # Re(n2 cos theta2)/(n1 cos theta1) * |t|^2 — the
                                           # flux factor is the contract; 0 above critical; R+T=1
penetration_depth(n1, n2, theta1, lam) -> delta   # lam/(2 pi sqrt(n1^2 sin^2 th1 - n2^2)); inf below crit.
evanescent_field(z, n1, n2, theta1, lam) -> a     # normalized profile |E(z)|/|E(0+)| = exp(-z/delta)
ftir_transmission(n1, n2, gap, theta1, lam, pol, n3=None) -> T
                                           # exact three-layer tunneling T; n3 defaults n1;
                                           # -> 1 as gap -> 0, ~ exp(-2*gap/delta) as gap -> inf
```

All `n` arguments accept complex values (forward compatibility with 16's $n + \ii\kappa$;
amplitude coefficients stay exact for absorbing media). Angles in radians; `lam` is the
vacuum wavelength against the `units` registry.

**`tests/physics/` additions:**

- *conservation:* $R + T = 1$ both polarizations across a dense $[0°, 90°)$ sweep,
  external and internal pairs; above critical, $R = 1$ to machine precision and the
  time-averaged normal Poynting flux in medium 2 is zero.
- *limits:* `fresnel_rs/ts(n1, n2, 0)` equal `waves.junction_coefficients(n1, n2)`
  exactly (the Z ↔ n unification); `fresnel_rp(n1, n2, 0) == -fresnel_rs(n1, n2, 0)`
  (the convention, pinned); grazing $R \to 1$; `fresnel_rp` zero at `brewster_angle`;
  `snell_angle` at `critical_angle` gives 90°; $t_s = 1 + r_s$ at every angle.
- *convergence:* `ftir_transmission` → bare-interface `transmittance` as gap → 0, → 0
  as gap → ∞ approaching the pure exponential $e^{-2d/\delta}$.
- *scaling:* `penetration_depth` ∝ $\lambda$ — fitted exponent 1.00 via
  `scaling_exponent`; slope of $\ln T$ vs gap equals $-2/\delta$.
- *dimensions:* `penetration_depth` in meters, angles in radians, `transmittance`
  dimensionless — against the `units` registry.
- *seeds:* noisy Brewster-angle location (fit of the $R_p$ minimum) via `seed_study`.

**Shared media:** one script `media/render/render_interfaces.py` produces all Part VI
MP4s (shot lists in §5); all field maps share one colormap and layout so 17's
propagating picture morphs recognizably into 19's evanescent one. **Glossary themes:**
interface optics — refraction and rays (17), polarization-resolved reflection (18), TIR
and evanescence (19).

## 5. Module specifications

### 5.1 `17-refraction` — Refraction: three routes to Snell's law

- **Identity and scope:** master-plan notebook 6.1. Directions only — amplitudes
  deferred to `18-fresnel`, beyond-critical behavior to `19-evanescent`, the full
  variational treatment of Fermat to `33-fermat` (a taste here, the meal there).
- **Prerequisites:** `14-em-waves` (plane waves, $\mathbf{k}$, wavefronts);
  `16-light-in-matter` ($v = c/n$, $\lambda = \lambda_0/n$, frequency unchanged);
  `08-wave-equation` (wavefront kinematics).
- **Learning objectives:**
  - `OBJ-17-1` — Apply n1 sin(theta1) = n2 sin(theta2) to compute refraction angles and
    trace rays through plane interfaces, stating when the ray bends toward the normal.
  - `OBJ-17-2` — Derive Snell's law from the Huygens wavefront construction, using the
    wavelength change lambda = lambda0/n across the boundary.
  - `OBJ-17-3` — Derive both the law of reflection and Snell's law from phase matching:
    the fields must agree at every interface point at every time, so omega and
    k_parallel are common to all three waves.
  - `OBJ-17-4` — Explain Fermat's stationary-time principle without teleology and
    verify numerically that the stationary path satisfies Snell's law.
  - `OBJ-17-5` — Explain from boundary matching why frequency cannot change across an
    interface while wavelength must, and compute lambda2 = lambda1 (n1/n2).
- **Mathematical background:** has — plane-wave phases, trigonometry, one-variable
  minimization; introduced here — the "match a function of $x, t$ on a plane" argument
  (a functional identity forces equal $\omega$, $k_\parallel$), reused verbatim in 31.
- **Physical intuition goals:** (1) refraction is wavefront traffic — the slow medium
  compresses wavelengths, so fronts hinge at the boundary; (2) the interface cannot
  invent or destroy oscillations: frequency is untouchable, wavelength pays; (3) denser
  medium → toward the normal, and rays retrace exactly when reversed; (4) "fastest
  path" is a *summary* of the physics, not a mechanism.
- **Section skeleton seeds:**
  - *puzzle:* the spearfisher's problem — aim straight at the fish you see and you miss
    high, every time. (Boxed: when a wave crosses into a slower medium, what rule
    decides the new direction — and what stays the same across the boundary?)
  - *predict:* (1) denser medium — toward or away from the normal? (2) in glass, which
    changes: frequency, wavelength, both? (reinforces `frequency-changes-in-medium`,
    owned by 16) (3) run the ray backwards — does it retrace? (4) "light takes the
    fastest route" — how would it know in advance?
  - *explore:* refraction sandbox — sliders $n_1, n_2 \in [1.0, 2.5]$, $\theta_1$; live
    rays with $\theta_2$ readout; wavefront overlay ($\lambda/n$ compression, hinge);
    phase-matching overlay painting the interface phase of all three waves (agreement
    only at the Snell angle); past critical the transmitted ray grays out ("module 19").
  - *derive:* Huygens construction → phase matching (the deep route; forward links to
    31, 19, 16 stated in prose) → Fermat as trailer: the lifeguard problem, stationary
    time gives Snell; teleology defused — paths near the stationary one agree in phase,
    so that is where amplitude survives (full story: 33).
  - *verify:* brute-force Fermat travel-time curve — stationary point matches
    `snell_angle` to $10^{-10}$ (`numerical-observation` box); phase-mismatch meter
    minimized exactly at the Snell angle; reversibility —
    `snell_angle(n2, n1, snell_angle(n1, n2, theta))` round-trips to machine precision.
  - *transfer:* gratings (31) — a periodic interface absorbs $k_\parallel$ in lumps of
    $2\pi m/d$; mirages — continuous $n(y)$ makes $n\sin\theta$ a ray invariant;
    seismic and underwater acoustics; apparent depth (the fish, quantified).
  - *quiz:* numeric Snell chain; bend-direction MC; wavelength-vs-frequency MC;
    phase-matching conceptual MC; Fermat free-response.
  - *explain:* rewrite "light bends because it seeks the fastest path" so no intention
    appears and the physics survives; tell the spearfisher where the fish really is;
    why can't the interface change the frequency?
  - *advanced:* continuous $n$: $n(y)\sin\theta(y)$ invariant, the ray ODE, a computed
    mirage; a pointer to negative refraction as engineered phase matching. Safe to
    skip; nothing later depends on it.
- **Core derivations:** (1) Huygens: fronts spaced $\lambda_0/n_1$, $\lambda_0/n_2$
  hinge at the boundary; the shared hypotenuse gives $\lambda_1/\sin\theta_1 =
  \lambda_2/\sin\theta_2$, i.e. $n_1\sin\theta_1 = n_2\sin\theta_2$. (2) Phase
  matching: with all fields $\propto e^{\ii(\mathbf{k}\cdot\mathbf{r} - \omega t)}$,
  any linear boundary condition on $z = 0$ must hold for all $x, t$; hence all three
  $\omega$ equal and all three $k_x$ equal: $k_x = n_1 k_0\sin\theta_1 =
  n_1 k_0\sin\theta_r = n_2 k_0\sin\theta_2$ — reflection law and Snell together,
  before any amplitude is computed. (3) Fermat: $T(x) = n_1\sqrt{h_1^2 + x^2}/c +
  n_2\sqrt{h_2^2 + (d-x)^2}/c$; $dT/dx = 0$ reproduces Snell.
- **Model specification draft:** System — one plane wave meeting one flat interface
  between transparent media; observables are directions and phase maps. Dynamics — free
  propagation plus a linear matching condition; no amplitudes solved. Boundary — the
  single infinite plane $z = 0$. Ensemble — deterministic; the refractometry lab adds
  seeded angle noise. Ignored — amplitudes and energy split (18), absorption,
  roughness, beam width. Valid when — interface flat over many wavelengths, media
  transparent and isotropic. Failure modes — ray reasoning on wavelength-scale
  structure (that is diffraction, Part IX); the real-angle formula past critical.
- **Epistemic classification:** Snell's law — historically an `empirical-law` (Snel and
  Descartes measured it long before Maxwell), then a `theorem` given the wave model:
  the page carries *both* boxes, an epistemology lesson. Phase matching — `theorem`.
  Fermat — `theorem` (statement; proof route in 33). Stationarity check —
  `numerical-observation`. "Light seeks the fastest path" — prose caveat, never boxed.
- **Misconceptions:** no NEW registry entry. Reinforces `frequency-changes-in-medium`
  (owned by 16) with a quiz distractor; the fastest-path teleology is handled in prose
  and an explain question, not the registry — a language habit without a falsifier
  distinct from the Fermat demonstration itself (logged in §8).
- **Glossary terms:** `refraction` (he: שבירה), `snells-law` (חוק סנל),
  `angle-of-incidence` (זווית פגיעה), `surface-normal` (אנך; `he_reject` candidate:
  נורמל), `wavefront` (חזית גל — dedupe if part-03 deposited it first),
  `phase-matching` (התאמת פאזה), `fermats-principle` (עקרון פרמה), `apparent-depth`
  (עומק מדומה — translator to confirm).
- **Interactive controls and simulations:** the refraction sandbox; wavefront animation
  with the hinge visible; Fermat path explorer — drag the crossing point, live
  travel-time readout, stationary point marked; phase-agreement strip.
- **Virtual lab outline** (`notebooks/en/labs/17-refraction.ipynb`): (1) sandbox play;
  (2) wavefront geometry — measure $\theta_2$ off rendered fronts vs `snell_angle`;
  (3) Fermat brute force; (4) phase-mismatch meter minimized over trial $\theta_2$;
  (5) *measurement:* refractometry — noisy $(\theta_1, \theta_2)$ pairs via
  `measurement.add_noise`, least squares on $\sin\theta_1$ vs $\sin\theta_2$, report
  $n_2/n_1$ ± uncertainty.
- **Real-experiment counterpart:** laser pointer into a glass block or water tank on
  printed protractor paper; photograph, extract angles, import as CSV into lab cell
  (5) and fit $n$. Secondary: coin-in-cup apparent depth.
- **Media assets** (`render_interfaces.py`): (a) Huygens construction — fronts hinging,
  wavelength compression visible; (b) phase-matching field map — phase stripes
  continuous across the interface, angle sweeping so the match breaks and re-locks.
  Language-neutral, no burned-in text.
- **Quiz bank outline:** `Q-17-1` numeric — slab exit angle and lateral shift
  (OBJ-17-1); `Q-17-2` MC — bend direction (OBJ-17-1); `Q-17-3` MC — what changes in
  glass (OBJ-17-5, distractor from `frequency-changes-in-medium`); `Q-17-4` MC —
  Huygens geometry (OBJ-17-2); `Q-17-5` MC — which quantities must agree on the
  boundary (OBJ-17-3); `Q-17-6` free — defuse the fastest-path teleology (OBJ-17-4).
- **Problem set outline:** analytical — apparent depth; prism minimum deviation; slab
  lateral displacement. Computational — mirage ray ODE in $n(y) = n_0(1 - \alpha y)$.
  Challenge — derive the grating order equation from phase matching with a periodic
  surface; check it reduces to Snell as $d \to \infty$ (forward link to 31).
- **Runtime budget:** closed-form rays and $10^4$-point Fermat scans — trivial; 2-D
  field maps $512^2$ complex, few interactive frames, sweeps precomputed as MP4.
- **Validation gates:** standard four (README) with `--module 17-refraction`; the
  reversibility and Fermat-agreement tests land with this module.
- **Open questions for the author:** whether the beyond-critical sandbox region shows a
  hint of evanescent field (teaser) or stays blank (suspense for 19); whether the
  mirage advanced section includes the ODE or only the invariant and the picture.

### 5.2 `18-fresnel` — Fresnel equations and the Brewster angle

- **Identity and scope:** master-plan notebooks 6.2 + 6.3, merged (§8). Amplitudes and
  energy split at one interface, both polarizations, plus Brewster. Defers: evaluation
  beyond critical to `19-evanescent`; multilayers to `24-thin-films`; polarization
  formalism to `20-polarization`/`21-jones-calculus`.
- **Prerequisites:** `17-refraction` ($k_\parallel$ conservation, $\theta_2$);
  `14-em-waves` (tangential $E$, $H$ continuity — cited as that module's result);
  `10-impedance` (`junction_coefficients`, `power_coefficients` — the algebra to be
  unified); `16-light-in-matter` ($n$ as material response).
- **Learning objectives:**
  - `OBJ-18-1` — Derive r_s = (n1 cos theta1 - n2 cos theta2)/(n1 cos theta1 + n2 cos
    theta2) and t_s = 1 + r_s from continuity of tangential E and H.
  - `OBJ-18-2` — State and apply the p-polarization coefficients in the course (Hecht)
    sign convention and compute all four amplitude coefficients below critical.
  - `OBJ-18-3` — Compute R = |r|^2 and T = (n2 cos theta2 / n1 cos theta1) |t|^2,
    verify R + T = 1, and explain why |t|^2 alone is not an energy statement.
  - `OBJ-18-4` — Show that at normal incidence r = (n1 - n2)/(n1 + n2) and map it onto
    the module-10 string-junction coefficients with the index in the impedance slot.
  - `OBJ-18-5` — Derive tan(theta_B) = n2/n1 from r_p = 0 and explain the Brewster
    angle microscopically via the dipole radiation pattern.
  - `OBJ-18-6` — Predict the reflected phase (0 or pi) for external and internal
    reflection, each polarization, below the critical angle.
- **Mathematical background:** has — boundary-condition algebra, phasors, the junction
  derivation of 10; introduced here — resolving a vector wave into s and p scalar
  problems (mirror symmetry decouples them — the course's first symmetry-decouples
  argument for fields).
- **Physical intuition goals:** (1) glass reflects ~4% per surface head-on — a number
  to carry for life; (2) everything reflects perfectly at grazing incidence; (3) at one
  angle the reflected p-wave dies because the transmitted-medium dipoles cannot radiate
  along their own axis; (4) an amplitude coefficient may exceed 1 — only flux-weighted
  quantities must balance.
- **Section skeleton seeds:**
  - *puzzle:* a shop window at dusk shows the goods *and* your face — one pane both
    transmits and reflects; polarized sunglasses kill lake glare only near one viewing
    angle, and tilting your head brings it back. (Boxed: what fraction of a wave
    reflects at a boundary, and what decides it — angle, polarization, or both?)
  - *predict:* (1) glass head-on: 50%, 20%, 4%? (2) where reflected p vanishes,
    transmitted p is zero / unchanged / maximal? (targets NEW
    `brewster-no-transmission`) (3) more reflection at grazing or normal? (4) does the
    reflected wave ever flip sign, and does it matter?
  - *explore:* Fresnel explorer — sliders $n_1, n_2, \theta_1$; signed $r_s, r_p$ and
    power $R_s, R_p$ curves; Brewster marker riding the $r_p$ zero; external/internal
    toggle (beyond-critical shaded "module 19"); phase panel with $\arg r$ jumping
    between 0 and $\pi$.
  - *derive:* s/p geometry fixed by one figure with the convention box FIRST → s-case
    fully worked → p-case by the same machinery → normal-incidence limit and the
    string-junction unification box → flux factors, $R + T = 1$ → Brewster from the
    $r_p$ numerator, then the dipole story → external/internal phase shifts (the
    $\pi$-shift ledger 24 will spend).
  - *verify:* $R + T = 1$ across the sweep (`numerical-observation` box, max deviation
    $<10^{-14}$); `fresnel_rp(brewster_angle)` zero to machine precision; normal
    incidence vs `waves.junction_coefficients(n1, n2)` — exact; grazing $R \to 1$;
    $t_s = 1 + r_s$ at every angle.
  - *transfer:* Brewster windows in laser cavities (45); reflection polarizers and the
    s/p basis (20); thin-film $\pi$-shift bookkeeping (24); $r, t$ as letters of the
    Fabry–Pérot alphabet (26); photography — the polarizing filter works only near 56°;
    anti-reflection coatings as the anti-4% industry (24).
  - *quiz:* the 4% numeric; Brewster numeric and transmitted-fraction MC; the
    flux-factor trap; phase-shift MC; junction-mapping matching item.
  - *explain:* how $t > 1$ (internal incidence) coexists with energy conservation;
    lake-glare geometry for a photographer; why s and p must be treated separately.
  - *advanced:* reflection off an absorbing medium — complex $n_2$ gives $|r| < 1$ and
    a pseudo-Brewster minimum instead of a zero (metallic sheen; physics owned by 16);
    degree of polarization of reflected skylight.
- **Core derivations:** in the course convention, non-magnetic media; s from continuity
  of $E_y$ and $H_x$, p in Hecht's sign:

  $$
  r_s = \frac{n_1\cos\theta_1 - n_2\cos\theta_2}{n_1\cos\theta_1 + n_2\cos\theta_2},
  \quad t_s = 1 + r_s ; \qquad
  r_p = \frac{n_2\cos\theta_1 - n_1\cos\theta_2}{n_2\cos\theta_1 + n_1\cos\theta_2},
  \quad t_p = \frac{2 n_1\cos\theta_1}{n_2\cos\theta_1 + n_1\cos\theta_2} .
  $$

  Normal incidence: $r_s = (n_1 - n_2)/(n_1 + n_2)$, $r_p = -r_s$ — the sign difference
  is pure convention (opposite arrow choices for the reflected p field; s and p are
  indistinguishable head-on). **Sign-convention box, fixed once in a boxed admonition:**
  Hecht and Griffiths choose that arrow oppositely, so their $r_p$ differ by an overall
  sign — Griffiths gets $r_p(0) = +r_s(0)$ where Hecht gets $-r_s(0)$; every $R$, $T$,
  and Brewster angle agrees. The course fixes **Hecht's convention**, states it here
  once, pins it with a unit test (§4), and names the discrepancy so students reading
  both books aren't burned. Power: $R = |r|^2$ and
  $T = (n_2\cos\theta_2 / n_1\cos\theta_1)\,|t|^2$ with $R + T = 1$ — energy compares
  normal Poynting components, and both wave speed *and* beam cross-section change
  across the boundary. **Unification box:** at normal incidence $(r_s, t_s) =$
  `waves.junction_coefficients(n1, n2)` — letter-for-letter the string algebra with $n$
  in the impedance slot. The physical EM impedance is $Z = Z_0/n$, and $E$ is
  force-like (voltage-like) where string displacement is velocity-like; swapping which
  member of the conjugate pair you track inverts the mismatch ratio, $Z \to 1/Z$ — two
  inversions, one identical formula. The flux factor is `waves.power_coefficients`'
  lesson again: $t^2$ alone is never a power ratio. Brewster: $r_p = 0$ at
  $n_2\cos\theta_1 = n_1\cos\theta_2$, with Snell $\theta_1 + \theta_2 = \pi/2$ and
  $\tan\theta_B = n_2/n_1$. Microscopically: the reflected ray would leave
  perpendicular to the transmitted one; the medium-2 dipoles oscillate along the
  transmitted $E_p$, which then points *along* the would-be reflected ray — and a
  dipole does not radiate along its own axis.
- **Model specification draft:** System — plane wave at a planar boundary between
  transparent media; observables are the four amplitude coefficients, $R$, $T$, and
  reflected phase, resolved into s and p. Dynamics — Maxwell boundary conditions at one
  plane; no propagation solved. Boundary — one infinite interface; semi-infinite media
  (no second surface — that is 24). Ensemble — deterministic; the Brewster hunt adds
  seeded detector noise. Ignored — roughness, absorption (aside only), beam width,
  multiple reflections. Valid when — flat clean interface, linear isotropic
  non-magnetic media, $\theta_1$ below critical for transmitted-wave statements.
  Failure modes — $|t|^2$ read as transmittance; convention mixing; real-angle formulas
  beyond critical.
- **Epistemic classification:** boundary conditions — `theorem` (given Maxwell; derived
  in 14); Fresnel coefficients — `theorem`; sign convention — `definition` (boxed — the
  module's mandatory admonition, alongside the unification box); dipole explanation of
  Brewster — `model-assumption` (re-radiation picture, honest about scope); the $R + T$
  deviation figure — `numerical-observation`.
- **Misconceptions:** NEW `brewster-no-transmission` — "At the Brewster angle no light
  is transmitted" (confusing $r_p = 0$ with $t_p = 0$). Falsifying experiment: plot
  $T_p$ across angles — at $\theta_B$ it is *maximal*, exactly 1: all of p goes
  through; the lab cell prints the number. Distractor: quiz option "at Brewster the
  interface blocks p-polarized light".
- **Glossary terms:** `s-polarization` (he: קיטוב s — translator to decide vs ניצב/TE),
  `p-polarization` (קיטוב p), `fresnel-equations` (משוואות פרנל), `reflectance`
  (החזרוּת; `he_reject` candidate: רפלקטיביות), `transmittance` (מעבירוּת; `he_reject`
  candidate: טרנסמיטנס), `brewster-angle` (זווית ברוסטר), `glare` (סנוור).
- **Interactive controls and simulations:** the Fresnel explorer; dipole-radiation
  Brewster view — sweep $\theta_1$, watch the reflected brightness follow the dipole
  donut pattern and die at $\theta_B$; phase-flip animation comparing external and
  internal reflection of a pulse (string-junction déjà vu, on purpose).
- **Virtual lab outline** (`notebooks/en/labs/18-fresnel.ipynb`): (1) explorer play,
  find the 4%; (2) conservation audit — $|r|^2 + |t|^2$ (fails) then $R + T$ (passes)
  in adjacent cells; (3) *Brewster hunt (measurement):* noisy reflected-p readings vs
  angle via `measurement.add_noise`, fit the $|r_p|^2$ model near the minimum, report
  $\theta_B \pm \sigma$ and inferred $n_2/n_1 \pm \sigma$; (4) phase inspection —
  $\arg r$ vs angle, external and internal; (5) junction cross-check —
  `fresnel_rs(n1, n2, 0)` against `waves.junction_coefficients(n1, n2)`.
- **Real-experiment counterpart:** laser pointer, glass slide, and a polarizer from old
  sunglasses; rotate the slide on a printed protractor, find the angle where the
  reflected spot vanishes; $\tan\theta_B$ gives $n$. Phone light-meter readings import
  as CSV into lab cell (3).
- **Media assets** (`render_interfaces.py`): (c) Brewster dipole animation — donut
  radiation patterns, reflected ray fading to zero through $\theta_B$; (d) external vs
  internal reflection of a wave packet, phase flip visible (mirrors part-03's junction
  framing). Language-neutral.
- **Quiz bank outline:** `Q-18-1` numeric — reflectance of glass at normal incidence
  (OBJ-18-3); `Q-18-2` MC — transmitted p at Brewster (OBJ-18-5, distractor from
  `brewster-no-transmission`); `Q-18-3` numeric — the flux-factor trap: given $t$,
  compute $T$ (OBJ-18-3); `Q-18-4` MC — phase of external vs internal reflection
  (OBJ-18-6); `Q-18-5` matching — Fresnel normal incidence ↔ string junction
  (OBJ-18-4); `Q-18-6` numeric — Brewster for water + sunglasses geometry (OBJ-18-5);
  `Q-18-7` free — derive $r_s$ from the two continuity statements (OBJ-18-1, OBJ-18-2).
- **Problem set outline:** analytical — derive $r_p, t_p$; prove $\theta_1 + \theta_2 =
  \pi/2$ at Brewster; two-surface pane net transmission (incoherent, ~92%).
  Computational — degree of polarization of reflected light vs angle; pseudo-Brewster
  for complex $n_2$. Challenge — Fresnel coefficients for $\mu \ne \mu_0$: impedance,
  not index, is the fundamental variable — the unification box vindicated.
- **Runtime budget:** closed-form curves on $10^3$-point angle grids; dipole animation
  ≤ 100 precomputed frames. Trivial in Pyodide.
- **Validation gates:** standard four with `--module 18-fresnel`; the §4 junction
  equality, Brewster zero, and $t_s = 1 + r_s$ tests land here, and
  `brewster-no-transmission` enters `assessment/misconceptions.yml`.
- **Open questions for the author:** one admonition or two for the sign-convention and
  unification boxes (recommendation: two — a `definition` and a synthesis); dipole
  Brewster story in core or advanced (recommendation: core — it is the module's best
  physics and Hecht tells it in prose).

### 5.3 `19-evanescent` — Total internal reflection and evanescent waves

- **Identity and scope:** master-plan notebook 6.4. TIR, the critical angle, evanescent
  decay and penetration depth, energy flow in TIR, frustrated TIR. Defers: guided modes
  to `46-waveguides`, fibers to `47-fibers`, Goos–Hänchen and the Fresnel rhomb to the
  advanced section, near-field microscopy to a pointer.
- **Prerequisites:** `17-refraction` (phase matching — this module is its
  continuation); `18-fresnel` (coefficients evaluated at complex $\cos\theta_2$);
  `02-damped-driven` (decaying-exponential motif); `16-light-in-matter` (contrast:
  decay by absorption vs decay by geometry).
- **Learning objectives:**
  - `OBJ-19-1` — Compute the critical angle sin(theta_c) = n2/n1 and state when total
    internal reflection can occur at all.
  - `OBJ-19-2` — Show that for theta1 > theta_c the transmitted k_z is imaginary and
    the field decays as exp(-z/delta) with delta = lambda/(2 pi sqrt(n1^2
    sin^2(theta1) - n2^2)), and compute delta.
  - `OBJ-19-3` — Demonstrate that beyond critical |r| = 1 exactly and the time-averaged
    normal energy flux into medium 2 is zero, while the field there is not zero.
  - `OBJ-19-4` — Predict frustrated-TIR transmission qualitatively and compute its
    exponential gap dependence T ~ exp(-2 d/delta).
  - `OBJ-19-5` — Explain the TIR phase shift and one working application: fingerprint
    sensor, beam-splitter cube, or ATR spectroscopy.
- **Mathematical background:** has — Fresnel algebra, complex exponentials, unimodular
  numbers as phase (00); introduced here — analytic continuation as physics: trusting a
  formula where a real angle no longer exists, choosing the branch by a boundary
  condition at infinity.
- **Physical intuition goals:** (1) beyond critical nothing *propagates* into medium 2,
  but the field there is not zero — it hugs the surface within about a wavelength;
  (2) $R = 1$ is exact — TIR out-mirrors any metal; (3) bring a third medium within
  $\sim\lambda$ and light jumps the gap; (4) the decay is not absorption: no energy is
  deposited, and $\delta$ depends on geometry, not on any loss constant.
- **Section skeleton seeds:**
  - *puzzle:* the fingerprint sensor — a prism face is a perfect mirror until a
    fingertip touches the far side; where ridges touch, light escapes. But no light
    crosses a totally reflecting surface. (Boxed: if nothing gets through, how can
    anything on the far side change the reflection?)
  - *predict:* (1) beyond critical, the field in medium 2 is exactly zero / nonzero but
    decaying / weakly propagating? (targets NEW `tir-zero-field`) (2) is $R$ exactly 1
    or just close? (3) a one-wavelength gap between two prisms: no light / some / all?
    (4) does $\delta$ grow or shrink as $\theta_1$ increases past $\theta_c$?
  - *explore:* TIR explorer — $\theta_1$ slider through $\theta_c$, live field map
    morphing from transmitted sinusoid to clinging exponential tail; $\delta$ readout
    in units of $\lambda$; FTIR panel — gap slider $d/\lambda \in [0, 3]$, $T$ readout,
    linear/log toggle, third-medium index slider.
  - *derive:* Snell continued into the complex → the evanescent field and $\delta$ →
    same mathematics as 02's damped exponential, and *not* absorption → $|r| = 1$ as a
    ratio of complex conjugates → energy: mean normal flux zero, tangential flux
    nonzero — energy skims the surface in a $\sim\delta$ sheet → FTIR: three layers,
    the tail re-converted to a propagating wave, exact form in `ftir_transmission`.
  - *verify:* $R = 1$ to machine precision across the beyond-critical sweep; fitted
    slope of $\ln T$ vs gap equals $-2/\delta$ (`numerical-observation` box); mean
    $S_z$ integrates to zero over a cycle; `ftir_transmission` limits — bare Fresnel at
    $d = 0$, pure exponential at large $d$.
  - *transfer:* fibers (47) — TIR as confinement, evanescent cladding tails as design
    constraint; waveguide couplers (46) — controlled FTIR; thin films (24) — the
    three-layer algebra generalizes to the transfer matrix; beam-splitter cubes and ATR
    spectroscopy; the quantum-tunneling analogy — same exponential, same matching.
  - *quiz:* $\theta_c$ numeric; $\delta$ numeric; field-beyond-the-surface MC
    (distractor from `tir-zero-field`); FTIR gap MC; $R = 1$ conservation item;
    fingerprint free-response.
  - *explain:* why a diver sees a mirrored surface outside a bright circle (Snell's
    window) and what sets its edge; how the prism "knows" the finger is there if no
    energy crosses; why evanescent decay is not absorption, in three sentences.
  - *advanced:* the TIR phase shift $\tan(|\varphi_s|/2) = \sqrt{n_1^2\sin^2\theta_1 -
    n_2^2}/(n_1\cos\theta_1)$ and the Fresnel rhomb — TIR phase as a retarder (seeds
    21); Goos–Hänchen — a *beam* reflects displaced because each plane wave picks up an
    angle-dependent phase; photon tunneling times through the FTIR gap as an
    `open-question` admonition — Hartman-effect claims are genuinely contested, cited
    as such, the analogy scoped honestly (exact mathematics, suggestive
    interpretation).
- **Core derivations:** with $k_x = n_1 k_0\sin\theta_1$ conserved (17), medium 2 gives
  $k_z = \sqrt{n_2^2 k_0^2 - k_x^2}$, imaginary beyond $\theta_c$ — the decaying branch
  is kept (the growing one dies by the condition at $z \to \infty$): $k_z = \ii/\delta$
  with

  $$
  \delta = \frac{1}{k_0\sqrt{n_1^2\sin^2\theta_1 - n_2^2}}
         = \frac{\lambda}{2\pi\sqrt{n_1^2\sin^2\theta_1 - n_2^2}} ,
  $$

  diverging at $\theta_c$, shrinking toward $\sim\lambda/2\pi$ at grazing. The field
  $\Real[\hat{E}\,e^{\ii(k_x x - \omega t)}\,e^{-z/\delta}]$ propagates along the
  surface and decays across it. Reflection: $r_s = (n_1\cos\theta_1 - \ii a)/
  (n_1\cos\theta_1 + \ii a)$ with $a = \sqrt{n_1^2\sin^2\theta_1 - n_2^2}$ — numerator
  and denominator are complex conjugates, so $|r_s| = 1$ identically and only a phase
  remains ($r_p$ analogously, with index weights). Energy: with $k_z$ imaginary, field
  and conjugate flux sit in quadrature, so $\langle S_z\rangle = 0$ (the "energy
  sloshes, none flows" bookkeeping of a standing wave, 11) while $\langle S_x\rangle
  \ne 0$. FTIR: matching across medium 1 / gap / medium 3 gives an exact two-interface
  tunneling coefficient with large-gap behavior $T \propto e^{-2d/\delta}$ — the
  amplitude crosses once as $e^{-d/\delta}$, the power squares it.
- **Model specification draft:** System — plane wave in the denser medium beyond the
  critical angle; observables are reflected phase, the evanescent profile, and (FTIR)
  transmitted power into medium 3. Dynamics — the same boundary-condition algebra as
  18, evaluated on the imaginary branch; no new equations. Boundary — one interface for
  TIR; two parallel interfaces at gap $d$ for FTIR. Ensemble — deterministic; decay-fit
  labs add seeded noise. Ignored — beam finiteness (Goos–Hänchen named, not computed),
  absorption, roughness. Valid when — $n_1 > n_2$, $\theta_1 > \theta_c$, interfaces
  flat and parallel over the beam footprint. Failure modes — the growing branch;
  reading $\delta$ as an absorption length; the FTIR formula with an absorbing gap.
- **Epistemic classification:** the decaying-branch choice — `model-assumption`
  (boundary condition at infinity); $|r| = 1$ and $\langle S_z\rangle = 0$ — `theorem`
  within the lossless model; the fitted FTIR slope — `numerical-observation`; photon
  tunneling time — `open-question` (mandatory admonition candidate); the
  quantum-tunneling correspondence — flagged as analogy.
- **Misconceptions:** NEW `tir-zero-field` — "Beyond the critical angle no field exists
  in the second medium." Falsifying experiment: plot the evanescent profile from
  `evanescent_field` (nonzero, decaying, non-propagating), then *demonstrate* FTIR —
  bring a third medium within $\sim\lambda$ and watch light jump the gap via
  `ftir_transmission`; if the field were zero, nothing could know the third medium was
  there. Distractor: quiz option "the field stops exactly at the interface, so a nearby
  third medium cannot receive any light".
- **Glossary terms:** `total-internal-reflection` (he: החזרה פנימית מלאה),
  `critical-angle` (זווית קריטית), `evanescent-wave` (גל דועך; `he_reject` candidate:
  גל אוונסנטי), `penetration-depth` (עומק חדירה), `frustrated-tir` (החזרה פנימית מלאה
  מסוכלת — translator to decide), `optical-tunneling` (מנהור אופטי), `snells-window`
  (חלון סנל).
- **Interactive controls and simulations:** the TIR explorer and FTIR panel;
  Snell's-window fisheye render — a hemisphere of sky compressed into the critical
  cone, mirror outside; phase-shift dial showing $\arg r_s$, $\arg r_p$ beyond critical
  (feeds the Fresnel-rhomb aside).
- **Virtual lab outline** (`notebooks/en/labs/19-evanescent.ipynb`): (1) explorer sweep
  through $\theta_c$; (2) *decay-length measurement:* noisy evanescent profiles at
  several angles (`measurement.add_noise`), log-linear fit per angle, fitted $\delta$
  vs $\theta_1$ against the formula; (3) *FTIR measurement:* $T$ vs gap on a log axis,
  fitted slope $\to \delta \pm \sigma$ — compared with (2): two independent routes to
  the same $\delta$, the measurement-culture punchline; (4) energy audit — numerical
  time-average of $S_z$ (zero within noise), $R = 1$ sweep; (5) fingerprint toy — a
  ridge/valley gap profile mapped through `ftir_transmission` into an image.
- **Real-experiment counterpart:** a glass of water shows Snell's window: photograph
  the underwater view upward, measure the window's angular radius, extract $n$ and
  compare with 17's refractometry. The wet-fingertip-on-glass demo is qualitative FTIR
  at zero cost; quantitative FTIR needs sub-micron gaps — impractical at home; the
  microwave two-prism classic is cited.
- **Media assets** (`render_interfaces.py`): (e) the morph shot — field map sweeping
  through $\theta_c$, the transmitted wave collapsing into a clinging exponential
  sheet; (f) FTIR gap sweep — two prisms closing, transmitted beam brightening, side
  meter drawing $\ln T$ vs $d$ as a straight line. Language-neutral.
- **Quiz bank outline:** `Q-19-1` numeric — $\theta_c$ for glass/air and water/air
  (OBJ-19-1); `Q-19-2` numeric — $\delta$ at a given angle, in units of $\lambda$
  (OBJ-19-2); `Q-19-3` MC — the field beyond the interface (OBJ-19-3, distractor from
  `tir-zero-field`); `Q-19-4` MC — FTIR vs gap width (OBJ-19-4); `Q-19-5` MC — is $R$
  exactly 1, and where does energy flow meanwhile (OBJ-19-3); `Q-19-6` free — explain
  the fingerprint sensor end-to-end (OBJ-19-5).
- **Problem set outline:** analytical — derive $\delta$ from $k_\parallel$
  conservation; TIR phase shifts and a Fresnel-rhomb quarter-wave design;
  Snell's-window radius from $n$. Computational — exact FTIR vs the naive
  $e^{-2d/\delta}$, mapping where the two-interface correction matters. Challenge —
  Goos–Hänchen from the stationary phase of a narrow angular spectrum (uses 04's
  machinery; previews 12's group-delay logic in space).
- **Runtime budget:** field maps $512 \times 256$ complex, ≤ 60 interactive frames; all
  coefficients closed-form; fingerprint image ≤ $256^2$. Seconds in Pyodide.
- **Validation gates:** standard four with `--module 19-evanescent`; the §4 TIR
  conservation, FTIR convergence, and scaling tests land here, and `tir-zero-field`
  enters `assessment/misconceptions.yml`.
- **Open questions for the author:** whether the Snell's-window photo lives here or in
  17 (recommendation: here — the window's *edge* is this module's quantity); how far to
  take the Hartman discussion (recommendation: three sentences and two citations — a
  trailhead, not a treatment); fingerprint toy as lab cell or media asset.

## 6. Part-level assessment and capstone hooks

- Master plan §23's **interface virtual lab** (measured reflection/transmission
  coefficients) is delivered by 18's Brewster hunt and conservation audit plus 19's two
  routes to $\delta$ — the part's measurement-culture set pieces.
- Capstone §35.2 (virtual optical bench) consumes this part directly: per-surface
  Fresnel losses, Brewster windows, and TIR prisms/beam-splitter cubes take their
  numbers from `interfaces.py`. Capstone §35.4 (optical communication link) stands on
  19: fiber confinement is TIR, evanescent couplers are FTIR on purpose. Capstone §35.3
  (grating spectrometer) inherits its central equation from 17's phase matching via 31.
- Cross-module synthesis problems (owned by the part): (a) *the dive mask* — chain
  17 + 18 + 19: where the fish appears, how bright it is, where the surface turns to
  mirror; (b) *the window pane* — two surfaces, ~4% each, net ~92%: why the reflections
  add *incoherently* here (trailer for 27) and what changes when the pane thins to a
  soap film (trailer for 24); (c) *the full energy audit* — one interface, all angles,
  both polarizations, external and internal, $R + T = 1$ everywhere.
- Exam themes: sketch $R_s, R_p$ vs angle from memory, labelling $\theta_B$ and
  $\theta_c$; the flux-factor trap in numeric form; order-of-magnitude $\delta$; which
  statements survive an $r_p$ sign flip and which do not.

## 7. Build order and validation gates

Build order `17-refraction` → `18-fresnel` → `19-evanescent`: each consumes the previous
(17's $k_\parallel$ conservation powers 18's geometry; 18's coefficients on the
imaginary branch *are* 19). All three follow part-05 in teaching order, leaning on
`14-em-waves` and `16-light-in-matter` as built modules.

`interfaces.py` lands incrementally with its owners: file, docstring model spec, and the
geometry functions (`snell_angle`, `critical_angle`, `brewster_angle`) with 17; the four
`fresnel_*` plus `reflectance`/`transmittance` and their conservation/limit tests with
18; `penetration_depth`, `evanescent_field`, `ftir_transmission` and the TIR/FTIR tests
with 19. Later parts cite these guarantees (24, 26, 46, 47), so the §4 tests must land
*with* their functions, not after.

With 17, deposit the §5.1 glossary terms; with 18, add `brewster-no-transmission` to
`assessment/misconceptions.yml` (status `pending` until the page's falsifier and
distractor exist, then `addressed`); with 19, likewise `tir-zero-field`. No registry
re-pointings belong to this part (README conflict log: `frequency-changes-in-medium`
re-points to 16 with part-05's build, not here).

Per module: the standard four gates (README bottom) with the module id.

## 8. Deviations from the master plan

- **Merge (6.2 + 6.3 → `18-fresnel`):** Brewster's angle is the zero of the $r_p$
  curve — a separate Brewster notebook would redraw the same four Fresnel plots to add
  one marker. Merged, the angle appears where it lives: on the curve. Precedent:
  `02-damped-driven` ← 1.2 + 1.3 (README canonical map already records this merge).
- **Fermat demoted from coequal route to trailer (17):** the master plan lists three
  derivations unranked; this plan ranks them and gives Fermat a taste only —
  `33-fermat` owns the variational machinery.
- **Phase matching elevated to the part's organizing principle:** an enhancement, not a
  contradiction — it is the only route that generalizes (gratings, evanescence,
  frequency invariance), and the forward links become explicit content.
- **Sign convention fixed by fiat (18):** the master plan is silent; this plan pins
  Hecht's $r_p$ (Griffiths differs by a sign at normal incidence), names the
  discrepancy in a boxed admonition, and enforces it with a unit test.
- **Quantitative FTIR (19):** the master plan lists frustrated TIR as an explore
  bullet; this plan promotes it to a specified function (`ftir_transmission`), a
  two-route measurement of $\delta$, and the falsifier of a new registry misconception.
- **Teleology handled in prose (17):** "light seeks the fastest path" is treated as a
  language habit in prose and an explain question, not a registry misconception — it
  lacks a falsifier distinct from the Fermat demonstration itself.
- **Additions beyond the master plan:** the string-junction unification box (18); the
  conservation program ($R + T = 1$ with flux factors as test, lab cell, and quiz
  trap); two new registry misconceptions (`brewster-no-transmission`,
  `tir-zero-field`); the Snell's-window photo experiment; the TIR energy-flow audit.
