---
title: "Problem set — normal modes and the N-mass chain"
short_title: 07 · Problems
---

# Problem set: normal modes and the N-mass chain

Exam-style problems. Work them with a pen before touching a computer; the last three are meant
to be finished numerically. Solutions and marking rubrics live with the instructor material
and are deliberately not on this site.

Throughout, a chain means $N$ equal masses $m$ joined by identical springs of stiffness $k_s$
at spacing $a$, with the ends fixed unless stated otherwise, so that

$$
\omega_p = 2\sqrt{\frac{k_s}{m}}\sin\!\left(\frac{p\pi}{2(N+1)}\right),
\qquad
a_p(j) \propto \sin\!\left(\frac{p\pi j}{N+1}\right),
\qquad
c = a\sqrt{\frac{k_s}{m}} .
$$

## Problem 1 — verifying the ansatz

<!-- objectives: OBJ-07-3 -->

(a) Write down the equation of motion for mass $j$ of a fixed-end chain, and say precisely what
role the conditions $x_0 = x_{N+1} = 0$ play — they are not equations of motion.

(b) Substitute $x_j = a(j)\cos\omega t$ and reduce the problem to a recursion in $a(j)$ alone.

(c) Show that $a_p(j) = \sin(p\pi j/(N+1))$ satisfies both end conditions for every integer
$p$, and that it satisfies the interior recursion for the $\omega_p$ quoted above. (Hint:
$\sin(\theta + \varphi) + \sin(\theta - \varphi) = 2\sin\theta\cos\varphi$.)

(d) Show that $p$ and $p + 2(N+1)$ describe the same motion, and that $p = N+1$ describes no
motion at all. Conclude that there are exactly $N$ modes and not more, and say why that number
had to come out equal to the number of masses.

## Problem 2 — three masses by hand, shapes first

<!-- objectives: OBJ-07-1, OBJ-07-3 -->

Take $N = 3$.

(a) Before computing anything, sketch the three mode shapes from the closed form and order
them by frequency. State the number of interior nodes in each.

(b) Write $M$ and $K$ and expand $\det(K - \omega^2 M) = 0$. You will get a cubic; factor it
using the shape you sketched for the middle mode as a hint about one of its roots.

(c) Show that the three roots are $\omega = \sqrt{k_s/m}\,\{\sqrt{2 - \sqrt2},\ \sqrt2,\
\sqrt{2 + \sqrt2}\}$, and check them against the closed form.

(d) In the middle mode, the central mass does not move. Explain that in one sentence without
algebra, and say what it means for the frequency of that mode — which is the same as some
simpler system's.

## Problem 3 — the free–free chain

<!-- objectives: OBJ-07-1, OBJ-07-6 -->

Remove both walls, leaving $N$ masses joined by $N-1$ springs.

(a) Write $K$ and show that every row sums to zero. Deduce that $\mathbf{a} = (1,1,\dots,1)$ is
a mode with $\omega = 0$.

(b) Show that the modal coordinate of the zero mode is proportional to the total momentum
divided by the total mass, and that the equation of motion for it, $\ddot q_0 = 0$, is momentum
conservation restated.

(c) Explain why the modal-energy formula $\tfrac12(\dot q_p^2 + \omega_p^2 q_p^2)$ is still
correct for this mode and reduces to $\tfrac12 \dot q_0^2$.

(d) The zero eigenvalue comes back from a numerical solver as a small number of either sign,
and taking its square root turns a $10^{-16}$ absolute error into a $10^{-8}$ frequency. State
what a test for a zero mode must therefore assert, and why asserting `omega == 0` would be
wrong even though the physics says it is zero.

## Problem 4 — reading a dispersion plot

<!-- objectives: OBJ-07-4 -->

You are handed a plot of $\omega$ against $k$ for an unfamiliar chain. It is a sine arch, zero
at $k=0$, reaching a maximum of $6.0\times10^{13}$ rad/s at $k = 1.6\times10^{10}$ m$^{-1}$.

(a) Find the spacing $a$ and the combination $\sqrt{k_s/m}$.

(b) Find the long-wavelength wave speed $c$, and compare it with the speed of sound in a
typical solid, a few thousand metres per second. Comment.

(c) A wave with $k = 2\times 10^{9}$ m$^{-1}$: find $\omega$ from the exact relation and from
the linear approximation, and give the error of the approximation as a percentage.

(d) A colleague proposes doubling the number of atoms in the sample to raise the maximum
frequency. Explain in one sentence why this cannot work, and say what would have to change
instead.

## Problem 5 — the plucked chain as a Fourier series

<!-- objectives: OBJ-07-2 -->

A chain of $N = 20$ is pulled into a symmetric triangle — mass $j$ displaced by
$A\min(j, N+1-j)/\tfrac{N+1}{2}$ — and released from rest.

(a) Compute the modal coordinates $q_p(0)$ by projection. Show that every even-$p$ coordinate
vanishes, and say what symmetry of the initial shape is responsible.

(b) The triangle wave's Fourier coefficients fall as $1/p^2$ with alternating sign. Verify
numerically that $q_1/q_3 \approx -9$ and $q_1/q_5 \approx 25$, and identify the small
departures from exactly $-9$ and $25$ — measured $-9.07$ and $25.6$ — as the effect of
sampling a triangle at 20 points rather than continuously.

(c) Compute the fraction of the total energy in the fundamental. Relate your answer to the
puzzle at the top of the module page.

(d) Now pluck at the quarter point instead. Recompute the modal energies and explain, in terms
of the projection integral, why a guitarist plucking near the bridge gets a brighter sound.

## Problem 6 — the continuum limit, measured

<!-- objectives: OBJ-07-5 -->

Using `coupled.chain_mode_frequencies` and `coupled.chain_continuum_frequencies`:

(a) For $p = 1$, compute the relative error against the continuum value for
$N \in \{10, 20, 40, 80, 160\}$ and fit its order on log-log axes. Report the exponent.

(b) Repeat the fit using $N$ as the refinement parameter instead of $N+1$. You will get about
1.95. Explain which is right and why, without appealing to which one is closer to 2.

(c) Overlay the predicted error $(p\pi)^2/(24(N+1)^2)$ on your measurements. Report the largest
relative discrepancy across your grid.

(d) Repeat (a) for $p = 1, 2, 4, 8, 16$ at fixed $N = 100$ and fit the exponent in $p$. State
the largest $p$ for which you would be willing to call a 100-mass chain "a string to 1%", and
give the number that justifies the choice.

## Problem 7 — challenge: a defect that traps a mode

<!-- objectives: OBJ-07-1, OBJ-07-4 -->

Build a fixed chain of $N = 41$ and replace the central mass with $\alpha m$.

(a) For $\alpha = 0.3$, solve for the modes and show that the highest frequency lies above the
perfect chain's band top $2\sqrt{k_s/m}$. Report both numbers.

(b) Plot the shape of that mode on a logarithmic vertical axis and fit the decay of its
envelope away from the defect. Report the per-mass factor.

(c) Explain why a mode above the band cannot propagate, and why that is the same statement as
"it is localized". Your explanation should use $\omega(k)$ and say what $k$ would have to be.

(d) Sweep $\alpha$ from $1$ downwards and find where the localized mode separates from the
band. Then repeat with $\alpha > 1$: report whether a *heavy* defect produces a localized mode
above the band, below it, or not at all, and explain the asymmetry.

## Problem 8 — challenge: Fermi–Pasta–Ulam–Tsingou

<!-- objectives: OBJ-07-2, OBJ-07-6 -->

Add a weak cubic term to each spring, so the force between neighbours becomes
$k_s\,\delta\,(1 + \beta\,\delta)$ with $\delta$ the extension and $\beta$ small.

(a) Modify a velocity-Verlet integrator to handle this force. Confirm at $\beta = 0$ that it
reproduces `coupled.simulate_coupled`.

(b) Start a chain of $N = 32$ in its lowest mode and track the modal energies over a long run,
projecting with the *linear* mode shapes throughout. Say why using the linear shapes is
legitimate here and what would break if $\beta$ were large.

(c) Show that the energy leaks into higher modes and then returns, and estimate the recurrence
time. Report the largest fraction of the total that ever leaves mode 1.

(d) Equipartition predicts the energy should end up shared equally among all 32 modes. State
what your run shows instead, and say precisely which assumption of this module's model
specification the result violates.
