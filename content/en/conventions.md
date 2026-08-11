---
title: Conventions used everywhere
short_title: Conventions
---

# Conventions used everywhere

Thermal physics has more arbitrary choices in it than most subjects: signs, symbols, which
variables are held fixed, what counts as established. None of them changes the physics, and
all of them change the formulas. Textbooks differ, and a student comparing two sources
silently switching between conventions can lose a week to a stray minus sign.

So this course fixes its choices once, here, and never varies them. This page is the place to
come back to when a formula elsewhere does not match one of ours.

(conventions-sign)=
## The sign of work

The first law says that the internal energy of a system changes by whatever energy crosses
its boundary. The arbitrary part is which *direction* counts as positive for work. Both
common choices appear in the literature:

| | This course | The other common choice |
|---|---|---|
| First law | $\mathrm{d}U = \dbar Q + \dbar \Won$ | $\mathrm{d}U = \dbar Q - \dbar W_{\mathrm{by}}$ |
| Positive work means | energy put **into** the system | energy taken **out** by the system |
| Quasistatic compression, $\mathrm{d}V<0$ | $\dbar \Won = -P\,\mathrm{d}V > 0$ | $\dbar W_{\mathrm{by}} = P\,\mathrm{d}V < 0$ |
| Converting between them | $\Won = -W_{\mathrm{by}}$ | $W_{\mathrm{by}} = -\Won$ |

**This course always uses the first column.** Heat added to the system is positive; work done
*on* the system is positive; both add to $U$, with no minus sign to remember. It is the
convention of most modern statistical-physics texts, and it has the pedagogical advantage that
the first law reads as plain energy bookkeeping: everything that goes in, adds.

:::{admonition} A worked example, so the sign is concrete
:class: definition
A gas is compressed quasistatically from $V_1$ to $V_2 < V_1$ against pressure $P$. The work
appearing in our first law is

$$
\Won = -\int_{V_1}^{V_2} P \,\mathrm{d}V .
$$

Because $V_2 < V_1$ the integral is negative, so $\Won$ is **positive**: you pushed the piston
in, and energy went into the gas. If the gas expands instead, $\Won$ is negative — the gas
spent energy pushing its surroundings. Check every result you derive against this one sentence
and you will never lose the sign.
:::

The other convention appears symbolically on this page and nowhere else in the course, with a
single exception: the engines and refrigerators of module 7 are conventionally analysed in
terms of the work delivered by the machine, so that one module converts explicitly, in one
clearly marked block, and converts back. Everywhere else — including problem sets, quizzes and
the laboratories — the first column is the only one in use. A project lint enforces this.

(conventions-differentials)=
## $\mathrm{d}$ and $\dbar$: state functions and path functions

| Symbol | Meaning | Examples |
|---|---|---|
| $\mathrm{d}X$ | an exact differential: $X$ is a property of the state | $\mathrm{d}U$, $\mathrm{d}S$, $\mathrm{d}V$, $\mathrm{d}T$ |
| $\dbar Y$ | an inexact differential: $Y$ describes a transfer, not a property | $\dbar Q$, $\dbar \Won$ |

A system *has* an internal energy and *has* an entropy; it does not have a heat or a work.
Heat and work are names for energy in transit, and how much of each crosses the boundary
depends on the route the system took, not merely on where it started and finished. Writing
$\mathrm{d}Q$ would assert that some function $Q$ of the state exists to be differentiated.
None does.

The mathematics behind the distinction — what makes a differential form exact, and how to
test — is in [the refresher](foundations/math-refresher.md#refresher-exactness); the physics
arrives in module 5.

(conventions-units)=
## Units and constants

- **SI throughout.** Metres, kilograms, seconds, kelvin, and their combinations. Where a
  problem quotes litres or atmospheres, convert before computing.
- **$\kB$ is always written explicitly.** Many advanced texts set $\kB = 1$ and measure
  temperature in energy units. That is elegant and it hides exactly the conversion a student
  is trying to learn, so the core modules never do it. Entropy therefore carries units of
  $\mathrm{J\,K^{-1}}$, not "nats".
- **$R = N_A \kB$.** Where chemistry writes $PV = nRT$ with $n$ in moles, we write
  $PV = N\kB T$ with $N$ a plain count of particles. The two are the same statement.
- **Temperatures are absolute.** Kelvin, always, unless a difference is being quoted.
- **The library works in plain SI floats.** `thermolab` deliberately does not wrap quantities
  in a units package, so that a student can read `P = N * K_B * T / V` and recognise it.
  Dimensional correctness is enforced in the test suite instead, where every formula is
  re-evaluated with `pint` quantities.

(conventions-epistemic)=
## Epistemic labels: what kind of claim is this?

Thermal physics mixes exact mathematics, empirical laws, modelling choices and numerical
evidence, often within one paragraph. Blurring them is how students end up believing that a
simulation "proved" an identity. Every boxed claim in this course therefore carries a label
saying what kind of statement it is, and the boxes below are one live example of each.

:::{admonition} Definition
:class: definition
A **definition** introduces a name for something. It cannot be true or false, only useful or
useless: *the heat capacity at constant volume is $C_V = (\partial U/\partial T)_V$*.
:::

:::{admonition} Empirical law
:class: empirical-law
An **empirical law** summarises measurement. It could have come out otherwise, and it holds
within the range where it has been tested: *the pressure of a dilute gas is proportional to
its absolute temperature at fixed volume*.
:::

:::{admonition} Theorem
:class: theorem
A **theorem** follows by mathematics from stated premises. If you accept the premises you must
accept the conclusion: *variances of independent random variables add*.
:::

:::{admonition} Model assumption
:class: model-assumption
A **model assumption** is a deliberate simplification, adopted because it makes a calculation
possible: *the particles in this simulation have no volume and never collide with one
another*.
:::

:::{admonition} Approximation
:class: approximation
An **approximation** is a controlled error with a regime of validity attached: *Stirling's
formula $\ln N! \approx N \ln N - N$, whose relative error falls off as $\ln N / N$*.
:::

:::{admonition} Numerical observation
:class: numerical-observation
A **numerical observation** is something a computation showed. It is evidence, not proof, and
it is only as good as the model behind it: *the fitted exponent was $-0.50 \pm 0.02$*.
:::

:::{admonition} Open question
:class: open-question
An **open question** flags a genuine unresolved issue, or a place where the course is being
deliberately silent: *whether the second law's arrow of time is explained by the initial
condition of the universe is not settled here, or anywhere*.
:::

(conventions-modelspec)=
## Model specifications

Every simulation in the course — on a page or in a notebook — carries a seven-field block
saying exactly what is being modelled. The fields never change and never reorder, so you can
scan them. This is the one from the orientation module, which is the simplest in the course:

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

The two fields students skip are the two worth reading. **Ignored** tells you what the model
is blind to, which is where its answers will be wrong. **Failure modes** names the regimes
where it stops being a useful description at all — and an exam question that asks "when does
this break down?" is asking you to reproduce that field.

(conventions-difficulty)=
## The shape of a module

Every module page climbs in the same four steps, and you can enter and leave at the step that
suits you.

1. **Opening** — a physical puzzle, and predictions you commit to before any equation. No
   prerequisites at all.
2. **Core** — the laboratory, the derivation, and the computational check. This is the
   exam-relevant spine, and it is the part to work through with a pen.
3. **Consolidation** — transfer to other settings, quizzes, exam-style problems, and
   reflection questions.
4. **Advanced** — deeper material, always marked with the box below and always last.

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Wherever you see this box, the material below it is optional. The promise is strict, and the
course is built to keep it: **no core content in any later module depends on any advanced
section**. Skip freely; come back when you are curious.
:::

(conventions-simulation)=
## Simulation never proves

A simulation is a numerical experiment on a model. It can show you that a result is plausible,
reveal where your intuition is wrong, and catch algebra errors. It cannot establish an
identity, because it only ever examined finitely many cases of one particular model.

The division of labour this course keeps to:

- **Derivations establish.** An identity is true because it follows from stated premises.
- **Simulations illustrate and check.** They make a result visible and they catch mistakes.
- **Experiments decide.** Whether a model describes the world is not a question mathematics or
  computation can answer.

When a page says "the fitted exponent is $-0.5$", that is a numerical observation about a
model. When it says "the relative scatter of an average of $N$ independent quantities is
$\sigma_1/(\mu_1\sqrt{N})$", that is a theorem. The first is evidence for having implemented
the second correctly. It is not why the second is true.
