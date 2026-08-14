---
title: Problem set — Fourier series
short_title: 03 · Problems
---

# Problem set: Fourier series

Exam-style problems. Work them with a pen before touching a computer; the last two are meant to
be finished numerically. Solutions and marking rubrics live with the instructor material and are
deliberately not on this site.

Throughout, the course convention holds: a periodic signal of period $T$ is written
$f(t) = \sum_n c_n e^{\ii n\omega_0 t}$ with $\omega_0 = 2\pi/T$, its coefficients are
$c_n = \frac{1}{T}\int_T f(t)\, e^{-\ii n\omega_0 t}\,\mathrm{d}t$, and the $n$th harmonic's
phasor is $\hat{f}_n = 2c_n^{*}$.

## Problem 1 — two waveforms, one method

<!-- objectives: OBJ-03-1, OBJ-03-5 -->

(a) Compute the coefficients of the sawtooth ramp that rises linearly from $-1$ to $+1$ across
each period. Show that every harmonic is present and that $|c_n| \propto 1/n$, and say which
symmetry the square wave has that this one lacks.

(b) Compute the coefficients of a pulse train that equals $1$ for a fraction $d$ of each period,
centred on $t = 0$, and $0$ otherwise. Show that
$c_n = d\,\operatorname{sinc}(nd)$ with the normalised sinc, and locate the zeros of the
envelope.

(c) Sketch both spectra. As $d \to 0$ at fixed pulse *area*, describe what happens to the
envelope, and say in one sentence what that implies about how much bandwidth a short pulse
needs. (You have just anticipated the central result of module `04-fourier-transform`.)

## Problem 2 — symmetry does the integrals

<!-- objectives: OBJ-03-2 -->

(a) Show that an even signal has purely real coefficients and an odd signal purely imaginary
ones, using $c_{-n} = c_n^{*}$ and the substitution $t \to -t$.

(b) Prove that half-wave symmetry, $f(t + T/2) = -f(t)$, forces $c_n = 0$ for all even $n$.

(c) Classify each of the following by inspection, stating which harmonics survive and whether
the coefficients are real, imaginary or neither: a square wave shifted so that it is even about
$t = 0$; a full-wave-rectified sine, $|\sin \omega t|$; a sawtooth; a pulse train of duty cycle
$1/2$.

(d) A signal has both half-wave symmetry and evenness. What is left, and what is the lowest
harmonic that can be nonzero?

## Problem 3 — Parseval and the energy budget

<!-- objectives: OBJ-03-1, OBJ-03-3 -->

(a) Derive Parseval's relation for a Fourier series, $\frac{1}{T}\int_T |f|^2\,\mathrm{d}t
= \sum_n |c_n|^2$, using orthogonality. Say in one sentence what it means physically.

(b) Apply it to the square wave of the page and deduce
$\sum_{n \text{ odd}} 1/n^2 = \pi^2/8$.

(c) What fraction of a square wave's power sits in the fundamental alone? In the first three
nonzero harmonics? Comment on how well the ear's impression of "a square wave" matches that
budget.

(d) Relate the mean-square error of the $N$-term partial sum to the tail $\sum_{|n|>N}|c_n|^2$,
and use the $1/n$ decay to recover the $N^{-1/2}$ rate quoted in the verify section.

## Problem 4 — rounding the corner, numerically

<!-- objectives: OBJ-03-3, OBJ-03-5 -->

Using `wavelab.fourier` (in the browser laboratory or locally):

(a) Build a square wave whose jumps have been smoothed over a width $\varepsilon$ of a period —
replace each jump by a linear ramp, or by $\tanh(t/\varepsilon)$, and say which you chose.
Compute its coefficients with `fourier_coefficients` for $\varepsilon = 0.1, 0.03, 0.01$.

(b) Plot $|c_n|$ against $n$ on log-log axes for each $\varepsilon$. Identify the crossover
harmonic $n^{*}$ beyond which the decay steepens, and show that $n^{*} \sim 1/\varepsilon$.

(c) Explain the result in one paragraph: a signal that is smooth on a fine scale still looks
discontinuous to harmonics too coarse to resolve that scale. What does this say about the
bandwidth a real amplifier needs to reproduce a real, not-quite-square, square wave?

## Problem 5 — a bank of resonators as a Fourier analyser

<!-- objectives: OBJ-03-4, OBJ-03-1 -->

Using `wavelab.oscillators` and `wavelab.fourier`:

(a) Drive an oscillator of quality factor $Q = 30$ with a square wave of repetition rate
$\omega_0$, and sweep the resonator's natural frequency $\wnat$ from $0.5\omega_0$ to
$10\omega_0$. Plot the steady-state RMS displacement against $\wnat$ using
`steady_state_response` harmonic by harmonic.

(b) Confirm the peaks fall on the odd harmonics only, and that the peak heights are in the ratio
$1 : 1/3 : 1/5 : \dots$ once the resonance gain is divided out. Measure the response at
$\wnat = 4\omega_0$ and express it as a fraction of the response at $3\omega_0$.

(c) Cross-check one point of the sweep against a direct integration with `simulate_forced`, and
explain why that check is worth doing at all — what could the harmonic-sum calculation get wrong
that the integration would catch?

## Problem 6 — challenge: averaging away the overshoot

<!-- objectives: OBJ-03-3 -->

(a) Define the Fejér sum $\sigma_N$ as the average of the partial sums $S_0, \dots, S_N$. Show
that it can be written as a single weighted sum over harmonics, and identify the weights.

(b) Show that $\sigma_N$ is the convolution of $f$ with a kernel that is *non-negative*
everywhere, and explain why non-negativity forbids an overshoot: a weighted average with
positive weights cannot exceed the largest value being averaged.

(c) Compute $S_{31}$ and $\sigma_{31}$ for the square wave and plot both near a jump. Confirm the
overshoot is gone. Then measure what it cost — compare the two at the *corner* of a triangle
wave, and state the trade in one sentence.
