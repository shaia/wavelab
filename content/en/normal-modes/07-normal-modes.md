---
title: "Normal modes: the right basis, the N-mass chain, and the road to the continuum"
short_title: 07 · Normal modes
module: 07-normal-modes
objectives:
  - id: OBJ-07-1
    text: Formulate the normal-mode problem as the generalized eigenvalue problem K a = omega^2 M a, solve it numerically, and interpret the eigenvalues as squared mode frequencies and the eigenvectors as mode shapes.
  - id: OBJ-07-2
    text: Decompose arbitrary initial conditions into modal coordinates using M-orthogonality, and predict the motion as a sum of independent oscillators.
  - id: OBJ-07-3
    text: State and use the fixed-end chain results — shapes a_p(j) ~ sin(p pi j/(N+1)) and frequencies omega_p = 2 sqrt(k_s/m) sin(p pi/(2(N+1))), with exactly N modes.
  - id: OBJ-07-4
    text: Plot and interpret the chain dispersion relation omega(k) = 2 sqrt(k_s/m) |sin(k a/2)| — the linear small-k regime with slope c = a sqrt(k_s/m), and the cutoff at the band edge k = pi/a.
  - id: OBJ-07-5
    text: Measure the continuum limit — show that the low chain modes converge to omega_p -> p pi c / L with a relative error scaling as 1/N^2 on a log-log plot.
  - id: OBJ-07-6
    text: Explain why modal energies are separately conserved while site energies are exchanged, and use the distinction to choose the right picture for a given question.
---

# Normal modes: the right basis, the N-mass chain, and the road to the continuum

:::{note} A change of letter, once
Module 06 called the spring constant $k$, following `01-sho`. From here on the springs
between masses are $k_s$, because $k$ is about to mean a wavenumber and will mean that for
the rest of the course. Nothing physical changes; the letter is being handed over.
:::

(07-normal-modes-puzzle)=
## The puzzle: why a guitar string plays a note

Pluck a guitar string and you hear one note. That should be surprising.

A string is not one oscillator. It is an enormous number of them — think of it as a chain of
atoms, each tied to its neighbours, something like $10^{23}$ coupled masses. Module 06 showed
what happens when you couple *two* oscillators and start them arbitrarily: the energy sloshes
back and forth for ever and neither mass has a single frequency. Couple $10^{23}$ of them,
displace them into some arbitrary shape, and let go.

By that reasoning the string should produce a mess. It does not. It produces a definite pitch,
with a definite set of overtones above it, and it holds them until friction takes the sound
away.

:::{important} The question
A hundred coupled masses obey a hundred equations, every one of them referring to its
neighbours. Is there a point of view from which they are a hundred *independent* module-01
problems? And if so, what are the hundred notes?
:::

(07-normal-modes-predict)=
## Predict before you calculate

Commit to an answer for each before running anything.

1. A chain of 5 masses between two fixed walls. How many distinct frequencies does it have —
   fewer than 5, exactly 5, more than 5, or infinitely many?
2. You keep adding masses at the same spacing, making the chain longer. Does the *highest*
   frequency in the system grow without bound?
3. You pull the middle mass aside so the chain makes a triangle, and release it. Does the
   chain stay triangle-shaped as it moves, changing only in scale?
4. Module 06's two pendulums traded their energy completely, back and forth. Do the *modes*
   of a plucked chain trade energy with each other in the same way?

:::{note} Why we ask first
Question 2 separates a chain from a string: one of them has a fastest possible vibration and
the other does not. Question 4 is this module's misconception, and it is easy to get wrong
precisely *because* you understood module 06 — the sloshing there was real, and the question
is what it was between.
:::

(07-normal-modes-explore)=
## Explore the model

Three animations, all generated from the same `wavelab.coupled` code the laboratory runs. The
chains are drawn sideways — masses at fixed spacing, displaced up and down — while the model
itself is a one-dimensional line of masses sliding along their own axis. They are the same
equations, and the sideways picture is the one in which a mode looks like what it is.

:::{figure} ../media/chain-modes.mp4
:width: 100%

The five modes of a five-mass chain, in order of frequency from top to bottom. Each keeps a
fixed shape and repeats at a single rate for ever. Count the places where the chain stands
still: mode 1 has none, mode 2 has one, mode 5 has four. Every extra motionless point costs
frequency, and the ordering is never violated. All five panels run for the same length of
time, so what you are watching is genuinely their different rates — the top completes one and
a half cycles while the bottom completes six.
:::

:::{figure} ../media/chain-continuum.mp4
:width: 100%

Adding masses at fixed total length. Left: the slowest mode's shape, against the smooth
half-sine a string would have. At two masses it is a tent, 4.5% off in frequency; by fifty it
is 1.6 parts in $10^4$ off and the two curves cannot be told apart. Right: each chain drops
its modes as dots onto the dispersion curve, and as $N$ grows they crowd in until they trace
the sine they were always sitting on. The curve does not depend on $N$ at all. Only which
points of it a given chain is allowed to occupy does.
:::

:::{figure} ../media/chain-pluck.mp4
:width: 100%

A twenty-mass chain, plucked in the middle and released. Middle panel: the energy belonging
to each mass, with dashes at the starting values. It leaves them within a frame or two and
never settles. Right panel: the energy belonging to each *mode*, with the same dashes. Those
bars do not move at all, for the whole run — including the nineteen too short to see, which
hold their energy to about one part in $10^7$ of the total. The two panels are the same
trajectory, read two ways.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** $N$ equal point masses $m$ in a row, joined by identical springs of stiffness $k_s$ and by nothing else, with the ends fixed to rigid walls by default; free ends and a periodic ring are available as variants, and the solver itself accepts any symmetric mass and stiffness matrices at all. Observables: displacements, velocities, mode frequencies and shapes, and the energy attributed to each mass or to each mode.
- **Dynamics:** $M\ddot{\mathbf{x}} + K\mathbf{x} = 0$, solved exactly by modal decomposition — project onto the modes, evolve each as an independent module-01 oscillator, resum — and independently integrated by velocity Verlet as a cross-check that knows nothing about modes.
- **Boundary:** walls that never move and never absorb. A free or periodic chain instead carries a zero-frequency mode — the whole system translating — which is physics rather than a numerical failure.
- **Ensemble:** a single deterministic trajectory per choice of initial conditions; measurement noise, where added, is Gaussian, independent and seeded.
- **Ignored:** damping, driving, spring masses, nonlinearity, the compliance of the walls, and the distinction between transverse and longitudinal motion — one polarization, one dimension.
- **Valid when:** springs are linear and displacements small; $M$ is symmetric positive definite and $K$ symmetric positive semi-definite; and continuum statements are made only for modes with $p \ll N$.
- **Failure modes:** matrices that are not symmetric; continuum formulas used near the band edge, where they are wrong by tens of percent rather than by a little; amplitudes large enough for nonlinearity to matter, at which point the modes stop being independent and the whole construction fails at once.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 07 — normal modes](/lite/lab/index.html?path=en/labs/07-normal-modes.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/07-normal-modes.ipynb`.
:::

Run the laboratory now, then come back. Four things are worth doing before you read on:

- Solve module 06's pair with the general machinery and check it against the answer you got
  from a determinant. It should agree to the last bit.
- Look at the five modes of a five-mass chain and count nodes before you look at frequencies.
- Pluck a twenty-mass chain and watch the two sets of energy bars. One set moves.
- Push $N$ from 2 to 100 and watch the lowest frequency stop changing.

(07-normal-modes-derive)=
## Derive the result

### The eigenvalue problem, and why it always has an answer

Module 06 assumed a single-frequency motion, $\mathbf{x} = \mathbf{a}\cos\omega t$, and found
that it required

$$
K\mathbf{a} = \omega^2 M \mathbf{a} .
$$

For two masses this is a quadratic and you solve it with a pen. For twenty it is a degree-20
polynomial, and nobody solves those. What saves the situation is that we do not need to: the
structure of the problem guarantees the answer exists and has exactly the properties the
physics needs.

:::{admonition} The spectral theorem for a mechanical system
:class: theorem
If $M$ is symmetric positive definite and $K$ is symmetric positive semi-definite — which is
what "masses are positive" and "the potential energy is a minimum at rest" mean written as
matrices — then $K\mathbf{a} = \omega^2 M\mathbf{a}$ has exactly $N$ solutions. Every
$\omega_p^2$ is real and non-negative, so every frequency is real. The shapes can be chosen
$M$-orthonormal,

$$
\mathbf{a}_p^{\mathsf T} M \mathbf{a}_q = \delta_{pq},
$$

and they span everything: **every** motion of the system is a sum of them.

Real frequencies are not a technicality. A complex $\omega$ would mean a motion growing
exponentially out of a system with no energy source, and it is the symmetry of $K$ — which
follows from the springs storing a potential energy rather than doing something stranger —
that rules it out.
:::

The route to the proof is also the route to the computation. Since $M$ is positive definite it
has a Cholesky factorization $M = LL^{\mathsf T}$. Substitute $\mathbf{a} = L^{-\mathsf T}\mathbf{b}$:

$$
K L^{-\mathsf T}\mathbf{b} = \omega^2 L L^{\mathsf T} L^{-\mathsf T}\mathbf{b}
\qquad\Longrightarrow\qquad
\left(L^{-1} K L^{-\mathsf T}\right)\mathbf{b} = \omega^2 \mathbf{b} .
$$

The matrix in brackets is symmetric, because $K$ is. So the generalized problem has become an
*ordinary* eigenvalue problem for a symmetric matrix — which is the one case where all of this
is guaranteed, and the case fast library routines are written for. That is why
`normal_mode_solve` calls `numpy.linalg.eigh`, the routine for symmetric matrices, and not the
general `eig`: `eig` would return complex numbers with tiny imaginary parts and leave you to
decide whether they mean anything.

For $2\times 2$ you can check the whole theorem by hand — it is module 06's determinant. Beyond
that we verify rather than prove, and the verification is real: the solver agrees with the
chain's closed form to $3.5\times 10^{-15}$ at $N = 100$.

### Modal evolution: N independent module-01 problems

Once the shapes are in hand, arbitrary motion costs nothing more. Write the state as a
combination of them, $\mathbf{x}(t) = \sum_p \mathbf{a}_p\, q_p(t)$. The $M$-orthonormality
extracts the coefficients:

$$
q_p(0) = \mathbf{a}_p^{\mathsf T} M \mathbf{x}(0),
\qquad
\dot q_p(0) = \mathbf{a}_p^{\mathsf T} M \dot{\mathbf{x}}(0) .
$$

Note that the projection carries $M$ with it. This is module 03's expansion in an orthogonal
basis, in $N$ dimensions instead of infinitely many, with the mass matrix supplying the inner
product — and the reason the inner product must be that one is that it is the one in which the
kinetic energy is a plain sum of squares.

Each $q_p$ then obeys $\ddot q_p + \omega_p^2 q_p = 0$: a module-01 oscillator, alone. So

$$
x_j(t) = \sum_{p=1}^{N} a_p(j)
\left[\, q_p(0)\cos\omega_p t + \frac{\dot q_p(0)}{\omega_p}\sin\omega_p t \,\right] .
$$

That is the answer to the puzzle's second sentence. There *is* a point of view in which a
hundred coupled equations are a hundred independent ones, and the change of coordinates that
reaches it is the projection above. Nothing is approximated and nothing accumulates: the state
after a million seconds costs exactly what the state after one second costs.

A zero mode is the one case needing care. If $\omega_p = 0$ the cosine formula divides by zero;
take the limit and the mode drifts linearly, $q_p(0) + \dot q_p(0)\,t$ — a free chain sliding
along at constant speed, which is momentum conservation wearing an eigenvalue's clothes.

### The chain, solved

Now specialise. $N$ equal masses, identical springs $k_s$, walls at both ends. Mass $j$ is
pulled by its two neighbours and nothing else:

$$
m\ddot x_j = k_s\left(x_{j+1} - x_j\right) - k_s\left(x_j - x_{j-1}\right)
= k_s\left(x_{j+1} - 2x_j + x_{j-1}\right),
$$

with $x_0 = x_{N+1} = 0$ standing for the walls. In matrix form $K$ is *tridiagonal*: $2k_s$
down the diagonal, $-k_s$ next to it, zero everywhere else. A mass only feels what it is tied
to, and the width of the band in $K$ is the range of the interaction.

Hold on to the combination $x_{j+1} - 2x_j + x_{j-1}$. It is a second difference, and it is
where this module ends up.

Substituting a single-frequency motion $x_j = a(j)\cos\omega t$ gives the recursion

$$
-m\omega^2 a(j) = k_s\left[\,a(j+1) - 2a(j) + a(j-1)\,\right] .
$$

Try $a_p(j) = \sin\!\left(\dfrac{p\pi j}{N+1}\right)$. The end conditions are satisfied for
free: $\sin 0 = 0$ at $j = 0$, and $\sin(p\pi) = 0$ at $j = N+1$, for every integer $p$. In
the interior, the sine addition formula collapses the bracket to a multiple of $a_p(j)$
itself,

$$
a_p(j+1) + a_p(j-1) = 2\cos\!\left(\frac{p\pi}{N+1}\right) a_p(j),
$$

so the recursion holds for every $j$ at once, with

$$
m\omega^2 = 2k_s\left[1 - \cos\!\left(\frac{p\pi}{N+1}\right)\right]
= 4k_s\sin^2\!\left(\frac{p\pi}{2(N+1)}\right) .
$$

$$
\boxed{\;
\omega_p = 2\sqrt{\frac{k_s}{m}}\;
\sin\!\left(\frac{p\pi}{2(N+1)}\right),
\qquad
a_p(j) \propto \sin\!\left(\frac{p\pi j}{N+1}\right),
\qquad p = 1, \dots, N .\;}
$$

Three answers fall out immediately. There are **exactly $N$** distinct modes, because $p$ and
$p + 2(N+1)$ give the same displacements at every mass and $p = N+1$ gives zero everywhere —
prediction 1, and the count is the number of masses, not a coincidence. The shapes are sine
waves *sampled at the masses*, so mode $p$ has $p-1$ interior nodes and the ordering by nodes
and the ordering by frequency are the same ordering. And the frequencies are **bounded**: the
sine cannot exceed one, so

$$
\omega_{\max} < 2\sqrt{k_s/m}
$$

for a chain of any length whatsoever — prediction 2, and the answer is no.

### The dispersion relation

The sampled-sine shape invites a rewrite. Put the masses at positions $x = ja$ with spacing
$a$, and write the mode as a travelling wave evaluated at those positions,

$$
x_j \propto \Real\!\left[e^{\ii(kja - \omega t)}\right],
\qquad
k_p = \frac{p\pi}{(N+1)a} .
$$

The recursion is then satisfied when

$$
\boxed{\;\omega(k) = 2\sqrt{\frac{k_s}{m}}\;\left|\sin\!\left(\frac{ka}{2}\right)\right|\;}
$$

which is the same formula as before with $p\pi/(N+1)$ renamed $ka$. Renaming it is the point.
$\omega_p$ is a statement about one chain of one length; $\omega(k)$ is a statement about the
*medium*, and every chain made of these masses and these springs obeys it whatever its length.
Chains of 5, 20 and 100 masses put their frequencies on this curve to a part in $10^{16}$;
what differs is only which points of it they are allowed to occupy.

This is a **dispersion relation**, the first of many. Two features of it will recur in every
later one.

**Small $ka$: straight, and therefore a wave.** For $ka \ll 1$ the sine is its own argument and

$$
\omega \approx \left(a\sqrt{k_s/m}\right) k = c\,k .
$$

Frequency strictly proportional to wavenumber means every long wave travels at the same speed
$c$, so a pulse made of them holds its shape as it goes. That is what it takes to be a wave in
the ordinary sense, and it is why long waves on a chain behave like waves on a string.

**Large $ka$: flat, and therefore a ceiling.** As $k \to \pi/a$ the curve levels off at
$2\sqrt{k_s/m}$. At the band edge, neighbouring masses move in exact antiphase — the most
violent thing a chain of springs can do — and there is no arrangement faster. This is a
**cutoff**, and it exists only because the medium is made of discrete pieces. A continuous
string has no such limit, and the difference is measurable.

Beyond $k = \pi/a$ nothing new happens: $k$ and $k + 2\pi/a$ displace the masses identically,
so the chain cannot tell them apart and the formula simply repeats. A row of discrete samplers
cannot distinguish a short wave from a long one — which is aliasing, arriving here a course
before module 04's sampling theorem needs it again.

### The continuum limit, and where it stops working

Hold the total length $L = (N+1)a$ fixed and let $N$ grow. The wavenumbers $k_p = p\pi/L$ then
do not move at all, and the low modes settle onto

$$
\omega_p \;\longrightarrow\; \omega_p^{\infty} = \frac{p\pi c}{L},
$$

evenly spaced, exactly proportional to $p$. That is what a musical instrument requires: a
fundamental with overtones at whole-number multiples of it, which is what the ear hears as one
pitch rather than as a chord.

How fast, and how far? Expand the sine. With $x = p\pi/(2(N+1))$ and
$\sin x \approx x - x^3/6$,

$$
\frac{\omega_p}{\omega_p^{\infty}} = \frac{\sin x}{x} \approx 1 - \frac{x^2}{6}
\qquad\Longrightarrow\qquad
\frac{\omega_p^{\infty} - \omega_p}{\omega_p^{\infty}} \approx
\frac{(p\pi)^2}{24\,(N+1)^2} .
$$

:::{admonition} A chain is a string, for the modes near the bottom
:class: approximation
The relative error falls as $1/N^2$ and grows as $p^2$. Both halves matter, and the second is
the one that is usually forgotten: the continuum is reached from the bottom of the band
upwards. At $N = 100$ the lowest mode is right to $4\times 10^{-5}$, the sixteenth to
$1\times 10^{-2}$ — 250 times worse for 16 times the mode number — and the highest mode of all
sits **36% below** the string frequency it is supposedly approaching, and stays there however
large $N$ becomes.

So "$N$ discrete masses represent a continuous string" is a claim with a stated domain,
$p \ll N$, and not a claim about the system as a whole. Near the band edge the discreteness is
the whole story, which is exactly the regime `54-photonic-crystals` is built on.
:::

Notice what the error does *not* depend on. The ratio $\sin x / x$ carries no mass and no
stiffness: a chain of any material converges at the same rate, which is the sign that the
statement is about discretisation rather than about springs.

### Where this module stops

Return to the second difference. With the masses at spacing $a$, write $\mu = m/a$ for mass
per unit length and $T = k_s a$ for tension, and the equation of motion for mass $j$ reads

$$
\mu\,\ddot x_j = T\,\frac{x_{j+1} - 2x_j + x_{j-1}}{a^2} .
$$

The fraction on the right is the standard finite-difference approximation to a second
derivative. Let $a \to 0$ holding $\mu$ and $T$ fixed, and it becomes one:

$$
\mu\,\frac{\partial^2 \psi}{\partial t^2} = T\,\frac{\partial^2 \psi}{\partial x^2} .
$$

That is the wave equation, and this module stops here — at the point where the step is
visible and has not yet been taken. [Module 08](../waves/08-wave-equation.md) takes it, and
starts by rediscovering $c = \sqrt{T/\mu} = a\sqrt{k_s/m}$, which you have already measured.

(07-normal-modes-verify)=
## Verify computationally

Each check below is also a test in the project's suite, so these claims cannot silently rot.

**1. The closed form, against the general solver.** `normal_mode_solve` is given the chain's
matrices and knows nothing about sines; `chain_mode_frequencies` evaluates the formula above
and knows nothing about matrices. They agree to $3.5\times10^{-15}$ relative at $N = 100$, and
at every size from one mass upwards. The single fixed mass is included deliberately: it has
*two* springs on it, so it runs at $\sqrt{2k_s/m}$, and a chain builder that writes $2k_s$ down
the diagonal without understanding why gets every other size right and that one wrong.

Mode shapes agree up to a sign. Eigenvectors are only defined up to one, and a mode shape
reversed is the same motion released half a period later.

**2. The falsifying experiment.** A twenty-mass chain is started and integrated with velocity
Verlet, which has no notion of a mode; the modal energies are computed afterwards by
projection. The laboratory starts it by plucking; the test suite starts it from a seeded
random state, so that every mode carries some energy and a claim about each mode separately
means something.

:::{admonition} What the modes do while the masses slosh
:class: numerical-observation
Every one of the twenty modal energies is constant to $2.5\times 10^{-4}$ of its own value —
and that residual is the integrator's, falling fourfold when the step is halved, not the
physics'. Over the same trajectory the share of energy held by a single mass swings across a
third of the total.

Run four times as long and the modal bound does not grow. That is the symplectic integrator's
guarantee, and checking it is what distinguishes "the modes do not exchange" from "the
exchange is too slow to see yet".

The plucked version gives the same verdict with different numbers — modal energies steady to
$10^{-6}$ of the total against a site share swinging by 17% — and one extra fact. A symmetric
pluck is orthogonal to every even mode, so twelve of the twenty hold *exactly* zero. Zero
stays zero, but asking how much a mode holding $10^{-31}$ of the energy has drifted *relative
to itself* returns a large meaningless number, which is why the per-mode claim above is made
on a state that excites everything.

Module 06's pendulums did trade energy completely — between *sites*. Between modes, nothing is
traded, then or now.
:::

**3. Modal evolution against integration.** `evolve` builds the motion from the eigensolution
and never steps anything; `simulate_coupled` steps and never diagonalizes. Started from seeded
random states on a twelve-mass chain, they agree to $1.7\times 10^{-4}$ of the amplitude over
three periods of the slowest mode — and that gap is the *integrator's* error, since `evolve`
has none to accumulate. At $t = 0$ the round trip through the modes and back is exact to
$10^{-14}$.

**4. The convergence experiment.** The chain's low-mode frequencies are compared with
`chain_continuum_frequencies` over $N = 10$ to $160$ and the error is fitted on log-log axes.

:::{admonition} The measured order
:class: numerical-observation
The fitted convergence order is **2.000, 1.999 and 1.997** for the first three modes, against
the predicted 2. The measured errors match $(p\pi)^2/(24(N+1)^2)$ to better than 2% — the
prediction is not merely of the right order, it is right in its coefficient.

The refinement parameter is the number of springs, $N+1$, and not $N$. Fit against $N$ and the
answer comes out 1.95, which is the same physics with a mislabelled axis. The mesh has $N+1$
cells because $N+1$ springs span the length.
:::

Separately, the error's growth with mode number is fitted at $N = 100$: exponent **1.999**
against the predicted $p^2$.

**5. The dispersion collapse.** Chains of 5, 20 and 100 masses land on
$\omega(k) = 2\sqrt{k_s/m}\,|\sin(ka/2)|$ to $10^{-16}$. The small-$k$ slope falls short of
$c = a\sqrt{k_s/m}$ by exactly $(\pi/(N+1))^2/24$ — 1.1% at $N = 5$, $4\times 10^{-5}$ at
$N = 100$ — which is the same expansion the continuum limit runs on, showing up in a second
measurement.

**6. Free ends and rings.** Remove the walls and one frequency drops to zero, with a uniform
shape: the chain translating. Its computed value is $8.5\times 10^{-8}$ at $N=5$ and exactly
$0$ at $N=20$, which is why a zero mode is always tested against a tolerance and never against
equality — a square root turns an eigenvalue's rounding error into a much larger relative one.
Join the ends into a ring and the modes above the zero come in *exactly* equal pairs.

(07-normal-modes-transfer)=
## Transfer the idea

:::{admonition} Mechanical modes, optical modes
:class: important
This is the motif to carry forward. A laser cavity is two mirrors with light between them, and
the light can only sustain those field patterns that fit the mirrors — a discrete set, each
with its own frequency, each keeping its shape. An optical fibre supports a discrete set of
guided modes and no others. In both cases the mathematics is this module's: a linear system
with boundary conditions, an eigenvalue problem, a countable set of shapes that persist, and
an arbitrary excitation written as a sum over them.

The chain is the version you can watch. `44-resonators` does cavity modes, `46-waveguides`
does guided modes, and neither introduces any idea that is not on this page.
:::

- **The wave equation.** [Module 08](../waves/08-wave-equation.md) starts where the derivation
  above stops, with the second difference becoming a second derivative. Everything from Part III
  onwards is a continuous medium, and this is the last time you can count the pieces.
- **Standing waves.** `11-standing-waves` finds the string's shapes as a boundary-value problem
  and gets $\sin(p\pi x/L)$ — the $N \to \infty$ limit of this page's $a_p(j)$, with the same
  integer $p$ counting the same nodes.
- **Dispersion in general.** `13-dispersion` takes $\omega(k)$ as a subject in its own right,
  where a curved relation means a pulse spreads as it travels. The lattice sine is its
  reference example, and you have already plotted it.
- **Phonons.** The chain's modes, with their energies quantized in units of $\hbar\omega_p$,
  are what a solid-state course calls phonons, and this $\omega(k)$ is a real one-dimensional
  phonon band. Heat capacity, thermal conductivity and the speed of sound in a crystal are all
  read off curves of this shape.
- **Quantum mechanics.** `01-sho`'s advanced section trailed "diagonalising the Hamiltonian".
  This is that operation, in the setting where you can see what it means: coupled quantities,
  an eigenproblem, a basis in which everything is independent.

:::{admonition} Dispersion relation
:class: definition
A **dispersion relation** is the function $\omega(k)$ giving the oscillation frequency of a
wave of wavenumber $k$ in a given medium. It is a property of the medium, not of any
particular system built from it: boundaries decide which $k$ are allowed, and the relation
decides what frequency each of them carries.

Where $\omega(k)$ is a straight line through the origin, all wavelengths travel at the same
speed $\omega/k$ and a pulse keeps its shape — the medium is *non-dispersive*. Where the line
bends, they do not and it does not. The chain is non-dispersive for $ka \ll 1$ and strongly
dispersive as $k$ approaches the band edge $\pi/a$, where $\omega(k)$ flattens out at the
**cutoff frequency** $2\sqrt{k_s/m}$ and the chain can carry nothing faster.
:::

(07-normal-modes-quiz)=
## Check your understanding

```{include} ../_generated/quiz-07-normal-modes.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](07-normal-modes-problems.md).

(07-normal-modes-explain)=
## Explain it in your own words

Answer in a few sentences each. No number will save you.

1. Explain to someone who has done module 06 but not this one why a plucked guitar string
   sounds like a note rather than like noise. Your explanation must use the words "mode" and
   "independent", and must say what the string's $10^{23}$ coupled equations have to do with
   the one pitch you hear.
2. A chain of 50 masses and a chain of 5 masses, same masses and same springs. Which
   statements about them are the same and which are different? Answer in terms of $\omega(k)$
   and of which $k$ each chain is allowed.
3. Why does the highest frequency of a chain stop growing as masses are added, when the
   highest frequency of a string does not? Answer without algebra, by describing what the
   fastest possible motion of a chain looks like.
4. Site energies are not conserved; modal energies are. Both statements describe the same
   motion. Say how that is possible, and then give one question about a plucked chain that the
   site picture answers faster and one that the mode picture answers faster.

(07-normal-modes-advanced)=
## Advanced: symmetry, degeneracy, defects, and a computation that failed usefully

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section.
:::

**Degeneracy comes from symmetry.** Join the chain's ends into a ring and its modes above the
zero come in exactly equal-frequency pairs — verified to $10^{-12}$, which is not a numerical
accident but an exact statement. A ring has no preferred direction, so a wave running one way
round and the same wave running the other way must cost exactly the same, and the two are
different motions. Wherever two modes share a frequency, look for the symmetry that makes them
interchangeable; the rule holds from molecules to atomic orbitals.

**Breaking it lifts the degeneracy.** Make one of six ring masses 10% heavier and the pairs
come apart: $(4.000, 4.000)\to(3.935, 4.000)$ and $(6.928, 6.928)\to(6.818, 6.928)$. Only one
partner of each pair moves, and which one is not arbitrary — the perturbed mass sits at a node
of the mode that stays put, so that mode does not notice the change at all. Sweep the
perturbation through zero and you trace module 06's avoided crossing again, now as the
splitting of a degenerate pair rather than the repulsion of two tuned oscillators. This is
mode splitting in a ring resonator, and `44-resonators` returns to it with light in the ring.

**A defect makes a mode that is nowhere else.** Replace the middle mass of a 41-chain with a
lighter one, $0.3m$. A mode appears at $11.2$ rad/s — *above* the band top of $8.0$ rad/s,
where the perfect chain has nothing at all — and its shape is not a sine wave. Its amplitude
falls by a factor of $0.177$ per mass on either side of the defect, so it is confined within a
handful of masses of the flaw and is exactly zero at the edges to $10^{-15}$.

A light mass can oscillate faster than the band permits, so no travelling wave can carry the
motion away and it has nowhere to go but to stay put. That is the whole mechanism of a defect
cavity: `54-photonic-crystals` builds a lattice with a band of forbidden frequencies, puts a
deliberate flaw in it, and traps light in the flaw for exactly this reason.

**Fermi, Pasta, Ulam and Tsingou.** Everything above assumes the springs are linear. In 1953,
on the MANIAC computer at Los Alamos, four researchers put a weak nonlinear term into a chain
of 64 masses and started it in its lowest mode. They expected the nonlinearity to leak energy
between modes until it was shared out evenly — thermalization, which is what statistical
mechanics says should happen and what everyone assumed a computer would confirm in an
afternoon.

:::{admonition} It did not thermalize
:class: open-question
The energy moved into the higher modes, then came back. After a long time almost all of it had
returned to mode 1 — a near-recurrence of the initial state, repeating. The result was
sufficiently unwelcome that the paper was left as a Los Alamos report for years.

The explanation, when it came, connected the chain to solitons and to integrable systems, and
the question of exactly when a nonlinear system does and does not reach equilibrium remains
open. The episode is also usually given as the first genuine numerical experiment: a
computation run not to get a number but to find out what a system does, and answering
something nobody had asked.

Mary Tsingou wrote the MANIAC code and was not among the named authors of the report; the
result is increasingly cited as Fermi–Pasta–Ulam–Tsingou.
:::
