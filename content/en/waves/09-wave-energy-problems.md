---
title: "Problem set — wave energy"
short_title: 09 · Problems
---

# Problem set: wave energy

Exam-style problems. Work them with a pen before touching a computer; problems 6 and 7 are
meant to be finished numerically. Solutions and marking rubrics live with the instructor
material and are deliberately not on this site.

Throughout, a string has tension $T$ and linear mass density $\mu$, so that

$$
v = \sqrt{\frac{T}{\mu}},
\qquad
u_K = \tfrac12\,\mu\,y_t^2,
\qquad
u_P = \tfrac12\,T\,y_x^2,
\qquad
P = -T\,y_x\,y_t .
$$

## Problem 1 — the stretch, and what it stores

<!-- objectives: OBJ-09-2 -->

(a) A piece of string of rest length $\mathrm{d}x$ is tilted to a slope $y_x$. Write its true
length, and show that the work done against a constant tension $T$ in stretching it is
$\tfrac12 T y_x^2\,\mathrm{d}x$ to leading order. State the size of the first term you dropped,
relative to the one you kept.

(b) A guitar string of length $L = 650$ mm and $\mu = 1.1$ g/m under $T = 75$ N is pulled
3.0 mm sideways at its midpoint into a triangle and released. Find the total energy stored,
using the triangle's two constant slopes, and express it in millijoules.

(c) Show that the answer to (b) can be written $2Th^2/L$ for a pluck of height $h$ at the
midpoint, and explain why it does not depend on $\mu$. What *does* $\mu$ decide about the
motion that follows?

(d) The same string is now lifted bodily, whole, 3.0 mm to one side while staying straight.
How much energy is stored? Reconcile your answer with the intuition that the string "has been
displaced".

## Problem 2 — the flux, from first principles

<!-- objectives: OBJ-09-3 -->

(a) Draw a cut through the string at $x$, and the tension with which the left piece pulls the
right one. Resolve it into components and show that the transverse component is $-T y_x$ for
small slopes.

(b) The point at the cut moves at $y_t$. Write the rate at which the left piece does work on the
right one, and show it is $P = -T y_x y_t$. Confirm from your own expression that $P$ is
positive when a right-moving wave passes.

(c) A snapshot of a string shows, at one point, a slope of $+0.012$ and a transverse velocity of
$-0.30$ m/s, on a string with $T = 20$ N. Find $P$ there, state which way the energy is going,
and say whether this point belongs to a wave moving right, left, or neither. What extra piece of
information would settle that last question?

(d) Show that $P = -T y_x y_t$ has the dimensions of power, working from the dimensions of $T$
alone.

## Problem 3 — continuity, checked by hand

<!-- objectives: OBJ-09-3, OBJ-09-4 -->

Let $y(x,t) = f(x - vt)$ for an arbitrary twice-differentiable $f$.

(a) Write $u_K$, $u_P$ and $P$ in terms of $f'$ alone, and verify $u_K = u_P$ and $P = v u$
without assuming anything about the shape of $f$.

(b) Verify by direct differentiation that $\partial u/\partial t + \partial P/\partial x = 0$.

(c) Now let $y = f(x - vt) + g(x + vt)$ with both pieces present. Show that $u$ picks up a cross
term while $P$ picks up a different one, that $u_K = u_P$ no longer holds pointwise, and that
the continuity equation holds anyway.

(d) Explain in one sentence why (c) had to come out that way, given that the wave equation is
linear but the energy is quadratic.

## Problem 4 — mean power, three ways

<!-- objectives: OBJ-09-4 -->

(a) A string carries $y = \Real[A e^{\ii(kx - \omega t)}]$. Derive
$\langle P\rangle = \tfrac12 \mu v \omega^2 |A|^2$, stating where the factor of one half comes
from.

(b) Rewrite the result in terms of the impedance $Z = \sqrt{T\mu}$ and the peak transverse
speed, and again in terms of $T$, $v$ and the wavenumber $k$. Check that all three have the
dimensions of power.

(c) A rope with $\mu = 0.080$ kg/m under 120 N is shaken at 8.0 Hz with an amplitude of 25 mm.
Find $v$, $\lambda$, and the average power the shaker must supply. Then find the amplitude that
would halve the power at the same frequency, and the frequency that would halve it at the same
amplitude.

(d) A *triangular* wave of peak height $A$ and wavelength $\lambda$ travels along the string —
straight segments alternating in slope. Find its mean power without any Fourier analysis, and
express the answer as a numerical multiple of $\tfrac12\mu v \omega^2 A^2$ for the sinusoid of
the same peak height and wavelength. Which carries more, and why is that the answer you should
have expected from $u_P \propto y_x^2$?

## Problem 5 — three velocities, and which can outrun which

<!-- objectives: OBJ-09-1 -->

(a) For a right-moving wave, show $y_t = -v\,y_x$ and hence that the ratio of the fastest
transverse speed to the wave speed is exactly the steepest slope.

(b) A wave on a string has $v = 20$ m/s, $A = 2.0$ mm and $f = 50$ Hz. Find the peak transverse
speed, the steepest slope, and the energy transport velocity. Which two of your four numbers
are the same, and which is free?

(c) Find the amplitude at which the peak transverse speed would equal $v$, at this frequency,
and the slope that amplitude implies. What has gone wrong with the model by then, and what
physically would happen to such a string?

(d) A student concludes that since energy travels at $v$ and $v$ can be made arbitrarily large
by tightening the string, energy could be sent faster than light. Identify the first assumption
in this module that fails, and say what actually limits $v$ for a real material.

## Problem 6 — the energy budget of a pluck

<!-- objectives: OBJ-09-2, OBJ-09-4 -->

A long string is plucked into a symmetric hump $y_0(x)$ and released from rest.

(a) Argue, without computing anything, that at $t = 0$ the string's energy is entirely
potential, and that some time later it is half kinetic and half potential. Say what happens in
between, and what fixes the time scale of the changeover.

(b) Using d'Alembert's solution, show that once the two half-height copies have separated, each
carries a quarter of the original potential energy as $u_K$ and a quarter as $u_P$. Verify that
the four quarters add to the energy you started with.

(c) Numerically: launch a Gaussian pluck with `waves.simulate_string`, and plot
$\int u_K\,\mathrm{d}x$ and $\int u_P\,\mathrm{d}x$ against time on one axis. Mark the moment
they cross, and compare it with your estimate from (a).

(d) The two half-copies each have half the height of the original. Half the height is a quarter
of the energy density, and there are two of them — so the travelling energy is half of what was
put in. Where is the other half? Answer with the plot from (c), not with words alone.

## Problem 7 — metering power through noise

<!-- objectives: OBJ-09-3, OBJ-09-5 -->

A sinusoidal train of amplitude $A$ passes a gate. The only data are the displacements of three
neighbouring grid points, spacing $\Delta x$, sampled every $\Delta t$, each carrying
independent Gaussian noise of standard deviation $\sigma$.

(a) One estimator forms $y_x$ from the two spatial neighbours and $y_t$ from the two temporal
neighbours, then takes $P = -T y_x y_t$. Show that its expected value is the true mean power,
and identify which property of the two finite differences makes the noise cross term vanish.

(b) A second estimator uses $P = T v\,y_x^2$, which is exact algebra for a right-mover. Show
that its expected value exceeds the truth by $T v\,\sigma^2/(2\Delta x^2)$, and that this offset
does not shrink as more samples are averaged.

(c) With $T = 4$ N, $v = 20$ m/s, $\Delta x = 6.25$ mm and $\sigma$ equal to 5% of a 2 mm
amplitude, evaluate the offset and compare it with $\tfrac12\mu v\omega^2A^2$ at 50 Hz. Is the
second estimator's error a small correction or a serious one?

(d) Propose a way to repair the second estimator using only the data it already has, and state
what new assumption your repair introduces. (Hint: the offset depends on $\sigma$, which the
same records can be made to reveal.)

(e) State the general rule this problem illustrates, in one sentence, in a form that would warn
someone measuring the intensity of light with a noisy photodetector.

## Problem 8 — challenge: does the wave push the string along?

<!-- objectives: OBJ-09-1 -->

This problem has no clean answer, and the point is to find out precisely why.

(a) The transverse momentum of a stretch of string is $\int \mu\,y_t\,\mathrm{d}x$. Evaluate it
for a pulse $y = f(x - vt)$ that starts and ends flat, and interpret the result.

(b) Now consider longitudinal motion. Show that if a string element is inextensible, a
transverse displacement of slope $y_x$ must pull its ends toward each other by an amount of
order $y_x^2$ per unit length, and hence that any longitudinal effect is second order in the
slope.

(c) Identify every place in this module's derivations where a term of order $y_x^2$ relative to
the leading one was discarded. Explain why this means the ideal-string model cannot be asked
about longitudinal momentum, even though it can be asked about energy.

(d) Read D. R. Rowland, *"The potential energy density in transverse string waves depends
critically on longitudinal motion,"* Eur. J. Phys. **32**, 1475 (2011). In half a page, state
what is at stake, which of this module's results survive the paper's argument untouched, and
which of them the paper shows to be convention rather than fact.

(e) Write one sentence explaining the difference between "physics does not know the answer" and
"this model cannot represent the question". Which one is the case here?

## Problem 9 — two velocities from one video

<!-- objectives: OBJ-09-1, OBJ-09-2 -->

Use the slinky footage of module 08's problem 5: a slinky stretched to $L = 4.0$ m along a
smooth floor, filmed at 240 frames per second, with tape marks every 0.50 m and a small flag
taped to one coil near the middle.

(a) The flag's sideways position is read off each frame. Over the eleven frames while the pulse
passes, it rises from 0 to 42 mm and returns. Estimate the flag's greatest transverse speed, and
compare it with the pulse speed you measured in module 08 (3.00 m in 69 frames). Which of the
module's three velocities have you now measured, and which have you not?

(b) Use $y_t = -v\,y_x$ to convert your answer to (a) into the pulse's steepest slope. Is the
small-slope assumption safe on this slinky? Give the size of the largest term the model drops.

(c) The slinky has mass $M = 0.22$ kg. Using $\mu = M/L$ and the speed from module 08, estimate
the tension, then estimate $u_K$ at the flag at the instant it was moving fastest. Say which of
your inputs your answer is most sensitive to.

(d) You want to measure the flux $P$ directly. Explain what two quantities you would have to
read off the same frame, at the same place, and why the product of two noisy small numbers is
harder to measure well than either of them — referring to problem 7 for the direction the error
goes.

(e) Design an experiment that measures the energy the pulse delivered *without* measuring $P$ at
all: something at the far end that the arriving pulse visibly moves, whose energy you can
compute afterwards. State what you would have to calibrate, and what you would compare your
answer with.
