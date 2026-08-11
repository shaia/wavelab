---
title: Conventions used everywhere
short_title: Conventions
---

# Conventions used everywhere

Wave physics has more arbitrary choices in it than most subjects: which way a phase rotates,
where the $2\pi$ lives in a Fourier transform, which sign of the imaginary part of a
refractive index means absorption. None of them changes the physics, and all of them change
the formulas. Textbooks differ, and a student comparing two sources silently switching
between conventions can lose a week to a stray minus sign.

So this course fixes its choices once, here, and never varies them. This page is the place to
come back to when a formula elsewhere does not match one of ours.

(conventions-phase)=
## The phase of a wave

Every complex representation of an oscillation or a wave requires one arbitrary decision:
which sign of the exponent represents motion forward in time. Both choices appear in the
literature:

| | This course | The other common choice |
|---|---|---|
| Plane wave | $\psi(x,t) = \Real\!\left[A\,e^{\ii(kx - \omega t)}\right]$ | $\psi = \Real\!\left[A\,e^{j(\omega t - kx)}\right]$ |
| Time factor | $e^{-\ii\omega t}$ | $e^{+j\omega t}$ |
| Found in | physics: Hecht, Griffiths, Goodman, Georgi | engineering: circuits, signal processing |
| Phasors rotate | clockwise | counterclockwise |
| Converting | $\ii \leftrightarrow -j$ | $j \leftrightarrow -\ii$ |

**This course always uses the first column.** The time factor is $e^{-\ii\omega t}$, a wave
with $k > 0$ travels toward $+x$, and phasors rotate clockwise. It is the convention of all
four of this course's backbone texts, and it is the one under which the quantum-mechanical
phase $e^{-\ii E t/\hbar}$ will later look familiar rather than backwards.

:::{admonition} A worked example, so the sign is concrete
:class: definition
The oscillation $x(t) = A\cos(\omega t + \varphi)$ has the phasor $\hat{x} = A e^{-\ii\varphi}$,
because

$$
\Real\!\left[\hat{x}\, e^{-\ii\omega t}\right]
= \Real\!\left[A e^{-\ii(\omega t + \varphi)}\right]
= A\cos(\omega t + \varphi).
$$

One consequence you will meet in the oscillations modules: the steady-state response of a
driven, damped oscillator is

$$
\hat{x}(\omega) = \frac{F_0/m}{\wnat^2 - \omega^2 - \ii\gamma\omega},
$$

whose argument at $\omega = \wnat$ is $+\pi/2$ — the displacement *lags* the drive by a
quarter cycle at resonance. Under the other convention the same physics carries the opposite
sign of the imaginary part. Check every result you derive against this one and you will never
lose the sign.
:::

The engineering convention appears symbolically on this page and nowhere else in the course.
Everywhere else — including problem sets, quizzes and the laboratories — the first column is
the only one in use. A project lint enforces this.

(conventions-fourier)=
## Fourier transforms

The transform pair carries two arbitrary choices: which direction gets the minus sign, and
where the $2\pi$ goes. This course puts the minus sign in the *forward* transform and the
$2\pi$ in the *inverse*:

$$
F(\omega) = \int_{-\infty}^{\infty} f(t)\, e^{-\ii\omega t}\, \mathrm{d}t,
\qquad
f(t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} F(\omega)\, e^{+\ii\omega t}\, \mathrm{d}\omega,
$$

and identically in space:

$$
A(k) = \int_{-\infty}^{\infty} \psi(x)\, e^{-\ii k x}\, \mathrm{d}x,
\qquad
\psi(x) = \frac{1}{2\pi} \int_{-\infty}^{\infty} A(k)\, e^{+\ii k x}\, \mathrm{d}k.
$$

Three things make this the right set of choices for this course, rather than merely a set:

- **It is internally consistent with the phase convention.** Assembling a wave packet from
  its spectrum gives $\psi(x,t) = \frac{1}{2\pi}\int A(k)\, e^{\ii(kx - \omega(k) t)}\,
  \mathrm{d}k$ — every component is a forward-travelling plane wave of the previous section,
  with no sign juggling.
- **It is what the code does.** `numpy.fft.fft` puts the minus sign in the forward transform,
  so a formula on a page and the line of NumPy that checks it never disagree about signs.
- **The asymmetric $2\pi$ keeps $F(0) = \int f$.** The value of the transform at zero
  frequency is the plain area under the signal, with no stray prefactor.

Note that an inverse transform legitimately displays a $e^{+\ii\omega t}$ — the lint that
polices the time factor knows about this page, and an inverse-transform display elsewhere
carries an explicit exception marker.

(conventions-index)=
## The complex refractive index

In an absorbing medium the refractive index becomes complex. This course writes it

$$
\tilde{n} = n + \ii\kappa, \qquad \kappa \ge 0 ,
$$

and the sign is *forced* by the phase convention, not free: a wave travelling toward $+x$
through the medium is

$$
e^{\ii \tilde{n} k_0 x} = e^{\ii n k_0 x}\, e^{-\kappa k_0 x},
$$

which decays, as absorption must. Under the engineering time factor the same physics requires
$\tilde{n} = n - j\kappa$; if you meet that spelling in another book, it is the same medium
described in the other convention, not a disagreement about the physics.

(conventions-real)=
## Real fields and intensity

The physical signal is always the real part. Complex exponentials are bookkeeping for
amplitude and phase; nothing measurable is complex. Two consequences, fixed here once:

- Nonlinear operations — energy, intensity, anything squared — act on the **real** signal,
  never on the complex representation. Take the real part first.
- The time average of $\cos^2$ over a cycle is $\tfrac{1}{2}$. The time-averaged intensity of
  a light wave of real amplitude $E_0$ in a medium of index $n$ is therefore

  $$
  I = \tfrac{1}{2}\, c\, \epsilon_0\, n\, E_0^2 ,
  $$

  and that factor of $\tfrac{1}{2}$ is stated here and never re-derived.

(conventions-units)=
## Units and constants

- **SI throughout.** Metres, kilograms, seconds, and their combinations. Where a problem
  quotes electron-volts or ångströms, convert before computing.
- **Wavelengths are vacuum wavelengths.** $\lambda_0$ quoted in nanometres; inside a medium
  the wavelength is $\lambda_0/n$ and the *frequency* is what stays fixed.
- **$c$ is exact.** $c = 299\,792\,458\ \mathrm{m\,s^{-1}}$ by definition of the metre, and
  $\epsilon_0 = 1/(\mu_0 c^2)$.
- **Angular frequency $\omega$ and frequency $\nu$ both appear.** $\omega = 2\pi\nu$ always;
  formulas carry $\omega$ unless a measurement is being quoted in hertz.
- **The library works in plain SI floats.** `wavelab` deliberately does not wrap quantities
  in a units package, so that a student can read `omega0 = np.sqrt(stiffness / mass)` and
  recognise it. Dimensional correctness is enforced in the test suite instead, where every
  formula is re-evaluated with `pint` quantities.

(conventions-epistemic)=
## Epistemic labels: what kind of claim is this?

Wave physics mixes exact mathematics, empirical laws, modelling choices and numerical
evidence, often within one paragraph. Blurring them is how students end up believing that a
simulation "proved" an identity. Every boxed claim in this course therefore carries a label
saying what kind of statement it is, and the boxes below are one live example of each.

:::{admonition} Definition
:class: definition
A **definition** introduces a name for something. It cannot be true or false, only useful or
useless: *the quality factor of an oscillator is $Q = \sqrt{mk}/b$*.
:::

:::{admonition} Empirical law
:class: empirical-law
An **empirical law** summarises measurement. It could have come out otherwise, and it holds
within the range where it has been tested: *the period of a pendulum clock is independent of
the amplitude of its swing, for small swings*.
:::

:::{admonition} Theorem
:class: theorem
A **theorem** follows by mathematics from stated premises. If you accept the premises you must
accept the conclusion: *two superposed harmonic oscillations of the same frequency form a
single harmonic oscillation of that frequency, whatever their amplitudes and phases*.
:::

:::{admonition} Model assumption
:class: model-assumption
A **model assumption** is a deliberate simplification, adopted because it makes a calculation
possible: *the spring in this simulation is massless, perfectly linear, and never heats up*.
:::

:::{admonition} Approximation
:class: approximation
An **approximation** is a controlled error with a regime of validity attached: *$\sin\theta
\approx \theta$, whose relative error is below $1\%$ for $\theta < 0.24\ \mathrm{rad}$*.
:::

:::{admonition} Numerical observation
:class: numerical-observation
A **numerical observation** is something a computation showed. It is evidence, not proof, and
it is only as good as the model behind it: *the fitted convergence order was $2.01 \pm 0.05$*.
:::

:::{admonition} Open question
:class: open-question
An **open question** flags a genuine unresolved issue, or a place where the course is being
deliberately silent: *what, if anything, is "waving" in the quantum wavefunction that these
mathematical structures will eventually describe is not settled here, or anywhere*.
:::

(conventions-modelspec)=
## Model specifications

Every simulation in the course — on a page or in a notebook — carries a seven-field block
saying exactly what is being modelled. The fields never change and never reorder, so you can
scan them. This is the one from the simple-harmonic-oscillator module:

:::{admonition} Model specification
:class: model-spec
- **System:** a point mass $m$ on a massless linear spring of stiffness $k$, moving in one dimension; the observables are position, velocity and the energies.
- **Dynamics:** Newton's second law with the Hooke restoring force, $m\ddot{x} = -kx$, integrated numerically by a velocity-Verlet scheme with a fixed time step.
- **Boundary:** none — the mass moves on an infinite line and nothing is exchanged with anything.
- **Ensemble:** a single deterministic trajectory per choice of $(x_0, v_0)$; where measurement noise is added it is Gaussian, independent, and seeded.
- **Ignored:** spring mass, nonlinearity at large extension, internal damping, and the three-dimensional world the real spring hangs in.
- **Valid when:** displacements stay in the linear regime of the real spring and the time step is well below the oscillation period.
- **Failure modes:** amplitudes large enough to feel the spring's nonlinearity, time steps near or above the stability limit, and any question about where the oscillation's energy ultimately goes.
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

When a page says "the fitted resonance frequency is $0.994\,\wnat$", that is a numerical
observation about a model. When it says "the amplitude of a driven oscillator peaks below its
natural frequency whenever there is damping", that is a theorem. The first is evidence for
having implemented the second correctly. It is not why the second is true.
