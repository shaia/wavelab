---
title: Problem set — the microscopic origin of pressure
short_title: 04 · Problems
---

# Problem set: the microscopic origin of pressure

Exam-style problems. Work them with a pen before touching a computer; the last two are
meant to be finished numerically. Solutions and marking rubrics live with the instructor
material and are deliberately not on this site.

Take $k_B = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$ throughout.

## Problem 1 — momentum bookkeeping

<!-- objectives: OBJ-04-2 -->

A particle of mass $m$ travelling with velocity components $(v_x, v_y)$ strikes a rigid wall
perpendicular to the $x$ axis and rebounds elastically.

(a) State the momentum transferred to the wall, and explain in one sentence why $v_y$ does
not appear.

(b) The particle is in a box of side $L_x$ in the $x$ direction. Show that its time-averaged
contribution to the force on that wall is $m v_x^2 / L_x$, stating clearly where you use the
assumption that it collides with nothing else on the way.

(c) A student writes the force as $2m|v_x| \times (\text{collision rate})$ and obtains twice
your answer. Find their error.

## Problem 2 — reading the equation of state

<!-- objectives: OBJ-04-2, OBJ-04-3 -->

A sealed rigid vessel of volume $2.0\ \mathrm{L}$ holds $N = 5.0 \times 10^{22}$ argon atoms
at $300\ \mathrm{K}$.

(a) Compute the pressure.

(b) The gas is heated to $600\ \mathrm{K}$. Compute the new pressure, the new mean kinetic
energy per atom, and the new total internal energy. State which of these three quantities
doubled and which did not, and why.

(c) The argon is replaced by the same number of helium atoms at the same temperature. Which
of the quantities in (b) change? Justify each answer in one sentence.

## Problem 3 — the mass paradox

<!-- objectives: OBJ-04-2, OBJ-04-3 -->

Two identical containers hold the same number of particles at the same temperature. The
particles in container B are four times as massive as those in A.

(a) Compare the mean speeds, the mean kinetic energies, the momentum delivered per collision,
and the collision rates in the two containers.

(b) Show that the pressures are equal, and identify precisely which two effects cancel.

(c) Now instead compare the containers at equal *particle speeds* rather than equal
temperature. Are the pressures still equal? Explain what this tells you about which quantity
pressure "really" tracks.

## Problem 4 — how steady is steady

<!-- objectives: OBJ-04-1, OBJ-04-4 -->

The relative fluctuation of the pressure of an ideal gas is $\sigma_P/\langle P\rangle
\simeq N^{-1/2}$.

(a) A pressure gauge resolves one part in $10^{4}$. Above what particle number $N$ does the
gauge read a perfectly steady pressure?

(b) A cubic micron of air at room temperature and atmospheric pressure contains about
$2.5 \times 10^{7}$ molecules. Estimate the relative pressure fluctuation. Would it be
detectable?

(c) The smallest volume in which pressure is still a useful concept is roughly where the
fluctuation reaches $1\%$. Estimate that volume for air at room temperature, and compare it
with the size of a bacterium.

(d) Explain why the answer to (c) is a statement about $N$ rather than about length.

## Problem 5 — where the model breaks

<!-- objectives: OBJ-04-5 -->

The derivation on the module page assumes point particles that never interact.

(a) Real argon atoms have a diameter of about $0.34\ \mathrm{nm}$. Estimate the fraction of
the volume they occupy at room temperature and atmospheric pressure, and comment on whether
neglecting it is reasonable.

(b) Give a physical argument for whether the *attraction* between atoms should raise or lower
the pressure below the ideal-gas value at fixed $N$, $V$, $T$.

(c) Two students disagree. One says the ideal gas law fails at low temperature because the
atoms move too slowly to hit the walls often. The other says it fails because attraction and
quantum statistics become important. Adjudicate.

## Problem 6 — computational

<!-- objectives: OBJ-04-1, OBJ-04-4, OBJ-04-5 -->

Using the module's laboratory notebook and the `thermolab.kinetics` module:

(a) Measure the pressure for $N \in \{50, 100, 200, 400, 800\}$ at fixed $T$ and $V$, and
verify that $P$ is proportional to $N$. Report your fitted slope with an uncertainty.

(b) For each $N$, draw at least 30 independent microstates (use
`initialise_gas(..., fix_temperature=False)`) and measure the relative spread of the pressure.
Plot it against $N$ on log-log axes and fit the exponent.

(c) Your fit should give $-0.5$. Explain why using `fix_temperature=True` instead would give
a much smaller spread, and say which of the two settings corresponds to a real gas in contact
with a thermal reservoir.

(d) State one thing your numerical result does *not* prove.
