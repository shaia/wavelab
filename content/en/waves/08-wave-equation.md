---
title: "The wave equation: oscillations acquire space"
short_title: 08 · The wave equation
module: 08-wave-equation
objectives:
  - id: OBJ-08-1
    text: Derive d^2y/dt^2 = v^2 d^2y/dx^2 two ways — continuum limit of the coupled-mass chain, and Newton for a string element under tension — stating the small-slope assumption |dy/dx| << 1 both routes require.
  - id: OBJ-08-2
    text: Verify that y = f(x - v t) + g(x + v t) solves the wave equation for any twice-differentiable f, g, and identify v = sqrt(T/mu) as fixed by the medium.
  - id: OBJ-08-3
    text: Solve the initial-value problem by d'Alembert — split a pluck (shape, no velocity) into half-amplitude counter-propagating copies; integrate a strike (velocity, no shape).
  - id: OBJ-08-4
    text: Predict how pulse speed responds to tension, density, amplitude, and shape (only T and mu matter), and check omega = v k for sinusoidal waves.
  - id: OBJ-08-5
    text: Integrate the wave equation with a leapfrog scheme, state the CFL condition v dt/dx <= 1, and recognise its violation in a solution.
  - id: OBJ-08-6
    text: Explain what travels and what does not — the disturbance moves at v while each medium element moves transversely about its rest position.
---

# The wave equation: oscillations acquire space

:::{note} Two changes of letter
Module 07 called the chain's long-wavelength speed $c$. From here on a wave's speed is $v$,
because $c$ is about to mean the speed of light, and module 14 needs it to mean nothing else.
And where module 07's last equation wrote the displacement as $\psi$, a string's displacement
is $y$ — sideways, like the plots. The physics is unchanged; the letters are being put where
they will stay.
:::

(08-wave-equation-puzzle)=
## The puzzle: something crosses, and nothing makes the trip

At a football match, a wave goes round the stadium. You can watch it travel: a band of
standing, arms-up fans sweeping along the stands, once round the ground in half a minute. And
yet nobody in the stadium has moved from their seat. Each person stood up and sat down again,
a little after their neighbour did.

Tie a 20 m rope to a wall, pull it taut, and flick the end. Something runs along the rope and
slaps the wall a fraction of a second later — you can feel it arrive through the wall if you
put your other hand on it. No piece of rope made that trip.

:::{important} The question
Something crosses the rope, and it is not rope. What is the thing that moves — and what
decides how fast it goes? Can you make it go faster by flicking harder?
:::

(08-wave-equation-predict)=
## Predict before you calculate

Commit to an answer for each before running anything.

1. Two pulses on the same rope, one twice as tall as the other. Which reaches the far end
   first — the taller one, the shorter one, or neither?
2. A speck of dust rests halfway along the rope. A pulse runs through it and on. Where is the
   speck afterwards?
3. You double the tension in the rope. Does the time a pulse takes to cross it halve, fall by
   some other factor, or stay the same?
4. You pull the middle of the rope aside into a triangle, hold it still, and let go. Does one
   pulse leave, or two?

:::{note} Why we ask first
Questions 1 and 2 are this module's two misconceptions, and both feel obvious. Everyday
experience says that harder means faster, and that a wave on water carries things along with
it. The first is false for any wave this module describes; the second confuses two different
things that happen to a floating object, and on a string only one of them survives.
:::

(08-wave-equation-explore)=
## Explore the model

Three animations, all generated from the same `wavelab.waves` solver the laboratory runs.
Every displacement is drawn in millimetres on a string several metres long, so every pulse
on screen is hundreds of times steeper than the string it depicts. The axis units say so;
the physics assumes the true, gentle slopes.

:::{figure} ../media/wave-pulse-speck.mp4
:width: 100%

A pulse runs 2.6 m along a string at 20 m/s. One point of the string, 2 m along, is marked in
orange, with a faint trail of everywhere it has been. The trail is a vertical line. The lower
panel records the point's height against time: it rises 10 mm as the front of the pulse
arrives, falls as the back leaves, and finishes within $6\times10^{-5}$ mm of where it
started. Whatever crossed the string, none of the string went with it.
:::

:::{figure} ../media/wave-pluck-split.mp4
:width: 100%

A string pulled into a 10 mm triangle and released from rest. It splits into two triangles
of half the height, running apart. The translucent fills beneath are d'Alembert's two halves,
$y_0(x - vt)/2$ in blue and $y_0(x + vt)/2$ in orange: at the first frame they lie on top of
each other and the string is their sum; as they slide apart the string follows. The solver
matches the formula to $2\times 10^{-14}$ of the height over the whole run — it is at the
special time step derived below, where a pluck is carried exactly.
:::

:::{figure} ../media/wave-cfl-blowup.mp4
:width: 100%

The same pluck computed twice, with the time step 1% under the stability limit (blue) and 1%
over it (orange). For a hundred steps the two strings look identical. The bottom panel shows
why that is misleading: on a logarithmic axis it tracks the shortest wave the grid can hold,
and in the orange run it climbs a straight line from rounding error, multiplying by 1.33 every
step. At step 137 it reaches the pulse's own size, and within a dozen steps the string panel is
overwhelmed. Nothing physical happened.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** the transverse displacement field $y(x,t)$ of a uniform string of tension $T$ and linear mass density $\mu$, of length $L$. Observables: the displacement and transverse velocity of every point, and the arrival times of pulses at fixed detectors.
- **Dynamics:** $\mu\,y_{tt} = T\,y_{xx}$, evaluated exactly by d'Alembert's solution and integrated numerically by the leapfrog scheme, whose stencil is Newton's law for a chain of masses $\mu\,\Delta x$ on springs $T/\Delta x$.
- **Boundary:** fixed ends, kept out of reach of the pulses; what happens when a pulse gets there is module 10's subject.
- **Ensemble:** deterministic; detector noise, where added, is Gaussian, independent and seeded.
- **Ignored:** bending stiffness, damping, gravity sag, longitudinal motion, and nonlinearity — the string is perfectly flexible, lossless, weightless in its sag and small in its slopes.
- **Valid when:** slopes are small, $|y_x| \ll 1$; numerically, the Courant number $S = v\,\Delta t/\Delta x \le 1$ and every feature of a pulse spans many grid points.
- **Failure modes:** order-one slopes, where the model rather than the code breaks; $S > 1$, where the scheme destroys itself from the grid scale upward; grid dispersion on under-resolved features, read as physics.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 08 — the wave equation](/lite/lab/index.html?path=en/labs/08-wave-equation.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/08-wave-equation.ipynb`.
:::

Run the laboratory now, then come back. Four things are worth doing before you read on:

- Watch a chain of 5, 20 and 100 beads turn into a string, and notice how slowly the corners
  of a triangular pluck get there.
- Time a pulse between two photogates as the tension changes, then race pulses of different
  heights and widths on the same string.
- Follow the dust speck, and compare how fast it moves with how fast the pulse moves.
- Set the time step 1% too long and count the steps the string survives.

(08-wave-equation-derive)=
## Derive the result

### Route (a): module 07's chain, one step further

Put beads of mass $m$ on a thread, a distance $a$ apart, and pull the thread to tension $T$.
Displace bead $n$ sideways by $y_n$. The stretch of thread to its right is tilted by an angle
whose sine is $(y_{n+1} - y_n)/\sqrt{a^2 + (y_{n+1}-y_n)^2}$, and it pulls the bead with a
transverse force $T$ times that sine. For small tilts the square root is just $a$, and the two
stretches together give

$$
m\,\ddot y_n = \frac{T}{a}\left(y_{n+1} - y_n\right) - \frac{T}{a}\left(y_n - y_{n-1}\right)
= \frac{T}{a}\left(y_{n+1} - 2y_n + y_{n-1}\right).
$$

This is module 07's chain exactly, with springs of stiffness $k_s = T/a$ — the dictionary
$T = k_s a$ that module 07 ended on, now with a reason behind it.

Now let the beads crowd together. Treat the displacements as samples of a smooth function,
$y_n(t) = y(na, t)$, and expand the neighbours about $x = na$:

$$
y_{n\pm1} = y \pm a\,y_x + \frac{a^2}{2}\,y_{xx} \pm \frac{a^3}{6}\,y_{xxx} + \frac{a^4}{24}\,y_{xxxx} + \cdots
$$

In the sum $y_{n+1} + y_{n-1}$ every odd term cancels, so the second difference is

$$
y_{n+1} - 2y_n + y_{n-1} = a^2\,y_{xx} + \frac{a^4}{12}\,y_{xxxx} + \cdots
$$

Keep the leading term, divide by $a$, and write $\mu = m/a$ for the mass per unit length:

$$
\mu\,\frac{\partial^2 y}{\partial t^2} = T\,\frac{\partial^2 y}{\partial x^2}.
$$

Module 07 already knew the answer to the speed. Its dispersion relation
$\omega(k) = 2\sqrt{k_s/m}\,|\sin(ka/2)|$ is a straight line at small $ka$, with slope
$a\sqrt{k_s/m} = \sqrt{(T/a)\,a^2/m} = \sqrt{T/\mu}$. The discarded $a^4 y_{xxxx}/12$ is exactly
what bends that line over at larger $k$: expanding the sine to the next order gives
$\omega^2 \approx (T/\mu)\,k^2\left(1 - (ka)^2/12\right)$, the same twelve.

### Route (b): Newton for a piece of string

Forget beads. Take a short piece of a continuous string, between $x$ and $x + \mathrm{d}x$, and
list the forces on it. At each end the rest of the string pulls along its own direction with
tension $T$. If the string is tilted at angle $\theta(x)$ at the left end and $\theta(x + \mathrm{d}x)$
at the right, the vertical parts of the two pulls are $-T\sin\theta(x)$ and
$+T\sin\theta(x + \mathrm{d}x)$, and they cancel only if the string is straight.

For small slopes, $\sin\theta \approx \tan\theta = y_x$. The net vertical force is then
$T\left[y_x(x + \mathrm{d}x) - y_x(x)\right] = T\,y_{xx}\,\mathrm{d}x$, the piece has mass
$\mu\,\mathrm{d}x$, and Newton's second law reads

$$
\mu\,\mathrm{d}x\;y_{tt} = T\,y_{xx}\,\mathrm{d}x
\qquad\Longrightarrow\qquad
\mu\,y_{tt} = T\,y_{xx}.
$$

:::{admonition} Small slopes, used three times
:class: model-assumption
Both routes need $|y_x| \ll 1$, and route (b) spends it three times. It replaces $\sin\theta$
by the slope. It takes the piece's mass as $\mu\,\mathrm{d}x$, when its true length is
$\sqrt{1 + y_x^2}\,\mathrm{d}x$. And it treats $T$ as the same at both ends: the horizontal parts
of the pulls, $T\cos\theta$, must balance because the piece does not move sideways, and
$\cos\theta$ differs from 1 only at second order in the slope. Route (a) uses the same
approximation once, hidden in each bead's pull.

How small is small? A guitar string plucked 3 mm out of line at the middle of 650 mm has slopes
near $0.01$, and every one of those corrections is a part in $10^4$. A skipping rope swung in a
wide arc has slopes of order one, and this model is simply wrong about it. That is a statement
about the model, not about the solver — no amount of computing rescues a model used outside the
range where it was derived.
:::

Two routes meeting at one equation is the lesson. The wave equation is not about beads and it
is not about strings: it is about any medium whose pieces are pulled back toward the line by
their neighbours, in proportion to how far out of line they are. Write the speed as

$$
\boxed{\;v = \sqrt{\frac{T}{\mu}}\;}
$$

and the equation takes the form every later part of the course will recognise:

$$
\frac{\partial^2 y}{\partial t^2} = v^2\,\frac{\partial^2 y}{\partial x^2}.
$$

:::{important} The course's first partial differential equation
Until now every equation of motion has been an ordinary differential equation: a few numbers,
$x_1(t), \dots, x_N(t)$, changing in time. Here the unknown is a *field* — a displacement at
every point, $y(x,t)$ — and its equation relates rates of change in time to rates of change in
space. The law is local: each piece of string responds only to the curvature right where it
is. The consequence is global: shapes travel, rigidly, over any distance, at a speed no single
piece knows anything about.
:::

### D'Alembert's solution: every solution is two travelling shapes

Try $y = f(x - vt)$ for any twice-differentiable function $f$. By the chain rule, each time
derivative brings down a factor $-v$ and each space derivative a factor 1:

$$
y_{tt} = v^2 f''(x - vt), \qquad y_{xx} = f''(x - vt),
$$

so $y_{tt} = v^2 y_{xx}$, whatever $f$ is. The graph of $f(x - vt)$ is the graph of $f$ shifted
right by $vt$: a shape moving toward $+x$ at speed $v$, unchanged. By the same argument
$g(x + vt)$ is a shape moving toward $-x$. The remarkable thing is that there is nothing else.

:::{admonition} d'Alembert's theorem
:class: theorem
Every solution of $y_{tt} = v^2 y_{xx}$ on the whole line is

$$
y(x,t) = f(x - vt) + g(x + vt)
$$

for some functions $f$ and $g$: one shape travelling right, one travelling left.

The proof is a change of variables. With $u = x - vt$ and $w = x + vt$, the chain rule gives
$\partial_x = \partial_u + \partial_w$ and $\partial_t = -v\,\partial_u + v\,\partial_w$, so

$$
y_{tt} - v^2 y_{xx} = v^2\left(\partial_u - \partial_w\right)^2 y - v^2\left(\partial_u + \partial_w\right)^2 y
= -4v^2\,\frac{\partial^2 y}{\partial u\,\partial w}.
$$

The wave equation therefore says $\partial^2 y/\partial u\,\partial w = 0$. Integrate over $w$:
$\partial y/\partial u$ depends on $u$ alone. Integrate over $u$: $y$ is a function of $u$ plus
a function of $w$.
:::

Read what the theorem leaves out. The speed $v$ is in the equation; the shapes $f$ and $g$ are
not. **The medium chooses the speed, and the hand chooses only the shape.** A taller pulse is the
same solution multiplied by a constant; a sharper one is a different $f$; both travel at
$\sqrt{T/\mu}$. That is prediction 1 — neither arrives first — and prediction 3: doubling the
tension multiplies $v$ by $\sqrt 2$, so the crossing time falls to $1/\sqrt 2$, about 71%, and
not to half.

### The initial-value problem: plucks and strikes

A real string starts with some shape $y_0(x)$ and some velocity $w_0(x)$. Which $f$ and $g$ do
those select? At $t = 0$,

$$
f(x) + g(x) = y_0(x),
\qquad
-v\,f'(x) + v\,g'(x) = w_0(x).
$$

Integrate the second equation, $g - f = \frac{1}{v}\int_0^x w_0(s)\,\mathrm{d}s$ up to a constant
that cancels, and solve the pair:

$$
\boxed{\;
y(x,t) = \frac{y_0(x - vt) + y_0(x + vt)}{2}
+ \frac{1}{2v}\int_{x - vt}^{x + vt} w_0(s)\,\mathrm{d}s \;}
$$

**A pluck** has a shape and no velocity. The integral vanishes, and the string becomes two
copies of the starting shape, each **half the height**, running apart. It must split — a single
copy moving one way would need a velocity from the start, and a string held still has none, so
neither direction is preferred and each gets half. That is prediction 4.

**A strike** has a velocity and no shape: a hammer hitting a piano string, a rectangle of speed
$w$ over a width $2\ell$. Now only the integral survives. At a given point it counts how much
struck string lies within a distance $vt$, so the string rises into a plateau that grows at
speed $w$ until $t = \ell/v$ and then holds at height $w\ell/v$, its edges running outward at
$v$. The string is left permanently displaced — nothing pulls it back, because moving a whole
straight stretch sideways stretches nothing.

### Sinusoidal waves, and $\omega = vk$

The course's travelling wave is

$$
y(x,t) = \Real\!\left[A\,e^{\ii(kx - \omega t)}\right] = |A|\cos(kx - \omega t + \arg A).
$$

Factor out $k$: $kx - \omega t = k\,(x - (\omega/k)\,t)$, so this is $f(x - vt)$ with
$v = \omega/k$. It solves the wave equation exactly when

$$
\omega = v\,k,
$$

the straight-line dispersion relation module 07 found at the bottom of the chain's band. Every
wavelength travels at the same speed: that is what it means for the ideal string to be
*non-dispersive*, and it is why a pulse — a superposition of many wavelengths — keeps its shape.
In everyday units, $v = \omega/k = f\lambda$.

### What travels, and what does not

Stand at one point, $x_0$, and watch a right-moving pulse go by. The displacement there is
$y(x_0, t) = f(x_0 - vt)$: as $t$ runs, the point reads off the pulse's shape backwards in
time, rising as the front arrives and falling as the back leaves. When the pulse has gone,
$f$ has returned to zero, and so has the point. That is prediction 2: **the speck ends exactly
where it started.**

What travelled was the pattern — the fact of being displaced, handed from each piece of string
to the next — and, as [module 09](09-wave-energy.md) shows, the energy that goes with it. The
pieces themselves move only sideways, and at a speed with nothing to do with $v$:

$$
y_t = -v\,f'(x - vt) = -v\,y_x .
$$

The transverse velocity is $v$ times the slope, and since the slope is small, the string moves
far more slowly than the wave. In the laboratory's pulse, the speck's fastest is 1.14 m/s while
the pulse travels at 20 m/s.

Two honesty notes. The ideal string has no motion along its own length at all, by assumption,
so the vertical trail in the animation is partly built in. A real string's pieces do move
slightly along it, by an amount second order in the slope — and they return too. The claim
that survives is the one that matters: *after the pulse, nothing is anywhere else.*

### How the computer solves it: the chain, rebuilt

To integrate the wave equation numerically, sample the string at points $x_i = i\,\Delta x$ and
times $t_n = n\,\Delta t$, and replace each second derivative by its centred difference:

$$
\frac{y_i^{n+1} - 2y_i^n + y_i^{n-1}}{\Delta t^2}
= v^2\,\frac{y_{i+1}^n - 2y_i^n + y_{i-1}^n}{\Delta x^2}.
$$

Solved for the future, this is the **leapfrog** scheme,

$$
y_i^{n+1} = 2y_i^n - y_i^{n-1} + S^2\left(y_{i+1}^n - 2y_i^n + y_{i-1}^n\right),
\qquad
S = \frac{v\,\Delta t}{\Delta x},
$$

where $S$ is the **Courant number**. Now look at the right-hand side of the difference equation
before dividing: it is $\mu\,\Delta x\;\ddot y_i = (T/\Delta x)\left(y_{i+1} - 2y_i + y_{i-1}\right)$.
That is Newton's law for a mass $\mu\,\Delta x$ on springs of stiffness $T/\Delta x$ — route (a)'s
chain, with the beads a grid spacing apart. The computer solves the continuum equation by
quietly rebuilding the chain it came from. Discretisation runs the continuum limit backwards.

One condition makes the scheme trustworthy. In one time step the update at point $i$ consults
only points $i-1$, $i$ and $i+1$, so information on the grid moves at most one spacing per
step. The true solution at $x_i$ depends on everything within $v\,\Delta t$ of it. If
$v\,\Delta t > \Delta x$, the solution depends on points the scheme never looked at, and no
arrangement of numbers can get it right. The **Courant–Friedrichs–Lewy condition** is

$$
\boxed{\; S = \frac{v\,\Delta t}{\Delta x} \le 1 \;}
$$

and violating it is not a small inaccuracy. The next section shows what it is.

(08-wave-equation-verify)=
## Verify computationally

Each check below is also a test in the project's suite, so these claims cannot silently rot.

**1. The solver against d'Alembert.** A Gaussian pluck on a 4 m string is integrated at a fixed
Courant number $S = 0.5$ and compared, at every point, with the exact solution. Halving the grid
spacing — and with it the step — reduces the $L^2$ error by factors of 3.996, 4.002, 4.001 and
4.000, and the fitted exponent is $-2.000$: the scheme is second order, as the centred
differences promise. This convergence test is run before any animation on this page is
rendered.

**2. The stencil is the chain.** `simulate_string` is handed a 201-point string, and
`coupled.simulate_coupled` — module 07's integrator, which knows nothing about grids — is
handed the chain of masses $\mu\,\Delta x$ on springs $T/\Delta x$. Started identically, they
agree for 2000 steps to about $1\times 10^{-14}$ of the largest displacement. The closing claim of the
derivation is not an analogy.

**3. The magic step.** At $S = 1$ exactly, the stencil simplifies to
$y_i^{n+1} = y_{i+1}^n + y_{i-1}^n - y_i^{n-1}$, which moves any travelling shape by exactly one
grid spacing per step.

:::{admonition} Exact at S = 1, and only there
:class: numerical-observation
A pluck integrated for 400 steps at $S = 1$ matches d'Alembert to $5.9\times 10^{-15}$ of its
height — rounding error. The same pluck at $S = 0.99$, on the same grid, is off by
$1.0\times 10^{-5}$: ten orders of magnitude for a one-percent change of step.

It is exact only given exact values at the first two steps. A pluck supplies them, because a
string at rest has an exact second step. A pulse *started moving* does not: its second step is
off at third order, the transport carries that defect faithfully, and the error settles at
second order — still about 7.5 times smaller than at $S = 0.5$ on the same grid, but no longer
exact. The trick is real and narrow.
:::

**4. Past the limit.** The pluck is run at $S = 1.01$.

:::{admonition} The blow-up, and its rate
:class: numerical-observation
The displacement passes ten times the pluck's height at step 140 and keeps multiplying. The
growth is not random: it lives in the shortest wave the grid can hold, neighbours in exact
antiphase, and it starts from rounding error at the very first step. Its measured growth per
step matches the von Neumann prediction derived in the advanced section to better than 0.5% at
$S = 1.01$, $1.05$ and $1.1$. At $S = 0.99$, two thousand steps leave the pulse's height where
it was.

The string is stable at every $S$. What failed is a scheme asked to carry information further
than one grid spacing per step — which is why `simulate_string` refuses $S > 1$ unless told
that watching it fail is the point.
:::

**5. Photogates, and what they measure.** Two detectors record the string where they sit, and
the pulse's arrival at each is timed by the centroid of its record. With the time step fixed
for the fastest string, tension is swept over a decade: the fitted exponent of $v$ against $T$
is 0.5000000, and against $\mu$ it is $-0.5000000$, every speed within $3\times 10^{-9}$ of
$\sqrt{T/\mu}$. Nine pulses of three heights and three widths on one string arrive at the same
speed to $10^{-7}$ — the falsifier for "shaking harder makes it faster", run nine times.

Timing the *peak* of each record instead reads slow, by the relative amount
$(1 - S^2)(\Delta x/\sigma)^2/4$ for a Gaussian of width $\sigma$ — measured to within 0.4% of
that formula at $S = 0.25$, $0.5$ and $0.75$, and exactly $v$ at $S = 1$. This is grid
dispersion: on the grid, short wavelengths travel slightly slower than long ones, and the peak
of a pulse drifts back. The centroid is immune, because it responds only to the dispersion
relation's slope at $k = 0$, where the grid is exact. The laboratory's measurement part
turns the same distinction into an error bar.

**6. Energy.** Over sixteen transits between two fixed ends, the solver's total energy wobbles
by $4.7\times 10^{-4}$ of itself at $S = 0.5$ and does not drift; halve the step and the wobble
falls fourfold. What that energy *is*, and where on the string it lives, is
[module 09](09-wave-energy.md).

(08-wave-equation-transfer)=
## Transfer the idea

:::{admonition} One equation, many media
:class: important
The derivation above never needed the string to be a string. It needed a quantity that can be
displaced, an inertia resisting the displacement, and a restoring effect proportional to the
curvature. Wherever those three meet, $y_{tt} = v^2 y_{xx}$ follows, with $v^2$ the restoring
stiffness divided by the inertia:

- **Sound in a gas:** pressure disturbances, $v = \sqrt{\gamma p/\rho}$ — 343 m/s in air at
  room temperature.
- **Seismic waves:** shear waves in rock with $v = \sqrt{G/\rho}$, and compressional waves,
  faster, with $v = \sqrt{(K + \tfrac43 G)/\rho}$; the gap between their arrival times is how a
  seismometer measures its distance to an earthquake.
- **Shallow water:** a tsunami in 4000 m of ocean travels at $\sqrt{g h}$, about 200 m/s — the
  speed of an airliner.
- **Light:** Maxwell's equations give this same equation for the electric field, with
  $v = 1/\sqrt{\mu_0\varepsilon_0} = c$. Module 14 derives it.
:::

- **Standing waves.** Put walls at both ends and the travelling halves come back.
  `11-standing-waves` builds a string's modes from d'Alembert's two directions, and recovers
  module 07's $\sin(p\pi x/L)$ as the $N \to \infty$ limit of the chain's mode shapes.
- **Dispersion.** The ideal string is non-dispersive by construction: $\omega = vk$ is a
  straight line. `13-dispersion` asks what happens when it is not, where a pulse spreads as it
  travels — and you have already seen it happen, on the grid, in the photogate check above.
- **Back to module 07.** The chain's band edge was a ceiling the string does not have. The
  string's equation is what remains of the chain when every wavelength of interest is much
  longer than the spacing, and route (a) says precisely how much longer.
- **Longitudinal waves.** Module 07's chain was drawn sideways but modelled lengthways: masses
  sliding along their own line. Read that way, route (a) is exact without any small-slope
  assumption, and gives sound in a solid rod, with $k_s a$ playing the part of the rod's
  stiffness rather than a tension.

(08-wave-equation-quiz)=
## Check your understanding

```{include} ../_generated/quiz-08-wave-equation.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](08-wave-equation-problems.md).

(08-wave-equation-explain)=
## Explain it in your own words

Answer in a few sentences each. No number will save you.

1. Explain what moves in a stadium wave, and what does not. Then explain what moves along a
   flicked rope, using the same words, and say what plays the part of each fan.
2. Why can "how hard you flick" not appear in the speed of the pulse? Give an answer that uses
   the wave equation, and a second answer that does not use any equation at all.
3. A string released from rest in a triangle splits into two triangles. A friend says one
   triangle travelling to the right would conserve energy just as well. Explain what is wrong
   with that, without mentioning energy.
4. A simulation of a vibrating string blows up after 140 steps. Explain why this is a statement
   about the numerical method and not about the string, and say what single change would fix
   it.

(08-wave-equation-advanced)=
## Advanced: stability, the magic step, images, and what a first PDE is

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section.
:::

**Von Neumann's argument.** Where exactly does $S \le 1$ come from? Try a single Fourier mode on
the grid, $y_i^n = g^n e^{\ii k i \Delta x}$, and ask how its amplitude $g$ changes per step.
Substituting into the leapfrog stencil gives

$$
g^2 - 2\left[1 - 2S^2\sin^2\!\left(\frac{k\Delta x}{2}\right)\right] g + 1 = 0 .
$$

The two roots multiply to 1. While the bracket lies between $-1$ and $1$ they are a complex
conjugate pair on the unit circle, $|g| = 1$, and the mode neither grows nor decays. Once the
bracket falls below $-1$ they are real, one of them has $|g| > 1$, and the mode grows
exponentially. The bracket stays in range for every $k$ if and only if $S \le 1$. The worst mode is the shortest the grid can hold,
$k\Delta x = \pi$, where for $S > 1$

$$
|g| = \left(2S^2 - 1\right) + \sqrt{\left(2S^2 - 1\right)^2 - 1} ,
$$

1.3266 at $S = 1.01$. That is the number the blow-up in the verification section matched — and
since rounding error contains every $k$ in small amounts, there is always a seed for it to grow
from.

**Why S = 1 is exact.** With $|g| = 1$, write $g = e^{-\ii\omega\Delta t}$ and the same equation
becomes the grid's dispersion relation,

$$
\sin\!\left(\frac{\omega\Delta t}{2}\right) = S\,\sin\!\left(\frac{k\Delta x}{2}\right).
$$

At $S = 1$ the two sines are equal, so $\omega\Delta t = k\Delta x$ and $\omega = vk$ exactly —
every wavelength the grid can hold travels at exactly $v$, and there is no grid dispersion at all.
For $S < 1$, expanding both sines gives
$\omega \approx vk\left[1 - (1 - S^2)(k\Delta x)^2/24\right]$: short waves lag, which is the
photogate bias measured above. The step that is exact and the step that is unstable are
$1\%$ apart.

**The half-line, by images.** d'Alembert's solution lives on an infinite line. Put a fixed end at
$x = 0$, where $y(0, t) = 0$ for all time, and it still works, by a trick. Extend the starting
shape to negative $x$ as an *odd* function, $y_0(-x) = -y_0(x)$, and solve on the whole line.
At $x = 0$ the two halves are then always equal and opposite, so the displacement there is zero
for ever — the boundary condition, satisfied by symmetry rather than imposed. A pulse
approaching the wall meets its own upside-down image coming the other way, and after they pass
through each other the image is the one that emerges: **a fixed end returns a pulse inverted.**
Extend evenly instead and the slope at $x = 0$ vanishes — a free end — which returns the pulse
upright. Module 10 derives both results properly, as the two limits of one formula.

**What makes a PDE "first".** The wave equation is the simplest *hyperbolic* equation, and its
character is in d'Alembert's variables: $x - vt$ and $x + vt$ are constant along lines in the
$(x, t)$ plane called **characteristics**, and information moves only along them. The solution
at $(x, t)$ depends on the starting data only in the interval $[x - vt, x + vt]$ — its *domain of
dependence* — and on nothing outside it. The CFL condition is the discrete echo of that fact:
the grid's own domain of dependence, one spacing per step, must contain the true one. The heat
equation, $y_t = D\,y_{xx}$, looks almost identical and behaves completely differently: it has no
characteristics, a disturbance is felt everywhere instantly, and shapes smear instead of
travelling. One derivative in time rather than two is the whole difference.
