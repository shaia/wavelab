# Part XIII — Optional Advanced Modules (Electives) — Implementation Plan

> **Master plan:** §20 (optional advanced modules), §36 (Research Connection tier).
> **Modules:** `50-holography`, `51-nonlinear-optics`, `52-quantum-optics`, `53-computational-imaging`,
> `54-photonic-crystals`, `55-ultrafast` — plus one-paragraph stubs for every remaining §20 topic.
> **Status:** planned (all elective — never blocks core).
> Canonical numbering, invariants, and conflict log: [README.md](README.md).
>
> Deliberately **lighter** than the core part plans: six outlined electives with condensed specs, no
> new library files at planning stage (§4, logged in §8), stubs for the rest of §20.

## 1. Part overview and narrative arc

Part XIII is the course's set of open ends. The master plan's §36 gives every notebook a Research
Connection tier — a box pointing from the module's physics toward where it lives in modern research.
The electives are those boxes made whole: each takes one such pointer, planted deliberately by an
earlier plan, and grows it into a full module. Nothing here is required; every elective is a door,
not a corridor.

The design principle, stated honestly: **each elective is a thin new layer on machinery the core
course already built.** Holography is the extreme case — roughly 90% reuse: recording a hologram
*is* two-beam interference (`interference.py`, wholesale), reconstructing one *is* diffraction
(`diffraction.py`, wholesale); the one new idea is that an interference pattern, illuminated,
diffracts the object wave back into existence. Photonic crystals promote part-02's lattice
dispersion to optics — `coupled.chain_dispersion` and the 1-D stack band structure are the *same*
folded curve gapping by the same zone-edge mechanism, and the module says so out loud. Ultrafast
optics is module 00's N-coherent-arrows argument at its most literal: a mode-locked pulse train is
nothing but the phasor sum of N phase-locked cavity lines. Nonlinear optics adds one term — an
anharmonic spring — to the Lorentz oscillator of modules 01/02/16 and gets second-harmonic
generation out. Quantum optics re-reads module 00's random walk as photon statistics and module 21's
Jones matrices as qubit gates. Computational imaging turns part-11's PSF/OTF machinery around: given
the blur, compute it back out.

**Invariant (course-wide):** every module in this part is OPTIONAL. Nothing in core parts 0–XII may
depend on any 50+ module — no prerequisite edge, no library import, no quiz reference. The only
forward reference in built content is `content/en/oscillations/01-sho.md`'s "nonlinear optics
(module 20)" pointer, re-pointed by the README conflict log to `51-nonlinear-optics`; module 51
keeps that promise. Electives may depend on core modules and on each other (55 → 51 for the
autocorrelation teaser is the one such soft edge), never the reverse.

## 2. Position in the course

- **Requires (per elective; specific results):**
  - `50-holography`: `23-interference` (the cross term $2\sqrt{I_1I_2}\cos\delta$ carries phase);
    `29-fraunhofer` + `32-fresnel-diffraction` (`fraunhofer_pattern`, `angular_spectrum_propagate`);
    `38-spatial-frequencies` (carrier/sideband reading of fringes).
  - `51-nonlinear-optics`: `02-damped-driven` (Lorentzian response); `16-light-in-matter`
    (`em.lorentz_susceptibility`, `em.refractive_index` — dispersion is why phase matching is hard);
    `20-polarization` + `21-jones-calculus` (birefringence, the fix); `01-sho` advanced section.
  - `52-quantum-optics`: `00-phasors` (`phasors.random_phasor_sum` — random-walk machinery reused
    for photon statistics); `21-jones-calculus` (the advanced qubit box is this module's entry
    ramp); `23-interference` + `25-michelson` (amplitude interferometry); `27-coherence`.
  - `53-computational-imaging`: `40-psf-otf` + `42-4f-processor` (image formation as convolution —
    machinery cited by module id, reused not rebuilt); `04-fourier-transform` (convolution theorem,
    phase-information thread); `37-aberrations` (the Zernike / adaptive-optics research box).
  - `54-photonic-crystals`: `06-coupled` + `07-normal-modes` (`coupled.chain_dispersion`);
    `24-thin-films` + `26-fabry-perot` (`interference.transfer_matrix_stack` — part-08's multilayer
    advanced trailer is this module's engine); `13-dispersion` (reading $\omega(k)$ diagrams).
  - `55-ultrafast`: `00-phasors` (`phasors.superpose`); `04-fourier-transform` (bandwidth theorem,
    `fourier.rms_widths`); `12-wave-packets` + `13-dispersion` (`waves.propagate_dispersive`,
    chirp); `26-fabry-perot` (`interference.fsr`); `44-resonators` / `45-lasers` by module id.
    Soft edge: `51-nonlinear-optics` for the SHG autocorrelation teaser.
- **Feeds:** nothing — terminal by design (the §1 invariant); electives cross-link among themselves
  forward-only where noted.
- **Explicitly not assumed:** quantized field theory (52 stays at amplitude-plus-statistics level);
  coupled-mode theory; anisotropic crystal optics beyond what 20/21 built; graduate nonlinear
  formalism (51 is phenomenology plus one honest oscillator).

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|
| `50-holography` | `content/en/advanced/50-holography.md` | Holography: interference recorded, diffraction replayed | §20: holography | Goodman, holography; Hecht, holography section | planned (elective) |
| `51-nonlinear-optics` | `content/en/advanced/51-nonlinear-optics.md` | Nonlinear optics: the anharmonic oscillator and SHG | §20: nonlinear optics, second-harmonic generation | Boyd, nonlinear susceptibilities & SHG; Saleh & Teich | planned (elective) |
| `52-quantum-optics` | `content/en/advanced/52-quantum-optics.md` | Quantum optics: one photon at a time | §20: quantum optics, single-photon interference, squeezed light | Loudon or Gerry & Knight; Saleh & Teich, photon optics | planned (elective) |
| `53-computational-imaging` | `content/en/advanced/53-computational-imaging.md` | Computational imaging: measure, then compute | §20: computational imaging (+ adaptive-optics note) | Goodman, inverse/holographic imaging; Saleh & Teich | planned (elective) |
| `54-photonic-crystals` | `content/en/advanced/54-photonic-crystals.md` | Photonic crystals: dispersion gets a band gap | §20: photonic crystals | Saleh & Teich, photonic-crystal optics; Joannopoulos (further) | planned (elective) |
| `55-ultrafast` | `content/en/advanced/55-ultrafast.md` | Ultrafast optics: the shortest events ever made | §20: ultrafast optics | Saleh & Teich, ultrafast optics; Boyd (SHG autocorrelation) | planned (elective) |

Companions extend the template's standard hierarchy: Saleh & Teich is the general part-XIII
companion; Boyd is specific to 51 (and 55's measurement), Goodman to 50/53, Loudon / Gerry & Knight
to 52. Chapters cited by topic, never number.

## 4. Shared infrastructure for this part

**No new `src/wavelab` files at planning stage** — this part's deliberate infrastructure decision
(logged in §8). Every elective runs primarily on machinery owned by core plans; each §5 spec names
the functions it reuses. Where an elective genuinely needs new code, it flags **at most 2–3
functions** below as *elective-local, specced when scheduled*: signatures, contracts, docstring
model specs, file placement, and the README ownership row are written only when that elective is
promoted to the build queue. Until then the names are reservations, not definitions.

**Existing machinery reused (by owner):** part-00 — `phasors.superpose`,
`phasors.random_phasor_sum`, `fourier.spectrum` / `inverse_spectrum`, `fourier.rms_widths`,
`fourier.convolve`; part-02 — `coupled.chain_dispersion` (54: the same curve, not an analogy);
part-04 — `waves.propagate_dispersive`, `waves.group_velocity` (55); part-05 —
`em.lorentz_susceptibility`, `em.refractive_index` (51); part-07 — `polarization.jones_hwp` /
`jones_qwp` / `cascade` (52's gate dictionary); part-08 — `interference.two_beam_intensity`,
`transfer_matrix_stack`, `fsr`, `finesse`, `fp_spectrum`, `visibility` (50, 54, 55); part-09/11 —
`fraunhofer_pattern`, `angular_spectrum_propagate`, `airy_radius`, `rayleigh_criterion` (50, 53),
all other imaging machinery by module id (40, 42); shared — `measurement`, `validation` throughout.

**Elective-local functions flagged (specced when scheduled; ≤ 3 per elective):**

| Elective | Flagged names | One-line role |
|---|---|---|
| 50 | `record_hologram`, `reconstruct_hologram` | $\|E_o+E_r\|^2$ on a grid; pattern × replay beam → `angular_spectrum_propagate` |
| 51 | `anharmonic_response`, `shg_field` | driven $\ddot x + \gamma\dot x + \wnat^2 x + \beta x^2 = F/m$ integrator; undepleted-pump $E_{2\omega}(z;\Delta k)$ |
| 52 | `photon_counts`, `g2_zero` | seeded click streams for coherent/thermal/single-photon sources; $g^{(2)}(0)$ estimator |
| 53 | `wiener_deconvolve`, `gerchberg_saxton` | $H^*/(\|H\|^2 + 1/\mathrm{SNR})$ filter; alternating-projection phase retrieval |
| 54 | `bloch_wavenumber` | bands from the unit-cell transfer matrix, $\cos(K\Lambda) = \tfrac12\operatorname{Tr}M$ |
| 55 | `mode_locked_train`, `autocorrelation_trace` | N-mode phasor sum with settable phases; $\int I(t)\,I(t-\tau)\,dt$ |

**`tests/physics/` additions:** none at planning stage — each elective's tests are specced with its
functions when scheduled (the §5 verify seeds name the physics they must pin). **Shared media:** one
render script per elective when scheduled (`media/render/render_<topic>.py`; shot lists in §5).
**Glossary themes:** each elective deposits its own short list (§5); stubs deposit nothing.

## 5. Module specifications

### 5.1 `50-holography` — Interference recorded, diffraction replayed

- **Identity and scope:** off-axis hologram recording and reconstruction, end-to-end in simulation;
  digital holography as the lab. Reuse is near-total (~90%): recording is part-08 interference,
  reconstruction is part-09 diffraction; the one new idea is that the stored fringes *are* the
  object wave, releasable by illumination. Deferred: volume holograms (one sentence toward 54),
  rainbow/display holography.
- **Prerequisites:** §2 list — 23, 29, 32, 38.
- **Learning objectives:**
  - `OBJ-50-1` — Explain recording as interference: the plate stores I = |E_o + E_r|^2, whose cross
    terms E_o conj(E_r) + conj(E_o) E_r keep the object wave's amplitude AND phase — the
    information a photograph discards.
  - `OBJ-50-2` — Derive the three reconstruction orders (zero order, virtual image, conjugate) by
    expanding t(x,y) E_r, and choose an off-axis carrier angle that separates them.
  - `OBJ-50-3` — Simulate record-and-reconstruct end-to-end with angular-spectrum propagation and
    identify each order in the output field.
  - `OBJ-50-4` — Predict what a cropped hologram fragment reconstructs (whole scene, reduced
    resolution) using aperture-resolution reasoning.
- **Section skeleton seeds:**
  - *puzzle:* photograph vs hologram of one scene — only one shows parallax; what did the other plate throw away?
  - *predict:* stored point-by-point? (targets `hologram-stores-image-pointwise`); cut in half — half the scene or all?; reference beam alone?; replay at another wavelength?
  - *explore:* record/replay sandbox — object, reference-angle slider, crop mask; live fringes, spatial spectrum (three lobes), reconstruction.
  - *derive:* recording law → transmission expansion → off-axis separation condition (below).
  - *verify:* reconstruction vs object field in the virtual-image window (`numerical-observation`: error vs carrier angle); fragment resolution vs crop size per `rayleigh_criterion` reasoning.
  - *transfer:* holographic elements (a lens = recorded zone plate, 32); digital holographic microscopy; recordable 4-f filters (`42-4f-processor`); volume holograms → `54-photonic-crystals`.
  - *quiz:* information content; order separation; fragment reconstruction; carrier-angle numeric.
  - *explain:* to a photographer, what a hologram stores that film cannot; why lasers made holography practical (coherence, one sentence of 27).
  - *advanced:* thin vs volume gratings, Bragg selectivity (safe to skip; feeds nothing).
- **Core derivations:** (1) recording + replay: $I = |E_o|^2 + |E_r|^2 + E_oE_r^* + E_o^*E_r$; with
  $t \propto I$ and replay beam $E_r$, the term $E_o|E_r|^2$ is the object wave again, $E_o^*E_r^2$
  its conjugate; for a plane reference $E_r = A\,e^{\ii kx\sin\theta}$ the three terms sit at
  spatial-frequency offsets $0, \pm k\sin\theta$ — separation demands a carrier above three halves
  of the object bandwidth. (2) a cropped hologram is an aperture on the reconstructed wave:
  resolution degrades per `airy_radius` scaling while the field of view survives.
- **Model spec draft:** System — scalar monochromatic 2-D fields: object, reference, recorded
  intensity, replayed field. Dynamics — none; intensity detection, then linear propagation.
  Boundary — thin planar medium, linear $t \propto I$, paraxial distances. Ensemble — deterministic;
  lab noise via `measurement`. Ignored — saturation, thickness (Bragg) effects, polarization. Valid
  when — object bandwidth below carrier separation and grid Nyquist. Failure modes — overlapping
  orders; aliased fringes; reading the conjugate as the object.
- **Misconceptions:** NEW `hologram-stores-image-pointwise` — "A hologram stores the picture the way
  film does, each piece holding one piece of the scene." Falsifier: crop the simulated hologram to a
  quarter and reconstruct — the whole scene appears at lower resolution, following aperture
  diffraction. Distractor: "half the hologram shows half the scene."
- **Glossary terms:** `hologram` (הולוגרמה), `reference-beam` (אלומת ייחוס), `twin-image`
  (תמונת תאום — translator to confirm), `off-axis-hologram` (הולוגרמה מחוץ לציר).
- **Lab outline:** (1) record: object + reference, fringes and spectrum; (2) replay, window the
  three orders; (3) crop study — resolution vs fragment size, fitted; (4) *measurement:* a feature
  size from its reconstruction, value ± uncertainty across noise seeds.
- **Media** (`render_holography.py`): (a) fringes forming as the beams interfere; (b) replay — the
  three orders separating as the carrier angle grows.
- **Quiz outline:** `Q-50-1` MC information content (OBJ-50-1, distractor
  `hologram-stores-image-pointwise`); `Q-50-2` numeric carrier angle (OBJ-50-2); `Q-50-3` MC label
  the orders in a spectrum (OBJ-50-2/3); `Q-50-4` MC cropped-fragment prediction (OBJ-50-4).
- **Runtime note:** grids ≤ 1024², two FFT propagations per replay — ~1 s in Pyodide.
- **Open questions:** photographic object (fun) vs synthetic letters (clean spectra); does the
  conjugate image earn its own subsection.

### 5.2 `51-nonlinear-optics` — The anharmonic oscillator and second-harmonic generation

- **Identity and scope:** one new term in the Lorentz oscillator → new frequencies; SHG growth with
  phase matching as the central constraint; $\chi^{(2)}$/$\chi^{(3)}$ phenomenology, Kerr teaser.
  **Keeps 01-sho's promise:** the built page's "nonlinear optics (module 20)" reference re-points
  here per the README conflict log — this module is that link's destination and opens by picking up
  the anharmonic pendulum where 01's advanced section left it. Deferred: pump depletion,
  quasi-phase-matching detail, parametric processes.
- **Prerequisites:** §2 list — 02, 16, 20/21, 01-advanced.
- **Learning objectives:**
  - `OBJ-51-1` — Show that a driven anharmonic oscillator x'' + gamma x' + omega0^2 x + beta x^2 =
    (qE/m) cos(omega t) responds at 2 omega and DC with amplitudes proportional to E^2, and map
    this onto P = eps0 (chi1 E + chi2 E^2 + chi3 E^3 + ...).
  - `OBJ-51-2` — Derive the undepleted-pump SHG intensity I(2 omega) proportional to
    L^2 sinc^2(Delta k L / 2) and compute the coherence length L_c = pi / |Delta k|.
  - `OBJ-51-3` — Explain phase matching as index matching n(omega) = n(2 omega), show normal
    dispersion forbids it, and evaluate the birefringent fix numerically.
  - `OBJ-51-4` — Estimate Kerr phenomenology: n = n0 + n2 I; self-phase modulation and
    self-focusing as one-line consequences (qualitative).
- **Section skeleton seeds:**
  - *puzzle:* a green laser pointer contains no green source — IR in, 532 nm out; where does a *new color* come from when linear systems answer only at the driving frequency?
  - *predict:* can a linear medium change frequency?; double the pump — SHG ×2 or ×4?; longer crystal always better? (targets `phase-matching-automatic`); why did SHG wait for the laser?
  - *explore:* anharmonic scope ($\beta$, drive; spectrum grows $2\omega$ and DC lines); SHG panel ($L$, $\Delta k$; oscillating vs growing $I_{2\omega}(L)$).
  - *derive:* perturbative response → $\chi^{(2)}$ dictionary → growth with mismatch → phase matching and the birefringent escape (below).
  - *verify:* second-harmonic line scales as drive² over two decades (`numerical-observation`: fitted exponent); `shg_field` vs analytic sinc; $L_c$ from `em.refractive_index` for a real glass.
  - *transfer:* $\chi^{(2)} = 0$ in centrosymmetric media, fibers get $\chi^{(3)}$; frequency combs; autocorrelation in `55-ultrafast`; electro-optics stub (Pockels = $\chi^{(2)}$ with a DC leg).
  - *quiz:* scaling numeric; coherence-length numeric; phase-matching MC; symmetry MC.
  - *explain:* why "the spring is slightly wrong" creates colors; why intensity, not energy, matters; why the crystal must be asymmetric.
  - *advanced:* quasi-phase-matching — flip the crystal sign every $L_c$, rectify the oscillation (safe to skip).
- **Core derivations:** (1) perturbation: $x = x^{(1)} + x^{(2)}$ with $x^{(1)}$ the module-02
  Lorentzian response at $\omega$; $\beta(x^{(1)})^2$ drives $x^{(2)}$ at $2\omega$ and 0,
  amplitudes $\propto E^2$. (2) growth with mismatch: each slab $dz$ contributes
  $\propto e^{\ii\Delta k z}\,dz$, $\Delta k = k(2\omega) - 2k(\omega) =
  (2\omega/c)[n(2\omega) - n(\omega)]$; the phasor integral (module 00's arc of arrows, literally)
  gives $|E_{2\omega}(L)| \propto L\,|\mathrm{sinc}(\Delta k L/2)|$ — power walks in a circle
  unless $\Delta k = 0$.
- **Model spec draft:** System — anharmonic Lorentz oscillators driving a scalar second-harmonic
  field in 1-D. Dynamics — perturbative response; undepleted pump. Boundary — uniform crystal of
  length $L$, plane waves. Ensemble — deterministic. Ignored — pump depletion, walk-off,
  absorption, the tensor character of $\chi^{(2)}$. Valid when — conversion ≪ 1, $\beta x \ll
  \wnat^2$. Failure modes — extrapolating $L^2$ past depletion; $\chi^{(2)}$ claims in
  centrosymmetric media; forgetting dispersion in $\Delta k$.
- **Misconceptions:** NEW `phase-matching-automatic` — "Any long-enough nonlinear crystal converts
  more and more light to the second harmonic." Falsifier: integrate `shg_field` with
  $\Delta k \ne 0$ — output oscillates with period $2L_c$, never exceeding the first maximum; only
  $\Delta k = 0$ grows as $L^2$. Distractor: "doubling the length always quadruples SHG output."
- **Glossary terms:** `nonlinear-susceptibility` (רגישות לא-ליניארית), `second-harmonic-generation`
  (יצירת הרמוניה שנייה), `phase-matching` (תיאום מופע), `kerr-effect` (אפקט קר).
- **Lab outline:** (1) drive-scaling of the $2\omega$ line (log-log fit → slope 2); (2) growth vs
  $L$ at several $\Delta k$, extract $L_c$; (3) phase-matching search — sweep birefringent
  $n_e(\theta)$ against $n_o$; (4) *measurement:* $L_c$ ± uncertainty from noisy growth data.
- **Media** (`render_nonlinear.py`): (a) response spectrum as $\beta$ ramps — harmonics sprouting;
  (b) the SHG phasor arc straightening as $\Delta k \to 0$.
- **Quiz outline:** `Q-51-1` numeric drive scaling (OBJ-51-1); `Q-51-2` numeric $L_c$ from indices
  (OBJ-51-2); `Q-51-3` MC longer-crystal prediction (OBJ-51-2/3, distractor
  `phase-matching-automatic`); `Q-51-4` MC $\chi^{(2)}$ symmetry + Kerr one-liner (OBJ-51-1/4).
- **Runtime note:** ODE runs ≤ 10⁴ steps; growth integrals vectorized — trivial in Pyodide.
- **Open questions:** tensor $\chi^{(2)}$ — honest paragraph or footnote; how far the Kerr teaser
  goes (self-focusing figure or text only).

### 5.3 `52-quantum-optics` — One photon at a time

- **Identity and scope:** what survives of the course when light arrives as clicks: single-photon
  interference and which-path complementarity at amplitude level (amplitudes are course phasors,
  probabilities their squared magnitudes), delayed choice, photon statistics ($g^{(2)}(0)$ for
  coherent / thermal / single-photon light — module 00's random-walk machinery reused), the
  Jones-as-qubit-gates payoff (part-07's advanced box), squeezed light qualitatively. Deferred:
  field quantization proper, entanglement/Bell, cavity QED (named as the §36 chain's next rungs).
- **Prerequisites:** §2 list — 00, 21 (advanced box), 23, 25, 27.
- **Learning objectives:**
  - `OBJ-52-1` — Compute single-photon interference as amplitude superposition with probabilistic
    detection: P(x) proportional to |a_1(x) + a_2(x)|^2; fringes build click by click and vanish
    when which-path information exists.
  - `OBJ-52-2` — Classify light by photon statistics: g2(0) = 1 (coherent/Poisson), 2
    (thermal/bunched), 0 (single photon/antibunched) — and explain why g2(0) < 1 has no classical
    wave model.
  - `OBJ-52-3` — Use Jones matrices as single-qubit gates (HWP at 22.5 deg = Hadamard; polarizer =
    projective measurement), completing module 21's advanced box.
  - `OBJ-52-4` — Describe squeezed light qualitatively: uncertainty area conserved but
    redistributable between quadratures; why interferometers (LIGO) use it.
- **Section skeleton seeds:**
  - *puzzle:* dim the double slit to one photon per microsecond — single clicks, yet the dots draw module 23's fringes; what went through both slits?
  - *predict:* fringes at one-at-a-time rates?; do photons interfere with each other? (targets `photons-interfere-with-each-other`); mark the slit — fringes?; can clicks be *less* random than a laser's?
  - *explore:* click accumulator (rate, which-path toggle, delayed-choice switch; dots → fringes live); statistics sandbox (source type; click raster, running $g^{(2)}(0)$).
  - *derive:* amplitude rules → click-by-click build-up → which-path erasure → $g^{(2)}$ and its three canonical values → classical bound (below).
  - *verify:* click histogram → `interference.two_beam_intensity` with $1/\sqrt{N}$ residual (`numerical-observation`); `g2_zero` on seeded streams hits 1 / 2 / 0; thermal stream from `phasors.random_phasor_sum` intensities.
  - *transfer:* the §36 chain onward — cavity QED, quantum information; QKD from the gate dictionary; `27-coherence` re-read as first- vs second-order coherence; squeezing → metrology.
  - *quiz:* click-rate fringe MC; $g^{(2)}$ classification numeric; Hadamard numeric; squeezing MC.
  - *explain:* what "went through both slits" does and does not claim; why antibunching is the quantum smoking gun while interference is not; the qubit dictionary in your own words.
  - *advanced:* delayed choice run honestly at amplitude level — choosing after the slit changes nothing observable (safe to skip).
- **Core derivations:** (1) detection statistics: fringes as $P(x)\,dx$ per click, sampled;
  which-path marking multiplies the cross term by distinguishability — module 27's $|\gamma|$
  reappears as an overlap of marker states. (2) for classical intensities
  $g^{(2)}(0) = \langle I^2\rangle/\langle I\rangle^2 \ge 1$ (variance non-negative — `theorem`);
  random phasor sums give 2; a one-photon source cannot double-click, $g^{(2)}(0) = 0$, so the
  bound breaks (`empirical-law`: antibunching observed).
- **Model spec draft:** System — one photon's amplitudes over discrete paths/modes; seeded click
  streams at detectors. Dynamics — linear amplitude maps (beam splitters, Jones elements);
  detection converts $|a|^2$ to Bernoulli/Poisson clicks. Boundary — ideal lossless elements,
  unit-efficiency detectors by default. Ensemble — the whole point: every result is an ensemble
  over seeded repetitions. Ignored — field quantization, multi-photon amplitudes, entanglement,
  dark counts. Valid when — one photon in the apparatus at a time; statistics over many trials.
  Failure modes — one stream read as an ensemble; $g^{(2)} < 1$ explained as a wave effect.
- **Misconceptions:** NEW `photons-interfere-with-each-other` — "Low-light fringes come from
  different photons interfering with each other." Falsifier: simulated visibility is independent
  of arrival rate down to one photon per apparatus lifetime; each click samples $|a_1 + a_2|^2$
  alone. Distractor: "below one photon at a time the fringes disappear."
- **Glossary terms:** `photon` (פוטון), `photon-statistics` (סטטיסטיקת פוטונים), `antibunching`
  (אנטי-התקבצות — translator to confirm), `squeezed-light` (אור דחוס), `which-path-information`
  (מידע איזה-מסלול — translator to decide).
- **Lab outline:** (1) click accumulator — visibility vs $N$; (2) which-path toggle — visibility
  vs distinguishability; (3) `photon_counts` + `g2_zero` for three sources, tabulated with
  uncertainties; (4) *measurement:* classify an unlabeled seeded stream by $g^{(2)}(0)$ ± error.
- **Media** (`render_quantum.py`): (a) dots accumulating into fringes; (b) three click rasters
  (coherent/thermal/single-photon) side by side, visibly different clustering.
- **Quiz outline:** `Q-52-1` MC low-rate fringes (OBJ-52-1, distractor
  `photons-interfere-with-each-other`); `Q-52-2` numeric $g^{(2)}$ classification (OBJ-52-2);
  `Q-52-3` numeric HWP-as-Hadamard transform (OBJ-52-3); `Q-52-4` MC quadratures (OBJ-52-4).
- **Runtime note:** click streams ≤ 10⁶ samples, pure NumPy sampling — ~1 s in Pyodide.
- **Open questions:** delayed choice — advanced or core subsection; how explicitly to write the
  "amplitudes are not fields" caveat without field quantization to lean on.

### 5.4 `53-computational-imaging` — Measure, then compute

- **Identity and scope:** imaging where computation is half the instrument: Wiener deconvolution
  (modules 40/42's PSF/OTF machinery reused wholesale, cited by id), Gerchberg–Saxton phase
  retrieval (spectacular and simple with FFTs — module 04's phase-information thread made
  constructive), lensless/coded-aperture teasers, and an adaptive-optics note completing part-10's
  Zernike research box (module 37). Deferred: compressed sensing, iterative reconstruction beyond
  GS, learned priors (named in transfer).
- **Prerequisites:** §2 list — 40, 42, 04, 37.
- **Learning objectives:**
  - `OBJ-53-1` — Implement Wiener deconvolution W = conj(H) / (|H|^2 + 1/SNR) on a blurred noisy
    image and explain why the naive inverse 1/H amplifies noise wherever the OTF is small.
  - `OBJ-53-2` — Recover phase from intensity-only data with the Gerchberg-Saxton algorithm and
    relate its success to the redundancy of two-plane measurements.
  - `OBJ-53-3` — Explain lensless / coded-aperture imaging as "measure a coded blur, then decode":
    the aperture is chosen for invertibility, not sharpness.
  - `OBJ-53-4` — Describe adaptive optics as measure-then-correct in the Zernike alphabet, and
    contrast correcting before detection (AO) with after (deconvolution).
- **Section skeleton seeds:**
  - *puzzle:* a blurred photo whose blur (the PSF) is *known* — the pixels are all there, scrambled by a convolution you can write down; can arithmetic un-take the photo?
  - *predict:* is sharpening just division?; deconvolve past the diffraction limit? (targets `deconvolution-beats-diffraction`); 04 says $|F|$ alone fails — what second measurement fixes it?; a camera with no lens?
  - *explore:* deconvolution bench (kernel, noise, SNR knob; live restored image and artifacts); GS viewer (error vs iteration, phase map emerging).
  - *derive:* Wiener from least squares → OTF zeros and the information they destroy → GS as alternating projections → coded-aperture sketch (below).
  - *verify:* `wiener_deconvolve` beats naive inverse in RMS error across seeds (`numerical-observation`: error vs SNR knob has an interior optimum); GS error monotone, phase recovered to a constant offset.
  - *transfer:* `airy_radius` / `rayleigh_criterion` — what deconvolution cannot buy back; module 37's JWST box → lucky imaging; computational photography; phase retrieval in X-ray lensless imaging.
  - *quiz:* Wiener-vs-inverse MC; OTF-zero conceptual; GS ingredients MC; AO-vs-deconvolution MC.
  - *explain:* "information gone" vs "information scrambled"; why the SNR term is a confession of ignorance, not a fudge; a lensless camera to a phone designer.
  - *advanced:* regularization as prior knowledge — one honest paragraph toward modern reconstruction (safe to skip).
- **Core derivations:** (1) Wiener: minimize $\langle|f_{\text{est}} - f|^2\rangle$ over linear
  filters for $g = h*f + n$ → $W = H^*/(|H|^2 + N/S)$; the naive inverse is the $N \to 0$ limit,
  and at OTF zeros the estimate honestly returns nothing rather than amplified noise. (2) GS:
  impose measured magnitudes alternately in two planes connected by `fraunhofer_pattern`-style
  transforms; error non-increasing (projection argument sketched — `theorem` for monotonicity,
  `numerical-observation` for recovery quality).
- **Model spec draft:** System — discrete images tied to objects by known linear convolutional
  forward models plus noise. Dynamics — none; forward model, then estimation. Boundary — periodic
  (FFT) boundaries, shift-invariant PSF. Ensemble — seeded noise realisations; every quality claim
  is an ensemble statement. Ignored — shift-variant blur, nonlinear sensors, PSF model error.
  Valid when — the forward model is known and linear; noise roughly stationary. Failure modes —
  dividing by OTF zeros; GS stagnation read as convergence; expecting detail beyond $H$'s support.
- **Misconceptions:** NEW `deconvolution-beats-diffraction` — "With enough computation you can
  deconvolve past the diffraction limit." Falsifier: outside the OTF support $H = 0$ exactly; the
  Wiener estimate there is zero regardless of SNR — restored two-point resolution saturates at the
  `rayleigh_criterion` scale as SNR → ∞. Distractor: "a large enough SNR knob recovers arbitrarily
  fine detail."
- **Glossary terms:** `deconvolution` (דה-קונבולוציה — translator to decide), `phase-retrieval`
  (שחזור מופע), `coded-aperture` (מפתח מקודד — translator to confirm), `adaptive-optics`
  (אופטיקה אדפטיבית).
- **Lab outline:** (1) blur-and-restore with module-40 machinery (by id), naive vs Wiener across
  noise levels; (2) sweep the SNR knob, find the error minimum; (3) GS on a letter-phase object,
  error curve; (4) *measurement:* restored two-point separation limit ± uncertainty vs
  `rayleigh_criterion`.
- **Media** (`render_computational.py`): (a) naive inverse exploding as noise ramps, Wiener
  stable; (b) GS phase map emerging over iterations.
- **Quiz outline:** `Q-53-1` MC why the naive inverse fails (OBJ-53-1); `Q-53-2` MC what GS needs
  (OBJ-53-2); `Q-53-3` MC diffraction-limit claim (OBJ-53-1/3, distractor
  `deconvolution-beats-diffraction`); `Q-53-4` MC AO vs deconvolution ordering (OBJ-53-4).
- **Runtime note:** 512² FFT pipelines, GS ≤ 100 iterations at 256² — seconds in Pyodide.
- **Open questions:** which coded aperture (URA vs random) makes the cleanest teaser; does the AO
  note carry a small simulated correction figure or text only.

### 5.5 `54-photonic-crystals` — Dispersion gets a band gap

- **Identity and scope:** part-02's lattice dispersion promoted to optics: Bloch waves in a 1-D
  periodic stack via unit-cell transfer matrices (part-08's multilayer advanced trailer,
  `interference.transfer_matrix_stack`, run to infinity), band gaps, Bragg mirrors as finite
  crystals operated at the gap, defect modes as cavities. Central honesty claim: the band diagram
  is the SAME curve as `coupled.chain_dispersion` — chain and stack fold and gap by the identical
  mechanism, plotted side by side. Deferred: 2-D/3-D crystals, density of states, slow light.
- **Prerequisites:** §2 list — 06/07, 24/26, 13.
- **Learning objectives:**
  - `OBJ-54-1` — Compute the Bloch band structure of a periodic bilayer from the unit-cell
    transfer matrix via cos(K Lambda) = (1/2) Tr M, identifying gaps where |Tr M| > 2.
  - `OBJ-54-2` — Map the photonic band diagram onto the mass-spring chain dispersion of modules
    06/07: same zone folding, same gap-at-the-zone-edge mechanism.
  - `OBJ-54-3` — Design a quarter-wave Bragg mirror and show its high-reflectance band converges
    to the infinite crystal's gap as layer count grows.
  - `OBJ-54-4` — Predict defect modes: a spacer inside the stack is a Fabry-Perot cavity whose
    resonance lives inside the gap.
- **Section skeleton seeds:**
  - *puzzle:* two transparent glasses, each layer passing ≥ 96% — yet 20 pairs reflect 99.99% in a color band; how do transparent materials build a perfect mirror, and why only some colors?
  - *predict:* more layers — 100% or saturating?; light that *cannot propagate* in the infinite stack?; where does a defect resonance sit?; is the forbidden light absorbed? (re-runs `interference-destroys-energy`).
  - *explore:* band-structure lab — $n_1, n_2, d_1, d_2$ sliders; live $\cos(K\Lambda)$ trace with ±1 rails, band diagram, finite-stack reflectance ($N$ slider); a second tab overlays `coupled.chain_dispersion` on the same axes — the same curve, visibly.
  - *derive:* unit-cell matrix → Bloch condition → gap criterion → quarter-wave case → defect mode (below).
  - *verify:* `bloch_wavenumber` gap edges vs the analytic quarter-wave gap width (`numerical-observation`); finite-stack $R \to 1$ inside the gap as $1 - O(e^{-2N\kappa\Lambda})$, fitted; defect resonance vs `interference.fp_spectrum` with mirror-phase corrections.
  - *transfer:* fiber Bragg gratings (`47-fibers` by id); laser mirrors (`44-resonators` by id); structural color closing `24-thin-films`; electronic band gaps — the same mathematics with matter waves; volume holograms (50-advanced) as recorded crystals.
  - *quiz:* gap-criterion reading; quarter-wave design numeric; chain-analogy MC; defect-mode MC.
  - *explain:* why transparent layers can forbid propagation, in interference language; what is and is not analogous between phonon and photon bands; a Bragg mirror to a laser engineer.
  - *advanced:* oblique incidence and the omnidirectional-gap question; 2-D/3-D crystals, inverse opals (safe to skip).
- **Core derivations:** (1) Bloch: for unit-cell matrix $M$ (built from `transfer_matrix_stack`
  factors), $\psi(x+\Lambda) = e^{\ii K\Lambda}\psi(x)$ makes $e^{\ii K\Lambda}$ an eigenvalue of
  $M$; with $\det M = 1$, $\cos(K\Lambda) = \tfrac12\operatorname{Tr}M$ — real $K$ (bands) where
  $|\operatorname{Tr}M| \le 2$, evanescent Bloch waves (gaps) beyond — the identical algebra that
  gapped the diatomic chain in module 07. (2) quarter-wave gap: at $d_i = \lambda_0/4n_i$ the
  fractional width is $\Delta\omega/\omega_0 = (4/\pi)\arcsin[(n_2-n_1)/(n_2+n_1)]$ — index
  contrast sets the gap, layer count sets how black the mirror is inside it.
- **Model spec draft:** System — 1-D lossless periodic bilayer stack, normal incidence, scalar
  amplitudes per part-08 conventions. Dynamics — none; stationary transfer-matrix algebra.
  Boundary — infinite periodicity for bands; $N$ cells between uniform media for mirrors.
  Ensemble — deterministic. Ignored — absorption, dispersion of $n_{1,2}$ across the band, oblique
  incidence, higher dimensions. Valid when — layers thin against coherence length, indices real.
  Failure modes — reading evanescent $K$ as absorption (the mirror reflects; nothing is lost);
  normal-incidence gaps applied at angle; confusing gap width (contrast) with mirror quality
  (count).
- **Misconceptions:** none NEW — "the stack absorbs the forbidden light" is staged as a predict
  question and quiz distractor via energy conservation ($R + T = 1$, part-08's test), but it is a
  re-run of `interference-destroys-energy`, not a new wrong model; no entry forced.
- **Glossary terms:** `photonic-crystal` (גביש פוטוני), `band-gap` (פער רצועות — align with
  solid-state usage), `bragg-mirror` (מראת ברג), `bloch-wave` (גל בלוך).
- **Lab outline:** (1) band-structure lab, `coupled.chain_dispersion` overlay; (2) quarter-wave
  mirror: reflectance vs $N$, extract the decay constant, compare to the gap's $\kappa$;
  (3) defect cavity: resonance and linewidth vs spacer thickness against `interference.finesse`
  reasoning; (4) *measurement:* gap edges ± uncertainty from noisy reflectance spectra.
- **Media** (`render_photonic.py`): (a) folded chain dispersion morphing into the stack band
  diagram; (b) a defect mode's field trapped between two mirror stacks.
- **Quiz outline:** `Q-54-1` MC gap criterion from a $\operatorname{Tr}M$ plot (OBJ-54-1);
  `Q-54-2` MC chain↔stack correspondence (OBJ-54-2); `Q-54-3` numeric quarter-wave design
  (OBJ-54-3); `Q-54-4` MC defect-mode location + where forbidden light goes (OBJ-54-4, distractor
  re-running `interference-destroys-energy`).
- **Runtime note:** 2×2 products over ≤ 10³ frequencies × ≤ 10² layers — trivial in Pyodide.
- **Open questions:** does the chain overlay open the module (strong) or land in derive (safe);
  shared-axis units (normalized $\omega\Lambda/2\pi c$ recommended).

### 5.6 `55-ultrafast` — The shortest events ever made

- **Identity and scope:** mode-locking as N phase-locked cavity modes — module 00's
  N-coherent-arrows at its most literal (pulse train = phasor sum; random phases = cw noise);
  pulse duration ↔ bandwidth as module 04's theorem at femtoseconds; chirp and compression via
  `waves.propagate_dispersive`; the measurement problem — SHG autocorrelation (51's payoff) as a
  teaser. Deferred: locking mechanisms (saturable absorbers, Kerr-lens — named), carrier-envelope
  phase, attosecond generation.
- **Prerequisites:** §2 list — 00, 04, 12/13, 26, 44/45 (by id); soft edge to 51.
- **Learning objectives:**
  - `OBJ-55-1` — Show that N cavity modes at spacing Delta omega = 2 pi c / (2L), summed with
    equal phases, form a pulse train with period T_rep = 2L/c and duration ~ T_rep / N, while
    random phases give quasi-cw noise of the same average power.
  - `OBJ-55-2` — Apply Delta t times Delta omega >= 1/2 at femtosecond scale: the bandwidth a
    10 fs pulse requires, and how gain bandwidth caps the shortest pulse.
  - `OBJ-55-3` — Propagate a pulse through group-delay dispersion, quantify chirp and stretching,
    and demonstrate compression by applying opposite-sign dispersion.
  - `OBJ-55-4` — Explain why no detector measures a femtosecond pulse directly and how intensity
    autocorrelation with SHG gates the pulse with itself (teaser).
- **Section skeleton seeds:**
  - *puzzle:* same cavity, same mirrors, same average power — flip one condition and cw light becomes 10 fs flashes a million times brighter at their peaks; what changed? (only the *phases*.)
  - *predict:* 100 modes, random phases — pulses or noise?; double the locked count — duration halves?; does a fs pulse survive a centimeter of glass? (re-stages `packet-at-phase-velocity`); can a ~ps photodiode see the shape?
  - *explore:* mode-summing sandbox — $N$ slider, phase-lock toggle, scramble/re-lock button; live time trace + spectrum; dispersion stage — glass-length slider, chirp readout, compressor toggle.
  - *derive:* N-mode phasor sum → train and duration → bandwidth bound → GDD stretching and compression (below).
  - *verify:* `mode_locked_train` peak $\propto N^2$ locked vs $\propto N$ random (module 00's law refitted — `numerical-observation`); duration × bandwidth vs `fourier.rms_widths` bound across $N$; compression restores the transform limit to <1%.
  - *transfer:* frequency combs — the locked train's spectrum *is* a ruler; chirped-pulse amplification (stretch–amplify–compress); fiber links where 13's dispersion budget becomes engineering (§35.4); two-photon microscopy living off peak power.
  - *quiz:* $N$-scaling numeric; bandwidth numeric; chirp-sign MC; measurement MC.
  - *explain:* why phase alone, no new energy, makes the brightest events on Earth; the pulse train as module 00's arrows in your own words; why "measure it with itself" is the only option.
  - *advanced:* carrier-envelope phase and comb offset; Kerr-lens mode-locking closing the loop to 51's $n_2 I$ (safe to skip).
- **Core derivations:** (1) the locked sum:
  $E(t) = \sum_{n=0}^{N-1} E_0\,e^{-\ii(\omega_0 + n\Delta\omega)t}$ has envelope
  $|\sin(N\Delta\omega t/2)/\sin(\Delta\omega t/2)|$ — module 31's grating array factor with time
  standing in for angle: peaks every $T_{\text{rep}} = 2\pi/\Delta\omega = 2L/c$, width
  $T_{\text{rep}}/N$, peak intensity $N^2|E_0|^2$. (2) chirp: quadratic spectral phase
  $\tfrac12\phi''(\omega-\omega_0)^2$ (GDD) stretches a Gaussian pulse by
  $\sqrt{1 + (\phi''/\tau_0^2)^2}$ and chirps it linearly; applying $-\phi''$ undoes it exactly —
  run, not just stated, through `waves.propagate_dispersive` in its module-12 space↔time
  correspondence.
- **Model spec draft:** System — scalar cavity field as a finite comb of longitudinal modes;
  pulses as complex envelopes on a time grid. Dynamics — free superposition and linear dispersive
  propagation; no gain dynamics. Boundary — ideal cavity of length $L$; infinite transverse
  extent. Ensemble — deterministic; random-phase comparisons seeded. Ignored — the locking
  mechanism (phases are *given*), gain saturation, self-phase modulation, carrier-envelope offset.
  Valid when — bandwidth ≪ carrier (envelope description); GDD-only dispersion. Failure modes —
  average power treated as the story (peak power is); adding mode *intensities*; third-order
  dispersion read as numerical error.
- **Misconceptions:** none NEW — the predict candidates re-stage `packet-at-phase-velocity` (12)
  and module 00's coherent-vs-random summation; both get quiz distractors without new registry
  entries.
- **Glossary terms:** `mode-locking` (נעילת אופנים), `chirp` (צ'ירפ — translator to decide),
  `group-delay-dispersion` (נפיצת השהיית חבורה — translator to confirm), `autocorrelation`
  (אוטוקורלציה), `femtosecond` (פמטו-שנייה).
- **Lab outline:** (1) mode sandbox — peak scaling vs $N$ locked/random, log-log fits (module
  00's lab refit at optical scale); (2) duration–bandwidth product across $N$ vs the module-04
  bound; (3) stretch a 10 fs pulse in "glass", read the chirp, compress back; (4) *measurement:*
  pulse duration ± uncertainty from a simulated `autocorrelation_trace` (deconvolution factor
  stated honestly).
- **Media** (`render_ultrafast.py`): (a) N arrows locking — random spray → aligned burst, time
  trace forming underneath; (b) a pulse stretching through glass and recompressing, color-coded.
- **Quiz outline:** `Q-55-1` numeric peak-intensity scaling locked vs random (OBJ-55-1); `Q-55-2`
  numeric bandwidth for 10 fs (OBJ-55-2); `Q-55-3` MC chirp sign after glass + the compensator's
  sign (OBJ-55-3); `Q-55-4` MC why autocorrelation, not a photodiode (OBJ-55-4).
- **Runtime note:** ≤ 10³ modes on ≤ 2¹⁶-point grids; dispersion via two FFTs — ~1 s in Pyodide.
- **Open questions:** draw the array-factor identity with module 31 explicitly (recommended);
  how hard the autocorrelation teaser leans on 51 (recommendation: cite, don't require).

### 5.7 Stubs — remaining §20 topics (one paragraph each; no spec)

Stubs cover every §20 topic not absorbed above. No ids are reserved; a promoted stub takes the
next free id (56+) and gets a full condensed spec by amending this plan.

- **Electro-optics.** Pockels and Kerr cells: a DC field breaks the crystal's symmetry and the
  index becomes voltage-controlled — $\chi^{(2)}$ with one leg at zero frequency, so the natural
  home is a sequel to `51-nonlinear-optics`, reusing module 21's Jones machinery for the modulator
  (a voltage-controlled waveplate between polarizers). Payoff: the fastest light switches,
  Q-switching, and the modulator of capstone §35.4.
- **Acousto-optics.** A sound wave writes a travelling index grating; light Bragg-diffracts from
  it, Doppler-shifted by exactly the acoustic frequency — module 31's gratings plus module 08's
  travelling waves in one device. Would reuse module 31's grating machinery (by id) and
  `interference` phasor sums; natural demos: beam deflectors and heterodyne frequency shifters.
- **Spectroscopy.** The course builds three spectrometers (grating — 31 and capstone §35.3; FTIR —
  25; Fabry–Pérot — 26) but never the *science* of lines: this elective would connect Lorentzian
  linewidths (02, 16, 27) to lifetimes, Doppler and pressure broadening, and absorption
  fingerprinting, reusing `fourier` and `interference` machinery end-to-end. Lab candidate:
  identify a gas from a synthetic absorption spectrum.
- **Metamaterials.** Sub-wavelength structure gives effective $\epsilon(\omega)$, $\mu(\omega)$
  nature declines to provide — negative-index media where phase and group velocity oppose (13's
  plot run backward), perfect-lens claims dissected with 40's OTF honesty, cloaking as coordinate
  optics (33's Fermat payoff). Sits atop 16's Lorentz model with engineered resonators for atoms.
- **Integrated photonics.** Waveguides (46), resonators (44), and interference (23) shrunk onto a
  chip: directional couplers as module 06's two-mode beat, ring resonators as `26-fabry-perot` in
  a loop, Mach–Zehnder modulators as 25's geometry with 21's phase control. A design lab — build a
  wavelength filter from reused parts — and the on-ramp to the quantum-photonic circuits named in
  52's transfer.
- **Adaptive optics.** Folded into `53-computational-imaging` as its note and OBJ-53-4 (measure
  the wavefront in module 37's Zernike alphabet, correct *before* detection); a standalone
  elective would add wavefront sensing (Shack–Hartmann as an array of module-34 lenslets) and
  closed-loop correction against seeded turbulence. Until promoted, 53 carries the topic.

## 6. Part-level assessment and capstone hooks

Electives complete research narratives; they add no required assessment anywhere.

- `50-holography` completes §35.5 (the 4-f processor's filters become *recordable* objects) and
  extends §35.2 (a hologram as a bench element); closes 32's zone-plate thread.
- `51-nonlinear-optics` completes 01-sho's anharmonic thread (the re-pointed "module 20" promise)
  and 16's Lorentz story — the same oscillator, one term deeper.
- `52-quantum-optics` completes the §36 example chain verbatim (normal modes → cavities → laser
  modes → cavity QED → quantum information), 21's qubit box, 00's random-walk arc, and 27's
  statistics thread.
- `53-computational-imaging` completes §35.1 (the computational telescope finally *computes*:
  deconvolve the aberrated, noisy image the capstone produces) and 37's Zernike/AO research box.
- `54-photonic-crystals` completes 07's dispersion-and-gap promise at optical frequencies and
  24/26's multilayer trailer; enriches §35.4 (fiber Bragg components).
- `55-ultrafast` completes 00's N-arrows argument, 04's bandwidth theorem at its extreme, 12/13's
  chirp machinery, and the laser story of 44/45 (by id); enriches §35.4 (dispersion management is
  the fiber link's real budget).

## 7. Build order and validation gates

There is no fixed build order: electives are built **on demand**, each after its §2 prerequisites
exist, independently of one another. Ids are stable regardless of sequence (README: ids are
opaque; TOC order governs). If a default is wanted, build `50-holography` first — highest reuse,
fastest payoff, best proof that the elective tier costs little once the core exists. One soft
ordering: build 51 before 55 if the autocorrelation teaser should link somewhere real.

Per built elective: the standard four gates (README) with `--module <NN-slug>`; its flagged
elective-local functions get specced, placed (README ownership row added), and tested in the same
change; its §5 glossary terms and any NEW misconception entries
(`hologram-stores-image-pointwise`, `phase-matching-automatic`,
`photons-interfere-with-each-other`, `deconvolution-beats-diffraction`) are deposited with the
module that stages them, `addressed` on landing. Building 51 also executes the README conflict-log
edit in `content/en/oscillations/01-sho.md` ("module 20" → `51-nonlinear-optics`), making the
course's only core→elective reference a real link.

## 8. Deviations from the master plan

- **Id block:** electives occupy `50+` with `48–49` reserved as core insertion slack (README
  canonical map); stubs take `56+` only when promoted. Part number XIII and the 50+ ids
  deliberately do not coincide (README numbering rule).
- **Lighter plan by design:** §5 specs are condensed (~40–60 lines) rather than core-depth; full
  specs are written when an elective is scheduled. Rationale: elective content should not consume
  planning budget ahead of demand.
- **No new library files at planning stage:** each elective names its reused machinery and flags
  ≤ 3 elective-local functions as *specced when scheduled* (§4 table). File placement and README
  ownership rows are decided at build time — logged here as this part's standing infrastructure
  decision.
- **Topic grouping vs §20's flat list:** second-harmonic generation merges into 51; single-photon
  interference and squeezed light merge into 52; adaptive optics folds into 53 (note + OBJ-53-4)
  and keeps a stub for possible promotion. The remaining five topics (electro-optics,
  acousto-optics, spectroscopy, metamaterials, integrated photonics) are stubs only. All fifteen
  §20 topics are thereby covered — six electives, six stub paragraphs.
- **All-optional invariant made explicit:** the master plan calls these "possible advanced
  extensions"; this plan hardens that into a checkable rule — no core module, library file, test,
  or quiz may reference a 50+ module as a dependency. The single existing forward reference
  (01-sho's "module 20" → 51) is prose enrichment, not a dependency, resolved per the README
  conflict log.
- **Companion additions:** Boyd (51), Loudon / Gerry & Knight (52), and Joannopoulos (54, further
  reading) extend the template's standard companion hierarchy, which stops at Saleh & Teich /
  Siegman.
