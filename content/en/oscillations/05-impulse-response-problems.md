---
title: "Problem set — impulse response and convolution"
short_title: 05 · Problems
---

# Problem set: impulse response and convolution

Exam-style problems. Work them with a pen before touching a computer; the last two are meant
to be finished numerically. Solutions and marking rubrics live with the instructor material
and are deliberately not on this site.

Throughout, $\gamma \equiv b/m$, $Q = \wnat/\gamma$, and the forward transform carries
$e^{-\ii\omega t}$, so that $\hat{G}(\omega) = (1/m)/(\wnat^2 - \omega^2 + \ii\gamma\omega)$
and module 02's swept amplitude is its conjugate. If a term's sign surprises you, check that
convention first — it is the one thing in this module that reliably goes wrong quietly.

## Problem 1 — the step response, by convolution

<!-- objectives: OBJ-05-1, OBJ-05-2 -->

A force $F_0$ is switched on at $t = 0$ and left on. The oscillator starts at rest.

(a) Write down $G(t)$ and confirm the three things it must do at $t = 0^+$: vanish, leave the
origin at slope $1/m$, and carry no dependence on $k$ in that slope.

(b) Evaluate $x(t) = \int_0^t G(t - t')F_0\,dt'$ directly and obtain

$$
x(t) = \frac{F_0}{k}\left[1 - e^{-\gamma t/2}\left(\cos\omega_d t
+ \frac{\gamma}{2\omega_d}\sin\omega_d t\right)\right].
$$

Check the two limits you can check without doing any work: $t \to \infty$, and $\gamma \to 0$.

(c) Locate the first maximum and show that the fractional overshoot is
$\exp\!\left(-\pi\gamma / 2\omega_d\right)$, a function of $Q$ alone. Evaluate it at $Q = 20$,
$Q = 2$ and at critical damping.

(d) A galvanometer needle must reach its final reading as fast as possible without ever
passing it. What $Q$ do you specify, and what does the answer to (c) say about $Q$ slightly
below that value?

## Problem 2 — kick timing

<!-- objectives: OBJ-05-2, OBJ-05-4 -->

Two identical kicks of impulse $J$ arrive, the second a time $\tau$ after the first.

(a) Write the motion for $t > \tau$ as a single decaying sinusoid. Give its amplitude as a
function of $\tau$, and identify the two competing effects that decide it.

(b) Show that the amplitude ratio against a single kick is $1 + e^{-\pi/Q}$ for
$\tau = T_d$ and $1 - e^{-\pi/2Q}$ for $\tau = T_d/2$, where $T_d = 2\pi/\omega_d$. Evaluate
both at $Q = 10$.

(c) Half-period spacing does not cancel the motion completely, at any finite $Q$. Explain why
in one sentence, and state the condition under which cancellation would be exact.

(d) You may choose $\tau$ freely to make the ringing at late times as *large* as possible for
two kicks of fixed impulse. Is $\tau = T_d$ optimal? Justify your answer — the reasoning
matters more than the number.

## Problem 3 — causality and what it forbids

<!-- objectives: OBJ-05-4 -->

(a) State the causality condition on $G$ and show that it is what puts the upper limit $t$ on
the convolution integral.

(b) Someone reports a measured impulse response that is small but nonzero for $t < 0$, and
attributes it to their apparatus. Give two mundane experimental explanations before reaching
for new physics.

(c) The equation $m\ddot{G} + b\dot{G} + kG = \delta(t)$ also admits the *advanced* solution,
zero for $t > 0$. Write it down and describe the motion it represents.

(d) Suppose the advanced solution were the physical one. Describe a machine you could build,
and say which conservation law — if any — it violates. (It is not energy. That is the point.)

## Problem 4 — the frequency response, two ways

<!-- objectives: OBJ-05-3, OBJ-05-5 -->

(a) Evaluate $\hat{G}(\omega) = \int_0^\infty G(t)e^{-\ii\omega t}\,dt$ and obtain
$(1/m)/(\wnat^2 - \omega^2 + \ii\gamma\omega)$. The integral is module 04's one-sided
exponential pair applied twice; say where the $\sin\omega_d t$ was split.

(b) Show that $X(\omega) = F_0\hat{G}(\omega)^{*}$, and explain the conjugate in terms of
which half of the spectrum the course's time factor $e^{-\ii\omega t}$ occupies.

(c) A force $F(t) = F_0 e^{-t/\tau}$ for $t \ge 0$ is applied. Find $x(t)$ twice — once by
convolution, once as the inverse transform of $\hat{G}\hat{F}$ — and show the two agree. State
which is less work and why.

(d) A series RLC circuit has $L = 10\ \mathrm{mH}$, $R = 2.0\ \Omega$ and
$C = 1.0\ \mathrm{\mu F}$. Find $f_0$ and $Q$, then give the $(m, b, k)$ of a mechanical
oscillator with the identical $G(t)$ when $x$ is measured in metres and $q$ in coulombs.

## Problem 5 — measuring $Q$ from one kick, numerically

<!-- objectives: OBJ-05-1, OBJ-05-3 -->

Simulate a ringdown of an oscillator with $Q = 15$, sampled well above $\omega_d$, and add
Gaussian noise at $0.5\%$ of the initial amplitude. Use a fixed seed and say what it is.

(a) Extract $Q$ from the envelope with `oscillators.q_from_ringdown`, and again from the
linewidth with `oscillators.q_from_linewidth` applied to `fourier.spectrum` of the same
record. Report both as value $\pm$ uncertainty over at least eight seeds.

(b) Now apply `oscillators.q_from_bandwidth` to the same spectrum. It will return a number
without complaint. Compute how many frequency bins lie across the full width of your line, and
use that to explain the discrepancy.

(c) Show that the number of bins across the linewidth depends only on how many amplitude
e-foldings your record contains, and not on $Q$. Deduce the record length needed for ten bins,
and the signal amplitude remaining at that point.

(d) Zero-pad the record by a factor of eight and repeat (b). The estimate improves. Explain
carefully why this is *not* the same as having recorded more data.

## Problem 6 — synthesis: a square wave through a resonator

<!-- objectives: OBJ-05-2, OBJ-05-3 -->

This one problem uses every module so far. A damped oscillator with $Q = 12$ is driven by a
square wave of fundamental frequency $\wnat/3$ and amplitude $F_0$, with a little noise added.

(a) Expand the square wave in a Fourier series (module 03) and predict the steady-state
response as a sum of harmonics, each weighted by module 02's $X$ at that harmonic's frequency.
Which harmonic dominates, and by what factor over the fundamental?

(b) **Watch the sign.** Module 03's synthesis writes the drive as $\sum_n c_n e^{+\ii n\omega_0 t}$,
which under this course's kernel places the $n$th harmonic at $\omega = -n\omega_0$. Show that
the correct weight for that term is $X(n\omega_0)^{*}$, not $X(n\omega_0)$, and state what the
response would look like if you used the wrong one.

(c) Compute the response numerically three ways: by summing the harmonics of (a), by
`oscillators.convolution_response`, and by `oscillators.simulate_forced`. Show all three agree
in the steady state, and say what limits the agreement in each case.

(d) Transform the computed response and compare its spectrum with the product
$\hat{G}\hat{F}$. Then explain, in two sentences, why a resonator driven by a square wave is
heard as very nearly a pure tone.

## Problem 7 — challenge: deconvolution and its limits

<!-- objectives: OBJ-05-3, OBJ-05-4 -->

You are given a measured $x(t)$ and a known $\hat{G}$, and asked to recover the force.

(a) Implement $\hat{F} = \hat{x}/\hat{G}$ by spectral division on noiseless simulated data and
confirm you recover the input force.

(b) Add Gaussian noise at $10^{-6}$, $10^{-4}$ and $10^{-2}$ of the peak response and repeat.
Plot the recovered force in each case and report its peak magnitude.

(c) Explain the failure quantitatively: relate the amplification of the noise at each
frequency to $|\hat{G}(\omega)|$, and identify the frequency band that does the damage.

(d) Rescue it crudely by zeroing every frequency where $|\hat{G}|$ falls below a threshold you
choose. Show the result is bounded, and state precisely what has been thrown away along with
the noise. What extra information would let you do better? Module `53-computational-imaging`
answers this properly; give your own answer first.
