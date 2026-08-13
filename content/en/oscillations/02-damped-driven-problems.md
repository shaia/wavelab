---
title: Problem set — damping, resonance, and the quality factor
short_title: 02 · Problems
---

# Problem set: damping, resonance, and the quality factor

Exam-style problems. Work them with a pen before touching a computer; the last two are meant
to be finished numerically. Solutions and marking rubrics live with the instructor material
and are deliberately not on this site.

Throughout, $\gamma \equiv b/m$, so amplitudes decay as $e^{-\gamma t/2}$ and
$Q = \wnat/\gamma$. If you are checking against a textbook that defines $\gamma = b/2m$, say
so in your working and convert once, at the start.

## Problem 1 — classifying a decay

<!-- objectives: OBJ-02-1, OBJ-02-4 -->

A cart of mass $0.50\ \mathrm{kg}$ on a spring of stiffness $8.0\ \mathrm{N\,m^{-1}}$ is
released from $x_0 = 0.10\ \mathrm{m}$ at rest. The damping coefficient is
$b = 0.20\ \mathrm{kg\,s^{-1}}$.

(a) Compute $\wnat$, $\gamma$, $\omega_d$ and $Q$. Which regime is this, and by what margin?

(b) By what factor has the amplitude fallen after ten full oscillations? After how many
oscillations has the *energy* fallen to $1\%$ of its initial value?

(c) What value of $b$ would make this system critically damped? Show that at that value the
solution $(C + Dt)e^{-\wnat t}$ is what the underdamped form becomes as $\omega_d \to 0$,
rather than a separate case bolted on.

(d) An overdamped oscillator crosses $x = 0$ at most once. Prove it from the general
overdamped solution $c_+e^{r_+t} + c_-e^{r_-t}$ with $r_\pm$ both real and negative.

## Problem 2 — the peak that is not where you expect

<!-- objectives: OBJ-02-2, OBJ-02-3 -->

(a) Starting from $m\ddot{x} + b\dot{x} + kx = F_0\cos\omega t$, substitute
$x = \Real\!\left[X e^{-\ii\omega t}\right]$ and derive
$X = (F_0/m)/(\wnat^2 - \omega^2 - \ii\gamma\omega)$ in three lines. State exactly where the
assumption "the transient has died" entered.

(b) Maximise $|X|$ and obtain $\omega_{\text{peak}} = \wnat\sqrt{1 - 1/(2Q^2)}$. Show that a
real maximum exists only for $Q > 1/\sqrt{2}$, and say in words what the response curve looks
like below that threshold.

(c) Show that $|X(\wnat)| = Q\,F_0/k$ exactly — no approximation — and that the phase lag
there is exactly $\pi/2$ whatever the damping.

(d) A structural engineer reports "the resonant frequency of this footbridge is
$1.85\ \mathrm{Hz}$" from a swept-force test, and separately measures $Q = 25$ from a
ringdown. By how much does the bridge's $\wnat$ differ from the reported figure? Was the
engineer wrong to conflate them?

## Problem 3 — energy bookkeeping at resonance

<!-- objectives: OBJ-02-4, OBJ-02-6 -->

(a) Show that the energy of a lightly damped free oscillator decays as $e^{-\gamma t}$, and
hence that $Q = 2\pi E / |\Delta E|_{\text{per cycle}}$ reduces to $\wnat/\gamma$. Where in
that derivation did you need $Q \gg 1$?

(b) For the driven steady state, compute the cycle average of the power delivered by the
drive, $\langle F\dot{x}\rangle$, and show it equals $\langle b\dot{x}^2\rangle$. Confirm the
result is $\tfrac12\gamma m\omega^2|X|^2$.

(c) Show that this power peaks at exactly $\wnat$ for any damping, and explain the physical
difference between that statement and the result of Problem 2(b). Which of the two would a
microphone measuring loudness report?

(d) Near resonance, reduce $\langle P\rangle$ to a Lorentzian and identify its full width at
half maximum. A quartz crystal at $32\,768\ \mathrm{Hz}$ has $Q = 10^5$: what is its
half-power bandwidth in hertz, and how long does it ring after a kick?

## Problem 4 — the RLC translation

<!-- objectives: OBJ-02-1, OBJ-02-6 -->

A series circuit has $L = 10\ \mathrm{mH}$, $C = 100\ \mathrm{nF}$ and
$R = 20\ \Omega$, driven by $V(t) = V_0\cos\omega t$.

(a) Write the equation for the charge $q$ on the capacitor and identify the mechanical
analogue of each term. What plays the role of mass, of damping, of stiffness?

(b) Compute the resonant frequency in hertz, $Q$, and the half-power bandwidth. Is this
circuit good enough to separate two AM stations $10\ \mathrm{kHz}$ apart at
$1\ \mathrm{MHz}$?

(c) You need to double $Q$ without changing the resonant frequency. Give two different ways,
and state a practical cost of each.

(d) The current, not the charge, is what a receiver measures. At which frequency is the
*current* amplitude largest, and why is that not the same question as (b)?

## Problem 5 — resonance on trial, numerically

<!-- objectives: OBJ-02-3, OBJ-02-5 -->

Using `wavelab.oscillators` (in the browser laboratory or locally):

(a) Compute amplitude-response curves with `steady_state_response` at $Q = 0.6$, $1.0$,
$3.0$ and $20$. Locate each maximum numerically and plot $\omega_{\text{peak}}/\wnat$
against $1/Q^2$ alongside the predicted line. At which of your four values does the peak
disappear, and does the numerical maximum warn you or fail quietly?

(b) Integrate from rest at exact resonance with `simulate` at $Q = 10$. Extract the amplitude
envelope and compare it with $Q(F_0/k)\left(1 - e^{-\gamma t/2}\right)$. How many periods
pass before the amplitude is within $5\%$ of its final value, and how does that compare with
$Q/\pi$?

(c) Repeat (b) at $Q = 40$. Confirm that the steady-state amplitude is four times larger and
that reaching it takes four times as long. Write two sentences on what this trade-off means
for a radio receiver, a musical instrument, and a shock absorber.

## Problem 6 — challenge: designing a shock absorber

<!-- objectives: OBJ-02-1, OBJ-02-5 -->

A car body of $400\ \mathrm{kg}$ per wheel sits on a spring chosen so that the suspension's
undamped natural frequency is $1.2\ \mathrm{Hz}$. Hitting a kerb displaces it by
$8\ \mathrm{cm}$; the ride is judged acceptable once the displacement stays within
$1\ \mathrm{mm}$.

(a) Compute the settling time to $1\ \mathrm{mm}$ as a function of $b$, for $b$ from well
under to well over critical, and find the value that minimises it.

(b) You will find the optimum lies slightly *below* critical damping, not at it. Explain why
— what does a small amount of overshoot buy?

(c) Real suspensions are tuned nearer $Q \approx 1$ than to the settling-time optimum. Name
one thing the model above ignores that could account for the difference, and say which
specification bullet on the module page licenses that ignorance.
