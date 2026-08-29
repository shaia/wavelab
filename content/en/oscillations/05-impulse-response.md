---
title: "Impulse response: the oscillator as a linear system"
short_title: 05 · Impulse response
module: 05-impulse-response
objectives:
  - id: OBJ-05-1
    text: Define the impulse response G(t) as the motion after a unit impulse, G(t) = e^(-gamma t/2) sin(omega_d t) / (m omega_d) for t >= 0 and zero before, and account for each feature — starts at zero, leaves at slope 1/m, rings at omega_d, decays at gamma/2.
  - id: OBJ-05-2
    text: Predict the response to an arbitrary force as the convolution x(t) = integral up to t of G(t - t') F(t') dt', read it as a superposition of kicks, and evaluate it numerically for steps, ramps and bursts.
  - id: OBJ-05-3
    text: State that the transform of G is the complex frequency response H(omega) = (1/m) / (omega0^2 - omega^2 + i gamma omega), connect it to module 02's steady-state amplitude, and use x-hat = H F-hat.
  - id: OBJ-05-4
    text: Use causality — G = 0 for t < 0 — to constrain any response, so that nothing moves before the force starts and x(t) cannot depend on F(t') for any t' > t.
  - id: OBJ-05-5
    text: Translate the oscillator into the series RLC circuit via m <-> L, b <-> R, k <-> 1/C, with x <-> q and F <-> V, carrying G, Q and H(omega) across unchanged.
---

# Impulse response: the oscillator as a linear system

(05-impulse-response-puzzle)=
## The puzzle: the bell that ignores the hammer

Strike a bell with a wooden mallet and it sounds soft; with a steel hammer, bright and loud;
with a felt beater, muffled. Three obviously different sounds. Now hum along with each one.
The pitch is identical every time.

You can hit it harder, softer, faster, in a different place, with a different material — and
you cannot make the bell sing a different note. Something about the strike is being thrown
away, and something about the bell is deciding what is left.

:::{important} The question
Why can no mallet choose the note? And — the useful half — if the bell's answer to a hammer
blow is so completely its own, how much can an engineer learn from a single strike? Module 02
needed a whole frequency sweep to measure a resonance curve. Can one hit do it?
:::

The answer to the second question is yes, exactly and in one line, and by the end of this
module you will have done it on data.

(05-impulse-response-predict)=
## Predict before you calculate

Commit to an answer for each *before* running anything. Write them down.

1. You kick a hanging mass twice, the two kicks one full period apart. Compared with a single
   kick, is the later ringing bigger, cancelled, or unchanged? What if the second kick lands
   half a period after the first?
2. A constant force is switched on and left on. Does the mass glide smoothly to its new
   equilibrium $F_0/k$, or overshoot and ring on the way?
3. Can the mass move *before* the kick — can $x(t)$ depend on the force at times later than
   $t$? If your answer is no, what exactly forbids it?
4. You drive at $\wnat$ in a burst of 3 cycles, then in a burst of 30 cycles. Ten times the
   drive: roughly how many times the response?

:::{note} Why we ask first
Question 2 is the module's misconception, and most people answer it wrongly the first time:
a featureless force does *not* produce a featureless motion. Question 4 catches nearly
everyone in the other direction — the answer is not ten, and it is not far from two.
:::

(05-impulse-response-explore)=
## Explore the model

Two animations, both generated from the same `wavelab.oscillators` code the laboratory runs.

:::{figure} ../media/impulse-convolution.mp4
:width: 100%

Kicks arriving at random times, each with its own strength and sign (top), and what the
oscillator does about it (bottom). Every kick spawns one faint ringdown, always the same
shape, always beginning exactly where its own arrow lands and never earlier. The bold curve
is nothing but their sum. Watch the third and fourth kicks partly *cancel* what the second
one built: superposition is addition, and addition includes subtraction.
:::

:::{figure} ../media/impulse-step-overshoot.mp4
:width: 100%

A constant force switched on at $t = 0$ and never changed again (top), and four oscillators
answering it (bottom). The force has exactly one feature in its whole history; the responses
ring for twenty seconds. All four end at the same place, $F_0/k$ — the dashed line — so the
only difference between them is the route. Overshoot grows with $Q$: none at all when the
damping is critical, and 85% above the final value at $Q = 10$.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** module 02's mass, spring and damper, viewed now as a *map* from a force history to a displacement history; the observables are input–output pairs and their spectra rather than any single trajectory.
- **Dynamics:** the same equation of motion $m\ddot{x} + b\dot{x} + kx = F(t)$, with solutions represented as the convolution $x = G * F$ and evaluated either that way or by direct integration.
- **Boundary:** at rest before the force begins — the causal condition, and what selects this Green function out of the two the equation admits; the environment is module 02's featureless sink.
- **Ensemble:** a single deterministic input–output pair per force history; measurement noise, where added, is Gaussian, independent and seeded.
- **Ignored:** the microscopic mechanism behind $b$, and every nonlinearity — superposition of kicks *is* linearity, so this specification has no room for a spring that stiffens.
- **Valid when:** the response is linear, the force is bounded and starts at a finite time, and the sampling step lies well below both $2\pi/\omega_d$ and the fastest feature of the force.
- **Failure modes:** nonlinear springs, where kicks stop superposing and the whole method collapses; discrete convolution of a force with content above the Nyquist frequency; and naive deconvolution, which amplifies noise without limit wherever the response is small.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 05 — impulse response and convolution](/lite/lab/index.html?path=en/labs/05-impulse-response.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/05-impulse-response.ipynb`.
:::

Run the laboratory now, then come back. Three things are worth doing before you read on:

- Drop two kicks on the time axis and slide the second one around. Find the spacings that
  build the ringing up and the spacings that nearly kill it, and check them against the
  period you can measure from a single kick.
- Take one ringdown, transform it, and lay module 02's swept response curve on top. Nothing
  in the sweep was used to produce the ringdown.
- Turn the drive frequency of a burst slightly off resonance and watch the response fall
  away. The shape you are tracing out with a stopwatch is a Lorentzian.

(05-impulse-response-derive)=
## Derive the result

**A kick sets a velocity.** Apply a force that is enormous and brief — total impulse
$J = \int F\,dt$, delivered in a time short compared with everything else in the problem.
Integrate the equation of motion across that instant. The term $\int m\ddot{x}\,dt = m\Delta v$
survives; $\int b\dot{x}\,dt$ and $\int kx\,dt$ do not, because $x$ and $\dot{x}$ are bounded
and the interval is vanishing. So

$$
m\,\Delta v = J
\qquad\Longrightarrow\qquad
x(0^+) = 0,
\qquad
\dot{x}(0^+) = \frac{J}{m} .
$$

A kick moves nothing and changes the velocity. Everything after the kick is therefore *free*
decay — module 02's undriven problem, with a particular starting condition. Define the
**impulse response** $G(t)$ as the motion after a *unit* impulse, $J = 1$:

$$
G(t) =
\begin{cases}
\dfrac{e^{-\gamma t/2}}{m\,\omega_d}\,\sin\omega_d t, & t \ge 0, \\[2ex]
0, & t < 0 .
\end{cases}
$$

Every feature of that expression is one of the four things you already know. It starts at
zero, because a kick does not teleport the mass. It leaves the origin at slope $1/m$, because
that is the velocity the kick supplied. It oscillates at $\omega_d$ — *the bell's own
frequency, not the hammer's* — and it decays at $\gamma/2$, so it is still audible after about
$Q/\pi$ cycles. There is the answer to the bell: the mallet sets the amplitude and only the
amplitude, and the pitch was never its to choose.

:::{admonition} Nothing happens before the kick
:class: model-assumption
The second line, $G = 0$ for $t < 0$, is not algebra. The differential equation is perfectly
happy with a solution that rings *backwards* in time, growing out of nothing before the kick
and stopping dead at it, and that solution is discarded on physical grounds alone. Causality
is an assumption imported from outside the mathematics — the boxed one of this module — and
every constraint in the rest of the page rests on it.
:::

**Any force is a train of kicks.** Chop an arbitrary $F(t)$ into slices of width $\Delta t$.
The slice at $t'$ delivers an impulse $F(t')\,\Delta t$, and — this is the whole of linearity
and time invariance — the oscillator answers it exactly as it answers any other kick, only
scaled and shifted: $G(t - t')\,F(t')\,\Delta t$. Add the answers:

$$
x(t) = \int_{-\infty}^{\,t} G(t - t')\,F(t')\,dt' \;\equiv\; (G * F)(t) .
$$

The upper limit is $t$ and not $+\infty$, and it is causality that put it there: $G(t - t')$
vanishes for $t' > t$, so the future of the force cannot reach the present of the motion. This
is the bold curve in the first animation, and it is the answer to prediction 3.

Two kicks now become arithmetic. Kick twice, a time $\tau$ apart, and the later ringing is the
sum of two decaying sinusoids that differ in phase by $\omega_d\tau$ and in size by
$e^{-\gamma\tau/2}$. Space them one period apart and they are in phase, giving
$1 + e^{-\pi/Q}$ times a single kick — $1.73$ at $Q = 10$, not $2$, because the first has
faded a little by the time the second arrives. Space them *half* a period apart and they are
in antiphase, leaving $1 - e^{-\pi/2Q}$, which is $0.15$ at $Q = 10$. Nearly cancelled, and
not exactly cancelled: perfect destruction would need two equal amplitudes, and damping has
already shrunk the first.

**The frequency response.** Transform $G$ with the course's forward kernel, $e^{-\ii\omega t}$.
Because $G$ vanishes for $t < 0$ the integral is one-sided — module 04's exponential pair,
with a sine in front of it:

$$
\hat{G}(\omega) = \int_{0}^{\infty} \frac{e^{-\gamma t/2}\sin\omega_d t}{m\,\omega_d}\,
e^{-\ii\omega t}\,dt
= \frac{1/m}{\wnat^2 - \omega^2 + \ii\gamma\omega} .
$$

Now compare that with module 02, which sweeps a drive and measures a complex amplitude
$X(\omega) = (F_0/m)/(\wnat^2 - \omega^2 - \ii\gamma\omega)$. The two are the same function
with the sign of one term flipped:

$$
X(\omega) = F_0\,\hat{G}(\omega)^{*} = F_0\,\hat{G}(-\omega) .
$$

:::{admonition} The kick and the sweep are one measurement
:class: theorem
The transform of the impulse response is the frequency response. A single ringdown therefore
contains module 02's entire resonance curve — every amplitude and every phase lag, at every
frequency at once — because one kick contains every frequency at once. This is why an engineer
tests a structure with a hammer instead of a shaker, and it is the reason the laboratory below
can measure $Q$ twice from one record and check the answers against each other.
:::

The conjugate is not a blemish to be tidied away; it is module 00's negative-frequency thread
arriving for the last time. The course's phasor $Ae^{-\ii\varphi}$ rides a time factor
$e^{-\ii\omega t}$, which under the forward kernel lives in the *negative*-frequency half of
the spectrum. So the sweep's arrow at $+\omega$ is the spectrum's value at $-\omega$, and
$\hat{G}(-\omega) = \hat{G}(\omega)^{*}$ because $G$ is real. Get this sign backwards and
every phase lag in the module reverses — the mass leads the force instead of trailing it.

**Multiply instead of convolving.** The convolution theorem, module 04's, turns the integral
into a product:

$$
\hat{x}(\omega) = \hat{G}(\omega)\,\hat{F}(\omega) .
$$

Three curves and one multiplication: what you push with, what the system will let through, and
what you get. It is the picture module 04 drew for signals, now with a *physical* system in
the middle, and it will be the picture module `40-psf-otf` draws for images.

**A step, worked out.** Switch on a constant force $F_0$ at $t = 0$ and convolve. The
particular solution is the new equilibrium $F_0/k$, and the homogeneous part is whatever
carries the mass there from the old one:

$$
x(t) = \frac{F_0}{k}\left[1 - e^{-\gamma t/2}\left(\cos\omega_d t
+ \frac{\gamma}{2\omega_d}\sin\omega_d t\right)\right],
\qquad t \ge 0 .
$$

Read the answer to prediction 2 off it. The bracket does not climb monotonically to $1$; it
overshoots and rings, at $\omega_d$, dying over $2/\gamma$ — 85% past the target at $Q = 10$,
44% at $Q = 2$, and only at critical damping not at all. **A featureless force does not
produce a featureless motion.** The oscillator answers with its own frequency no matter what
you ask it, which is the same lesson the bell taught, and this time there was not even a bang
to blame it on.

Prediction 4 falls out of the same reasoning. Driving on resonance, the response builds as
$1 - e^{-\gamma t/2}$ and saturates at $Q F_0/k$ after roughly $Q$ cycles. Three cycles at
$Q = 10$ reaches $1.45$ in units of $F_0/k$; thirty cycles reaches $2.50$, the saturated
value. Ten times the drive bought $1.7$ times the response, because after the first $Q$
cycles the oscillator is losing energy exactly as fast as the drive supplies it.

**The dictionary.** Write Kirchhoff's loop rule for a series RLC circuit driven by $V(t)$,
with $q$ the charge on the capacitor:

$$
L\ddot{q} + R\dot{q} + \frac{q}{C} = V(t) .
$$

That is this module's equation with the symbols renamed. Under

$$
m \leftrightarrow L,
\qquad
b \leftrightarrow R,
\qquad
k \leftrightarrow \frac{1}{C},
\qquad
x \leftrightarrow q,
\qquad
F \leftrightarrow V,
$$

every result on this page transfers untouched: the same $G$, the same
$Q = \sqrt{L/C}\,/\,R$, the same Lorentzian. Nothing was derived about springs. What was
derived was the behaviour of *any* system obeying a linear second-order equation, and the
mass on the spring was a convenient place to watch it happen.

(05-impulse-response-verify)=
## Verify computationally

Each check below is also a test in the project's suite, so these claims cannot silently rot.

**1. Convolution against integration.** `convolution_response` builds the motion by summing
kicks; `simulate_forced` steps the differential equation forward in time and knows nothing
about Green functions. Pointed at the same step, ramp, burst and noise records they agree,
and the disagreement falls fourfold each time the step is halved — the second-order
convergence each method separately claims.

**2. The resonance curve from one kick.** `fourier.spectrum` is applied to a computed
ringdown and the result laid over module 02's `steady_state_response`, conjugated.

:::{admonition} What the measured bridge costs
:class: numerical-observation
The two curves agree to about one part in $10^5$ — but *not* because the arithmetic is exact,
and the way it fails is worth knowing. Two errors sit underneath. One is the grid, and falls
fourfold when the step is halved. The other is the record: a ringdown that has not finished
ringing is wrapped back onto its own start by the transform's periodic extension. At $Q = 20$,
holding the step fixed and doubling the record, the error tracks the surviving tail almost
exactly — $2.9\times10^{-4}$ when the record holds $8$ amplitude e-foldings,
$6.8\times10^{-6}$ at $16$ — and then stops falling, pinned at what the grid alone can
support. Refining a grid cannot fix a record that was too short.
:::

**3. Two kicks, timed.** Kicks spaced one period apart give $1 + e^{-\pi/Q}$ times the single
response, kicks a half period apart give $1 - e^{-\pi/2Q}$, and kicks a quarter period apart
give $\sqrt{2}$ — measured, and matching the closed forms.

**4. Two routes to $Q$ from one record.** The laboratory's punchline, run under eight
independent seeds. The *same* noisy ringdown is read in the time domain, where $Q$ comes from
how fast the envelope decays, and in the frequency domain, where it comes from how wide the
line is. They agree to better than $2\%$, and nothing but the data passes between them.

There is one trap in step 4, and the library is built around it. `q_from_bandwidth` finds the
half-power points by interpolating between samples, which is the right thing to do on a
*swept* curve, where the experimenter chooses how finely to sample. Nobody chooses the grid of
a ringdown's spectrum: its bin spacing is $2\pi/T$ while its linewidth is $\gamma$, so a
record holding $n$ amplitude e-foldings gets $n/\pi$ bins across the full width **whatever $Q$
is** — fewer than two, for a realistic record. Recording for longer is not the escape it looks
like, since ten bins would need thirty-one e-foldings, by which point the signal is $10^{-14}$
of where it started. The fix is to fit the whole lineshape rather than interpolate two points
on it, which is what `q_from_linewidth` does and why it exists.

(05-impulse-response-transfer)=
## Transfer the idea

- **Imaging is this module with $t$ replaced by $(x, y)$.** A lens answers a point of light
  with a small blur — the point spread function — and answers an extended object by
  superposing one blur per point, which is a convolution. $G$ becomes the PSF and $\hat{G}$
  becomes the optical transfer function; module `40-psf-otf` is this page with two spatial
  coordinates instead of one temporal one, and almost nothing else changes.
- **The atom as a kicked oscillator.** Module `16-light-in-matter` binds an electron with a
  spring; its absorption line is $|\hat{G}|$ for that oscillator, and its ringdown is
  fluorescence.
- **Cavity ringdown.** Modules `26-fabry-perot` and `44-resonators` measure mirror losses by
  filling a cavity with light, switching the light off, and timing the decay. That is this
  module's experiment performed on photons, and the linewidth it implies is $\hat{G}$ again.
- **Every wavelet is an impulse response.** Module `28-huygens` builds a propagating wave by
  treating each point of a wavefront as a source of secondary wavelets and adding them up.
  Same structure, same word: the wavelet is the medium's Green function in space.
- **Electronics, permanently.** The RLC dictionary is not an analogy to be admired once. Any
  result you meet in circuit theory about transfer functions, step responses, ringing, or
  bandwidth is a result about this oscillator.

:::{admonition} Linear time-invariant system
:class: definition
A system is **linear** if its response to a sum of inputs is the sum of its responses, and
**time-invariant** if delaying the input only delays the output. Any such system is completely
described by its **impulse response** $G(t)$ — its answer to a single unit kick — because
every input is a superposition of kicks. Its transform $\hat{G}(\omega)$ is the **frequency
response**, and the two carry identical information in different clothes. This is the single
most reused idea in the course.
:::

(05-impulse-response-quiz)=
## Check your understanding

```{include} ../_generated/quiz-05-impulse-response.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](05-impulse-response-problems.md).

(05-impulse-response-explain)=
## Explain it in your own words

Answer in a few sentences each. No number will save you.

1. Explain to a musician why hitting a bell harder makes it louder but never higher, and what
   would have to be true of the bell for a harder strike to change the pitch.
2. What, physically, is the oscillator's "memory"? How long does it last, and what sets that
   duration? Give the answer in cycles as well as in seconds.
3. Describe convolution in words, to someone who has not seen an integral sign. You may use
   the word "kick" as often as you like.
4. Suppose someone showed you a measured $G(t)$ that was nonzero for $t < 0$. What absurdity
   follows? Name something you could then build.

(05-impulse-response-advanced)=
## Advanced: the name, the other solution, and undoing a convolution

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section.
:::

**The name.** $G$ is a **Green function**, and the definition is more general than the use made
of it above. Given a linear differential operator $\mathcal{L}$, the Green function is the
solution of

$$
\mathcal{L}\,G(t) = \delta(t),
$$

that is, the response to a unit spike of source. Here $\mathcal{L} = m\,d^2/dt^2 + b\,d/dt + k$
and the spike is the kick. The reason this is worth a name is that it works for *any* linear
operator: replace $\mathcal{L}$ with the wave operator and you get the propagating wavelets of
module `28-huygens`; replace it with the Laplacian and you get the potential of a point charge.
Solving a linear problem once for a point source solves it for every source, by superposition.

**The solution we threw away.** The equation $\mathcal{L}G = \delta$ has more than one
solution, and the difference between any two of them solves $\mathcal{L}G = 0$ — a free
oscillation, which can be added at will. Fixing $G = 0$ for $t < 0$ picks one out, the
*retarded* Green function. The other natural choice, $G = 0$ for $t > 0$, is the *advanced*
one, and it is a perfectly good solution of the differential equation describing a mass that
rings with growing amplitude and is brought to rest by a kick that has not happened yet. There
is no equation to rule it out. We rule it out because we have never seen one, which is a
statement about the world and not about the algebra — and, it is worth saying, a statement
physicists have had to revisit more than once at the edges of electrodynamics.

**Undoing it.** If $\hat{x} = \hat{G}\hat{F}$, then surely $\hat{F} = \hat{x}/\hat{G}$: measure
the motion, divide by the known response, recover the force that caused it. This is
**deconvolution**, and it is how you would sharpen a blurred photograph. Try it in the
laboratory's last cell and watch it fall apart. The trouble is that $\hat{G}$ is small far
from resonance, so dividing by it multiplies whatever is there by a large number — and what is
there, out where the signal is small, is noise. With no noise at all the recovery is exact.
Add noise at one part in $10^6$ and the recovered force is still recognisable; at one part in
$10^4$ it is already twice too large; at one part in $100$ it overshoots by a factor of a
hundred and looks like nothing whatever.

The crude rescue is to refuse to divide where $|\hat{G}|$ is small, simply zeroing those
frequencies. That keeps the answer bounded and throws away real information along with the
noise. Doing better than crude — deciding how much to trust each frequency, given what you
know about the noise — is a genuine subject, and module `53-computational-imaging` takes it up
properly. The reason to see the wreckage now is that it explains a limit you will meet
repeatedly: you cannot recover what the system did not transmit, and no amount of arithmetic
afterwards will put it back.
