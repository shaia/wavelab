---
title: "Problem set — coupled oscillators"
short_title: 06 · Problems
---

# Problem set: coupled oscillators

Exam-style problems. Work them with a pen before touching a computer; the last two are meant
to be finished numerically. Solutions and marking rubrics live with the instructor material
and are deliberately not on this site.

Throughout, two masses $m$ are each anchored by a spring of stiffness $k$ and joined by a
coupling spring $k_c$, so that $\wnat = \sqrt{k/m}$, $\omega_s = \wnat$ and
$\omega_a = \sqrt{(k + 2k_c)/m}$.

## Problem 1 — unequal masses

<!-- objectives: OBJ-06-1, OBJ-06-2 -->

Replace the second mass by $2m$, leaving both anchor springs and the coupling spring unchanged.

(a) Write $M$ and $K$. Note that $M$ is no longer a multiple of the identity, and say which
step of the module's derivation used that fact.

(b) Find the two frequencies from $\det(K - \omega^2 M) = 0$. Verify that they reduce to the
module's answers when the second mass is returned to $m$.

(c) Find the two mode shapes. Show that neither is $(1, \pm 1)$ any more, and say which mass
moves further in each mode. Is the heavier or the lighter mass the one with the larger
amplitude in the *lower*-frequency mode?

(d) The module argued that the symmetric mode keeps $\wnat$ because the coupling spring never
stretches. Does that argument survive unequal masses? Explain what breaks.

## Problem 2 — energy in the normal coordinates

<!-- objectives: OBJ-06-4 -->

(a) Starting from $q_\pm = (x_1 \pm x_2)/\sqrt2$, show that
$\tfrac12 m(\dot{x}_1^2 + \dot{x}_2^2) = \tfrac12 m(\dot{q}_+^2 + \dot{q}_-^2)$ — the kinetic
energy has the same form in either set of coordinates.

(b) Show that the potential energy becomes
$\tfrac12 k q_+^2 + \tfrac12 (k + 2k_c)\,q_-^2$, with **no cross term** in $q_+q_-$. The
absence of that term is the whole content of "the modes are independent"; say why.

(c) Conclude that $E_+ = \tfrac12 m\dot{q}_+^2 + \tfrac12 k q_+^2$ and its partner are each
separately conserved, and that the total is their sum.

(d) The site energies of the two masses are *not* separately conserved. Reconcile this with
(c) in one sentence: both statements are about the same motion.

## Problem 3 — reading a measurement

<!-- objectives: OBJ-06-3, OBJ-06-5 -->

A student reports that in their apparatus the energy takes $12.0\ \mathrm{s}$ to travel from
one pendulum to the other and back, and that a single pendulum, with its partner clamped, has a
period of $1.50\ \mathrm{s}$.

(a) Find $\omega_s$, $\Delta\omega$, and $\omega_a$.

(b) Is this pair weakly or strongly coupled? Justify by a number, not an impression.

(c) Estimate $k_c/k$. State which approximation you used and check afterwards that the
conditions for it hold.

(d) The student wants the exchange to take $3.0\ \mathrm{s}$ instead. By what factor must
$k_c$ change? What happens to $\omega_s$?

## Problem 4 — three pendulums by symmetry

<!-- objectives: OBJ-06-1, OBJ-06-2 -->

Three identical masses in a row, each anchored by a spring $k$, with coupling springs $k_c$
between neighbours 1–2 and 2–3 but *not* between 1 and 3.

(a) Write $M$ and $K$.

(b) Without computing a determinant, guess the three mode shapes from the symmetry of the
arrangement. (Hint: the system is unchanged if you reflect it left-to-right, so each mode must
be either unchanged or exactly reversed by that reflection.)

(c) Verify your guesses by substituting each into $(K - \omega^2 M)\mathbf{a} = 0$ and reading
off the frequency. Order them.

(d) In one of your three modes the middle mass does not move at all. Which one, and what is its
frequency? Explain that frequency in one sentence without algebra.

## Problem 5 — the exchange-time law and where it fails

<!-- objectives: OBJ-06-3, OBJ-06-5 -->

Using `coupled.two_mass_matrices` and `coupled.normal_mode_solve`:

(a) Compute $T_{\text{ex}}$ across $k_c/k$ from $0.002$ to $2$ and plot it on log-log axes.
Fit a straight line to the weak-coupling end and report the exponent.

(b) The predicted exponent is $-1$. Over what range of $k_c/k$ does your fit stay within 2% of
it? Mark that range on the plot.

(c) Derive the exact $T_{\text{ex}}(k_c)$ without approximating, and overlay it. Explain the
shape of the departure at large $k_c$ from the exact expression.

(d) Show that as $k_c \to \infty$ the exchange time approaches zero but the *fraction* of
energy transferred does not approach one. Compute that fraction at $k_c/k = 1$ and at
$k_c/k = 10$ by simulation, using `coupled.site_energies`.

## Problem 6 — synthesis: driving the pair

<!-- objectives: OBJ-06-2, OBJ-06-3 -->

This problem uses every module so far. Attach a drive $F_0\cos\omega t$ to mass 1 only, and add
light damping $b$ to both masses, so that a steady state exists.

(a) In normal coordinates, show that the drive on mass 1 alone excites **both** modes, each
with weight $1/\sqrt2$. This is the same decomposition the start-one experiment used, now for a
force rather than an initial condition.

(b) Each normal coordinate is therefore a module-02 driven oscillator. Predict the steady-state
response of mass 1 as a sum of two Lorentzian resonances centred on $\omega_s$ and $\omega_a$,
using `oscillators.driven_amplitude` at each mode's frequency. Sketch it.

(c) Verify by direct integration of the damped, driven coupled equations, sweeping $\omega$ and
recording the steady-state amplitude after the transient has died. Compare with (b).

(d) Under what condition on $b$ do the two peaks appear as two, rather than merging into one?
Express the condition as a comparison between the mode splitting and a quantity from module 02,
and check it numerically by raising $b$ until the two peaks merge.

## Problem 7 — challenge: damping that preserves the modes

<!-- objectives: OBJ-06-4 -->

Add damping to the pair as $M\ddot{\mathbf{x}} + C\dot{\mathbf{x}} + K\mathbf{x} = 0$.

(a) Show that if $C = \alpha M + \beta K$ for constants $\alpha, \beta$, the normal coordinates
of the undamped problem still decouple the damped one, each becoming an independent module-02
damped oscillator. This is called Rayleigh damping.

(b) Find the quality factor of each mode in terms of $\alpha$, $\beta$ and that mode's
frequency. Do the two modes share a $Q$?

(c) Construct an explicit $C$ that is symmetric, positive definite, and *not* of that form.
Show numerically that the modal energies are then no longer independently decaying — energy
moves between modes.

(d) The module's model specification lists "damping added naively" as a failure mode. In the
light of (c), state precisely what "naively" means, and what a modeller should check before
assuming a damped coupled system still has normal modes.
