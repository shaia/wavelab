---
title: Damping, resonance, and the quality factor
short_title: 02 · Resonance
module: 02-damped-driven
objectives:
  - id: OBJ-02-1
    text: Solve m x'' + b x' + k x = 0 in the underdamped, critical and overdamped regimes, classify a system from gamma = b/m against 2 omega0, and sketch each.
  - id: OBJ-02-2
    text: Solve the driven oscillator by the complex-amplitude method — divide out the time factor — obtaining X = (F0/m) / (omega0^2 - omega^2 - i gamma omega).
  - id: OBJ-02-3
    text: Read amplitude and phase response curves — lag 0 -> pi/2 -> pi, peak at omega0 sqrt(1 - 1/(2 Q^2)) existing only for Q > 1/sqrt(2), and |X(omega0)| = Q F0/k.
  - id: OBJ-02-4
    text: Extract Q = omega0/gamma three equivalent ways — energy decay per radian of a ringdown, bandwidth omega0/Delta omega, and phase slope 2Q/omega0 at resonance.
  - id: OBJ-02-5
    text: Decompose driven motion into a decaying transient plus a steady state, and estimate the takeover time 2/gamma, about Q/pi periods.
  - id: OBJ-02-6
    text: Identify the high-Q power response as a Lorentzian of full width gamma, and transfer Q-and-bandwidth reasoning to cavities, atoms and circuits.
---

# Damping, resonance, and the quality factor

(02-damped-driven-puzzle)=
## The puzzle: the note that breaks the glass

A singer holds one sustained note and a wine glass across the room shatters. The same singer,
just as loud, a tone higher or lower — nothing. Not quieter destruction: *no* destruction. The
glass is indifferent to almost every sound in the world and lethally sensitive to one.

Module 01 gave you an oscillator that ignores how hard you push it. This one is exquisitely
sensitive to *when* you push it, and it is the same oscillator. Nothing has been added but a
loss term and a hand on the other end.

:::{important} The question
Why is an oscillator's response so violently frequency-dependent — what sets the deadly
pitch, and how violent does it get? And since the singer cannot supply unlimited energy, what
decides where the growth stops?
:::

The second half of the puzzle is where the physics is. If the response at the right frequency
were truly unbounded, every bridge would fall and every radio would receive every station at
once. Something finite is at work, and it turns out to be the same something that makes a
struck glass eventually go quiet.

(02-damped-driven-predict)=
## Predict before you calculate

Commit to an answer for each of these *before* running anything. Write them down.

1. You push a mass on a spring back and forth very slowly — far below its natural frequency.
   Does the mass move in step with your hand, opposite to it, or a quarter cycle behind?
   What about very fast pushing?
2. As you sweep the drive frequency, the response peaks somewhere. Is the peak *below*, *at*,
   or *above* the natural frequency $\wnat$?
3. You drive at exactly $\wnat$ and never stop. Does the amplitude grow without limit?
4. You double the damping. What happens to the number of visible cycles after a single
   plucked release, and what happens to the width of the resonance peak? Are those two
   answers related?

:::{note} Why we ask first
Question 2 catches almost everybody, including textbooks: the peak is *not* at $\wnat$, and
you will measure exactly how far below it sits. Question 4 is the module in one line — the
same $\gamma$ answers both halves, which is why one number can describe a ringing bell and a
radio's selectivity.
:::

(02-damped-driven-explore)=
## Explore the model

Two animations, both generated from the same `wavelab.oscillators` code the laboratory runs.

:::{figure} ../media/resonance-regimes.mp4
:width: 100%

The same oscillator released from rest, over and over, as the damping is swept continuously
from very light to very heavy. Left: the motion, inside its decaying envelope. Right: the
same history in phase space, module 01's closed ellipse unwinding into a spiral and finally
into a curve that never completes a turn. The green mark on the top bar is critical damping
— note that nothing discontinuous happens as the sweep crosses it. The system does not
change kind; it simply runs out of cycles.
:::

:::{figure} ../media/resonance-sweep.mp4
:width: 100%

A drive slowly ramped through resonance. Left: the steady-state motion (blue) against the
drive (grey) — watch the lag grow from nothing, through a quarter cycle, to a half cycle, so
that far above resonance the mass moves *against* the hand pushing it. Right: the amplitude
and lag curves being filled in as the ramp passes over them. The dotted line is $\wnat$; the
dashed line is where the amplitude actually peaks. They are not the same line.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** a point mass $m$ on a massless linear spring of stiffness $k$, with linear velocity damping $b$ and a sinusoidal driving force, in one dimension; the observables are position, velocity, the energies and the cycle-averaged power.
- **Dynamics:** $m\ddot{x} = -kx - b\dot{x} + F_0\cos\omega t$, solved in closed form where one exists and integrated by velocity Verlet elsewhere.
- **Boundary:** none spatially; the environment appears only as a featureless sink that accepts energy and is never asked what it does with it.
- **Ensemble:** a single deterministic trajectory per choice of parameters and initial conditions; measurement noise, where added, is Gaussian, independent and seeded.
- **Ignored:** the microscopic mechanism behind $b$, the drive's back-reaction on whatever supplies it, the spring's nonlinearity, and any heating of the system by its own dissipation.
- **Valid when:** displacements stay in the linear regime of the real spring, the damping is genuinely viscous — proportional to velocity — and any claim about the steady state is made after the transient has died.
- **Failure modes:** dry friction (a constant-magnitude force, not proportional to $v$), resonant amplitudes large enough to leave the linear regime, transient data read as steady state, and any question about where the dissipated energy goes.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 02 — damping, resonance, and Q](/lite/lab/index.html?path=en/labs/02-damped-driven.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/02-damped-driven.ipynb`.
:::

Run the laboratory now, then come back. Three things are worth doing before you read on:

- Sweep the damping slider slowly through the critical value and watch for the moment the
  motion stops being oscillatory. Try to catch it happening. You cannot — and that is the
  observation, not a failure of the slider.
- Put the response explorer at a high $Q$ and find the peak by eye. Then lower $Q$ and watch
  the peak slide *downhill* in frequency until it falls off the edge and disappears.
- Start from rest driving exactly at $\wnat$, and count how many cycles pass before the
  amplitude settles. Compare that count with $Q$.

(02-damped-driven-derive)=
## Derive the result

**System.** Module 01's mass and spring, plus two additions: a resistive force $-b\dot{x}$
and an applied force $F(t)$. Newton's second law reads

$$
m\ddot{x} + b\dot{x} + kx = F(t),
\qquad
\wnat \equiv \sqrt{\frac{k}{m}},
\qquad
\gamma \equiv \frac{b}{m} .
$$

:::{admonition} Viscous damping
:class: model-assumption
$F_{\text{damp}} = -b\dot{x}$ is a *modelling choice*, not a law. It describes a body moving
slowly through a fluid well, and describes dry sliding friction — whose magnitude does not
care about speed — badly. It is adopted here for one honest reason beyond realism: it is the
only dissipation law that keeps the equation linear, and linearity is what lets every result
below be written down exactly. Where a real system disagrees, it disagrees with this line.
:::

Note the course's convention: $\gamma \equiv b/m$, so amplitudes decay as
$e^{-\gamma t/2}$ and energies as $e^{-\gamma t}$. Several textbooks (French among them)
define $\gamma = b/2m$ instead. Both are in print; mixing them within one calculation is the
only real mistake.

**Free decay: loss as an imaginary frequency.** With $F = 0$, try the module-00 move — assume
the answer rotates — but allow the frequency to be complex,
$x = \Real\!\left[C\,e^{-\ii\Omega t}\right]$. Each derivative brings down a factor
$-\ii\Omega$, and the whole equation collapses to a quadratic in $\Omega$:

$$
\Omega^2 + \ii\gamma\Omega - \wnat^2 = 0
\qquad\Longrightarrow\qquad
\Omega = \pm\,\omega_d - \frac{\ii\gamma}{2},
\qquad
\omega_d = \sqrt{\wnat^2 - \frac{\gamma^2}{4}} .
$$

Read what that says. The real part of $\Omega$ is a frequency of oscillation; the imaginary
part is a decay rate, because $e^{-\ii(-\ii\gamma/2)t} = e^{-\gamma t/2}$. *Loss is the
imaginary part of a frequency.* Hold onto that sentence: it returns as the complex refractive
index $n + \ii\kappa$ of an absorbing medium, and again as the linewidth of an optical cavity.

Three cases follow from the square root, and they are three cases of one formula:

- **Underdamped** ($\gamma < 2\wnat$): $\omega_d$ is real and the motion is
  $e^{-\gamma t/2}$ times a sinusoid at $\omega_d$ — ringing, inside a decaying envelope.
  Note $\omega_d < \wnat$: damping slows the ringing as well as killing it.
- **Critical** ($\gamma = 2\wnat$): the two roots coincide, $\omega_d = 0$, and the solution
  picks up a factor of $t$: $(C + Dt)e^{-\wnat t}$. This is the fastest possible return to
  equilibrium without overshoot, which is why it is what a door closer or a car suspension
  aims at.
- **Overdamped** ($\gamma > 2\wnat$): both roots are purely imaginary, the motion is a sum of
  two decaying exponentials, and it crosses zero at most once. Heavier damping now makes the
  return *slower*, not faster — the mass creeps home through treacle.

**Quality factor.** In the underdamped case the energy, which goes as amplitude squared,
decays as $e^{-\gamma t}$. Ask how much is lost per radian of oscillation and one
dimensionless number falls out:

$$
Q \equiv \frac{\wnat}{\gamma}
= 2\pi \times \frac{\text{energy stored}}{\text{energy lost per cycle}}
= \frac{\sqrt{mk}}{b} .
$$

A struck oscillator rings for about $Q$ radians, which is $Q/2\pi$ cycles, before its energy
falls by $1/e$; its *amplitude* survives about $Q/\pi$ cycles. A wine glass has
$Q \sim 10^3$, a quartz watch crystal $10^5$, the mirrors of a gravitational-wave detector
$10^7$. Suspension dampers are built at $Q \approx 1$ on purpose.

**Driven: the complex-amplitude method.** Now switch the drive on, $F = F_0\cos\omega t$, and
wait for the transient to die. Whatever is left must repeat at the drive frequency — nothing
else in the problem has a memory — so write both drive and response as rotating arrows,
$F = \Real[F_0 e^{-\ii\omega t}]$ and $x = \Real\!\left[X e^{-\ii\omega t}\right]$, with $X$
complex. Every derivative becomes a multiplication by $-\ii\omega$, the exponential divides
out of every term, and a differential equation becomes one line of arithmetic:

$$
\left(-\omega^2 - \ii\gamma\omega + \wnat^2\right) X = \frac{F_0}{m}
\qquad\Longrightarrow\qquad
X(\omega) = \frac{F_0/m}{\wnat^2 - \omega^2 - \ii\gamma\omega} .
$$

This is module 00 collecting its debt. The arrow's length is the amplitude and its angle is
the phase lag:

$$
|X| = \frac{F_0/m}{\sqrt{\left(\wnat^2 - \omega^2\right)^2 + \gamma^2\omega^2}},
\qquad
\tan\varphi_{\text{lag}} = \frac{\gamma\omega}{\wnat^2 - \omega^2} .
$$

**Reading the two curves.** Three landmarks answer the first prediction question:

- $\omega \ll \wnat$: the denominator is $\wnat^2$, so $|X| \to F_0/k$ with
  $\varphi_{\text{lag}} \to 0$. Push slowly and the mass simply sits where the force puts it.
  The spring is in charge.
- $\omega = \wnat$: the real part of the denominator vanishes, leaving
  $|X| = Q\,F_0/k$ and $\varphi_{\text{lag}} = \pi/2$ *exactly*. Damping alone limits the
  response, and the mass runs a quarter cycle behind the hand — which is precisely the phase
  at which the drive does the most work per cycle.
- $\omega \gg \wnat$: $|X| \to F_0/m\omega^2$ with $\varphi_{\text{lag}} \to \pi$. Inertia is
  in charge, and the mass moves *against* the force.

**Where the peak really is.** Maximising $|X|$ means minimising
$\left(\wnat^2 - \omega^2\right)^2 + \gamma^2\omega^2$. Differentiate with respect to
$\omega^2$ and the answer is immediate:

$$
\omega_{\text{peak}} = \sqrt{\wnat^2 - \frac{\gamma^2}{2}}
= \wnat\sqrt{1 - \frac{1}{2Q^2}} .
$$

:::{admonition} The amplitude peak sits below the natural frequency
:class: theorem
For any damping at all, $\omega_{\text{peak}} < \wnat$, and the gap widens as $Q$ falls. When
$Q \le 1/\sqrt{2}$ the square root has no real value: the interior maximum does not exist,
the response falls monotonically from its static value $F_0/k$, and the system has no
resonance to speak of — it is a low-pass filter. "The response peaks at the natural
frequency" is therefore not a slightly imprecise statement but a false one, exactly true only
in the limit of no damping, where there is no steady state at all.
:::

**Q, three ways.** The same number can be read off three completely different experiments,
and this is the module's central claim:

$$
Q = \frac{\wnat}{\gamma}
\qquad\text{(ringdown: } E \propto e^{-\gamma t}\text{)},
$$

$$
Q = \frac{\wnat}{\Delta\omega}
\qquad\text{(bandwidth: half-power full width } \Delta\omega = \gamma\text{)},
$$

$$
Q = \frac{\wnat}{2}\left.\frac{d\varphi_{\text{lag}}}{d\omega}\right|_{\wnat}
\qquad\text{(phase slope: } d\varphi_{\text{lag}}/d\omega = 2/\gamma\text{)}.
$$

The first is measured in the time domain by watching something die away; the second and third
in the frequency domain by sweeping a drive and recording amplitude, or phase. Nothing
guarantees in advance that three such different measurements return one number. That they do
is the content of the theory, and the laboratory checks it on data.

**Power and the Lorentzian.** In the steady state, every joule the drive supplies is
dissipated — the amplitude is not growing, so nothing is being stored on average. The
cycle-averaged power is

$$
\langle P \rangle = \tfrac12\,\gamma\, m\, \omega^2 |X|^2
= \frac{F_0^2}{2m}\,\frac{\gamma\omega^2}{\left(\wnat^2 - \omega^2\right)^2 + \gamma^2\omega^2} .
$$

Divide numerator and denominator by $\omega^2$ and the frequency dependence becomes
$\left[\left(\wnat^2 - \omega^2\right)/\omega\right]^2 + \gamma^2$, which is smallest at
$\omega = \wnat$ *exactly*, whatever the damping. Displacement resonance and power resonance
are different frequencies. Near a sharp resonance the expression simplifies further:

:::{admonition} The Lorentzian
:class: approximation
For $Q \gg 1$ and $\omega$ near $\wnat$, write $\wnat^2 - \omega^2 \approx 2\wnat(\wnat -
\omega)$ and $\omega \approx \wnat$ everywhere else. Then

$$
\langle P \rangle \approx \frac{F_0^2}{2m\gamma}\,
\frac{\left(\gamma/2\right)^2}{\left(\omega - \wnat\right)^2 + \left(\gamma/2\right)^2},
$$

a **Lorentzian** centred on $\wnat$ with full width at half maximum $\gamma$ — hence
$Q = \wnat/\Delta\omega$. The approximation is good to a few percent for $Q \gtrsim 10$ and
worthless below $Q \sim 2$, where the "peak" is wider than its own centre frequency. This
curve is not a special fact about springs: it is the universal shape of a weakly damped
resonance, and you will meet it again as an atom's absorption line, a Fabry–Pérot
transmission peak, and a laser cavity mode.
:::

**Transient plus steady state.** The full solution of a linear equation with a drive is *any*
particular solution plus the general solution of the undriven equation. Here that reads

$$
x(t) = \underbrace{|X|\cos\left(\omega t - \varphi_{\text{lag}}\right)}_{\text{steady state}}
\; + \; \underbrace{e^{-\gamma t/2}\left(A\cos\omega_d t + B\sin\omega_d t\right)}_{\text{transient}},
$$

with $A$ and $B$ fixed by the initial conditions — and by nothing else, which is why the
steady state is the same however you start. The transient lives for about $2/\gamma$, or
$Q/\pi$ periods. Starting from rest at exact resonance, the two pieces combine into a growing
envelope

$$
x(t) \approx Q\,\frac{F_0}{k}\left(1 - e^{-\gamma t/2}\right)\sin\wnat t .
$$

There is the answer to the third prediction. The amplitude does *not* grow without limit: it
climbs toward $Q$ times the static response and stops, taking about $Q/\pi$ cycles to get
there. Resonance is $Q$-fold amplification, paid for in patience. A high-$Q$ system is
selective and loud *and* slow to respond — one number, three consequences, and the reason no
receiver can be arbitrarily sharp and arbitrarily fast at once.

(02-damped-driven-verify)=
## Verify computationally

Each check below is also a test in the project's suite, so these claims cannot silently rot.

**1. The closed forms, in every regime.** Velocity-Verlet integration against
`damped_position` for light, critical and heavy damping, including from both sides of the
critical boundary — the three branches are one function, and agree where they meet to better
than one part in $10^6$.

**2. The peak position, swept.** The falsifying experiment. Amplitude-response curves are
computed at a range of dampings, the maximum of each is located numerically, and the results
are plotted as $\omega_{\text{peak}}/\wnat$ against $1/Q^2$.

:::{admonition} Measured peak positions
:class: numerical-observation
The measured maxima fall on $\sqrt{1 - 1/(2Q^2)}$ across two decades of damping, agreeing
with the prediction to within the sweep's own grid spacing. At $Q = 20$ the peak sits
$0.06\%$ below $\wnat$ — invisible on any plot, which is exactly why the misconception
survives. At $Q = 2$ it sits $6.5\%$ below, unmissable. And below $Q = 1/\sqrt{2}$ the
numerical maximum jumps to $\omega = 0$: the peak has not moved off the plot, it has ceased
to exist.
:::

**3. Three ways to Q, on one dataset.** `q_from_ringdown`, `q_from_bandwidth` and
`q_from_phase_slope` are pointed at simulated measurements of the *same* oscillator — a
decay record, an amplitude sweep, a phase sweep — with detector noise added and eight
independent seeds. All three agree with $\sqrt{mk}/b$, and with each other, to better than
$1\%$. The residual is not scatter: it is systematic, and each estimator's is different. The
bandwidth route reads low because the half-power width is only asymptotically $\gamma$; the
ringdown route reads high because a noisy record's mean square is its signal's plus its
noise's. Telling the two kinds of error apart is what a measurement culture is.

**4. Power balance.** In the steady state, the cycle average of $F\dot{x}$ computed from an
integration equals the cycle average of $b\dot{x}^2$, and both equal `power_absorbed`, to two
parts in $10^3$ at 800 steps per period. The drive is not storing energy anywhere; it is
paying the damper, exactly.

(02-damped-driven-transfer)=
## Transfer the idea

- **A periodic but non-sinusoidal drive** — a square wave, a shove once per cycle — is a comb
  of harmonics, and this response curve weights each one. That is the whole content of
  [module 03](../foundations/03-fourier-series.md): the resonator is a filter, and the Fourier series is the
  decomposition it filters.
- **The atom as an oscillator.** Bind an electron with a spring and drive it with a light
  wave and you have the Lorentz model of a medium. Its absorption line is the
  $\langle P\rangle$ curve above, its refractive index the real part of the same response.
  This module *is* module `16-light-in-matter`, with charge attached.
- **Cavities.** A Fabry–Pérot resonator's finesse and a laser cavity's photon lifetime are
  $Q$ in other costumes; the transmission peak is this Lorentzian; the linewidth is
  $\Delta\omega = \wnat/Q$.
- **The series RLC circuit.** $L\ddot{q} + R\dot{q} + q/C = V(t)$ is this equation with
  $m \to L$, $b \to R$, $k \to 1/C$. Tuning a radio is choosing $\wnat$; the station you do
  not hear is $\Delta\omega$ doing its job.
- **The tuned mass damper.** The 660-tonne sphere near the top of Taipei 101 is a pendulum
  deliberately built to resonate with the tower and dissipate, moving out of phase with the
  building and taking the energy the wind puts in.

:::{admonition} The quality factor
:class: definition
The **quality factor** $Q$ of a resonator is $2\pi$ times the energy it stores divided by the
energy it loses per cycle; equivalently $Q = \wnat/\gamma$, $Q = \wnat/\Delta\omega$, and
$Q = (\wnat/2)\,d\varphi_{\text{lag}}/d\omega$ at resonance. It is dimensionless and it is a
property of the resonator, not of how hard it is driven. Everything a linear resonator does —
how long it rings, how sharply it selects, how much it amplifies, how slowly it responds — is
this one number.
:::

(02-damped-driven-quiz)=
## Check your understanding

```{include} ../_generated/quiz-02-damped-driven.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](02-damped-driven-problems.md).

(02-damped-driven-explain)=
## Explain it in your own words

Answer in a few sentences each. No number will save you.

1. Explain to someone on a swing why pushing at one particular rhythm works and pushing
   harder at the wrong rhythm does not. Where in the cycle does a good push happen, and why
   is that the same as "a quarter cycle behind"?
2. Give three one-sentence definitions of $Q$ — one about time, one about frequency, one
   about phase — and then say what single physical fact makes them the same number.
3. Why does the amplitude peak sit *below* $\wnat$ while the absorbed power peaks exactly
   *on* it? Both are properties of the same motion.
4. Where does the dissipated energy go? Say what this model can tell you, and then say
   precisely which of its seven specification bullets makes the question unanswerable here.

(02-damped-driven-advanced)=
## Advanced: three resonances, and the world without one

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section.
:::

**Displacement, velocity, power.** "The resonant frequency" is three different frequencies
wearing one name. The displacement amplitude $|X|$ peaks at
$\wnat\sqrt{1 - 1/(2Q^2)}$, below $\wnat$. The velocity amplitude $\omega|X|$ peaks at
$\wnat$ exactly — and so, therefore, does the absorbed power, which goes as the square of the
velocity. The acceleration amplitude $\omega^2|X|$ peaks *above* $\wnat$, at
$\wnat/\sqrt{1 - 1/(2Q^2)}$, the mirror image of the displacement peak. At $Q = 20$ the three
sit within a quarter of a percent of each other and the distinction is pedantry; at $Q = 2$
they are visibly different curves and the pedantry is the answer to an exam question.

That velocity resonance is exact is not an accident. Write the equation in terms of velocity
and the oscillator becomes an impedance, $Z = b + \ii(m\omega - k/\omega)$, whose magnitude
is least when the reactive part cancels — at $\wnat$, for any $b$. That is the same
mechanical impedance that will decide how much of a wave reflects at a boundary in
module `10-impedance`, and the same cancellation of two opposing reactances.

**The world below $Q = 1/\sqrt{2}$.** Everything above assumed a peak exists. Below
$Q = 1/\sqrt{2}$ — damping heavier than $\sqrt{2}\,\wnat$ — the response curve simply slides
downhill from $F_0/k$, and the system is a second-order low-pass filter with no resonance at
all. Engineers reach for this deliberately: $Q = 1/\sqrt{2}$ is the flattest possible
response with no peak, the Butterworth condition, and it is what a loudspeaker enclosure or an
anti-aliasing filter is usually tuned to. Critical damping, $Q = 1/2$, is flatter still and
settles fastest without overshoot. Between them lies most of engineering; above them lies
most of physics.

**A harder question the model cannot answer.** The damping term removes energy from the mass
and the model stops there. In reality that energy goes into the molecular motion of the
surrounding fluid, which then jostles the mass back — the same coupling that dissipates must
also fluctuate. That is not a loose end but a theorem, the fluctuation–dissipation theorem,
and it says that a resonator's damping and its thermal noise are two faces of one coefficient.
It is the reason a gravitational-wave detector's mirror suspensions are made of fused silica
with $Q \sim 10^7$: not to ring longer, but to be quiet.
