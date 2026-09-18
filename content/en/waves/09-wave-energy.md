---
title: "Wave energy: what actually travels"
short_title: 09 · Wave energy
module: 09-wave-energy
objectives:
  - id: OBJ-09-1
    text: Distinguish and compute three velocities — the transverse medium velocity dy/dt, the pattern velocity v, and the energy transport velocity P/u — and say which of them the medium fixes and which the source chooses.
  - id: OBJ-09-2
    text: Compute u_K = (1/2) mu (dy/dt)^2 and u_P = (1/2) T (dy/dx)^2 and locate where along a wave the energy sits.
  - id: OBJ-09-3
    text: Derive the energy flux P = -T (dy/dx)(dy/dt) and verify the local conservation law du/dt + dP/dx = 0.
  - id: OBJ-09-4
    text: Show that a travelling wave has u_K = u_P at every point and instant, that its energy travels at exactly v, and that a sinusoidal wave carries mean power (1/2) mu v omega^2 A^2.
  - id: OBJ-09-5
    text: Contrast travelling and standing waves as energy transporters — the standing wave's time-averaged flux is zero everywhere.
---

# Wave energy: what actually travels

(09-wave-energy-puzzle)=
## The puzzle: the wave arrives, and the water was always here

A storm in the Southern Ocean puts energy into the sea. Ten days later, swell arrives on a
Californian pier and breaks a plank. Nothing crossed the Pacific: the water that hit the pier
had been floating off California the whole time, and the water that the storm pushed on is
still off Antarctica. Module 08 established that much on a string — a speck of dust rises,
falls, and is exactly where it started once the pulse has gone.

Yet the plank broke. Whatever made the storm's energy and whatever broke the plank are the
same joules, and in between they were *somewhere*, in a medium that stayed put.

:::{important} The question
If no water makes the trip, where does the energy live while it crosses the ocean, and how fast
does it move? And is that the same speed as the wave?
:::

(09-wave-energy-predict)=
## Predict before you calculate

Commit to an answer for each before running anything.

1. A sinusoidal wave travels along a string. Where is the energy per unit length largest — at
   the crests, at the zero crossings, or is it the same everywhere?
2. Can a piece of string move faster than the wave travelling along it?
3. You double the amplitude of a wave and change nothing else. The power it delivers rises by
   what factor?
4. A travelling wave and a standing wave have the same amplitude and the same frequency. Which
   one delivers more energy past a point in the middle of the string?

:::{note} Why we ask first
Question 1 is this module's misconception, and the wrong answer is the one everybody gives.
The crest is the most visible part of a wave, the part that breaks over the pier, the part a
photograph is *about*. It is also, at that instant, the emptiest place on the string.
:::

(09-wave-energy-explore)=
## Explore the model

Three animations, all computed from the same `wavelab.waves` functions the laboratory calls.

:::{figure} ../media/wave-energy-paint.mp4
:width: 100%

A sinusoidal wave travelling right, over its own energy density. The orange marker rides a
crest; the green marker rides the zero crossing a quarter wavelength behind it. The crest
marker sits in a *trough* of the energy for the whole loop — never above $2.5\times10^{-4}$ of
what the green marker stands on — and the energy humps come twice as often as the crests,
because the density goes as the square of a sine. Both travel at the wave speed, so the picture
below the string is as rigid as the picture above it.
:::

:::{figure} ../media/wave-energy-densities.mp4
:width: 100%

A single Gaussian pulse, with its energy beneath. Two things are happening at once. The thick
pale curve is $u_P$ and the thin dark one $u_K$, and they lie on top of each other everywhere,
at every frame, to $2\times10^{-4}$ of the peak. And one hump of string carries *two* humps of
energy: both densities go as the square of the slope, and a pulse is flat on top. The dotted
curve is the flux divided by $v$, which lands on the grey total to $2\times10^{-8}$ — the
energy moves at exactly the speed the shape does.
:::

:::{figure} ../media/wave-energy-transport.mp4
:width: 100%

A travelling train and a standing mode of the same amplitude and frequency, each with a gate
where the power crossing is read. The travelling wave's flux (blue) never goes below zero:
energy crosses the gate twice a cycle and keeps going. The standing wave's flux (orange) swings
symmetrically about zero and nets $1.4\times10^{-10}$ of what it moved. Its peak is a quarter of
the travelling wave's, not a thousandth — a standing wave pushes comparable energy about and
simply puts it all back.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** module 08's ideal string — transverse displacement $y(x,t)$, tension $T$, linear mass density $\mu$ — now carrying three derived fields: the kinetic and potential energy densities $u_K(x,t)$, $u_P(x,t)$, and the energy flux $P(x,t)$.
- **Dynamics:** $\mu\,y_{tt} = T\,y_{xx}$ as before. The energy quantities are *diagnostics*: they are computed from the solution and never fed back into it, so every agreement between them and the solver is evidence rather than construction.
- **Boundary:** fixed ends. No energy crosses one, because $y_t = 0$ there and a force that does no work transports no power.
- **Ensemble:** deterministic; detector noise, where added, is Gaussian, independent and seeded.
- **Ignored:** dissipation, longitudinal motion, and the momentum a transverse wave may or may not carry — the last is a genuinely open question, flagged in the advanced section rather than waved away.
- **Valid when:** slopes are small, $|y_x| \ll 1$. The potential density needs this one order deeper than the equation of motion did: the equation dropped terms of order $y_x^2$, and $u_P$ keeps them and drops $y_x^4$.
- **Failure modes:** the densities read as exact for a steep wave; a lossy string's energy assumed conserved because the ideal one's is; the "energy velocity" trusted once the medium becomes dispersive, where module 13 finds it is no longer $\omega/k$.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 09 — wave energy](/lite/lab/index.html?path=en/labs/09-wave-energy.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/09-wave-energy.ipynb`.
:::

Run the laboratory now, then come back. Four things are worth doing before you read on:

- Read the three velocities off one pulse, and notice that two of them are the same number.
- Plot the energy density under a sinusoidal wave and find the offset between the two curves.
- Meter the power at a point, and check that what the meter counted is what ended up beyond it.
- Measure the mean power twice, through the same noise, with two estimators that are both
  correct algebra. One of them will lie to you.

(09-wave-energy-derive)=
## Derive the result

### The two densities

A short piece of string between $x$ and $x + \mathrm{d}x$ has mass $\mu\,\mathrm{d}x$ and moves
sideways at $y_t$. Its kinetic energy is $\tfrac12(\mu\,\mathrm{d}x)\,y_t^2$, and per unit
length that is

$$
u_K = \tfrac12\,\mu\left(\frac{\partial y}{\partial t}\right)^2 .
$$

The potential energy takes one more step. A string stores energy by being *longer* than it was:
tilted to a slope $y_x$, a piece of rest length $\mathrm{d}x$ becomes
$\sqrt{1 + y_x^2}\;\mathrm{d}x$, and the work done against the constant tension $T$ is $T$ times
that extra length. Expanding the square root,

$$
T\left(\sqrt{1 + y_x^2} - 1\right)\mathrm{d}x
= \tfrac12\,T\,y_x^2\,\mathrm{d}x + O(y_x^4)\,\mathrm{d}x ,
$$

so

$$
u_P = \tfrac12\,T\left(\frac{\partial y}{\partial x}\right)^2 .
$$

:::{admonition} Energy densities on a string
:class: definition
$$
u_K = \tfrac12\,\mu\,y_t^2,
\qquad
u_P = \tfrac12\,T\,y_x^2,
\qquad
u = u_K + u_P ,
$$
each in joules per metre. The total energy on a stretch is the integral of $u$ over it.

Both are approximations of the same order as the wave equation, and $u_P$ spends the
small-slope assumption once more than the equation of motion did. The equation of motion
discarded terms of order $y_x^2$ relative to what it kept; $u_P$ keeps those and discards
$y_x^4$. A wave steep enough to need the next term is a wave the model no longer describes at
all.
:::

Read what $u_P$ says about *where* a wave's energy is. It is not displacement that stores
energy — pick up a straight stretch of string, hold it a metre higher, and you have stretched
nothing. It is slope. And $u_K$ needs motion. On a travelling sine
$y = A\sin(kx - \omega t)$ the crests have neither: there the string is momentarily flat and
momentarily at rest, both densities vanishing together. **The crest is the emptiest place on
the string**, and the energy piles up at the zero crossings, where the string is steepest and
moving fastest. That is prediction 1, and the laboratory measures the crest holding
$4\times10^{-5}$ of what the zero crossing holds.

### The flux: force times velocity, as always

Cut the string at $x$ and ask what the left piece does to the right one. It pulls along the
string's own direction with tension $T$, whose transverse component is $-T\,y_x$ for small
slopes. That force acts on a point moving at $y_t$, and power is force times velocity:

$$
\boxed{\;P = -T\,\frac{\partial y}{\partial x}\,\frac{\partial y}{\partial t}\;}
$$

in watts, counted positive when energy flows toward $+x$. There is no new physics in it — it is
the same $F v$ that module 01 used on a single mass, applied at a cut rather than to a body.

The sign is the direction, and both signs occur. For a right-mover, module 08's
$y_t = -v\,y_x$ gives $P = T v\,y_x^2 \ge 0$ everywhere: energy flows the way the wave goes,
whether the string at that point happens to be rising or falling. A left-mover has
$y_t = +v\,y_x$ and $P \le 0$ everywhere. A negative $P$ is not a paradox; it is a wave going
the other way.

### The first local conservation law

Now watch a short stretch of string and account for its energy. Differentiate the density in
time:

$$
\frac{\partial u}{\partial t}
= \mu\,y_t\,y_{tt} + T\,y_x\,y_{xt} .
$$

Use the wave equation, $\mu\,y_{tt} = T\,y_{xx}$, on the first term:

$$
\frac{\partial u}{\partial t}
= T\,y_t\,y_{xx} + T\,y_x\,y_{xt}
= T\,\frac{\partial}{\partial x}\!\left(y_x\,y_t\right)
= -\,\frac{\partial P}{\partial x} .
$$

:::{admonition} Continuity, and what a conservation law looks like locally
:class: theorem
$$
\boxed{\;\frac{\partial u}{\partial t} + \frac{\partial P}{\partial x} = 0\;}
$$

The energy in any stretch $[a,b]$ changes only by what crosses its two ends:

$$
\frac{\mathrm{d}}{\mathrm{d}t}\int_a^b u\,\mathrm{d}x = P(a) - P(b) .
$$

Energy does not vanish here and reappear there. It flows, continuously, through every point in
between — which is the statement the ocean needed.

This is the course's first *local* conservation law, and the template for every one that
follows. Wherever a quantity is conserved, the same two objects appear: a density that says how
much is here, and a flux that says how much is going past. Module 15 builds the Poynting
vector this way for electromagnetic energy; probability current in quantum mechanics is the
same sentence again, with $|\psi|^2$ for $u$.
:::

Take the two fixed ends of a string as $a$ and $b$. A fixed end cannot move, so $y_t = 0$
there, so $P = 0$: nothing crosses, and the string's total energy is constant. That is the
conservation module 08's solver was already demonstrating, now derived rather than observed.

### Equipartition, and the speed of the energy

For a travelling wave everything collapses. Put $y_t = -v\,y_x$ into the two densities:

$$
u_K = \tfrac12\,\mu\,v^2\,y_x^2 = \tfrac12\,T\,y_x^2 = u_P ,
$$

since $\mu v^2 = T$ by definition of $v$.

:::{admonition} A travelling wave splits its energy evenly, everywhere and always
:class: theorem
At every point and at every instant, with nothing averaged over,

$$
u_K(x,t) = u_P(x,t) ,
$$

and therefore

$$
P = T v\,y_x^2 = v\left(u_K + u_P\right) = v\,u .
$$

The flux is the density times $v$: **the energy travels at exactly the wave speed**, which is
what that phrase can mean for a quantity that is spread out rather than located.
:::

Do not read this as the familiar equipartition of a mass on a spring. Module 01's oscillator is
all potential at the turning points and all kinetic at the middle, and its halves are equal only
after averaging over a cycle. Here nothing is averaged. The two densities are the *same
function of position*, at the same instant, because every element of the string is a little
behind its neighbour: what one mass does in sequence, the string does all at once, laid out
along its length.

And a standing wave does not do it either. For $y = A\sin kx\,\cos\omega t$ the string is all
potential at the moment of release and all kinetic a quarter period later, so $u_K$ and $u_P$
are as unequal pointwise as two quantities can be. Only the cycle averages match. Pointwise,
instantaneous equipartition is a property of a *travelling* wave, not of waves in general.

### The power a sinusoidal wave carries

For the course's travelling wave,

$$
y(x,t) = \Real\!\left[A\,e^{\ii(kx - \omega t)}\right] = |A|\cos(kx - \omega t + \arg A) ,
$$

the transverse velocity is $y_t = |A|\,\omega\sin(kx - \omega t + \arg A)$, so
$u_K = \tfrac12\mu|A|^2\omega^2\sin^2(\cdot)$ and, doubling for the equal potential part,
$u = \mu|A|^2\omega^2\sin^2(\cdot)$. The flux is $v$ times that, and the average of $\sin^2$
over a cycle is $\tfrac12$:

$$
\boxed{\;\langle P\rangle = \tfrac12\,\mu\,v\,\omega^2 |A|^2\;}
$$

Every factor earns its place. Doubling the amplitude quadruples the power, and so does doubling
the frequency — that is prediction 3, and both squares have one cause: the flux is quadratic in
the transverse velocity $|A|\omega$, and the two symbols enter only through that product. A
wave of half the amplitude and twice the frequency delivers exactly what it did before, on a
string that looks nothing like it did.

Written with the string's **impedance** $Z = \sqrt{T\mu} = \mu v$, the same result is

$$
\langle P\rangle = \tfrac12\,Z\,\left(|A|\omega\right)^2 ,
$$

a medium constant times the square of a velocity amplitude. Module 10 makes $Z$ the whole
subject; from there it runs to the Fresnel equations and to the irradiance of a light beam,
which is this formula with fields in place of displacements.

### Three velocities, told apart

| What moves | How fast | Chosen by |
|---|---|---|
| a piece of the medium, sideways | $\partial y/\partial t = -v\,y_x$ | whoever made the wave |
| the pattern | $v = \sqrt{T/\mu}$ | the medium |
| the energy | $P/u = v$ | the medium |

Two of the three are the same number and the third is unrelated. The medium's speed is
$|y_t| = v|y_x|$: the wave speed times the slope, and since the slope is small, the string
always crawls compared with its wave. In the laboratory's pulse the string's fastest is
1.145 m/s while the pattern runs at 20 m/s.

But nothing *forbids* $|A|\omega$ from exceeding $v$ — they are independent knobs, and that is
prediction 2. What stops it is the model, not the physics: $|A|\omega > v$ is the same
statement as $|A|k > 1$, a slope of order one, which is exactly where the small-slope
derivation of everything above gives out. A string whose pieces keep up with its own wave is a
string this module cannot describe.

(09-wave-energy-verify)=
## Verify computationally

Each check below is also a test in the project's suite, so these claims cannot silently rot.

**1. The densities are equal, pointwise.** A right-moving Gaussian pulse on a 1600-cell grid:
the largest gap between $u_K$ and $u_P$ anywhere is $1.1\times10^{-4}$ of the peak density, and
the integrated totals agree to $1.6\times10^{-4}$. Both fall fourfold for every halving of the
spacing, so the disagreement is the grid's.

**2. The energy rides at $v$.** On the same runs, $P/u$ is within $1.1\times10^{-6}$ of $v$
across the pulse.

:::{admonition} The energy velocity is better than second order
:class: numerical-observation
Refining the grid closes $u_K = u_P$ fourfold per halving — ordinary second-order behaviour —
but closes $P/u = v$ *sixteenfold*: $1.7\times10^{-5}$, $1.1\times10^{-6}$,
$6.9\times10^{-8}$, $4.4\times10^{-9}$ at 400, 800, 1600 and 3200 cells.

The reason is worth having. Write the departure from a pure right-mover as
$\varepsilon = (y_t + v\,y_x)/(v\,y_x)$; the grid is slightly dispersive, so a pulse made of
many wavelengths does not stay perfectly one-directional, and $\varepsilon$ is small but not
zero. The two densities differ at first order in $\varepsilon$. In the ratio $P/(vu)$ the
first-order terms cancel between numerator and denominator, leaving $\varepsilon^2$. The claim
that a wave's energy travels at exactly $v$ is the most numerically robust statement in the
module.
:::

**3. The local law holds where nothing imposed it.** `simulate_string` propagates displacements;
it has never heard of $u$ or $P$. Reading $\partial u/\partial t + \partial P/\partial x$ off
its output with centred differences gives a residual of $1.1\times10^{-3}$ of
$|\partial P/\partial x|$ on the laboratory's grid, falling as the spacing refines.

:::{admonition} The scheme obeys a discrete conservation law exactly
:class: numerical-observation
There is a stronger statement available, and it is about the scheme rather than the string.
Assign the kinetic energy to the grid points, where the masses are, and the potential energy
and the flux to the cells between them, where the springs are — the slope of a cell times the
mean velocity of its two ends. Then differentiating in time and substituting the solver's own
update makes every term cancel against the difference of two neighbouring cell fluxes,
*identically, for any $\Delta x$*.

So the residual cannot be improved by refining the grid and must be improved by refining the
step. Measured on one fixed grid: $3.3\times10^{-3}$, $8.3\times10^{-4}$, $2.1\times10^{-4}$ at
$S = 0.5$, $0.25$, $0.125$ — fourfold per halving, which is the velocity Verlet time error and
nothing else. The same law read pointwise instead sits at $1.0\times10^{-2}$ over those three
runs and does not move, because its error belongs to the spacing.

This is module 08's closing loop again, one level up. There the stencil *was* the mass chain;
here the chain's exact energy bookkeeping is what the grid inherits.
:::

**4. The wattmeter balances the books.** A pulse is launched at 1 m and metered at 2 m. The
integral of $P\,\mathrm{d}t$ at the gate comes to 4.177317 mJ; weighing the string beyond the
gate at the end of the run gives 4.177487 mJ, a ratio of 0.999959, and that is also exactly the
energy the pulse set out with. Three formulas that share nothing agree to four parts in
$10^5$ — and the laboratory repeats the measurement on a different pulse, to the same figure.

**5. Mean power, and its two squares.** A windowed sinusoidal train passes a gate and the flux
there is averaged over whole cycles. Against $\tfrac12\mu v\omega^2A^2$ the measurement lands
within 0.2% across a factor of four in amplitude and a factor of four in frequency; the fitted
exponent in amplitude is $2.000000$ and in frequency $1.995$.

The frequency exponent's shortfall is instructive and is not the string's. The slope at the
gate is recovered by a centred difference, which reads the slope of a sine low by
$(k\Delta x)^2/6$ — 0.6% for the shortest wave in the sweep, where a wavelength spans 32 grid
points. The amplitude sweep has no such term and comes out exact. As in module 08's photogates,
what you measure depends on how you measure it.

**6. The standing wave delivers nothing.** Four periods of the fourth mode of a fixed string:
the largest time-averaged flux anywhere is $2.6\times10^{-7}$ of the largest instantaneous
flux, while the instantaneous flux itself peaks at 12.6 mW. The cycle-averaged kinetic and
potential totals agree to $1.6\times10^{-4}$, and the pointwise difference between the densities
reaches the entire density — the contrast with the travelling wave, in one run.

**7. And what a real string can be asked.** Two of this module's three velocities are within
reach of a phone camera. Film a pulse on a stretched slinky, time its arrival at two tape marks
as module 08's problem 5 does, and then track a single taped coil frame by frame: two velocities
out of one video, differing by more than a factor of ten. The flux is another matter. Measuring
$P$ at a point means knowing the slope and the transverse velocity there *at the same instant*
and multiplying them — two small, separately noisy numbers, with the bias the laboratory's last
part measures waiting underneath. No affordable apparatus reads it directly, so a home
experiment measures the flux's *consequences* instead: energy arriving where it was not before.
The problem set sets that up.

(09-wave-energy-transfer)=
## Transfer the idea

:::{admonition} One flux, many fields
:class: important
The pattern established here — a density, a flux, and a continuity equation tying them — is how
every conserved quantity in physics is accounted for locally. The wave equation just happens to
be the simplest place to meet it.

- **Electromagnetic energy.** Module 15 derives $\partial u/\partial t + \nabla\cdot\mathbf{S} = 0$
  with $u = \tfrac12(\varepsilon_0 E^2 + B^2/\mu_0)$ and the Poynting vector
  $\mathbf{S} = \mathbf{E}\times\mathbf{H}$. The equal split of $u_K$ and $u_P$ becomes the
  equal split of the electric and magnetic energy densities in a light wave — the same theorem,
  the same proof.
- **Intensity.** From module 23 onward, "intensity" means the time-averaged flux of a wave, and
  every interference and diffraction pattern in this course is a map of $\langle P\rangle$. That
  it goes as the square of an amplitude is decided here.
- **Sound.** Acoustic intensity is $\langle p\,u\rangle$ — pressure times particle velocity,
  the same product of a force-like and a velocity-like quantity.
- **Quantum mechanics.** $\partial|\psi|^2/\partial t + \partial j/\partial x = 0$ defines the
  probability current. Nothing is conserved differently; only the density changes its name.
:::

- **Standing waves.** `11-standing-waves` puts walls at both ends and asks where the energy goes
  when the flux averages to zero. The answer — that it is stored, sloshing between kinetic and
  potential a quarter wavelength at a time, rather than transported — starts from this module's
  last verification.
- **Impedance.** [Module 10](10-impedance.md) sends a wave at a junction between two media
  and divides its
  energy in two. The reflection and transmission coefficients are fixed by requiring exactly
  what this module built: that the flux arriving equals the flux leaving.
- **Dispersion.** The energy velocity $P/u$ came out equal to $v = \omega/k$ here because the
  ideal string is non-dispersive. `13-dispersion` finds that when $\omega/k$ varies with
  wavelength, the energy travels at the *group* velocity $\mathrm{d}\omega/\mathrm{d}k$ instead,
  and the two can differ by a lot — the reason a phase velocity above $c$ breaks nothing.
- **Cables and antennas.** Power sent along a transmission line is $\tfrac12 Z |I|^2$, the same
  algebra with current for transverse velocity. An unterminated cable reflects it, for the
  reason [module 10](10-impedance.md) gives.

(09-wave-energy-quiz)=
## Check your understanding

```{include} ../_generated/quiz-09-wave-energy.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](09-wave-energy-problems.md).

(09-wave-energy-explain)=
## Explain it in your own words

Answer in a few sentences each. No number will save you.

1. Explain why the crest of a wave is the least energetic part of the string, to someone who
   is certain the energy is where the displacement is. Use only the two things a string can do
   to store energy.
2. Energy flows through a medium that goes nowhere. Describe how, using the word "neighbour"
   and without using the word "carry".
3. A wattmeter on a string reads $-0.4$ W. Say what is happening, and what would have to change
   for it to read $+0.4$ W with the string looking exactly the same in a photograph.
4. A travelling wave and a standing wave of the same amplitude have the same energy on the
   string and the same instantaneous flux, to within a factor of four. One delivers power and
   the other delivers none. Explain the difference without writing down a formula.

(09-wave-energy-advanced)=
## Advanced: the momentum question, and what "energy velocity" will stop meaning

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section.
:::

**Energy velocity, and its expiry date.** Defining the energy transport velocity as $P/u$ is
more than a convenience: it is the definition that survives when $\omega/k$ stops being the
answer. On the ideal string all three of $\omega/k$, $\mathrm{d}\omega/\mathrm{d}k$ and $P/u$
coincide, so the module can afford to be casual. In a dispersive medium they separate, $P/u$
follows the group velocity $\mathrm{d}\omega/\mathrm{d}k$, and the phase velocity $\omega/k$ —
which can exceed $c$ without embarrassment — stops describing the motion of anything at all.
`13-dispersion` does this properly; the reason it *can* is that the quantity to track was
defined here as a ratio of two things a measurement can reach.

**Does a transverse wave carry momentum along the string?**

:::{admonition} A question the ideal string cannot answer
:class: open-question
The energy bookkeeping above is settled physics. The momentum bookkeeping is not, and it is
worth knowing which is which.

Transverse momentum is easy: the string's pieces move sideways, $\int \mu\,y_t\,\mathrm{d}x$ is
their total transverse momentum, and for a pulse that starts and ends at rest it is zero. The
hard question is *longitudinal* momentum — does a pulse push the string along its own length?
The answer is second order in the slope, $O(y_x^2)$, which is precisely the order at which the
ideal string model was built by throwing things away. Whether an element is carried forward or
back, and by how much, depends on constitutive details the model discarded: whether the string
is inextensible or Hookean, whether the tension is held constant or the length is, what the
ends are attached to. Papers in the American Journal of Physics have gone back and forth on it
for decades — a representative entry is D. R. Rowland, *"The potential energy density in
transverse string waves depends critically on longitudinal motion,"* Eur. J. Phys. **32**, 1475
(2011), which shows that even the potential-energy *density* is not unambiguous once
longitudinal motion is taken seriously.

What survives that argument is everything this module actually used. The total energy, the
flux, the continuity equation and the mean power are all first-order-in-$y_x^2$ quantities that
every version of the model agrees on. The course stays at the flux level on purpose, and says
so rather than quietly choosing a side.

The corresponding question for light — whether a photon in a medium carries momentum
$n\hbar\omega/c$ or $\hbar\omega/(nc)$ — is the Abraham–Minkowski controversy, a century old and
resolved only in the sense that the two answers turn out to account for different halves of the
same total. `16-light-in-matter` mentions it in passing, for the same reason it appears here:
knowing where a model's authority ends is part of knowing the model.
:::

**Why the potential density has that form, exactly.** The derivation above expanded
$\sqrt{1 + y_x^2}$ and kept one term. A fair objection is that the discarded $-\tfrac18 y_x^4$
is of the same order as corrections to the *equation of motion* that were also discarded, so
what licenses keeping $\tfrac12 T y_x^2$? The answer is that both are the leading term of their
own quantity: the equation of motion's leading term is $O(y_x)$ and the energy's is $O(y_x^2)$,
so each is the first non-vanishing contribution, and the ratio of neglected to kept is $y_x^2$
in both. The two approximations are consistent, which is why the continuity equation closes
exactly rather than to some order — as the discrete version above shows, it closes exactly even
on a grid.
