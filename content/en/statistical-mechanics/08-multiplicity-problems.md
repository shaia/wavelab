---
title: Problem set — entropy and multiplicity
short_title: 08 · Problems
---

# Problem set: entropy and multiplicity

Exam-style problems. Work them with a pen before touching a computer; the last two are meant
to be finished numerically. Solutions and marking rubrics live with the instructor material
and are deliberately not on this site.

Take $k_B = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$ throughout.

## Problem 1 — counting by hand

<!-- objectives: OBJ-08-2, OBJ-08-3 -->

Six distinguishable coins are flipped.

(a) List, or count systematically, $\Omega(6,n)$ for every $n$ from $0$ to $6$, and confirm
that they sum to $2^6$.

(b) State, in one sentence, the assumption that lets you convert this list of counts into a
list of probabilities.

(c) Which is more probable: exactly $3$ heads, or exactly $5$ heads? By what factor?

## Problem 2 — the even split and its width

<!-- objectives: OBJ-08-3 -->

A two-state system has $N$ objects.

(a) Explain, without computing anything, why $\Omega(N,n)$ must be symmetric under
$n \to N-n$.

(b) For $N = 400$, use the Gaussian approximation to estimate the range of $n$ that contains
roughly $68\%$ of the total probability (one standard deviation either side of the peak).

(c) Repeat for $N = 40{,}000$. Express both ranges as a *fraction* of $N$, and state what
happens to that fraction as $N$ grows.

(d) A friend claims that because $\sigma = \sqrt{N}/2$ grows with $N$, "the system becomes less
predictable as it gets bigger." Explain what is wrong with this reading of the formula.

## Problem 3 — entropy from multiplicity

<!-- objectives: OBJ-08-4, OBJ-08-6 -->

A macrostate has multiplicity $\Omega$.

(a) A macrostate has $\Omega = 1$. State its entropy, and describe a physical macrostate of a
two-state system for which this is true.

(b) Two independent, non-interacting subsystems have multiplicities $\Omega_1 = 10^{20}$ and
$\Omega_2 = 10^{30}$. Find the multiplicity and the entropy of the combined system.

(c) A textbook claims "entropy measures disorder." Using the isotope-crystal example from the
module page, construct a short argument for why this claim, stated without qualification, is
misleading. Your argument should not merely assert the conclusion — it should use the
multiplicity of the two macrostates being compared.

## Problem 4 — Stirling and extensivity

<!-- objectives: OBJ-08-5 -->

(a) Write down the two-term and three-term versions of Stirling's approximation to $\ln N!$,
and state which additional physical information the three-term version captures that the
two-term version does not.

(b) Using the asymptotic result
$\ln\Omega(N,N/2) = N\ln 2 - \tfrac12\ln(\pi N/2) + O(1/N)$, estimate the relative size of the
sub-leading term compared to the leading term at $N = 10^3$ and at $N = 10^{20}$.

(c) A student argues: "Since entropy is $S = k_B \ln \Omega$ and $\ln\Omega(N,N/2)$ is not
exactly proportional to $N$, entropy is never really extensive." Evaluate this claim precisely,
distinguishing what is exact from what is a large-$N$ limit.

## Problem 5 — subsystems and the second law

<!-- objectives: OBJ-08-4, OBJ-08-6 -->

Two independent two-state subsystems, $A$ and $B$, each have $N=200$ objects.

(a) Subsystem $A$ starts at its own peak, $n_A = 100$. Subsystem $B$ starts at $n_B = 180$.
Using $\ln\Omega(N,n) = \ln N! - \ln n! - \ln(N-n)!$ (you may use a calculator or Stirling's
approximation), find $\ln\Omega_A$ and $\ln\Omega_B$ in their initial macrostates.

(b) The subsystems are now allowed to relax. $B$ moves to its own peak, $n_B = 100$, while $A$,
weakly coupled to $B$, is nudged to $n_A = 96$. Find the new $\ln\Omega_A$ and $\ln\Omega_B$,
and hence $\Delta S_A$ and $\Delta S_B$ in units of $k_B$.

(c) Show explicitly that $\Delta S_A < 0$ while $\Delta S_A + \Delta S_B > 0$, and explain why
this is entirely consistent with everything derived in this module.

(d) State precisely what physical assumption would be violated if $A$ and $B$ were *not*
independent — i.e. if the objects in $A$ could also interact with the objects in $B$ directly.

## Problem 6 — computational

<!-- objectives: OBJ-08-1, OBJ-08-3, OBJ-08-6 -->

Using the module's laboratory notebook and `thermolab.multiplicity`:

(a) For $N \in \{10^2, 10^3, 10^4, 10^5\}$, compute `peak_relative_width(N)` and verify the
$N^{-1/2}$ scaling by fitting the exponent on log-log axes.

(b) Run `sample_two_box` starting from every object in one box, for $N=200$ and $N=800$.
Measure how many steps it takes each trajectory to first reach within $5\%$ of the even split,
and comment on how that compares with $N$ itself.

(c) Run at least $20$ independent realisations of `sample_two_box` for $N=400$, each for the
same number of steps, and measure the late-time occupancy fraction in each. Confirm that the
spread across realisations is consistent with the Gaussian width $\sigma/N = 1/(2\sqrt N)$
predicted in the derivation.

(d) State one claim from the module page that your simulation results support, and one claim
that they do not — and cannot — establish on their own.
