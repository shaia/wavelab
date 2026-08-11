---
title: Mathematics refresher
short_title: Refresher
---

# Mathematics refresher

Thermal physics uses a small, specific set of mathematical tools, and it uses them constantly.
This page is the toolkit — not a course in calculus, but the particular corners of it that
this subject leans on, with the notation this course will use for them.

It is a reference, not a narrative. Read the section the
[readiness map](00-orientation.md#00-orientation-transfer) sent you to, work its examples with
a pen, and come back when a later module makes you unsure.

(refresher-dimensions)=
## Dimensional analysis and units

Every physical quantity carries dimensions, built from the SI base quantities. Four of the
seven matter for us:

| Quantity | Dimension | SI unit |
|---|---|---|
| length | $\mathsf{L}$ | metre, $\mathrm{m}$ |
| mass | $\mathsf{M}$ | kilogram, $\mathrm{kg}$ |
| time | $\mathsf{T}$ | second, $\mathrm{s}$ |
| temperature | $\Theta$ | kelvin, $\mathrm{K}$ |

Everything else is a product of powers of these. Energy is
$\mathsf{M}\mathsf{L}^2\mathsf{T}^{-2}$ (the joule); pressure is force per area,
$\mathsf{M}\mathsf{L}^{-1}\mathsf{T}^{-2}$ (the pascal).

:::{admonition} Two rules, and what they let you do
:class: definition
1. **Only quantities of the same dimensions may be added or compared.** An equation whose two
   sides differ dimensionally is not approximately right; it is meaningless.
2. **The argument of $\exp$, $\ln$, $\sin$ and friends must be dimensionless.** This is why
   $\exp(-E/\kB T)$ has the form it does: $\kB T$ exists to make the exponent a pure number.
:::

**Reading the units of an unfamiliar constant.** You never need to memorise them. From
$PV = N \kB T$, with $N$ a pure count,

$$
[\kB] = \frac{[P][V]}{[T]} = \frac{\mathrm{Pa} \cdot \mathrm{m}^3}{\mathrm{K}}
= \frac{\mathrm{J}}{\mathrm{K}} ,
$$

so $\kB$ is an energy per unit temperature — which is the whole content of the statement
"temperature is a measure of energy per degree of freedom".

**Checking a candidate formula.** Suppose you cannot remember whether the root-mean-square
speed of a gas molecule is $\sqrt{3\kB T/m}$ or $\sqrt{3\kB T/m^2}$ or $\sqrt{3\kB T m}$. Only
one of them is a speed:

$$
\left[\frac{\kB T}{m}\right]
= \frac{\mathsf{M}\mathsf{L}^2\mathsf{T}^{-2}}{\mathsf{M}}
= \mathsf{L}^2\mathsf{T}^{-2} ,
\qquad \text{so} \qquad
\left[\sqrt{\frac{\kB T}{m}}\,\right] = \mathsf{L}\mathsf{T}^{-1} . \checkmark
$$

The other two fail. This costs ten seconds and catches a large fraction of all algebra errors.

**When two different quantities share a unit.** Pressure is a force per area and energy
density is an energy per volume, and they are the same thing dimensionally:

$$
\mathrm{Pa} = \frac{\mathrm{N}}{\mathrm{m}^2}
= \frac{\mathrm{N}\cdot\mathrm{m}}{\mathrm{m}^3}
= \frac{\mathrm{J}}{\mathrm{m}^3} .
$$

That is not a coincidence — it is the hint that pressure is going to turn out to be about
energy — but it is also not an identity. A monatomic ideal gas has $P = \tfrac{2}{3}u$ and
isotropic radiation has $P = \tfrac{1}{3}u$, where $u$ is the energy density. Sharing a
dimension tells you two quantities *can* be related; it never tells you by what factor. (This
is prediction 4 on the [orientation page](00-orientation.md#00-orientation-predict); the
physics behind the factors arrives in modules 4 and 16.)

:::{admonition} What dimensional analysis cannot do
:class: approximation
It cannot produce dimensionless factors. $\sqrt{\kB T/m}$, $\sqrt{2\kB T/m}$ and
$\sqrt{3\kB T/m}$ are dimensionally identical, and which one is right depends on physics the
dimensions know nothing about. Use it to *reject* wrong formulas, never to *derive* right
ones.
:::

**Comparing numbers honestly.** Two quantities agree when their *fractional* difference is
small:

$$
|a - b| / |b| \ll 1 .
$$

Absolute differences mean nothing without a scale to compare
them to: the energies in this course are routinely around $10^{-18}\,\mathrm{J}$, so a test
asking whether two of them differ by less than $10^{-12}\,\mathrm{J}$ will answer "no
difference" whatever the physics did.

(refresher-partials)=
## Partial derivatives, and saying what is held fixed

For a function of several variables, the **partial derivative** with respect to one of them
is the ordinary derivative taken with the others held constant. For $f(x,y) = x^2 y$:

$$
\left(\frac{\partial f}{\partial x}\right)_{y} = 2xy ,
\qquad
\left(\frac{\partial f}{\partial y}\right)_{x} = x^2 .
$$

The subscript is not decoration. In ordinary calculus the notation $\partial f/\partial x$ is
unambiguous because the list of variables is fixed by how $f$ was written. In thermodynamics
it is not: $P$, $V$, $T$ and $N$ are tied together by an equation of state, so any of them can
be eliminated in favour of the others, and "the derivative with respect to $T$" means
different things depending on what you chose to hold.

:::{admonition} Why thermodynamics writes the subscript
:class: definition
$\left(\partial U/\partial T\right)_{V}$ and $\left(\partial U/\partial T\right)_{P}$ are
different functions — they are the heat capacities at constant volume and at constant
pressure, and they differ by a measurable amount. Dropping the subscript makes the expression
ambiguous rather than merely untidy. Write it every time.
:::

**Mixed partials commute.** For any function with continuous second derivatives,

$$
\frac{\partial}{\partial y}\left(\frac{\partial f}{\partial x}\right)
= \frac{\partial}{\partial x}\left(\frac{\partial f}{\partial y}\right) .
$$

For $f = x^2y$ both routes give $2x$. This innocuous fact turns into a machine for generating
thermodynamic identities — the Maxwell relations of module 10 are nothing more than this
statement applied to the thermodynamic potentials — and it is also the exactness criterion
below.

(refresher-differential)=
## The total differential

The **total differential** of $f(x,y)$ collects both first-order responses:

$$
\mathrm{d}f
= \left(\frac{\partial f}{\partial x}\right)_{y} \mathrm{d}x
+ \left(\frac{\partial f}{\partial y}\right)_{x} \mathrm{d}y .
$$

For $f = x^2 y$ this reads $\mathrm{d}f = 2xy\,\mathrm{d}x + x^2\,\mathrm{d}y$. Read
practically: it says how much $f$ changes when you nudge $x$ and $y$ by small amounts, to
first order in the nudges.

**Along a path, the partial and the total derivative differ.** Suppose we move along the line
$y = x$. Substituting first gives $f = x^3$, hence $\mathrm{d}f/\mathrm{d}x = 3x^2$, which is
$3$ at $x=1$. But $(\partial f/\partial x)_y$ at $(1,1)$ is $2xy = 2$. The two numbers are
different and both are correct — they answer different questions. Dividing the total
differential by $\mathrm{d}x$ shows exactly where the gap comes from:

$$
\frac{\mathrm{d}f}{\mathrm{d}x}\bigg|_{y=x}
= \left(\frac{\partial f}{\partial x}\right)_{y}
+ \left(\frac{\partial f}{\partial y}\right)_{x} \frac{\mathrm{d}y}{\mathrm{d}x}
= 2xy + x^2 \cdot 1 = 3x^2 .
$$

The partial derivative ignores the fact that $y$ is changing too. The total derivative does
not. If prediction 5 on the module page caught you, this is the identity that resolves it.

(refresher-lineintegral)=
## Line integrals of a differential form

An expression $\omega = M(x,y)\,\mathrm{d}x + N(x,y)\,\mathrm{d}y$ is called a **differential
form**. It is not a number; it becomes one only once you supply a path $C$ to integrate along:

$$
\int_C \omega = \int_C \big( M\,\mathrm{d}x + N\,\mathrm{d}y \big) .
$$

To evaluate it, parametrise the path as $\big(x(t), y(t)\big)$ for $t$ from $t_0$ to $t_1$ and
substitute:

$$
\int_C \omega = \int_{t_0}^{t_1}
\left[ M\big(x(t),y(t)\big) \frac{\mathrm{d}x}{\mathrm{d}t}
     + N\big(x(t),y(t)\big) \frac{\mathrm{d}y}{\mathrm{d}t} \right] \mathrm{d}t .
$$

**Worked example.** Take $\omega = y\,\mathrm{d}x$ and go from $(0,0)$ to $(1,1)$ three ways.

- *Along the diagonal* $y = x$: put $x = t$, $y = t$, so
  $\int_0^1 t \,\mathrm{d}t = \tfrac{1}{2}$.
- *Across, then up*: on the first leg $y = 0$, so the integrand vanishes; on the second leg
  $x$ is constant so $\mathrm{d}x = 0$. Total: $0$.
- *Up, then across*: on the first leg $\mathrm{d}x = 0$; on the second $y = 1$ and $x$ runs
  from $0$ to $1$, giving $\int_0^1 1 \,\mathrm{d}x = 1$. Total: $1$.

Same start, same finish, three different answers: $0$, $\tfrac{1}{2}$, $1$. The integral of a
differential form is in general a property of the *route*, not of the endpoints.

(refresher-exactness)=
## Exact and inexact forms

Sometimes a form is the total differential of some function, and then the route stops
mattering.

:::{admonition} Exactness, and how to test for it
:class: theorem
The form $\omega = M\,\mathrm{d}x + N\,\mathrm{d}y$ is **exact** when there is a function
$f(x,y)$ — a potential — with $M = (\partial f/\partial x)_y$ and
$N = (\partial f/\partial y)_x$, so that $\omega = \mathrm{d}f$.

On a simply connected region this holds exactly when

$$
\left(\frac{\partial M}{\partial y}\right)_{x}
= \left(\frac{\partial N}{\partial x}\right)_{y} ,
$$

which is just the statement that mixed partials of $f$ commute. When $\omega$ is exact,

$$
\int_C \omega = f(\text{end}) - f(\text{start})
$$

for every path $C$ between those points, and $\oint \omega = 0$ around every closed loop.
:::

Apply the test to the two forms we have been using:

- $\omega_1 = y\,\mathrm{d}x + x\,\mathrm{d}y$: here $\partial M/\partial y = 1$ and
  $\partial N/\partial x = 1$. Equal, so $\omega_1$ is **exact** — and indeed
  $\omega_1 = \mathrm{d}(xy)$. Every route from $(0,0)$ to $(1,1)$ gives $1 \cdot 1 - 0 = 1$.
- $\omega_2 = y\,\mathrm{d}x$: here $\partial M/\partial y = 1$ but $\partial N/\partial x = 0$.
  Unequal, so $\omega_2$ is **inexact** — which is why the three routes above disagreed. There
  is no function whose differential it is, and writing "$\mathrm{d}(\text{something})$" for it
  would be a mistake.

This distinction is the reason this page exists. In module 5 the plane becomes the $P$–$V$
plane, and one of the forms you will integrate is exact while another is not. The exact one
integrates to a change in internal energy, which depends only on the endpoints; the inexact
one integrates to heat or to work, which depend on the route. Nothing physical is needed to
see the difference — it is already here, in $y\,\mathrm{d}x$.

:::{admonition} A notation you will meet
:class: definition
Because the distinction matters so much, this course marks it in the symbol itself: an exact
differential is written $\mathrm{d}$, an inexact one $\dbar$. So $\mathrm{d}U$ but
$\dbar Q$ and $\dbar \Won$. See [conventions](../conventions.md#conventions-differentials).
:::

:::{admonition} Looking ahead: integrating factors
:class: advanced
An inexact form can sometimes be made exact by multiplying it by a well-chosen function. Take
$\omega_3 = y\,\mathrm{d}x - x\,\mathrm{d}y$, which is inexact because
$\partial M/\partial y = 1$ while $\partial N/\partial x = -1$. Divide it by $y^2$:

$$
\frac{y\,\mathrm{d}x - x\,\mathrm{d}y}{y^{2}}
= \frac{\mathrm{d}x}{y} - \frac{x\,\mathrm{d}y}{y^{2}}
= \mathrm{d}\!\left(\frac{x}{y}\right) ,
$$

which is exact on any region avoiding $y = 0$. The function you multiplied by — here $1/y^2$ —
is called an **integrating factor**.

This is not a curiosity. The single most important statement in module 8 is that heat, which
is inexact, acquires an integrating factor $1/T$ — and that the resulting exact form is the
differential of entropy. You are not expected to anticipate that now. It is here so that when
it arrives, it arrives as a piece of mathematics you have already met.
:::

## Quick self-test

If you can do these without notes, this page has nothing further for you.

1. Give the SI units of $\kB$, and of $\kB T / m$.
2. For $f(x,y) = x/y$, write $(\partial f/\partial x)_y$, $(\partial f/\partial y)_x$ and
   $\mathrm{d}f$.
3. Is $x\,\mathrm{d}x + y\,\mathrm{d}y$ exact? If so, give its potential.
4. Is $x\,\mathrm{d}y - y\,\mathrm{d}x$ exact? Integrate it from $(1,0)$ to $(0,1)$ along the
   straight line, and then along the unit circle, and compare.
5. A formula gives an answer of $2.7 \times 10^{-21}\,\mathrm{J}$ where the expected value is
   $2.6 \times 10^{-21}\,\mathrm{J}$. Do they agree?
