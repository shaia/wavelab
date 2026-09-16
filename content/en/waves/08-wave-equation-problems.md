---
title: "Problem set — the wave equation"
short_title: 08 · Problems
---

# Problem set: the wave equation

Exam-style problems. Work them with a pen before touching a computer; problems 6 and 7 are
meant to be finished numerically. Solutions and marking rubrics live with the instructor
material and are deliberately not on this site.

Throughout, a string has tension $T$ and linear mass density $\mu$, so that

$$
\frac{\partial^2 y}{\partial t^2} = v^2\,\frac{\partial^2 y}{\partial x^2},
\qquad
v = \sqrt{\frac{T}{\mu}},
\qquad
S = \frac{v\,\Delta t}{\Delta x} .
$$

## Problem 1 — which way, and how fast

<!-- objectives: OBJ-08-2 -->

(a) Show by the chain rule that $y = f(x - vt)$ satisfies the wave equation for any
twice-differentiable $f$. Then show that $y = f(x - ut)$ with $u \ne v$ does not, unless $f$ is
a straight line.

(b) A pulse is described by $y(x,t) = h\,\exp\!\left[-(3x + 12t)^2\right]$, with $x$ in metres and
$t$ in seconds. Find its direction of travel and its speed, and the positions of its peak at
$t = 0$ and $t = 0.5$ s.

(c) A sinusoidal wave on a string is $y = \Real\!\left[A\,e^{\ii(kx - \omega t)}\right]$ with
$k = 4.0$ rad/m and $\omega = 60$ rad/s. Find its speed, wavelength and frequency in hertz, and
say which way it travels. What would you change to make the same wave travel the other way?

(d) Explain why $y = \sin(kx)\cos(\omega t)$ with $\omega = vk$ solves the wave equation even
though it does not travel at all. Write it as $f(x - vt) + g(x + vt)$.

## Problem 2 — the piece of string, carefully

<!-- objectives: OBJ-08-1 -->

(a) Draw a short piece of string between $x$ and $x + \mathrm{d}x$, tilted at angles
$\theta(x)$ and $\theta(x + \mathrm{d}x)$, with the tension at each end. Write the horizontal and
vertical components of the net force exactly, with no approximation.

(b) The string moves only transversely. Use the horizontal equation to show that
$T\cos\theta$ is the same everywhere, and deduce how much $T$ itself can vary along a string
whose slope never exceeds $0.05$.

(c) Using $\sin\theta = y_x/\sqrt{1 + y_x^2}$ and the true length of the piece, write the
vertical equation of motion without approximation. Show that it reduces to
$\mu\,y_{tt} = T\,y_{xx}$ when $|y_x| \ll 1$, and identify the three places the approximation
was used.

(d) A guitar string 650 mm long is plucked 3 mm out of line at its midpoint. Estimate the
largest slope, and the size of the largest correction you neglected in (c), as a fraction.

## Problem 3 — a rectangular strike

<!-- objectives: OBJ-08-3 -->

A long string at rest and straight is struck so that, at $t = 0$, the stretch
$-\ell < x < \ell$ has velocity $w$ and the rest is still.

(a) Write down an antiderivative $W(x)$ of the starting velocity, and use d'Alembert's solution
to write $y(x,t)$ in terms of $W$.

(b) Sketch the string at $t = \ell/(2v)$, $t = \ell/v$ and $t = 3\ell/v$. Label the height of the
plateau and the positions of its corners in each sketch.

(c) Show that the height at $x = 0$ grows at rate $w$ until $t = \ell/v$ and is $w\ell/v$
afterwards, for ever. Explain physically why the string does not come back down.

(d) The string's centre of mass moves. Find its velocity, and show that it equals the total
momentum the strike delivered divided by the mass of the whole string — or explain why that
statement needs care on an infinitely long string.

## Problem 4 — what the speed can depend on

<!-- objectives: OBJ-08-2, OBJ-08-4 -->

(a) Suppose the speed of a pulse could depend on $T$, $\mu$, the pulse height $h$ and the pulse
width $\sigma$. Use dimensional analysis to show that
$v = \sqrt{T/\mu}\;\Phi(h/\sigma)$ for some function $\Phi$ of the dimensionless ratio.

(b) Dimensional analysis has not ruled out a dependence on height. Use the linearity of the
wave equation to show that $\Phi$ must be a constant. Say, in one sentence, which step of the
derivation made the equation linear, and so what a steep enough pulse is free to do.

(c) Show that $\sqrt{T/\mu}$ has units of velocity, starting from newtons and kilograms per
metre.

(d) A student measures pulse speeds of 12.0, 16.9 and 24.1 m/s at tensions of 2.0, 4.0 and
8.0 N on one rope. Fit the exponent of $v$ against $T$ and find $\mu$. State whether the data
support $v \propto \sqrt{T}$.

## Problem 5 — measure it with a slinky

<!-- objectives: OBJ-08-4, OBJ-08-6 -->

A slinky is stretched along a smooth floor and a sideways pulse is sent along it. A phone films
it at 240 frames per second. The pulse's peak passes a tape mark at frame 112 and a second mark
3.00 m further on at frame 181.

(a) Find the pulse speed. Assuming each frame number is uncertain by $\pm 1$, independently,
give the speed with its uncertainty.

(b) Reading frames by eye times the peak. Using this module's photogate check, explain why
timing the whole pulse — for example, the frame at which a coil has risen halfway on the way up
and the frame at which it is halfway on the way down, averaged — should do better.

(c) A slinky is a spring: stretched from its natural length $L_0$ to $L$, its tension is
$T = k(L - L_0)$, while its mass $M$ spreads over the new length. Show that the time for a pulse
to cross it is $\sqrt{ML/\left(k(L - L_0)\right)}$, and that for $L \gg L_0$ this barely depends
on how far it is stretched. Predict what happens to the crossing time when you stretch the slinky
from 4 m to 8 m, and design a two-measurement test of the prediction.

(d) Tape a small flag to one coil. Describe what the video will show the flag doing as the
pulse passes, and what it must not show if the model is right.

## Problem 6 — grid dispersion, measured

<!-- objectives: OBJ-08-5 -->

Using `waves.simulate_string` and `measurement.pulse_arrival_time`:

(a) On a 2 m string with 800 cells at $S = 0.5$, launch Gaussian plucks of widths
$\sigma = 5\,\Delta x$, $10\,\Delta x$ and $20\,\Delta x$, and measure the speed between two
detectors 0.4 m apart by timing the *peak* of each record. Fit the exponent of the relative
speed error against $\sigma$.

(b) Compare your errors with $(1 - S^2)(\Delta x/\sigma)^2/4$. Report the largest discrepancy.

(c) Repeat with centroid timing and report the errors. Explain, using the leapfrog dispersion
relation $\sin(\omega\Delta t/2) = S\sin(k\Delta x/2)$, why the centroid is not affected.

(d) Plot the narrowest pulse after it has travelled 1 m. Describe the ripples you see, say which
side of the pulse they are on, and explain why that side. Then repeat at $S = 1$ and explain what
changed.

## Problem 7 — the magic step

<!-- objectives: OBJ-08-5 -->

(a) Show that at $S = 1$ the leapfrog update becomes
$y_i^{n+1} = y_{i+1}^n + y_{i-1}^n - y_i^{n-1}$.

(b) Show that $y_i^n = F(i - n) + G(i + n)$ satisfies that update for *any* sequences $F$ and $G$.
This is d'Alembert's theorem on a grid.

(c) Integrate a Gaussian pluck at $S = 1$ for 400 steps on a string long enough that it never
reaches the ends, and compare with `waves.dalembert_solution`. Repeat at $S = 0.99$. Report both
errors and their ratio.

(d) Start instead a pulse that moves right, with $y_t = -v\,y_x$. Show that the error at $S = 1$
is no longer at rounding level, and trace the reason to the second time level, which the solver
builds as $y^1 = y^0 + \Delta t\,v^0 + \tfrac12\Delta t^2 a^0$. How does the error scale with
$\Delta x$?

## Problem 8 — challenge: a pluck near a wall, by images

<!-- objectives: OBJ-08-3, OBJ-08-6 -->

A string occupies $x \ge 0$ with a fixed end at $x = 0$. It is plucked into a triangle of height
$h$ and half-width $\ell$ centred at $x = 3\ell$, and released from rest.

(a) Extend the starting shape to $x < 0$ as an odd function and show that d'Alembert's solution
on the whole line then satisfies $y(0, t) = 0$ for all $t$.

(b) Sketch the string on $x \ge 0$ at $t = \ell/v$, $2\ell/v$, $3\ell/v$, $4\ell/v$ and $5\ell/v$.
At which of these times is the left-moving half *at* the wall, and what does the string look
like there?

(c) At $t = 3\ell/v$ part of the string near the wall is momentarily straight. Is it at rest?
Use $y_t = -v\,y_x$ for each travelling piece to find its velocity, and say where the energy of
that half of the pluck is at that instant.

(d) Check your sketches against `waves.simulate_string` with a fixed end, and report the height
and sign of the pulse that comes back from the wall.

(e) Repeat (a) and (b) with an even extension, and state the boundary condition it satisfies at
$x = 0$ and the kind of end it describes. Which of your two answers describes a rope tied to a
ring that slides freely on a vertical pole?
