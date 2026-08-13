# Part XII — Gaussian Beams, Lasers, and Photonics — Implementation Plan

> **Master plan:** §19 (Part XII). **Modules:** `43-gaussian-beams`, `44-resonators`, `45-lasers`, `46-waveguides`, `47-fibers`. **Status:** planned.
> Canonical numbering, invariants, and conflict log: [README.md](README.md).

## 1. Part overview and narrative arc

Part XII is the course's synthesis. Nothing in it is a new kind of physics; everything
in it is an earlier structure returning on real hardware. The phasor habit of
`00-phasors` — pack two real numbers into one complex number and let arithmetic do the
work — returns as the beam parameter $q$, which packs spot size and wavefront curvature
into one complex number and propagates through optics by the *same* ABCD matrices as
rays. The oscillator's $Q$ — one number, three lab coats, planted in `02-damped-driven`
and reunited in optics in `26-fabry-perot` — makes its **third appearance** as the
photon-storage quality of a laser cavity, and the plan says so in exactly those words.
The mechanical normal modes of `07-normal-modes`, whose boxed motif promised "mechanical
normal modes ↔ optical cavity modes", are paid off literally: the Hermite–Gauss
transverse modes of module 44 are the cavity's normal modes, with node counting the
student already knows from the string. The Fabry–Pérot of module 26 gets gain and
becomes a laser. The total internal reflection and evanescent tails of `19-evanescent`
stop being a curiosity and start carrying the internet. And the packet-spreading law of
`12-wave-packets` / `13-dispersion` cashes in on real infrastructure: chromatic
dispersion is the reason a fiber link has a maximum bit rate × distance.

The arc runs from light shaped, to light stored, to light created, to light delivered.
**43** answers the question Part IX left open — what does a *real*, finite beam do in
free space? — with the Gaussian beam as the paraxial wave equation's fundamental
solution: waist, Rayleigh range, divergence as the **bandwidth theorem in space** (its
third appearance, after `04-fourier-transform` in time and `29-fraunhofer` on a screen —
the plan requires the page to say so), the Gouy phase *explained* rather than stated,
and the $q$-parameter riding part-10's ABCD matrices through lens systems. **44** closes
the loop: a cavity is a beam that must reproduce itself after a round trip, and that
self-consistency delivers the stability condition $0 \le g_1 g_2 \le 1$, the mode
geometry, longitudinal modes as module 26's Airy comb, and transverse modes whose
frequencies are shifted by 43's Gouy phase — degenerate at confocal, a designed
discovery. **45** puts atoms between the mirrors: Einstein coefficients, rate equations,
the classic two-level trap, threshold as gain = loss, gain clamping above threshold, and
the payoff of the course's oldest promise — module 00's violinists, whose "$N$ versus
$N^2$ … is the entire engineering case for the laser" line is kept on this module's
page, with a coherence-length measurement as the falsifier that a laser is not a bright
lamp. **46** turns the mirror pair sideways: a guided mode is a plane wave zig-zagging
under TIR whose transverse round-trip phase closes on itself — the standing-wave
quantization of `11-standing-waves`, transverse now. **47** rolls the slab into a
fiber and asks the engineering question: how much information can glass carry, and what
stops it? Dispersion is the villain, `em.group_index` and `waves.spreading_time` are the
weapons, and the optical-communication capstone (§35.4) is seeded explicitly.

Relative to master plan §19 the plan deepens each notebook with the machinery the
earlier parts built: notebooks 12.1 and 12.2 are **merged** into `43-gaussian-beams`
(the $q$-parameter *is* the propagation story; §8), the laser module is semiclassical
by design with the quantum description explicitly deferred to `52-quantum-optics`, the
waveguide module derives its modes by transverse resonance rather than asserting them,
and the fiber module carries real numbers — loss windows, dispersion parameters,
bit-rate limits — so the course ends touching the hardware of the present.

The textbook baton passes one last time: Hecht and Goodman hand over to **Saleh &
Teich** (companion for all five modules; chapter topics in §3) with **Siegman** as the
depth reference for beams and resonators. One convention flag runs through the whole
part: Siegman and much of the laser literature write $e^{+\ii\omega t}$, so their
$q = z + \ii z_R$ is the complex conjugate of the course's $q = z - \ii z_R$ (course
convention $e^{-\ii\omega t}$, forward phase $e^{+\ii k z}$). The sign contract is fixed
once in §4, boxed in 43's derive section, pinned by a unit test, and logged in §8 —
students reading Siegman must not get burned, and the lint must not fire.

## 2. Position in the course

- **Requires:**
  - `00-phasors`: the complex-amplitude habit (the $q$-parameter is a phasor for beam
    geometry); the random-phase walk and the $N$ vs $N^2$ violinists via
    `phasors.random_phasor_sum` — module 45's inheritance.
  - `02-damped-driven` / `05-impulse-response`: $Q$ three ways (`q_from_ringdown`,
    `q_from_bandwidth`, `q_from_phase_slope` — cited by name in 44's Q reunion); the
    Lorentzian; rate-of-change reasoning for rate equations.
  - `04-fourier-transform`: the bandwidth theorem $\Delta t\,\Delta\omega \ge \tfrac12$
    (43 restates it in space) and `fourier.rms_widths`.
  - `07-normal-modes`: the boxed "mechanical normal modes ↔ optical cavity modes"
    motif (44 closes it); node counting; `11-standing-waves`: the quantization-by-
    boundary-conditions argument (46 replays it transversely).
  - `12-wave-packets` / `13-dispersion`: `waves.group_velocity`,
    `waves.spreading_time`, `waves.propagate_dispersive`, `waves.gaussian_packet`
    (47's pulse engine, reused as-is per part-04's feed note); the packet-spreading
    law $\sigma(t)$ whose mathematics *is* 43's $w(z)$ (part-04 says so; 43 says it
    back).
  - `14-em-waves` / `16-light-in-matter`: plane waves; `em.refractive_index`,
    `em.sellmeier`, `em.group_index` (47's material database);
    `em.intensity_from_amplitude` (45's intensity bookkeeping).
  - `18-fresnel` / `19-evanescent`: s/p bookkeeping (46's TE/TM); Brewster windows
    (45's transfer, promised by 18); `interfaces.critical_angle`,
    `interfaces.penetration_depth`, `interfaces.evanescent_field`,
    `interfaces.ftir_transmission` and the TIR phase shifts (46's transverse-resonance
    input, 47's NA).
  - `26-fabry-perot`: `interference.airy_transmission`, `interference.finesse`,
    `interference.fsr`, `interference.fp_linewidth`, `interference.airy_coefficient`
    — the cavity of 44 *is* this instrument with curvature, and its transfer bullet
    ("a laser is this cavity with gain") is the promise 45 keeps.
  - `27-coherence`: `interference.coherence_length`, `interference.coherence_time`,
    `interference.degree_of_coherence`, `interference.visibility`,
    `interference.partial_coherence_source` — 45's falsifier machinery and the
    vocabulary for "why laser light is different".
  - `29-fraunhofer` / `32-fresnel-diffraction` (dictated names only):
    `diffraction.fraunhofer_pattern` (the far-field reflex),
    `diffraction.angular_spectrum_propagate` (43's numerical cross-check and the
    honest engine behind the Gouy-phase explanation).
  - `35-abcd-matrices` (dictated names only): `rayoptics.free_space`,
    `rayoptics.thin_lens`, `rayoptics.mirror`, `rayoptics.cascade` — 43 propagates
    $q$ through exactly these matrices; 44 builds round trips from them.
  - `39-fourier-lens` (part-11): quadratic-phase reflexes (43 inherits them, per
    part-11's feed note).
- **Feeds:**
  - `50-holography` / `51-nonlinear-optics` / `52-quantum-optics` /
    `54-photonic-crystals` / `55-ultrafast`: Gaussian-beam and cavity literacy is the
    entry ticket to every photonics elective; 45's Schawlow–Townes and frequency-comb
    research boxes are 52's and 55's front doors; 46's coupled waveguides seed 54;
    47's soliton teaser is 51's.
  - Capstone §35.4 (optical communication system): laser (45) → modulator → fiber
    (47) → dispersion (47 via part-04's propagator) → detector — seeded explicitly in
    47's §5.5 and §6.
  - Capstone §35.2 (virtual optical bench): Gaussian-beam propagation and cavity
    alignment as bench engines alongside part-10's rays and part-11's fields.
- **Explicitly not assumed:** quantum optics (photons appear only as $h\nu$ energy
  quanta in rate equations; field quantization, $g^{(2)}$, and cavity QED are
  `52-quantum-optics`); full vector waveguide theory (LP-mode algebra stated, not
  derived; the slab is scalar-per-polarization via TIR phases); nonlinear optics
  (solitons and SHG are teasers for `51-nonlinear-optics`); laser dynamics beyond
  steady state and small perturbations (relaxation oscillations are one advanced
  aside; mode locking is `55-ultrafast`); thermal and mechanical engineering of real
  lasers.

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|
| `43-gaussian-beams` | `content/en/photonics/43-gaussian-beams.md` | Gaussian beams and the q-parameter | 12.1 + 12.2 | Saleh & Teich, beam optics; Siegman, wave optics and Gaussian beams | planned |
| `44-resonators` | `content/en/photonics/44-resonators.md` | Optical resonators: stability and modes | 12.3 | Saleh & Teich, resonator optics; Siegman, stable two-mirror resonators | planned |
| `45-lasers` | `content/en/photonics/45-lasers.md` | Lasers: gain, threshold, and clamping | 12.4 | Saleh & Teich, laser amplifiers and lasers; Siegman, laser pumping and oscillation | planned |
| `46-waveguides` | `content/en/photonics/46-waveguides.md` | Waveguides: light confined by resonance | 12.5 | Saleh & Teich, guided-wave optics (planar waveguides) | planned |
| `47-fibers` | `content/en/photonics/47-fibers.md` | Optical fibers: modes, dispersion, and bit rates | 12.6 | Saleh & Teich, fiber optics; fiber-communication chapter for the link numbers | planned |

## 4. Shared infrastructure for this part

**`src/wavelab` — existing used:** `phasors.random_phasor_sum` (45's $N$ vs $N^2$
figures); `oscillators.q_from_ringdown` / `q_from_bandwidth` / `q_from_phase_slope`
(44's Q-three-ways reunion — by name only, owned by part-01);
`fourier.rms_widths` (43's uncertainty product), `fourier.spectrum` (45's linewidth
cells); `waves.propagate_dispersive`, `waves.gaussian_packet`, `waves.group_velocity`,
`waves.spreading_time`, `waves.envelope_rms_width` (47's pulse engine — by name, owned
by part-03/04); `em.sellmeier`, `em.refractive_index`, `em.group_index` (47's material
dispersion), `em.intensity_from_amplitude` (45); `interfaces.critical_angle`,
`interfaces.penetration_depth`, `interfaces.evanescent_field`,
`interfaces.ftir_transmission`, `interfaces.fresnel_rs` / `fresnel_rp` evaluated beyond
critical (46's TIR phases — by name, owned by part-06); `interference.airy_transmission`,
`airy_coefficient`, `finesse`, `fsr`, `fp_linewidth` (44's longitudinal modes),
`interference.coherence_length`, `coherence_time`, `degree_of_coherence`, `visibility`,
`partial_coherence_source` (45's falsifier); `diffraction.fraunhofer_pattern`,
`diffraction.angular_spectrum_propagate` (dictated names, part-09 — 43's cross-checks);
`rayoptics.free_space`, `thin_lens`, `mirror`, `cascade` (dictated names, part-10 —
consumed by `propagate_q` / `beam_through_system` / round trips);
`measurement.add_noise` and fit helpers (all five labs); `validation.scaling_exponent`,
`convergence_study`, `seed_study`, `relative_error`.

**`src/wavelab` — new file 1: `gaussian.py`** (introduced and owned by this part;
README ownership table — serves 43–44). Docstring model spec:

- **System:** paraxial monochromatic scalar Gaussian beams in uniform media, described
  by the complex beam parameter $q$; two-mirror standing-wave cavities described by
  $(L, R_1, R_2)$; observables are spot size, wavefront curvature, Gouy phase,
  transverse mode fields, stability margins, and mode frequencies.
- **Dynamics:** none integrated — closed-form beam laws and ABCD algebra; cavities are
  solved as fixed points of the round-trip map, never time-stepped.
- **Boundary:** free space and thin ideal elements (matrices from `rayoptics`); mirrors
  are ideal phase surfaces — losses, apertures, and gain belong to `photonics.py` and
  `interference.py`.
- **Ensemble:** deterministic; the knife-edge simulator draws seeded Gaussian noise via
  `wavelab.measurement` conventions.
- **Ignored:** polarization; aberrations and non-quadratic phase; vector and high-NA
  corrections; misalignment (tilt/decenter) beyond the stability discussion; thermal
  lensing.
- **Valid when:** paraxial ($\theta \lesssim 0.3$ rad, $w_0 \gtrsim \lambda$); elements
  thin and aligned; the cavity is used within its stability region.
- **Failure modes:** the conjugate-$q$ sign error (Siegman's $e^{+\ii\omega t}$ pages;
  the sign contract below); waists below $\sim\lambda$ read literally; stability-margin
  claims at exactly $g_1 g_2 \in \{0, 1\}$ (marginal cases are physics, not bugs);
  Hermite–Gauss formulas applied to unstable resonators.

**Sign contract (fixed here, boxed in 43, tested):** under the course convention
($e^{-\ii\omega t}$, forward factor $e^{+\ii k z}$) the fundamental beam carries the
transverse phase $e^{+\ii k r^2/(2q)}$ with

$$
q(z) = z - \ii z_R, \qquad
\frac{1}{q} = \frac{1}{R(z)} + \ii\,\frac{\lambda}{\pi w^2(z)} ,
$$

so that $\Imag(q) < 0$ for a physical (decaying) beam, and the on-axis phase is
$k z - \psi(z)$ with Gouy phase $\psi = \arctan(z/z_R)$. Siegman's and Saleh & Teich's
$e^{+\ii\omega t}$ convention gives the complex conjugate, $q = z + \ii z_R$ and
$1/q = 1/R - \ii\lambda/(\pi w^2)$ — same physics, conjugate bookkeeping. The ABCD
propagation law is real-coefficient and holds verbatim in both conventions. A limits
test pins $\Imag(q_{\text{parameter}}) < 0$ and the round-trip consistency of the
conjugate dictionary.

Function-level sketch (signatures + contracts):

```python
rayleigh_range(w0, lam) -> zR              # pi w0^2 / lam [m]
waist(z, w0, lam) -> w                     # w0 sqrt(1 + (z/zR)^2); the hyperbola
curvature_radius(z, w0, lam) -> R          # z (1 + (zR/z)^2); inf at z = 0 (returned as inf)
divergence(w0, lam) -> theta               # lam / (pi w0) [rad], far-field half-angle;
                                           #   theta * w0 = lam/pi — the invariant the tests pin
gouy_phase(z, w0, lam) -> psi              # arctan(z / zR); -pi/2 -> +pi/2 across the focus
q_parameter(z, w0, lam) -> q               # z - i zR (course sign; contract above)
q_from_w_R(w, R, lam) -> q                 # inverts 1/q = 1/R + i lam/(pi w^2)
w_R_from_q(q, lam) -> (w, R)               # spot size and curvature read off one complex number
propagate_q(q, abcd) -> q2                 # (A q + B) / (C q + D); abcd is any 2x2 from rayoptics
beam_through_system(q0, *elements) -> q    # folds propagate_q over rayoptics matrices given in
                                           #   the order light MEETS them (rayoptics.cascade contract)
field_amplitude(r, z, w0, lam) -> E        # full complex fundamental mode: 1/q prefactor,
                                           #   e^{+i k r^2/(2q)}, Gouy included; |E|^2 integrates to
                                           #   constant power at every z (the conservation contract)
hermite_gauss_mode(m, n, x, y, z, w0, lam) -> E
                                           # HG_mn field with (m+n+1) Gouy factor; orthonormal set
cavity_g(L, R1, R2) -> (g1, g2)            # g_i = 1 - L/R_i; resonator sign convention (concave
                                           #   mirror facing the cavity: R > 0) — the dictionary to
                                           #   rayoptics.mirror's Hecht sign (R_hecht = -R_res) is
                                           #   applied internally where round trips are built
cavity_stability(g1, g2) -> margin         # g1*g2 clipped report: stable iff 0 <= g1 g2 <= 1;
                                           #   returns the product (the margin the diagram plots)
stability_map(g1_grid, g2_grid) -> mask    # boolean stability region for the module's map
cavity_mode(L, R1, R2, lam) -> (w0, z1, z2)# self-consistent q: waist size and position (distances
                                           #   from mirror 1); ValueError outside stability
round_trip_abcd(L, R1, R2) -> M            # cascade(free_space, mirror, free_space, mirror) with
                                           #   the sign dictionary applied; trace test: |A+D| <= 2
                                           #   iff 0 <= g1 g2 <= 1
mode_frequencies(L, R1, R2, q_max, mn_max) -> nu
                                           # nu_{q,mn} = fsr * (q + (m+n+1) * arccos(s*sqrt(g1 g2))/pi),
                                           #   s = sign(g1); cites interference.fsr for the prefactor
knife_edge_scan(edge_positions, w, power=1.0, noise=0.0, seed=None) -> P
                                           # P(x) = (power/2) erfc(sqrt(2) x / w) + seeded noise —
                                           #   the lab's synthetic instrument
waist_fit(z_positions, w_measured, lam, sigma_w=None) -> (w0, z0, errors)
                                           # least-squares hyperbola fit; the measurement engine
                                           #   behind 43's "waist location +/- error" result
```

**`src/wavelab` — new file 2: `photonics.py`** (introduced and owned by this part;
README ownership table — serves 45–47). Docstring model spec:

- **System:** laser gain media as two-, three-, or four-level population models coupled
  to one cavity mode (photon-number description); symmetric step-index slab waveguides
  $(n_1, n_2, d)$; step-index fibers $(n_1, n_2, a)$; observables are populations,
  photon numbers, output powers, mode counts, effective indices, delay spreads, and bit
  rates.
- **Dynamics:** rate equations (ODEs in populations and photon number) integrated
  explicitly; everything else algebraic (mode conditions solved by bracketed
  root-finding).
- **Boundary:** the cavity enters as a photon lifetime / loss rate (from module 44's
  quantities); waveguide claddings are semi-infinite; fibers are weakly guiding
  ($\Delta \ll 1$).
- **Ensemble:** deterministic; measurement noise via `wavelab.measurement` in labs;
  spontaneous emission enters the rate equations as a mean seed term, not a stochastic
  process (semiclassical scope).
- **Ignored:** field quantization and photon statistics (52); spatial hole burning and
  multimode competition (one advanced aside); gain dispersion beyond a single
  Lorentzian line; fiber nonlinearity (51); polarization-mode dispersion; bend and
  splice losses beyond a lumped dB budget.
- **Valid when:** photon numbers large enough for mean-field rate equations; pump
  near-steady; slab and fiber weakly guiding and single-wavelength per call; bit-rate
  estimates read as order-of-magnitude engineering bounds.
- **Failure modes:** two-level "inversion" (the model itself forbids it — the classic
  trap, pinned by a limits test); rate equations trusted at threshold's critical
  fluctuations; $V^2/2$ mode counting near $V \approx 2.405$; dispersion formulas
  applied across the zero-dispersion wavelength without sign care.

Function-level sketch (signatures + contracts):

```python
rate_equations(scheme, pump_rate, t, tau_upper, tau_lower=0.0, sigma=None,
               photon_lifetime=None, beta=1e-6) -> (N_levels, phi)
                                           # scheme in {"two", "three", "four"}; integrates
                                           #   populations (+ photon number phi when a cavity is
                                           #   coupled); spontaneous seed beta * N_upper / tau_upper
steady_state_inversion(scheme, pump_rate, tau_upper, tau_lower=0.0) -> dN
                                           # closed form per scheme; "two" returns dN <= 0 for ALL
                                           #   pump rates — the impossibility is the contract
gain_coefficient(dN, sigma) -> g           # g = sigma * dN [1/m]
cavity_loss_rate(L, R1, R2, alpha_int=0.0, n=1.0) -> gamma_c
                                           # c/(2 n L) * ln(1/(R1 R2)) + c * alpha_int / n [1/s];
                                           #   1/gamma_c is module 26/44's photon lifetime
threshold_pump(scheme, gamma_c, sigma, tau_upper, mode_volume_factor=1.0) -> p_th
                                           # pump rate where steady-state gain equals loss
output_vs_pump(pump_rate, p_th, slope_efficiency) -> P_out
                                           # ~0 below p_th (spontaneous floor), slope * (p/p_th - 1)
                                           #   above — the knee the lab measures through noise
clamped_inversion(pump_rate, p_th, dN_th) -> dN
                                           # min(dN_free_running, dN_th): flat above threshold
tir_phase(n1, n2, theta, pol) -> phi       # TIR phase shift at angle theta (> critical), from the
                                           #   interfaces Fresnel coefficients; pol in {"TE", "TM"}
slab_mode_condition(theta, n1, n2, d, lam, m, pol) -> residual
                                           # transverse resonance: 2 k0 n1 d cos(theta)
                                           #   - 2 phi_TIR(theta) - 2 pi m; zero at a guided mode
slab_modes(n1, n2, d, lam, pol="TE") -> (n_eff, theta)
                                           # all guided modes by bracketed bisection on the
                                           #   condition; n_eff = n1 sin(theta), n2 < n_eff < n1
slab_mode_count(n1, n2, d, lam) -> int     # ceil(2 d sqrt(n1^2 - n2^2) / lam) — TE count, tested
                                           #   against len(slab_modes)
slab_mode_profile(x, n_eff, n1, n2, d, lam) -> u
                                           # cos/sin core + exponential cladding tails (matched);
                                           #   decay rate consistent with interfaces.penetration_depth
numerical_aperture(n1, n2) -> na           # sqrt(n1^2 - n2^2); meridional acceptance from
                                           #   interfaces.critical_angle geometry (derived in 47)
acceptance_angle(n1, n2, n0=1.0) -> theta  # arcsin(na / n0), the half-cone the lab measures
v_number(a, lam, na) -> V                  # 2 pi a * na / lam; single-mode iff V < 2.405
mode_count(V) -> N                         # ~ V^2 / 2 (step-index estimate); returns 1 for V < 2.405
modal_delay_spread(L, n1, delta) -> dt     # L n1 delta / c [s], step-index worst case;
                                           #   delta = (n1 - n2)/n1
chromatic_broadening(L, D, dlam) -> dt     # |D| * L * dlam; D in s/m^2 with a ps/(nm km)
                                           #   convenience conversion documented against `units`
dispersion_parameter(lam, n_of_lam) -> D   # -(lam / c) * d2n/dlam2 (material part), numerical
                                           #   second derivative; callers pass em.sellmeier closures
bit_rate_limit(dt, scheme="NRZ") -> B      # ~ 1/(4 dt) engineering bound [bit/s]; the honest
                                           #   quarter-of-a-slot rule, stated as such
```

**`tests/physics/` additions:**

- *limits:* `beam_through_system(q0, free_space(z))` reproduces `waist(z)` and
  `curvature_radius(z)` closed forms to $10^{-12}$ (q-propagation vs the hyperbola);
  `hermite_gauss_mode(0, 0, ...)` ≡ `field_amplitude`; `Imag(q_parameter(...)) < 0`
  pinned (the sign contract); symmetric confocal `cavity_mode` gives
  $w_0 = \sqrt{\lambda L / 2\pi}$ exactly; `round_trip_abcd` trace satisfies
  $|A + D| \le 2 \Leftrightarrow 0 \le g_1 g_2 \le 1$ across a $(g_1, g_2)$ sweep;
  `steady_state_inversion("two", ...)` $\le 0$ for pump rates spanning 8 decades (the
  impossibility test); `output_vs_pump` → spontaneous floor below threshold, linear
  above; `mode_count(V)` = 1 for $V < 2.405$; `slab_mode_count` = 1 below the first
  cutoff and matches `len(slab_modes)` across a $d/\lambda$ sweep;
  `slab_mode_profile` cladding decay length equals `interfaces.penetration_depth` at
  the mode angle; `mode_frequencies` transverse spacing → FSR/2 at confocal
  (degeneracy pinned).
- *conservation:* transverse power integral of `field_amplitude` and of every
  `hermite_gauss_mode` constant in $z$ to $10^{-8}$ (lossless propagation, and through
  a lossless `thin_lens` system); `knife_edge_scan` at zero noise spans the full power
  monotonically ($P(-\infty) = $ power, $P(+\infty) = 0$); photon-number balance in
  `rate_equations`: pump in = photons out + spontaneous + population change, per step.
- *convergence:* `slab_modes` roots vs a dense-grid sign-scan reference (every root
  found, none spurious, error → 0 with grid refinement); `rate_equations` integrator
  error $\propto \Delta t^2$ against the closed-form four-level steady state;
  `dispersion_parameter`'s numerical second derivative error $\propto d\lambda^2$.
- *scaling:* fitted exponents via `validation.scaling_exponent`: `divergence` $\propto
  \lambda^{+1} w_0^{-1}$; focused waist through `thin_lens(f)` $\propto f^{+1}$ for a
  collimated input; `modal_delay_spread` $\propto L^{+1} \Delta^{+1}$;
  `chromatic_broadening` $\propto L^{+1} \Delta\lambda^{+1}$; slab mode count slope
  $\propto d/\lambda$.
- *seeds:* `knife_edge_scan` reproducible per seed; `waist_fit` on noisy scans across
  $M$ seeds — mean within uncertainty of truth, scatter $\propto 1/\sqrt{M}$;
  threshold-knee location fitted from noisy `output_vs_pump` data stable across seeds.
- *dimensions:* `rayleigh_range` in m, `divergence` in rad, `cavity_loss_rate` in 1/s,
  `mode_frequencies` in Hz, `modal_delay_spread` / `chromatic_broadening` in s,
  `bit_rate_limit` in 1/s — against the `units` registry, including the
  ps/(nm·km) ↔ s/m² conversion documented in `chromatic_broadening`.

**Shared media:** two render scripts mirroring the two library files:
`media/render/render_gaussian.py` (modules 43–44 MP4s) and
`media/render/render_photonics.py` (modules 45–47 MP4s); shot lists in §5.
**Glossary themes:** beam vocabulary (43), resonator vocabulary (44), laser vocabulary
(45), guided-wave vocabulary (46), fiber and communication vocabulary (47) — per-module
lists in §5. `numerical-aperture` is deposited by `36-instruments` (part-10); module 47
adds the fiber usage to the same key as a citation.

## 5. Module specifications

### 5.1 `43-gaussian-beams` — Gaussian beams and the q-parameter

- **Identity and scope:** master-plan notebooks 12.1 + 12.2, merged (§8): beam
  parameters and their propagation through optical systems are one calculus — the
  $q$-parameter — and splitting them would teach half a tool twice. Deferred: cavities
  and self-consistency → `44-resonators`; apertures and diffraction loss → problem-set
  mention only; higher-order-mode *physics* beyond patterns and Gouy factors →
  `44-resonators` (frequencies) and part-13.
- **Prerequisites:** `35-abcd-matrices` (`rayoptics.free_space`, `thin_lens`,
  `cascade` and their conventions); `32-fresnel-diffraction`
  (`diffraction.angular_spectrum_propagate`, $k_z \approx k - k_\perp^2/2k$);
  `04-fourier-transform` (Gaussian ↔ Gaussian pair, `fourier.rms_widths`, the
  bandwidth theorem); `29-fraunhofer` (far field ∝ transform; `airy_radius` and
  `rayleigh_criterion` for the focused-spot bridge); `00-phasors` (complex packing).
- **Learning objectives:**
  - `OBJ-43-1` — State the paraxial wave equation 2 i k du/dz + (d2u/dx2 + d2u/dy2) = 0
    as an approximation to the Helmholtz equation, identify the Gaussian beam as its
    fundamental solution, and compute w(z) = w0 sqrt(1 + (z/zR)^2) with
    zR = pi w0^2 / lambda.
  - `OBJ-43-2` — Compute wavefront curvature R(z) = z (1 + (zR/z)^2) and far-field
    divergence theta = lambda/(pi w0), and state w0 * theta = lambda/pi as the
    bandwidth theorem in space (equality case of the module-04 inequality).
  - `OBJ-43-3` — Explain the Gouy phase psi(z) = arctan(z/zR) as the axial-wavenumber
    deficit of a transversely confined beam, and predict the total pi phase slip
    through a focus.
  - `OBJ-43-4` — Pack w and R into 1/q = 1/R + i lambda/(pi w^2), propagate
    q' = (A q + B)/(C q + D) through ABCD systems, and compute the waist produced by a
    lens, including the collimated-input limit w0' ~ lambda f/(pi w_in).
  - `OBJ-43-5` — Design a two-lens mode-matching system to place a target waist at a
    target location, and extract w0 and the waist position with uncertainties from
    noisy knife-edge scans.
  - `OBJ-43-6` — (advanced) Use the M^2 factor to describe real beams: divergence
    M^2 times the ideal at the same waist, and fit M^2 from w(z) data.
- **Mathematical background:** has — complex Gaussians and completing the square (04),
  ABCD matrices (35), quadratic-phase reflexes (39); introduced here — the slowly
  varying envelope, the complex beam parameter, Hermite polynomials (used, not
  derived).
- **Physical intuition goals:** (1) squeeze the waist and the cone opens — collimation
  is *bought* with width, never free; (2) a beam is "flat" for $\pm z_R$ and cone-like
  after — one number tells you which regime you are in; (3) a lens cannot focus a beam
  to a point: the focal spot is $\lambda f/(\pi w_{\text{in}})$, so a *bigger* input
  beam focuses *smaller*; (4) the far field of a Gaussian is a Gaussian — the one
  aperture with no rings.
- **Section skeleton seeds:**
  - *puzzle:* a laser pointer's spot barely grows across a lecture hall, yet no
    lens anywhere in it is "focused at infinity" — while the same pointer *cannot* be
    focused to a point by any lens, however perfect. (Boxed: what law relates how
    narrow a beam is to how fast it must spread — and what exactly does a laser beam
    look like near its narrowest point?)
  - *predict:* (1) halve the waist — divergence doubles, halves, or unchanged?
    (2) can a perfect lens focus a laser to a geometric point? (targets
    `perfect-lens-focuses-to-point`) (3) where along the beam is the wavefront most
    curved — at the waist, at $z_R$, or far away? (4) a beam and a plane wave start in
    phase at the focus: after passing through it, is the beam ahead, behind, or in
    phase?
  - *explore:* beam explorer — $w_0$, $\lambda$ sliders; live hyperbola $w(z)$ with
    asymptotes, wavefront arcs, $z_R$ brackets, on-axis phase-vs-plane-wave meter (the
    Gouy readout); lens bench — drag `thin_lens` elements along the axis, watch $q$
    propagate (complex-plane inset showing $q$ in the lower half-plane) and the
    hyperbola re-form after each element.
  - *derive:* Helmholtz → paraxial (`approximation` box with validity) → the $q$
    ansatz $u = (1/q)\,e^{+\ii k r^2/(2q)}$, $dq/dz = 1$ → unpacking $q = z - \ii z_R$
    into $w(z)$, $R(z)$, Gouy (the §4 sign contract, boxed) → divergence and the
    bandwidth theorem in space (equality case; **third appearance, said so**) → Gouy
    phase from the angular spectrum ($k_z$ deficit, integral done) → ABCD law for $q$
    (proved for `free_space` and `thin_lens`, composed by `cascade`) → lens
    transformation of a waist → mode matching with two lenses → knife-edge integral
    $P(x) = (P_0/2)\,\mathrm{erfc}(\sqrt{2}\,x/w)$.
  - *verify:* `beam_through_system` vs `waist`/`curvature_radius` closed forms
    (machine precision); `angular_spectrum_propagate` of a sampled waist reproduces
    $w(z)$ *and* the Gouy phase — the paraxial closed form checked against the honest
    propagator (the `numerical-observation` box: fitted phase slip $\pi$ to three
    digits); fitted divergence exponents $(+1, -1)$ in $(\lambda, w_0)$;
    `fourier.rms_widths` on the waist profile: $\sigma_x \sigma_{k_x} = 1/2$ exactly.
  - *transfer:* `44-resonators` (the beam that reproduces itself); `29-fraunhofer`
    backward (Gaussian's far field; `airy_radius` vs $\lambda f/(\pi w)$ — hard vs
    soft apertures); `12-wave-packets` (same $\sqrt{1 + (z/z_R)^2}$ law as
    $\sigma(t)$ spreading — part-04 promised it, 43 says it back); laser machining
    and optical tweezers (waist = tool size); `52-quantum-optics` (mode = the thing
    one photon occupies); free-space optical links.
  - *quiz:* $z_R$/divergence numerics; waist–divergence trade; Gouy totals; focused
    spot (registry distractor); knife-edge width extraction.
  - *explain:* why "collimated" is always temporary; the waist–divergence trade as a
    Fourier statement, no formulas; what the Gouy phase is *not* (not dispersion, not
    a medium effect); why doubling the input beam diameter halves the focal spot.
  - *advanced:* $M^2$ — real lasers as "Gaussian with a handicap", the embedded-
    Gaussian trick $w_0 \to w_0/M$, fitting $M^2$ honestly; the ISO knife-edge/second-
    moment caveats; higher-order HG patterns previewed (`hermite_gauss_mode` gallery)
    with node counting, frequencies deferred to 44. Safe to skip: 44 core needs only
    the fundamental mode.
- **Core derivations** (ordered): (1) paraxial reduction with the dropped
  $\partial_z^2 u$ term exhibited and bounded ($\theta^2/2$ relative). (2) $q$ ansatz:
  substituting $u = (1/q) e^{+\ii k r^2/(2q)}$ gives $dq/dz = 1$; with
  $q = z - \ii z_R$,
  $$E \propto \frac{w_0}{w(z)}\, e^{-r^2/w^2(z)}\,
  e^{+\ii\left[k z + \tfrac{k r^2}{2 R(z)} - \psi(z)\right]} e^{-\ii\omega t},$$
  $w$, $R$, $\psi$ as in the objectives — one complex first-order ODE replacing a PDE
  (the phasor habit, named). (3) Divergence: $w \to w_0 z/z_R$, so
  $\theta = \lambda/(\pi w_0)$ and $\sigma_x \sigma_{k_x} = 1/2$ — the Gaussian
  equality case of 04's theorem, third appearance after 04 (time) and 29 (aperture),
  and the appearance part-00's plan promised by name ("module 43's beam divergence").
  (4) Gouy: $k_z = \sqrt{k^2 - k_\perp^2} \approx k - k_\perp^2/2k$; averaging
  $\langle k_\perp^2\rangle = 2/w^2(z)$ over the beam and integrating the deficit
  $\int_0^z \langle k_\perp^2\rangle/(2k)\, dz' = \arctan(z/z_R)$ — transverse
  confinement *costs* axial phase; tighter focus, faster slip. (5) ABCD for $q$:
  free space $q \to q + d$; thin lens $1/q \to 1/q - 1/f$; both are
  $q \to (Aq+B)/(Cq+D)$, and matrix composition = map composition (`cascade`).
  (6) Waist through a lens: waist-at-lens case worked exactly; collimated limit
  $w_0' = \lambda f/(\pi w_{\text{in}})$ with its validity ($f \ll z_R^{\text{in}}$)
  stated. (7) Knife-edge: integrating the Gaussian gives the erfc form behind
  `knife_edge_scan` / `waist_fit`.
- **Model specification draft:** System — a monochromatic scalar paraxial beam in a
  uniform medium, fully described by $(w_0, z_{\text{waist}}, \lambda)$ — equivalently
  one complex $q$; observables: $w(z)$, $R(z)$, on-axis phase, knife-edge powers.
  Dynamics — none; closed forms and the algebraic ABCD map. Boundary — free space and
  thin ideal elements; no apertures. Ensemble — deterministic; knife-edge noise
  seeded via `wavelab.measurement`. Ignored — polarization, aberrations, misalignment,
  loss. Valid when — $\theta \ll 1$ ($w_0 \gtrsim \lambda$); elements paraxial and
  aligned. Failure modes — conjugated $q$ (sign contract); waists $\lesssim \lambda$
  read literally; hard apertures treated as if absent; $M^2 > 1$ beams fed to
  fundamental-mode formulas.
- **Epistemic classification:** paraxial equation — `approximation` (the boxed one,
  with the $\theta^2/2$ validity edge); Gaussian solution, ABCD-for-$q$, Gouy
  integral — `theorem` (within the paraxial model); $w_0\theta = \lambda/\pi$ —
  `theorem` (equality case of 04's theorem); angular-spectrum agreement and the
  measured $\pi$ slip — `numerical-observation`; $M^2$ — `definition` (an ISO metric,
  flagged as such).
- **Misconceptions:** NEW **`perfect-lens-focuses-to-point`** — "An ideal,
  aberration-free lens focuses a laser beam to a geometric point." Falsifying
  experiment: propagate $q$ through `thin_lens(f)` for perfect lenses of several $f$:
  the focal spot is $\lambda f/(\pi w_{\text{in}})$, never zero, and *shrinking* it
  requires a *bigger* input beam — the same $\Delta x\,\Delta k_x$ bill the aperture
  paid in 29/30 (`rayleigh_criterion` cited). Distractor: quiz option "with a
  sufficiently well-made lens the spot can be made arbitrarily small at fixed beam
  size".
- **Glossary terms:** `gaussian-beam` (אלומה גאוסית), `beam-waist` (מותן האלומה),
  `rayleigh-range` (טווח ריילי), `beam-divergence` (התבדרות אלומה), `gouy-phase`
  (מופע גואי), `q-parameter` (פרמטר q; `he_reject` candidate: הפרמטר המרוכב של
  האלומה — translator to decide), `mode-matching` (התאמת אופנים), `knife-edge-method`
  (שיטת סכין־המדידה — translator to confirm), `m-squared` (מקדם M²),
  `paraxial-approximation` (קירוב פרקסיאלי; `he_reject` candidate: קירוב צירי).
- **Interactive controls and simulations:** beam explorer ($w_0$ 0.05–5 mm, $\lambda$
  400–1600 nm, $z$ span ±10 $z_R$); lens bench (drag lenses, $f$ 25–500 mm, live $q$
  inset and hyperbola); knife-edge bench (edge position, $z$ station, noise level,
  re-roll seed); mode-match game: hit a target $(w_0', z')$ ring with two lenses.
- **Virtual lab outline** (`notebooks/en/labs/43-gaussian-beams.ipynb`): (1) explorer
  play, predictions checked; (2) *measurement:* synthetic knife-edge scans at ~8
  stations (`knife_edge_scan` with noise), erfc-fit each for $w$, then `waist_fit`
  → $w_0 \pm \sigma$, $z_0 \pm \sigma$ — the measurement-culture centrepiece;
  (3) divergence audit: fitted asymptote slope vs `divergence(w0, lam)`;
  (4) lens transform: predict the post-lens waist with `beam_through_system`, verify
  by re-scanning; the perfect-lens falsifier across $f$; (5) mode-match design task
  with tolerance analysis (waist-position error vs lens-spacing error — which knob is
  touchy); (6) advanced: fit $M^2$ on a synthetic HG-mixture beam.
- **Real-experiment counterpart:** a laser pointer down a corridor: photograph or
  trace the spot at 5–10 distances (graph paper on a wall), import widths, run the
  same `waist_fit` — $w_0$, $z_R$, and $\theta$ from hardware, $\theta$ vs
  $\lambda/(\pi w_0)$ compared with honest error bars (pointer $M^2 > 1$ noted).
- **Media assets** (`render_gaussian.py`): (a) the see-saw: $w_0$ sweeping down while
  the far-field cone opens — hyperbola and asymptotes, no text; (b) Gouy race: beam
  and plane-wave wavefronts through a focus, the accumulated slip highlighted, ending
  at $\pi$; (c) $q$-plane inset: the dot $q = z - \ii z_R$ translating, jumping under
  a lens, while the physical beam morphs alongside.
- **Quiz bank outline:** `Q-43-1` numeric — $z_R$ and $w$ at given $z$ (OBJ-43-1);
  `Q-43-2` MC — halve $w_0$, what happens to $\theta$ (OBJ-43-2); `Q-43-3` MC — total
  Gouy slip through a focus, and is it a medium effect (OBJ-43-3); `Q-43-4` numeric —
  waist after a given lens via $q$ (OBJ-43-4); `Q-43-5` MC — smallest achievable
  focal spot (OBJ-43-4, distractor `perfect-lens-focuses-to-point`); `Q-43-6` free —
  $w_0\theta = \lambda/\pi$ as a Fourier statement (OBJ-43-2); `Q-43-7` numeric —
  $w$ from a knife-edge 10–90% distance (OBJ-43-5).
- **Problem set outline:** analytical — verify the Gaussian solves the paraxial
  equation; derive $R(z)$ by comparing to a spherical wave; general waist-to-waist
  lens formulas; $\sigma_x\sigma_{k_x} = 1/2$ from the transform pair. Computational
  — `angular_spectrum_propagate` vs closed forms: error vs $\theta$ (where paraxial
  honestly dies); knife-edge fit bias vs noise level. Challenge — mode-match into
  44's cavity: two catalog lenses, tolerance budget, and a written "alignment
  procedure" (the capstone §35.2 seed).
- **Runtime budget:** all closed-form; angular-spectrum checks on $512^2$ grids,
  ≤ 10 FFTs — about a second in Pyodide; knife-edge cells trivial; animations ≤ 200
  frames.
- **Validation gates:** standard set with `--module 43-gaussian-beams`; the §4
  q-propagation limits, conservation, and knife-edge seed tests land with this
  module.
- **Open questions for the author:** whether the Gouy angular-spectrum derivation
  lives in core derive or advanced (recommendation: core, compressed to five lines —
  44's degeneracy needs it believed, not just quoted); whether the $q$-plane inset
  appears in the content page or lab only (recommendation: page — it is the phasor
  picture's return); whether to name "confocal parameter $b = 2z_R$" (recommendation:
  one parenthetical, Siegman readers will meet it).

### 5.2 `44-resonators` — Optical resonators: stability and modes

- **Identity and scope:** master-plan notebook 12.3. Two-mirror cavities: stability,
  mode geometry, longitudinal and transverse mode spectra. Deferred: gain and
  threshold → `45-lasers`; ring and multi-element cavities → problem set; mode
  locking → `55-ultrafast`; cavity QED → `52-quantum-optics`.
- **Prerequisites:** `43-gaussian-beams` ($q$, ABCD, Gouy phase);
  `26-fabry-perot` (`interference.airy_transmission`, `finesse`, `fsr`,
  `fp_linewidth`, photon lifetime); `02-damped-driven` ($Q$ three ways, cited names);
  `07-normal-modes` (normal modes, node counting, the boxed motif);
  `11-standing-waves` (quantization by boundary conditions);
  `35-abcd-matrices` (`rayoptics.mirror`, `cascade`).
- **Learning objectives:**
  - `OBJ-44-1` — Impose round-trip self-consistency q = (A q + B)/(C q + D) on a
    two-mirror cavity and derive the stability condition 0 <= g1 g2 <= 1 with
    g_i = 1 - L/R_i; place named cavities on the stability diagram.
  - `OBJ-44-2` — Compute the self-consistent mode geometry — waist size and position —
    of a stable cavity, and predict how it degenerates toward the stability
    boundaries.
  - `OBJ-44-3` — Compute the longitudinal-mode comb nu_q = q c/(2L), its FSR, the
    linewidth from mirror reflectivity, the photon lifetime, and the cavity Q by
    three equivalent measurements.
  - `OBJ-44-4` — Identify Hermite-Gauss patterns as the cavity's transverse normal
    modes, count their nodes, and compute
    nu_qmn = (c/2L) (q + (m + n + 1) arccos(+-sqrt(g1 g2))/pi).
  - `OBJ-44-5` — Predict and explain the transverse-mode degeneracy of the confocal
    cavity as a Gouy-phase effect.
- **Mathematical background:** has — $q$ calculus, ABCD, Airy machinery (26),
  eigen-language (07); introduced here — fixed points of a Möbius map (operationally:
  the self-consistency quadratic), the $(g_1, g_2)$ parametrization.
- **Physical intuition goals:** (1) a cavity does not store *any* beam — it stores
  the one beam whose diffraction the mirrors exactly undo; (2) the stability diagram
  is a map, and every laser you will ever meet lives at a point on it; (3) sharper
  mirrors → longer photon storage → narrower lines: $Q$ again, third time; (4) a
  transverse mode is a note — you can *count its nodes* in the output spot exactly as
  on the string.
- **Section skeleton seeds:**
  - *puzzle:* the mirrors in every real laser are curved, and a HeNe's beam emerges
    with a definite waist nobody dialed in. Two flat mirrors — the "obvious"
    resonator — are almost never used. (Boxed: what chooses the beam that comes out
    of a laser, and why do flat mirrors fail at the job?)
  - *predict:* (1) are two flat parallel mirrors a stable light trap? (targets
    `any-mirrors-make-cavity`) (2) two mirrors of focal-length-like curvature
    $R_1 = R_2 = L$ (confocal): nudge $L$ slightly longer — still stable? (3) what
    happens to the cavity waist as a stable cavity approaches its stability edge?
    (4) do the $\mathrm{TEM}_{00}$ and $\mathrm{TEM}_{01}$ modes of the same $q$
    share a frequency?
  - *explore:* the **stability diagram as the module's map** — drag a dot in the
    $(g_1, g_2)$ plane; live panels: cavity cartoon with the mode drawn to scale
    (`cavity_mode`), waist readout, and an escape animation (iterated `propagate_q`
    walking off) whenever the dot leaves the stable region; named cavities pinned
    (plane-plane $(1,1)$, confocal $(0,0)$, concentric $(-1,-1)$, hemispherical
    $(1,0)$); spectrum panel: the $\nu_{q,mn}$ ladder from `mode_frequencies` sliding
    as the dot moves — transverse satellites migrating between FSR teeth and
    collapsing onto them at special points.
  - *derive:* round trip via `round_trip_abcd` → self-consistency
    $q = (Aq+B)/(Cq+D)$ → quadratic $Cq^2 + (D-A)q - B = 0$ → confined solution
    ($\Imag q < 0$) exists iff $|A+D| \le 2$ → trace identity
    $(A + D + 2)/4 = g_1 g_2$ → $0 \le g_1 g_2 \le 1$ → mode geometry ($z_R$, waist
    position) → longitudinal comb: round-trip phase $2kL = 2\pi q$ → FSR $c/2L$ —
    **the cavity *is* module 26's Fabry–Pérot** (`interference.fsr`, promise kept),
    linewidth = FSR/finesse (`interference.finesse`, `fp_linewidth`) → photon
    lifetime → $Q = \omega\tau_p$, measured three ways (**third appearance of $Q$,
    said so**: `q_from_ringdown` on decay, `q_from_bandwidth` on the Airy line,
    `q_from_phase_slope` on transmitted phase) → transverse modes: HG$_{mn}$
    self-reproduce (shape-invariant under the round trip) — **the part-02 boxed
    motif closed explicitly**: these are the cavity's normal modes, nodes countable
    like the string's → round-trip Gouy phase $\Delta\psi =
    \arccos(\pm\sqrt{g_1 g_2})$ → $\nu_{q,mn}$ formula → confocal:
    $\Delta\psi = \pi/2$, transverse modes land exactly on half-FSR — massive
    degeneracy (the designed discovery); plane-plane and concentric edges:
    $\Delta\psi \to 0, \pi$ — degeneracy of a different kind, at the cliff.
  - *verify:* `round_trip_abcd` trace vs $g_1 g_2$ identity across a sweep;
    `cavity_mode` at symmetric confocal = $\sqrt{\lambda L/2\pi}$ exactly; iterated
    `propagate_q` converges to the `cavity_mode` fixed point inside stability and
    diverges outside — convergence rate vs stability margin (the
    `numerical-observation` box); `mode_frequencies` confocal degeneracy to machine
    precision; ringdown $\tau_p$ vs `fp_linewidth` (`q_from_ringdown` /
    `q_from_bandwidth` agreeing — the reunion measured).
  - *transfer:* `45-lasers` (gain into *this* mode structure — what lases is what
    fits); `26-fabry-perot` backward (curvature completes the instrument);
    `07-normal-modes` backward (motif closed — say it in the page);
    `24-thin-films` (the quarter-wave stack is how $R = 0.999$ exists →
    `54-photonic-crystals`); `55-ultrafast` (phase-lock the comb → pulses);
    `52-quantum-optics` (one atom + one of these modes = cavity QED, the §36 chain);
    LIGO's arm cavities (module 25's box, now with the machinery).
  - *quiz:* stability classification; waist numerics; FSR/linewidth numerics; node
    counting from a mode image; confocal degeneracy.
  - *explain:* why flat mirrors are marginal in principle and hopeless in practice
    (alignment as the physical reading of marginality); "the cavity mode is the beam
    whose diffraction the mirrors undo" in your own words; what exactly is
    degenerate at confocal and why the Gouy phase is the culprit.
  - *advanced:* unstable resonators used on purpose (high-power lasers take the
    walk-off as the output coupler — one honest paragraph, Siegman flagged);
    misalignment as motion on the diagram; ray picture of stability (the same
    $|A+D| \le 2$ from `rayoptics` orbits — one figure). Safe to skip: 45 needs
    only stability + loss.
- **Core derivations** (ordered): as in the seeds, with (1) the trace identity
  worked in two lines from `round_trip_abcd`'s entries; (2) the mode-geometry closed
  forms $z_R^2 = \dfrac{g_1 g_2 (1 - g_1 g_2)}{(g_1 + g_2 - 2 g_1 g_2)^2}\,L^2$ and
  waist position $z_1 = \dfrac{g_2(1 - g_1)}{g_1 + g_2 - 2 g_1 g_2}\,L$ (from mirror
  1), $w_0^2 = \lambda z_R/\pi$ — each checked against `cavity_mode`;
  (3) the resonance condition with Gouy correction: round-trip phase
  $2kL - 2(m{+}n{+}1)\,\Delta\psi = 2\pi q$ under the course convention
  $e^{+\ii k z}$, giving the $\nu_{q,mn}$ formula (sign of the square root follows
  $\operatorname{sign}(g_1)$ — contract of `mode_frequencies`); (4) photon lifetime
  $\tau_p = -t_{\text{rt}}/\ln(R_1 R_2)$ and $Q = \omega\tau_p$, tied to
  `interference.fp_linewidth` via $\delta\nu = 1/(2\pi\tau_p)$.
- **Model specification draft:** System — two spherical mirrors $(R_1, R_2)$ facing
  across $L$ in a uniform medium; observables: stability margin, mode geometry, mode
  frequencies, ringdown. Dynamics — none integrated; fixed points of the round-trip
  map (ringdown is the one transient, inherited from 26). Boundary — ideal
  phase-surface mirrors; loss only as a lumped reflectivity in lifetime formulas.
  Ensemble — deterministic. Ignored — gain, apertures and diffraction loss,
  misalignment beyond the stability discussion, mirror figure error, astigmatism.
  Valid when — paraxial mode ($w \ll$ mirror aperture), $0 \le g_1 g_2 \le 1$ for
  mode-geometry claims. Failure modes — geometry formulas at marginal points
  (denominators vanish — physics, handled); Hecht vs resonator mirror-sign mixups
  (`cavity_g`'s dictionary); HG mode formulas applied to unstable cavities.
- **Epistemic classification:** stability condition and mode geometry — `theorem`
  (within the paraxial model); "the cavity mode is the self-reproducing beam" —
  `definition` (boxed — it *defines* "mode" for the rest of the part);
  $\nu_{q,mn}$ formula — `theorem`; iterated-map convergence rates —
  `numerical-observation`; ideal-mirror model — `model-assumption` (loss lives in
  26's machinery); "unstable cavities are useless" — explicitly *false*, the
  advanced box (honesty note).
- **Misconceptions:** NEW **`any-mirrors-make-cavity`** — "Any two facing mirrors
  form a stable resonator — perfectly flat ones best of all." Falsifying experiment:
  iterate the round trip (`propagate_q`, and the ray twin) for plane-plane and for
  $g_1 g_2 > 1$ geometries: the field walks off; the stability map is *measured* by
  escape time, and plane-plane sits exactly on the marginal boundary where any tilt
  kills it. Distractor: quiz option "flat mirrors return each ray on itself, so they
  trap light best".
- **Glossary terms:** `optical-cavity` (מהוד אופטי), `cavity-stability` (יציבות
  מהוד), `stability-diagram` (דיאגרמת יציבות), `longitudinal-mode` (אופן אורכי),
  `transverse-mode` (אופן רוחבי), `hermite-gauss-modes` (אופני הרמיט–גאוס),
  `confocal-cavity` (מהוד קונפוקלי; `he_reject` candidate: מהוד מוקד־משותף —
  translator to decide), `g-parameters` (פרמטרי g). Cited, not re-deposited:
  `finesse`, `free-spectral-range`, `linewidth`, `photon-lifetime`,
  `cavity-ringdown` (26), `degeneracy` (07).
- **Interactive controls and simulations:** the stability-diagram map (drag
  $(g_1, g_2)$, or drive $(L, R_1, R_2)$ sliders and watch the dot move); spectrum
  ladder (`mode_frequencies`, $q$ window ~5 FSR, $m{+}n \le 4$); escape-time
  heatmap over the diagram (iterated map, log color); HG mode gallery
  (`hermite_gauss_mode`, $m, n \le 4$) beside part-02's string-mode figures for node
  counting.
- **Virtual lab outline** (`notebooks/en/labs/44-resonators.ipynb`): (1) preset
  cavities on the map; `cavity_mode` geometry vs the closed forms; (2) *stability
  experiment:* fix $R_1, R_2$, sweep $L$ through the stable window — measure
  $w_0(L)$, watch it collapse at both edges; escape-time curve outside; (3) *the
  designed discovery:* sweep $L$ around $R_1 = R_2 = L$ while plotting
  `mode_frequencies` — the student is asked to find the length where the transverse
  ladder collapses, then explain it with 43's `gouy_phase`; (4) ringdown → $\tau_p$
  → $Q$ via `q_from_ringdown`, cross-checked against `q_from_bandwidth` on the Airy
  peak (`interference.airy_transmission`) — value ± uncertainty, one number two
  ways; (5) *measurement:* noisy scanning-cavity trace → fit FSR and finesse ± σ
  (26's calibration workflow, reused verbatim).
- **Real-experiment counterpart:** none practical — stable open cavities need
  super-polished mirrors and alignment beyond household reach; the lab ships an
  import cell for a teaching-lab scanning Fabry–Pérot trace (26's precedent), and
  one honest sentence points at the HeNe's visible output spot as the cavity mode
  the student can already see.
- **Media assets** (`render_gaussian.py`, continued): (d) stability tour: the dot
  driven around the diagram while the cavity cartoon morphs plane-plane → confocal →
  concentric, escape animation outside the region; (e) HG gallery beside string
  modes, node counting synchronized (part-02 echo, no text); (f) spectrum collapse:
  the transverse ladder sliding as $L$ sweeps, snapping into degeneracy at confocal.
- **Quiz bank outline:** `Q-44-1` MC — which of four sketched cavities are stable
  (OBJ-44-1, distractor `any-mirrors-make-cavity`); `Q-44-2` numeric — $g_1 g_2$
  and stability for given $L, R_1, R_2$ (OBJ-44-1); `Q-44-3` numeric — waist of a
  symmetric cavity (OBJ-44-2); `Q-44-4` numeric — FSR and linewidth for given $L$,
  $R$ (OBJ-44-3, cites 26's formulas); `Q-44-5` MC — identify $(m, n)$ from a mode
  image by node counting (OBJ-44-4); `Q-44-6` numeric — transverse-mode offset at
  confocal (OBJ-44-5); `Q-44-7` free — cavity $Q$ three ways, optics edition
  (OBJ-44-3).
- **Problem set outline:** analytical — derive the trace identity; symmetric-cavity
  geometry from the general formulas; show the confocal $\Delta\psi = \pi/2$ from
  43's Gouy integral; ray-orbit stability (same condition, rays only).
  Computational — escape-time map generation; mode-frequency fingerprinting (given
  a measured comb, infer $g_1 g_2$); near-planar HeNe: full budget $L = 30$ cm,
  $R_2 = 60$ cm, $R_1 = \infty$ — waist, FSR, transverse splitting. Challenge —
  three-mirror folded cavity via `cascade` (astigmatism ignored, stated); mode
  matching 43's beam into it (bridge problem).
- **Runtime budget:** all algebraic; escape-time map $200^2$ dots × ≤ 200
  iterations — about a second; HG gallery $256^2$ grids; animations ≤ 250 frames.
- **Validation gates:** standard set with `--module 44-resonators`; the §4 cavity
  limits (confocal closed form, trace identity, degeneracy pin) land with this
  module — part-13's electives will cite them.
- **Open questions for the author:** whether the escape-time heatmap belongs in the
  content page or lab only (recommendation: page thumbnail, lab interactive);
  whether to introduce "TEM$_{mn}$" labels alongside HG$_{mn}$ (recommendation:
  yes, once, as the laser-lab dialect); whether the unstable-resonator honesty box
  cites a use case (recommendation: one line — high-power CO$_2$ lasers).

### 5.3 `45-lasers` — Lasers: gain, threshold, and clamping

- **Identity and scope:** master-plan notebook 12.4, semiclassical by design (§8):
  Einstein coefficients, rate equations, inversion, threshold, gain clamping,
  spectral narrowing, and the coherence payoff. Deferred: field quantization, photon
  statistics, $g^{(2)}$ → `52-quantum-optics`; mode locking → `55-ultrafast`;
  semiconductor gain → named as hardware only; injection locking and full laser
  dynamics → Siegman pointer in advanced.
- **Prerequisites:** `44-resonators` (mode structure; photon lifetime / cavity loss);
  `27-coherence` (`interference.coherence_length`, `visibility`,
  `partial_coherence_source`, the source table); `00-phasors`
  (`phasors.random_phasor_sum`, the violinists); `16-light-in-matter` (the Lorentz
  absorption line — gain is that line with the population difference reversed;
  `em.lorentz_susceptibility` cited in an aside); `02-damped-driven` (rate reasoning,
  the Lorentzian).
- **Learning objectives:**
  - `OBJ-45-1` — State the Einstein relations g1 B12 = g2 B21 and
    A21/B21 = 8 pi h nu^3 / c^3, and explain why equilibrium with the Planck
    spectrum forces stimulated emission to exist.
  - `OBJ-45-2` — Write and solve rate equations for two-, three-, and four-level
    schemes; show a two-level system pumped by its own transition saturates at
    N2 = N1 and can never invert; explain why four-level thresholds are low.
  - `OBJ-45-3` — State the threshold condition gain = loss, compute the threshold
    inversion from sigma and the cavity loss rate, and the threshold pump from the
    level lifetimes.
  - `OBJ-45-4` — Explain gain clamping: above threshold the inversion stays pinned
    at its threshold value and output power grows linearly with pump; extract
    threshold and slope efficiency from noisy output-vs-pump data.
  - `OBJ-45-5` — Contrast light below threshold (spontaneous, random phases,
    intensity ~ N) with light above threshold (one mode, phase-locked,
    intensity ~ N^2), and predict the coherence-length ratio of a lamp and a laser
    at equal power.
  - `OBJ-45-6` — (advanced) Estimate the Schawlow-Townes linewidth floor and read a
    frequency comb as a phase-locked mode ladder.
- **Mathematical background:** has — rate-of-change bookkeeping (02/05), ensemble
  averages (00/27), the Lorentzian; introduced here — detailed balance as an
  argument pattern, coupled nonlinear ODEs solved by finding fixed points first.
- **Physical intuition goals:** (1) stimulated emission is not exotic — equilibrium
  bookkeeping *demands* it; (2) a two-level atom pumped at its own line is a
  fifty-fifty coin, never a lasing medium; (3) above threshold the medium is a
  saturated amplifier: pump harder and you get more *photons*, not more *gain*;
  (4) the lamp and the laser can carry the same wattage and differ by seven orders
  of magnitude in how far their phase reaches.
- **Section skeleton seeds:**
  - *puzzle:* a 1 mW laser pointer and a 60 W bulb: the bulb wins on power ×60,000 —
    yet the pointer's spot outshines its patch of wall, makes fringes metres long,
    and the bulb can do neither at any wattage. (Boxed: what did the laser do to its
    milliwatt that the bulb cannot do with sixty watts — and what, physically, flips
    on at "threshold"?)
  - *predict:* (1) lamp and laser at exactly equal power through module 25's
    Michelson at 1 m path difference — which shows fringes? (targets
    `laser-bright-lamp`) (2) pump a two-level medium ever harder: does $N_2$ ever
    exceed $N_1$? (the classic trap) (3) doubling the pump above threshold — what
    happens to the inversion? to the output? (4) as pump crosses threshold, does the
    emission spectrum widen, narrow, or hold?
  - *explore:* rate-equation dashboard — scheme selector (two/three/four level),
    pump slider, live population bars + photon number + an output-vs-pump curve that
    accrues a dot per setting (the knee emerges from the student's own sweep);
    "violinist view": $N$ emitter phasors (via `phasors.random_phasor_sum`) random
    below threshold, locking above, with an intensity meter jumping from $\propto N$
    to $\propto N^2$; spectrum panel narrowing through threshold.
  - *derive:* Einstein's argument — two-level atoms in a Planck bath; balance
    forces $g_1 B_{12} = g_2 B_{21}$ and $A/B = 8\pi h\nu^3/c^3$ (core states the
    result and the logic; advanced runs the algebra) → cross-section and gain
    $\gamma(\nu) = \sigma(\nu)\,\Delta N$ — module 16's absorption with $\Delta N$
    flipped (one aside, `em.lorentz_susceptibility` cited) → rate equations per
    scheme (`rate_equations`) → two-level steady state: $\Delta N \le 0$ always
    (`steady_state_inversion("two", ...)` — the trap sprung, pinned by a test) →
    three-level pain (half the population must move) vs four-level ease (lower level
    drains) → threshold: round-trip gain = loss, i.e. stimulated rate = cavity loss
    rate `cavity_loss_rate` (44's $1/\tau_p$) → threshold inversion and pump
    (`threshold_pump`) → **gain clamping**: above threshold the photon number grows
    until stimulated emission burns inversion exactly as fast as pumping restores
    it — $\Delta N$ pins at $\Delta N_{\text{th}}$ (`clamped_inversion`), output
    linear in pump (`output_vs_pump`), slope efficiency read off →
    spectral narrowing: the lasing line collapses inside the cavity line →
    coherence payoff: below threshold, spontaneous — random phases, the violinists'
    $\propto N$; above, one mode stimulated into step — $\propto N^2$; **module
    00's line quoted verbatim**: "That gap, $N$ versus $N^2$, is the entire
    engineering case for the laser" — promise kept, on this page.
  - *verify:* `rate_equations` late-time vs `steady_state_inversion` (convergence
    test in view); the two-level impossibility sweep across 8 decades of pump;
    clamping measured — $\Delta N$ vs pump flat above threshold to 1% (the
    `numerical-observation` box); knee fit on noisy `output_vs_pump` across seeds;
    the falsifier: equal-power lamp-like and laser-like fields from
    `partial_coherence_source`, visibility vs delay → `coherence_length` ratio
    $\sim 10^7$.
  - *transfer:* `44-resonators` backward (what lases is the mode that fits);
    `27-coherence` backward (the vocabulary bought there, spent here);
    `16-light-in-matter` (gain = negative absorption — one sign);
    `18-fresnel` (Brewster windows in gas-laser tubes — 18's promise kept);
    `50-holography` (the enabler); `52-quantum-optics` (what "one mode, in step"
    really means; photon statistics); `55-ultrafast` (combs: 44's ladder
    phase-locked); the semiconductor diode as the world's default laser (named,
    not modeled).
  - *quiz:* two-level trap; threshold numeric; clamping MC; slope-efficiency
    numeric; lamp-vs-laser MC (registry distractor); Einstein-argument MC.
  - *explain:* why equilibrium requires stimulated emission (no formulas); gain
    clamping as a thermostat story; what threshold *is* in one sentence; why
    "brighter" and "more coherent" are different axes.
  - *advanced:* the Einstein-relation algebra run fully (Planck equilibrium →
    both relations); relaxation oscillations (the turn-on ringing in the lab, named
    and shown); Schawlow–Townes
    $\Delta\nu_{\text{ST}} \approx \pi h\nu\,(\delta\nu_c)^2 / P_{\text{out}}$ —
    order-of-magnitude: millihertz for a milliwatt HeNe (`open-question` pointer:
    the quantum origin, 52); frequency combs as the research box (44's ladder +
    mode locking teaser → `55-ultrafast`).
- **Core derivations** (ordered): (1) detailed balance in a Planck bath:
  $N_2(A + B_{21}\rho) = N_1 B_{12}\rho$ with Boltzmann populations forces the two
  Einstein relations — spontaneous-to-stimulated ratio fixed by thermodynamics, no
  atom details. (2) Four-level rate equations (course workhorse):
  $\dot{N}_2 = R_p - N_2/\tau_2 - \sigma\Phi\,\Delta N$,
  $\dot{\phi} = V_g\sigma\Phi\,\Delta N - \phi/\tau_p + \beta N_2/\tau_2$ (photon
  number $\phi$, flux $\Phi \propto \phi$; spontaneous seed $\beta$) — fixed points
  before trajectories. (3) Two-level closed form:
  $\Delta N/N = -1/(1 + 2W\tau/\,\cdots) \le 0$ — saturation at transparency,
  the impossibility as algebra, one line. (4) Threshold:
  $\sigma c\,\Delta N_{\text{th}}/n = 1/\tau_p$, so
  $\Delta N_{\text{th}} = n/(c\,\sigma\tau_p)$ — 44's photon lifetime doing laser
  work; threshold pump from $\Delta N_{\text{th}}/\tau_2$. (5) Clamping: for
  $R_p > R_{\text{th}}$, the photon fixed point moves, the inversion fixed point
  does not: $\Delta N = \Delta N_{\text{th}}$,
  $P_{\text{out}} \propto (R_p/R_{\text{th}} - 1)$ — the knee. (6) The coherence
  contrast: below threshold the field is 00's random-phasor sum (intensity
  $\propto N$, coherence set by the *spontaneous* linewidth); above, one mode with
  a common phase (intensity $\propto N^2$, coherence set by the *cavity-narrowed*
  line) — quantitative via `partial_coherence_source` at the two linewidths.
- **Model specification draft:** System — an ensemble of pumped atoms (two-, three-,
  or four-level) exchanging energy with one cavity mode; observables: populations,
  photon number, output power, emission spectrum, coherence length. Dynamics — rate
  equations (mean-field, semiclassical); no phases inside the medium. Boundary —
  the cavity as a lumped loss rate (module 44's number); pump as a given rate.
  Ensemble — populations are ensemble means; the coherence cells use seeded field
  ensembles (27's machinery). Ignored — spatial structure (hole burning), multimode
  competition, coherent (Rabi) dynamics, quantum noise except as the spontaneous
  seed $\beta$. Valid when — dephasing fast against population change
  (rate-equation regime); photon numbers large; single mode dominant. Failure
  modes — rate equations read as field dynamics; two-level "lasers"; thresholdless
  claims from $\beta \to 1$ taken literally; Schawlow–Townes quoted as exact.
- **Epistemic classification:** Einstein relations — `theorem` (boxed —
  thermodynamic argument, the module's crown); rate equations —
  `model-assumption` (boxed: the semiclassical scope statement, with the honest
  edge "phases erased"); two-level no-inversion — `theorem` (within the model;
  pinned test); measured clamping — `numerical-observation`; threshold condition —
  `theorem`; Schawlow–Townes — `approximation` (order-of-magnitude, quantum origin
  an `open-question` pointer to 52).
- **Misconceptions:** NEW **`laser-bright-lamp`** — "A laser is just a very bright
  lamp." Falsifying experiment: simulate a lamp-like and a laser-like source at
  *equal optical power* (`interference.partial_coherence_source` with
  $\Delta\lambda \approx 30$ nm vs a cavity-narrowed line), run both through 25's
  Michelson, measure visibility vs delay and extract
  `interference.coherence_length`: micrometres vs hundreds of metres at identical
  wattage — brightness and coherence are different axes, and no filter recovers
  the difference without discarding almost all the power (shown: filtering the
  lamp to the laser's linewidth leaves picowatts). Distractor: quiz option "any
  lamp, filtered and focused well enough, is equivalent to a laser of the same
  power". (The two-level trap is deliberately a quiz item, `Q-45-1`, not a
  registry entry — an error pattern, not a stable wrong model; precedent: 24's
  $\pi$-shift trap.)
- **Glossary terms:** `stimulated-emission` (פליטה מאולצת), `spontaneous-emission`
  (פליטה ספונטנית; `he_reject` candidate: פליטה עצמונית — translator to decide),
  `population-inversion` (היפוך אוכלוסייה — translator to confirm form),
  `optical-pumping` (שאיבה אופטית), `gain-medium` (תווך הגבר), `laser-threshold`
  (סף הלייזר), `gain-clamping` (קיבוע ההגבר — translator to confirm),
  `rate-equations` (משוואות קצב), `einstein-coefficients` (מקדמי איינשטיין),
  `slope-efficiency` (נצילות שיפוע — translator to decide), `four-level-laser`
  (לייזר ארבעה רמות — translator to confirm), `frequency-comb` (מסרק תדרים).
- **Interactive controls and simulations:** rate-equation dashboard (scheme, pump
  0–10× threshold, $\tau_2$, $\tau_1$, $R$'s via a cavity preset from 44); the
  violinist view ($N \le 200$ arrows, threshold crossing animated); spectrum panel
  (below-threshold spontaneous line vs above-threshold narrowed line);
  output-vs-pump plotter with noise toggle and two-line fit overlay.
- **Virtual lab outline** (`notebooks/en/labs/45-lasers.ipynb`): (1) turn-on:
  integrate the four-level `rate_equations`, watch relaxation-oscillation ringing
  settle to the fixed point; (2) *measurement:* pump sweep with
  `measurement.add_noise` on the detector → two-line fit →
  $R_{\text{th}} \pm \sigma$ and slope efficiency ± σ (the measurement-culture
  centrepiece); (3) clamping: $\Delta N$ vs pump — flat above threshold (the
  falsifying plot for "more pump, more gain"); (4) scheme shoot-out: three- vs
  four-level threshold ratio at equal $\sigma, \tau_p$; two-level: inversion never
  (the trap, run honestly); (5) *the registry falsifier:* equal-power lamp vs
  laser → visibility vs delay → `coherence_length` both, ratio reported with
  uncertainty across seeds; (6) advanced: $\beta$ sweep — the knee softening, and
  what "thresholdless" would mean.
- **Real-experiment counterpart:** laser pointer vs LED flashlight through a CD
  grating (spectrum: one sharp line vs a broad band — photograph and import), and
  laser speckle on a wall vs none from the LED — two coherence signatures with
  zero equipment; import the spectra photos and compare linewidths
  order-of-magnitude.
- **Media assets** (`render_photonics.py`): (g) the violinists' payoff: random
  arrows → phase-locking as pump crosses threshold, intensity meter jumping from
  $N$-fold to $N^2$-fold (module 00's animation reborn, no text); (h) the knee:
  population bars, photon number, and output climbing as pump ramps — the
  inversion needle *sticking* at clamp while output soars; (i) spectral collapse
  through threshold.
- **Quiz bank outline:** `Q-45-1` MC — pump a two-level medium harder and harder
  (OBJ-45-2, trap distractor "eventually $N_2 > N_1$"); `Q-45-2` numeric —
  threshold inversion from $\sigma$, $\tau_p$ (OBJ-45-3); `Q-45-3` MC — inversion
  when pump doubles above threshold (OBJ-45-4); `Q-45-4` numeric — threshold and
  slope efficiency from four data points (OBJ-45-4); `Q-45-5` MC — equal-power
  lamp vs laser in a Michelson (OBJ-45-5, distractor `laser-bright-lamp`);
  `Q-45-6` MC — which Einstein process is required by equilibrium and why
  (OBJ-45-1); `Q-45-7` free — the $N$ vs $N^2$ story in your own words
  (OBJ-45-5).
- **Problem set outline:** analytical — run the Einstein-relation algebra; derive
  the two-level saturation closed form; three-level threshold pump vs four-level
  (the ruby-vs-Nd:YAG numbers); clamped output power from the photon fixed point.
  Computational — relaxation-oscillation frequency vs pump (fit, compare to the
  linearized prediction); knee-fit bias vs noise and $\beta$. Challenge — the
  filtered-lamp problem: compute the power surviving a filter that matches the
  laser's linewidth (the honest quantitative burial of `laser-bright-lamp`);
  Schawlow–Townes ballpark for a HeNe and for a diode.
- **Runtime budget:** ODE integrations ≤ $10^4$ steps; coherence ensembles
  $M \le 64$ of $2^{13}$-sample fields (27's heaviest-cell precedent) — a few
  seconds; everything else trivial; animations ≤ 250 frames.
- **Validation gates:** standard set with `--module 45-lasers`; the §4 two-level
  impossibility, clamping, and knee-fit seed tests land with this module.
- **Open questions for the author:** whether the Einstein argument's algebra is
  core or advanced (recommendation: logic in core, algebra in advanced —
  precedent: 27's Wiener–Khinchin went core, but that proof is three lines);
  whether the violinist view lives on the page or lab-only (recommendation: page —
  it is the course's oldest promise being kept); whether to include the
  spectral-radiance "brighter than the Sun" number for the pointer (recommendation:
  yes, one boxed order-of-magnitude estimate in the puzzle).

### 5.4 `46-waveguides` — Waveguides: light confined by resonance

- **Identity and scope:** master-plan notebook 12.5. The symmetric step-index slab:
  guidance by transverse resonance, discrete modes, cutoff, effective index,
  evanescent tails; TE/TM kept light. Deferred: fibers and their engineering →
  `47-fibers`; rigorous vector modes and LP algebra → advanced note + part-13;
  photonic-crystal and periodic guidance → `54-photonic-crystals`; integrated-optics
  device zoo → one transfer paragraph.
- **Prerequisites:** `19-evanescent` (`interfaces.critical_angle`,
  `penetration_depth`, `evanescent_field`, TIR phase shifts from the complex-safe
  `fresnel_rs` / `fresnel_rp`, `ftir_transmission`); `18-fresnel` (s/p = TE/TM
  dictionary); `11-standing-waves` (round-trip quantization); `06-coupled`
  (two-oscillator exchange, for the advanced coupler); `16-light-in-matter`
  (phase $n k_0 x$).
- **Learning objectives:**
  - `OBJ-46-1` — Derive the transverse-resonance condition
    2 k0 n1 d cos(theta) - 2 phi_TIR(theta) = 2 pi m for a slab of thickness d, and
    explain why guided modes form a discrete set even though TIR allows a continuum
    of angles.
  - `OBJ-46-2` — Solve the symmetric-slab mode equations graphically and
    numerically, count modes as 1 + floor(2 d NA / lambda), and predict cutoff
    thicknesses; state that the symmetric slab's fundamental mode never cuts off.
  - `OBJ-46-3` — Interpret the effective index n2 < n_eff = n1 sin(theta) < n1 as
    the mode's phase index, and connect it to the zig-zag angle and the mode's
    speed.
  - `OBJ-46-4` — Compute the evanescent decay length of a mode's cladding tail and
    the core confinement fraction, and predict how both change with d/lambda.
  - `OBJ-46-5` — (advanced) Estimate the beat length of a two-guide directional
    coupler from the splitting of its symmetric and antisymmetric supermodes, and
    map the power exchange onto module 06's coupled pendulums.
- **Mathematical background:** has — TIR phases (19), standing-wave quantization
  (11), s/p bookkeeping (18); introduced here — the graphical-solution idiom
  (transcendental equation as curve crossings), the normalized parameters
  $u, w_{\text{ev}}, V_{\text{slab}}$.
- **Physical intuition goals:** (1) TIR traps light; *interference* selects which
  trapped light survives — guidance is a resonance, not a cage; (2) thinner core →
  fewer modes, but the symmetric slab never loses its last one; (3) a mode is not
  "inside" the core: its evanescent tail carries real fielding into the cladding,
  and near cutoff *most* of the mode lives there; (4) $n_{\text{eff}}$ is a speed
  dial between core and cladding glass.
- **Section skeleton seeds:**
  - *puzzle:* a glass film one micron thick on a chip carries light for
    centimetres with no mirrors anywhere — but shine light in at most angles above
    critical and it *still* dies out. (Boxed: TIR permits every angle past
    critical; what selects the handful that actually guide?)
  - *predict:* (1) is every ray steeper than the critical angle guided? (targets
    `tir-guides-all-angles`) (2) halve the film thickness — more guided modes or
    fewer? (3) can a guided mode's field be entirely inside the core? (4) does
    guided light travel at $c/n_1$, $c/n_2$, or in between?
  - *explore:* zig-zag explorer — angle slider past critical; phase-front overlay
    showing the wave interfering with its own double reflection; a live round-trip
    transverse-phase readout that snaps to $2\pi m$ at the special angles (the
    resonance made visible); graphical solver — the tan-branch curves against the
    $V_{\text{slab}}$ circle, $d/\lambda$ slider growing the circle so
    intersections (modes) are *born* one at a time; mode-profile panel with
    evanescent tails and a confinement-fraction meter.
  - *derive:* zig-zag ansatz: core plane wave at angle $\theta$ from the normal,
    transverse wavenumber $\kappa = k_0 n_1\cos\theta$ → round-trip transverse
    phase must close: $2\kappa d - 2\varphi_{\text{TIR}}(\theta) = 2\pi m$ — **the
    standing-wave condition of `11-standing-waves`, transverse now — said in
    those words**, with $\varphi_{\text{TIR}}$ from 19's phase shifts
    (`tir_phase` wrapping `interfaces.fresnel_rs` / `fresnel_rp`) →
    $n_{\text{eff}} = n_1\sin\theta$, bounded by $n_2$ (TIR fails) and $n_1$
    (grazing) → normalized form: $u = \kappa d/2$,
    $w_{\text{ev}} = \gamma d/2$, $u^2 + w_{\text{ev}}^2 = V_{\text{slab}}^2$
    with $V_{\text{slab}} = (\pi d/\lambda)\,\mathrm{NA}$; even TE:
    $w_{\text{ev}} = u\tan u$, odd TE: $w_{\text{ev}} = -u\cot u$ → the graphical
    solution → cutoffs at $V_{\text{slab}} = m\pi/2$; mode count
    $1 + \lfloor 2 V_{\text{slab}}/\pi \rfloor$; the fundamental survives at every
    $V_{\text{slab}} > 0$ → cladding tails: decay rate
    $\gamma = k_0\sqrt{n_{\text{eff}}^2 - n_2^2}$ — exactly the
    `interfaces.penetration_depth` form with $n_1\sin\theta_1 \to n_{\text{eff}}$
    (19's payoff, cited) → confinement fraction and its collapse near cutoff →
    TE/TM: same story, TM phases differ slightly (18's s/p, one paragraph) →
    waveguide dispersion: $n_{\text{eff}}(\lambda)$ even for dispersionless glass
    — geometry disperses (the seed 47 harvests).
  - *verify:* `slab_modes` vs a dense sign-change scan of `slab_mode_condition`
    (roots complete, none spurious — the convergence test in view);
    `slab_mode_count` vs `len(slab_modes)` across a $d/\lambda$ sweep (staircase);
    tail decay vs `interfaces.penetration_depth` (limits test); **the falsifier
    run:** superpose the zig-zag wave with its reflections at an off-resonance
    angle — the field self-cancels along $z$ while resonant angles persist
    unchanged (the `numerical-observation` box: decay length vs detuning from
    resonance).
  - *transfer:* `47-fibers` (roll the slab into a cylinder — same logic, Bessel
    bookkeeping); `11-standing-waves` backward (the same condition, rotated 90°);
    `19-evanescent` backward (the tail is the mode's glue — and two guides close
    enough share it: `interfaces.ftir_transmission` is the coupler's engine);
    `06-coupled` (supermode splitting ↔ exchange — same physics as the pendulums);
    integrated photonics: silicon waveguides, modulators, splitters — the chips
    the internet switches with; `54-photonic-crystals` (replace TIR by Bragg
    reflection: guidance without an index step).
  - *quiz:* which-angles-guide MC (registry distractor); mode-count numeric;
    cutoff numeric; $n_{\text{eff}}$ interpretation MC; decay-length numeric.
  - *explain:* why discreteness follows from "the wave must agree with itself"
    (no formulas); what $n_{\text{eff}}$ means physically; where a mode near
    cutoff actually lives; how you would explain to a ray-optics believer what the
    ray picture misses.
  - *advanced:* the directional coupler — two slabs, gap $g$: supermodes split by
    an amount $\propto e^{-\gamma g}$ (the tails overlap), power beats between
    guides with beat length $L_b = \pi/(\beta_s - \beta_a)$ — module 06's
    exchange, verbatim, with `exchange_time`'s logic in space; asymmetric slabs
    (the fundamental *can* cut off — the symmetric result is a symmetry gift);
    TM phase algebra. Safe to skip: 47 needs none of it.
- **Core derivations** (ordered): as in the seeds; the transverse-resonance
  condition written with the TIR phase in the course convention (phases of the
  complex `fresnel_rs` above critical, $e^{-\ii\omega t}$ throughout); the even/odd
  TE equations derived from the symmetric/antisymmetric standing-wave split (06's
  parity logic echoed); the mode-count formula derived by counting circle-branch
  crossings; the near-cutoff limit $w_{\text{ev}} \to 0$: tail length diverges,
  confinement $\to 0$, $n_{\text{eff}} \to n_2$ — "the mode evaporates into the
  cladding", stated as the physical meaning of cutoff.
- **Model specification draft:** System — a symmetric step-index slab
  $(n_1, d, n_2)$, monochromatic light, one transverse dimension; observables:
  mode angles, effective indices, profiles, counts, decay lengths. Dynamics —
  none; algebraic self-consistency (root-finding on the resonance condition).
  Boundary — claddings semi-infinite; interfaces ideal planes (19's model spec
  inherited). Ensemble — deterministic; the profile-fit lab cell adds seeded
  noise. Ignored — loss, roughness scattering, substrate asymmetry (advanced
  aside), vector corrections beyond the TE/TM phase split, wavelength dependence
  of $n_{1,2}$ (supplied per call). Valid when — $d \sim \lambda$ within an order
  of magnitude; index step real (lossless); weak guidance not required (the slab
  is exact within the scalar-per-polarization model). Failure modes — counting
  TIR angles as modes; reading the tail as loss; trusting mode counts at exact
  cutoff; applying symmetric-slab no-cutoff to asymmetric guides.
- **Epistemic classification:** transverse-resonance condition and discreteness —
  `theorem` (boxed — the module's spine); mode-count formula — `theorem` (with
  the boundary-case caveat); "guided mode" — `definition` (self-reproducing
  transverse pattern — deliberately the same sentence shape as 44's cavity-mode
  definition, and the page says so); off-resonance self-cancellation decay —
  `numerical-observation`; ideal lossless slab — `model-assumption`.
- **Misconceptions:** NEW **`tir-guides-all-angles`** — "Any ray steeper than the
  critical angle is trapped, so a waveguide carries a continuum of guided rays."
  Falsifying experiment: plot the transverse-resonance residual over all angles
  above critical — zeros only at discrete $\theta_m$ (`slab_modes` returns a
  finite list); propagate an off-resonance zig-zag superposition and watch it
  self-destruct within tens of bounces while the resonant angles persist — TIR
  conserves the light, interference disqualifies it. Distractor: quiz option
  "all angles above critical propagate equally; the discrete modes are a
  mathematical convenience".
- **Glossary terms:** `waveguide` (מוליך גלים), `slab-waveguide` (מוליך גלים
  לוחי — translator to confirm), `guided-mode` (אופן מונחה), `effective-index`
  (מקדם שבירה אפקטיבי), `transverse-resonance` (תהודה רוחבית), `mode-cutoff`
  (קטעון אופן — translator to decide; distinct from part-02's `cutoff-frequency`,
  which is cited for the band-edge sense), `confinement-fraction` (מקדם כליאה —
  translator to confirm), `directional-coupler` (מצמד כיווני).
- **Interactive controls and simulations:** zig-zag explorer ($\theta$ from
  critical to grazing, $d/\lambda$ 0.1–20, live round-trip-phase dial);
  graphical solver (tan branches + growing $V$ circle, intersections
  highlighted, each spawning its profile); mode-profile panel (profile, tail
  ruler, confinement meter); advanced: two-guide coupler (gap slider, power
  see-saw between guides — 06's site-energy bars, in space).
- **Virtual lab outline** (`notebooks/en/labs/46-waveguides.ipynb`): (1) zig-zag
  explorer: find the first three resonant angles by hand from the phase dial;
  (2) graphical solution: overlay branches and circle, then `slab_modes` — hand
  vs solver; (3) profiles: plot `slab_mode_profile`, fit the tail decay length,
  compare `interfaces.penetration_depth`; confinement fraction vs
  $d/\lambda$ (the evaporation curve toward cutoff); (4) mode census: staircase
  of `len(slab_modes)` vs $d/\lambda$ against `slab_mode_count`; (5) *the
  falsifier:* off-resonance launch — decay length vs angular detuning, plotted;
  (6) *measurement:* noisy near-field profile of an "unknown" slab → fit $d$ and
  $n_1$ from the mode shape, value ± uncertainty across seeds; (7) advanced:
  coupler beat length vs gap — log-linear fit, slope vs $\gamma$ (19's
  exponential, again).
- **Real-experiment counterpart:** qualitative only, honestly flagged: a laser
  pointer into the edge of a clear acrylic sheet or a water stream in a dark room
  shows TIR guidance (scratches and bends glow where the condition breaks); mode
  *counting* needs micron films, so the quantitative pairing waits for 47's NA
  cone (which imports cleanly).
- **Media assets** (`render_photonics.py`, continued): (j) self-selection: two
  zig-zag launches side by side — off-resonance phase fronts misregistering and
  dying, resonant fronts locking into a travelling standing pattern; (k) mode
  births: the $V$ circle growing through tan branches, each new intersection
  spawning a profile whose tail shortens as it pulls into the core.
- **Quiz bank outline:** `Q-46-1` MC — which angles above critical guide
  (OBJ-46-1, distractor `tir-guides-all-angles`); `Q-46-2` numeric — mode count
  for given $d, \lambda, n_1, n_2$ (OBJ-46-2); `Q-46-3` numeric — largest $d$
  for single-mode operation (OBJ-46-2); `Q-46-4` MC — meaning and bounds of
  $n_{\text{eff}}$ (OBJ-46-3); `Q-46-5` numeric — cladding decay length of a
  given mode (OBJ-46-4); `Q-46-6` free — why guided modes are discrete, in three
  sentences without equations (OBJ-46-1); `Q-46-7` MC (advanced) — what happens
  to the coupler's beat length when the gap widens (OBJ-46-5).
- **Problem set outline:** analytical — derive the even/odd TE equations from
  symmetry; asymmetric slab: show the fundamental acquires a cutoff; TM
  condition and the TE–TM $n_{\text{eff}}$ split; near-cutoff tail divergence.
  Computational — dispersion curves $n_{\text{eff}}(\lambda)$ for a fixed slab
  (the waveguide-dispersion seed for 47, plotted); mode-orthogonality check by
  numerical overlap. Challenge — the two-guide coupler as a $2\times2$
  eigenproblem (06's matrices, optical costume): supermodes, splitting, beat
  length vs gap against the overlap estimate.
- **Runtime budget:** root-finding and profiles trivial; the falsifier's
  propagation cells are analytic superpositions on $512 \times 2000$ grids —
  about a second; coupler cells $2\times2$ algebra; animations ≤ 200 frames.
- **Validation gates:** standard set with `--module 46-waveguides`; the §4
  slab-mode convergence, count, and tail-limit tests land with this module
  (47 cites the count machinery).
- **Open questions for the author:** whether TM algebra appears at all in core
  (recommendation: one paragraph, s/p dictionary + "phases differ", algebra to
  problems); whether the coupler demo is advanced-section or lab-only
  (recommendation: advanced section with the 06 side-by-side figure — the motif
  is too good to hide); notation handshake — 19 uses $\theta_1$ for the
  incidence angle, this module renames the mode's angle $\theta_m$ once, in the
  derive section (one explicit sentence, part-02 §5.2's precedent).

### 5.5 `47-fibers` — Optical fibers: modes, dispersion, and bit rates

- **Identity and scope:** master-plan notebook 12.6. Step-index fibers: NA and
  acceptance, the V-number and single-mode condition, mode counting, modal and
  chromatic dispersion, and bit-rate × distance limits with real hardware numbers.
  Deferred: LP-mode algebra (Bessel machinery) → advanced note + part-13; fiber
  nonlinearity and solitons → `51-nonlinear-optics`; amplifiers (EDFA) and coherent
  detection → named in the research box only; polarization-mode dispersion → one
  honest sentence.
- **Prerequisites:** `46-waveguides` (discreteness, $n_{\text{eff}}$, cutoff logic,
  waveguide dispersion seed); `13-dispersion` / `12-wave-packets`
  (`waves.group_velocity`, `waves.spreading_time`, `waves.propagate_dispersive`,
  `waves.gaussian_packet`); `16-light-in-matter` (`em.sellmeier`,
  `em.group_index`, `em.refractive_index`); `17-refraction` / `19-evanescent`
  (`interfaces.snell_angle`, `interfaces.critical_angle`); `27-coherence`
  (source linewidth $\Delta\lambda$); `45-lasers` (the source the link starts
  with).
- **Learning objectives:**
  - `OBJ-47-1` — Derive NA = sqrt(n1^2 - n2^2) from total internal reflection at
    the core-cladding boundary plus refraction at the entrance face, compute the
    acceptance angle, and extract NA from a measured output cone.
  - `OBJ-47-2` — Compute V = 2 pi a NA / lambda, apply the single-mode condition
    V < 2.405, estimate the mode count as V^2/2 for large V, and state honestly
    where 2.405 comes from (first zero of the Bessel function J0).
  - `OBJ-47-3` — Compute the modal delay spread Delta t = L n1 Delta / c of a
    step-index multimode fiber and the bit-rate x distance limit it implies.
  - `OBJ-47-4` — Compute chromatic pulse broadening Delta t = |D| L Delta lambda
    from the dispersion parameter D, connect D to the group index and to the
    packet-spreading law of module 13, and locate the zero-dispersion wavelength
    of silica near 1.31 um.
  - `OBJ-47-5` — Assemble a link budget: choose fiber type, wavelength, and source
    linewidth to meet a bit-rate x distance target, and explain why long-haul
    telecom converged on single-mode fiber at 1.55 um.
- **Mathematical background:** has — everything (this is the part's cash-out
  module); introduced here — the dispersion parameter $D$ and its ps/(nm·km)
  engineering units, the eye-diagram reading of pulse spreading, dB bookkeeping
  for loss (stated operationally).
- **Physical intuition goals:** (1) a fiber's capacity is a *time* question, not a
  brightness question — bits blur into each other before they get dim; (2) wider
  core = more modes = more arrival times = fewer bits: the "bigger pipe" intuition
  is exactly backwards; (3) a single-mode fiber still spreads pulses, because glass
  itself is dispersive — 13's law with $z$ for $t$; (4) the world's fiber runs at
  1.55 µm because two curves — loss falling, infrared absorption rising — cross
  their minimum there, and at 2.405 because a Bessel function says so.
- **Section skeleton seeds:**
  - *puzzle:* TAT-8 (1988) carried 40,000 conversations through glass hair across
    the Atlantic; a modern single fiber carries terabits over the same route. Yet
    the limiting physics is not how much light survives — amplifiers fix that — but
    that different paths and different colours *arrive at different times*. (Boxed:
    what sets the maximum bits × kilometres a glass thread can carry, and why did
    the answer turn out to be a 9 µm core at 1.55 µm?)
  - *predict:* (1) which carries more data over 10 km: a 50 µm core or a 9 µm
    core? (targets `thicker-fiber-more-data`) (2) a sharp pulse enters a multimode
    fiber — what does it look like 10 km later? (3) does a *single-mode* fiber
    spread pulses at all? (4) which property of the 45-style laser limits a
    single-mode link: its power or its linewidth?
  - *explore:* fiber designer — $a$, $\Delta$, $\lambda$ sliders; live V, mode
    count, single-mode badge (`v_number`, `mode_count`); pulse-race panel: launch
    a bit train, watch modal smearing (multimode) or chromatic broadening
    (single-mode) accumulate with $L$; eye-diagram panel closing as $B$ or $L$
    rises (`bit_rate_limit` threshold drawn); the silica loss curve with the
    850/1310/1550 windows marked and the OH peak labelled.
  - *derive:* acceptance: Snell at the face + `interfaces.critical_angle` at the
    core wall → $\sin\theta_{\text{acc}} = \sqrt{n_1^2 - n_2^2} = \mathrm{NA}$
    (`numerical_aperture`, `acceptance_angle`) → V-number
    $V = 2\pi a\,\mathrm{NA}/\lambda$; the honest Bessel statement: rolling 46's
    slab into a cylinder turns cosines into Bessel functions, the second mode's
    cutoff sits at $J_0$'s first zero, 2.405 — stated, sourced, not derived
    (`empirical`-free honesty; algebra deferred) → mode count $\approx V^2/2$
    (`mode_count`) with SMF-28 and 50 µm-MMF numbers worked → modal dispersion:
    fastest (axial) vs slowest (critical-angle) ray gives
    $\Delta t = L n_1 \Delta/c$ (`modal_delay_spread`); with $\Delta = 1\%$:
    50 ns/km, so `bit_rate_limit` gives $B\cdot L \sim 5$ Mb/s·km — why multimode
    lost long-haul (graded-index as the clever patch, one paragraph, named) →
    chromatic dispersion: group delay $L n_g/c$ (`em.group_index`); different
    $\lambda$, different $n_g$ →
    $\Delta t = |D|\,L\,\Delta\lambda$, $D = -(\lambda/c)\,d^2n/d\lambda^2$
    (`dispersion_parameter` over `em.sellmeier`) — **this is `13-dispersion`'s
    packet-spreading law cashing in on real infrastructure, said in those words**
    (`waves.spreading_time`; dictionary $\beta_2 = -D\lambda^2/(2\pi c)$ stated) →
    silica's story: $D_{\text{mat}} = 0$ near 1.31 µm; loss minimum
    0.2 dB/km at 1.55 µm (Rayleigh scattering $\propto \lambda^{-4}$ falling into
    rising infrared absorption — `empirical-law` box); waveguide dispersion (46's
    seed) shifts the zero → dispersion-shifted fiber → worked budget:
    $D = 17$ ps/(nm·km), $\Delta\lambda = 0.1$ nm, $L = 100$ km →
    $\Delta t = 170$ ps → $B \lesssim 1.5$ Gb/s — and the escape routes named:
    narrower sources, dispersion management, DWDM, coherent detection, solitons
    (research box, → 51).
  - *verify:* `mode_count` staircase vs V; `modal_delay_spread` vs a Monte-Carlo
    ray ensemble's arrival histogram (limits + scaling); **the cross-library
    consistency check:** `chromatic_broadening` vs `waves.propagate_dispersive`
    of a `waves.gaussian_packet` under $\beta_2$ built from `em.sellmeier` +
    `em.group_index` — two independent routes to the same spread (the
    `numerical-observation` box); `bit_rate_limit` vs measured eye closure on
    synthetic bit trains.
  - *transfer:* capstone §35.4 — **seeded explicitly here**: laser (45) →
    modulator → fiber (this module) → dispersion (part-04's propagator) →
    detector; the module's challenge problem *is* the capstone's skeleton;
    `13-dispersion` backward (the lab curiosity that runs the internet — say
    it); `45-lasers` (linewidth as a link budget line item); `51-nonlinear-optics`
    (solitons: the nonlinear rescue); `27-coherence` ($\Delta\lambda$ ↔ $\ell_c$);
    fiber sensors and endoscope bundles (one line each); DWDM as "the comb of 44
    put to work" (one sentence).
  - *quiz:* NA/acceptance numerics; V and single-mode check; core-size capacity MC
    (registry distractor); modal-spread and chromatic-broadening numerics; the
    1.55 µm story.
  - *explain:* why capacity is a time question, to a network engineer, without
    equations; why single-mode won; what 2.405 is and is not (a Bessel zero, not
    deep magic); where 13's mathematics shows up on a repair bill.
  - *advanced:* LP modes properly named: weakly guiding limit, LP$_{01}$/LP$_{11}$,
    the V–b diagram sketched, algebra deferred to part-13; graded-index delay
    equalization ($\Delta t \propto \Delta^2$ — why the parabola helps);
    polarization-mode dispersion in one honest paragraph; the research box:
    solitons, DWDM, space-division multiplexing (modes as channels — the
    respectable version of the misconception, flagged as research).
- **Core derivations** (ordered): as in the seeds, each with its numbers run:
  (1) NA for SMF-28 ($n_1 = 1.468$, $\Delta = 0.36\%$): NA $= 0.12$,
  $\theta_{\text{acc}} \approx 7°$; (2) V at 1550 nm with $a = 4.1$ µm: 2.33 —
  single-mode; at 1260 nm: 2.405 — the cutoff wavelength *is* the spec sheet's
  number (real hardware reproduced in two lines); 50 µm MMF at 850 nm, NA 0.2:
  $V \approx 37$, $\approx 680$ modes; (3) modal spread and its $B\cdot L$;
  (4) chromatic budget as above; (5) the loss window (numbers quoted:
  ~3 dB/km at 850, ~0.35 at 1310, ~0.2 at 1550 — `empirical-law`).
- **Model specification draft:** System — a step-index fiber $(n_1, n_2, a)$ in
  the weakly guiding limit carrying pulses of centre wavelength $\lambda$ and
  width $\Delta\lambda$ over length $L$; observables: NA, V, mode counts, delay
  spreads, eye diagrams, bit-rate limits. Dynamics — none integrated here;
  chromatic evolution delegated to `waves.propagate_dispersive` (part-04's
  machinery, cited); modal spread by ray bookkeeping. Boundary — perfect
  cylindrical step; splices, bends, and connectors as a lumped dB line item.
  Ensemble — deterministic; the ray race uses seeded launch ensembles; detector
  noise via `wavelab.measurement`. Ignored — nonlinearity (51),
  polarization-mode dispersion (one sentence), amplifier noise, graded profiles
  beyond the advanced aside. Valid when — $\Delta \ll 1$ (weak guidance);
  $\Delta\lambda \ll \lambda$; lengths where loss keeps the signal above
  detector noise (stated, not modeled). Failure modes — $V^2/2$ near cutoff;
  modal and chromatic spreads combined without the stated quadrature assumption;
  dispersion formulas ridden across the zero-dispersion point without sign care;
  bit-rate "limits" read as exact rather than quarter-slot engineering bounds.
- **Epistemic classification:** NA and V results — `theorem` (within the
  step-index model); $V < 2.405$ — `theorem` *stated with honest provenance*
  (Bessel origin named, derivation deferred — the honesty box);
  $\Delta t = L n_1\Delta/c$ — `theorem` (ray model, worst case); silica loss
  window and $D$ values — `empirical-law` (boxed, measured properties of real
  glass); the two-route chromatic agreement — `numerical-observation`;
  `bit_rate_limit`'s quarter-slot rule — `model-assumption` (an engineering
  convention, flagged as such).
- **Misconceptions:** NEW **`thicker-fiber-more-data`** — "A thicker core
  carries more information because it collects and carries more light."
  Falsifying experiment: race equal-power bit trains through a 50 µm multimode
  and a 9 µm single-mode fiber (`modal_delay_spread` + the eye panel): the
  multimode eye closes at Mb/s·km while the single-mode link runs Gb/s over
  100 km — capacity is arrival-time spread, not light collection; the extra
  modes are extra *clocks*, not extra channels. Distractor: quiz option "more
  modes means more parallel channels, so the wide core carries more data" (with
  the research-grade rehabilitation — mode-division multiplexing — named in
  advanced so the distractor stays honest).
- **Glossary terms:** `optical-fiber` (סיב אופטי), `fiber-core` (ליבת הסיב),
  `cladding` (מעטפת), `numerical-aperture` (cited, deposited by `36-instruments`;
  47 adds the fiber usage to the same key), `v-number` (מספר V),
  `single-mode-fiber` (סיב חד־אופני), `multimode-fiber` (סיב רב־אופני),
  `modal-dispersion` (נפיצה אופנית — translator; `he_reject` candidate:
  דיספרסיה מודלית), `chromatic-dispersion` (נפיצה כרומטית),
  `zero-dispersion-wavelength` (אורך גל אפס־נפיצה — translator to confirm),
  `fiber-loss` (ניחות בסיב — dB/km, translator to decide), `soliton` (סוליטון),
  `wavelength-division-multiplexing` (ריבוב אורכי גל — translator to confirm).
- **Interactive controls and simulations:** fiber designer ($a$ 2–50 µm,
  $\Delta$ 0.1–3%, $\lambda$ 600–1700 nm; live V, count, badge); pulse race
  (bit rate, length, fiber preset; modal histogram + chromatic envelope); eye
  diagram (accumulating, with the `bit_rate_limit` threshold line); loss-window
  explorer (the three telecom windows, clickable presets loading $D$ and loss
  into the race).
- **Virtual lab outline** (`notebooks/en/labs/47-fibers.ipynb`): (1) designer
  play: reproduce SMF-28's spec sheet (single-mode at 1550, cutoff near
  1260 nm) from $(a, \Delta)$ alone — real hardware from two numbers; (2) *NA
  measurement:* synthetic far-field cone with noise → fit the half-angle →
  NA ± σ vs `numerical_aperture`; (3) *modal race:* seeded ray ensemble →
  arrival histogram → spread vs `modal_delay_spread`; eye diagram vs $B$ —
  find the closing rate, compare `bit_rate_limit`; (4) *chromatic:*
  `waves.gaussian_packet` through `waves.propagate_dispersive` with $\beta_2$
  from `em.sellmeier` / `em.group_index`; measure width growth vs
  `chromatic_broadening` and `waves.spreading_time`; locate the zero-dispersion
  wavelength by sweeping $\lambda$; (5) *link design (the capstone seed):*
  given $L = 100$ km and a 45-style source with $\Delta\lambda = 0.1$ nm, find
  the maximum $B$ ± uncertainty from noisy eye closure — value, error, and a
  one-paragraph design justification (measurement culture, engineering
  edition); (6) import cell for the real cone photo below.
- **Real-experiment counterpart:** two honest classics: (a) Colladon's light
  fountain — a laser pointer through a water jet from a punctured bottle: the
  jet guides until it breaks up (TIR guidance photographed); (b) fiber NA — a
  bare patch cable or cheap plastic/TOSLINK fiber: pointer in one end,
  photograph the output cone on paper at a measured distance, import the
  photo, fit the cone radius → NA ± σ, compare the spec (~0.5 for plastic,
  ~0.12–0.22 for glass — the difference itself is the lesson).
- **Media assets** (`render_photonics.py`, continued): (l) the pulse race:
  three lanes — input bit train, multimode smear, single-mode with slight
  chromatic breathing — eye diagrams closing at wildly different lengths;
  (m) the acceptance cone: rays inside the cone guided down the core, rays
  outside refracting into the cladding and leaking, the cone angle labelled
  only by geometry (language-neutral).
- **Quiz bank outline:** `Q-47-1` numeric — NA and acceptance angle from
  $n_1, n_2$ (OBJ-47-1); `Q-47-2` numeric — V and the single-mode verdict
  (OBJ-47-2); `Q-47-3` MC — which core carries more data over 10 km
  (OBJ-47-3, distractor `thicker-fiber-more-data`); `Q-47-4` numeric — modal
  spread and $B\cdot L$ for $\Delta = 1\%$ (OBJ-47-3); `Q-47-5` numeric —
  chromatic broadening and max $B$ for a given $D, L, \Delta\lambda$
  (OBJ-47-4); `Q-47-6` MC — why 1.55 µm (OBJ-47-5); `Q-47-7` free — explain to
  a network engineer why the limit is picoseconds, not milliwatts (OBJ-47-4,
  OBJ-47-5).
- **Problem set outline:** analytical — derive NA including a non-air launch
  medium (`refraction_flat` at the face); graded-index delay equalization
  sketch ($\Delta t \propto \Delta^2$, why); the $\beta_2 \leftrightarrow D$
  dictionary; cutoff wavelength of SMF-28 from its V. Computational — the
  two-route chromatic check as a convergence study in $\Delta\lambda$;
  eye-diagram closure vs $B$ across fiber presets; dispersion-shifted design:
  find the waveguide contribution needed to move the zero to 1.55 µm (uses
  46's $n_{\text{eff}}(\lambda)$ curve). Challenge — **the §35.4 skeleton**:
  end-to-end link simulator — 45's source linewidth, modulator as an on/off
  envelope, this module's fiber, part-04's propagator, a thresholded detector;
  report the achievable $B\cdot L$ frontier and which physics sets each
  segment of it.
- **Runtime budget:** ray ensembles $\le 10^4$ rays; packet propagation
  $\le 2^{14}$-point FFTs, a handful per cell; eye diagrams $\le 256$ traces —
  all seconds in Pyodide; animations ≤ 250 frames.
- **Validation gates:** standard set with `--module 47-fibers`; the §4
  fiber-limit, scaling, and cross-library chromatic tests land with this
  module — the capstone build will cite them.
- **Open questions for the author:** whether dB loss bookkeeping gets a short
  boxed primer or stays operational (recommendation: three-line box — the
  numbers are unreadable without it); whether graded-index gets a simulation
  or one figure (recommendation: figure only; the ray race stays step-index);
  whether the TAT-8 hook opens with the cable photo or the capacity graph
  (recommendation: cable cross-section photo — hardware first, curve second).

## 6. Part-level assessment and capstone hooks

- **Capstone §35.4 (optical communication system) is this part's capstone in all but
  name**: laser (45: source, linewidth, power) → modulator (envelope model, supplied
  by the capstone) → fiber (47: NA, V, loss window) → dispersion (47's budget over
  part-04's `waves.propagate_dispersive`) → detector (thresholded, noise via
  `wavelab.measurement`). 47's challenge problem is the capstone's skeleton; 45
  contributes the source model and $\hat{H}$-style link thinking inherited from
  `05-impulse-response` (part-01 §6's note). The capstone build cites the §4
  cross-library chromatic test as its correctness anchor.
- **Capstone §35.2 (virtual optical bench)** gains two engines: 43's $q$-propagation
  (mode matching as a bench task) and 44's cavity alignment/stability (the
  escape-time map as the bench's "alignment difficulty" meter).
- **The §36 research-connection chain** — normal modes → optical cavities → laser
  modes → cavity QED → quantum information — is realized across 07 → 44 → 45 and
  handed to `52-quantum-optics` exactly as the master plan sketches; 44's and 45's
  research boxes are its middle links, and the part's closing page says the chain
  out loud.
- **Cross-module synthesis problems** (live with the part, not one module):
  (a) *design a laser:* choose $R_1, R_2, L$ for a stable single-transverse-mode
  cavity with a target waist, compute its threshold with a given gain medium, and
  its longitudinal-mode count under the gain bandwidth — 43 + 44 + 45 in one
  artifact; (b) *fiber-coupled laser:* mode-match 44's output beam into 47's SMF-28
  via 43's two-lens design, computing the coupling efficiency as the overlap
  integral of the Gaussian with 46's fundamental mode profile — the whole part in
  one number (and an honest one: ~80% is a good answer); (c) *the lamp-vs-laser
  audit:* at equal wattage, compare radiance, coherence length, and achievable
  focused intensity — 45 + 27 + 43 closing the course's oldest promise
  quantitatively.
- **Exam themes:** one-line $q$-propagation problems; stability-diagram reading
  under time pressure; threshold and clamping reasoning from sketched
  output-vs-pump data; V-number and link-budget numerics with order-of-magnitude
  answers; and the synthesis question the part exists for — "name the earlier
  module this formula is wearing a costume of."

## 7. Build order and validation gates

Build order `43 → 44 → 45 → 46 → 47`, teaching order and dependency order aligned:
44 consumes 43's $q$ and Gouy phase; 45 consumes 44's loss rate and mode structure;
46 needs only parts 04/06/11/19 and could in principle parallel 44–45, but it stays
in sequence so 47 — which needs both 46's mode logic and 45's source model — lands
last, with the capstone seed complete.

`gaussian.py` lands in two increments: with 43 — the beam family (`rayleigh_range`,
`waist`, `curvature_radius`, `divergence`, `gouy_phase`, `q_parameter`,
`q_from_w_R`, `w_R_from_q`, `propagate_q`, `beam_through_system`, `field_amplitude`,
`hermite_gauss_mode`, `knife_edge_scan`, `waist_fit`) plus the sign-contract,
q-propagation, conservation, and knife-edge tests; with 44 — the cavity family
(`cavity_g`, `cavity_stability`, `stability_map`, `cavity_mode`, `round_trip_abcd`,
`mode_frequencies`) plus the trace-identity, confocal, and degeneracy tests.
`photonics.py` lands in three increments: with 45 — the laser family
(`rate_equations`, `steady_state_inversion`, `gain_coefficient`,
`cavity_loss_rate`, `threshold_pump`, `output_vs_pump`, `clamped_inversion`) plus
the two-level impossibility and clamping tests; with 46 — the slab family
(`tir_phase`, `slab_mode_condition`, `slab_modes`, `slab_mode_count`,
`slab_mode_profile`) plus the root-completeness and tail-limit tests; with 47 — the
fiber family (`numerical_aperture`, `acceptance_angle`, `v_number`, `mode_count`,
`modal_delay_spread`, `chromatic_broadening`, `dispersion_parameter`,
`bit_rate_limit`) plus the fiber limits, scaling, and the cross-library chromatic
consistency test (which requires parts 04 and 05's `waves.py` / `em.py` to be
merged — they precede this part in every ordering).

With each module, deposit its NEW registry entry into
`assessment/misconceptions.yml`, status `pending` until the page addresses it:
`perfect-lens-focuses-to-point` (43), `any-mirrors-make-cavity` (44),
`laser-bright-lamp` (45), `tir-guides-all-angles` (46), `thicker-fiber-more-data`
(47) — and its §5 glossary list into `glossary/terms.yml` (suggested Hebrew is a
proposal for the translator, README invariant 4; at 47, `numerical-aperture` is
cited from `36-instruments` per §4). `content/en/photonics/` is created with 43.

Per module: the standard four gates (README). Additionally: the §4 test increments
must land *with* their modules, since part-13's elective plans will cite the cavity
and beam guarantees, and the capstone cites the fiber ones.

## 8. Deviations from the master plan

- **Merge (12.1 + 12.2 → `43-gaussian-beams`):** beam parameters and propagation
  through lenses are one calculus — the $q$-parameter is thin without the ABCD rule
  and the ABCD rule for beams is contentless without $q$. Precedent:
  `02-damped-driven` ← 1.2 + 1.3; canonical per README module map.
- **Semiclassical-only laser scope:** master plan 12.4 says "keep the initial
  treatment semiclassical" — kept strictly: populations and photon *numbers*, no
  field quantization, spontaneous emission as a rate (and a mean seed $\beta$),
  Schawlow–Townes quoted as an order-of-magnitude with its quantum origin flagged
  as an `open-question` pointer to `52-quantum-optics`.
- **LP modes deferred:** master plan 12.6 lists "guided modes" for fibers; this
  plan states the V-number results with honest Bessel provenance ($V = 2.405$ as
  $J_0$'s first zero) and defers LP-mode algebra to 47's advanced tier and
  part-13. Rationale: the Bessel machinery buys no new physics at this level —
  discreteness, cutoff, and counting are all already earned in 46.
- **Nonlinear fiber optics deferred:** solitons and Kerr effects are research
  teasers in 47 only; `51-nonlinear-optics` (part-13) owns them. Mode locking is
  trailered in 44/45 and owned by `55-ultrafast`.
- **Sign convention (logged; the part's one systematic textbook clash):** the
  course's $e^{-\ii\omega t}$ makes the confined beam's parameter
  $q = z - \ii z_R$, the complex conjugate of Siegman's and Saleh & Teich's
  $e^{+\ii\omega t}$ form $q = z + \ii z_R$. Fixed once in §4's sign contract,
  boxed in 43's derive section, pinned by the $\Imag q < 0$ test; content quoting
  the engineering form carries the lint exception comment. The ABCD law itself is
  convention-neutral (real matrices).
- **Resonator mirror signs:** cavity work uses the resonator convention (concave
  facing the cavity: $R > 0$) with the dictionary to `rayoptics.mirror`'s Hecht
  sign applied inside `cavity_g` / `round_trip_abcd` — stated once, never mixed
  in content.
- **Additions beyond master plan §19:** the Gouy phase explained via the angular
  spectrum and cashed out as the confocal degeneracy (a designed discovery); the
  mode-matching / knife-edge measurement culture in 43; the Einstein
  thermodynamic argument, the two-level trap as a pinned test, and *measured*
  gain clamping in 45; guidance derived by transverse resonance with 19's TIR
  phases in 46; real engineering numbers (loss windows, dispersion parameters,
  $B\cdot L$ budgets, SMF-28's spec sheet reproduced) in 47; five NEW registry
  misconceptions with falsifying experiments; the explicit §35.4 capstone
  skeleton.
- **Terminology:** "mode" is disambiguated once, in 44 (longitudinal vs
  transverse) and again in 46/47 (guided); TEM$_{mn}$ introduced as the
  laser-lab dialect for HG$_{mn}$; `finesse` / `linewidth` / `photon-lifetime`
  vocabulary is 26's, cited not redefined — this part adds no competing terms.
