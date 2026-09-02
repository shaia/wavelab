# Part 2 — Coupled Oscillators and Normal Modes — Implementation Plan

> **Master plan:** §9 (Part II). **Modules:** `06-coupled`, `07-normal-modes`. **Status:** complete — both built.
> Canonical numbering, invariants, and conflict log: [README.md](README.md).

## 1. Part overview and narrative arc

Part II is the hinge of the course: the last part about *things* that oscillate and the first
about *systems* that wave. Everything before it has one degree of freedom; everything after it
has infinitely many. The two modules cross that gap the only honest way — by walking it, mass by
mass: two coupled oscillators (06), then $N$, then the measured limit $N \to \infty$ (07).
Master-plan notebooks 2.2 and 2.3 merge into 07 because the escalation $2 \to 5 \to 20 \to 100$
is the *same eigenvalue problem run at increasing $N$*, and the continuum limit is that
problem's payoff, not a separate subject (§8).

The through-line is one idea stated twice. As physics: **a coupled system has special motions —
normal modes — that never exchange energy, and every motion is a sum of them.** As mathematics:
**the right basis makes coupled things simple** — diagonalization is a change of coordinates in
which $N$ coupled oscillators become $N$ independent module-01 oscillators. Module 06 discovers
the physical statement empirically: the student watches two pendulums trade their swing in
simulation and hunts for the two starting shapes that refuse to trade, *before* any matrix is
diagonalized. Module 07 earns the mathematical statement with the eigenvalue machinery, scales
it to $N$ masses, and *measures* the discrete chain converging to a continuous string. Two
earlier ideas get their payoff along the way: module 00's beats return as 06's central mechanism
— starting one pendulum excites both modes equally, and the exchange *is* the module-00 beat
between the two mode frequencies, now carrying energy between visible objects — and module 03's
orthogonal-basis expansion gets its finite-dimensional twin, since projecting a plucked shape
onto mode shapes is a Fourier series with $N$ terms (07 measures exactly that).

Three long-range seeds are planted. The $N$-mass chain yields the course's **first dispersion
relation**, $\omega(k) = 2\sqrt{k_s/m}\,|\sin(ka/2)|$ — plotted, named, and left standing as the
reference example for `13-dispersion` and, at its band edge, the first hint of
`54-photonic-crystals`. Master-plan 2.2's boxed motif — mechanical normal modes ↔ optical cavity
modes — is planted in 07's transfer toward `44-resonators` and `46-waveguides`, beside the
quantum echo trailed in `01-sho`'s advanced section ("diagonalising the Hamiltonian"). And
weak-vs-strong coupling — exchange time against mode splitting — is staged in 06's advanced
section as the classical face of Rabi physics (`52-quantum-optics`).

Beyond master-plan §9, the plan upgrades 2.3's continuum limit from a visual to a **measured
convergence experiment** (frequency error vs $N$ on log-log, order fitted — the
`tests/physics/test_convergence.py` culture applied to curriculum), registers two new
misconceptions with falsifying experiments, and builds an advanced tier — degeneracy, symmetry
breaking, avoided crossings, defect localization, Fermi–Pasta–Ulam–Tsingou — as a corridor to
modern physics.

## 2. Position in the course

- **Requires:**
  - `06-coupled`: `01-sho` ($\wnat = \sqrt{k/m}$, energy bookkeeping, amplitude/phase from
    initial conditions); `00-phasors` (the beat identity and its envelope).
  - `07-normal-modes`: `06-coupled` (matrix form, the hand-solved $2\times 2$, normal
    coordinates); `03-fourier-series` (expansion in an orthogonal basis);
    `04-fourier-transform` (`spectrum()` for reading mode frequencies out of motion).
- **Feeds:** `08-wave-equation` — the continuum limit, taken over at the exact point 07 stops;
  `11-standing-waves` — string modes are the $N \to \infty$ chain; `13-dispersion` — the
  lattice $\omega(k)$ is its opening example; `44-resonators` / `46-waveguides` — cavity and
  guided modes as "normal modes with light in them"; `52-quantum-optics` — exchange vs
  splitting is Rabi in classical costume; `54-photonic-crystals` — band edge, cutoff, defect
  localization return as photonic bands and defect cavities.
- **Explicitly not assumed:** linear algebra beyond a hand-solved $2\times 2$ (eigen-machinery
  is *taught* here, operationally); PDEs or continuum mechanics (tension and mass density wait
  for Part III); damping and driving (systems here are free and conservative — the driven pair
  appears only as a part-level synthesis problem); quantum mechanics (referenced, never used).

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|
| `06-coupled` | `content/en/normal-modes/06-coupled.md` | Coupled oscillators: the sympathy of pendulums | 2.1 | French, coupled oscillators; Georgi, coupled oscillations; MIT 8.03 coupled-oscillator lectures | **built** |
| `07-normal-modes` | `content/en/normal-modes/07-normal-modes.md` | Normal modes: the right basis, the N-mass chain, and the road to the continuum | 2.2 + 2.3 | Georgi, normal modes and the infinite chain; French, N coupled oscillators; MIT 8.03 | **built** |

## 4. Shared infrastructure for this part

**`src/wavelab` — existing used:** `oscillators.natural_frequency`, `oscillators.amplitude_phase`
(each modal coordinate *is* a module-01 oscillator); `oscillators.simulate` (single-oscillator
baseline); `phasors.beat_signal` (the 06 exchange overlaid on the module-00 beat form);
`fourier.spectrum` (mode frequencies read from trajectories — part-00 function, cited by name);
`measurement.add_noise`, `measurement.fit_cosine` (noisy measurements);
`validation.convergence_study`, `validation.seed_study`, `validation.scaling_exponent`.

**`src/wavelab` — new: `coupled.py`** (introduced and owned by this part; README ownership
table). Docstring model spec:

- **System:** $N$ point masses on a line joined by linear springs, described by mass and
  stiffness matrices $M$, $K$; observables are displacements, velocities, site/modal energies.
- **Dynamics:** $M\ddot{\mathbf{x}} + K\mathbf{x} = 0$ — solved exactly by modal decomposition,
  and independently by velocity-Verlet integration ("discover before diagonalizing").
- **Boundary:** fixed walls, free ends, or a periodic ring, chosen by the builders.
- **Ensemble:** deterministic; noise only via `wavelab.measurement`, randomness only seeded.
- **Ignored:** damping, driving, spring masses, nonlinearity, the transverse/longitudinal
  distinction (one polarization, one dimension).
- **Valid when:** $M$ symmetric positive definite, $K$ symmetric positive semi-definite (linear
  springs, small displacements); time steps well below the fastest mode period.
- **Failure modes:** non-symmetric input matrices; zero modes of free/periodic chains misread
  as errors; continuum formulas applied at $p \sim N$; nonlinear amplitudes (FPUT, 07 advanced).

Function-level sketch (signatures + contracts):

```python
two_mass_matrices(m, k, k_c, detune=0.0) -> (M, K)   # two oscillators + coupling spring; detune scales the second stiffness k*(1+detune)
chain_matrices(n, m, k_s, boundary="fixed") -> (M, K)# N-mass chain; boundary in {"fixed", "free", "periodic"}
simulate_coupled(M, K, x0, v0, dt, n_steps) -> CoupledTrajectory
                                                     # velocity Verlet, kick-drift-kick, a = -M^-1 K x; knows nothing about modes
normal_mode_solve(M, K) -> Modes                     # K a = omega^2 M a via Cholesky M = L L^T then eigh on L^-1 K L^-T; frequencies
                                                     # ascending (zero modes first), shapes M-orthonormal columns
mode_coordinates(modes, x0, v0) -> (q0, qdot0)       # M-inner-product projection of a state onto the mode shapes
evolve(modes, x0, v0, t) -> positions                # exact motion: sum_p a_p [q_p(0) cos(w_p t) + (qdot_p(0)/w_p) sin(w_p t)]
modal_energies(modes, x0, v0) -> E                   # energy per mode; constant in time — the conservation contract
site_energies(M, K, positions, velocities) -> E      # per-mass energy, each coupling spring's energy split half-half between its ends
exchange_time(omega_a, omega_b) -> float             # 2 pi / |omega_a - omega_b|: full there-and-back energy-exchange period
chain_mode_frequencies(n, m, k_s) -> omega           # closed form 2 sqrt(k_s/m) sin(p pi/(2(N+1))), fixed ends — the tested reference
chain_mode_shapes(n) -> shapes                       # columns sin(p pi j/(N+1)), fixed ends, M-orthonormalized
chain_dispersion(k_wave, a, m, k_s) -> omega         # omega(k) = 2 sqrt(k_s/m) |sin(k a / 2)|
chain_continuum_frequencies(n, m, k_s) -> omega      # the string values low modes converge to: p pi sqrt(k_s/m) / (N+1)
```

`Modes` is a frozen dataclass: `frequencies` (rad/s, ascending), `shapes` (columns,
$M$-orthonormal), and the `mass_matrix` retained for projections.

**`tests/physics/` additions:**

- *conservation:* each `modal_energies` entry constant along a `simulate_coupled` trajectory of
  the $N=20$ chain ($<10^{-6}$ relative over 100 slow-mode periods) while `site_energies`
  visibly vary; total energy bounded, not drifting (symplectic).
- *limits:* `normal_mode_solve(two_mass_matrices)` matches the analytic $N=2$ modes —
  $\sqrt{k/m}$, $\sqrt{(k+2k_c)/m}$, shapes $(1,\pm 1)/\sqrt2$ — to $10^{-12}$;
  `chain_matrices(1)` gives $\sqrt{2k_s/m}$; chain numerics match `chain_mode_frequencies` to
  $N=100$; free chain has one zero mode, uniform shape; started with one mass displaced, the
  equal pair's first site energy falls below 1% of the total within half an exchange period
  (the `energy-stays-in-excited-pendulum` falsifier, pinned).
- *convergence:* low chain modes → `chain_continuum_frequencies` with observed order $\approx 2$
  in $N$ via `validation.convergence_study`; error of mode $p$ grows as $p^2$.
- *scaling:* $(k_p, \omega_p)$ for $N \in \{5, 20, 100\}$ collapse onto `chain_dispersion`;
  small-$k$ slope equals $a\sqrt{k_s/m}$; `exchange_time` vs $k_c$ in weak coupling has
  `validation.scaling_exponent` $\approx -1$.
- *seeds:* random seeded $(x_0, v_0)$ decompose via `mode_coordinates` and reassemble through
  `evolve` at $t=0$ to $10^{-12}$, agreeing with `simulate_coupled` later within integrator
  tolerance; noisy mode-frequency extraction stable across seeds via `validation.seed_study`.
- *dimensions:* `chain_dispersion` in rad/s and `exchange_time` in seconds against the `units`
  registry; $K$ entries in N/m.

**Shared media:** one script `media/render/render_normal_modes.py` produces both modules' MP4s
(shot lists in §5). **Glossary themes:** coupling and modal vocabulary (06); eigen-language,
dispersion, and continuum vocabulary (07).

## 5. Module specifications

### 5.1 `06-coupled` — Coupled oscillators: the sympathy of pendulums (as built)

- **Identity and scope:** master-plan notebook 2.1. Two coupled oscillators only; the general
  eigenvalue treatment, $N > 2$, and the continuum are deferred to `07-normal-modes`.
- **Prerequisites:** `01-sho` ($\wnat$, energy bookkeeping, amplitude/phase); `00-phasors` (the
  beat identity and its envelope).
- **Learning objectives:**
  - `OBJ-06-1` — Write the equations of motion of two coupled oscillators in the matrix form
    M x'' + K x = 0 and assemble M and K for given masses and springs.
  - `OBJ-06-2` — Identify, from simulation, the initial conditions under which the pair
    oscillates at a single frequency with no energy exchange, and define these as the normal
    modes.
  - `OBJ-06-3` — Predict the energy-exchange period of two weakly coupled identical oscillators
    from the mode splitting, T_ex = 2 pi / (omega_a - omega_s), and connect the exchange to
    beats between the two mode frequencies.
  - `OBJ-06-4` — Decouple the pair with the normal coordinates q_pm = (x1 pm x2)/sqrt(2) and
    show each obeys an independent single-oscillator equation.
  - `OBJ-06-5` — Estimate the mode splitting in the weak-coupling limit,
    omega_a - omega_s approx omega0 k_c / k for k_c << k, and classify coupling as weak or
    strong by comparing the splitting to omega0.
- **Mathematical background:** has — $2\times 2$ matrices at the read-and-multiply level, the
  beat identity; introduced here — Newton's law in matrix form, the determinant condition.
- **Physical intuition goals:** (1) start one pendulum — the swing migrates *entirely* to the
  other and back, periodically; (2) the two no-exchange shapes (together / opposite) can be
  pointed at before computing; (3) stiffer coupling → faster exchange, *because* wider
  splitting; (4) the symmetric mode keeps the uncoupled frequency — its spring never stretches.
- **Section skeleton seeds:**
  - *puzzle:* start one of two identical pendulums on a common support; it gradually stops dead
    — then un-stops, stealing its swing back (Huygens' 1665 "odd kind of sympathy" as hook; an
    honesty footnote separates linear exchange from his escapement-driven locking). Boxed: how
    does the motion "know" how to come back — and can the pair start so nothing is exchanged?
  - *predict:* (1) start pendulum 1 alone — where is the energy after many swings? (targets
    `energy-stays-in-excited-pendulum`) (2) how many no-exchange starts exist? (3) stiffer
    coupling: exchange faster or slower? (4) does either special frequency equal $\wnat$?
  - *explore:* coupling slider $k_c/k \in [0.01, 2]$; initial-condition dial $(x_1, x_2)$; live
    site-energy bars; a "mode meter" showing $q_+, q_-$ amplitudes beside the physical view —
    the course's first site-picture/mode-picture side-by-side (master plan §22).
  - *derive:* Newton per mass → matrix form → trial $\mathbf{x} = \mathbf{a}\cos\omega t$ →
    determinant → the two modes → normal coordinates → start-one condition as equal mode mix →
    beat identity → exchange period → weak-coupling splitting.
  - *verify:* hand frequencies vs `normal_mode_solve` ($10^{-12}$); the simulated exchange on
    `phasors.beat_signal`; measured $T_{\text{ex}}$ vs $2\pi/\Delta\omega$; log-log
    $T_{\text{ex}}$ vs $k_c$ slope $\approx -1$ (the `numerical-observation` box).
  - *transfer:* `07-normal-modes` ($N$ of everything); coupled LC circuits (same matrices);
    CO$_2$'s symmetric vs antisymmetric stretch; `52-quantum-optics` — two-level systems trade
    excitation at a rate set by their splitting.
  - *quiz:* energy-exchange fate; exchange-time numeric; mode identification and count;
    assembling $M$ and $K$; weak-coupling splitting estimate.
  - *explain:* why the pendulum "stops itself" without friction; why the symmetric mode keeps
    $\wnat$; the exchange's relation to module 00's beats; weak vs strong coupling in one line.
  - *advanced:* weak vs strong coupling and the Rabi analogy — exchange slow and clean when
    $\Delta\omega \ll \wnat$; the detuned pair ($k \to k(1+\delta)$ on one mass): sweeping
    $\delta$ through zero the frequencies approach but never cross — the avoided crossing,
    minimum gap set by the coupling (trailer: coupled optical resonators, `44-resonators`);
    Huygens' locking as the linear model's honest edge.
- **Core derivations** (ordered):
  1. Two masses $m$, anchor springs $k$, coupling $k_c$: $m\ddot{x}_1 = -kx_1 - k_c(x_1 - x_2)$
     and $1 \leftrightarrow 2$; matrix form with $M = m\,\mathbb{1}$,
     $K = \begin{pmatrix} k+k_c & -k_c \\ -k_c & k+k_c \end{pmatrix}$.
  2. Trial $\mathbf{x} = \mathbf{a}\cos\omega t$ → $(K - \omega^2 M)\mathbf{a} = 0$ → $\det = 0$
     → $\omega_s = \sqrt{k/m}$, $\mathbf{a}_s \propto (1,1)$ and $\omega_a = \sqrt{(k+2k_c)/m}$,
     $\mathbf{a}_a \propto (1,-1)$: the symmetric mode never stretches the coupling spring.
  3. Normal coordinates $q_\pm = (x_1 \pm x_2)/\sqrt2$: $\ddot{q}_\pm + \omega_{s,a}^2 q_\pm = 0$
     — two independent module-01 oscillators; modal energies separately conserved.
  4. Start-one condition $(A, 0)$ at rest = equal mode mix:
     $x_1(t) = A\cos(\tfrac{\Delta\omega}{2}t)\cos(\bar\omega t)$,
     $x_2(t) = A\sin(\tfrac{\Delta\omega}{2}t)\sin(\bar\omega t)$, $\Delta\omega = \omega_a -
     \omega_s$, $\bar\omega = (\omega_s+\omega_a)/2$ — the module-00 beat identity verbatim.
     Site energies $\propto \cos^2, \sin^2(\Delta\omega t/2)$: full transfer at
     $\pi/\Delta\omega$, full return at $T_{\text{ex}} = 2\pi/\Delta\omega$.
  5. Weak coupling: $\omega_a \approx \wnat(1 + k_c/k)$, so $\Delta\omega \approx \wnat k_c/k$
     and $T_{\text{ex}} \propto 1/k_c$ — slow, clean exchange signals small splitting.
- **Model specification draft:** System — two identical point masses with anchor stiffness $k$
  joined by a coupling spring $k_c$ (equivalently two small-angle spring-coupled pendulums);
  observables: displacements, velocities, site and modal energies. Dynamics —
  $M\ddot{\mathbf{x}} + K\mathbf{x} = 0$, integrated by `simulate_coupled`, solved exactly by
  the $2\times 2$ modal decomposition. Boundary — anchored to rigid supports. Ensemble —
  deterministic; measurement cells add seeded Gaussian noise. Ignored — damping, driving,
  spring masses, pendulum nonlinearity, the escapement mechanics of real coupled clocks. Valid
  when — displacements linear (small angles), $\Delta t$ well below the fast-mode period.
  Failure modes — amplitudes where nonlinearity couples the modes; damping added naively (modes
  stay independent only for proportional damping); reading the site picture as fundamental.
- **Epistemic classification:** "the pair has exactly two single-frequency motions, and every
  motion is their sum" — `theorem` (boxed; linearity load-bearing); linear springs / small
  angles — `model-assumption`; exchange period $2\pi/\Delta\omega$ — `theorem`; measured
  $T_{\text{ex}} \propto k_c^{-1}$ — `numerical-observation` (boxed); Huygens' locking —
  honest note: outside the linear model.
- **Misconceptions:** NEW `energy-stays-in-excited-pendulum` — "If you start one pendulum of a
  coupled pair, the energy stays mostly in that pendulum." Falsifying experiment: simulate the
  start-one condition, plot `site_energies` — pendulum 1's energy falls below 1% of the total
  within half an exchange period, then fully returns; pinned by a limits test. Distractor:
  "most of the energy remains in pendulum 1, with small ripples leaking to 2".
- **Glossary terms:** `coupled-oscillators` (מתנדים מצומדים), `normal-mode` (אופן תנודה עצמי;
  `he_reject` candidate: מוד נורמלי — transliteration, translator to decide),
  `normal-coordinates` (קואורדינטות נורמליות), `coupling-strength` (חוזק צימוד),
  `mode-splitting` (פיצול אופנים — translator to confirm).
- **Interactive controls and simulations:** coupled-pair sandbox (coupling slider,
  initial-condition dial, site-energy bars, mode meter); exchange-time experiment (sweep $k_c$,
  timer readout); mode hunt (adjust $x_2/x_1$ until `fourier.spectrum` shows a single peak);
  advanced: detuning slider tracing the avoided crossing live.
- **Virtual lab outline** (`notebooks/en/labs/06-coupled.ipynb`): (1) build `two_mass_matrices`,
  integrate the start-one condition with `simulate_coupled`, plot site energies — the
  falsifying experiment, run first; (2) mode hunt via `fourier.spectrum` of $x_1(t)$: record
  both special ratios and frequencies; (3) overlay the exchange on `phasors.beat_signal` at
  $(\omega_s, \omega_a)$; (4) sweep $k_c$, measure $T_{\text{ex}}$, log-log fit slope
  $\approx -1$; (5) *measurement:* `measurement.add_noise`, extract $\omega_s, \omega_a$ from
  spectrum peaks across seeds, report $\Delta\omega \pm \sigma$, compare $2\pi/\Delta\omega$ to
  the directly timed exchange — value ± error, loop closed.
- **Real-experiment counterpart:** two nut-on-string pendulums hung from a slack horizontal
  string between two chairs (the string is the coupling). Phone video → frame-extracted bob
  displacements → arrays; measure the exchange period from a start-one release and the mode
  frequencies from together/opposite releases; compare $2\pi/T_{\text{ex}}$ to $\Delta\omega$.
- **Media assets** (`render_normal_modes.py`): (a) start-one exchange with site-energy bars
  pulsing in antiphase; (b) the two modes side by side, amplitudes steady; (c) split screen of
  one motion in site view (sloshing) and mode view (two constant bars). Language-neutral.
- **Quiz bank outline:** `Q-06-1` MC start-one energy fate (OBJ-06-2, distractor
  `energy-stays-in-excited-pendulum`); `Q-06-2` numeric exchange time from $\omega_s, \omega_a$
  (OBJ-06-3); `Q-06-3` MC how many no-exchange starts and their shapes (OBJ-06-2); `Q-06-4`
  free — assemble $M$, $K$ from a diagram (OBJ-06-1); `Q-06-5` numeric weak-coupling splitting
  from $k_c/k$ (OBJ-06-5); `Q-06-6` free — show $q_\pm$ decouple the equations (OBJ-06-4).
- **Problem set outline:** analytical — unequal masses ($2\times 2$, modes leave $(1,\pm 1)$);
  prove modal energies separately conserved; three coupled pendulums by symmetry.
  Computational — exchange-time scaling incl. the strong-coupling breakdown of
  $T_{\text{ex}} \propto 1/k_c$; transfer completeness vs detuning. Challenge — coupled LC
  circuits mapped and measured; Rayleigh damping ($b \propto M$ or $K$): modes still decouple —
  and why generic damping mixes them.
- **Runtime budget:** $2\times 2$ everything; `simulate_coupled` $\le 10^4$ steps; FFTs
  $\le 2^{12}$; animations $\le 200$ frames. Trivial in Pyodide.
- **Validation gates:** standard set (README) with `--module 06-coupled`; the
  conservation/limits/scaling test entries of §4 land with this module.
- **Open questions, as resolved when built.** Huygens opens the puzzle as a historical hook and
  the honest correction — that his clocks locked permanently, which no conservative linear
  system can do — closes *advanced*, so the anecdote earns its place twice without misleading
  in between. The mode meter is lab-only; the content page gets the site-versus-mode split
  screen as an animation instead, which says the same thing without an interactive budget. And
  the recommendation on imagery was taken: pendulums for the puzzle and the media, mass-and-
  spring for the derivation, with the equivalence stated once in the model specification.
- **As-built deviations from this section.** Six, each forced by the numbers or the repository
  rather than by taste, each pinned by a test.

  (1) **`normal_mode_solve` uses NumPy, not SciPy.** §4 specifies the Cholesky route without
  naming a library; `numpy.linalg.cholesky` and `numpy.linalg.eigh` match `scipy.linalg` to
  8.6e-14 at $N = 100$ and 8.9e-15 with unequal masses, with $M$-orthonormality to 1.6e-15.
  Choosing NumPy keeps the package docstring's "plain vectorized NumPy" promise and removes any
  question about `scipy.linalg` in the Pyodide kernel the laboratories run on. The reduced
  matrix is symmetrised explicitly before the eigensolve, so rounding cannot make it asymmetric.

  (2) **Mode-shape signs have to be fixed, and §4 does not say so.** `eigh` returns eigenvectors
  up to sign, and for the identical pair it hands back $(-1,-1)$ and $(-1,1)$. Without a
  convention the limits test comparing against $(1,\pm1)$ fails on sign alone, and the media
  would draw the symmetric mode upside down. Each column is now normalised so its
  largest-magnitude entry is positive, which reproduces exactly the shapes this section writes.

  (3) **A near-zero eigenvalue does not give a zero frequency.** Eigenvalues are clipped at zero
  before the square root — without the clip a free chain's translation mode, whose eigenvalue
  lands within rounding of zero on either side, produces a nan. With it the frequency comes back
  near $8\times10^{-8}$ rather than $0$, because a square root turns an eigenvalue's absolute
  error into a much larger relative one. §5.2's free-chain test must use a tolerance, never
  equality; the docstring says so.

  (4) **The conservation test is scoped to the pair, not the chain.** §7 assigns "the
  conservation/limits/scaling tests of §4" to this module, but §4 writes the conservation entry
  against the $N = 20$ chain, which needs `chain_matrices` — a 07 function. The pair version
  lands here and the chain version waits. That is fortunate as well as necessary: §4's
  `<1e-6` tolerance is reachable for the pair (9.6e-7 at $\Delta t = T_{\text{fast}}/3200$) and
  **not** for the chain, where the bounded symplectic error sits near 1.6e-3 at any step size a
  test suite can afford. 07 will need an honest tolerance and a bounded-not-secular check
  rather than a small number.

  (5) **The falsifier is a weak-coupling claim, and the 1% figure needs its condition.** §5.1
  says site 1's energy falls below 1% of the total. Measured: 0.06% at $k_c/k = 0.05$, 0.7% at
  $0.2$, and **7.4% at $k_c = k$**, where the transfer is genuinely incomplete. The page pins
  the weak case and states the strong one, and both are asserted in the tests — the second as a
  negative control, since a module claiming complete transfer at any coupling would be wrong.
  The same restriction applies to the $T_{\text{ex}} \propto 1/k_c$ law, whose fitted exponent
  is $-0.991$ over $k_c/k \in [0.005, 0.05]$ and $-0.830$ over $[0.2, 2]$.

  (6) **`site_energies` credits the undisplaced mass at $t = 0$.** Splitting each spring's
  energy half and half between its ends is the only convention under which the site energies sum
  to the true total, so it is a contract rather than a preference — but it has a visible
  consequence this section did not anticipate. Released with mass 1 displaced, mass 2 already
  holds 2.4% of the energy before anything has moved, because the coupling spring is stretched
  and belongs to both. The page and the laboratory both say so rather than rounding it away.

  One finding worth carrying into 07, from the laboratory's measurement step. **The two routes
  to the splitting are not equally good, and the reason is worth more than the number.** Reading
  two spectral peaks is good to 0.2% at 10% detector noise and barely degrades at 30%; timing
  the exchange minimum is 25% high with a 25% spread at 10% noise and collapses beyond it. The
  spectrum averages the whole record, while timing a minimum asks the data its weakest possible
  question — where is the signal smallest — and noise is proportionally largest exactly there.
  It is the same lesson as module 05's `q_from_bandwidth` trap in a new setting.

### 5.2 `07-normal-modes` — Normal modes: the right basis, the N-mass chain, and the road to the continuum

- **Identity and scope:** master-plan notebooks 2.2 + 2.3 (merged — §8). The general eigenvalue
  treatment, mode shapes and frequencies for $N$ masses ($2 \to 3 \to 5 \to 20 \to 100$), the
  chain dispersion relation, and the measured continuum limit. Deferred: the wave equation
  itself (`08-wave-equation`); general-media dispersion (`13-dispersion`); standing waves as
  boundary-value problem (`11-standing-waves`).
- **Prerequisites:** `06-coupled` (matrix form, hand-solved pair, normal coordinates);
  `03-fourier-series` (orthogonal-basis expansion); `04-fourier-transform` (`spectrum()`).
- **Learning objectives:**
  - `OBJ-07-1` — Formulate the normal-mode problem as the generalized eigenvalue problem
    K a = omega^2 M a, solve it numerically, and interpret eigenvalues as squared mode
    frequencies and eigenvectors as mode shapes.
  - `OBJ-07-2` — Decompose arbitrary initial conditions into modal coordinates using
    M-orthogonality, and predict the motion as a sum of independent oscillators.
  - `OBJ-07-3` — State and use the fixed-end chain results: shapes a_p(j) ~ sin(p pi j/(N+1))
    and frequencies omega_p = 2 sqrt(k_s/m) sin(p pi/(2(N+1))), with exactly N modes.
  - `OBJ-07-4` — Plot and interpret the chain dispersion relation
    omega(k) = 2 sqrt(k_s/m) |sin(k a/2)|: the linear small-k regime with slope
    c = a sqrt(k_s/m), and the cutoff at the band edge k = pi/a.
  - `OBJ-07-5` — Measure the continuum limit: show low chain modes converge to
    omega_p -> p pi c / L with relative error scaling as 1/N^2 on a log-log plot.
  - `OBJ-07-6` — Explain why modal energies are separately conserved while site energies are
    exchanged, and use the distinction to choose the right picture for a given question.
- **Mathematical background:** has — the $2\times 2$ by hand, orthogonal expansion from 03;
  introduced here — eigenvalues/eigenvectors operationally, the spectral theorem for the
  symmetric pencil (stated, verified numerically, proved for $2\times 2$), the $M$-inner
  product, and the wavenumber $k$ (notation handshake in open questions).
- **Physical intuition goals:** (1) given $N$ masses the student says "$N$ modes" before
  counting; (2) the first three mode shapes of a short chain can be sketched — more nodes,
  higher frequency; (3) the highest frequency saturates near $2\sqrt{k_s/m}$ — neighbors in
  antiphase is the fastest arrangement there is; (4) a plucked shape's motion is predictable
  *without integration*: project, evolve each mode, resum.
- **Section skeleton seeds:**
  - *puzzle:* a guitar string is $\sim 10^{23}$ coupled oscillators, yet plucked it plays one
    clean note plus overtones — not noise; a 100-mass simulated chain does the same. (Boxed:
    100 coupled equations — is there a point of view from which they are 100 *independent*
    module-01 problems? What are the 100 "notes"?)
  - *predict:* (1) how many distinct frequencies does a 5-mass chain have? (2) adding masses at
    fixed spacing — does the highest frequency grow without bound? (3) pluck a triangle shape:
    does the motion stay triangle-shaped? (4) do the *modes* of a plucked chain trade energy
    the way 06's pendulums did? (targets `modes-exchange-energy`)
  - *explore:* chain sandbox — $N$ slider $\{2, 3, 5, 10, 20, 50, 100\}$, mode picker with
    animated shape, boundary toggle, pluck tool; dispersion panel where each mode drops a dot
    at $(k_p, \omega_p)$ and the sine curve fills in as $N$ grows; the three synchronized views
    (chain / $x_j(t)$ traces / modal bars) per master plan §22.
  - *derive:* eigenproblem structure (why `eigh` after Cholesky, not `eig`) → modal expansion
    and evolution → the fixed chain by the $\sin$ ansatz → closed-form frequencies → shapes as
    sampled travelling waves → the dispersion relation, named → continuum limit → error rate.
  - *verify:* solver vs closed forms ($10^{-12}$); `evolve` vs `simulate_coupled` for seeded
    random starts; modal energy bars constant while site energies slosh; the convergence
    experiment — fitted order $\approx 2$ is the module's `numerical-observation` box.
  - *transfer:* the boxed motif — **mechanical normal modes ↔ optical cavity modes**
    (`44-resonators`; guided modes `46-waveguides`); `08-wave-equation` takes the limit this
    module stops before; `11-standing-waves` — the string's shapes at $N \to \infty$;
    `13-dispersion` — this $\omega(k)$ as the lattice example; phonons — this *is* the 1-D
    phonon band; quantum — diagonalising the Hamiltonian, per `01-sho`'s advanced trailer.
  - *quiz:* mode counting; closed-form numerics; dispersion-plot reading; modal-energy
    constancy; convergence scaling; eigenproblem formulation.
  - *explain:* why the guitar note is clean; site picture vs mode picture in your own words;
    why the top frequency saturates; what a linear small-$k$ dispersion means physically.
  - *advanced:* degeneracy and symmetry — the ring's modes come in equal-frequency pairs
    (counter-propagating shapes) because rotational symmetry demands it; perturbing one mass
    splits each pair — degeneracy lifting, tracing an avoided crossing (trailer:
    `44-resonators`); a light defect mass births a mode *above* the band, exponentially
    localized (trailer: `54-photonic-crystals` defect cavities); FPUT — with weak cubic
    nonlinearity modal energies drift yet refuse to thermalize: the near-recurrence that
    founded computational physics (`open-question` box).
- **Core derivations** (ordered):
  1. Structure: for $M$ SPD and $K$ symmetric PSD, $K\mathbf{a} = \omega^2 M\mathbf{a}$ has $N$
     real eigenvalues $\omega_p^2 \ge 0$ and $M$-orthogonal shapes. Route: Cholesky
     $M = LL^{\mathsf T}$ gives the symmetric standard problem
     $L^{-1}KL^{-\mathsf T}\mathbf{b} = \omega^2\mathbf{b}$ — why `numpy.linalg.eigh`, and why
     the theorem is 06's hand result grown up. Proof for $2\times 2$; verification beyond.
  2. Modal evolution: with $q_p(0), \dot{q}_p(0)$ from $M$-projection,
     $x_j(t) = \sum_p a_p(j)[\,q_p(0)\cos\omega_p t + (\dot{q}_p(0)/\omega_p)\sin\omega_p t\,]$
     — $N$ independent module-01 solutions, resummed (zero modes evolve linearly in $t$).
  3. Fixed chain: the ansatz $a_p(j) = \sin\!\big(\tfrac{p\pi j}{N+1}\big)$ satisfies the
     interior recursion and both ends, giving
     $\omega_p = 2\sqrt{k_s/m}\,\sin\!\big(\tfrac{p\pi}{2(N+1)}\big)$, $p = 1,\dots,N$.
  4. Dispersion: writing the shape as a sampled travelling wave
     $x_j \propto \Real\big[e^{\ii(kja - \omega t)}\big]$ with $k_p = p\pi/((N+1)a)$ turns the
     same recursion into the course's first dispersion relation,
     $$\boxed{\;\omega(k) = 2\sqrt{k_s/m}\;\big|\sin(ka/2)\big|\;}$$
     — linear at small $ka$ with slope $c = a\sqrt{k_s/m}$, saturating at the band edge
     $k = \pi/a$, where neighbors move in exact antiphase and $\omega_{\max} = 2\sqrt{k_s/m}$.
  5. Continuum limit: at fixed length $L = (N+1)a$ the low modes approach
     $\omega_p^\infty = p\pi c/L = p\pi\sqrt{k_s/m}/(N+1)$; since $\sin x/x \approx 1 - x^2/6$,
     the relative error of mode $p$ is $\approx (p\pi)^2/\big(24(N+1)^2\big)$ — order $N^{-2}$,
     growing as $p^2$: the continuum is reached from the bottom of the band up, and the band
     edge never converges. The second difference $k_s(x_{j+1} - 2x_j + x_{j-1})$ stands ready
     to become a second derivative — where the module stops; `08-wave-equation` takes the step.
- **Model specification draft:** System — $N$ equal masses joined by identical springs $k_s$,
  ends fixed (free/periodic variants via builders); the solver accepts any symmetric $(M, K)$
  pencil. Dynamics — $M\ddot{\mathbf{x}} + K\mathbf{x} = 0$; exact modal evolution from the
  eigensolution, velocity-Verlet as independent cross-check. Boundary — fixed walls by default;
  free and periodic carry zero modes (translation) that are physics, not bugs. Ensemble —
  deterministic; seeded noise in measurement cells, seeded random starts in tests. Ignored —
  damping, driving, nonlinearity, transverse/longitudinal distinction, wall compliance. Valid
  when — linear springs; $M$ SPD, $K$ symmetric PSD; continuum statements only for $p \ll N$.
  Failure modes — non-symmetric matrices; continuum formulas near the band edge; nonlinear
  amplitudes (FPUT: modal independence itself fails).
- **Epistemic classification:** spectral structure of the pencil — `theorem` (boxed; proof
  $2\times 2$, verification to $N = 100$); chain closed forms and dispersion sine law —
  `theorem` within the model; "$N$ discrete masses represent a continuous string" —
  `approximation` (boxed, validity edge $p \ll N$ explicit); measured convergence order
  $\approx 2$ — `numerical-observation` (boxed); FPUT non-thermalization — `open-question`.
- **Misconceptions:** NEW `modes-exchange-energy` — "Like the coupled pendulums, the normal
  modes of a system gradually trade energy back and forth over time." Falsifying experiment:
  pluck the $N=20$ chain, plot `modal_energies` — each bar constant to integrator precision
  over hundreds of periods while `site_energies` slosh continuously; 06's pendulums traded
  energy between *sites*, never between modes. Distractor: "the mode energies slowly equalize
  as the chain rings".
- **Glossary terms:** `eigenvalue` (ערך עצמי), `eigenvector` (וקטור עצמי), `mode-shape` (צורת
  אופן — translator to confirm), `dispersion-relation` (יחס נפיצה; `he_reject` candidate: יחס
  דיספרסיה), `continuum-limit` (גבול הרצף), `cutoff-frequency` (תדר קטעון; `he_reject`
  candidate: תדר חיתוך — translator to decide), `degeneracy` (ניוון).
- **Interactive controls and simulations:** chain sandbox ($N$, mode picker, boundary toggle,
  pluck tool, speed); dispersion accumulator; mode-vs-site energy view (both bar sets,
  evolving); continuum morph ($N$ ramp $2 \to 100$, lowest three shapes overlaid on smooth
  string shapes); advanced: defect-mass slider showing the localized mode split off the band.
- **Virtual lab outline** (`notebooks/en/labs/07-normal-modes.ipynb`): (1) `normal_mode_solve`
  on 06's pair — machine agreement with the hand result; (2) $N=5$ mode gallery: animate
  shapes, verify $M$-orthonormality; (3) pluck → `mode_coordinates` → `evolve` vs
  `simulate_coupled`; modal energy bars constant while site energies slosh — the falsifying
  experiment; (4) dispersion: $(k_p, \omega_p)$ for $N = 20$ then $100$ against
  `chain_dispersion`; extract the small-$k$ slope, compare to $a\sqrt{k_s/m}$; (5) *the
  convergence experiment:* $\omega_{1..3}$ vs $N \in \{2, 5, 10, 20, 50, 100\}$ against
  `chain_continuum_frequencies`, log-log error plot, order via `validation.convergence_study`,
  reported ± fit uncertainty; (6) *measurement:* a noisy record of one mass
  (`measurement.add_noise`), `fourier.spectrum` peak-picking to identify the excited modes,
  frequencies ± uncertainty across seeds vs the closed form.
- **Real-experiment counterpart:** a beaded chain — 3–5 heavy nuts threaded at equal spacing on
  elastic cord stretched between fixed points. Film transverse vibration after shaped releases;
  extract frequencies from frame timestamps; compare the *ratio* $\omega_2/\omega_1$ to
  `chain_mode_frequencies` (ratios cancel the unknown stiffness). Honest framing: damping and
  imperfect release limit this to ~10% — itself the measurement-culture lesson.
- **Media assets** (`render_normal_modes.py`, continued): (d) $N=5$ mode gallery,
  frequency-ordered; (e) continuum morph $N = 2 \to 5 \to 20 \to 100$ with the dispersion panel
  filling its sine curve dot by dot; (f) pluck decomposition — chain motion beside constant
  modal bars and sloshing site bars. Language-neutral.
- **Quiz bank outline:** `Q-07-1` MC mode count for $N$ masses (OBJ-07-3); `Q-07-2` numeric
  $\omega_p$ from the closed form (OBJ-07-3); `Q-07-3` MC dispersion-plot reading — slope,
  cutoff, band edge (OBJ-07-4, distractor "the top frequency grows without bound as masses are
  added"); `Q-07-4` MC modal energies of a plucked chain over time (OBJ-07-6, distractor
  `modes-exchange-energy`); `Q-07-5` numeric — error at $N = 100$ given the error at $N = 10$
  (OBJ-07-5); `Q-07-6` free — formulate the eigenproblem, state what the solver returns
  (OBJ-07-1); `Q-07-7` numeric — decompose a given $N = 2$ start into modes, give $x_1(t)$
  (OBJ-07-2).
- **Problem set outline:** analytical — verify the $\sin$ ansatz; the free–free chain's zero
  mode and momentum conservation; $N = 3$ by hand, shapes sketched first; modal Parseval.
  Computational — dispersion collapse across $N \in \{5, 20, 100\}$; triangular pluck: modal
  weights vs the triangle's Fourier coefficients from `03-fourier-series`; ring degeneracy
  verified, then split with one perturbed mass. Challenge — FPUT near-recurrence under a weak
  cubic force; defect localization: find the out-of-band mode, fit its exponential envelope.
- **Runtime budget:** `eigh` on $\le 200 \times 200$ — milliseconds; `simulate_coupled` for
  $N \le 100$, $\le 2\times 10^4$ steps, vectorized — about a second; FFTs $\le 2^{14}$;
  animations $\le 200$ frames per shape. Comfortably in-browser.
- **Validation gates:** standard set (README) with `--module 07-normal-modes`; the
  convergence/seeds/dimensions test entries of §4 land with this module.
- **Open questions for the author:** how much linear algebra to *teach* vs *use*
  (recommendation: state the spectral theorem, prove $2\times 2$, verify numerically); ring
  boundary in core or advanced (recommendation: advanced); show the second-difference →
  second-derivative step explicitly? (recommendation: show it and stop, letting
  `08-wave-equation` take the limit); notation handshake — stiffness is $k$ in 06 (matching
  `01-sho`) and renamed $k_s$ at the top of 07 when wavenumber $k$ enters, one explicit
  sentence marking the handover.
- **Open questions, as resolved when built.** All four recommendations were taken. The spectral
  theorem is stated in a `theorem` box and proved only for $2\times2$ — which is module 06's
  determinant, so the proof costs a sentence rather than a section — and verified against the
  chain's closed form to $3.5\times10^{-15}$ at $N = 100$. The ring lives in *advanced*, though
  `chain_matrices` carries its builder in the core library, because the laboratory's boundary
  toggle needs it and a student who reaches for `periodic` should find it working. The
  second-difference → second-derivative step is shown in full and the module stops on it. And
  the notation handshake is a single `note` admonition at the top of the page, before the
  puzzle, rather than a remark inside the derivation where it would be missed.
- **As-built deviations from this section.** Seven, each forced by the numbers or the repository
  rather than by taste, each pinned by a test.

  (1) **Mode shapes agree with the closed form only up to a sign, and §4 does not say so.**
  Module 06's deviation (2) fixed `normal_mode_solve` to make each column's largest-magnitude
  entry positive. `chain_mode_shapes` returns the sine's own sign, positive at $j = 1$. Those
  are different conventions and they genuinely disagree — modes 2 and 3 of a 3-chain, mode 3 of
  a 5-chain, modes 4 and 5 of a 6-chain — so every shape comparison in the tests and on the page
  is made up to sign. This is not a defect to fix: an eigenvector is defined up to sign, and a
  mode shape reversed is the same motion released half a period later. Worth recording that the
  solver's rule *ties* on chain shapes such as $(0.707, 0, -0.707)$, where its choice therefore
  rests on rounding; that was left alone rather than changed underneath a built module, and a
  sign-agnostic comparison is immune to it either way.

  (2) **`chain_mode_shapes(n)` cannot be $M$-orthonormal, because it is not given $M$.** §4
  writes the signature with `n` alone and simultaneously asks for $M$-orthonormal columns. With
  only `n` the best available is orthonormality in the ordinary dot product, which *is*
  $M$-orthonormality for unit masses; `normal_mode_solve` on a chain of mass $m$ returns these
  divided by $\sqrt{m}$, and the docstring says so. The normalisation is exact rather than
  computed: $\sum_j \sin^2(p\pi j/(N+1)) = (N+1)/2$ for every $p$, so the constant is
  $\sqrt{2/(N+1)}$.

  (3) **The conservation tolerance depends entirely on the excitation, and 06's forecast was
  pessimistic.** §5.1's deviation (4) predicted the chain's bounded symplectic error would sit
  near $1.6\times10^{-3}$ "at any step size a test suite can afford". Measured on the $N = 20$
  chain it is $3.4\times10^{-4}$ of the total at 100 steps per fast period, $8.5\times10^{-5}$
  at 200 and $2.1\times10^{-5}$ at 400, and identical at 2 and at 8 slow periods — bounded, as
  promised, and two orders of magnitude better than forecast. The real trap is the one 06 did
  not anticipate: **normalisation, not step size**. A symmetric pluck is orthogonal to every
  even mode, so twelve of the twenty hold exactly zero, and asking how far a mode holding
  $10^{-31}$ of the energy has drifted *relative to itself* returns $\approx 200$. The test
  therefore starts from a seeded random state, where every mode carries something and the
  per-mode claim of $2.5\times10^{-4}$ means what it says.

  (4) **The convergence refinement parameter is $N+1$, not $N$.** §5.2 asks for "observed order
  $\approx 2$ in $N$". Fitted against $N$ the answer is 1.95, which no honest window around a
  second-order law admits; against $N+1$ it is 2.000, 1.999 and 1.997 for the first three modes.
  The mesh has $N+1$ cells because $N+1$ springs span the length, so this is a mislabelled axis
  rather than a tolerance question. The measured errors match $(p\pi)^2/(24(N+1)^2)$ to better
  than 2%, which pins the coefficient and not merely the order. Problem 6(b) asks the student to
  make the same argument.

  (5) **The small-$k$ slope is not $a\sqrt{k_s/m}$, and the shortfall is worth asserting.** §4's
  scaling entry says the slope "equals" it. It falls short by exactly $(\pi/(N+1))^2/24$ — 1.1%
  at $N = 5$, $4\times10^{-5}$ at $N = 100$ — because the lowest mode already sits a little way
  up the sine. That is the same $\sin x / x$ expansion the continuum limit runs on, showing up
  in an unrelated measurement, so the test asserts the shortfall rather than tolerating it.

  (6) **The laboratory's measurement lesson is the opposite of module 06's, and both are kept.**
  §5.1 carried forward the finding that spectral peak-reading is robust where timing a minimum
  is not. Reading five mode frequencies out of one noisy record of a single mass is good to
  0.21% at 2% detector noise and to the *same* 0.21% at 30%: the error is set by the DFT's bin
  width, which is the record's length, and the noise never becomes the limiting term. The error
  bar shrinks with more seeds while the error itself does not move — a bias, not a variance, and
  the one situation where averaging harder is precisely the wrong response. The laboratory's
  closing question asks what the student would change about the apparatus rather than about the
  analysis.

  (7) **`mode_coordinates` and `modal_energies` grew trajectory support, which §4 did not ask
  for.** Both were specified on a single state, as `site_energies` was not. Three call sites —
  two in the laboratory, one in `render_normal_modes.py` — were about to stack a Python loop
  over states to put the two energy pictures side by side, which is the single thing this module
  exists to show. They now accept whole trajectories and carry the leading shape through,
  exactly as `site_energies` already did.

## 6. Part-level assessment and capstone hooks

- This part delivers the modal column of master plan §22's three synchronized representations
  (coupled oscillators: $\mathbf{x}(t)$ ↔ normal-mode amplitudes); the site/mode side-by-side
  built here is the UI motif reused for cavity modes (`44-resonators`) and guided modes
  (`46-waveguides`). §23's "Coupled pendulums — normal-mode frequencies" virtual lab is
  delivered by 06; the §36 research-connection chain (normal modes → optical cavities → laser
  modes → cavity QED) starts at 07's transfer and advanced sections.
- No §35 capstone consumes `coupled.py` directly; the part contributes conceptually —
  cavity-mode and band-structure literacy for the photonics electives, and the dispersion
  intuition `13-dispersion` carries into capstone §35.4's fiber link.
- Cross-module synthesis problem (once `02-damped-driven` exists): drive the coupled pair
  through a frequency sweep — the response is two module-02 Lorentzians centred on the mode
  frequencies, predicted per-mode via `oscillators.driven_amplitude`, verified by direct
  integration; one problem touching 00–07. Second synthesis: the triangular pluck as a Fourier
  exercise (modal weights vs `03-fourier-series` coefficients).
- Exam themes: sketch the modes of $N \le 3$ systems without computing; splitting ↔
  exchange-time estimates; dispersion-plot reading; "which picture — site or mode — answers
  this question fastest?"

## 7. Build order and validation gates

Build `06-coupled` first, then `07-normal-modes`: 07 generalizes the hand-solved pair 06
constructs, and 07's first lab cell re-runs 06's system through the general solver. Both follow
`05-impulse-response` in teaching order; nothing in Part III can be built before 07 lands, since
`08-wave-equation` opens at 07's stopping point.

`coupled.py` lands in two increments: with 06 — `two_mass_matrices`, `simulate_coupled`,
`normal_mode_solve` (used as a black-box check in 06, taught in 07), `mode_coordinates`,
`modal_energies`, `site_energies`, `exchange_time`, plus the conservation/limits/scaling tests
of §4; with 07 — `chain_matrices`, `evolve`, `chain_mode_frequencies`, `chain_mode_shapes`,
`chain_dispersion`, `chain_continuum_frequencies`, plus the convergence/seeds/dimensions tests.
Later parts may cite any of these names once merged.

With 06, deposit both NEW misconception entries into `assessment/misconceptions.yml`
(`energy-stays-in-excited-pendulum` assigned to `06-coupled`, `modes-exchange-energy` assigned
to `07-normal-modes`), status `pending` until each page addresses its own; and deposit the §5
glossary lists into `glossary/terms.yml` (suggested Hebrew is a proposal for the translator,
README invariant 4). Per module: the standard four gates (README bottom).

## 8. Deviations from the master plan

- **Merge (2.2 + 2.3 → `07-normal-modes`):** master plan §9 separates "Normal Modes and
  Eigenvectors" (2.2) from "From Discrete Oscillators to a Continuous Medium" (2.3). Merged
  because 2.3's escalation $2 \to 5 \to 20 \to 100$ is the same eigenproblem run at increasing
  $N$ — splitting would force re-teaching the machinery — and the continuum limit is the
  eigenvalue treatment's payoff, giving the merged module its lab (the convergence experiment).
  Precedent: `02-damped-driven` ← 1.2 + 1.3.
- **Scope boundary at the wave equation:** master plan 2.3 says the limit "creates a natural
  path to the wave equation"; this plan stops 07 at the second difference ready to become a
  second derivative and defers the PDE to `08-wave-equation` (part-03 ownership).
- **Dispersion named early:** the master plan first names dispersion at notebook 4.4; this plan
  plots and names $\omega(k)$ for the chain in 07, giving `13-dispersion` a concrete lattice
  example to generalize rather than introduce.
- **Continuum limit upgraded to a measurement:** master plan 2.3 asks to "show visually"; this
  plan additionally requires the error-vs-$N$ log-log convergence experiment with a fitted
  order, aligning curriculum with the `tests/physics/test_convergence.py` culture.
- **Additions beyond the master plan:** discovery-first staging of 2.1 made explicit (modes
  found in simulation before any diagonalization); two new registry misconceptions with
  falsifying experiments; weak/strong coupling and the Rabi foreshadowing (06 advanced);
  degeneracy, symmetry breaking, avoided crossings, defect localization, and FPUT (advanced
  tiers); the beaded-chain real experiment.
