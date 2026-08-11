---
title: Problem set — the simple harmonic oscillator
short_title: 01 · Problems
---

# Problem set: the simple harmonic oscillator

Exam-style problems. Work them with a pen before touching a computer; the last one is meant
to be finished numerically. Solutions and marking rubrics live with the instructor material
and are deliberately not on this site.

## Problem 1 — reading the equation of motion

<!-- objectives: OBJ-01-1, OBJ-01-2 -->

A cart of mass $0.50\ \mathrm{kg}$ on a frictionless track is attached to a spring of
stiffness $8.0\ \mathrm{N\,m^{-1}}$. At $t = 0$ it is at $x_0 = +0.10\ \mathrm{m}$ moving
with $v_0 = +0.20\ \mathrm{m\,s^{-1}}$.

(a) Compute $\wnat$, the period, the amplitude and the phase, and write $x(t)$ explicitly.

(b) Find the first time at which the cart passes the origin, and its speed there.

(c) A classmate claims the amplitude is just $x_0$ "because that is where it started".
Produce a one-line counterexample using the given numbers.

## Problem 2 — scaling arguments

<!-- objectives: OBJ-01-1, OBJ-01-3 -->

Without solving any differential equation, use $\wnat = \sqrt{k/m}$ and energy reasoning:

(a) The mass is quadrupled. What happens to the period? To the maximum speed at fixed release
amplitude?

(b) Two identical springs are attached to the same mass, first side by side (parallel), then
end to end (series). Find the ratio of the two oscillation frequencies.

(c) A spring is cut in half and one half is used with the original mass. Does the frequency
rise or fall, and by what factor? (Careful — cutting a spring changes its stiffness.)

## Problem 3 — energy bookkeeping

<!-- objectives: OBJ-01-3, OBJ-01-4 -->

For the cart of Problem 1:

(a) Compute the total energy, and the position(s) where kinetic and potential energy are
equal.

(b) Sketch one full period of $K(t)$ and $U(t)$ on shared axes, marking the times at which
each peaks. At what frequency does each curve oscillate?

(c) Sketch the phase-space orbit, mark the four points corresponding to your answers in (b),
and state in which direction the orbit is traced and why.

## Problem 4 — every valley is a parabola

<!-- objectives: OBJ-01-5 -->

The Lennard-Jones potential
$U(r) = \varepsilon\left[(r_0/r)^{12} - 2\,(r_0/r)^{6}\right]$
models the interaction of two argon atoms, with $\varepsilon = 1.65 \times 10^{-21}$ J and
$r_0 = 3.8 \times 10^{-10}$ m.

(a) Verify that $r_0$ is the equilibrium separation, and compute $U''(r_0)$ in
$\mathrm{N\,m^{-1}}$.

(b) Estimate the vibration frequency of the argon dimer (use the reduced mass), and the
wavelength of light that frequency corresponds to.

(c) State two physical reasons the harmonic prediction must eventually fail for this
potential — one visible in the sketch of $U(r)$, one quantum-mechanical.

## Problem 5 — isochronism on trial, numerically

<!-- objectives: OBJ-01-3, OBJ-01-5 -->

Using `wavelab.oscillators` (in the browser laboratory or locally):

(a) Integrate the linear oscillator at release amplitudes $x_0$ spanning a factor of ten,
fit the period of each trajectory, and report period versus amplitude with uncertainties.

(b) Now integrate the exact pendulum, $\ddot{\theta} = -(g/\ell)\sin\theta$ (write the force
callback yourself, or adapt the laboratory's), for $\theta_0 = 5°, 20°, 45°, 90°$. Measure
the period's growth and compare with $T(\theta_0)/T_{\text{small}} = 1 + \theta_0^2/16 + \cdots$

(c) At what amplitude does the pendulum's period first deviate from the small-angle value by
more than $1\%$? By more than the uncertainty of your period fit? Write two sentences on
what "isochronism is an approximation" now means, quantitatively.
