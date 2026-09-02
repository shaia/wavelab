---
title: "Coupled oscillators: the sympathy of pendulums"
short_title: 06 · Coupled
module: 06-coupled
objectives:
  - id: OBJ-06-1
    text: Write the equations of motion of two coupled oscillators in the matrix form M x'' + K x = 0, and assemble M and K for given masses and springs.
  - id: OBJ-06-2
    text: Identify from simulation the initial conditions under which the pair oscillates at a single frequency with no energy exchange, and define those motions as the normal modes.
  - id: OBJ-06-3
    text: Predict the energy-exchange period of two weakly coupled identical oscillators from the mode splitting, T_ex = 2 pi / (omega_a - omega_s), and connect the exchange to beats between the two mode frequencies.
  - id: OBJ-06-4
    text: Decouple the pair with the normal coordinates q_pm = (x1 pm x2)/sqrt(2), and show that each obeys an independent single-oscillator equation.
  - id: OBJ-06-5
    text: Estimate the mode splitting in the weak-coupling limit as omega_a - omega_s approx omega0 k_c / k for k_c << k, and classify coupling as weak or strong by comparing the splitting with omega0.
---

# Coupled oscillators: the sympathy of pendulums

(06-coupled-puzzle)=
## The puzzle: the pendulum that stops itself

Hang two identical pendulums from the same slightly slack string. Start one swinging and leave
the other hanging still. Come back a minute later and you find the opposite: the one you
started is hanging dead, and the one you never touched is swinging.

Wait the same time again and it has reversed. Nothing is being damped away — a minute after
that, the first pendulum is swinging as widely as when you let it go.

Christiaan Huygens noticed something like this in 1665, from a sickbed, watching two clocks
hung on a common beam settle into step with each other. He called it "an odd kind of sympathy".

:::{important} The question
How does the motion know how to come back? Nothing is keeping score. And — the question that
turns out to open the whole subject — can the pair be started so that *nothing* is exchanged
at all?
:::

Hold on to how strange the first pendulum's behaviour is. It slows to a complete stop without
any friction, and then, unprompted, starts again.

(06-coupled-predict)=
## Predict before you calculate

Commit to an answer for each *before* running anything. Write them down.

1. You start pendulum 1 alone and wait a long time. Where is the energy — mostly still in
   pendulum 1, mostly in pendulum 2, or split evenly between them?
2. How many ways are there to start the pair so that no energy is ever exchanged? Zero, one,
   two, infinitely many?
3. You stiffen the coupling between them. Does the trading get faster or slower?
4. Does either of the no-exchange motions, if they exist, happen at exactly the frequency a
   single uncoupled pendulum would have?

:::{note} Why we ask first
Question 1 is the module's misconception, and intuition pulls hard toward "mostly where I put
it". Question 4 looks like a technicality and is the key to the whole derivation — one of the
two answers is *exactly* yes, for a reason you can see rather than calculate.
:::

(06-coupled-explore)=
## Explore the model

Three animations, all generated from the same `wavelab.coupled` code the laboratory runs.

:::{figure} ../media/coupled-exchange.mp4
:width: 100%

One mass started alone, with the two displacements in the middle and the energy held by each
mass on the right. Watch the bars rather than the masses: they pulse in antiphase beneath the
dashed line, which marks the total. The total never moves. Pendulum 1 does not slow down
because something is draining it — nothing is — but because its energy is somewhere else, and
it comes back.
:::

:::{figure} ../media/coupled-modes.mp4
:width: 100%

The two motions that never trade anything. Top: both masses move together, and the green
coupling spring keeps exactly its rest length the whole time. Bottom: they move in opposite
directions, and the coupling spring stretches and compresses twice a cycle. Each of these
repeats for ever at a single frequency, with no sloshing at all.
:::

:::{figure} ../media/coupled-site-vs-mode.mp4
:width: 100%

The same motion as the first animation, in two pictures at once. Left: energy per mass, which
trades back and forth. Right: energy per *mode*, which does not move. Neither picture is more
true than the other. The right-hand one is simply the picture in which the answer is already
two constant numbers, and finding it is what this module is for.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** two identical point masses, each held to a wall by a spring of stiffness $k$ and joined to each other by a coupling spring of stiffness $k_c$ — equivalently two small-angle pendulums on a shared support; the observables are the two displacements, their velocities, and the energy attributed to each mass or to each mode.
- **Dynamics:** $M\ddot{\mathbf{x}} + K\mathbf{x} = 0$ with $M = m\,\mathbb{1}$, integrated by velocity Verlet and solved exactly by decomposition into two independent oscillators.
- **Boundary:** both outer springs anchored to rigid supports that never move and never absorb anything.
- **Ensemble:** a single deterministic trajectory per choice of initial conditions; measurement noise, where added, is Gaussian, independent and seeded.
- **Ignored:** damping and driving — the pair here is free and conservative; also spring masses, the pendulum's large-angle nonlinearity, and the escapement mechanics of the real clocks that gave Huygens his observation.
- **Valid when:** displacements stay in the linear range of the real springs (small angles for pendulums), and the time step stays well below the period of the faster mode.
- **Failure modes:** amplitudes large enough for nonlinearity to couple the modes, at which point superposition itself fails; damping added carelessly, since the modes stay independent only for special damping; and reading the site picture as though it were fundamental.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 06 — coupled oscillators](/lite/lab/index.html?path=en/labs/06-coupled.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/06-coupled.ipynb`.
:::

Run the laboratory now, then come back. Three things are worth doing before you read on:

- Start one mass and time how long the energy takes to arrive at the other and return. Then
  stiffen the coupling and time it again.
- Hunt for the no-exchange starts by hand. Set $x_2/x_1$ to different ratios, release from
  rest, and watch the energy bars. Two ratios make the sloshing stop completely; find them
  before anyone tells you what they are.
- Having found them, check whether either one swings at the frequency a single mass on its
  anchor spring would have.

(06-coupled-derive)=
## Derive the result

**Two masses, three springs.** Let $x_1$ and $x_2$ be the displacements from rest. Mass 1 feels
its own anchor spring pulling it back, and the coupling spring, which cares only about how much
*further apart* the two masses are than at rest:

$$
m\ddot{x}_1 = -k x_1 - k_c\,(x_1 - x_2),
\qquad
m\ddot{x}_2 = -k x_2 - k_c\,(x_2 - x_1).
$$

Each equation contains the other mass's coordinate. That is what "coupled" means, and it is why
neither can be solved on its own. Collect them:

$$
M\ddot{\mathbf{x}} + K\mathbf{x} = 0,
\qquad
M = \begin{pmatrix} m & 0 \\ 0 & m \end{pmatrix},
\qquad
K = \begin{pmatrix} k + k_c & -k_c \\ -k_c & k + k_c \end{pmatrix}.
$$

The off-diagonal entries of $K$ are the coupling and nothing else. Set $k_c = 0$ and the matrix
is diagonal, the two equations fall apart, and the masses never learn of each other's existence.

**Look for a motion at a single frequency.** The prediction section asked whether such motions
exist. Assume one does and see what it must satisfy. Try
$\mathbf{x} = \mathbf{a}\cos\omega t$, with a fixed *shape* $\mathbf{a}$ and one frequency for
both masses. Two derivatives bring down $-\omega^2$, and the cosine divides out:

$$
\left(K - \omega^2 M\right)\mathbf{a} = 0 .
$$

A matrix times a nonzero vector giving zero means the matrix has no inverse, so its determinant
vanishes:

$$
\det\begin{pmatrix} k + k_c - m\omega^2 & -k_c \\ -k_c & k + k_c - m\omega^2 \end{pmatrix}
= \left(k + k_c - m\omega^2\right)^2 - k_c^2 = 0 .
$$

That is a difference of two squares, so it factors immediately:
$k + k_c - m\omega^2 = \pm k_c$. Two roots, and with them two shapes:

$$
\omega_s = \sqrt{\frac{k}{m}} = \wnat,
\qquad
\mathbf{a}_s \propto \begin{pmatrix} 1 \\ 1 \end{pmatrix};
\qquad\qquad
\omega_a = \sqrt{\frac{k + 2k_c}{m}},
\qquad
\mathbf{a}_a \propto \begin{pmatrix} 1 \\ -1 \end{pmatrix}.
$$

There is the answer to prediction 2: exactly two. And to prediction 4, which is the more
interesting one.

:::{admonition} The symmetric mode never notices the coupling
:class: theorem
$\omega_s = \wnat$ **exactly**, for any coupling strength whatsoever. You can see why without
the algebra: in that motion the two masses move together, in step, so the distance between them
never changes, so the coupling spring never stretches. A spring that never changes length exerts
no changing force and cannot affect the period. Stiffen the coupling as much as you like and
this motion is untouched.

The other mode is the opposite case — the masses move against each other, so the coupling spring
is worked hardest, and it is stiffer and faster: $\omega_a > \omega_s$ whenever $k_c > 0$.
:::

These two motions are the **normal modes**. Their existence is not obvious and their number is
not accidental: two masses, two modes. And because the equations are linear, any sum of the two
is also a solution — which turns out to be every solution there is.

**Normal coordinates: the same fact as a change of variables.** Add and subtract the two
equations of motion and define

$$
q_+ = \frac{x_1 + x_2}{\sqrt2},
\qquad
q_- = \frac{x_1 - x_2}{\sqrt2}.
$$

The addition gives $m\ddot{q}_+ = -k q_+$, because the coupling terms cancel exactly. The
subtraction gives $m\ddot{q}_- = -(k + 2k_c) q_-$, because they reinforce. So

$$
\ddot{q}_+ + \wnat^2 q_+ = 0,
\qquad
\ddot{q}_- + \omega_a^2 q_- = 0 .
$$

Two independent module-01 oscillators, with no trace of each other. Nothing was thrown away —
$q_\pm$ carry exactly the information $x_{1,2}$ do — and yet in these coordinates the problem
has no coupling in it at all. The coupling was never in the physics; it was in the *choice of
coordinates*, and a different choice removes it. That sentence is the whole of Part II, and the
rest of the course keeps finding new systems it applies to.

**Starting one mass.** Now solve the puzzle. Release from rest with $x_1 = A$, $x_2 = 0$. In
normal coordinates that is $q_+ = q_- = A/\sqrt2$: *equal* amounts of both modes. Each then
oscillates at its own frequency, and converting back,

$$
x_1(t) = A\cos\!\left(\frac{\Delta\omega}{2}t\right)\cos\bar\omega t,
\qquad
x_2(t) = A\sin\!\left(\frac{\Delta\omega}{2}t\right)\sin\bar\omega t,
$$

with $\Delta\omega = \omega_a - \omega_s$ and $\bar\omega = (\omega_s + \omega_a)/2$.

This is module 00's beat identity, unchanged. Two nearby frequencies added give a fast
oscillation at their mean inside a slow envelope at half their difference — except that here
the two envelopes belong to two different objects, and where one is large the other is small.
The energies go as $\cos^2$ and $\sin^2$ of $\Delta\omega t/2$, so they hand over completely and
come back:

$$
T_{\text{ex}} = \frac{2\pi}{\Delta\omega} .
$$

There is the answer to the puzzle. Nothing keeps score; the two modes simply run at slightly
different rates, and the pattern of who-has-the-energy is set by how far out of step they have
drifted. Full transfer at $T_{\text{ex}}/2$, full return at $T_{\text{ex}}$.

**How big is the splitting?** For weak coupling, $k_c \ll k$, expand the square root:

$$
\omega_a = \wnat\sqrt{1 + \frac{2k_c}{k}} \approx \wnat\left(1 + \frac{k_c}{k}\right)
\qquad\Longrightarrow\qquad
\Delta\omega \approx \wnat\,\frac{k_c}{k},
\qquad
T_{\text{ex}} \approx \frac{2\pi}{\wnat}\,\frac{k}{k_c} .
$$

Stiffer coupling, wider splitting, faster trading — the answer to prediction 3, and it is
inverse rather than merely monotonic. Turn it around and it becomes a measuring instrument: a
slow, clean exchange is the signature of a *small* splitting, and timing the sloshing measures a
frequency difference far too small to see on any spectrum.

The estimate is a weak-coupling estimate and should be trusted like one — it runs 1% low at
$k_c/k = 0.02$, 5% at $0.1$, and 17% at $0.5$, where the expansion has no business being used.

(06-coupled-verify)=
## Verify computationally

Each check below is also a test in the project's suite, so these claims cannot silently rot.

**1. The hand-solved modes.** The frequencies and shapes derived above by determinant, against
`normal_mode_solve` working numerically on the same matrices: they agree to $10^{-15}$, at
couplings from $k_c/k = 0.006$ to $5$. The symmetric frequency is $\wnat$ to the last bit every
time.

**2. The falsifying experiment.** Released with one mass displaced, `site_energies` is tracked
through a full exchange period.

:::{admonition} Where the energy actually goes
:class: numerical-observation
Mass 1's share falls from 98% to **0.06%** of the total within half an exchange period, and
returns to 98% by the end of it. The total is constant throughout to better than one part in
$10^3$ — the residual is the integrator's, not the physics'. There is no damping anywhere in
the model, so nothing was lost; the energy was simply elsewhere.

Two details are worth pausing on. Mass 1 starts with 98% rather than 100% because the coupling
spring is already stretched at $t = 0$, and its energy belongs to both masses at once. And this
is a *weak*-coupling result: at $k_c = k$ the transfer is genuinely incomplete, with 7.4% never
leaving mass 1 at all.
:::

**3. The exchange is the beat.** The simulated $x_1(t)$ is laid over
`phasors.beat_signal` evaluated at the two mode frequencies. They agree to better than
$5\times 10^{-3}$ of the amplitude, and the integrator knows nothing about either mode — so a
measurement of module 00's identity in a new setting, not a restatement of it.

**4. The scaling law.** $T_{\text{ex}}$ is measured across a decade of coupling strengths and
fitted on log-log axes. The exponent comes out $-0.991$ against the predicted $-1$ over
$k_c/k \in [0.005, 0.05]$. Extend the sweep into strong coupling and it drifts to $-0.830$,
which is the approximation failing exactly where it was derived to fail.

**5. Modes hold still while sites slosh.** The same trajectory, read both ways: the site
energies traverse essentially the whole total, while the modal energies are constant to a part
in $10^5$. The bound does not grow when the run is made four times longer — the integrator is
symplectic, so its error oscillates instead of accumulating.

(06-coupled-transfer)=
## Transfer the idea

- **More of everything.** Two masses gave two modes. Twenty give twenty, and the counting is
  not a coincidence; [module 07](07-normal-modes.md) does the general case and then lets the
  number of masses run away to infinity, which is where waves come from.
- **Two coupled LC circuits.** Two identical resonant circuits sharing a capacitor obey these
  matrices with the module-05 dictionary applied twice. Energy sloshes between the circuits at
  a rate set by the splitting, and the design of band-pass filters is the art of choosing it.
- **Molecules.** Carbon dioxide is a mass between two others, and its symmetric stretch — both
  oxygens moving out together — is a genuine normal mode with its own frequency, distinct from
  the antisymmetric stretch. Which modes absorb infrared light and which do not is the reason
  the molecule matters to the climate.
- **Two-level systems.** Module `52-quantum-optics` describes an atom trading a quantum of
  excitation with a light field at a rate set by the splitting between two coupled states. The
  arithmetic is this module's arithmetic, and the exchange has the same name in reverse: a
  splitting measured in the frequency domain, a trading period measured in time.

:::{admonition} Normal mode
:class: definition
A **normal mode** of a coupled system is a motion in which every part oscillates at the same
single frequency, keeping a fixed pattern of relative amplitudes — so that no energy is
exchanged between the parts, for ever. A system of $N$ coupled oscillators has $N$ of them, and
because the equations are linear, every possible motion of the system is a sum of its normal
modes. The **normal coordinates** are the combinations of displacements that isolate each one,
turning $N$ coupled equations into $N$ independent ones.
:::

(06-coupled-quiz)=
## Check your understanding

```{include} ../_generated/quiz-06-coupled.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](06-coupled-problems.md).

(06-coupled-explain)=
## Explain it in your own words

Answer in a few sentences each. No number will save you.

1. Explain to someone who has not done any of this why the first pendulum stops, given that
   there is no friction in the model at all. Where is its energy at that moment, and how do you
   know it is coming back?
2. Why does the symmetric mode oscillate at exactly the frequency of a single uncoupled
   pendulum? Answer without algebra — describe what the coupling spring is doing.
3. The exchange of energy between two pendulums and the beat you hear between two slightly
   mistuned guitar strings are the same phenomenon. Say in what sense, and say what plays the
   role of "the two strings" in the pendulum case.
4. What would you have to measure to decide whether a given pair is weakly or strongly coupled,
   and why is "the coupling spring feels stiff" not an answer?

(06-coupled-advanced)=
## Advanced: weak coupling, strong coupling, and the crossing that isn't

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section.
:::

**Two regimes, one number.** The splitting $\Delta\omega$ is the only thing that distinguishes
coupled pairs, and comparing it with $\wnat$ sorts them into two worlds. When
$\Delta\omega \ll \wnat$ — weak coupling — the exchange is slow compared with the oscillation
itself, so a pendulum completes many clean swings while its amplitude drifts, and the
handover is essentially complete. When $\Delta\omega$ approaches $\wnat$, the two modes are so
different in frequency that "an oscillation whose amplitude is slowly changing" stops being a
useful description at all, and the transfer is partial: at $k_c = k$, 7.4% of the energy never
leaves the mass it started on.

The same distinction organises a great deal of physics under other names. In `52-quantum-optics`
an atom in a cavity is weakly coupled if it loses its excitation before it can trade it back,
and strongly coupled if the trading wins — and the trading rate is the splitting between two
states, exactly as here. The classical pendulums are not an analogy for that situation; they are
the same mathematics with heavier objects.

**Detuning, and the crossing that isn't.** Break the symmetry. Stiffen the second mass's anchor
spring alone, $k \to k(1 + \delta)$, and sweep $\delta$ through zero. Uncoupled, the two
frequencies would cross cleanly at $\delta = 0$ — one rising, one flat. Coupled, they do not.
They approach, turn away from each other, and separate again, and at no value of $\delta$ are
they ever equal.

The gap is narrowest exactly where the uncoupled frequencies would have met, and its minimum
value is set by the coupling alone: at $k_c/k = 0.1$ the closest approach is $0.38$ rad/s and
never smaller, however carefully $\delta$ is tuned. This is an **avoided crossing**, and once
you have seen one you will see it everywhere — in molecular energy levels, in the band structure
of `54-photonic-crystals`, and in a pair of optical resonators tuned through each other in
`44-resonators`. Two things that are coupled cannot be made degenerate merely by tuning them.

**Where the linear model gives out.** Huygens' clocks did not do what the pendulums above do.
His two clocks settled into *permanent* antiphase lock and stayed there, which no conservative
linear system can do: this model's motion is periodic and always returns. Real clocks are driven
by escapements and lose energy to friction, and a driven, damped, weakly nonlinear pair can
settle onto a stable synchronised state and stay on it. That belongs to the theory of coupled
self-sustained oscillators, and it is a genuinely different subject — worth knowing that the
famous observation at the top of this page is not, strictly, the phenomenon derived below.
