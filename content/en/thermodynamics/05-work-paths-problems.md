---
title: Problem set — work and thermodynamic paths
short_title: 05 · Problems
---

# Problem set: work and thermodynamic paths

Use the convention $dU = \delta Q + \delta W_{\mathrm{on}}$ throughout, and say so in your
working. Take the gas to be ideal and monatomic ($f = 3$, $\gamma = 5/3$) unless told
otherwise.

## Problem 1 — three routes, one destination

<!-- objectives: OBJ-05-1, OBJ-05-2 -->

One mole of gas begins at $P_1 = 2.00 \times 10^{5}\ \mathrm{Pa}$, $V_1 = 10.0\ \mathrm{L}$
and ends at $V_2 = 20.0\ \mathrm{L}$, $P_2 = 1.00 \times 10^{5}\ \mathrm{Pa}$.

(a) Show that the two states lie on the same isotherm, and find that temperature.

(b) Compute $W_{\mathrm{on}}$ for each of three routes: (i) the isotherm; (ii) expansion at
constant $P_1$ followed by cooling at constant $V_2$; (iii) cooling at constant $V_1$ followed
by expansion at constant $P_2$.

(c) Compute $\Delta U$ and $Q$ for each route. Comment on which quantities came out equal and
which did not, and say why that was inevitable before doing any arithmetic.

## Problem 2 — a cycle

<!-- objectives: OBJ-05-1, OBJ-05-3 -->

A gas is taken clockwise around the rectangle in the $P$–$V$ plane with corners
$(V_1, P_1)$, $(V_2, P_1)$, $(V_2, P_2)$, $(V_1, P_2)$, where $V_2 > V_1$ and $P_1 > P_2$.

(a) Compute the work done on the gas for each of the four legs, and the net work per cycle.

(b) State the net change in internal energy per cycle, and justify it in one sentence without
computing anything.

(c) Deduce the net heat absorbed per cycle. Which direction around the loop makes the device
an engine rather than a refrigerator?

(d) Show that the magnitude of the net work equals the area enclosed by the rectangle, and
explain why the enclosed area — rather than the area under a single curve — is the relevant
quantity for a cycle.

## Problem 3 — isotherm against adiabat

<!-- objectives: OBJ-05-2, OBJ-05-4 -->

A gas at $(P_0, V_0)$ expands to $2V_0$, once isothermally and once adiabatically.

(a) Sketch both paths on the same axes and state which is steeper, with a physical reason
rather than an appeal to the exponent.

(b) Compute $W_{\mathrm{on}}$ for each.

(c) Compute $Q$ for each, and use the results to explain why the adiabatic expansion ends at a
lower temperature.

(d) Which final state has the greater internal energy? Which has the greater entropy? (You may
answer the second part qualitatively; module 8 makes it quantitative.)

## Problem 4 — the sudden piston

<!-- objectives: OBJ-05-5 -->

A gas at pressure $P_1$ in volume $V_1$ is compressed to $V_2$ by pushing the piston with a
constant external pressure $P_{\text{ext}} = 3P_1$, quickly enough that the gas is never in
equilibrium during the process.

(a) Compute the work done on the gas.

(b) Explain why the answer is *not* $-\int P\,dV$ evaluated along any curve in the $P$–$V$
plane, and what would have to be true for it to be.

(c) Compare your answer with the work required to reach the same final volume quasistatically
along an adiabat. Which is larger, and where did the extra energy go?

(d) A classmate objects that the gas ends at the same volume either way, so the work must be
the same. Diagnose their error precisely.

## Problem 5 — exactness by calculation

<!-- objectives: OBJ-05-4 -->

For one mole of ideal gas, write $\delta Q$ in terms of $dT$ and $dV$.

(a) Apply the cross-derivative test and show explicitly that $\delta Q$ is inexact.

(b) Repeat the test for $\delta Q / T$ and show that it is exact.

(c) Integrate $\delta Q/T$ along two different routes between the same endpoints and confirm
that you get the same answer. Name the state function you have just constructed.

(d) Explain in words what it means that a quantity becomes a state function only after
division by $T$.

## Problem 6 — computational

<!-- objectives: OBJ-05-2, OBJ-05-5 -->

Using the module's laboratory notebook and `thermolab.paths`:

(a) Construct at least four different paths between the same endpoints, including one you
invent yourself, and tabulate $W_{\mathrm{on}}$, $\Delta U$ and $Q$ for each.

(b) Verify numerically that $\Delta U$ agrees across all of them to machine precision while
$W_{\mathrm{on}}$ does not, and quote the fractional spread of the work values.

(c) Compute the isothermal work at increasing sampling resolution and confirm that the error
falls as the square of the step size. Report the fitted convergence order.

(d) Explain why the fractional spread in (b) is the meaningful comparison, and what would have
gone wrong had you compared the work values with an absolute tolerance instead.
