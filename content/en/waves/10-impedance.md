---
title: "Impedance: what decides how much comes back"
short_title: 10 · Impedance
module: 10-impedance
objectives:
  - id: OBJ-10-1
    text: Compute the impedance Z = sqrt(T mu) = mu v = T / v and interpret it as the transverse force per unit transverse velocity the medium presents to whatever drives it.
  - id: OBJ-10-2
    text: Apply the junction conditions — continuity of displacement and of transverse force — to derive r = (Z1 - Z2)/(Z1 + Z2) and t = 2 Z1/(Z1 + Z2) for displacement amplitudes, and check them against 1 + r = t.
  - id: OBJ-10-3
    text: Predict pulse reflection at a fixed end (Z2 -> infinity, r = -1) and a free end (Z2 -> 0, r = +1) as limits of the junction formulas, including the sign of the reflected pulse.
  - id: OBJ-10-4
    text: Verify energy conservation R + T = 1 with R = r^2 and T = (Z2/Z1) t^2, and explain why t can exceed 1 while no energy is gained.
  - id: OBJ-10-5
    text: State the impedance-matching condition r = 0, give physical examples such as ultrasound gel and a terminated cable, and explain qualitatively why matching two given media needs an intermediate layer.
---

# Impedance: what decides how much comes back

(10-impedance-puzzle)=
## The puzzle: why the gel

Before an ultrasound scan, the technician squirts cold gel on your skin and presses the probe
into it. Without the gel the image is not grainy or dim — it is *black*. The instrument works
perfectly; sound simply refuses to enter you. A layer of air a fraction of a millimetre thick
between the probe and your skin sends essentially all of it straight back.

Two more everyday facts, from the other end of the apparatus scale. Tie a rope to a wall, send a
pulse down it, and the pulse comes back **upside down**. Tie the same rope to a light thread
instead, send the same pulse, and it comes back **right side up**. Nobody changed the rope.

:::{important} The question
At a change of medium, what decides how much of a wave bounces, how much crosses, and which way
up the part that bounces comes back?
:::

(10-impedance-predict)=
## Predict before you calculate

Commit to an answer for each before running anything.

1. A pulse travels along a rope tied to a wall. Upright or inverted on the way back?
2. A heavy rope is knotted to a light string. A pulse arrives from the heavy side. Is the
   reflected pulse upright or inverted — and is the transmitted pulse taller or shorter than the
   one that made it?
3. Can a transmitted pulse be taller than the incident pulse? If it can, where did the extra
   energy come from?
4. Is there a junction between two *different* strings that produces no echo at all?

:::{note} Why we ask first
Question 2 is this module's misconception. "Reflection flips a pulse" is a rule almost everyone
carries out of a first course, and it is half a rule: the wall in question 1 does invert, and
the light string in question 2 does not. Nothing changes in the middle of the story except which
side is harder.
:::

(10-impedance-explore)=
## Explore the model

Three animations, all computed from the same `wavelab.waves` functions the laboratory calls.

:::{figure} ../media/wave-end-reflection.mp4
:width: 100%

The same pulse at a wall and at a free end — one string each, differing in a single word passed
to the solver. Against the wall the returning pulse is inverted and the end never moves. At the
free end, a ring sliding on a frictionless rod, the pulse returns upright and the end itself
swings to twice the incident amplitude while the incoming and outgoing pulses sit on top of each
other. The dotted guides mark $\pm A$ and $2A$. Measured off these runs, the two returns are
$-1.0000\,A$ and $+1.0000\,A$, and neither end takes any energy.
:::

:::{figure} ../media/wave-junction-pair.mp4
:width: 100%

One junction, approached from each side. The densities differ fourfold, so the impedances differ
twofold and the coefficients are exactly thirds. From the heavy side (top, shaded): the echo is
upright at $+\tfrac13$ and the transmitted pulse is *taller* than the incident one, $\tfrac43$,
and twice as wide because it travels twice as fast. From the light side (bottom): the echo is
inverted at $-\tfrac13$ and the transmitted pulse is shorter and narrower. Both panels are in
step, so the two outcomes can be compared rather than remembered.
:::

:::{figure} ../media/wave-quarter-wave-match.mp4
:width: 100%

A six-cycle packet at a 3:1 impedance step, bare (top) and with a quarter-wave matching section
(bottom, the green sliver). The bare step sends a quarter of the energy back, $R = 0.2504$
against the formula's $0.2500$. The sliver — one piece of string of impedance $\sqrt{Z_1Z_3}$,
57.7 mm long — drops that to $R = 0.0077$, an echo thirty-two times weaker in energy. Nothing
absorbed it. This is the advanced section, and the direct ancestor of the coating on a camera
lens.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** two semi-infinite ideal strings, densities $\mu_1$ and $\mu_2$, under one common tension $T$, joined at $x = 0$ — numerically a single grid whose density jumps at a point.
- **Dynamics:** the wave equation $\mu\,y_{tt} = T\,y_{xx}$ on each side, and at the junction the two matching conditions: $y$ continuous (the string is unbroken) and $-T\,y_x$ continuous (the joint is massless, so no net transverse force may act on it).
- **Boundary:** the junction itself. The outer ends — fixed or free — are kept far enough away that nothing measured here has heard from them.
- **Ensemble:** deterministic; detector noise, where added, is Gaussian, independent and seeded.
- **Ignored:** junction mass, stiffness and damping; loss of any kind; oblique incidence, which has no meaning in one dimension.
- **Valid when:** slopes are small, $|y_x| \ll 1$, on *both* sides — the transmitted wave has its own slope — and the junction is a point. A density that changes gradually over a length comparable with the wavelength is a different problem, and the problem set makes it one.
- **Failure modes:** reading $t > 1$ as a gain of energy; applying the amplitude coefficients to power; forgetting the flux factor $Z_2/Z_1$; a junction placed on too coarse a grid, where the measured $r$ is wrong in the third decimal for reasons that have nothing to do with impedance.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 10 — impedance](/lite/lab/index.html?path=en/labs/10-impedance.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/10-impedance.ipynb`.
:::

Run the laboratory now, then come back. Four things are worth doing before you read on:

- Plot the transverse force against the transverse velocity on a travelling pulse, and read the
  impedance off the slope.
- Measure $r$ and $t$ across a 625-fold range of density and find where the sign changes.
- Weigh the energy on the two sides of a junction and watch $R + T$ come out at 1.
- Measure a reflection coefficient through 5% noise, twice, with two estimators that are both
  honest arithmetic. One of them is off by a fifth of the answer.

(10-impedance-derive)=
## Derive the result

### What the medium feels like to push

Take hold of the end of a semi-infinite string and wave it. Everything you launch travels away
and never comes back, so the string at your hand is a pure right-mover and obeys module 08's
$y_t = -v\,y_x$. The transverse force you must supply is the transverse component of the
tension, $-T\,y_x$, so

$$
F = -T\,\frac{\partial y}{\partial x}
  = \frac{T}{v}\,\frac{\partial y}{\partial t}
  = Z\,\frac{\partial y}{\partial t},
\qquad
Z \equiv \frac{T}{v} = \sqrt{T\mu} = \mu v .
$$

:::{admonition} Impedance of a string
:class: definition
$$
\boxed{\;Z = \sqrt{T\mu} = \mu v = \frac{T}{v}\;}
$$

in kilograms per second — force per unit transverse velocity, N/(m/s).

Force proportional to velocity and *in phase* with it: the string resists like a dashpot, not
like a spring and not like a mass. That is the whole content of the word. You do work at every
instant and none of it is stored where you can get it back, because what you paid for is
travelling away. An ideal infinite string is a perfect absorber, and an oscillator with one tied
to it is a damped oscillator — module 02's $\gamma$, supplied by geometry rather than by friction.

$Z$ and $v$ are separate properties: $T$ and $\mu$ are two knobs, and $v = \sqrt{T/\mu}$ and
$Z = \sqrt{T\mu}$ can be set independently. On a string they are not independent *in practice*,
because a junction between two densities carries one tension; there
$Z_2/Z_1 = \sqrt{\mu_2/\mu_1} = v_1/v_2$, and the heavier side is both the slower and the harder
one.
:::

The laboratory reads $Z$ straight off a simulated pulse: plot $-T\,y_x$ against $y_t$ at every
point and the cloud is a straight line of slope $+0.199991$ kg/s against
$\sqrt{T\mu} = 0.2$ kg/s. A left-moving pulse gives $-0.199991$: the sign is the direction the
energy goes, not a different medium.

### The junction: two conditions and nothing else

Now join two strings at $x = 0$ and send a wave in from the left. Write the three waves in the
course convention,

$$
y_{\text{inc}} = \Real\!\left[A\,e^{\ii(k_1x - \omega t)}\right],
\qquad
y_{\text{ref}} = \Real\!\left[rA\,e^{\ii(-k_1x - \omega t)}\right],
\qquad
y_{\text{tr}} = \Real\!\left[tA\,e^{\ii(k_2x - \omega t)}\right],
$$

with the same $\omega$ on both sides — the junction is driven at the frequency it is fed, and
nothing about it changes in time — and $k_{1,2} = \omega/v_{1,2}$ adjusting instead. The
wavelength changes at the junction; the frequency cannot.

Two statements about the joint finish the problem.

1. **The string is unbroken.** $y$ is continuous at $x = 0$, so $1 + r = t$.
2. **The joint is massless.** A point with no mass cannot survive a net force, so the transverse
   force $-T\,y_x$ is continuous too. With $T$ common to both sides that gives
   $k_1(1 - r) = k_2 t$, and since $k = \omega/v$ and $Z = T/v$, it is
   $Z_1(1 - r) = Z_2 t$.

:::{admonition} Reflection and transmission of displacement
:class: theorem
Solving those two lines together:

$$
\boxed{\;r = \frac{Z_1 - Z_2}{Z_1 + Z_2},
\qquad
t = \frac{2Z_1}{Z_1 + Z_2}\;}
$$

Both are ratios of *displacement* amplitudes, and both are real: at a lossless junction a wave
can only come back in step or exactly out of step, never anywhere in between. The identity
$1 + r = t$ was the first condition and survives as the check to run on any numbers claiming to
be $r$ and $t$.

The sign of $r$ is the sign of $Z_1 - Z_2$, and it is the whole of prediction 2:

- $Z_2 > Z_1$ — a **harder** far side — gives $r < 0$: the echo is inverted.
- $Z_2 < Z_1$ — a **softer** far side — gives $r > 0$: the echo is upright.
- $Z_2 = Z_1$ gives $r = 0$ and $t = 1$: no echo at all.

And $t$ is never negative and never zero: whatever the junction, the far side moves the same way
the incident wave pushed it. Only the echo can flip.
:::

### The wall and the free end were never special

Let $Z_2$ grow without bound — a far side too heavy to move:

$$
r \to -1, \qquad t \to 0 .
$$

That is a fixed end. The displacement there is $A(1 + r) = 0$ at all times, which is what
"fixed" means, and the reflected pulse is the incident one turned upside down.

Let $Z_2 \to 0$ instead — a far side too light to resist:

$$
r \to +1, \qquad t \to 2 .
$$

That is a free end. The displacement there is $2A$: incident and reflected pulses arrive on top
of each other and add, which is why the ring on the rod overshoots. The slope there is zero,
which is what "free" means.

:::{admonition} One formula, two boundary conditions
:class: theorem
A wall and a free end are not two rules to memorise. They are the two limits of
$r = (Z_1 - Z_2)/(Z_1 + Z_2)$, at $Z_2 \to \infty$ and $Z_2 \to 0$. Everything between them is a
junction, and the sign of the echo changes exactly once, at $Z_2 = Z_1$.

This also explains the inversion, which otherwise has to be taken on trust. At a wall the string
pulls up on the support; the support pulls down on the string, with an equal and opposite force
it has no trouble supplying. That downward kick *is* the inverted pulse leaving.
:::

### The energy, and the factor that settles the paradox

A transmitted amplitude larger than the incident one looks like something for nothing. It is
not, and the bookkeeping says exactly why.

Module 09 found that a sinusoidal travelling wave carries mean power
$\langle P\rangle = \tfrac12 Z\,\omega^2|A|^2$. All three waves here share $\omega$, so dividing
each power by the incident one leaves the squared amplitude ratio and, for the transmitted wave,
the impedance it travels on:

$$
R = r^2,
\qquad
T = \frac{Z_2}{Z_1}\,t^2 .
$$

:::{admonition} The junction conserves energy — and was never asked to
:class: theorem
$$
\boxed{\;R + T = 1\;}
$$

by algebra, not by assumption. Substituting,

$$
R + T
= \frac{(Z_1 - Z_2)^2}{(Z_1 + Z_2)^2} + \frac{Z_2}{Z_1}\cdot\frac{4Z_1^2}{(Z_1+Z_2)^2}
= \frac{(Z_1 - Z_2)^2 + 4Z_1Z_2}{(Z_1 + Z_2)^2}
= 1 .
$$

Nothing was imposed. Energy conservation at the junction was already inside the two matching
conditions — continuity of displacement and of force — which is the strongest argument that
those were the right two conditions.
:::

Now the paradox. Onto a string a hundred times lighter, $Z_2/Z_1 = 1/10$, so

$$
r = +0.818, \qquad t = 1.818, \qquad R = 0.669, \qquad T = 0.331 .
$$

The far side swings almost twice as far as the incident wave did *and* carries only a third of
its power. There is no contradiction: the light string is cheap to move. Power is
$\tfrac12 Z(\omega|A|)^2$, and the amplitude went up by 1.8 while the $Z$ in front of it went
down by 10. The flux factor $Z_2/Z_1$ is the entire difference between how far something swings
and what it cost to make it swing, and confusing the two is this module's standing trap.

:::{note} Amplitude and energy answer different questions
$r$ and $t$ answer "how far does the string move?". $R$ and $T$ answer "where did the joules
go?". They are related by a factor that is *not* 1 unless the two media are identical. Every
later part of this course inherits the same pair — the Fresnel coefficients $r, t$ for field
amplitudes and the reflectance and transmittance $R, T$ for irradiance, with the same kind of
factor in between.
:::

### Matching: the case where nothing comes back

$r = 0$ requires $Z_1 = Z_2$, and that is the whole criterion. It says something slightly
surprising: two media may differ in every other respect and still be invisible to each other, as
long as $\sqrt{T\mu}$ — or its analogue — agrees.

On a string this is a blunt instrument, because tension is one number from end to end: equal
impedance means equal density, and the "matched junction" is a string with no junction in it.
The idea earns its keep where the two constants are free of each other. Ultrasound gel has
roughly the acoustic impedance of tissue and fills the place where air would otherwise sit;
a 50 Ω cable terminated in a 50 Ω resistor absorbs its signal instead of echoing it back.

Matching two *given* media is a harder problem: you cannot choose $Z_2$ when both media are
given. You insert a third. A section of impedance $\sqrt{Z_1Z_3}$ and a quarter-wavelength long
sends back two reflections that cancel, and the advanced section builds one. That is the
anti-reflection coating on every camera lens, and module 24 does it properly.

(10-impedance-verify)=
## Verify computationally

Each check below is also a test in the project's suite, so these claims cannot silently rot.

**1. The split is the one the impedances predict.** A pulse is fired at a jump in density and
the two pieces it becomes are measured off the final frame. The solver integrates
displacements; it has no notion of an amplitude ratio.

| $\mu_2/\mu_1$ | $Z_2/Z_1$ | $r$ formula | $r$ measured | $t$ formula | $t$ measured |
|---|---|---|---|---|---|
| 0.04 | 0.2 | $+0.6667$ | $+0.6669$ | 1.6667 | 1.6660 |
| 0.25 | 0.5 | $+0.3333$ | $+0.3336$ | 1.3333 | 1.3330 |
| 1.00 | 1.0 | $0.0000$ | $+0.0002$ | 1.0000 | 1.0002 |
| 4.00 | 2.0 | $-0.3333$ | $-0.3336$ | 0.6667 | 0.6666 |
| 25.00 | 5.0 | $-0.6667$ | $-0.6668$ | 0.3333 | 0.3332 |

Worst disagreement over the laboratory's full eleven-point sweep: $6.9\times10^{-4}$. **The sign
column is the falsifier for "reflection always inverts"** — it changes at $\mu_2 = \mu_1$ and
nowhere else.

**2. A wall and a free end land on the limits.** The same pulse under `boundary="fixed"` returns
at $-1.0000\,A$; under `boundary="free"` it returns at $+1.0000\,A$ and the end itself reaches
$+1.999\,A$. Both runs keep their energy to one part in $10^9$. The solver was told about ghost
points and clamped displacements, never about impedance.

**3. The books balance, and they balance the same way from either side.**

| $\mu_2/\mu_1$ | $R$ formula | $R$ weighed | $T$ formula | $T$ weighed | $R + T$ |
|---|---|---|---|---|---|
| 0.04 | 0.444444 | 0.444778 | 0.555556 | 0.555222 | 0.9999999 |
| 0.25 | 0.111111 | 0.111320 | 0.888889 | 0.888679 | 0.9999990 |
| 4.00 | 0.111111 | 0.111320 | 0.888889 | 0.888679 | 0.9999991 |
| 25.00 | 0.444444 | 0.444778 | 0.555556 | 0.555222 | 0.9999999 |

Two things are visible at once. Nothing is lost — no mechanism for loss was put into the model,
so a leak would have been the scheme's. And the rows for $1/4$ and $4$ are *identical*: the same
fraction of the energy comes back whichever side the pulse arrives from, though the amplitudes
in the two directions are completely different ($+0.33$ against $-0.33$, $1.33$ against $0.67$).
Energy cannot tell which way the wave was going.

:::{admonition} $R + T = 1$ measured, not imposed
:class: numerical-observation
The identity holds to $10^{-15}$ as algebra and to $10^{-6}$ as a measurement on weighed
pulses. The gap between those two numbers is the grid, and it closes as the grid refines —
see check 4. What does *not* appear at any resolution is a systematic loss, which is the
useful negative result: the discretisation of a junction can be inaccurate, but it is not
quietly dissipative.
:::

**4. The measured $r$ converges on the formula at second order.** A junction is a step the grid
can only place to within $\Delta x$, so agreement is a question about resolution. With 10, 20,
40 and 80 points across the incident pulse, the measured reflected amplitude misses $-1/3$ by
$8.9\times10^{-4}$, $2.2\times10^{-4}$, $5.6\times10^{-5}$ and $1.4\times10^{-5}$ — a factor of
four per halving of the spacing, the same second order the solver obeys everywhere else. This is
the gate the module's animations sit behind: a junction rendered on too coarse a grid returns an
amplitude that is wrong for reasons that have nothing to do with physics.

**5. $t > 1$, measured, with the energy accounted for.** At $\mu_2/\mu_1 = 0.01$ the transmitted
pulse stands $1.818$ times as tall as the incident one, and the weighed energy fractions are
$R = 0.669$ and $T = 0.331$. Taller and weaker, in the same run.

**6. A reflection coefficient with an error bar.** The laboratory corrupts the final frame with
Gaussian noise of 5% of the incident amplitude and estimates $r$ twice from the same data: by
projection onto the expected pulse shape, and by picking the largest excursion in the window.
At $\mu_2/\mu_1 = 4$, where $r = -0.3333$, the projection gives $-0.3355 \pm 0.0009$ over 64
frames and the peak-pick gives $-0.4311 \pm 0.0029$ — off by 29%, and no number of frames
repairs it.

:::{admonition} Why one honest estimator is wrong
:class: numerical-observation
The projection is *linear* in the data: noise enters it with a plus sign as often as a minus and
averages away, leaving a scatter of about 0.011 per frame, close to the
$\sigma/\sqrt{\sum g_i^2}$ the noise level predicts.

Picking the largest excursion is not linear. The maximum of many noisy samples is not an
estimate of the signal at any of them; it is a search for the noise's best excursion, and it
finds one. The bias is *away from zero*, it does not shrink with more frames, and it grows as
the pulse gets smaller relative to the noise — so the flattest, most interesting junctions are
where it lies worst. Module 09 met the same trap in a wattmeter that squared a noisy signal.
It will be waiting again at every photodetector in the optics half of this course.
:::

**7. And what a real rope can be asked.** Knot a length of thick rope to a thin one, stretch the
pair, and film a pulse crossing the knot from each side with a phone. The *signs* need no
calibration at all — upright from the thin side, inverted from the thick — and that alone
falsifies the misconception. Amplitudes need a ruler in frame and a fixed camera position;
frame-by-frame, a heavy-to-light knot with a 4:1 mass ratio should give you $r \approx +1/3$ and
$t \approx 4/3$ to perhaps 10%, with the pulse width changing visibly as it crosses. The problem
set sets this up as a measurement with an uncertainty rather than a demonstration.

(10-impedance-transfer)=
## Transfer the idea

:::{admonition} One calculation, many costumes
:class: important
The two lines that produced $r$ and $t$ — *the field is continuous, and so is the thing that
carries force across the boundary* — are the template for every boundary in this course. The
algebra below is the same algebra, and it is worth recognising it now rather than deriving it
four more times.

- **Light at a surface (module 18).** For normal incidence the Fresnel coefficients are
  $r = (n_1 - n_2)/(n_1 + n_2)$ and $t = 2n_1/(n_1 + n_2)$ — this module's formulas letter for
  letter, with the refractive index sitting in the slot where $Z$ sits here. Light reflecting
  off glass comes back inverted for the same reason a pulse off a wall does: in the slot that
  decides the sign, glass is the harder side. (The index is *not* light's impedance, which is
  $Z = Z_0/n$ and falls as $n$ rises. The advanced section says why the formula still reads
  this way.)
- **Anti-reflection coatings (module 24).** A quarter-wave layer of index $\sqrt{n_1n_3}$ is the
  advanced section of this page with $Z \to n$.
- **Cavities and interferometers (module 26).** Two junctions facing each other, with the wave
  bouncing between them, is a Fabry–Pérot etalon; everything about it is these coefficients
  applied repeatedly.
- **Cables, ultrasound, loudspeakers.** A transmission line has $Z = \sqrt{L'/C'}$, a fluid has
  $\rho c$, and an unterminated cable, a missing gel layer and a badly matched horn are one
  engineering failure with three names.

One calculation, many costumes. This is among the largest unifications the course offers, and
it is available here, on a rope, before any of the fields arrive.
:::

- **Standing waves.** `11-standing-waves` puts a junction at *each* end. With $r = \mp 1$ there,
  a wave cannot escape and can only interfere with itself — which is what a mode is. The
  quantisation of allowed frequencies comes from these two reflection coefficients and nothing
  else.
- **Light in matter.** `16-light-in-matter` keeps the frequency fixed across a boundary and lets
  $k$ adjust, exactly as here. That is why the colour of light does not change when it enters
  glass, though its wavelength does.
- **The tsunami.** A long ocean wave entering shallow water meets a rising impedance
  continuously rather than at a point. Almost nothing reflects — which is the problem set's
  smeared junction — and the amplitude climbs as the depth falls. The wave that arrives at the
  coast is the one that was never turned back.
- **Impedance matching as engineering.** Between an amplifier and a speaker, an antenna and a
  feedline, an optical fibre and a detector (module 47), the same transformer idea recurs: you
  cannot change either end, so you put something in between.

(10-impedance-quiz)=
## Check your understanding

```{include} ../_generated/quiz-10-impedance.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](10-impedance-problems.md).

(10-impedance-explain)=
## Explain it in your own words

Answer in a few sentences each. No number will save you.

1. Explain to someone who is certain that reflection always inverts a pulse why a rope tied to a
   thread returns it upright, without writing down a formula. Then say what a wall and a thread
   have in common.
2. A transmitted pulse is twice as tall as the incident one. Say where the energy is, and why
   the string on the far side being "cheap to move" is the whole answer.
3. Ultrasound gel is not a lubricant and not a conductor of sound in any special sense. Say in
   one sentence what it is for.
4. Two strings of different densities are joined, and someone claims they can make the junction
   echo-free by pulling harder on one side. Explain what is wrong with that, using the fact that
   a string at rest has one tension.

(10-impedance-advanced)=
## Advanced: the flux derivation in full, the analogue table, and a section that erases an echo

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section.
:::

**$R$ and $T$ from the flux directly.** The derivation above divided mean powers, which needed
module 09's sinusoidal result. The same answer comes straight from the instantaneous flux
$P = -T\,y_x\,y_t$, and it is worth seeing once because it never assumes a sinusoid.

On the left of the junction the field is incident plus reflected, so the flux there has three
terms: one from each wave and one cross term. For pulses that do not overlap in time the cross
term integrates to nothing, and the energies are $\int P\,\mathrm{d}t$ over each pulse:

$$
E_{\text{inc}} = Z_1\!\int (y_t^{\text{inc}})^2\,\mathrm{d}t,
\qquad
E_{\text{ref}} = Z_1 r^2\!\int (y_t^{\text{inc}})^2\,\mathrm{d}t,
\qquad
E_{\text{tr}} = Z_2 t^2\!\int (y_t^{\text{inc}})^2\,\mathrm{d}t,
$$

using $P = Z\,y_t^2$ for a travelling wave in each medium — module 09's $P = vu$ written with
the impedance. Divide by $E_{\text{inc}}$ and $R = r^2$, $T = (Z_2/Z_1)t^2$ drop out with no
mention of frequency. That is why the laboratory can weigh *pulses* and still land on formulas
derived for sinusoids.

**The analogue table.** Impedance is not a string concept that others borrow. It is what any
medium answers when asked for force per unit velocity, and only the names change:

| System | Displacement-like | Force-like | Impedance |
|---|---|---|---|
| string | transverse displacement $y$ | transverse force $-T y_x$ | $Z = \sqrt{T\mu} = \mu v$ |
| sound in a fluid | particle displacement | pressure $p$ | $Z = \rho c$ |
| transmission line | charge | voltage $V$ | $Z = \sqrt{L'/C'}$ |
| light (normal incidence) | electric field $E$ | magnetic field $H$ | $Z = \sqrt{\mu_0/\varepsilon} = Z_0/n$ |

The last row is module 14's, and it carries a subtlety worth meeting once. Light's impedance
*falls* as the index rises, $Z = Z_0/n$, and yet the Fresnel coefficient at normal incidence
reads $r = (n_1 - n_2)/(n_1 + n_2)$ — the index in the slot where this module puts $Z$. Both
statements are true. The amplitude quoted for light is the electric field, which is the
force-like member of its pair, where a string's $y$ is the motion-like member of ours;
swapping which member you track inverts the mismatch ratio, $Z 	o 1/Z$, and the two
inversions cancel into one identical formula. Module 18 boxes the two side by side.

**A junction with no echo, on a string.** Insert a section of impedance $Z_2 = \sqrt{Z_1Z_3}$
and length $\lambda_2/4$ between media 1 and 3, where $\lambda_2$ is the wavelength *in the
section*. Its front face reflects, its back face reflects, and the second reflection makes a
round trip of $2 \times \lambda_2/4 = \lambda_2/2$ — half a wavelength, so it returns exactly out
of step with the first. Equal sizes, opposite signs, nothing comes back.

The animation above does this for a 9:1 density step: $R$ falls from $0.2504$ to $0.0077$ with
a 57.7 mm sliver of string. The cancellation is exact only at the design frequency, and the
residual there is the packet's own bandwidth, not a numerical error — which is exactly why a
lens coating is optimised for the middle of the visible spectrum and leaves the purple fringe
that tells you it is there. The problem set asks for $R(\omega)$.

**And the kick the wall takes.** A pulse reflecting off a wall reverses the transverse momentum
it carries, $\int \mu\,y_t\,\mathrm{d}x$, so the wall receives twice that in impulse. This is
honest and unremarkable. The *longitudinal* question — whether the wall is also pushed along the
string's direction — is the one module 09 flagged as open, and this module does not reopen it:
the answer is second order in the slope, and everything computed here is first order in $y_x^2$
and agrees across every version of the model.
