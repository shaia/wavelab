---
title: Orientation — how many makes a law
short_title: 00 · Orientation
module: 00-orientation
objectives:
  - id: OBJ-00-1
    text: Explain how predictable aggregate behaviour emerges from unpredictable individual events, using the average of many independent random quantities.
  - id: OBJ-00-2
    text: Compute the mean and variance of a discrete random variable, and of the sum and average of N independent copies of it.
  - id: OBJ-00-3
    text: Derive and apply the N^(-1/2) law — the relative scatter of an average falls as N^(-1/2) while the absolute scatter of a sum grows as N^(1/2).
  - id: OBJ-00-4
    text: Check a formula by dimensional analysis in SI units, and state the unit conventions this course uses.
  - id: OBJ-00-5
    text: Compute partial derivatives in held-variable notation, form a total differential, and evaluate the line integral of a differential form along a path.
  - id: OBJ-00-6
    text: Decide whether a differential form is exact using the mixed-partials criterion, and exhibit an inexact form whose integral depends on the path.
  - id: OBJ-00-7
    text: State the conventions this course runs on — the sign of work in the first law, the meaning of the inexact differential, and what the epistemic labels and model specifications promise.
---

# Orientation: how many makes a law

This module has two jobs. The first is to state the question the whole course is an answer to,
in the smallest setting where it can be asked honestly — no particles, no energy, no
container. The second is to find out which tools you will need to sharpen, before a physical
problem is riding on them.

(00-orientation-puzzle)=
## The puzzle: one die is lawless, a thousand dice are a law

Roll one fair die. No theory in physics will tell you what comes up. Newtonian mechanics
governs the tumble completely, and is useless to you: the outcome depends on the throw so
sensitively that predicting it would require knowing the initial conditions to a precision
nobody can achieve. The single roll is, for practical purposes, lawless.

Now roll a thousand dice and average them. You will get $3.50$, give or take about $0.05$.
Do it again — $3.50$ again, within about the same margin. Do it in another room, with another
set of dice, next year. Still $3.50$. Roll a million and average: now the answer is $3.500$
to within about $0.002$, and you could calibrate an instrument against it.

Nothing about any individual die changed. Each one is exactly as unpredictable as before.
Yet a quantity built entirely out of unpredictable things has become reproducible enough to
be treated as a *property of the collection* rather than as an accident of the throw.

:::{important} The question
This is the question the entire course exists to answer:

> **How does predictable macroscopic behaviour emerge from uncertain microscopic behaviour?**

Dice are its smallest honest instance. A gas is the same question with $10^{23}$ molecules
instead of a thousand dice, and with momentum instead of a face value.
:::

Every topic in this course gets looked at from four directions at once, and it is worth
seeing all four on something as simple as dice before they arrive attached to thermodynamics:

| View | For dice | Later, for a gas |
|---|---|---|
| **Macroscopic** | the average, $3.50$ | pressure, temperature, entropy |
| **Microscopic** | the individual rolls | the positions and velocities of molecules |
| **Mathematical** | means, variances, independence | the same algebra, plus differentials and asymptotics |
| **Computational** | roll many, measure the scatter | simulate the gas, measure the fluctuation |

This module is also a diagnostic. Thermal physics leans hard on four skills — units,
conventions, derivatives, and probability — and it leans on them from the first week. By the
end of this page you should know precisely which of the four to spend a weekend on.

(00-orientation-predict)=
## Predict before you calculate

Commit to an answer for each of these *before* reading on or running anything. Write them
down. The point is not to be right; it is to find out which of your intuitions is about to be
overturned, and which of your tools is rusty.

1. You average $100$ fair dice. What number do you expect, and how far from it would you bet
   a single such experiment lands?
2. You now average $400$ dice instead of $100$. Does the typical distance from $3.5$ halve,
   quarter, or stay about the same?
3. You look at the *sum* of the $400$ dice rather than their average. Does its scatter also
   shrink?
4. Pressure is measured in pascals; energy density in joules per cubic metre. Do these have
   the same dimensions? If they do, is that a coincidence?
5. Let $f(x,y) = x^2 y$. Is $(\partial f/\partial x)_y$ at the point $(1,1)$ the same number
   as $\mathrm{d}f/\mathrm{d}x$ at $x=1$ along the line $y = x$?

:::{note} Why we ask first
Question 3 catches most people, and it is the single most useful thing on this page: the sum
and the average behave in *opposite* directions, and both follow from one line of algebra.

Questions 4 and 5 are the diagnostic half. If either made you hesitate, that is not a problem
— it is information, and [the mathematics refresher](math-refresher.md) exists for exactly
this. A prediction you committed to is the only way to notice you were wrong; reading the
right answer afterwards always feels like you knew it.
:::

(00-orientation-explore)=
## Explore the model

Here is the phenomenon in one picture. On the left, four hundred rolls of one die, in order.
On the right, the running average of that very same sequence, settling onto the dashed line
at $3.5$ without anything on the left ever becoming orderly.

:::{figure} ../media/running-average.mp4
:alt: Left, individual die rolls scattered between one and six with no pattern. Right, the running average of the same rolls converging on 3.5.
:width: 100%

**Left:** individual die rolls, scattered between one and six with no pattern that ever
emerges. **Right:** the running average of those same rolls, converging on the dashed line at
$3.5$. The left panel is the raw randomness; the right panel is the same data, accumulated.
Nothing was smoothed, filtered or corrected — the only operation applied was division by the
number of rolls so far.
:::

Now watch what changes when each experiment gets bigger. Below, the experiment "average $N$
dice" is repeated $160$ times at three values of $N$, with one dot per completed experiment:

:::{figure} ../media/spread-shrinks.mp4
:alt: Three panels at N = 10, 100 and 1000; each shows dots for repeated experiments, and the vertical scatter of the dots narrows sharply as N grows.
:width: 100%

Three panels at $N = 10$, $100$ and $1000$, sharing a vertical scale, with one dot per
completed experiment. The vertical spread of a column of dots *is* the reproducibility of a
single experiment, and it narrows sharply as $N$ grows. The rest of this page is about how
fast.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** $N$ dice, each showing one of six equally likely faces; the observable is their sum or their average.
- **Dynamics:** none — each draw is independent of every other, with no memory between them and nothing evolving in time.
- **Boundary:** closed trivially; $N$ is fixed for one experiment and nothing is exchanged with anything.
- **Ensemble:** every face equally probable, by assumption rather than by proof.
- **Ignored:** all physics of real dice — the tumble, the bounce, pip asymmetry, air drag, and the deterministic chaos that is the actual reason a throw looks random.
- **Valid when:** the randomness is well described by independent uniform draws; a seeded pseudo-random generator is, by construction.
- **Failure modes:** correlated draws, loaded dice, and any question about a *single* roll beyond its distribution.
:::

Every simulation in this course carries a block like that one, and it is worth knowing why
before you meet a harder example. Two of its seven fields are doing unusual work here.
*Dynamics: none* is unusual — most models in this course evolve something — and it is the
reason dice are the right starting point: whatever makes the average settle down, it cannot be
a dynamical mechanism, because there is no dynamics. And *Ensemble* looks like an odd word for
dice, but the entry is the honest one: "every face equally probable" is a postulate we are
choosing, not a fact we established. Module 8 makes exactly this kind of postulate about the
microstates of a gas, and the whole of statistical mechanics rests on it.

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 00 — how many makes a law](/lite/lab/index.html?path=en/labs/00-orientation.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/00-orientation.ipynb`.
:::

Run the laboratory now, then come back. Three things are worth doing before you read on:

- Watch the running average for $N = 10$, then for $N = 10{,}000$. Note that the curve is
  just as jagged at the start in both cases.
- Re-run the same experiment with a different seed, several times, and watch how much the
  final answer moves.
- Load the die — make a six twice as likely as any other face — and see which parts of the
  picture change and which do not.

:::{admonition} What the picture shows and does not show
:class: numerical-observation
That the running average settles is, so far, an *observation*: we ran a simulation and looked.
It is not yet established, and the picture cannot tell us how fast the settling should be, or
whether it would still happen for a loaded die, or for a quantity other than a die roll.

The next section settles those questions by derivation. Keep the two kinds of statement apart
— this course labels every boxed claim with which kind it is, and the habit is worth more than
any single result in it.
:::

(00-orientation-derive)=
## Derive the result

We now do the calculation the simulation is imitating. It needs no calculus and no central
limit theorem — only the definitions of mean and variance, plus one property of independent
quantities.

**System.** $N$ dice. **Independent variables.** $N$, and the distribution of one die.
**Assumption.** The draws are independent — the outcome of one tells you nothing about any
other.

### Definitions, and one die

:::{admonition} Random variable, mean, variance, independence
:class: definition
A **random variable** $X$ takes value $x_k$ with probability $p_k$, where $\sum_k p_k = 1$.
Its **mean** (or expectation) and **variance** are

$$
\mu = \langle X \rangle = \sum_k p_k x_k ,
\qquad
\sigma^2 = \big\langle (X - \mu)^2 \big\rangle = \langle X^2 \rangle - \mu^2 .
$$

The **standard deviation** $\sigma$ is the square root of the variance, and carries the same
units as $X$ itself. Two random variables are **independent** when
$\langle XY \rangle = \langle X \rangle \langle Y \rangle$ — knowing one tells you nothing
about the other.
:::

For one fair six-sided die, $p_k = 1/6$ for $k = 1,\dots,6$, so

$$
\mu_1 = \frac{1+2+3+4+5+6}{6} = \frac{7}{2} = 3.5 ,
\qquad
\langle X^2 \rangle = \frac{1+4+9+16+25+36}{6} = \frac{91}{6} ,
$$

$$
\sigma_1^2 = \frac{91}{6} - \left(\frac{7}{2}\right)^2 = \frac{35}{12} \approx 2.917 ,
\qquad
\sigma_1 \approx 1.708 .
$$

No approximation anywhere: those are the exact properties of one die.

### The one property that does all the work

:::{admonition} Means always add; variances add for independent quantities
:class: theorem
For any two random variables, $\langle X + Y \rangle = \langle X \rangle + \langle Y \rangle$.
For the variance, expanding the definition gives

$$
\operatorname{Var}(X+Y)
= \operatorname{Var}(X) + \operatorname{Var}(Y)
+ 2\big( \langle XY \rangle - \langle X \rangle \langle Y \rangle \big) .
$$

The last bracket is the covariance. It vanishes exactly when $X$ and $Y$ are independent, and
then — and only then —

$$
\operatorname{Var}(X+Y) = \operatorname{Var}(X) + \operatorname{Var}(Y) .
$$

Repeating the argument $N-1$ times extends it to any number of mutually independent terms.
:::

Notice what the proof did **not** use: nothing about dice, nothing about six faces, nothing
about the shape of the distribution. It needs only that each quantity has a finite variance and
that they are mutually independent. That generality is why this one calculation will still be
doing the work when the random quantities are molecular velocities (module 4) or occupation
numbers (module 8) — and the independence hypothesis is exactly what fails in the systems where
thermal physics gets hard.

### The consequence

Let $S_N = X_1 + \dots + X_N$ be the sum of $N$ independent dice, and
$\bar{A}_N = S_N / N$ their average. Means add, so both have the expected value you would
guess. Variances add, so $\operatorname{Var}(S_N) = N \sigma_1^2$; and since scaling a
quantity by $1/N$ scales its variance by $1/N^2$,

$$
\boxed{\;
\sigma_{S_N} = \sigma_1 \sqrt{N} ,
\qquad
\sigma_{\bar{A}_N} = \frac{\sigma_1}{\sqrt{N}} \; }
$$

Read those two together, because they are the answer to prediction 3 and they point in
opposite directions. The sum gets *noisier* in absolute terms as $N$ grows; the average gets
*steadier*. Both statements come from the same $N\sigma_1^2$, and confusing them is the usual
error.

### Why the honest statement is a ratio

The scatter $\sigma$ carries the units of whatever was measured. That makes it useless as a
measure of "steadiness" on its own: a scatter of $0.05$ is enormous for a quantity of size
$0.01$ and invisible for a quantity of size $10^6$. The quantity that means something is the
dimensionless ratio

$$
\frac{\sigma_{\bar{A}_N}}{\mu_1} = \frac{\sigma_1}{\mu_1} \, N^{-1/2}
\qquad\text{with}\qquad
\frac{\sigma_1}{\mu_1} = \frac{\sqrt{35/12}}{7/2} \approx 0.488 \ \text{for a die.}
$$

That is the $N^{-1/2}$ law, with its coefficient. For $N = 100$ it gives about $4.9\%$; for
$N = 10^4$, about $0.49\%$; for $N = 10^{23}$, about $10^{-12}$ — which is why a gas has a
pressure and a single die does not have an average.

This habit — comparing fractions rather than absolute differences — is not a stylistic
preference. Energies in this course are routinely $10^{-18}\,\mathrm{J}$, and any test that
asks whether two of them agree "to within $10^{-12}$" will answer yes no matter what the
physics did.

Two things have deliberately *not* been shown. We have not shown what shape the distribution
of $\bar{A}_N$ takes — that it becomes a bell curve is the central limit theorem, and it is
module 3's result, not ours. And we have not shown that the average is *guaranteed* to be
close, only that its typical distance shrinks; turning that into a genuine probability bound
is the [advanced section](#00-orientation-advanced) below.

(00-orientation-verify)=
## Verify computationally

Deriving a formula and trusting it are different things. The laboratory measures the law
rather than assuming it, and every check below is also a test in the project's test suite, so
the claims on this page cannot silently rot.

**1. The exponent.** Measure the relative spread of $\bar{A}_N$ at
$N \in \{4, 16, 64, 256, 1024\}$, fit a straight line to $\log \sigma$ against $\log N$, and
read off the slope. It comes out at $-0.5$.

**2. The coefficient.** A fitted exponent alone is weak evidence — many wrong models produce
a slope near $-\tfrac{1}{2}$. So we also check the prefactor: measured spread times $\sqrt{N}$
must return $\sigma_1/\mu_1 \approx 0.488$, and it does, to a few percent.

**3. Sum versus average.** The same data, read two ways: the absolute scatter of the sum is
fitted at $+0.5$ while the relative scatter of the average is fitted at $-0.5$.

**4. The mechanism.** This is the one worth running yourself.

:::{admonition} Dilution, not compensation
:class: numerical-observation
It is tempting to explain the settling by saying that early deviations get cancelled by later
ones. The laboratory falsifies this directly: keep only the runs whose first ten rolls
averaged well above $3.5$, then look at what those same runs did *afterwards*. The subsequent
rolls average $3.5$, exactly like everyone else's. The dice have no memory and nothing
compensates.

What actually happens is that the early excess is a fixed quantity being divided by an
ever-larger $N$. It is never corrected; it is diluted.
:::

The three habits that make those numbers trustworthy are worth naming, because every later
module uses them:

- **Every random function takes its generator as an argument.** Nothing in `thermolab` reaches
  for global random state, so any result you see can be reproduced exactly.
- **Stochastic results are compared with an error bar, never bare.** A measurement that
  "agrees with theory" without an uncertainty attached has not been compared with anything.
- **Agreement is judged as a fraction.** See the previous section for what goes wrong
  otherwise.

:::{admonition} What the simulation cannot establish
:class: open-question
The generator produces draws that are independent *by construction* — that is what the
algorithm does. So these runs test our algebra, not our assumption. Whether any real
randomness source is genuinely independent is an empirical question about that source, and no
amount of simulation can settle it. Physical dice are slightly loaded; molecules in a dense
gas are genuinely correlated. Independence is where this whole chain of reasoning is bolted to
the world, and it is the joint to check first when a prediction fails.
:::

(00-orientation-transfer)=
## Transfer the idea

The algebra above is three lines long and it is load-bearing for the rest of the course.

- **Module 3 — probability and emergence.** The same sum of independent variables, asking the
  question we deferred: not how *wide* the distribution of an average is, but what *shape* it
  takes. The answer is the central limit theorem.
- **Module 4 — kinetic theory.** The random variables become molecular velocities and the
  average becomes the pressure on a wall. The relative fluctuation comes out as $N^{-1/2}$,
  from this same argument, and you can watch it on a simulated pressure gauge:
  [the microscopic origin of pressure](../thermodynamics/04-pressure.md).
- **Module 8 — entropy.** The objects being counted become microstates. The peak of the
  multiplicity narrows as $N^{-1/2}$, which is why an isolated gas never gathers in one
  corner: [entropy and multiplicity](../statistical-mechanics/08-multiplicity.md).

### The road ahead

| # | Module | The question it answers |
|---|---|---|
| 0 | Orientation | How can many unpredictable things add up to a reliable one? |
| 1 | Thermal equilibrium | What does it mean for two bodies to be "at the same temperature"? |
| 2 | Equations of state | How are pressure, volume and temperature tied together? |
| 3 | Probability and emergence | What shape does an average of many random quantities take? |
| 4 | Kinetic theory | Where does pressure come from, mechanically? |
| 5 | First law | Why does the energy delivered depend on the route taken? |
| 6 | Thermodynamic processes | What distinguishes the routes from one another? |
| 7 | Second law | Why can no engine do better than a certain efficiency? |
| 8 | Entropy | Why does anything happen in one direction and not the other? |
| 9–12 | Fundamental relation, potentials, ensembles, partition functions | How is all of the above one theory rather than a list of identities? |
| 13–18 | Advanced | Chemical potential, phases, transitions, radiation, quantum statistics, transport |

Modules 4, 5 and 8 are written; the rest are on their way. Nothing on this page depends on
reading them in order.

### Your readiness map

Match your five predictions against the answers, and use the quiz below as the real test. Then
spend your time where this table sends you.

<!-- Question numbers follow the order of assessment/quizzes/00-orientation.en.yml; reorder
     the bank and this table must be updated with it. -->

| Skill | Predicted in | Tested by | Refresh at |
|---|---|---|---|
| Mean and variance of a random variable | 1 | Q2 | [Derive](#00-orientation-derive), definitions box |
| The $N^{-1/2}$ law, and sum versus average | 2, 3 | Q1, Q3, Q9 | [Derive](#00-orientation-derive), boxed result |
| Dimensional analysis and SI units | 4 | Q4 | [Refresher — dimensional analysis](math-refresher.md#refresher-dimensions) |
| Partial derivatives and the total differential | 5 | Q5, Q6 | [Refresher — partial derivatives](math-refresher.md#refresher-partials) |
| Exact versus inexact differentials | — | Q7 | [Refresher — exact and inexact](math-refresher.md#refresher-exactness) |
| The course's conventions | — | Q8, Q10 | [Conventions](../conventions.md) |

Two reference pages sit outside the module sequence and are meant to be returned to rather
than read once: [conventions](../conventions.md), which lists the choices this course makes and
sticks to, and [the mathematics refresher](math-refresher.md), which is the toolkit it assumes.

(00-orientation-quiz)=
## Check your understanding

Score yourself honestly — this is a diagnostic, not an exam, and every item's feedback names
the section to revisit. The readiness map above turns your wrong answers into a study plan.

```{include} ../_generated/quiz-00-orientation.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](00-orientation-problems.md).

(00-orientation-explain)=
## Explain it in your own words

Answer in a few sentences each. These are the questions that reveal whether the ideas landed;
no number will save you.

1. A casino's profit on any single spin is unpredictable, yet its annual revenue is budgeted
   to within a fraction of a percent. Explain why, without letting the word "average" do
   unexamined work — your answer must say what role the number of spins plays.
2. A student says: "The average settles down because a run of high rolls gets cancelled by a
   run of low ones later." Repair this sentence, and say precisely what is wrong with the
   version given.
3. Why is a dimensionless ratio the only honest way to say that something is "steady"? Give an
   example where an absolute scatter would mislead you.
4. Look back at your five predictions. Which one was wrong, or which took you longest? Name
   the specific tool involved, and where you will go to sharpen it.

(00-orientation-advanced)=
## Advanced: from "typically close" to "almost certainly close"

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section. Later modules cite the variance
algebra above; none of them cite what follows.
:::

The derivation showed that the *typical* distance of $\bar{A}_N$ from $\mu$ shrinks as
$N^{-1/2}$. That is not the same as a guarantee. Turning it into one takes two short steps.

**Markov's inequality.** For a random variable $Y \ge 0$ and any $a > 0$,
$\langle Y \rangle \ge a \, P(Y \ge a)$, because the sum defining $\langle Y\rangle$ can only
lose by discarding every outcome below $a$ and replacing the rest by $a$. Hence

$$
P(Y \ge a) \le \frac{\langle Y \rangle}{a} .
$$

**Chebyshev's inequality.** Apply Markov to $Y = (X - \mu)^2$ and $a = \varepsilon^2$:

$$
P\big(|X - \mu| \ge \varepsilon\big) \le \frac{\sigma^2}{\varepsilon^2} .
$$

Applied to the average of $N$ independent dice, whose variance is $\sigma_1^2/N$, this gives

$$
P\big(|\bar{A}_N - \mu_1| \ge \varepsilon\big) \le \frac{\sigma_1^2}{N \varepsilon^2}
\;\xrightarrow[N \to \infty]{}\; 0
\qquad\text{for every fixed } \varepsilon > 0 .
$$

That is the **weak law of large numbers**, and it is now a genuine probability statement:
fix any tolerance you like, however tight, and the chance of missing it can be driven below
any bound by taking $N$ large enough. Note what carried the argument — only the existence of a
finite variance. No bell curve, no shape assumption, nothing about dice in particular.

**Why variance, and not some other measure of spread?** The mean absolute deviation
$\langle |X - \mu| \rangle$ is arguably a more natural measure of typical distance, and it is
the wrong tool here for one decisive reason: it does not add. Variances of independent
quantities add exactly, which is what let us go from one die to $N$ in a single line. That
additivity is the whole reason the second moment, rather than the first, sits at the centre of
statistical physics — and it is why you will meet $\sigma^2$ again as an energy fluctuation
tied to a heat capacity in module 18.
