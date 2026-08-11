---
title: Problem set — phasors
short_title: 00 · Problems
---

# Problem set: phasors

Exam-style problems. Work them with a pen before touching a computer; the last one is meant
to be finished numerically. Solutions and marking rubrics live with the instructor material
and are deliberately not on this site.

Throughout, the course convention holds: phasor $\hat{x} = A e^{-\ii\varphi}$ for the
oscillation $A\cos(\omega t + \varphi)$.

## Problem 1 — the representation, both ways

<!-- objectives: OBJ-00-1, OBJ-00-5 -->

(a) Write the phasors of $3\cos(\omega t)$, $3\sin(\omega t)$, and
$3\cos(\omega t - 2\pi/3)$, and draw all three arrows.

(b) A phasor is $\hat{x} = -2\ii$. Write the oscillation $x(t)$ it represents, and state at
what time (in units of the period, starting from $t = 0$) the signal first reaches its
maximum.

(c) A classmate using the engineering convention writes the phasor of
$3\sin(\omega t)$ and gets the complex conjugate of your answer to (a). Explain in one
sentence why, and why neither of you is wrong.

## Problem 2 — the interference law

<!-- objectives: OBJ-00-2 -->

Two same-frequency oscillations have amplitudes $A_1 = 3$ and $A_2 = 4$ (same units).

(a) What are the largest and smallest amplitudes their sum can have, and at what phase
differences do they occur?

(b) Find the phase difference at which the sum has amplitude exactly $5$, and notice which
famous triangle you have just drawn.

(c) For equal amplitudes $A_1 = A_2 = a$, show that the resultant amplitude is
$2a\left|\cos(\delta/2)\right|$, and check both extremes against (a)-style reasoning.

## Problem 3 — beats at the tuning fork

<!-- objectives: OBJ-00-3 -->

A violinist tunes the A string against a 440 Hz fork and hears the loudness pulse 2.0 times
per second.

(a) What are the two possible frequencies of the string?

(b) The player tightens the string slightly and the pulsing *speeds up*. Which of the two was
it, and what should the player do instead?

(c) The pulsing slows to one beat every 4 s and then the player stops adjusting. Estimate how
far from 440 Hz the string is, and how long you would have to listen to notice the residual
detuning at all.

## Problem 4 — one hundred sources

<!-- objectives: OBJ-00-2, OBJ-00-4 -->

$N = 100$ identical emitters each produce, at a distant detector, a unit-amplitude
oscillation of the same frequency.

(a) The emitters are phase-locked ($\varphi_k = 0$ for all $k$). What amplitude and what
intensity (in units of one emitter's) arrive at the detector?

(b) The phases are instead independent and uniformly random. What is the *expected*
intensity? Derive it from the double sum over cross terms, stating exactly which average
vanishes.

(c) The random-phase resultant amplitude is itself random: about how large are its typical
fluctuations from one realisation to the next, relative to its RMS value? (A qualitative
answer with a reason suffices — this is the seed of the speckle phenomenon, module 8.)

## Problem 5 — the phasor polygon, numerically

<!-- objectives: OBJ-00-2, OBJ-00-4 -->

Using `wavelab.phasors` (in the browser laboratory or locally):

(a) Compute the resultant of $N$ unit phasors with phases $\varphi_k = k\,\delta$ for
$k = 0, \dots, N-1$ (a fixed phase *step* — arrows forming a regular polygon) for $N = 6$ and
a range of $\delta$. At which values of $\delta$ does the resultant vanish exactly? Compare
with $\left|\sin(N\delta/2)/\sin(\delta/2)\right|$.

(b) Repeat with random phases at $N = 10, 100, 1000$, averaging $\left|\text{sum}\right|^2$
over at least 50 seeds, and fit the scaling exponent of RMS amplitude versus $N$.

(c) The pattern in (a) is the diffraction grating of module 9 in disguise; the scaling in
(b) is incoherent light. In two sentences, connect each computation to its optics future.
