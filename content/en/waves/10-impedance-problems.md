---
title: "Problem set — impedance"
short_title: 10 · Problems
---

# Problem set: impedance

Exam-style problems. Work them with a pen before touching a computer; problems 6 and 7 are meant
to be finished numerically. Solutions and marking rubrics live with the instructor material and
are deliberately not on this site.

Throughout, two ideal strings of densities $\mu_1$ and $\mu_2$ are joined at $x = 0$ under one
common tension $T$, so that

$$
v = \sqrt{\frac{T}{\mu}},
\qquad
Z = \sqrt{T\mu} = \mu v = \frac{T}{v},
\qquad
r = \frac{Z_1 - Z_2}{Z_1 + Z_2},
\qquad
t = \frac{2Z_1}{Z_1 + Z_2} .
$$

## Problem 1 — the junction conditions, and what each one is

<!-- objectives: OBJ-10-1, OBJ-10-2 -->

(a) A semi-infinite string is driven at one end so that only a right-moving wave exists on it.
Starting from $y_t = -v\,y_x$, show that the transverse force the driver must supply is
$F = Z\,y_t$ with $Z = \sqrt{T\mu}$, and state the SI unit of $Z$ in base units.

(b) Explain, in one sentence each, why the driver's force is in phase with its *velocity* rather
than with its displacement, and what that implies about the work it does over a cycle.

(c) Write the incident, reflected and transmitted waves at a junction in the course convention
$\psi = \Real[A e^{\ii(kx - \omega t)}]$, state which quantity is the same on both sides and
which adjusts, and say what physical fact forces that choice.

(d) State the two junction conditions, name the physical assumption behind each, and derive $r$
and $t$. Verify that your answers satisfy $1 + r = t$, and say which of the two conditions that
identity *is*.

(e) A student writes the force condition as "$y_x$ is continuous" instead of "$T y_x$ is
continuous". On this pair of strings, does it matter? Construct a physical situation where it
would.

## Problem 2 — the two ends, as limits and as images

<!-- objectives: OBJ-10-3 -->

(a) Take $Z_2 \to \infty$ and $Z_2 \to 0$ in the formulas for $r$ and $t$, and state the four
limiting values. For each end, say what the displacement and the slope do at the boundary.

(b) The method of images treats a fixed end at $x = L$ by placing a mirror pulse of opposite
sign at the reflected position beyond it. Write $y(x,t)$ for a Gaussian pulse
$f(x) = A\exp[-(x-x_0)^2/w^2]$ approaching a fixed end, as a sum of two travelling terms, and
show that your expression gives $y(L, t) = 0$ for all $t$.

(c) Repeat (b) for a free end, and show that your expression gives $y_x(L,t) = 0$ for all $t$
and that the end's displacement momentarily reaches $2A$.

(d) A pulse 12 cm wide (at $1/e$) approaches a free end on a string with $v = 20$ m/s. Sketch
$y(x)$ at the instants the pulse's centre is 20 cm from the end, at the end, and 20 cm past it.
Mark the amplitude at the end in each sketch.

(e) Energy is conserved at both ends, yet one of them exerts a force on the string and the other
does not. Resolve the apparent conflict, using the fact that power is force times velocity.

## Problem 3 — numbers at a junction

<!-- objectives: OBJ-10-2, OBJ-10-4 -->

A string with $\mu_1 = 4.0$ g/m is joined to one with $\mu_2 = 36$ g/m. The tension is
$T = 25$ N throughout. A sinusoidal wave of amplitude 3.0 mm and frequency 60 Hz arrives from
the light side.

(a) Find $v_1$, $v_2$, $Z_1$, $Z_2$, and the wavelength on each side. State which quantity is
the same on both sides and why.

(b) Find $r$, $t$, and the amplitudes of the reflected and transmitted waves in millimetres.
State whether the reflected pulse is upright or inverted.

(c) Find $R$ and $T$ from your $r$ and $t$, and verify $R + T = 1$. Then compute the three mean
powers in milliwatts directly from $\tfrac12 Z\omega^2 A^2$ and check that the incident power
equals the sum of the other two.

(d) The wave now arrives from the *heavy* side instead, with the same amplitude and frequency.
Recompute $r$, $t$, $R$ and $T$. Which of the four changed, and which did not? Explain the
pattern in one sentence.

(e) At which junction — light-to-heavy or heavy-to-light — does the far side of the string move
*further* than the incident wave did? Reconcile that with your answer to (d).

## Problem 4 — the $t > 1$ paradox, settled

<!-- objectives: OBJ-10-4 -->

(a) Show that $t > 1$ for every junction with $Z_2 < Z_1$, that $t < 2$ always, and that $t = 2$
only in the free-end limit.

(b) For $Z_2/Z_1 = 1/10$, compute $r$, $t$, $R$ and $T$. State the transmitted amplitude as a
multiple of the incident one and the transmitted power as a fraction of the incident one.

(c) Prove $R + T = 1$ algebraically from the definitions, showing the step where
$(Z_1 - Z_2)^2 + 4Z_1Z_2$ collapses.

(d) Explain in words, to someone holding the two ropes, why a bigger swing can carry less power.
Your explanation must use the fact that power is $\tfrac12 Z(\omega A)^2$ and must not use the
word "impedance" more than once.

(e) Show that $R$ is unchanged when $Z_1$ and $Z_2$ are swapped, while $r$ changes sign and $t$
does not. Then state what a measurement of $R$ alone can and cannot tell you about a junction
you cannot see.

## Problem 5 — the gel, and other matched media

<!-- objectives: OBJ-10-1, OBJ-10-5 -->

Acoustic impedance for a fluid is $Z = \rho c$. Use $\rho c$ values of
$1.5\times10^{6}$ kg m$^{-2}$ s$^{-1}$ for soft tissue, $1.6\times10^{6}$ for ultrasound gel,
and $430$ for air.

(a) Compute $R$ for a tissue–air interface and for a tissue–gel interface. Express the first as
a percentage and comment on what the ultrasound image looks like without gel.

(b) The gel layer is a fraction of a millimetre thick and the wavelength in it is about 0.3 mm
at 5 MHz. Explain why the layer's *thickness* matters here and would not matter if the gel were
perfectly matched to both neighbours.

(c) A 50 Ω coaxial cable is left unterminated (an open circuit, $Z_2 \to \infty$) and a pulse is
sent down it. Predict what returns, with a sign, and say what a terminating 50 Ω resistor does
to that pulse and where the energy goes instead.

(d) Give one example each of impedance matching in acoustics, electronics and optics, and in one
sentence each say what would go wrong without it.

(e) A student proposes matching two given strings by increasing the tension in the lighter one.
Explain why this cannot work on a single stretched string, and identify the assumption in the
model that forbids it.

## Problem 6 — the junction that is not a point

<!-- objectives: OBJ-10-2, OBJ-10-5 -->

*A discovery problem: the answer is not stated anywhere above.* Use
`wavelab.waves.simulate_string` with an array `mu`.

(a) Replace the step in density by a ramp: $\mu$ rises from $\mu_1$ to $\mu_2 = 9\mu_1$ linearly
over a width $w$ centred on the junction. Fire a sinusoidal packet of wavelength $\lambda_1$ at
it and measure the reflected energy fraction $R$ by weighing the string behind the junction, as
the laboratory's part 6 does.

(b) Repeat for $w/\lambda_1$ from 0 to about 3 and plot $R$ against $w/\lambda_1$. Describe the
shape of the curve. What is $R$ as $w \to 0$, and does your run agree with the formula?

(c) At what ramp width has the echo fallen to a tenth of its value at the sharp step? Express
your answer in wavelengths and explain, physically, why the wavelength is the natural unit here
and the ramp width alone is not.

(d) Explain the result in terms of what the wave "sees": at what rate of change of $Z$ per
wavelength does a junction stop being a junction? This effect has a name — *adiabatic* matching
— and is why a horn works, why a tsunami grows instead of reflecting, and why optical fibres are
tapered rather than butted.

(e) State the limitation of your numerical experiment: what would happen at very large $w$ on a
grid of fixed length, and how you checked that your $R$ is the junction's and not the far end's.

## Problem 7 — the quarter-wave transformer

<!-- objectives: OBJ-10-4, OBJ-10-5 -->

*Challenge.* Media 1 and 3 are given, with $\mu_3 = 9\mu_1$. Insert a section of density
$\mu_2$ and length $\ell$ between them.

(a) Show that choosing $Z_2 = \sqrt{Z_1Z_3}$ makes the reflections from the two faces equal in
magnitude, and that choosing $\ell = \lambda_2/4$ — a quarter wavelength *in the section* — puts
them exactly out of phase on return. Give $\mu_2$ and $\ell$ in terms of $\mu_1$ and the
frequency.

(b) Compute $R$ for the bare 1→3 step, and predict $R$ for the matched pair at the design
frequency.

(c) Simulate both, as the module's third animation does, and report the two reflected energy
fractions. Explain any difference between your matched $R$ and the zero predicted in (b): what
is the residual made of, and does it shrink if you send a longer packet?

(d) Sweep the frequency and plot $R(\omega)$ for the matched structure over, say, half to twice
the design frequency. Mark the design frequency. Describe the shape of the curve near the
minimum and state its order in the detuning.

(e) Camera lenses look purple in reflection. Using your curve, explain why — and say what
"broadband anti-reflection coating" must therefore mean in terms of the number of layers.

## Problem 8 — a rope, a knot and a phone

<!-- objectives: OBJ-10-2, OBJ-10-3 -->

Knot a length of thick rope to a thin one — a skipping rope and a shoelace will do — lay the pair
on a smooth floor, and have someone hold the far end. Film pulses crossing the knot with a phone
at 60 frames per second or better, with a ruler or metre stick lying in frame and the camera
fixed.

(a) Send a pulse from the thick side and then from the thin side. Classify each reflection as
upright or inverted. Explain why this result needs no calibration whatsoever — not of length,
time, or amplitude — and what exactly it falsifies.

(b) Weigh both ropes and measure their lengths to get $\mu_1$ and $\mu_2$. Predict $r$ and $t$
for each direction, and state your predicted amplitudes to two figures.

(c) From the video, measure the incident, reflected and transmitted amplitudes in ruler units.
Estimate the uncertainty in each from the pixel scale and from how much your reading changes
between neighbouring frames. Compare with (b), with error bars.

(d) You will find the measured $|r|$ comes out high if you read each amplitude as the largest
excursion you can see. Explain why, referring to the laboratory's part 7, and propose a reading
method that does not have that bias.

(e) Measure the pulse's width on each side of the knot, in centimetres. Show that the ratio
should be $v_2/v_1 = \sqrt{\mu_1/\mu_2}$, compare with your measurement, and say what this tells
you that the amplitude ratio does not.

(f) State one systematic error this apparatus has that the simulation does not, and estimate its
size: friction with the floor, a knot with real mass, or a tension that differs between the two
ropes because someone is holding the end.
