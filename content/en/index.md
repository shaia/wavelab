# WaveLab: Explore, Derive and Simulate Waves and Optics

An interactive computational textbook and virtual laboratory for university-level waves,
oscillations and optics — built to take you from zero to exam-ready, at the depth of a good
book, with everything a computer adds: live simulations, laboratories, quizzes, exams and
demonstration videos.

Everything in this course revolves around one idea:

> **A vibrating string, a resonant cavity, a diffraction pattern and a quantum wavefunction
> are one mathematical structure wearing four costumes. Learn to think in waves once, and
> you have learned them all.**

## How to study here

Every module follows the same climb:

1. **Opening** — a physical puzzle you can feel, and a prediction you commit to *before* any equation.
2. **Core** — an interactive laboratory, the precise derivation, and a computational check. This is the exam-relevant spine.
3. **Consolidation** — transfer to new contexts, worked examples, quizzes and exam-style problems.
4. **Advanced** — clearly marked deeper material. Skip it freely on a first pass; nothing later depends on it.

:::{note} Conventions used everywhere
A plane wave is always $\Real[A\,e^{\ii(kx - \omega t)}]$ — the time factor is
$e^{-\ii\omega t}$ and phasors rotate clockwise. Forward Fourier transforms carry the minus
sign, matching `numpy.fft`, and an absorbing medium has index $n + \ii\kappa$. Units are SI.
The full list is on the [conventions](conventions.md) page.
:::

## The course map

The full course runs from oscillations through waves to optics and photonics: mathematical
foundations, oscillations, coupled oscillators and normal modes, the wave equation, Fourier
methods and dispersion, electromagnetic waves, interfaces, polarization, interference,
diffraction, geometrical optics, Fourier optics, and Gaussian beams, lasers and waveguides.

Currently available:

- **[Phasors: the language of waves](foundations/00-phasors.md)** — why adding two sounds can
  produce silence, and the one complex-number idea the whole course runs on. Start here.
- **[The simple harmonic oscillator](oscillations/01-sho.md)** — the single curve that clocks,
  molecules and circuits all follow, and why its period ignores its amplitude.

One reference page sits outside the sequence and is meant to be returned to:
[conventions](conventions.md).
