---
title: Entropy and multiplicity
short_title: 08 · Multiplicity
module: 08-multiplicity
objectives:
  - id: OBJ-08-1
    text: Explain why an isolated system's drift toward equilibrium is a statement about counting microstates, not a mechanical law, and why time-reversible dynamics is fully consistent with it.
  - id: OBJ-08-2
    text: State the fundamental assumption of statistical mechanics — equal a priori probability of accessible microstates — and identify it correctly as a postulate, not a derived result.
  - id: OBJ-08-3
    text: Compute the multiplicity Ω(N,n) of a two-state system, explain why the even split dominates, and state how the peak's relative width scales with N.
  - id: OBJ-08-4
    text: Derive the Boltzmann entropy S = k_B ln Ω and explain why the logarithm is required for entropy to be additive across independent subsystems.
  - id: OBJ-08-5
    text: Use Stirling's approximation to connect microscopic counting to macroscopic, extensive thermodynamics, and state the size of the correction it neglects.
  - id: OBJ-08-6
    text: Distinguish entropy as a count of accessible microstates from "disorder," and state correctly which entropy the second law requires to increase.
---

# Entropy and multiplicity

(08-multiplicity-puzzle)=
## The puzzle: nothing forbids the corner

Open a valve between a chamber full of gas and an identical chamber that has been pumped out,
and the gas rushes through until both halves hold the same density. Wait as long as you like
and it never rushes back. Release a drop of perfume in a still room and the scent spreads
through the whole space; it never spontaneously regathers into the bottle.

Here is what makes this strange. Every collision between two gas molecules obeys Newton's
laws, and Newton's laws do not care which way time runs — reverse every velocity in a movie of
colliding billiard balls, and you get another perfectly valid movie of colliding billiard
balls. Microscopically, there is nothing that forbids the gas molecules from happening to
collide their way back into one corner. No law of mechanics singles out "spread out" as
special.

:::{important} The question
If the microscopic laws are indifferent to the direction of time, why does the macroscopic
world have such a strong preference for it? Why does gas spread and never regather, why does
cream mixed into coffee never unmixes, why does a shuffled deck never sort itself?
:::

The answer this module builds has nothing to do with forces becoming one-directional. It has
to do with *how many ways* each outcome can happen. "Spread out" is not special because it is
mechanically favoured — it is special because there are astronomically more arrangements of
the molecules that look spread out than arrangements that look gathered in a corner. Once you
can count those arrangements, the puzzle dissolves into arithmetic.

(08-multiplicity-predict)=
## Predict before you calculate

Commit to an answer for each of these before running anything.

1. You flip $4$ coins. How many of the $2^4 = 16$ possible outcomes have exactly $2$ heads?
   Now flip $100$ coins: is the *fraction* of outcomes with exactly $50$ heads larger or
   smaller than the fraction with exactly $2$ heads out of $4$?
2. $N$ gas particles start entirely in the left half of a partitioned box. The partition is
   removed. For $N = 10$, would you be surprised to see all $10$ particles back in the left
   half within a minute of watching? For $N = 10^{23}$?
3. Two crystals of the same element look identical under a microscope: same lattice, same
   density, same colour. One is made entirely of a single isotope. The other is a 50/50
   mixture of two isotopes of the same element, arranged randomly on the same lattice sites.
   Which crystal has the higher entropy — or are they the same?
4. An ice cube melts in a glass of warm water. Does the ice cube's own entropy go up or down
   as it melts? Does the water's entropy go up or down? Does the total?

:::{note} Why we ask first
Question 3 is the one this module will use to break a very common intuition, and question 4
is the one that breaks a second one. Committing to an answer first is the only way to notice
that you were wrong — reading the resolution afterwards feels obvious in a way that hides how
easy it is to get wrong in the moment.
:::

(08-multiplicity-explore)=
## Explore the model

The system here is deliberately the simplest one that shows the phenomenon: $N$ distinguishable
objects, each independently in one of two states. Read it as particles in the left or right
half of a box, coins showing heads or tails, or spins pointing up or down — the counting is
identical in every case.

:::{admonition} Model specification
:class: model-spec
- **System:** $N$ distinguishable objects, each in one of two states — particles in the left or right half of a box, coins showing heads or tails, spins up or down.
- **Dynamics:** for the sampled (Ehrenfest urn) version, one randomly chosen object switches state per step.
- **Boundary:** closed; $N$ is fixed throughout.
- **Ensemble:** microcanonical in the specific sense that every microstate is postulated equally probable — this assumption is the object this module examines, not a background detail.
- **Ignored:** interactions between objects, any energy difference between the two states, and any dynamics that would prefer one state over the other.
- **Valid when:** the two states are energetically equivalent and the objects behave independently of one another.
- **Failure modes:** interacting systems (an Ising magnet below its ordering temperature), or states with different energies, where the Boltzmann factor — not equal weighting — governs the probabilities.
:::

Here is the phenomenon that resolves the opening puzzle. On the left, two hundred objects
start entirely in one box and hop back and forth, one at a time, between it and an empty
second box; watch how quickly the occupancy settles near the even split and then stays there.
On the right, the multiplicity distribution $\Omega(N,n)/\Omega(N,N/2)$ itself, shown as $N$
grows — the same shape every time, only narrower.

:::{figure} ../media/multiplicity-two-box.mp4
:alt: Two hundred objects hopping between two boxes, one at a time; the occupancy of the first box starts at the extreme and settles near the even split.
:width: 100%

Left: the two boxes' populations as objects hop between them one at a time. Right: the
occupancy trace of the first box, drifting from the extreme starting point to the even split
and staying there — not because anything forbids it from wandering back, but because so few
of the accessible microstates put it there.
:::

:::{figure} ../media/multiplicity-peak.mp4
:alt: The relative multiplicity distribution as a function of fractional occupancy, narrowing sharply as N grows from a few objects to several hundred.
:width: 100%

The relative multiplicity $\Omega(N,n)/\Omega(N,N/2)$ against the fractional occupancy $n/N$,
for growing $N$. The curve is generated directly by `thermolab.multiplicity`. As $N$ grows the
region of appreciable multiplicity collapses onto the even split.
:::

:::{admonition} What this model cannot do
:class: model-assumption
This model does not explain *why* every microstate should be equally probable — that is a
postulate about the underlying dynamics (ergodicity, in more careful language), and this
module takes it as given rather than deriving it. What the model *can* do is show, with plain
counting, what that one postulate implies once you accept it. Be suspicious of any account
that treats "equal probability" as something obvious rather than as the specific assumption it
is.
:::

Run the laboratory now, then come back. Three things are worth doing before you read on:

- Start the two-box simulation from an extreme occupancy and watch how long it takes to reach
  the even split, for $N = 20$ versus $N = 400$.
- Plot $\Omega(N,n)$ for a small $N$ (say $N=10$) and check by hand what fraction of the
  $2^{10}=1024$ total arrangements sit at the peak, $n=5$.
- Watch the multiplicity distribution narrow as you increase $N$, and note that it narrows
  around the *same* central value, $n = N/2$, every time.

(08-multiplicity-derive)=
## Derive the result

**System and boundary.** $N$ distinguishable objects, each independently in one of two states,
isolated as a whole.

**Independent variable.** $N$; the macrostate is labelled by $n$, the number of objects in the
first state.

:::{admonition} Microstate versus macrostate
:class: definition
A **microstate** specifies the state of every object individually — for $N$ coins, the full
sequence of heads and tails. A **macrostate** specifies only a coarse summary — for $N$ coins,
just the total number of heads, $n$. Many microstates share one macrostate; the number that do
is the macrostate's **multiplicity**, $\Omega$.
:::

:::{admonition} The fundamental assumption of statistical mechanics
:class: model-assumption
Every accessible microstate of an isolated system is equally probable. This is **not a
theorem** — nothing in this module derives it from anything more basic. It is the foundational
postulate of statistical mechanics, justified by the fact that everything built on it agrees
with experiment, not by a proof from first principles. Every result below is a consequence of
this one assumption.
:::

Given the postulate, the probability of observing a particular macrostate is just the fraction
of all microstates that belong to it:

$$
P(n) = \frac{\Omega(N,n)}{2^N} ,
$$

since $2^N$ is the total number of microstates (each of the $N$ objects independently in
either state) and $\Omega(N,n)$ counts how many of them have exactly $n$ objects in the first
state.

### Counting the multiplicity

Choosing *which* $n$ of the $N$ objects are in the first state is a combinations problem:

$$
\Omega(N,n) = \binom{N}{n} = \frac{N!}{n!\,(N-n)!} .
$$

For $N=10$, direct counting gives $\Omega(10,0)=1$, $\Omega(10,5)=252$, and
$\sum_{n=0}^{10}\Omega(10,n) = 1024 = 2^{10}$, exactly as it must. The macrostate $n=5$ alone
accounts for $252/1024 \approx 24.6\%$ of all microstates, while $n=0$ (every object in the
first state) accounts for $1/1024 \approx 0.1\%$. Already at $N=10$ the even split is roughly
$250$ times more likely than the fully ordered extreme — and this ratio only grows with $N$.

### Why the even split dominates, and by how much

$\Omega(N,n)$ is maximised at $n=N/2$ (for even $N$) because moving away from the even split
in either direction always removes more ways of achieving the macrostate than it adds — the
binomial coefficients fall off symmetrically from the centre. Near the peak, expanding
$\ln\Omega(N,n)$ to second order in $n - N/2$ turns the discrete distribution into a Gaussian:

:::{admonition} The Gaussian limit
:class: approximation
For $N$ large, $\dfrac{\Omega(N,n)}{2^N} \approx \dfrac{1}{\sigma\sqrt{2\pi}}
\exp\!\left[-\dfrac{(n - N/2)^2}{2\sigma^2}\right]$ with $\sigma = \sqrt{N}/2$. This is the
central limit theorem in its most physical guise: a sum of many independent binary choices
becomes Gaussian regardless of the details, and the width of that Gaussian is set by $N$ alone.
The approximation is excellent once $N$ is a few thousand — it matches the exact combinatorial
result to better than $1\%$ near the peak for $N=4000$ — but it is an approximation, valid only
near $n=N/2$ and only for large $N$; it says nothing reliable about the far tails.
:::

The relative width of that peak — its standard deviation divided by its centre — is

$$
\frac{\sigma}{N/2} = \frac{\sqrt{N}/2}{N/2} = \frac{1}{\sqrt{N}} .
$$

This is the same $N^{-1/2}$ law that governed the pressure fluctuations in module 04, arising
here from the sharpest possible source: pure combinatorics. It is exact algebra given the
Gaussian width above, and it says that the *fraction* of microstates lying within a fixed
relative distance of the even split shrinks as the system grows — which is precisely why an
isolated gas is never observed gathering in a corner. Nothing forbids it mechanically; there
are simply too few ways for it to happen once $N$ is large.

### Boltzmann entropy

:::{admonition} Boltzmann's entropy
:class: definition
$$
\boxed{\; S = k_B \ln \Omega \;}
$$
The entropy of a macrostate is $k_B$ times the natural log of its multiplicity. A macrostate
reachable by only one microstate has $\Omega=1$ and $S=0$ — the anchor of the entropy scale;
every other macrostate has strictly positive entropy.
:::

:::{admonition} Why entropy is a logarithm
:class: theorem
For two independent subsystems A and B, every microstate of A can be paired with every
microstate of B, so multiplicities multiply: $\Omega_{AB} = \Omega_A \, \Omega_B$. Thermodynamic
entropy is required to be additive — the entropy of two separate systems brought together
without interaction is the sum of their entropies, exactly as $N$ or $V$ add for two combined
samples of gas. A function that turns products into sums is, up to a constant, the logarithm.
That is why $S \propto \ln\Omega$ rather than, say, $S \propto \Omega$: the logarithm is not a
stylistic choice, it is the one operation compatible with extensivity.
:::

:::{admonition} Entropy counts arrangements, not appearance
:class: numerical-observation
Take $N=1000$ atomic sites in a crystal lattice. A crystal built from a single isotope has
$n=0$ (or $n=N$): $\Omega=1$ and $S=0$. A crystal built from a 50/50 random mixture of two
isotopes of the *same* element, on the *same* lattice, is chemically and visually
indistinguishable from the pure crystal — same structure, same density, same appearance under
any ordinary microscope. But its multiplicity is $\Omega(1000,500) \approx 2.7\times10^{299}$ —
larger than the pure crystal's $\Omega=1$ by a factor of $e^{689.5}$ — giving
$S \approx 9.5\times 10^{-21}\ \mathrm{J/K}$ against the pure crystal's exactly zero. Nothing
about the mixed crystal *looks* more disordered. It has enormously more entropy because
entropy counts accessible microstates, and there are astronomically many ways to distribute two
isotopes across a lattice while producing the same macroscopic appearance every time.
:::

That example is worth sitting with. "Entropy is disorder" is a useful cartoon for some cases —
a shuffled deck genuinely has higher multiplicity than a sorted one — but the cartoon breaks
whenever the *appearance* of a macrostate and its *multiplicity* come apart, and isotope
mixing is exactly such a case: the crystal looks equally tidy either way.

### Stirling's approximation and the thermodynamic limit

Direct computation of $N!$ for macroscopic $N$ is neither necessary nor possible; the results
above rest on $\ln N!$, approximated by Stirling's formula:

:::{admonition} Stirling's approximation
:class: approximation
$$
\ln N! \approx N\ln N - N + \tfrac{1}{2}\ln(2\pi N) ,
$$
The first two terms are the version usually quoted in introductory treatments; the third,
$\tfrac{1}{2}\ln(2\pi N)$, is the next correction, and the full asymptotic series continues with
a term of order $1/(12N)$. Measured against the exact value, the two-term form is off by about
$2.1$ at $N=10$ and grows *slowly worse* in absolute terms as $N$ grows (about $5.5$ at
$N=10^4$, since the omitted piece scales as $\tfrac12\ln(2\pi N)$); the three-term form is off
by about $0.008$ at $N=10$ and about $8\times10^{-6}$ at $N=10^4$, matching the predicted
$1/(12N)$ bound. For any $N$ worth calling macroscopic, both forms are excellent — but only the
three-term form should be trusted for the sub-leading, order-$\ln N$ physics this module cares
about.
:::

Applying Stirling to the peak multiplicity gives the exact asymptotic form

$$
\ln \Omega(N, N/2) = N \ln 2 - \tfrac{1}{2}\ln\!\left(\frac{\pi N}{2}\right) + O(1/N) .
$$

The leading term, $N\ln 2$, is extensive — it doubles when $N$ doubles, exactly as entropy
should. The correction term is not: it grows only logarithmically, so it becomes negligible
*relative to* the leading term as $N\to\infty$, but it is never exactly zero at finite $N$.

:::{admonition} Extensivity is a thermodynamic-limit statement
:class: numerical-observation
Splitting a system of $2N$ objects (macrostate $n=N$, i.e. the even split) into two identical
halves of $N$ objects each (each also at its own even split) should, if entropy were exactly
extensive, give $S(2N,N) = 2\,S(N,N/2)$. Computed directly, the relative discrepancy between
the two sides is about $0.9\%$ at $N=200$, $0.13\%$ at $N=2000$, $0.017\%$ at $N=20{,}000$, and
$0.0022\%$ at $N=200{,}000$ — shrinking exactly as the $\tfrac12\ln(\pi N)$ correction above
predicts. Extensivity is not built into the definition of entropy; it is something the
combinatorics delivers only in the limit of large $N$, and the approach to that limit is
measurable, not assumed.
:::

(08-multiplicity-verify)=
## Verify computationally

**1. Small-$N$ combinatorics.** $\Omega(N,n)$ from the log-gamma implementation matches
$\binom{N}{n}$ computed by exact integer arithmetic, for every $n$ at $N=1,2,10,25$.

**2. The peak sits at the even split.** For $N=100$, the macrostate that maximises
$\Omega(100,n)$ over all $101$ values of $n$ is exactly $n=50$.

**3. The Gaussian limit.** At $N=4000$, the Gaussian approximation to $\Omega(N,n)/2^N$ agrees
with the exact combinatorial value to better than $1\%$ across the range $n \in [1700, 2300]$.

**4. Stirling's error bound.** The three-term approximation's error stays under $1.01/(12N)$
at $N=10,100,1000$ — the code's tests measure this bound rather than asserting it.

**5. The Ehrenfest urn finds and holds the even split.** Started from every object on one
side, a system of $N=400$ objects sampled for $40{,}000$ steps has its late-time occupancy
fraction land within $2\%$ of exactly one half, with a late-time spread under $5\%$ of $N$ —
and it *stays* there rather than passing through and continuing on.

:::{admonition} Where the resistance to the corner comes from
:class: numerical-observation
At $N=100$, a macrostate $10\%$ off the even split ($n=60$ instead of $n=50$) is still about
$13.6\%$ as probable as the peak — not rare at all. At $N=10{,}000$, the *same* $10\%$ relative
excess ($n=6000$ instead of $n=5000$) is suppressed by a factor of roughly
$3.6\times10^{-88}$ relative to the peak. Nothing about the underlying dynamics changed between
these two cases — only $N$ did. This is the quantitative answer to the opening puzzle: the gas
never gathers in a corner not because it is forbidden to, but because the number of ways to do
so, relative to the number of ways to be spread out, falls off faster than any physical process
could ever explore in the time available.
:::

:::{admonition} A caution about what the simulation proves
:class: open-question
The Ehrenfest urn shows a system started away from equilibrium finding its way to the peak and
staying near it — consistent with the derivation, and useful for building intuition. It does
not, by itself, prove that *every* isolated system behaves this way; that rests on the
equal-probability postulate, which this module assumes rather than establishes. A simulation
can support a derivation. It is not a substitute for one.
:::

(08-multiplicity-transfer)=
## Transfer the idea

The same structure — count the microstates, note that one macrostate has overwhelmingly more
of them, and call the log of that count "entropy" — reappears far beyond two-state systems.

- **Free expansion and diffusion.** A gas released into a larger volume, or a drop of ink
  diffusing through water, is the same phenomenon as the two-box system: astronomically more
  microstates correspond to "spread out" than to "concentrated," so spreading is what happens,
  every time, without any force driving it.
- **Entropy of mixing.** Two different gases (or, as above, two isotopes on a lattice) mixed
  together have more entropy than either kept separately, purely from the combinatorics of
  interleaving them — the same $\Omega(N,n)$ counting, applied to molecules instead of coin
  flips.
- **Entropic elasticity.** A stretched rubber band pulls back not primarily because stretching
  its polymer chains costs energy, but because a stretched chain has far fewer available
  configurations than a relaxed, coiled one — an entropic force, with the restoring tendency
  coming from exactly the same "more ways to be typical" counting used throughout this module.
- **Shannon information entropy.** Claude Shannon's measure of the information content of a
  message, $H = -\sum_i p_i \log p_i$, has the identical mathematical form as the entropy this
  module derives, for the identical reason: it is the unique measure, up to a constant, that is
  additive over independent choices.

:::{admonition} A word on irreversibility
:class: definition
A process is **statistically irreversible** when the reverse process, while not forbidden by
the microscopic laws, corresponds to such a small fraction of the accessible microstates that
it is never observed in practice. This is different from being *mechanically* forbidden.
Nothing here contradicts time-reversal symmetry; the asymmetry lives entirely in the counting,
not in the laws of motion.
:::

(08-multiplicity-quiz)=
## Check your understanding

```{include} ../_generated/quiz-08-multiplicity.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](08-multiplicity-problems.md).

(08-multiplicity-explain)=
## Explain it in your own words

Answer in a few sentences each.

1. A student says: "Gases spread out because spreading out is the natural direction of time."
   Rewrite this so that it is actually correct, and say precisely what was wrong with the
   original.
2. Two crystals look identical to the eye but have very different entropies. Explain how this
   is possible without contradicting the idea that entropy measures "how spread out" a system
   is.
3. A subsystem's entropy decreases while the total entropy of the isolated system it belongs to
   increases. Is this a violation of anything you have learned in this module? Justify your
   answer using the additivity of $\Omega$ for independent subsystems.
4. Explain, without writing an equation, why doubling the number of coin flips makes the
   fraction landing exactly at $50\%$ heads shrink relative to nearby outcomes, even though the
   *number of ways* to land at $50\%$ heads grows enormously.

(08-multiplicity-advanced)=
## Advanced: beyond the simplest picture

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section.
:::

**A subsystem's entropy can fall while the total rises.** Consider two independent two-state
populations, $L$ and $R$, each with $N=300$ objects, so that their combined entropy is exactly
additive: $S_{LR} = S_L + S_R$. Suppose $L$ starts exactly at its own peak, $n_L=150$
($\ln\Omega_L \approx 204.87$), while $R$ starts far from its peak, at $n_R=280$
($\ln\Omega_R \approx 71.09$). Now let the coupling between them nudge $L$ slightly away from
its peak, to $n_L=145$ ($\ln\Omega_L \approx 204.70$, a decrease of about $0.17\,k_B$), while
$R$ relaxes all the way to its own peak, $n_R=150$ ($\ln\Omega_R \approx 204.87$, an increase of
about $133.77\,k_B$). Subsystem $L$'s entropy strictly *decreased*. The total,
$\Delta S_{LR}/k_B \approx -0.17 + 133.77 \approx 133.6$, strictly increased. Both statements are
exact consequences of the same combinatorics used throughout this module. The second law, as
this module has derived it, constrains the entropy of an *isolated total system*; it places no
such requirement on any piece of that system considered on its own.

Read that example for what it is: an arithmetic demonstration that the two statements are
compatible, not a dynamical account of why $L$ would move. In this energy-free two-state model
nothing couples $L$ to $R$, so the displacement of $L$ is stipulated rather than driven. A
mechanism needs a conserved quantity the two subsystems actually exchange — energy in module
11, particles in module 13 — and then the direction of the exchange is fixed by requiring the
*total* multiplicity to increase. The arithmetic above is what makes room for a refrigerator:
a subsystem's entropy may fall, provided something else pays more than the difference.

**Full Stirling series.** The three-term approximation used above is the start of an asymptotic
series, $\ln N! = N\ln N - N + \tfrac12\ln(2\pi N) + \tfrac{1}{12N} - \tfrac{1}{360N^3} +
\cdots$. The series does not converge as $N\to\infty$ for fixed number of terms — it is an
asymptotic expansion, useful because truncating it after a few terms gives an error smaller
than the first omitted term, which is exactly the bound the $1/(12N)$ figure above reflects.

**Loschmidt's paradox and Poincaré recurrence.** If the microscopic dynamics are exactly
time-reversible, a purist objection follows: any trajectory that spreads out has a
time-reversed twin that gathers back up, so how can spreading be typical? The resolution is
entirely quantitative, and this module has already computed the relevant number: at $N=10{,}000$,
a state just $10\%$ off the even split is suppressed by a factor of $10^{-88}$ relative to the
peak. A macroscopic gas has $N \sim 10^{23}$, where the analogous suppression factor is
inconceivably smaller still. Poincaré's recurrence theorem guarantees that an isolated,
bounded, energy-conserving system does eventually return arbitrarily close to any earlier
state, including a "gathered in one corner" state — but for a macroscopic $N$ the expected
waiting time vastly exceeds the age of the universe. Reversibility of the underlying dynamics
and the practical irreversibility of the macroscopic world are both true at once; the numbers
above are what reconcile them.

**Gibbs paradox, briefly.** The isotope-mixing example earlier relied on the two isotopes being
genuinely distinguishable species — the entropy of mixing counted above is real and measurable.
Mixing two samples of the *literally same* substance, by contrast, produces no increase in
multiplicity at all, because swapping two identical particles does not create a new microstate.
Treating identical particles as if they were distinguishable is precisely the mistake that
historically produced the paradox; the fix is to divide the naive count by the particles'
indistinguishability, a correction this module's model sidesteps by keeping its $N$ objects
explicitly distinguishable (particles by box, coins by flip) throughout.
