# Part III — Continuous Systems and the Wave Equation — Implementation Plan

> **Master plan:** §10 (Part III). **Modules:** `08-wave-equation`, `09-wave-energy`, `10-impedance`. **Status:** in progress — `08-wave-equation` and `09-wave-energy` built.
> Canonical numbering, invariants, and conflict log: [README.md](README.md).

## 1. Part overview and narrative arc

Space enters the course here. Through Part II the dynamical variables were finitely many numbers
$x_1(t), \dots, x_N(t)$; from this part on the variable is a *field* $y(x,t)$, and the oscillator
equation becomes the course's first partial differential equation,
$\partial^2 y/\partial t^2 = v^2\,\partial^2 y/\partial x^2$. That is a conceptual event, and the
plan marks it as one: a local law (each string element obeys Newton) produces a global consequence
(shapes that travel rigidly at a speed the *medium* chooses). From here on $\omega$ and $k$ are
partners, and everything in Parts IV+ — packets, dispersion, EM waves, interference, diffraction —
lives on this foundation.

The chief enhancement over the master plan is a **double derivation** of the wave equation,
presented as mutually reinforcing rather than redundant. Route (a) is inherited: take
`07-normal-modes`' $N$-mass chain to the continuum limit — the small-$ka$ limit of the chain
dispersion $\omega(k) = 2\sqrt{k_s/m}\,|\sin(ka/2)|$ already predicts $v = a\sqrt{k_s/m}$, and the
dictionary $\mu = m/a$, $T = k_s a$ turns that into $v = \sqrt{T/\mu}$. Route (b) is fresh: Newton
for a string element under tension, with the small-slope approximation
$|\partial y/\partial x| \ll 1$ stated honestly as the model assumption it is. Two routes meeting
at one equation is the lesson: the wave equation is not about strings; it is about any medium whose
parts pull their neighbours back toward the line. A closing loop gives the numerics unusual weight:
the leapfrog/FDTD stencil *is* the mass-chain equation with $m = \mu\Delta x$, $k_s = T/\Delta x$ —
the computer solves the continuum equation by quietly rebuilding Part II's chain. The CFL stability
condition is staged as a designed laboratory experiment (watch it blow up), not an incantation.

Module 09 answers what 08 deliberately leaves dangling: if no material travels with the pulse, what
*does*? Three velocities are separated — transverse medium velocity, pattern velocity, energy
transport velocity — and the bookkeeping yields the part's quiet surprise: in a travelling wave the
kinetic and potential energy densities are equal at *every point and instant*, and the energy rides
at exactly $v$. Module 10 asks what happens when the medium changes underfoot; the answer —
impedance, $r = (Z_1{-}Z_2)/(Z_1{+}Z_2)$ — is algebra the course reuses, essentially unchanged, as
the Fresnel equations (`18-fresnel`) and anti-reflection coatings (`24-thin-films`), a unification
announced here in a box, on purpose. The registry misconception `wave-carries-medium` is confronted
in 08 (re-pointed here per the README conflict log) with the cleanest falsifier the course owns: a
marked "dust speck" on the simulated string moves transversely and returns home while the pulse
passes through it.

## 2. Position in the course

- **Requires:** `00-phasors` — the complex form $\Real[A\,e^{\ii(kx-\omega t)}]$, the phasor's
  first spatial use; `01-sho` — kinetic/potential energy of one element (09's densities are these
  per unit length); `06-coupled` / `07-normal-modes` — the chain equation
  $m\ddot{y}_n = k_s(y_{n+1} - 2y_n + y_{n-1})$ and its dispersion
  $\omega(k) = 2\sqrt{k_s/m}\,|\sin(ka/2)|$, whose small-$ka$ limit seeds derivation (a).
- **Feeds:** `11-standing-waves` (d'Alembert + 10's end reflections $r = \mp 1$ build standing
  waves; 09's zero-average-flux seed cashed there); `12-wave-packets` / `13-dispersion` (consume
  `waves.py`'s solver and the $\omega = vk$ baseline that dispersion breaks; packet and
  group-velocity functions are *theirs*, §4); `14-em-waves` (Maxwell yields this same PDE with
  $v = c$); `16-light-in-matter` (10's "same $\omega$, different $k$" is frequency continuity on a
  string); `18-fresnel`, `24-thin-films`, `26-fabry-perot` (the junction algebra, quarter-wave
  matching, and two-junction multiple reflections, respectively).
- **Explicitly not assumed:** group velocity or any packet concept (12/13); Fourier decomposition
  of string initial conditions (11); EM content; dispersion — the ideal string is non-dispersive
  *by construction* and the prose must not pretend otherwise; momentum-flux subtleties beyond 09's
  flagged advanced note.

## 3. Canonical module table

| Module id | Content path | Title | Master-plan notebooks | Textbook companion | Status |
|---|---|---|---|---|---|
| `08-wave-equation` | `content/en/waves/08-wave-equation.md` | The wave equation: oscillations acquire space | 3.1 + 3.2 | Georgi, continuum limit & travelling waves; French, progressive waves | **built** |
| `09-wave-energy` | `content/en/waves/09-wave-energy.md` | Wave energy: what actually travels | 3.3 | French, energy in progressive waves; MIT 8.03 energy-transport lectures | **built** |
| `10-impedance` | `content/en/waves/10-impedance.md` | Impedance: reflection and transmission at boundaries | 3.4 | Georgi, impedance & reflections; French, boundary effects | planned |

## 4. Shared infrastructure for this part

**`src/wavelab` — existing used:** `phasors.real_signal`; the part-02 chain integrator from
`coupled.py` for 08's continuum-limit opening (exact name per part-02's plan as built);
`measurement.add_noise` / `measurement.fit_cosine`; `validation.scaling_exponent`,
`validation.convergence_study`, `validation.seed_study`.

**`src/wavelab` — new: `waves.py`** (introduced by this part; extended by part-04 per the README
ownership table). **Ownership split, stated explicitly:** this plan defines ONLY the
string-dynamics core — FDTD/leapfrog solver with CFL guard, d'Alembert evaluator, energy densities
and flux, impedance/junction coefficients, boundary handling (fixed / free / junction to a second
medium). Packet construction, group velocity, and dispersion-relation functions live in the *same
file* but are specified by part-04's plan, written in parallel; this plan must not define, rename,
or constrain them beyond the docstring's general scope. The file-level 7-bullet model spec below is
owned here and covers the whole file's eventual scope in general terms:

- **System:** the transverse displacement field $y(x,t)$ of a one-dimensional medium on a finite
  grid — a uniform or piecewise-uniform string here; dispersive media in part-04's extensions.
- **Dynamics:** the linear wave equation $\mu\,y_{tt} = T\,y_{xx}$, integrated by leapfrog FDTD or
  evaluated from exact solutions; part-04 adds dispersive generalisations.
- **Boundary:** fixed or free ends, or an impedance junction between two media; part-04 may add
  wide "open" windows for packet studies.
- **Ensemble:** deterministic; callers add noise via `wavelab.measurement`.
- **Ignored:** stiffness, damping, gravity sag, longitudinal motion, nonlinearity.
- **Valid when:** $|\partial y/\partial x| \ll 1$, and numerically when the Courant number
  $S = v\,\Delta t/\Delta x \le 1$ with pulses resolved by many grid points.
- **Failure modes:** CFL violation (exponential grid-scale blow-up); order-one slopes (the model,
  not the code, breaks); grid dispersion on under-resolved features read as physics.

Function-level sketch (signatures + contracts; the definitive list this plan owns):

```python
wave_speed(tension, mu) -> v                     # sqrt(T/mu); scalar or per-point array
impedance(tension, mu) -> Z                      # sqrt(T*mu) = mu*v; scalar or array
cfl_max_dt(dx, v_max) -> dt                      # the stability bound dx/v_max
simulate_string(y0, v0, dx, dt, tension, mu, n_steps,
                boundary=("fixed", "fixed"), allow_unstable=False) -> StringEvolution
                                                 # leapfrog; mu may be an array (piecewise = junction);
                                                 # raises on S > 1 unless allow_unstable (the blow-up lab)
dalembert_solution(y0_func, v0_func, v, x, t) -> y
                                                 # exact f(x-vt)+g(x+vt) from initial shape and velocity
kinetic_density(dydt, mu) -> u_K                 # (1/2) mu (dy/dt)^2 per point
potential_density(dydx, tension) -> u_P          # (1/2) T (dy/dx)^2 per point
energy_flux(dydx, dydt, tension) -> P            # -T (dy/dx)(dy/dt); signed
total_energy(y, dydt, dx, tension, mu) -> float  # trapezoid of u_K + u_P over the string
junction_coefficients(Z1, Z2) -> (r, t)          # displacement amplitudes: (Z1-Z2)/(Z1+Z2), 2*Z1/(Z1+Z2)
power_coefficients(Z1, Z2) -> (R, T)             # r**2 and (Z2/Z1)*t**2; sums to 1
```

`StringEvolution` is a small dataclass (times, per-step $y$ and $\partial y/\partial t$) so energy
diagnostics need no re-differencing by callers.

As built, this part's share of `waves.py` gained a fifth energy function beyond the sketch:
`sinusoidal_mean_power(amplitude, omega, tension, mu)`, the closed form
$	frac12\mu v\omega^2 A^2$, because invariant 3 forbids the page and the laboratory from
writing it out themselves (§5.2, deviation 1).

**`tests/physics/` additions:**

- *conservation:* fixed-end solver total energy constant over many transits (drift second order in
  $\Delta t$); junction run — incident pulse energy = reflected + transmitted.
- *convergence:* FDTD vs `dalembert_solution` $L^2$ error second order in $\Delta x$ at fixed
  $S < 1$; at $S = 1$ exactly, machine precision (the "magic time step").
- *limits:* `junction_coefficients(Z, Z) == (0, 1)`; $Z_2 \to \infty$: $r \to -1, t \to 0$;
  $Z_2 \to 0$: $r \to +1, t \to 2$; `power_coefficients` sums to 1 across a log-spaced sweep.
- *scaling:* measured pulse speed vs tension fits exponent $0.50$ via `scaling_exponent`;
  likewise $-0.50$ vs $\mu$.
- *dimensions:* `wave_speed` in m/s, `impedance` in kg/s, `energy_flux` in W, against `units`.
- *seeds:* noisy two-photogate speed measurement reproducible via `seed_study`.

Part-04 files its own tests for its own functions; the above land with this part's modules.
**Shared media:** one script `media/render/render_waves.py` produces all Part III MP4s (shot lists
in §5). **Glossary themes:** wave kinematics, energy transport, impedance — the course's first
deposits of wave (as opposed to oscillation) terminology.

## 5. Module specifications

### 5.1 `08-wave-equation` — The wave equation: oscillations acquire space (as built)

- **Identity and scope:** master-plan notebooks 3.1 + 3.2, merged (§8): derivation, travelling
  solutions, initial-value problem, numerical solver. Deferred: standing waves
  (`11-standing-waves`); energy (`09-wave-energy`); boundaries (`10-impedance`); dispersion
  (`13-dispersion`).
- **Prerequisites:** `07-normal-modes` (chain EOM, dispersion, small-$ka$ limit); `00-phasors`
  (complex travelling-wave form); `01-sho` (what one element's $\omega_0$ means).
- **Learning objectives:**
  - `OBJ-08-1` — Derive d^2y/dt^2 = v^2 d^2y/dx^2 two ways — continuum limit of the coupled-mass
    chain, and Newton for a string element under tension — stating the small-slope assumption
    |dy/dx| << 1 both routes require.
  - `OBJ-08-2` — Verify that y = f(x - v t) + g(x + v t) solves the wave equation for any
    twice-differentiable f, g, and identify v = sqrt(T/mu) as fixed by the medium.
  - `OBJ-08-3` — Solve the initial-value problem by d'Alembert: split a pluck (shape, no velocity)
    into half-amplitude counter-propagating copies; integrate a strike (velocity, no shape).
  - `OBJ-08-4` — Predict how pulse speed responds to tension, density, amplitude, and shape (only
    T and mu matter), and check omega = v k for sinusoidal waves.
  - `OBJ-08-5` — Integrate the wave equation with a leapfrog scheme, state the CFL condition
    v dt/dx <= 1, and recognise its violation in a solution.
  - `OBJ-08-6` — Explain what travels and what does not: the disturbance moves at v while each
    medium element moves transversely about its rest position.
- **Mathematical background:** has — Taylor expansion, chain rule, the chain dispersion; new —
  partial derivatives in earnest, change of variables in a PDE, the idea of a field equation
  (flagged as the course's first PDE).
- **Physical intuition goals:** (1) the medium chooses the speed — the hand chooses only the
  shape; (2) a pluck released from rest *must* split in two; (3) two pulses pass through each
  other unchanged; (4) the speck goes up, down, and home — nothing material travels.
- **Section skeleton seeds:**
  - *puzzle:* the stadium wave circles the stadium while every fan stays seated; flick a 20 m rope
    and something crosses it and slaps the wall, yet no piece of rope makes the trip. Boxed: what
    is the thing that moves, and what sets its speed?
  - *predict:* (1) two pulses, one twice the amplitude — which arrives first? (targets NEW
    `speed-set-by-source`); (2) a dust speck mid-string as a pulse passes — where does it end up?
    (targets `wave-carries-medium`); (3) doubling tension changes crossing time how? (4) a plucked
    triangle released from rest — one pulse or two?
  - *explore:* pulse launcher (shape / width / amplitude), $T$ and $\mu$ sliders, two "photogate"
    cursors with live speed readout, dust-speck toggle, counter-propagating pulses superposing.
  - *derive:* double derivation → d'Alembert → IVP → $\omega = vk$ → leapfrog stencil = mass chain.
  - *verify:* FDTD vs `dalembert_solution` overlay; measured $v$ vs $\sqrt{T/\mu}$; CFL blow-up
    and $S = 1$ exactness (both `numerical-observation`).
  - *transfer:* `11-standing-waves` (add walls); `13-dispersion` (what if $\omega/k$ varies);
    `14-em-waves` (Maxwell will produce this equation); `07-normal-modes` backward; sound and
    seismic waves as the same PDE.
  - *quiz:* what sets $v$; the dust speck; d'Alembert splitting; direction of $g(x+vt)$; CFL.
  - *explain:* what moves in a stadium wave; why "how hard you flick" cannot appear in $v$; why
    the solver blowing up is a numerics statement, not physics.
  - *advanced:* von Neumann sketch of $S \le 1$; the magic step $S = 1$ as exact transport;
    half-line d'Alembert by images (trailer for 10/11); what "first PDE" means.
- **Core derivations:** (1) *chain route:* in $m\ddot{y}_n = k_s(y_{n+1} - 2y_n + y_{n-1})$ set
  $y_n(t) = y(na, t)$, Taylor-expand $y_{n\pm1} = y \pm a\,y_x + \tfrac{a^2}{2}y_{xx} + O(a^3)$:
  $y_{tt} = (k_s a^2/m)\,y_{xx}$; the dictionary $\mu = m/a$, $T = k_s a$ gives $v^2 = T/\mu$;
  cross-check — the small-$ka$ limit of $\omega(k) = 2\sqrt{k_s/m}\,|\sin(ka/2)|$ is
  $\omega \approx a\sqrt{k_s/m}\,k$, the same $v$. (2) *string route:* transverse Newton on
  $[x, x+dx]$ with $\sin\theta \approx \tan\theta = y_x$ (the `model-assumption`):
  $\mu\,y_{tt} = T\,y_{xx}$. (3) *d'Alembert:* $u = x - vt$, $w = x + vt$ turns the PDE into
  $\partial^2 y/\partial u\,\partial w = 0$, hence $y = f(u) + g(w)$ (`theorem`). (4) *IVP:*
  $y(x,t) = \tfrac12[y_0(x-vt) + y_0(x+vt)] + \tfrac{1}{2v}\int_{x-vt}^{x+vt} w_0(s)\,ds$ —
  pluck = two half-copies; strike = a spreading plateau. (5) *sinusoidal:*
  $y = \Real[A\,e^{\ii(kx-\omega t)}]$ solves iff $\omega = vk$. (6) *numerics:*
  $y_i^{n+1} = 2y_i^n - y_i^{n-1} + S^2(y_{i+1}^n - 2y_i^n + y_{i-1}^n)$, $S = v\Delta t/\Delta x$;
  the stencil is Newton for a chain with $m = \mu\Delta x$, $k_s = T/\Delta x$ — discretisation
  reruns the continuum limit backwards.
- **Model specification draft:** System — transverse displacement field $y(x,t)$ of a uniform
  string ($T$, $\mu$, length $L$). Dynamics — $\mu y_{tt} = T y_{xx}$; numerically, leapfrog.
  Boundary — fixed ends kept out of reach (boundaries become physics in 10). Ensemble —
  deterministic; seeded noise only in measurement cells. Ignored — stiffness, damping, gravity
  sag, longitudinal motion, nonlinearity. Valid when — $|y_x| \ll 1$; numerically $S \le 1$ with
  well-resolved pulses. Failure modes — order-one slopes; CFL violation; grid dispersion.
- **Epistemic classification:** small-slope assumption — `model-assumption` (boxed; the honesty
  moment); d'Alembert general solution — `theorem` (boxed); CFL blow-up and $S = 1$ exactness —
  two `numerical-observation` boxes; "the first PDE" — an `important` narrative call-out.
- **Misconceptions:** registry `wave-carries-medium`, re-pointed here per the README conflict log
  (the `assigned_module` edit lands with this module). Falsifier: mark a dust speck on the
  simulated string, pass a pulse through it, plot its trajectory — purely transverse, returns to
  rest; nothing material travels with the pulse. Distractor: "the speck is carried a little way in
  the direction of travel." NEW `speed-set-by-source` — "Shaking harder or faster makes the wave
  travel faster." Falsifier: race pulses of different amplitude/width on one cord — identical
  transit times; only $T$ or $\mu$ moves the reading. Distractor: "the taller pulse arrives first."
- **Glossary terms:** `wave-equation` (משוואת הגלים), `travelling-wave` (גל רץ; `he_reject`: גל
  נודד), `pulse` (פולס; `he_reject`: דופק), `wave-speed` (מהירות הגל), `linear-mass-density`
  (צפיפות מסה אורכית), `dalembert-solution` (פתרון ד'אלמבר), `cfl-condition` (תנאי CFL —
  translator to decide), `field` (שדה).
- **Interactive controls and simulations:** beyond the explore bullets — the CFL panel ($S$ slider
  crossing 1, lab only); a snapshot-pair tool freezing $y(x)$ at two times for reading off $v$.
- **Virtual lab outline** (`notebooks/en/labs/08-wave-equation.ipynb`): (1) continuum warm-up —
  part-02 chain at $N = 5, 20, 100$ beside `simulate_string`; (2) photogate speed vs tension over
  a decade, log-log fit via `scaling_exponent`; (3) pluck vs strike against `dalembert_solution`;
  (4) dust-speck trace (the falsifier); (5) CFL experiment — $S = 0.9, 1.0, 1.01$, the third
  explodes; (6) *measurement:* noisy photogate speed via `add_noise`, $v \pm \sigma_v$ across
  seeds vs $\sqrt{T/\mu}$.
- **Real-experiment counterpart:** pulse on a long spring/slinky filmed with a phone at known fps;
  hang weights for tension steps; measure $v$ vs $T$ from frame timestamps. Import: frame/position
  CSV from stepping through the video → NumPy cell; fps converts frames to seconds.
- **Media assets** (`render_waves.py`): (a) pulse crossing while a marked element traces its
  transverse loop; (b) plucked triangle splitting into two half-copies; (c) CFL blow-up at
  $S = 0.99$ vs $1.01$. Language-neutral, no burned-in text.
- **Quiz bank outline:** `Q-08-1` MC what sets $v$ (OBJ-08-4, distractor `speed-set-by-source`);
  `Q-08-2` MC dust speck (OBJ-08-6, distractor `wave-carries-medium`); `Q-08-3` MC pluck splitting
  (OBJ-08-3); `Q-08-4` numeric $v$ from $T, \mu$ and a crossing time (OBJ-08-2); `Q-08-5` numeric
  largest stable $\Delta t$ (OBJ-08-5); `Q-08-6` MC direction/speed of $g(x+vt)$ from snapshots
  (OBJ-08-2); `Q-08-7` free — the two derivations in words (OBJ-08-1).
- **Problem set outline:** analytical — chain-rule check of $f(x - vt)$; d'Alembert for a
  rectangular strike; dimensional analysis. Computational — grid-dispersion study; $S = 1$ magic
  step verified. Challenge — half-line pluck with a fixed end by images (foreshadows 10).
- **Runtime budget:** grids $\le 2000$ points, $\le 4000$ steps — under a second in Pyodide;
  animations $\le 120$ frames; chain warm-up at $N \le 100$.
- **Validation gates:** standard set (README) with `--module 08-wave-equation`; §4 conservation
  and convergence tests land with this module.
- **Open questions for the author:** which derivation leads (recommendation: chain first — Part
  II's payoff — string second); CFL experiment in `verify` or lab only (recommendation: still
  frame in `verify`, live in the lab).
- **Open questions, as resolved when built.** Both recommendations were taken, one of them with
  a twist. The chain leads, read as beads on a taut thread rather than as module 07's masses
  sliding lengthways. That reading gives the dictionary a reason: the thread's transverse pull on
  a bead is a spring of stiffness $T/a$, so $T = k_s a$ is derived rather than asserted, and the
  small-slope assumption appears in both routes instead of only the second. The lengthways
  reading survives as a transfer bullet, where it is exact without that assumption. The CFL
  experiment is live in the laboratory. On the page it is not a still frame but a pair of
  `numerical-observation` boxes in `verify`, with the animation in `explore` — the growth rate
  against von Neumann's $|g|$ is a number worth quoting, and a frame cannot quote it.
- **As-built deviations from this section.** Nine, each forced by the numbers or the repository
  rather than by taste; the numerical ones are pinned by tests.

  (1) **`dalembert_solution` takes the velocity's antiderivative, not the velocity.** §4 writes
  `dalembert_solution(y0_func, v0_func, v, x, t)`. Integrating an arbitrary callable over
  $[x - vt, x + vt]$ for every point and time would need a quadrature. That quadrature would be
  inexact for the rectangular strike the problem set poses, where the velocity jumps, and the
  function is named as the *exact* solution. As built: `dalembert_solution(y0_func, v, x, t,
  v0_integral=None)`, with `v0_integral` any $W$ satisfying $W' = v_0$. A rectangular strike is
  then `w * clip(s - a, 0, b - a)`, and the plateau comes out to $10^{-12}$.

  (2) **`simulate_string` is kick-drift-kick, stores a velocity, and gained `save_every`.** The
  stencil in §5.1's derivation (6) is exactly what runs: eliminating the velocity from velocity
  Verlet returns it, from the start $y^1 = y^0 + \Delta t\,v^0 + \tfrac12\Delta t^2 a^0$. The
  velocity form was chosen because `StringEvolution` promises $\partial y/\partial t$ at the
  same instants as $y$. It also makes the closing claim testable directly: handed to
  `coupled.simulate_coupled` as the chain $\mu\,\Delta x$ on $T/\Delta x$, the solver agrees
  to $10^{-14}$ over 2000 steps. `StringEvolution` carries `times, x, y, dydt`, with `x` beyond
  §4's list. `save_every` was added because a 2000-point, 4000-step run stored in full is 128 MB
  in the browser kernel. `tension` is a scalar: purely transverse motion makes a string's
  tension uniform by horizontal force balance, while `mu` may vary per point.

  (3) **`total_energy` came forward from `09-wave-energy`.** §4 assigns the fixed-end
  conservation test to this module, but lists the energy function under 09. As built,
  `total_energy` computes the kinetic term with trapezoid weights at the grid points and the
  potential term on the cells between them: the chain's energy, which velocity Verlet keeps
  bounded. The trapezoid is not a nicety. A free end moves as half a cell of string, and booking
  a whole cell there turns a $4.1\times10^{-4}$ wobble into $1.7\times10^{-2}$. `kinetic_density`,
  `potential_density` and `energy_flux` remain 09's to define, and 09 may re-express
  `total_energy` through them.

  (4) **The magic step is exact for plucks only.** §4 asks for "at $S = 1$ exactly, machine
  precision". A pluck gets it: $5.9\times10^{-15}$ after 400 steps, against $1.0\times10^{-5}$ at
  $S = 0.99$. A start with velocity does not. Its second time level is off at third order, and
  the exact transport spreads that into a settled second-order error, 7.5 times below
  $S = 0.5$'s but not rounding. The docstring, the tests and the page all say so.

  (5) **Photogates must be timed by centroid, and `measurement` gained `pulse_arrival_time`.**
  §4's scaling entry — measured speed against tension, exponent 0.50 — hid a trap. Timing the
  *peak* of a detector's record reads slow by $(1 - S^2)(\Delta x/\sigma)^2/4$: grid dispersion
  drags a pulse's peak back, matched to 0.4%. The centroid of the displacement responds only to
  the dispersion relation's slope at $k = 0$, where leapfrog is exact, and reads $v$ to
  $3\times10^{-9}$ at every $S$. With centroid timing and a fixed $\Delta t$, both fitted
  exponents are 0.5 to $10^{-9}$, so the scaling test is sharp rather than approximate. Under
  5% detector noise the centroid also scatters about three times less than the peak. The
  function lives in the shared `measurement` module, not in `waves.py`, because timing a pulse
  is analysis rather than physics, and modules 10 and 12 will time pulses too.

  (6) **Two convergence rates the plan did not anticipate.** The laboratory's continuum warm-up
  approaches the string at roughly $1/N$, not module 07's $1/N^2$, because the pluck is a
  triangle: 7.7%, 1.8% and 0.69% at $N = 5$, 20 and 100. A corner holds every wavelength, and
  the short ones sit near the band edge. The rectangular strike likewise converges at first
  order under refinement, the cost of a sampled discontinuity that module 04's rect pulse
  showed first. Both are stated where they occur rather than smoothed away.

  (7) **Glossary: `travelling-wave` is גל מתקדם, and two keys were added.** §5.1 proposed גל רץ.
  The deposit uses גל מתקדם, the form Hebrew physics texts use and the partner of the existing
  standing-wave entry גל עומד, with גל נודד rejected as proposed. Module 07's Hebrew page used
  the rejected form twice, and both were corrected in the authoring commit. `tension` and
  `courant-number` were added beyond §5.1's list: the page and laboratory rely on both, and the
  glossary is the only permitted source of their Hebrew.

  (8) **Media: longer shots, and one quantity §5.1 did not name.** The runtime budget says
  animations of at most 120 frames. The three shots run 300–310 frames, matching every render
  since the MP4 move — they render at authoring time and never in the browser, so the budget
  does not bind. Shot (c) adds a logarithmic panel of the grid's shortest-wave amplitude,
  because for a hundred steps the two strings look identical while the damage grows from
  rounding error at 1.3264 per step (von Neumann: 1.3266). Shot (b) runs at $S = 1$ so the
  triangle's corners stay sharp, with d'Alembert's halves as translucent fills. As lines, they
  sat under the string once separated, and only their flat stretches showed — under the wrong
  pulse.

  (9) **The real-experiment counterpart became problem 5.** No built module has a page section
  for experiments, and the slinky measurement works better as an exam-style problem. It adds a
  result §5.1 did not have: a stretched slinky's crossing time $\sqrt{ML/(k(L - L_0))}$ barely
  depends on the stretch when $L \gg L_0$, which makes a two-measurement test.

### 5.2 `09-wave-energy` — Wave energy: what actually travels (as built)

- **Identity and scope:** master-plan notebook 3.3: energy densities, flux, transport, the
  three-velocities distinction. Deferred: standing-wave energy budget (`11-standing-waves`);
  Poynting vector (`15-em-energy`); momentum beyond an honesty note (advanced only, below).
- **Prerequisites:** `08-wave-equation` (travelling solutions, $y_t = \mp v\,y_x$, the solver);
  `01-sho` (element energies).
- **Learning objectives:**
  - `OBJ-09-1` — Distinguish and compute three velocities — transverse medium velocity dy/dt,
    pattern velocity v, energy transport velocity — and state which can exceed which.
  - `OBJ-09-2` — Compute u_K = (1/2) mu (dy/dt)^2 and u_P = (1/2) T (dy/dx)^2 and locate where
    along a wave the energy sits.
  - `OBJ-09-3` — Derive the energy flux P = -T (dy/dx)(dy/dt) and verify the local conservation
    law du/dt + dP/dx = 0.
  - `OBJ-09-4` — Show that a travelling wave has u_K = u_P at every point and instant, that its
    energy travels at exactly v, and that a sinusoidal wave carries mean power
    (1/2) mu v omega^2 A^2.
  - `OBJ-09-5` — Contrast travelling and standing waves as energy transporters: the standing
    wave's time-averaged flux is zero everywhere.
- **Mathematical background:** has — partial derivatives, $y_t = -v\,y_x$ for right-movers; new —
  a local conservation law (density + flux + continuity), the course's template for every later
  one (Poynting, probability current).
- **Physical intuition goals:** (1) a travelling sine's energy lives at the zero crossings — steep
  and fast — not the crests; (2) work done at one end shows up at the other, later, having been
  *somewhere* in between; (3) doubling amplitude quadruples power; (4) a string element can move
  faster than the wave ($A\omega$ vs $v$ — independent knobs).
- **Section skeleton seeds:**
  - *puzzle:* ocean swell crosses the Pacific and slams a pier — but the water that hits was
    always local. Boxed: where does the energy live en route, and how fast does it move?
  - *predict:* (1) travelling sine — energy density largest at crests, zero crossings, or uniform?
    (targets NEW `energy-peaks-at-crests`); (2) can a piece of string outrun the wave? (3) double
    the amplitude — power up by what factor? (4) travelling vs standing — which delivers net
    energy across a mid-string point?
  - *explore:* energy-painted string (colour = $u(x,t)$; toggles $u_K$/$u_P$/total); flux arrows;
    a "wattmeter" station integrating $P\,dt$; travelling/standing presets; speck velocity vector.
  - *derive:* densities → flux as force × velocity → continuity → equipartition → mean power →
    standing-wave zero.
  - *verify:* pointwise $u_K = u_P$ for a simulated pulse (`numerical-observation`); solver
    total-energy conservation; wattmeter vs $\tfrac12\mu v\omega^2 A^2$; standing-wave average
    flux consistent with zero.
  - *transfer:* `11-standing-waves` (stored vs transported — the seed); `15-em-energy` (Poynting
    is this flux with fields); intensity $\propto A^2$ from `23-interference` on; cables.
  - *quiz:* energy location; power scaling; three velocities; standing-wave flux; flux sign.
  - *explain:* why the crest is the *least* energetic place; how energy flows through a medium
    that goes nowhere; what a negative $P$ means.
  - *advanced:* the momentum honesty note — longitudinal momentum carried by a transverse wave is
    a genuinely delicate $O(y^2)$ question whose answer depends on constitutive details the
    ideal-string model discards; the literature disagrees (flagged `open-question`); core stays at
    the flux level. Also energy velocity $P/u$ (= $v$ here), reopened in `13-dispersion`.
- **Core derivations:** (1) *densities:* an element $\mu\,dx$ moving at $y_t$ gives
  $u_K = \tfrac12\mu\,y_t^2$; stretching $ds - dx \approx \tfrac12 y_x^2\,dx$ against tension
  gives $u_P = \tfrac12 T\,y_x^2$ (`definition` boxes; honest about $|y_x| \ll 1$). (2) *flux:*
  the string left of $x$ pulls the right with transverse force $-T\,y_x$ acting at velocity $y_t$:
  $P = -T\,y_x\,y_t$. (3) *continuity:* $\partial_t(u_K + u_P) + \partial_x P = 0$ via the wave
  equation — the first local conservation law (`theorem`). (4) *equipartition:* for
  $y = f(x - vt)$, $y_t = -v\,y_x$, so $u_K = \tfrac12\mu v^2 y_x^2 = \tfrac12 T y_x^2 = u_P$ —
  equal at every point and instant, not merely on average (boxed as the module's surprise), and
  $P = T v\,y_x^2 = v\,(u_K + u_P)$: energy rides at exactly $v$. (5) *sinusoidal:*
  $y = \Real[A e^{\ii(kx - \omega t)}]$ gives $\langle P\rangle = \tfrac12\mu v\,\omega^2 A^2$.
  (6) *standing wave:* $y = A\sin kx\,\cos\omega t$ gives $P \propto \sin 2kx\,\sin 2\omega t$ —
  zero on time average everywhere (seed for `11-standing-waves`).
- **Model specification draft:** System — the ideal string of 08 carrying the derived fields
  $u_K$, $u_P$, $P$. Dynamics — the wave equation; energy quantities are diagnostics. Boundary —
  fixed ends for conservation checks (no flux through a fixed end: $y_t = 0$). Ensemble —
  deterministic; noise only in wattmeter cells. Ignored — dissipation, momentum-flux subtleties,
  longitudinal motion. Valid when — as 08, plus the $O(y_x^2)$ stretch expansion. Failure modes —
  densities read as exact for steep waves; the model's conserved energy assigned to a lossy
  string; "energy velocity" trusted once dispersion enters.
- **Epistemic classification:** density and flux expressions — `definition` (approximation
  flagged); continuity — `theorem`; equipartition and $P = vu$ — `theorem` with a
  `numerical-observation` companion; momentum delicacy — `open-question` box in advanced.
- **Misconceptions:** NEW `energy-peaks-at-crests` — "A wave's energy is concentrated at the
  crests, where displacement is biggest." Falsifier: energy-paint a travelling sine — colour
  maxima sit at the zero crossings (steepest, fastest) and the crests are momentarily *empty*;
  the lab plots $u(x)$ under $y(x)$ to make the offset unmissable. Distractor: "largest at the
  crests, since displacement is maximal there."
- **Glossary terms:** `energy-density` (צפיפות אנרגיה), `energy-flux` (שטף אנרגיה),
  `instantaneous-power` (הספק רגעי), `transverse-velocity` (מהירות רוחבית), `conservation-law`
  (חוק שימור), `continuity-equation` (משוואת רציפות).
- **Interactive controls and simulations:** beyond the explore bullets — amplitude/frequency
  sliders with a live $\langle P\rangle$ readout; flux arrows that visibly reverse where $P < 0$.
- **Virtual lab outline** (`notebooks/en/labs/09-wave-energy.ipynb`): (1) energy-paint a pulse;
  $u_K(x)$, $u_P(x)$ on one axis — they coincide; (2) sine: $u(x)$ under $y(x)$, find the offset
  (the falsifier); (3) wattmeter: sweep $A$ and $\omega$, fit both exponents (2 and 2); (4) total
  energy vs time; (5) standing wave: wattmeter averages to zero; (6) *measurement:* noisy
  wattmeter via `add_noise`, $\langle P\rangle \pm \sigma$ across seeds vs
  $\tfrac12\mu v\omega^2 A^2$.
- **Real-experiment counterpart:** reuse 08's slinky footage — track one taped coil for transverse
  velocity, compare its peak to the measured pulse speed: two velocities from one video,
  numerically different. (No affordable direct power measurement; the page says so.)
- **Media assets** (`render_waves.py`): (d) energy-painted travelling sine, colour maxima marching
  at the zero crossings; (e) pulse with coinciding $u_K$, $u_P$ curves beneath it.
- **Quiz bank outline:** `Q-09-1` MC energy location (OBJ-09-2, distractor
  `energy-peaks-at-crests`); `Q-09-2` numeric power scaling (OBJ-09-4); `Q-09-3` MC three
  velocities (OBJ-09-1); `Q-09-4` MC standing-wave net transport (OBJ-09-5); `Q-09-5` numeric
  flux sign/value from $y_x$, $y_t$ (OBJ-09-3); `Q-09-6` free — the continuity equation in words
  (OBJ-09-3).
- **Problem set outline:** analytical — $u_P$ from the stretch integral; continuity verified for
  $f(x - vt)$; mean power of a triangular wave. Computational — energy budget of a pluck: the
  pure-$u_P$ hump splits into two packets each with $u_K = u_P$. Challenge — the momentum question
  stated precisely with a guided reading note.
- **Runtime budget:** 08's runs plus per-step density arrays; seconds at most in Pyodide.
- **Validation gates:** standard set with `--module 09-wave-energy`; §4 flux/density tests here.
- **Open questions for the author:** cite the momentum literature explicitly? (recommendation: one
  citation); wattmeter in the page's `explore` or lab only (recommendation: lab only).
- **Open questions, as resolved when built.** Both recommendations were taken. The momentum note
  carries exactly one citation, and the choice of *which* is itself a decision: Rowland's 2011
  Eur. J. Phys. paper, rather than a general treatment, because it shows that the potential
  energy *density* — a quantity this module defines and uses — stops being unambiguous once
  longitudinal motion is taken seriously. A reference that undermines something the module
  actually asserts is worth more than one that merely reports a disagreement. The
  Abraham–Minkowski parallel was added beside it, forwarding to `16-light-in-matter`. The
  wattmeter is in the laboratory only; the page shows the flux through the third animation and
  quotes the laboratory's numbers, which is as much `explore` as it needs.
- **As-built deviations from this section.** Ten. The numerical ones are pinned by tests, and the
  first two are the only changes to what §4 said the part would contain.

  (1) **`sinusoidal_mean_power` is a fifth function, beyond §4's list.** §4 specifies
  `kinetic_density`, `potential_density`, `energy_flux` and `total_energy` and stops there,
  leaving $\langle P\rangle = \tfrac12\mu v\omega^2 A^2$ as something a caller would write out.
  Invariant 3 forbids that: it is physics, and the page, the laboratory and three tests all need
  it. Added as `sinusoidal_mean_power(amplitude, omega, tension, mu)`, whose docstring also
  carries the impedance form $\tfrac12 Z (A\omega)^2$ that part-06 onwards reuses.

  (2) **Four glossary keys belonging by subject to later modules were deposited here.**
  §5.2's list is the six the module owns, plus `equipartition`, which the page needs and the
  plan did not foresee. Beyond those, this page is the first in teaching order to use
  `impedance`, `phase-velocity`, `group-velocity` and `poynting-vector` in prose, and
  README.md's rule assigns a key to its earliest depositor. §5.3 and part-04 §5.2 now cite
  rather than deposit; the conflict log records all four. The `impedance` gap was the oldest of
  them: modules 00 and 02 have written עכבה in Hebrew since Part 0 with nothing in the glossary
  to hold them to it.

  (3) **The energy velocity converges at fourth order, and earned a box for it.** §5.2 asks for
  $P = vu$ as a `theorem` with a `numerical-observation` companion, expecting the companion to
  report second order like everything else. It does not: $1 - P/(vu)$ falls sixteenfold per
  halving of $\Delta x$ — $1.7\times10^{-5}$, $1.1\times10^{-6}$, $6.9\times10^{-8}$,
  $4.4\times10^{-9}$ — because the first-order departure from a pure right-mover cancels between
  the flux and the density, leaving its square. The equipartition it is built on converges at
  the ordinary second order, $1.8\times10^{-3}$ to $2.8\times10^{-5}$ over the same grids. The
  box says so, and the claim that a wave's energy travels at exactly $v$ is the most robust
  number in the module.

  (4) **The scheme satisfies a discrete conservation law exactly in space, which is a second
  box.** Not in the plan at all. Assign the kinetic energy to the grid points and the potential
  energy and flux to the cells between them — the cell's slope times the mean velocity of its
  two ends — and substituting the solver's own update makes every term cancel identically, for
  any $\Delta x$. So the residual is purely the time step: $3.3\times10^{-3}$,
  $8.3\times10^{-4}$, $2.1\times10^{-4}$ at $S = 0.5, 0.25, 0.125$ on one grid, while the same
  law read pointwise sits at $1.0\times10^{-2}$ and does not move when the step does. It is
  module 08's "the stencil is the chain" one level up, and the test carries both readings so the
  contrast cannot be lost.

  (5) **Every sinusoidal measurement runs on a windowed train launched with an analytic slope.**
  §5.2's verify and lab bullets ask for a wattmeter against $\tfrac12\mu v\omega^2A^2$ without
  saying what carries the sine, and a travelling sine cannot live on a string with fixed ends —
  it would have to move them. The train is windowed, flat-topped, and kept clear of both walls,
  and the gate averages over whole cycles of the flat part. Launching it with `np.gradient` of
  its own shape instead of the written-down derivative sends $(k\Delta x)^2/6$ of the shortest
  wave the other way, and the measured mean power then falls 1.4% below the closed form at
  100 Hz instead of 0.8%.

  (6) **The fitted frequency exponent is 1.995, not 2, and the shortfall is the measurement's.**
  The slope at the gate is recovered by a centred difference, which reads the slope of a sine
  low by $(k\Delta x)^2/6$ — 0.6% where a wavelength spans 32 grid points. The amplitude sweep
  has no such term and fits $2.000000$. The laboratory quotes both and explains the difference
  rather than rounding it away; it is module 08's centroid-against-peak lesson in a second
  costume.

  (7) **The noisy wattmeter grew a biased twin, and it became the measurement lesson.** §5.2's
  lab step (6) asks only for $\langle P\rangle \pm \sigma$ across seeds. As built there are two
  estimators on the same noisy record: one cross-differencing space and time, which is unbiased
  because the two noises come from disjoint samples, and one squaring a single slope record —
  legitimate algebra for a right-mover — which is biased high by $T v\sigma^2/(2\Delta x^2)$ and
  does not improve with averaging. On the laboratory's grid that is 26% of the signal, measured
  to within 1% of the prediction; on the finer test grid, 253%. `seed_study.agrees_with` accepts
  the first and rejects the second. Every later part of the course measures something
  proportional to an amplitude squared, so the course says once, here, that the square of a
  noisy number is not the noisy number's square.

  (8) **Three media shots, not two.** §5.2 lists the energy-painted sine and the pulse with
  coinciding densities. A third, `wave-energy-transport`, puts a travelling train and a standing
  mode side by side with a gate on each and plots what the gates see, because OBJ-09-5 otherwise
  has no picture and the module's last verification is its sharpest contrast. Both fluxes
  oscillate at twice the wave frequency and the standing peak is a quarter of the travelling
  one, so they share an axis with no scaling. The frame spacing these shots want is far past the
  Courant limit, so `_frame_step` divides it down to a stable step and saves every k-th one.

  (9) **The standing-wave contrast is stated in the densities as well as the flux.** §5.2 asks
  for zero time-averaged flux. The mirror-image result is at least as useful and costs one line:
  a standing wave's $u_K$ and $u_P$ are *not* equal pointwise — at release all potential, a
  quarter period later all kinetic, so their largest pointwise difference is the whole density —
  and only the cycle averages match, to $1.6\times10^{-4}$. Pointwise equipartition is thereby a
  signature of one-way travel rather than a fact about waves, which is what makes it worth a
  theorem box.

  (10) **A rejected spelling collided with an ordinary Hebrew word.** §5.3 proposes
  `he_reject: [אימפדנס, התנגדות]` for `impedance`, and deposit (2) brought it forward to this
  module. התנגדות is the right rejection — it is electrical *resistance* — and also the ordinary
  Hebrew for "objection", which this page's advanced section had used in that sense. The lint
  caught it on the first run over the new glossary. The rejection stands and the prose says
  השגה; module 10 will need the protection more than any one page needs the word. Recorded here
  because it will happen again.

### 5.3 `10-impedance` — Impedance: reflection and transmission at boundaries (as built)

- **Identity and scope:** master-plan notebook 3.4: impedance, junction conditions, reflection and
  transmission, energy bookkeeping, fixed/free limits, matching. Deferred: standing waves from
  repeated reflection (`11-standing-waves`); quarter-wave matching in full (`24-thin-films`); the
  EM version of the algebra (`18-fresnel`).
- **Prerequisites:** `08-wave-equation` (travelling waves; solver with piecewise $\mu$);
  `09-wave-energy` (flux — the bookkeeping's currency); `00-phasors` (complex amplitudes).
- **Learning objectives:**
  - `OBJ-10-1` — Compute the impedance Z = sqrt(T mu) = mu v and interpret it as the transverse
    force per unit transverse velocity the medium presents to whatever drives it.
  - `OBJ-10-2` — Apply the junction conditions (continuity of displacement and of transverse
    force) to derive r = (Z1 - Z2)/(Z1 + Z2) and t = 2 Z1/(Z1 + Z2) for displacement amplitudes.
  - `OBJ-10-3` — Predict pulse reflection at fixed (Z2 -> infinity, r = -1) and free (Z2 -> 0,
    r = +1) ends as limits of the junction formulas, including the reflected pulse's sign.
  - `OBJ-10-4` — Verify energy conservation R + T = 1 with R = r^2 and T = (Z2/Z1) t^2, and
    explain why t can exceed 1 while power is conserved.
  - `OBJ-10-5` — State the impedance-matching condition r = 0 and give physical examples
    (ultrasound gel, cable termination); anticipate the quarter-wave idea qualitatively.
- **Mathematical background:** has — travelling-wave phasors, flux; new — matching conditions at
  an interface (the template for every boundary problem through `18-fresnel` and beyond), solving
  small linear systems of amplitudes.
- **Physical intuition goals:** (1) a wall is just an infinitely heavy second medium; (2) the
  reflection flips iff the far side is "harder" ($Z_2 > Z_1$); (3) a transmitted displacement can
  exceed the incident one and no energy law minds; (4) no mismatch, no echo.
- **Section skeleton seeds:**
  - *puzzle:* the ultrasound technician squirts gel on your skin — without it the image is black:
    at a skin–air gap nearly all the sound reflects. A rope tied to a wall returns your pulse
    upside down; tied to a thin thread, right side up. Boxed: at a change of medium, what decides
    how much bounces, how much crosses, and which way up?
  - *predict:* (1) pulse hits a wall — upright or inverted return? (2) heavy rope to light string:
    reflection upright or inverted, transmitted pulse taller or shorter? (targets NEW
    `reflection-always-inverts`); (3) can the transmitted amplitude exceed the incident? (4) is
    there a junction with *no* reflection at all?
  - *explore:* junction sandbox — $\mu_2/\mu_1$ on a log slider (common $T$); live $r, t$ readouts
    vs the formula; energy bars (incident = reflected + transmitted); fixed/free presets at the
    slider's ends; sinusoidal mode showing the wavelength change (same $\omega$, different $k$).
  - *derive:* impedance of a semi-infinite string → junction conditions → $r, t$ → limits →
    energy bookkeeping → matching.
  - *verify:* measured amplitude ratios vs $r$, $t$ across the sweep; integrated pulse energies
    giving $R + T = 1$ (`numerical-observation`); matched junction echo-free to grid tolerance.
  - *transfer:* `11-standing-waves` ($r = \mp1$ at the ends is why modes exist); `18-fresnel` and
    `24-thin-films` (the unification box); `26-fabry-perot` (two junctions, many bounces);
    `16-light-in-matter` (same $\omega$, new $k$); coax termination; tsunami growth in shallowing
    water as an impedance gradient.
  - *quiz:* reflection sign by cases; $r, t$ numerics; the $t > 1$ paradox; matching; the gel.
  - *explain:* why wall and free end are opposite limits of one formula; how the transmitted pulse
    can be taller yet weaker; what the gel is *for*, in one sentence.
  - *advanced:* flux-factor derivation of $R, T$ in full; impedance analogues table (string
    $\sqrt{T\mu}$, sound $\rho c$, transmission line $\sqrt{L'/C'}$); a three-segment string with
    an intermediate $Z = \sqrt{Z_1 Z_3}$ quarter-wave section as a `24-thin-films` teaser; the
    momentum kick on the wall at reflection.
- **Core derivations:** (1) *impedance:* drive a semi-infinite string at $x = 0$; the outgoing
  wave obeys $y_t = -v\,y_x$, so the transverse driving force is
  $F = -T\,y_x = (T/v)\,y_t = Z\,y_t$ with $Z = T/v = \sqrt{T\mu} = \mu v$ (`definition`, boxed):
  what the medium feels like to push — force per velocity, drag-like and real, because energy
  leaves and never returns. (2) *junction:* incident $A\,e^{\ii(k_1x - \omega t)}$, reflected
  $rA\,e^{\ii(-k_1x - \omega t)}$, transmitted $tA\,e^{\ii(k_2x - \omega t)}$; the string is
  unbroken ($y$ continuous) and the junction massless ($-T\,y_x$ continuous); same $\omega$ both
  sides, $k = \omega/v_{1,2}$ adjusts; the conditions give $r = (Z_1 - Z_2)/(Z_1 + Z_2)$,
  $t = 2Z_1/(Z_1 + Z_2)$, with $1 + r = t$ as the built-in check. (3) *limits:* $Z_2 \to \infty$:
  $r = -1, t = 0$ (fixed end, inverted image); $Z_2 \to 0$: $r = +1, t = 2$ (free end,
  displacement doubling). (4) *energy:* powers $\tfrac12 Z_1\omega^2A^2$,
  $\tfrac12 Z_1\omega^2 r^2A^2$, $\tfrac12 Z_2\omega^2 t^2A^2$ give $R = r^2$,
  $T = (Z_2/Z_1)\,t^2$, and $R + T = 1$ by algebra — the flux factor $Z_2/Z_1$ is why $t = 2$
  carries almost no power into a nearly-free medium. (5) *matching:* $r = 0$ iff $Z_1 = Z_2$;
  matching genuinely different media needs an intermediate layer, and a $\lambda/4$ section of
  $Z = \sqrt{Z_1 Z_3}$ does it. TRAILED, not derived: the full treatment is `24-thin-films`.
- **Model specification draft:** System — two semi-infinite ideal strings, common tension $T$,
  densities $\mu_1, \mu_2$, joined at $x = 0$ (numerically one grid, piecewise $\mu$). Dynamics —
  the wave equation each side; matching conditions at the junction. Boundary — the junction, plus
  fixed/free outer ends kept out of reach. Ensemble — deterministic; noise in measurement cells.
  Ignored — junction mass, stiffness, damping; oblique incidence has no meaning in 1-D. Valid
  when — as 08, both sides; the junction is a point (a smeared gradient is a different problem,
  flagged in the problem set). Failure modes — reading $t > 1$ as energy gain; applying amplitude
  $r, t$ to power; forgetting the flux factor $Z_2/Z_1$.
- **Epistemic classification:** impedance — `definition` (boxed); $r, t$ formulas — `theorem`;
  $R + T = 1$ — `theorem`, verified as a `numerical-observation` on integrated pulse energies;
  **the unification box** — an `important` admonition stating explicitly: *this same algebra
  returns as the Fresnel equations at normal incidence (`18-fresnel`) and as anti-reflection
  coatings (`24-thin-films`); ultrasound gel and cable terminators are impedance matching; one
  calculation, many costumes* — one of the course's great unifications, planted here on purpose.
- **Misconceptions:** NEW `reflection-always-inverts` — "A reflected pulse always comes back
  upside down." Falsifier: junction sweep in the sandbox — inversion occurs only for $Z_2 > Z_1$;
  free-end and heavy-to-light runs return the pulse upright, and the live $r$ readout changes sign
  exactly at $Z_2 = Z_1$. Distractor: "inverted in both cases, since reflection always flips a
  pulse."
- **Glossary terms:** `impedance` — deposited by `09-wave-energy`, whose page is the first to
  use the word (see §5.2's as-built deviation 2); this module cites it. New here:
  `reflection-coefficient`
  (מקדם החזרה), `transmission-coefficient` (מקדם העברה), `junction` (צומת; translator to weigh
  חיבור), `impedance-matching` (תיאום עכבות), `fixed-end` (קצה קבוע), `free-end` (קצה חופשי).
- **Interactive controls and simulations:** beyond the explore bullets — a "find the match" game
  (dial $\mu_2$ until the echo vanishes); the three-segment quarter-wave teaser (lab only).
- **Virtual lab outline** (`notebooks/en/labs/10-impedance.ipynb`): (1) fixed and free ends — sign
  of the return; (2) junction sweep: measured amplitudes over the $\mu_2/\mu_1$ decades, overlay
  $r$, $t$; (3) energy bookkeeping via `total_energy` windows, verify $R + T = 1$; (4) matching
  game; (5) *measurement:* noisy amplitudes via `add_noise`, $r \pm \sigma_r$ at three ratios vs
  the formula; (6) advanced: the quarter-wave three-segment run.
- **Real-experiment counterpart:** join two visibly different ropes (or slinky + light cord), film
  a pulse hitting the junction from each side; classify upright/inverted, estimate amplitude
  ratios frame-by-frame; same CSV import path as 08.
- **Media assets** (`render_waves.py`): (f) pulse hitting fixed vs free end side by side; (g)
  junction pair heavy→light and light→heavy; (h) matched junction: the echo that isn't there.
- **Quiz bank outline:** `Q-10-1` MC reflection signs by cases (OBJ-10-3, distractor
  `reflection-always-inverts`); `Q-10-2` numeric $r, t$ from $\mu_1, \mu_2$ (OBJ-10-2); `Q-10-3`
  MC the $t = 2$ paradox — where did the energy go (OBJ-10-4); `Q-10-4` numeric $R + T$ with flux
  factors (OBJ-10-4); `Q-10-5` MC which junction is echo-free (OBJ-10-5); `Q-10-6` free —
  impedance in words (OBJ-10-1); `Q-10-7` MC the gel question (OBJ-10-5).
- **Problem set outline:** analytical — derive $r, t$; fixed/free limits by images; the
  $R + T = 1$ algebra. Computational — smeared junction: replace the step in $\mu$ by a ramp of
  width $w$, measure $R(w/\lambda)$ — the echo fades as the ramp widens (adiabatic matching, a
  discovery problem). Challenge — the quarter-wave transformer on strings: a $\sqrt{Z_1Z_3}$
  section of length $\lambda/4$ kills the reflection at one frequency; plot $R(\omega)$ (the
  `24-thin-films` curve, met early).
- **Runtime budget:** two-media runs $\le 3000$ points, $\le 6000$ steps; the sweep is $\sim 20$
  runs — a few seconds in Pyodide; the $R(\omega)$ challenge stays under $\sim 10$ s.
- **Validation gates:** standard set with `--module 10-impedance`; §4 limit and
  junction-conservation tests land here.
- **Open questions for the author:** pulse pictures or phasor algebra first in the junction
  derivation (recommendation: pulses first, phasors second); analogue table in core or advanced
  (recommendation: advanced). Both went the way the plan recommended.

- **As-built deviations from this section.** Ten. The first is the one that moved the module:
  the plan's central image of a matched junction turns out not to exist on a string.

  (1) **A matched junction cannot exist inside one string.** Tension is a single number from end
  to end — the model's own consequence, stated in `waves.py`'s docstring since 08 — so
  $Z_1 = Z_2$ means $\mu_1 = \mu_2$, and "the matched junction" is a string with no junction in
  it. The plan's shot (h) would therefore have animated a uniform string doing nothing. The page
  says this in as many words and moves matching to where it is not trivial, which costs nothing:
  the criterion $r = 0$ and its examples (gel, cable terminator) are unaffected, because in media
  whose two constants are free of each other the match is a real achievement.

  (2) **Shot (h) became the quarter-wave comparison.** A six-cycle packet meets a 3:1 impedance
  step bare and then through a $\sqrt{Z_1Z_3}$ section 57.7 mm long: $R = 0.2504$ against the
  formula's $0.2500$, falling to $0.0077$ — an echo thirty-two times weaker in energy. §5.3 had
  the three-segment string as a laboratory extra and an advanced teaser only. It is now also the
  page's third animation, because it is the only matching a string can *show*, and because it
  puts a cancellation of two reflections on screen two parts before interference is taught.

  (3) **The coefficient functions refuse infinite and zero arguments.** §4's sketch is silent;
  the built `junction_coefficients` and `power_coefficients` raise on a non-finite impedance,
  with the message that fixed and free ends are limits of these formulas rather than values of
  them. A module whose argument is that a wall is not a special case should not ship a special
  case for it. `impedance` itself took `wave_speed`'s overloads, so a varying density gives a
  varying $Z$ and the laboratory's sweep is one call.

  (4) **A convergence test beyond §4's list.** §4 assigns convergence to the FDTD-vs-d'Alembert
  comparison and stops. But a junction is a step the grid can only place to within $\Delta x$,
  so "does the simulation agree with $r$" is a question about resolution before it is a question
  about physics: the measured reflected amplitude misses $-1/3$ by $8.9\times10^{-4}$,
  $2.2\times10^{-4}$, $5.6\times10^{-5}$, $1.4\times10^{-5}$ at 10, 20, 40 and 80 points across
  the pulse. Second order, like everything else this solver does, and now the page's
  verification 4 and the gate the animations sit behind.

  (5) **Reciprocity is exact, measurable, and absent from the plan.** $R(Z_1,Z_2) = R(Z_2,Z_1)$
  holds to $10^{-15}$ as algebra and shows up in the weighed energies as two identical rows —
  $\mu_2/\mu_1 = 1/4$ and $4$ both return $0.111320$ of the pulse — while their amplitudes are
  entirely different ($+1/3$ against $-1/3$, $4/3$ against $2/3$). Energy cannot tell which way
  the wave was going; the displacement can. It is in the limits test, the conservation test, the
  page's second table and `Q-10-4`'s feedback.

  (6) **The measurement part needed a second estimator, not noisier data.** §5.3 asks for "noisy
  amplitudes via `add_noise`, $r \pm \sigma_r$ at three ratios vs the formula", which as written
  teaches nothing module 09 had not already taught. Built with two estimators on the same frame
  it does: a projection onto the expected pulse shape is linear in the data and returns the
  noiseless answer, while picking the largest excursion — what an eye does — is biased away from
  zero by 23% at $\mu_2/\mu_1 = 1/4$ and 29% at 4, and no number of frames repairs it. The
  laboratory reuses `validation.seed_study` for both, so the bias is reported with a standard
  error rather than asserted.

  (7) **The falsifier is the pair shot and the sweep, not the sandbox readout.** §5.3 puts the
  live $r$ readout in the explore sandbox at the centre of `reflection-always-inverts`. As built
  the falsifier is animation (g) — one junction approached from both sides, in step — backed by
  the laboratory's eleven-point measured sweep, where the sign turns over at $\mu_2 = \mu_1$ and
  nowhere else. The sandbox survives as the matching game of part 8.

  (8) **The real-experiment counterpart shipped with the module.** Module 09 needed a second
  commit for its own. Here it is problem 8 from the start, and it is built around the one thing
  a phone can measure with no calibration whatsoever: the *sign* of the reflection from each
  side of a knot. Amplitudes follow, with the estimator bias of (6) as the reason the naive
  reading comes out high.

  (9) **The `junction` glossary key carries no rejected spelling.** §5.3 asks the translator to
  weigh חיבור against צומת. צומת is right — the junction as a place — but recording חיבור as
  `he_reject` is not the way to say so: it is an ordinary word that pages 05 and 07 and the
  Hebrew index already use for coupling and for addition, and the lint rejected all three on the
  first run. Weighed, not taken, and deliberately not rejected. The comment in `terms.yml` says
  why, as §5.2's deviation (10) predicted this would need saying again.

  (10) **The optical unification had to be corrected after it was written.** The transfer box
  first claimed the Fresnel coefficients are this module's formulas "with the optical impedance
  $Z \propto 1/n$ in place of $\sqrt{T\mu}$". Substituting $Z = Z_0/n$ into
  $r = (Z_1 - Z_2)/(Z_1 + Z_2)$ returns the *negative* of the Fresnel result, and the analogue
  table then explained a sign that was not there. Part-06's plan already had the right account
  and the page now carries it: the index sits in the slot where $Z$ sits, letter for letter,
  because the amplitude quoted for light is $E$ — the force-like member of its pair — where a
  string's $y$ is the motion-like member of ours, and the two inversions cancel. Worth recording
  because module 18's planned unification test compares `fresnel_rs(n1, n2, 0)` against
  `junction_coefficients(n1, n2)`, indices in the impedance slot, and would have looked wrong
  against a page that said otherwise.

## 6. Part-level assessment and capstone hooks

- Master plan §23's virtual-lab table lists "String — wave velocity" and "Interface —
  reflection/transmission coefficients": exactly 08's and 10's labs, built once here and reused as
  apparatus by Parts IV–VI.
- Capstone §35.4 (optical communication) inherits impedance matching as the reason fiber
  connectors and terminations exist; §35.2 (virtual optical bench) consumes the junction algebra
  through its `18-fresnel` descendant.
- Cross-module synthesis problem (with this part's problem sets): a pluck on a composite string —
  d'Alembert splits it (08), each half carries equal $u_K$ and $u_P$ (09), the right-mover divides
  at a junction by $r, t$ (10); account for every joule end to end.
- Exam themes: what sets $v$; energy location on a travelling wave; reflection sign by cases;
  $R + T$ bookkeeping with flux factors; CFL numeric.

## 7. Build order and validation gates

Build `08-wave-equation` first (the solver and d'Alembert evaluator are the part's apparatus),
then `09-wave-energy` (adds density/flux functions and the conservation diagnostics 10 needs),
then `10-impedance` (consumes both). All three follow part-02's modules in teaching order.

With 08: create `waves.py` with the §4 docstring and the 08-scoped functions; execute the README
conflict-log re-point of `wave-carries-medium` (`assigned_module: 04-waves` → `08-wave-equation`,
status `addressed` once the page lands); add NEW registry entry `speed-set-by-source`; deposit
08's glossary terms. With 09: add `energy-peaks-at-crests` plus the flux/density functions and
tests. With 10: add `reflection-always-inverts` plus the junction functions and limit tests. The
§4 test additions must land *with* their modules — part-04's plan cites the solver and
conservation guarantees as prerequisites for its packet work.

Per module: the standard four gates (README). Additionally: run the convergence gate (FDTD vs
d'Alembert) before any content screenshot or MP4 is rendered, so every published frame comes from
a validated solver.

## 8. Deviations from the master plan

- **Merge 3.1 + 3.2 → `08-wave-equation`** (precedent: `02-damped-driven` ← 1.2 + 1.3). Deriving
  the wave equation and exhibiting its travelling solutions are one motion — the solution is the
  payoff that justifies the derivation; split pages would strand 3.1 without a punchline. Master
  plan 3.2's interactives (launch, reverse, superpose, measure) all survive inside 08.
- **`waves.py` ownership split with part-04** (README ownership table; both plans state it). This
  plan owns the file's docstring model spec and exactly the string-dynamics core: `wave_speed`,
  `impedance`, `cfl_max_dt`, `simulate_string`, `dalembert_solution`, `kinetic_density`,
  `potential_density`, `energy_flux`, `total_energy`, `junction_coefficients`,
  `power_coefficients`. Packet construction, group velocity, and dispersion-relation functions are
  specified only in part-04's plan, though they live in the same file. Neither plan redefines the
  other's functions.
- **Registry re-point:** `wave-carries-medium` moves `04-waves` → `08-wave-equation` per the
  README conflict log; the one-line YAML edit ships with module 08, not before.
- **Scope choice on 3.1's "possible physical systems":** the string is the single core system;
  acoustic pressure and the elastic rod appear only as the impedance-analogue table in 10's
  advanced section. One system fully owned beats three sketched.
- **Additions beyond the master plan:** the double derivation with the chain/continuum dictionary;
  the leapfrog-stencil-equals-mass-chain closing loop; CFL as a designed blow-up experiment; the
  travelling-wave equipartition box; the honest momentum `open-question`; the Fresnel/thin-film
  unification box in 10; three NEW registry misconceptions (`speed-set-by-source`,
  `energy-peaks-at-crests`, `reflection-always-inverts`).
