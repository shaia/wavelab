---
title: Work and thermodynamic paths
short_title: 05 · Work and paths
module: 05-work-paths
objectives:
  - id: OBJ-05-1
    text: Distinguish state functions from path functions, and identify which of U, Q, W is which.
  - id: OBJ-05-2
    text: Compute the work done on a gas along an arbitrary quasistatic path as W_on = -∫P dV.
  - id: OBJ-05-3
    text: Apply the first law dU = δQ + δW_on with a consistent sign convention.
  - id: OBJ-05-4
    text: Explain why δQ and δW are inexact differentials while dU is exact.
  - id: OBJ-05-5
    text: Contrast quasistatic and irreversible processes, and say when the area under a P-V curve is the work.
---

# Work and thermodynamic paths

(05-work-paths-puzzle)=
## The puzzle: same start, same finish, different bill

Take a gas in a cylinder. Its state is fixed by two numbers — say its pressure and its volume.
Move it from state $A$ to state $B$, and you might reasonably expect the cost of the journey
to be fixed too. A litre of gas at two atmospheres is a litre of gas at two atmospheres,
whatever route you took to get there.

That expectation is wrong, and the way in which it is wrong organises the whole of
thermodynamics.

Two engineers each take the same gas from $A$ to $B$. The first lets it expand slowly while
keeping it at constant pressure, then cools it at constant volume. The second lets it expand
while holding its temperature fixed. Both end with exactly the same gas in exactly the same
state — same pressure, same volume, same temperature, same energy. And yet they did different
amounts of work, and they moved different amounts of heat.

:::{important} The question
If the gas ends up in an identical state either way, how can the amounts of work and heat
differ? And if they differ, in what sense is heat "contained" in the gas at all?
:::

The answer will force us to be careful about a distinction we have been sliding over: some
quantities describe *where a system is*, and others describe *what happened to it*. Confusing
the two is the single most common error in this subject, and the mathematics has a precise
name for the difference — exact versus inexact differentials.

(05-work-paths-predict)=
## Predict before you calculate

Commit to answers before reading on.

1. A gas expands from $V_1$ to $2V_1$ at constant pressure. Then a second gas expands between
   the same two volumes at constant temperature, starting from the same pressure. Which does
   more work, and why?
2. In the two-leg route above (expand at constant pressure, then cool at constant volume) and
   the isothermal route, which transfers more heat?
3. Take a gas around a closed loop, back to exactly where it started. Is the net work zero?
   Is the net change in internal energy zero?
4. A gas is compressed suddenly by slamming a piston down. Is the work still the area under
   the curve in the $P$–$V$ plane?

:::{note} On question 4
This one separates people who have memorised $W = -\int P\,dV$ from people who know what it
means. Hold on to your answer — we will come back to it, and the difference matters for
every engine you will ever analyse.
:::

(05-work-paths-explore)=
## Explore the model

The laboratory for this module is a path editor: you place points in the $P$–$V$ plane, the
notebook joins them into a route, and it computes the work along that route while comparing
it with other routes between the same two endpoints.

:::{admonition} Model specification
:class: model-spec
- **System:** a fixed quantity of ideal gas, $N$ particles, in a cylinder closed by a piston.
- **Dynamics:** quasistatic — the gas is in equilibrium at every point of the path, so a single $(P, V)$ pair describes it and $P\,dV$ is meaningful.
- **Boundary:** a frictionless piston; heat may cross the boundary unless the process is stated to be adiabatic.
- **Ensemble:** not applicable — this is macroscopic thermodynamics, and no microstate counting is involved.
- **Ignored:** friction, turbulence, finite-rate effects, gas non-ideality, the piston's mass.
- **Valid when:** the process is slow compared with the gas's internal relaxation time (nanoseconds for ordinary gases, so "slow" is generous).
- **Failure modes:** fast or irreversible processes, where the gas has no single well-defined pressure and the area under a drawn curve is *not* the work done on it.
:::

Here is the comparison the module is about. Two routes leave the same point and arrive at the
same point. The bars track the work accumulating along each one:

:::{figure} ../media/paths-two-routes.mp4
:alt: Two routes traced between identical endpoints in the P-V plane, with bars showing the work accumulating differently along each.
:width: 100%

Two routes traced between identical endpoints in the pressure–volume plane, with bars tracking
the work accumulating along each. Identical endpoints, identical final state — and two
different bills. Nothing about the endpoints could have told you this; only the route does.
:::

And here is why engines can exist at all. A cycle brings the gas back to precisely where it
started, so every state function returns to its value. The enclosed area does not:

:::{figure} ../media/paths-cycle.mp4
:alt: A rectangular cycle traced repeatedly in the P-V plane with the enclosed area shaded.
:width: 70%

A rectangular cycle traced repeatedly in the pressure–volume plane, with the enclosed area
shading in. Around a closed loop $\oint dU = 0$, but $\oint \delta W \ne 0$. The shaded area is
the net work per cycle, and an engine is a device for collecting it.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 05 — work and thermodynamic paths](/lite/lab/index.html?path=en/labs/05-work-paths.ipynb).

To run it locally instead: `uv run jupyter lab notebooks/en/labs/05-work-paths.ipynb`.
:::

Before reading the derivation, do three things in the notebook:

- Draw any two different routes between the same endpoints and compare the work.
- Draw a closed loop and check whether the net work is zero.
- Compare an isotherm with an adiabat starting from the same point, and notice which is
  steeper.

(05-work-paths-derive)=
## Derive the result

**System and boundary.** The gas inside the cylinder. The piston is the moving boundary.

**Sign convention.** This course uses, everywhere and without exception,

$$
dU = \delta Q + \delta W_{\mathrm{on}},
$$

where $\delta Q$ is positive when heat flows *into* the gas and $\delta W_{\mathrm{on}}$ is
positive when work is done *on* the gas. Compressing a gas therefore does positive work on it;
letting it expand does negative work on it.

<!-- sign-convention-exception -->
:::{admonition} Why the sign convention needs saying out loud
:class: definition
Many textbooks write $dU = \delta Q - \delta W$, where $W$ means work done *by* the system.
Both conventions are correct; mixing them within one calculation is not, and it is the source
of an enormous number of sign errors. Whenever you read a formula elsewhere, find out which
convention it uses before you use it.
:::

### The work done in a small displacement

The gas pushes on the piston with force $PA$, where $A$ is the piston's area. To move the
piston inward by $dx$, an external agent must do work $PA\,dx$ on the gas. The volume change
is $dV = -A\,dx$, so

$$
\delta W_{\mathrm{on}} = -P\,dV .
$$

For a finite quasistatic path from $V_1$ to $V_2$,

$$
\boxed{\; W_{\mathrm{on}} = -\int_{V_1}^{V_2} P\,dV \;}
$$

Everything hinges on that innocent-looking $P$ inside the integral. It is the *gas's own*
pressure, and writing it there already assumes the gas has one — that it is in equilibrium
throughout. That assumption is exactly the quasistatic condition in the model specification,
and question 4 above was about what happens when it fails.

### Why the answer depends on the route

$P$ inside the integral is not a fixed function of $V$; it depends on what else you are doing
to the gas. Along an isotherm, $P = N k_B T / V$. Along an adiabat, $P V^{\gamma}$ is
constant. Along an isobar, $P$ is constant. Each gives a different curve between the same two
points, and therefore a different area beneath it.

For the ideal-gas routes in the puzzle, between $(V_1, P_1)$ and $(V_2, P_2)$ at the same
temperature:

$$
W_{\mathrm{on}}^{\text{isothermal}} = -N k_B T \ln\frac{V_2}{V_1},
\qquad
W_{\mathrm{on}}^{\text{isobaric then isochoric}} = -P_1 (V_2 - V_1).
$$

With $V_2 = 2V_1$ these are $-N k_B T \ln 2 \approx -0.69\, N k_B T$ and $-N k_B T$
respectively. The two-leg route costs about 45% more work, for an identical final state.

### The exactness of $dU$, and the inexactness of $\delta Q$ and $\delta W$

For an ideal gas, $U = \tfrac{f}{2} N k_B T = \tfrac{f}{2} PV$, a function of the state alone.
Its change between two states is therefore the same for every route:

$$
\Delta U = \tfrac{f}{2}\left(P_2 V_2 - P_1 V_1\right).
$$

:::{admonition} State function
:class: definition
A **state function** has a definite value in each equilibrium state, so its change around any
closed path is zero: $\oint dU = 0$. Its differential is **exact**. Internal energy,
temperature, pressure, volume and entropy are state functions.
:::

:::{admonition} Path function
:class: definition
A **path function** is defined only for a process, not for a state. Its "differential" is
**inexact**, written $\delta$ rather than $d$ as a permanent warning: there is no function
$Q(P,V)$ whose difference gives the heat transferred. Heat and work are path functions.
:::

This is why the phrase "the heat contained in this gas" is not merely imprecise but
meaningless. A gas contains internal energy. Heat is one of the two ways energy crosses its
boundary; work is the other. Asking how much heat is in a gas is like asking how much of the
water in a lake arrived by river rather than by rain.

Combining the two facts gives the resolution of the puzzle: since $\Delta U$ is fixed by the
endpoints and $W_{\mathrm{on}}$ is not, the first law forces $Q$ to differ too, by exactly the
compensating amount:

$$
Q = \Delta U - W_{\mathrm{on}} .
$$

The two path functions vary; their combination does not.

:::{admonition} What is a theorem here and what is an assumption
:class: approximation
$W_{\mathrm{on}} = -\int P\,dV$ is exact for a quasistatic process, and is a *definition of
work* applied to a system with a well-defined pressure. That $U$ depends only on $T$ is a
property of the *ideal* gas, not of gases in general; for a real gas $U$ depends on volume
too, because pulling molecules apart against their mutual attraction costs energy.
:::

(05-work-paths-verify)=
## Verify computationally

Four checks, each of which is also an automated test in the project's suite.

**1. The closed forms.** Numerical integration of $-\int P\,dV$ along an isotherm reproduces
$-N k_B T \ln(V_2/V_1)$, and along an adiabat reproduces
$(P_2V_2 - P_1V_1)/(\gamma - 1)$, to a relative error below $10^{-6}$.

**2. Convergence.** The trapezoid rule converges at second order. Refining the sampling of a
path from 17 to 257 points shrinks the error by the predicted factor, and the fitted
convergence order is $2.0$. A scheme that produced a plausible number without that scaling
would be wrong in a way no eyeball could catch.

**3. Path dependence, quantitatively.** Two routes between identical endpoints differ in
$W_{\mathrm{on}}$ by more than $25\%$, while their $\Delta U$ agree to machine precision. That
single pair of numbers is the entire lesson of this module in computational form.

:::{admonition} A trap worth naming
:class: numerical-observation
The energies involved for a thousand particles are around $10^{-18}\,\mathrm{J}$. Compared
with an absolute tolerance of $10^{-12}$, *every* such number looks equal to every other.
Testing path dependence with a naive floating-point comparison would "prove" that work is a
state function. The project's test suite compares fractional differences for exactly this
reason — a reminder that a green test is only as good as the question it asks.
:::

**4. The first law closes.** On every path, $Q + W_{\mathrm{on}} = \Delta U$ identically. This
is not a check of physics — it is a check that the code has not quietly redefined a sign.

(05-work-paths-transfer)=
## Transfer the idea

The state-versus-path distinction is not a quirk of gases.

- **Altitude and distance travelled.** Your change in altitude between two points on a
  mountain is a state function of the endpoints; the distance you walked is not. Nobody is
  tempted to ask how much "distance" is stored at the summit.
- **Bank balance, deposits and withdrawals.** The balance is a state function; the amounts
  deposited and withdrawn are path functions. A balance of £100 does not consist of "£300 of
  deposits and −£200 of withdrawals" — the split is a property of the history, not of the
  account.
- **Electrical work.** For a battery, $\delta W = \mathcal{E}\,dq$ plays exactly the role of
  $-P\,dV$; the pattern "intensive variable times change in extensive variable" recurs for
  every kind of work, including magnetic ($-\mathbf{B}\cdot d\mathbf{m}$) and surface
  ($\sigma\,dA$) work.
- **Engines.** A cycle returns the working substance to its starting state, so $\oint dU = 0$
  and the net work equals the net heat. Everything an engine does is contained in the fact
  that the *path* functions do not cancel around a loop even though the state functions do.
  That is module 7.

:::{admonition} Reversible does not simply mean "can run backwards"
:class: model-assumption
A quasistatic process can be reversed *and leave no trace*: run it backwards and both system
and surroundings return to their original states. Many processes can be run backwards in the
weaker sense of returning the system alone — a gas can be compressed back to its old volume
after a free expansion — while leaving the surroundings permanently changed. That distinction
is what the second law is about, and confusing the two makes module 7 impossible.
:::

(05-work-paths-quiz)=
## Check your understanding

```{include} ../_generated/quiz-05-work-paths.md
```

Exam-style problems are in [the problem set](05-work-paths-problems.md).

(05-work-paths-explain)=
## Explain it in your own words

1. Explain to someone who has not taken this course why "the heat contained in a gas" is not
   a meaningful quantity, using an analogy of your own rather than one of ours.
2. A student writes $\Delta Q = Q_2 - Q_1$ for a process. What has gone wrong, and what is the
   correct way to write what they meant?
3. Two processes take a gas between the same states; one transfers twice as much heat as the
   other. Explain how this is consistent with energy conservation.
4. Why does the notation use $\delta$ for heat and work but $d$ for internal energy? Answer in
   terms of what would go wrong if we used $d$ for all three.

(05-work-paths-advanced)=
## Advanced: what "inexact" means mathematically

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section, though it makes module 10
(thermodynamic potentials) considerably less mysterious.
:::

**Differential forms.** In the $(V, T)$ plane the heat transfer of an ideal gas is

$$
\delta Q = \frac{f}{2} N k_B \, dT + \frac{N k_B T}{V}\, dV .
$$

For a differential $M\,dx + N\,dy$ to be exact — that is, to be $dF$ for some function
$F(x,y)$ — it must satisfy $\partial M/\partial y = \partial N/\partial x$. Here
$\partial(\tfrac{f}{2}Nk_B)/\partial V = 0$ while $\partial(Nk_BT/V)/\partial T = Nk_B/V \ne 0$.
The test fails, and it fails by exactly the amount that makes heat path-dependent. There is no
function $Q(V,T)$, and no amount of clever algebra will produce one.

**Integrating factors.** Remarkably, dividing by $T$ fixes it:

$$
\frac{\delta Q}{T} = \frac{f}{2}\frac{N k_B}{T}\, dT + \frac{N k_B}{V}\, dV ,
$$

and now the cross-derivatives both vanish. The inexact $\delta Q$ has become an exact
differential, and the state function whose differential it is has a name: the entropy,
$dS = \delta Q_{\text{rev}}/T$. That $1/T$ is an integrating factor for heat is one way to
state the second law, and it is where module 8 begins.

**Irreversible work, properly.** When a piston is slammed down, the gas near it is compressed
before the far side knows anything has happened; there is no single $P$ and the $P$–$V$ plane
has no curve to draw. What is still true is that the work done on the gas is
$-\int P_{\text{ext}}\,dV$, using the *external* pressure applied at the boundary. For a
quasistatic process $P_{\text{ext}} = P$ and the two agree. Otherwise
$P_{\text{ext}} > P$ during compression and $P_{\text{ext}} < P$ during expansion, so an
irreversible round trip always leaves the gas with more energy than it started with — which is
dissipation, seen from the mechanical side. If you answered "yes" to question 4 in the
predictions, this paragraph is the correction.
