---
title: Problem set — orientation
short_title: 00 · Problems
---

# Problem set: orientation

Exam-style problems. Work them with a pen before touching a computer; the last one is meant to
be finished numerically. Solutions and marking rubrics live with the instructor material and
are deliberately not on this site.

Take $\kB = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$ throughout.

## Problem 1 — the honest die

<!-- objectives: OBJ-00-2 -->

(a) From the definitions, compute the mean $\mu_1$ and variance $\sigma_1^2$ of one fair
six-sided die. Show the sums; do not quote the closed form.

(b) A die is loaded so that a six comes up with probability $1/3$ and each of the other five
faces with probability $2/15$. Compute its mean and variance, and say in one sentence why the
variance moved in the direction it did.

(c) Two fair dice are rolled independently. By enumerating all $36$ equally likely outcomes,
compute $\langle X + Y \rangle$ and $\operatorname{Var}(X+Y)$ directly, and check both against
the addition rules derived on the module page.

(d) Now let $Y = X$ — the "second die" is a copy of the first, read twice. Compute
$\operatorname{Var}(X + Y)$ for this case and compare with (c). Which hypothesis of the
addition rule has been violated, and by how much does the answer change?

## Problem 2 — scatter bookkeeping

<!-- objectives: OBJ-00-1, OBJ-00-3 -->

(a) You average $100$ fair dice. Give the mean and the standard deviation of the result.

(b) How many dice must you average for the standard deviation of the answer to fall to
$0.001$? Comment on whether this is a practical experiment.

(c) For the same $N$ as in (b), give the standard deviation of the *sum* of those dice, and
state how it changed relative to $N = 100$. Explain in one sentence how the sum can become
less predictable while the average becomes more predictable.

(d) A laboratory measurement is repeated $M$ times and the results averaged. The precision is
said to improve as $\sqrt{M}$. State precisely what must be true of the individual
measurements for this to hold, and give one realistic way an experiment can violate it — in
which case averaging more data buys you much less than $\sqrt{M}$.

## Problem 3 — dimensional detective

<!-- objectives: OBJ-00-4 -->

(a) Three candidate expressions are offered for a molecular speed:
$\sqrt{3\kB T/m}$, $\quad 3\kB T/m$, $\quad \sqrt{3\kB T m}$.
Reject the ones that cannot be a speed, showing the dimensions of each.

(b) From $PV = N\kB T$, with $N$ a pure number, deduce the SI units of $\kB$.

(c) Show that the pascal and the joule per cubic metre are the same unit. Given that, may we
conclude that the pressure of a gas *equals* its energy density? Explain what dimensional
analysis does and does not license here.

(d) A calculation returns an internal energy of $6.214 \times 10^{-21}\ \mathrm{J}$ where
theory predicts $6.207 \times 10^{-21}\ \mathrm{J}$. A student checks agreement by testing
whether the two differ by less than $10^{-12}\ \mathrm{J}$ and reports a perfect match. State
what is wrong with the test, propose a better one, and apply it.

## Problem 4 — partial derivatives at work

<!-- objectives: OBJ-00-5 -->

An ideal gas has $P(V,T) = N \kB T / V$ with $N$ fixed.

(a) Compute $(\partial P/\partial T)_V$ and $(\partial P/\partial V)_T$, and write the total
differential $\mathrm{d}P$.

(b) Take $N = 1.00\times10^{22}$, $V = 1.00\times10^{-3}\ \mathrm{m^3}$ and
$T = 300\ \mathrm{K}$. Use the total differential to estimate the change in pressure when the
temperature rises by $3\ \mathrm{K}$ while the volume falls by $1.0\times10^{-5}\ \mathrm{m^3}$.
Then compute the change exactly and give the fractional error of the estimate.

(c) Repeat (b) with the volume *rising* by $1.0\times10^{-5}\ \mathrm{m^3}$ instead. Explain
the result without calculation, using only the form of $P(V,T)$.

(d) For $f(x,y) = x^2 y$, evaluate $(\partial f/\partial x)_y$ at $(1,1)$ and
$\mathrm{d}f/\mathrm{d}x$ at $x=1$ along the line $y=x$. The two differ. Say exactly which
question each of them answers, and identify the term in the total differential that accounts
for the difference.

## Problem 5 — exact or not

<!-- objectives: OBJ-00-6 -->

Consider the two differential forms

$$
\omega_1 = y\,\mathrm{d}x + x\,\mathrm{d}y ,
\qquad
\omega_2 = y\,\mathrm{d}x .
$$

(a) Apply the mixed-partials criterion to each and state which is exact.

(b) For the exact one, find its potential $f$ explicitly.

(c) Integrate *both* forms from $(0,0)$ to $(1,1)$ along (i) the straight line $y=x$ and
(ii) the two-leg route across to $(1,0)$ and then up. Present the four numbers in a table and
comment on the pattern.

(d) Compute $\oint \omega_2$ counter-clockwise around the unit square with corners $(0,0)$,
$(1,0)$, $(1,1)$, $(0,1)$. Explain why the answer had to be non-zero.

(e) In module 5 the plane becomes the $P$–$V$ plane and one of the forms you integrate is
inexact. In one sentence, say what physical consequence follows from that inexactness — no
calculation.

## Problem 6 — computational

<!-- objectives: OBJ-00-1, OBJ-00-3 -->

Using the module's laboratory notebook and the `thermolab.sampling` module:

(a) For $N \in \{4, 16, 64, 256, 1024\}$, measure the relative spread of the average of $N$
dice over at least $500$ repetitions. Plot it against $N$ on log-log axes and fit the exponent
with `validation.scaling_exponent`. Report the fitted value.

(b) Check the coefficient as well as the exponent: multiply each measured spread by $\sqrt{N}$
and compare with $\sigma_1/\mu_1$. Explain why a test of the exponent alone would be weak
evidence.

(c) Design and run the falsifying experiment for the claim "the average settles because later
rolls compensate earlier ones": generate many runs, keep only those whose first ten rolls
averaged above $4.5$, and measure the mean of the *subsequent* rolls in those runs. Report the
result with an uncertainty and state what it rules out.

(d) Repeat (a) with a loaded die of your choice. State which of the two numbers — the exponent
or the coefficient — changed, and why the derivation on the module page predicts exactly that.

(e) State one thing your numerical results do *not* prove.
