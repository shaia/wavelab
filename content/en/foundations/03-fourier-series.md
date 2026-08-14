---
title: "Fourier series: periodic signals as harmonic sums"
short_title: 03 · Fourier series
module: 03-fourier-series
objectives:
  - id: OBJ-03-1
    text: Compute Fourier coefficients c_n = (1/T) integral over one period of f(t) e^(-i n omega0 t) dt using orthogonality, and read |c_n| and arg(c_n) as the size and timing of the nth harmonic.
  - id: OBJ-03-2
    text: Predict from symmetry alone which harmonics a waveform contains — even/odd symmetry and half-wave symmetry — before computing any integral.
  - id: OBJ-03-3
    text: Relate smoothness to coefficient decay (a jump gives 1/n, a corner 1/n^2) and identify the Gibbs overshoot as a fixed 8.9 percent of the jump that no number of terms removes.
  - id: OBJ-03-4
    text: Predict the steady-state response of a damped driven oscillator to a periodic non-sinusoidal drive by weighting each harmonic with the module 02 response curve.
  - id: OBJ-03-5
    text: Convert between time-domain and spectrum descriptions of the square, triangle, sawtooth and pulse-train waveforms.
---

# Fourier series: periodic signals as harmonic sums

(03-fourier-series-puzzle)=
## The puzzle: the note that isn't there

A tuning fork is a resonator with a sharply defined pitch. Stand one that rings at 300 Hz next
to a loudspeaker and drive the speaker with a 100 Hz *square* wave — the blunt on-off signal a
cheap buzzer makes. The fork sings. Drive the speaker instead with a 100 Hz *sine* wave, at the
same loudness, and the fork stays silent.

Nothing in the second signal is missing that the first has. Both repeat one hundred times a
second. Both are, by any reasonable description, "a 100 Hz signal". Yet one of them is carrying
something at 300 Hz and the other is not.

:::{important} The question
Where does a 100 Hz square wave keep its 300 Hz? More generally: what *is* the frequency
content of a periodic signal that is not a sinusoid — and is that content a physical fact
about the signal, or a way of talking about it?
:::

There is a second version of the same puzzle you have heard all your life. A violin and a flute
play the same written A. Both repeat 440 times a second, so both have the same pitch, and
nobody has ever confused the two instruments. Whatever distinguishes them survives having the
same period, and this module is about what that is.

(03-fourier-series-predict)=
## Predict before you calculate

Commit to an answer for each of these *before* running anything. Write them down.

1. Does a resonator tuned to $3\omega_0$ respond to a square-wave drive of repetition rate
   $\omega_0$? Does it respond to a *sine* drive at $\omega_0$? What about a resonator tuned to
   $2\omega_0$ under the square drive?
2. A square wave is built by adding sine waves. How many terms does it take before the result
   is a square wave — ten, a thousand, or is there a number after which it is exact?
3. Zoom in on the jump while you add more and more terms. The wiggles there get narrower. Do
   they also get *shorter*, and does the overshoot go to zero?
4. A triangle wave and a square wave have the same period and the same peak height. Which one
   is reproduced better by its first five harmonics, and what feature of the waveform decides?

:::{note} Why we ask first
Question 3 is the one that catches people, and it will be settled by measurement rather than by
argument: something about the approximation genuinely does not improve. Question 1 is the module
in miniature — by the end you will be able to say which of those three resonators rings, and
how loudly, without touching an oscilloscope.
:::

(03-fourier-series-explore)=
## Explore the model

The laboratory notebook gives you a harmonic mixer: a slider for the size of each harmonic and
another for its timing, up to thirty-two of them, with four preset waveforms to reconstruct. The
waveform and its spectrum sit side by side and update together — the dual view that becomes this
course's standard way of looking at any signal, here for the first time.

:::{figure} ../media/fourier-square-buildup.mp4
:width: 100%

A square wave assembling itself from rotating arrows. Each arrow is one harmonic's phasor —
module 00's picture, one arrow per harmonic, the $n$th turning $n$ times faster — laid tip to
tail, and the height of the running tip traces the waveform on the right. The animation holds
$N = 1, 3, 5, 9, 33$ for one period each. Arrow lengths are not chosen: they are
$4/\pi n$, so the ninth arrow is exactly a ninth of the first, and the $1/n$ decay of the
coefficients is visible as geometry. Watch the corners sharpen as arrows are added — and watch
what happens at the jump, which does not.
:::

:::{figure} ../media/fourier-gibbs-zoom.mp4
:width: 100%

The jump, magnified. First the window holds still while the number of terms climbs: the ripples
crowd in toward the discontinuity. Then the number of terms freezes and the window magnifies
twentyfold: the same structure reappears at every scale. Through both halves the first
overshoot stays on the dashed line — it is not converging to the true value, and adding terms
moves it sideways rather than downwards.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** a real periodic signal of period $T$, represented by its complex coefficients $\{c_n\}$; the observables are partial sums, harmonic amplitudes, and harmonic phases.
- **Dynamics:** none — this is a change of representation, not an evolution; when the harmonics are used to drive the module 02 oscillator, each one drives it independently by linearity.
- **Boundary:** exact periodicity, extending forwards and backwards forever; one period carries the entire signal and nothing is stored between periods.
- **Ensemble:** deterministic; the laboratory's extraction experiment is the only stochastic part, and its noise is Gaussian, independent and seeded.
- **Ignored:** transients of every kind — the driven results are steady state only — and convergence pathologies beyond piecewise-smooth signals.
- **Valid when:** the signal really is periodic and piecewise smooth, and partial sums near a jump are read with the Gibbs overshoot in mind.
- **Failure modes:** treating the overshoot as an error that more terms would remove, applying the series to a signal that never repeats, and summing harmonic responses through anything nonlinear.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 03 — Fourier series](/lite/lab/index.html?path=en/labs/03-fourier-series.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/03-fourier-series.ipynb`.
:::

Run the laboratory now, then come back. Three things are worth doing before you read on:

- Build a square wave from three sliders, then five, then thirty-one, watching the spectrum
  panel as much as the waveform. Notice which harmonics you never need to touch.
- Play the four presets through the audio cell at the same pitch. They are the same note. Your
  ear tells them apart instantly, and the only thing that differs is the spectrum panel.
- Zoom on the jump and raise $N$ until the laboratory runs out of harmonics. Decide, from what
  you see rather than from what you expect, what is shrinking and what is not.

(03-fourier-series-derive)=
## Derive the result

**What can be in the sum.** A signal of period $T$ repeats exactly. If it is to be built from
sinusoids, each of those must also repeat with period $T$, which allows only the frequencies
$\omega_0, 2\omega_0, 3\omega_0, \dots$ with $\omega_0 = 2\pi/T$ — the **harmonics** of the
fundamental. Anything else would still be mid-cycle when the signal starts over. So the
candidate is

$$
f(t) = \sum_{n=-\infty}^{\infty} c_n\, e^{\ii n \omega_0 t},
$$

with both signs of $n$ present. That is not a complication to apologise for: module 00 already
showed that a real cosine is *two* counter-rotating exponentials, and here the pairing is
$c_{-n} = c_n^{*}$, which is precisely the condition for $f$ to come out real.

**Orthogonality picks out one coefficient.** Everything follows from a single integral. For
integer $n$ and $m$,

$$
\frac{1}{T}\int_{T} e^{\ii (n-m)\omega_0 t}\,\mathrm{d}t = \delta_{nm},
$$

because unless $n = m$ the integrand is a complex exponential going through a whole number of
turns, and a whole number of turns averages to nothing.

:::{admonition} Orthogonality of the harmonics
:class: theorem
Distinct harmonics are orthogonal under the average-over-a-period inner product. Multiplying
the candidate sum by $e^{-\ii m \omega_0 t}$ and averaging therefore annihilates every term but
one, giving

$$
c_m = \frac{1}{T}\int_{T} f(t)\, e^{-\ii m \omega_0 t}\,\mathrm{d}t .
$$

Each coefficient can be extracted without knowing any of the others. That independence is what
makes the decomposition useful rather than merely true.
:::

The language is worth pausing on. "Multiply and average" is an inner product; the harmonics are
an orthonormal *basis*; $c_n$ is the component of $f$ along the $n$th basis direction. The
picture is the familiar one of resolving a vector into perpendicular components, with functions
in place of arrows and an integral in place of a dot product. You will meet the same move again
in module `07-normal-modes` and again in quantum mechanics.

:::{admonition} The spectrum
:class: definition
The **spectrum** of a periodic signal is the set $\{c_n\}$. Under the course convention the
$n$th harmonic's phasor — the module 00 object, with the time factor $e^{-\ii n\omega_0 t}$ —
is $\hat{f}_n = 2c_n^{*}$. So $|2c_n|$ is the amplitude of that harmonic and $\arg c_n$ fixes
where in the cycle it peaks. The negative-index half of the sum is not extra information; it is
the other half of every real oscillation, and [module 04](04-fourier-transform.md) makes that
explicit.
:::

**Symmetry answers the question before the integral does.** Two symmetries do most of the work
in practice, and both are one substitution deep.

If $f$ is even, $f(-t) = f(t)$, the coefficient integral is unchanged under $t \to -t$, which
sends $c_n \to c_{-n}$; combined with $c_{-n} = c_n^{*}$ this forces every $c_n$ to be real. If
$f$ is odd, the same argument makes every $c_n$ purely imaginary. Evenness and oddness are
statements about *timing*, and they show up as the phases of the harmonics.

Half-wave symmetry is sharper. Suppose the second half of each period is the first half turned
upside down, $f(t + T/2) = -f(t)$ — true of a square wave, a triangle wave, and most things
that swing symmetrically about zero. Substituting into the coefficient integral multiplies term
$n$ by $e^{-\ii n \pi} = (-1)^n$, so $c_n = (-1)^{n+1} c_n$. For even $n$ that reads
$c_n = -c_n$, and the only number equal to minus itself is zero.

:::{admonition} Half-wave symmetry kills the even harmonics
:class: theorem
If $f(t + T/2) = -f(t)$, then $c_n = 0$ for every even $n$, including the mean. Such a signal
is built from odd harmonics alone — and no integral was computed to learn it.
:::

**The square wave, worked.** Take $f(t) = +1$ for the first half of each period and $-1$ for the
second. It is odd and half-wave symmetric, so we already expect purely imaginary coefficients on
odd harmonics only. The integral confirms it:

$$
c_n = \frac{1}{T}\int_{0}^{T/2} e^{-\ii n\omega_0 t}\,\mathrm{d}t
    - \frac{1}{T}\int_{T/2}^{T} e^{-\ii n\omega_0 t}\,\mathrm{d}t
    = \frac{2}{\ii \pi n} \quad (n \text{ odd}), \qquad c_n = 0 \quad (n \text{ even}).
$$

In real terms this is $f(t) = \frac{4}{\pi}\left(\sin\omega_0 t + \tfrac13 \sin 3\omega_0 t
+ \tfrac15 \sin 5\omega_0 t + \cdots\right)$. The third harmonic is there, with a third of the
fundamental's amplitude. That is the answer to the opening puzzle, and it is not a figure of
speech: put a filter tuned to $3\omega_0$ in front of the signal and a sinusoid of amplitude
$4/3\pi$ comes out the other side.

**Smoothness buys decay.** The square wave's coefficients fall as $1/n$, which is slow. The
reason is general. Integrating the coefficient formula by parts trades a factor of
$1/(\ii n \omega_0)$ for a derivative of $f$; the boundary terms cancel by periodicity *provided
$f$ is continuous*. So each derivative that survives without jumping buys one more power of
$1/n$.

:::{admonition} Coefficient decay is set by the worst discontinuity
:class: theorem
If $f$ itself jumps, $|c_n| \sim 1/n$. If $f$ is continuous but its slope jumps — a corner —
then $|c_n| \sim 1/n^2$. In general, if the first discontinuous derivative is the $k$th, the
coefficients fall as $1/n^{k+1}$; a signal with no discontinuity at any order decays faster than
every power. Sharp features are expensive, and *how* expensive is set by how sharp.
:::

| Waveform | Sharpest feature | Harmonics present | Decay |
|---|---|---|---|
| Square | jump | odd only | $1/n$ |
| Sawtooth | jump | all | $1/n$ |
| Triangle | corner | odd only | $1/n^2$ |
| Pulse train | two jumps | all, under a $\operatorname{sinc}$ envelope | $1/n$ |

The table earns its keep in the laboratory, where you measure these exponents rather than
looking them up, and again in [module 04](04-fourier-transform.md), where the same statement is made
about the transform of a single pulse.

**Gibbs: where the series does not do what you want.** Adding terms reduces the *energy* of the
error — the mean-square distance between the partial sum and the signal goes to zero, and for
the square wave it does so as $N^{-1/2}$. But convergence in energy is a weaker promise than it
sounds, and near a jump it is not enough.

:::{admonition} The Gibbs phenomenon
:class: theorem
Near a jump discontinuity, the partial sum of a Fourier series overshoots by about $8.95\%$ of
the height of the jump, on both sides. As $N$ grows the overshoot moves closer to the
discontinuity and becomes narrower, but its *height does not decrease*. It is a property of
truncating the series, not an error that more terms remove.
:::

That is the answer to prediction 3, and it is worth being blunt about what it does and does not
mean. It does not mean the series fails to converge — at every point away from the jump it
converges perfectly well, and at the jump itself it converges to the midpoint. It means that the
*worst* error over the whole signal does not shrink. An amplifier reproducing a square wave with
a finite bandwidth really does overshoot, really does ring, and no amount of extra bandwidth
removes the overshoot; more bandwidth only makes it briefer.

**The resonator is a harmonic selector.** Now the puzzle can be closed quantitatively. Write the
periodic drive as its harmonics, each one a phasor $\hat{F}_n = 2c_n^{*}$ carrying the course's
time factor $e^{-\ii n \omega_0 t}$.

:::{admonition} Each harmonic drives independently
:class: model-assumption
The oscillator equation is linear, so the response to a sum of drives is the sum of the
responses to each. Nothing in this section survives a nonlinear element: a diode, a spring
driven past its linear range, or anything that squares the signal will generate harmonics of
its own and mix the ones already present.
:::

Module 02 already solved the problem for one sinusoid: a drive of phasor $\hat{F}$ at angular
frequency $\omega$ produces a displacement of phasor $\hat{F}/m$ divided by
$\wnat^2 - \omega^2 - \ii\gamma\omega$. Applying it harmonic by harmonic and adding,

$$
x(t) = \sum_{n \ge 1} \Real\!\left[\hat{X}_n\, e^{-\ii n \omega_0 t}\right],
\qquad
\hat{X}_n = \frac{\hat{F}_n/m}{\wnat^2 - (n\omega_0)^2 - \ii\gamma\, n\omega_0} .
$$

Read what that says. The drive supplies a comb of harmonics with amplitudes falling as $1/n$.
The resonator multiplies each by a curve that is sharply peaked at $\wnat$ and small everywhere
else. If $\wnat$ sits on the third harmonic, the third harmonic is amplified by roughly $Q$ and
the others are not: the fork rings at $3\omega_0$, a frequency the drive's repetition rate never
names. And under a pure sine drive the comb has one tooth, at $\omega_0$, so a fork tuned to
$3\omega_0$ hears nothing at all.

Park the resonator on an *even* harmonic and the comb has no tooth there to amplify: half-wave
symmetry deleted it. The response does not vanish outright — the laboratory measures about 8% of
what the same resonator gives at $3\omega_0$ — but what survives is the off-resonant tail of the
third and fifth harmonics, not a response to a fourth. There is no fourth harmonic to respond
to.

A resonator does not measure how often a signal repeats. It asks how much of the signal is at
*its* frequency, and a Fourier series is the answer.

(03-fourier-series-verify)=
## Verify computationally

Each check below is also a test in the project's suite, so these claims cannot silently rot.

**1. The closed forms against the integrals.** `wavelab.fourier.fourier_coefficients` evaluates
the coefficient integral numerically on a sampled period; the four closed forms are compared
against it. The triangle agrees to better than $10^{-7}$. The square, sawtooth and pulse train
agree only to about one part in $N$, the number of samples — and that gap is the same physics as
the decay table above, seen from the other side. A finite grid cannot resolve a discontinuity,
so the waveforms with jumps are the ones whose numerics are limited.

**2. Convergence rates by smoothness class.** The mean-square error between a partial sum and
its waveform is measured for $N = 15, 31, 63, 127, 255$ and fitted in log-log. The square wave
returns an exponent of $-0.49$ and the triangle $-1.47$, against the predicted $-1/2$ and
$-3/2$. Both sit slightly inside their asymptotes because these orders are finite; carried to
511 harmonics they tighten to $-0.495$ and $-1.484$.

**3. The overshoot that will not move.**

:::{admonition} The measured Gibbs overshoot
:class: numerical-observation
`gibbs_overshoot` locates the first maximum of the square wave's partial sum and reports its
excess over the true value as a fraction of the jump. It returns $9.21\%$ at 7 harmonics,
$8.97\%$ at 31, $8.950\%$ at 127 and $8.9491\%$ at 511 — approaching a constant from above, not
approaching zero. Over the same range the error *energy* falls by a factor of six. Two different
things are being measured, and only one of them is improving.

The measurement has a trap in it worth knowing about. The overshoot moves toward the
discontinuity as $N^{-1}$, so a fixed measurement window eventually misses it entirely and
reports a comfortable, shrinking, wrong number. The window in the library shrinks with $N$ for
exactly that reason.
:::

**4. The driven oscillator, two ways.** The harmonic-sum prediction above is compared against a
direct velocity-Verlet integration of the same oscillator under a sampled square-wave force,
using `oscillators.simulate_forced`. The integrator knows nothing about harmonics — it only
knows the force at each instant — so agreement is a genuine check of the decomposition rather
than a restatement of it. The laboratory sweeps the resonator across the comb and finds the
peaks where the odd harmonics are, and near-silence between them.

(03-fourier-series-transfer)=
## Transfer the idea

- **Standing waves (module `11-standing-waves`).** A string clamped at both ends admits only
  those shapes that fit the boundary — the same discreteness argument that opened this module,
  with $\sin k_n x$ in place of $e^{\ii n\omega_0 t}$. An arbitrary pluck is decomposed into
  modes by an integral that is orthogonality again, and each mode then evolves as its own
  module 01 oscillator.
- **Timbre.** The spectrum *is* what distinguishes a violin from a flute at the same pitch. The
  fundamental sets the note; the pattern of $|c_n|$ sets the instrument. Synthesizers exploit
  this directly, and so does every instrument maker who has ever adjusted a bore or a bridge.
- **Power engineering.** A rectifier draws current in sharp pulses rather than sinusoids, so it
  injects odd harmonics back into the supply, where they heat transformers designed for
  50 or 60 Hz. Harmonic limits are written into grid codes because of the decay table above.
- **Gratings (module `31-gratings`).** The pulse train's comb of harmonics under a
  $\operatorname{sinc}$ envelope reappears as a diffraction pattern: many sharp orders,
  modulated by the transform of a single slit. Same arithmetic, drawn in light.
- **The next module.** Everything here needed exact periodicity. A hand-clap never repeats, and
  the comb of harmonics has to become a continuum. Letting $T \to \infty$ is the whole of
  [module 04](04-fourier-transform.md), and it starts from the formulas on this page.

(03-fourier-series-quiz)=
## Check your understanding

```{include} ../_generated/quiz-03-fourier-series.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](03-fourier-series-problems.md).

(03-fourier-series-explain)=
## Explain it in your own words

Answer in a few sentences each. These are the questions that reveal whether the ideas landed;
no number will save you.

1. A clarinet and a violin play the same written A. Both signals repeat 440 times a second.
   Explain what physically differs between them, and why "they have different pitches" is the
   wrong answer.
2. A sceptic says: "Saying a square wave *contains* 300 Hz is just a way of talking — it is one
   signal at 100 Hz, and the harmonics are bookkeeping." Answer them using the resonator
   experiment, and be clear about what would have to happen for the sceptic to be right.
3. An amplifier is described as overshooting by 9% when fed a square wave. A colleague proposes
   fixing it by extending the bandwidth. What will that actually change, and what will it not?
4. Which bullet of the model specification forbids applying this module's machinery to the sound
   of a single hand-clap, and what goes wrong if you ignore it?

(03-fourier-series-advanced)=
## Advanced: what "equals" is doing in that equation

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section.
:::

**Two senses of convergence.** Writing $f = \sum c_n e^{\ii n \omega_0 t}$ hides a choice. The
series converges to $f$ *in mean square*: the energy of the difference goes to zero, which is
the sense Parseval measures and the sense the $N^{-1/2}$ rate describes. It does not converge
*uniformly* near a jump — the largest pointwise error stays stubbornly at 9% of the jump — and
Gibbs is exactly the gap between those two statements. For continuous, piecewise-smooth signals
the two senses agree and the distinction never surfaces; it surfaces here because a jump is
precisely the case where they part company.

**Averaging beats truncating.** The overshoot is a property of the sharp cutoff, not of the
harmonics. Replace the partial sum by the average of all partial sums up to $N$ — the Fejér, or
Cesàro, sum — and the overshoot vanishes entirely, with convergence now uniform. The cost is
paid at the edges: the Fejér sum is smoother than the signal and rounds the corners it is trying
to reproduce. This is the same trade every window function makes, and
[module 04](04-fourier-transform.md) meets it again under the name of spectral leakage.

**The negative half.** Under the course convention the $n$th harmonic's phasor is $2c_n^{*}$,
which is to say the *negative*-index coefficient carries it: $\hat{f}_n = 2c_{-n}$. The
clockwise half of the sum is module 00's rotating arrow, and the counter-clockwise half is its
mirror, required only to keep the total real. Keeping one half alone gives the analytic signal
that module 00's advanced section previewed. [Module 04](04-fourier-transform.md) closes the thread —
and shows that the same asymmetry is why the spectrum of a real cosine puts its phasor at
$-\omega_0$ rather than at $+\omega_0$.
