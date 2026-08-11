# Waves, Oscillations & Optics
## Master Plan for an Interactive University-Level Physics Course

**Format:** Jupyter Notebook–centered interactive course  
**Level:** Strong undergraduate physics, with optional early graduate extensions  
**Primary optics backbone:** Eugene Hecht, *Optics*  
**Primary waves backbone:** MIT 8.03 / Howard Georgi / A. P. French / Cambridge Oscillations, Waves & Optics  
**Advanced optics companion:** Joseph W. Goodman, *Introduction to Fourier Optics*  
**Modern photonics extensions:** Saleh & Teich, Siegman, and selected advanced sources

> **Math rendering:** This document uses standard Jupyter/MathJax syntax: inline mathematics is written as `$...$` and display mathematics as `$$...$$`. It should render correctly in Jupyter Notebook/JupyterLab and Markdown viewers with MathJax-compatible equation support.

---

# 1. Vision

The goal is to build an interactive environment for teaching university-level **wave physics and optics** that is:

- scientifically accurate,
- mathematically rigorous,
- computationally literate,
- experimentally motivated,
- visually intuitive,
- engaging enough to encourage exploration,
- modular enough to serve both a standard undergraduate course and an advanced track.

The course should not be an electronic textbook with long blocks of prose followed by Python code.

Instead, the notebooks should function as a combination of:

- textbook,
- derivation notebook,
- simulation environment,
- virtual laboratory,
- computational physics workspace,
- problem set,
- experimental data-analysis environment.

The central pedagogical principle is:

$$
\boxed{
\text{Observe}
\rightarrow
\text{Predict}
\rightarrow
\text{Model}
\rightarrow
\text{Derive}
\rightarrow
\text{Simulate}
\rightarrow
\text{Measure}
\rightarrow
\text{Explain}
}
$$

The student should repeatedly move between physical intuition, analytical reasoning, numerical experimentation, and scientific interpretation.

---

# 2. Why Waves and Optics Belong in One Course

A strong modern course should not teach waves and optics as disconnected subjects.

The most useful conceptual progression is:

$$
\boxed{
\text{harmonic oscillator}
\rightarrow
\text{coupled oscillators}
\rightarrow
\text{normal modes}
\rightarrow
\text{continuous media}
\rightarrow
\text{wave equation}
\rightarrow
\text{Fourier analysis}
\rightarrow
\text{electromagnetic waves}
\rightarrow
\text{interference}
\rightarrow
\text{diffraction}
\rightarrow
\text{imaging}
}
$$

This sequence exposes a deep unity:

- a vibrating string,
- a coupled mass system,
- a resonant optical cavity,
- a diffraction pattern,
- a Gaussian beam,
- an optical image,
- a waveguide mode,
- and eventually a quantum wavefunction

all use closely related mathematical structures.

This course should therefore serve as a conceptual bridge between:

- classical mechanics,
- electromagnetism,
- optics,
- signal analysis,
- quantum mechanics,
- photonics.

---

# 3. Curriculum Philosophy Based on Leading Physics Programs

The proposed structure follows the common intellectual pattern seen in leading physics departments.

## 3.1 MIT

MIT's **8.03 Physics III: Vibrations and Waves** develops:

- simple harmonic motion,
- damping,
- forced oscillation,
- resonance,
- coupled oscillators,
- normal modes,
- traveling waves,
- sound,
- electromagnetic waves,
- polarization,
- reflection and refraction,
- interference,
- diffraction,
- Fourier methods,
- phase and group velocity.

This is an excellent model for the **waves half** of the course.

Reference:

https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/

---

## 3.2 University of Cambridge

Cambridge's **Oscillations, Waves & Optics** curriculum strongly emphasizes:

- linear oscillators,
- forced response,
- impedance,
- coupled systems,
- wave propagation,
- dispersion,
- group velocity,
- Fourier analysis,
- interference,
- diffraction,
- gratings,
- thin films,
- Michelson interferometry,
- Fabry–Pérot systems.

Particularly important for this course is Cambridge's use of **Fourier methods as a central organizing principle**, rather than introducing Fourier analysis only as a mathematical afterthought.

Reference:

https://www-teach.phy.cam.ac.uk/students/courses/oscillations%2C-waves-%26-optics/85

---

## 3.3 Caltech

Caltech's optics courses extend the standard curriculum toward:

- ray-transfer matrices,
- wave optics,
- coherence,
- diffraction,
- imaging,
- resonators,
- Gaussian beams,
- optical cavities,
- waveguides,
- fibers,
- laser optics.

Caltech provides an excellent model for the **advanced optics extension**.

Reference:

https://catalog.caltech.edu/current/2025-26/department/Ph/

---

## 3.4 University of California, Berkeley

Berkeley integrates:

- electromagnetism,
- wave propagation,
- scattering,
- interference,
- diffraction,
- geometrical optics,
- Fourier optics,
- computational physics,
- advanced quantum and nonlinear optics.

This supports a course architecture in which computational physics and mathematical methods appear before or alongside advanced optics.

Reference:

https://physics.berkeley.edu/bpie-program-course-options

---

## 3.5 Stanford

Stanford courses combine:

- geometrical optics,
- wave optics,
- physical demonstrations,
- group problem solving,
- laboratory work.

This reinforces the idea that the course should not be purely analytical.

---

## 3.6 Oxford

Oxford introduces waves, differential equations, and elementary optics early and integrates optics with later electromagnetism and laboratory physics.

This supports treating optics as part of a broader physics sequence rather than as an isolated subject.

---

# 4. Recommended Reference Hierarchy

Rather than adopting a single textbook, the course should use a **hierarchy of references**.

$$
\boxed{
\begin{array}{c}
\textbf{Georgi / MIT / Cambridge}\\
\text{Foundations of oscillations and waves}
\\[6pt]
\downarrow
\\[6pt]
\textbf{Hecht}\\
\text{Main optics backbone}
\\[6pt]
\downarrow
\\[6pt]
\textbf{Goodman}\\
\text{Fourier and computational optics}
\\[6pt]
\downarrow
\\[6pt]
\textbf{Saleh \& Teich / Siegman}\\
\text{Modern optics, photonics, and lasers}
\end{array}
}
$$

---

# 5. Role of Hecht's *Optics*

Eugene Hecht's *Optics* should be one of the primary intellectual backbones of the **optics half** of the course.

It is especially suitable for:

- the nature of light,
- electromagnetic waves,
- propagation,
- reflection and refraction,
- geometrical optics,
- polarization,
- interference,
- coherence,
- diffraction.

However, the entire course should **not** simply become "Hecht converted into Jupyter notebooks."

The waves foundation should be broader and more systematic than a traditional optics-first treatment.

A better structure is:

| Course Area | Primary Source |
|---|---|
| Oscillations | MIT / French / Georgi |
| Coupled oscillators | Georgi / MIT |
| Normal modes | Georgi / MIT |
| Wave equation | Georgi / Cambridge |
| Fourier methods | Cambridge / Georgi |
| Dispersion and wave packets | MIT / Cambridge |
| Electromagnetic waves | Griffiths + Hecht |
| Geometrical optics | Hecht |
| Polarization | Hecht |
| Interference | Hecht |
| Coherence | Hecht |
| Diffraction | Hecht + Goodman |
| Fourier optics | Goodman + Hecht |
| Imaging | Goodman + Hecht |
| Lasers | Hecht introduction + Saleh & Teich |
| Advanced photonics | Saleh & Teich / Siegman |

The ideal synthesis is therefore:

$$
\boxed{
\text{MIT/Cambridge Waves}
+
\text{Hecht Optics}
+
\text{Goodman Fourier Optics}
}
$$

with Griffiths for electromagnetic foundations and Saleh & Teich/Siegman for advanced optics.

---

# 6. Course Scope

A complete version of the course could contain approximately **35–45 notebooks**.

A standard semester offering might select approximately **24–30 core notebooks**.

A more advanced version could include the full sequence.

Suggested structure:

| Part | Subject | Approximate Notebooks |
|---|---|---:|
| 0 | Mathematical and computational foundations | 3 |
| I | Oscillations | 4 |
| II | Coupled oscillators and normal modes | 3 |
| III | Continuous systems and wave equation | 4 |
| IV | Fourier methods, packets, and dispersion | 3 |
| V | Electromagnetic waves and interfaces | 4 |
| VI | Polarization | 2–4 |
| VII | Interference and coherence | 3–5 |
| VIII | Diffraction | 4 |
| IX | Geometrical optics | 3–5 |
| X | Fourier optics and imaging | 4–6 |
| XI | Gaussian beams, lasers, and photonics | 4–8 |
| XII | Optional advanced topics | 6–10 |

---

# 7. Part 0 — Mathematical and Computational Foundations

This section establishes the mathematical language used throughout the course.

---

## Notebook 0.1 — Complex Numbers as the Language of Waves

### Goals

Students should understand why complex numbers are not merely notation but a natural representation of oscillatory systems.

Start from

$$
x(t)=A\cos(\omega t+\phi)
$$

and introduce

$$
z(t)=Ae^{i(\omega t+\phi)}.
$$

### Interactive components

- rotating complex phasor,
- real and imaginary projections,
- amplitude slider,
- frequency slider,
- phase slider,
- addition of several phasors,
- constructive and destructive superposition,
- beats from nearby frequencies.

### Key ideas

- Euler's formula,
- amplitude and phase,
- phasor notation,
- complex representation of sinusoidal signals,
- superposition.

---

## Notebook 0.2 — Fourier Series

### Core equation

$$
f(t)=\sum_{n=-\infty}^{\infty}c_n e^{in\omega_0t}.
$$

### Interactive experiments

Reconstruct:

- square wave,
- triangle wave,
- sawtooth wave,
- pulse train.

The user should control the number of Fourier terms.

### Concepts

- harmonics,
- convergence,
- spectral representation,
- Gibbs phenomenon,
- time-domain versus frequency-domain thinking.

---

## Notebook 0.3 — Fourier Transform and Convolution

### Core equation

$$
F(\omega)=
\int_{-\infty}^{\infty}
f(t)e^{-i\omega t}\,dt.
$$

Introduce convolution:

$$
(f*g)(t)=
\int_{-\infty}^{\infty}
f(\tau)g(t-\tau)\,d\tau.
$$

### Interactive design

Always show:

$$
\text{time/position domain}
\leftrightarrow
\text{frequency/wavenumber domain}.
$$

This dual representation should become one of the signature visual motifs of the course.

---

# 8. Part I — Oscillations

---

## Notebook 1.1 — Simple Harmonic Oscillator

Derive

$$
m\ddot{x}+kx=0.
$$

Solution:

$$
x(t)=A\cos(\omega_0 t+\phi),
\qquad
\omega_0=\sqrt{\frac{k}{m}}.
$$

### Interactive panels

Display simultaneously:

- physical animation,
- $x(t)$,
- $v(t)$,
- $a(t)$,
- kinetic energy,
- potential energy,
- total energy,
- phase-space trajectory.

### Student controls

- mass,
- spring constant,
- initial displacement,
- initial velocity.

---

## Notebook 1.2 — Damped Harmonic Oscillator

$$
m\ddot{x}+b\dot{x}+kx=0.
$$

Explore:

- underdamping,
- critical damping,
- overdamping.

Students should move continuously through the damping parameter space and observe the transition between dynamical regimes.

---

## Notebook 1.3 — Driven Oscillator and Resonance

$$
m\ddot{x}+b\dot{x}+kx=F_0\cos(\omega t).
$$

Explore:

- resonance,
- amplitude response,
- phase response,
- bandwidth,
- quality factor $Q$,
- energy dissipation.

Plot:

$$
|A(\omega)|
$$

and phase as functions of driving frequency.

---

## Notebook 1.4 — Impulse Response and Transients

Connect oscillator physics with linear systems.

Introduce:

$$
x(t)=G(t)*F(t).
$$

This is an important conceptual bridge to later sections on imaging and Fourier optics.

---

# 9. Part II — Coupled Oscillators and Normal Modes

---

## Notebook 2.1 — Two Coupled Oscillators

Introduce the matrix form:

$$
M\ddot{\mathbf{x}}+K\mathbf{x}=0.
$$

Students should discover normal modes through simulation before formal diagonalization.

---

## Notebook 2.2 — Normal Modes and Eigenvectors

Animate systems with:

- two masses,
- three masses,
- five masses,
- arbitrary $N$.

Show:

- eigenvalues,
- eigenvectors,
- modal frequencies,
- physical motion.

Establish:

$$
\boxed{
\text{mechanical normal modes}
\leftrightarrow
\text{optical cavity modes}
}
$$

---

## Notebook 2.3 — From Discrete Oscillators to a Continuous Medium

Increase the number of masses:

$$
2\rightarrow5\rightarrow20\rightarrow100\rightarrow\infty.
$$

Show visually how a discrete lattice approaches a continuous string.

This creates a natural path to the wave equation.

---

# 10. Part III — Continuous Systems and the Wave Equation

---

## Notebook 3.1 — Deriving the Wave Equation

Derive:

$$
\frac{\partial^2 y}{\partial t^2}
=
v^2\frac{\partial^2 y}{\partial x^2}.
$$

Possible physical systems:

- string under tension,
- acoustic pressure,
- elastic rod.

---

## Notebook 3.2 — Traveling Waves

General solution:

$$
y(x,t)=f(x-vt)+g(x+vt).
$$

Interactive components:

- launch arbitrary pulse,
- reverse propagation direction,
- superpose left- and right-moving waves,
- measure velocity.

---

## Notebook 3.3 — Energy and Momentum Transport

Distinguish:

- medium motion,
- disturbance motion,
- energy transport.

This directly addresses a common misconception.

---

## Notebook 3.4 — Reflection, Transmission, and Impedance

Introduce wave impedance and interfaces.

Explore:

- reflected pulses,
- transmitted pulses,
- fixed boundary,
- free boundary,
- impedance matching.

---

# 11. Part IV — Standing Waves, Fourier Modes, and Dispersion

---

## Notebook 4.1 — Standing Waves and Boundary Conditions

Study:

- fixed-fixed,
- fixed-free,
- free-free.

Derive allowed modes such as:

$$
k_n=\frac{n\pi}{L}.
$$

---

## Notebook 4.2 — Fourier Decomposition of Arbitrary Initial Conditions

Construct arbitrary string shapes and decompose them into normal modes.

Show how each mode evolves independently.

---

## Notebook 4.3 — Phase Velocity and Group Velocity

Define:

$$
v_p=\frac{\omega}{k}
$$

and

$$
v_g=\frac{d\omega}{dk}.
$$

Animate a wave packet while tracking:

- carrier wave,
- envelope,
- phase velocity,
- group velocity.

---

## Notebook 4.4 — Dispersion

Allow students to specify or choose dispersion relations:

$$
\omega=\omega(k).
$$

Examples:

- nondispersive medium,
- lattice dispersion,
- deep-water waves,
- optical material model.

Simulate pulse broadening.

---

# 12. Part V — Electromagnetic Waves

The transition into optics should occur only after students are comfortable with waves in general.

---

## Notebook 5.1 — Maxwell Equations to the Wave Equation

Starting from Maxwell's equations, derive:

$$
\nabla^2\mathbf{E}
=
\mu_0\epsilon_0
\frac{\partial^2\mathbf{E}}{\partial t^2},
$$

and similarly for $\mathbf{B}$.

Then:

$$
c=\frac{1}{\sqrt{\mu_0\epsilon_0}}.
$$

This should be treated as a major conceptual event:

> Light is an electromagnetic wave governed by the same mathematical structures developed earlier.

---

## Notebook 5.2 — Plane Electromagnetic Waves

Visualize:

- $\mathbf{E}$,
- $\mathbf{B}$,
- propagation vector $\mathbf{k}$,
- phase fronts.

Show their mutual orthogonality.

---

## Notebook 5.3 — Energy and the Poynting Vector

Introduce:

$$
\mathbf{S}=
\frac{1}{\mu_0}
\mathbf{E}\times\mathbf{B}.
$$

Connect field amplitude to intensity.

---

## Notebook 5.4 — Electromagnetic Waves in Matter

Explore:

- refractive index,
- phase velocity,
- absorption,
- complex refractive index,
- dispersion.

---

# 13. Part VI — Reflection, Refraction, and Interfaces

This section should use **Hecht heavily**.

---

## Notebook 6.1 — Snell's Law

Derive using:

- wavefront geometry,
- phase matching,
- Fermat's principle.

$$
n_1\sin\theta_1=n_2\sin\theta_2.
$$

---

## Notebook 6.2 — Fresnel Equations

Treat s and p polarization separately.

Interactive plots:

- amplitude reflection coefficient,
- intensity reflection,
- transmission,
- angle of incidence.

---

## Notebook 6.3 — Brewster Angle

Visualize the vanishing p-polarized reflection.

---

## Notebook 6.4 — Total Internal Reflection and Evanescent Fields

Explore:

- critical angle,
- evanescent decay,
- frustrated total internal reflection.

---

# 14. Part VII — Polarization

This is one of the areas where the interactive environment can dramatically outperform a static textbook.

---

## Notebook 7.1 — Polarization States

Visualize:

$$
\mathbf{E}(z,t)
=
E_x\cos(kz-\omega t)\hat{x}
+
E_y\cos(kz-\omega t+\delta)\hat{y}.
$$

Students control:

$$
E_x,\quad E_y,\quad \delta.
$$

Observe:

- linear polarization,
- circular polarization,
- elliptical polarization.

---

## Notebook 7.2 — Malus' Law

$$
I=I_0\cos^2\theta.
$$

Build a virtual polarizer/analyzer experiment.

---

## Notebook 7.3 — Jones Calculus

Introduce Jones vectors:

$$
\mathbf{E}
=
\begin{pmatrix}
E_x\\
E_y e^{i\delta}
\end{pmatrix}.
$$

Model systems:

$$
\mathbf{E}_{out}
=
J_NJ_{N-1}\cdots J_1\mathbf{E}_{in}.
$$

Components:

- linear polarizer,
- quarter-wave plate,
- half-wave plate,
- birefringent material.

---

## Notebook 7.4 — Stokes Parameters and Poincaré Sphere

Advanced extension.

Introduce:

- Stokes vector,
- degree of polarization,
- representation on the Poincaré sphere.

---

# 15. Part VIII — Interference and Coherence

This section should follow Hecht closely while adding computational experiments.

---

## Notebook 8.1 — Two-Wave Interference

Derive:

$$
I=
I_1+I_2+
2\sqrt{I_1I_2}\cos\delta.
$$

Allow adjustment of:

- amplitudes,
- phase,
- wavelength,
- relative coherence.

---

## Notebook 8.2 — Young's Double-Slit Experiment

Controls:

$$
\lambda,\quad d,\quad a,\quad L.
$$

Display simultaneously:

1. optical geometry,
2. path difference,
3. phase difference,
4. field contributions,
5. resulting intensity distribution.

---

## Notebook 8.3 — Thin-Film Interference

Example stack:

```text
air
↓
film
↓
glass
```

Student controls:

- thickness,
- refractive index,
- wavelength,
- incidence angle.

Advanced visualization:

- reflected spectrum,
- perceived color.

---

## Notebook 8.4 — Michelson Interferometer

Create a virtual interferometer.

Move a mirror by nanometers and observe fringe motion.

Students should infer wavelength from:

- fringe count,
- mirror displacement.

---

## Notebook 8.5 — Fabry–Pérot Interferometer

Explore:

- cavity length,
- reflectivity,
- finesse,
- free spectral range,
- linewidth.

---

## Notebook 8.6 — Temporal and Spatial Coherence

Introduce:

- coherence time,
- coherence length,
- visibility,
- partially coherent sources.

---

# 16. Part IX — Diffraction

This should be one of the centerpiece sections of the course.

---

## Notebook 9.1 — Huygens–Fresnel Principle

Build diffraction from secondary-wavelet intuition.

---

## Notebook 9.2 — Fraunhofer Diffraction

Introduce the far-field relation:

$$
U(k_x,k_y)
\propto
\mathcal{F}\{A(x,y)\}.
$$

This is one of the most important conceptual connections in the course.

---

## Notebook 9.3 — Single-Slit Diffraction

For a rectangular aperture:

$$
I(\theta)
=
I_0
\operatorname{sinc}^2
\left(
\frac{\pi a\sin\theta}{\lambda}
\right).
$$

Students should already know:

$$
\operatorname{rect}(x)
\stackrel{\mathcal{F}}{\longleftrightarrow}
\operatorname{sinc}(k).
$$

Therefore the diffraction pattern should appear as a natural consequence rather than an isolated formula.

---

## Notebook 9.4 — Double Slit with Finite Slit Width

Show the product of:

- interference structure,
- diffraction envelope.

---

## Notebook 9.5 — Circular Aperture and the Airy Pattern

Introduce diffraction-limited imaging.

---

## Notebook 9.6 — Diffraction Gratings

Explore:

- grating spacing,
- wavelength,
- diffraction orders,
- angular dispersion,
- resolving power.

---

## Notebook 9.7 — Fresnel Diffraction

Numerically propagate fields between planes.

Students observe the transition:

$$
\text{near field}
\rightarrow
\text{far field}.
$$

---

# 17. Part X — Geometrical Optics

Hecht should be the primary reference for this section.

Importantly, geometrical optics should be presented as an **approximation to wave optics**, rather than as the first and most fundamental description of light.

---

## Notebook 10.1 — Fermat's Principle

Introduce optical path length and derive reflection/refraction principles.

---

## Notebook 10.2 — Spherical Surfaces, Mirrors, and Thin Lenses

Cover:

- focal length,
- object distance,
- image distance,
- magnification,
- sign conventions.

---

## Notebook 10.3 — Ray-Transfer / ABCD Matrices

Represent rays as:

$$
\begin{pmatrix}
y\\
\theta
\end{pmatrix}.
$$

Optical systems act as:

$$
\begin{pmatrix}
y_2\\
\theta_2
\end{pmatrix}
=
\begin{pmatrix}
A&B\\
C&D
\end{pmatrix}
\begin{pmatrix}
y_1\\
\theta_1
\end{pmatrix}.
$$

Students should construct compound optical systems interactively.

---

## Notebook 10.4 — Optical Instruments

Model:

- camera,
- microscope,
- telescope,
- magnifier.

---

## Notebook 10.5 — Aberrations

Explore:

- spherical aberration,
- coma,
- astigmatism,
- chromatic aberration.

Optional advanced ray tracing can be added.

---

# 18. Part XI — Fourier Optics

This is where Hecht should transition into Goodman as the main reference.

---

## Notebook 11.1 — Spatial Frequencies

Interpret images as superpositions of spatial Fourier components.

---

## Notebook 11.2 — Fourier Transforming Property of a Lens

Demonstrate how a lens maps angular/spatial-frequency information into a Fourier plane.

---

## Notebook 11.3 — Point Spread Function

Introduce the response of an imaging system to a point source.

---

## Notebook 11.4 — Optical Transfer Function and MTF

Introduce:

- OTF,
- MTF,
- spatial-frequency response,
- resolution.

---

## Notebook 11.5 — Coherent and Incoherent Imaging

Explain the difference between field transfer and intensity transfer.

---

## Notebook 11.6 — 4-f Optical Processor

Build:

```text
object
  ↓
lens
  ↓
Fourier plane
  ↓
spatial filter
  ↓
lens
  ↓
image
```

Let students perform:

- low-pass filtering,
- high-pass filtering,
- edge enhancement,
- directional filtering.

---

# 19. Part XII — Gaussian Beams, Lasers, and Photonics

This section moves toward Caltech-style advanced optics.

---

## Notebook 12.1 — Gaussian Beams

Introduce:

$$
w(z)
=
w_0
\sqrt{
1+
\left(
\frac{z}{z_R}
\right)^2
}.
$$

Explore:

- beam waist,
- Rayleigh range,
- divergence,
- wavefront curvature.

---

## Notebook 12.2 — Gaussian Beam Propagation Through Lenses

Use ABCD matrices for Gaussian beams.

---

## Notebook 12.3 — Optical Resonators

Explore cavity stability and modes.

---

## Notebook 12.4 — Laser Fundamentals

Introduce:

- spontaneous emission,
- stimulated emission,
- population inversion,
- optical feedback.

Keep the initial treatment semiclassical.

---

## Notebook 12.5 — Waveguides

Explore:

- boundary conditions,
- guided modes,
- cutoff,
- propagation constants.

---

## Notebook 12.6 — Optical Fibers

Introduce:

- numerical aperture,
- total internal reflection,
- guided modes,
- modal dispersion,
- chromatic dispersion.

---

# 20. Optional Advanced Modules

Possible advanced extensions:

- nonlinear optics,
- second-harmonic generation,
- electro-optics,
- acousto-optics,
- holography,
- spectroscopy,
- ultrafast optics,
- photonic crystals,
- metamaterials,
- integrated photonics,
- quantum optics,
- single-photon interference,
- squeezed light,
- computational imaging,
- adaptive optics.

---

# 21. Recommended Notebook Pedagogy

Every notebook should follow a repeatable structure.

## Phase 1 — Observe

Present a physical phenomenon.

Example:

> What happens to a diffraction pattern when the slit becomes narrower?

---

## Phase 2 — Predict

Ask the student to commit to a qualitative prediction before calculation.

---

## Phase 3 — Explore

Provide sliders or parameter controls.

Example:

- wavelength,
- aperture width,
- distance,
- refractive index,
- damping,
- drive frequency.

---

## Phase 4 — Derive

Develop the analytical physics.

---

## Phase 5 — Compute

Use numerical methods to reproduce or extend the analytical result.

---

## Phase 6 — Measure

Treat the simulation as an experiment.

Include:

- noise,
- finite detector resolution,
- imperfect alignment,
- calibration.

---

## Phase 7 — Explain

Ask the student to interpret the result physically.

---

## Phase 8 — Extend

Modify assumptions and investigate a harder version.

---

# 22. Three Synchronized Representations

A signature feature of the course should be the simultaneous presentation of:

1. physical system,
2. mathematical representation,
3. spectral or modal representation.

Examples:

| Physical System | Mathematical View | Spectral/Modal View |
|---|---|---|
| Oscillator | $x(t)$ | $X(\omega)$ |
| Wave packet | $y(x,t)$ | $A(k)$ |
| Optical aperture | $A(x,y)$ | $\mathcal{F}[A]$ |
| Image | $I(x,y)$ | Spatial-frequency spectrum |
| Optical pulse | $E(t)$ | $E(\omega)$ |
| Coupled oscillators | $\mathbf{x}(t)$ | Normal-mode amplitudes |

The student should gradually internalize that Fourier space and modal space are not artificial tricks; they are natural descriptions of wave systems.

---

# 23. Virtual Laboratories

Virtual laboratories should be a major component.

| Virtual Lab | Main Quantities Measured |
|---|---|
| Spring oscillator | $k,\omega,Q$ |
| Driven oscillator | resonance frequency, bandwidth |
| Coupled pendulums | normal-mode frequencies |
| String | wave velocity |
| Resonance tube | speed of sound |
| Interface | reflection/transmission coefficients |
| Polarization apparatus | Malus' law |
| Double slit | wavelength |
| Michelson interferometer | wavelength/displacement |
| Thin film | optical thickness |
| Diffraction slit | slit width |
| Grating spectrometer | unknown wavelengths |
| Telescope | diffraction-limited resolution |
| Fabry–Pérot | finesse and FSR |
| Gaussian beam | waist and Rayleigh range |

---

# 24. Synthetic Experimental Noise

The course should deliberately avoid unrealistically perfect numerical measurements.

For example, instead of obtaining:

$$
\lambda=632.800000\;\mathrm{nm},
$$

students might obtain:

$$
\lambda=(633\pm4)\;\mathrm{nm}.
$$

Students then perform:

- curve fitting,
- uncertainty propagation,
- residual analysis,
- parameter estimation,
- goodness-of-fit evaluation.

This transforms the notebooks from demonstrations into physics laboratories.

---

# 25. Integration with Real Experiments

Where practical, computational notebooks should be paired with inexpensive physical experiments.

Ideal workflow:

$$
\boxed{
\text{simulation}
\rightarrow
\text{prediction}
\rightarrow
\text{real measurement}
\rightarrow
\text{data import}
\rightarrow
\text{analysis}
}
$$

Examples:

## Diffraction

Photograph a real diffraction pattern and use the notebook to estimate slit width.

## Polarization

Measure intensity through crossed polarizers and compare to Malus' law.

## Michelson interferometry

Use fringe counts to measure wavelength or displacement.

## Fourier optics

Compare an experimentally measured diffraction pattern with an FFT prediction.

---

# 26. Assessment Philosophy

Assessment should measure more than algebraic ability.

Four layers are recommended.

## 26.1 Concept Checks

Example:

> A slit becomes narrower. Does the diffraction pattern become wider or narrower?

---

## 26.2 Analytical Derivations

Students derive physical relationships.

---

## 26.3 Computational Investigations

Students vary parameters and identify relationships numerically.

Example:

Fit

$$
\Delta x \propto a^\alpha
$$

for single-slit diffraction and determine $\alpha$.

---

## 26.4 Open Investigations

Example:

> A telescope has a 10 mm aperture. Determine how its resolving capability changes with wavelength. Verify the result analytically and computationally and explain the underlying physics.

The desired skill set is:

$$
\boxed{
\text{intuition}
+
\text{mathematics}
+
\text{computation}
+
\text{experimental reasoning}
}
$$

---

# 27. Hecht Companion Strategy

The optics notebooks should explicitly indicate relevant Hecht reading.

A notebook can contain a heading such as:

> **Textbook companion:** Hecht, *Optics* — Polarization

Avoid tying the course too rigidly to chapter numbers because editions may differ.

A recommended four-stage Hecht companion structure is:

## Stage 1 — Before Reading

Begin with a physical question or simulation.

## Stage 2 — Theory

Develop the rigorous physics covered in Hecht.

## Stage 3 — Computational Experiment

Explore parameters interactively.

## Stage 4 — Analytical Problems

Solve traditional textbook-style problems.

Then add a fifth stage that a textbook normally cannot provide:

## Stage 5 — Generalization

Change assumptions and investigate the broader parameter space.

---

# 28. Example: Hecht Polarization as an Interactive Sequence

Students begin with:

$$
\mathbf{E}(z,t)
=
E_x\cos(kz-\omega t)\hat{x}
+
E_y\cos(kz-\omega t+\delta)\hat{y}.
$$

Controls:

$$
E_x,\quad E_y,\quad \delta.
$$

They observe:

- linear polarization,
- circular polarization,
- elliptical polarization.

Then introduce Jones vectors and components.

Virtual system:

```text
Laser
  ↓
Linear polarizer
  ↓
Quarter-wave plate
  ↓
Half-wave plate
  ↓
Analyzer
  ↓
Detector
```

Students can predict the output polarization and verify it computationally.

---

# 29. Example: Hecht Interference as a Virtual Laboratory Family

A traditional interference chapter can become several virtual laboratories.

## Two-Beam Interference

$$
I=
I_1+I_2+
2\sqrt{I_1I_2}\cos\delta.
$$

## Young's Experiment

Vary:

- wavelength,
- slit spacing,
- slit width,
- screen distance.

## Thin Films

Specify:

```text
air
↓
film n = 1.38
thickness = 250 nm
↓
glass n = 1.52
```

Compute reflected intensity versus wavelength.

## Michelson Interferometer

Move the mirror and count fringes.

## Fabry–Pérot

Change:

$$
R,\quad L,\quad n,\quad \lambda
$$

and observe:

- resonance peaks,
- finesse,
- free spectral range.

---

# 30. Example: Hecht Diffraction + Goodman Fourier Optics

This is one of the most important textbook transitions.

Hecht provides the physical picture and classical derivations.

Goodman provides the deeper Fourier framework.

For an aperture:

$$
A(x,y),
$$

the far-field optical amplitude is approximately:

$$
U(k_x,k_y)
\propto
\mathcal{F}\{A(x,y)\}.
$$

Students should be able to create arbitrary apertures and calculate diffraction.

Possible apertures:

- single slit,
- double slit,
- square,
- circle,
- triangle,
- grating,
- arbitrary drawing,
- uploaded image.

This leads directly to:

$$
\boxed{
\text{Optics}
\leftrightarrow
\text{Fourier Analysis}
}
$$

---

# 31. Why Fourier Methods Should Appear Earlier Than in Many Traditional Optics Courses

One deliberate modification from many textbook-first sequences is to introduce Fourier analysis before diffraction.

Students should already know:

$$
\operatorname{rect}(x)
\stackrel{\mathcal F}{\longleftrightarrow}
\operatorname{sinc}(k).
$$

Then a rectangular aperture:

$$
A(x)
=
\operatorname{rect}
\left(
\frac{x}{a}
\right)
$$

naturally gives:

$$
I(\theta)
\propto
\operatorname{sinc}^{2}
\left(
\frac{\pi a\sin\theta}{\lambda}
\right).
$$

This is pedagogically stronger than presenting the sinc function as an unexpected diffraction formula.

---

# 32. Software Architecture

Recommended stack:

```text
Python
├── NumPy
├── SciPy
├── Matplotlib
├── SymPy
├── ipywidgets
├── Plotly
├── Pillow / imageio
└── optional JAX or Numba for advanced simulations
```

The notebooks should not contain large amounts of infrastructure code.

Instead, create a reusable internal library.

```text
wavephysics/
├── oscillators/
├── coupled/
├── waves/
├── fourier/
├── electromagnetism/
├── interfaces/
├── polarization/
├── interference/
├── diffraction/
├── rayoptics/
├── gaussian/
├── imaging/
├── photonics/
├── experiments/
└── visualization/
```

Example notebook API:

```python
from wavephysics.diffraction import Aperture

aperture = Aperture.double_slit(
    width=20e-6,
    separation=100e-6
)

aperture.interactive_far_field(
    wavelength=532e-9
)
```

This keeps the notebooks focused on physics.

---

# 33. Suggested Repository Structure

```text
physics-courses/
│
├── common/
│   ├── mathematics/
│   ├── numerical_methods/
│   ├── visualization/
│   ├── uncertainty/
│   └── units/
│
├── classical_mechanics/
│
├── thermodynamics/
│
├── waves_optics/
│   ├── 00_foundations/
│   ├── 01_oscillations/
│   ├── 02_coupled_oscillators/
│   ├── 03_wave_equation/
│   ├── 04_fourier_waves/
│   ├── 05_em_waves/
│   ├── 06_interfaces/
│   ├── 07_polarization/
│   ├── 08_interference/
│   ├── 09_diffraction/
│   ├── 10_geometrical_optics/
│   ├── 11_fourier_optics/
│   ├── 12_gaussian_beams/
│   ├── 13_lasers_photonics/
│   ├── labs/
│   ├── hecht_problems/
│   ├── projects/
│   └── exams/
│
└── quantum_mechanics/
```

---

# 34. Notebook Types

A useful repository organization could distinguish notebook purposes.

```text
notebooks/
├── theory/
├── explorations/
├── laboratories/
├── hecht_problems/
├── projects/
└── assessments/
```

Each serves a different pedagogical function.

---

# 35. Capstone Projects

---

## 35.1 Computational Telescope

Model:

$$
\text{scene}
\rightarrow
\text{aperture}
\rightarrow
\text{diffraction}
\rightarrow
\text{PSF}
\rightarrow
\text{sensor}.
$$

Students change:

- aperture,
- wavelength,
- focal length,
- aberrations,
- detector sampling,
- noise.

---

## 35.2 Virtual Optical Bench

Allow a student to assemble:

```text
Laser
  ↓
Polarizer
  ↓
Wave plate
  ↓
Lens
  ↓
Aperture
  ↓
Lens
  ↓
Detector
```

The system propagates the optical field automatically.

Possible propagation models:

- ray optics,
- Fresnel propagation,
- Fraunhofer propagation,
- Gaussian beam approximation.

---

## 35.3 Grating Spectrometer

Students design a spectrometer and analyze:

- angular dispersion,
- wavelength range,
- spectral resolution,
- resolving power,
- detector sampling.

---

## 35.4 Optical Communication System

Model:

$$
\text{laser}
\rightarrow
\text{modulator}
\rightarrow
\text{fiber}
\rightarrow
\text{dispersion}
\rightarrow
\text{detector}.
$$

---

## 35.5 Fourier-Optics Image Processor

Create a simulated 4-f optical system.

Students manipulate spatial-frequency filters and process images optically.

This single project unifies:

- diffraction,
- Fourier transforms,
- imaging,
- spatial filtering,
- lenses,
- resolution.

---

# 36. Layered Difficulty Within Each Notebook

Every notebook should support multiple levels.

## Core

Required material.

Focus:

- conceptual understanding,
- essential derivation,
- standard computation.

## Deep Dive

More mathematical or computational detail.

Possible topics:

- Green functions,
- eigenfunction expansions,
- numerical PDE solution,
- matrix methods,
- Fourier-integral derivations.

## Research Connection

Show where the topic appears in modern physics.

Example:

```text
Normal modes
    ↓
Optical cavities
    ↓
Laser modes
    ↓
Cavity QED
    ↓
Quantum information
```

This allows advanced students to continue deeper without making every section mandatory.

---

# 37. Recommended Textbooks and References

## Waves

### Howard Georgi
*The Physics of Waves*

Strong theoretical backbone for waves and normal modes.

### A. P. French
*Vibrations and Waves*

Excellent undergraduate introduction.

### MIT 8.03
*Physics III: Vibrations and Waves*

OpenCourseWare lectures, notes, problems, and curriculum structure.

https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/

---

## General Optics

### Eugene Hecht
*Optics*

Primary optics textbook for this course.

Use especially for:

- electromagnetic theory of light,
- propagation,
- geometrical optics,
- polarization,
- interference,
- coherence,
- diffraction.

---

## Electromagnetism

### David J. Griffiths
*Introduction to Electrodynamics*

Useful for deriving electromagnetic waves and boundary conditions rigorously.

### J. D. Jackson
*Classical Electrodynamics*

Advanced reference only.

---

## Fourier Optics

### Joseph W. Goodman
*Introduction to Fourier Optics*

Primary advanced companion for:

- spatial frequencies,
- diffraction integrals,
- imaging systems,
- Fourier transforms,
- OTF/MTF,
- coherent and incoherent imaging,
- spatial filtering.

---

## Classical Physical Optics

### Born and Wolf
*Principles of Optics*

Advanced reference for physical optics.

---

## Photonics

### Saleh and Teich
*Fundamentals of Photonics*

Use for:

- guided waves,
- optical fibers,
- lasers,
- nonlinear optics,
- modern photonics.

---

## Lasers

### A. E. Siegman
*Lasers*

Advanced reference for Gaussian beams, resonators, and laser physics.

---

# 38. Recommended Teaching Sequence

A strong full sequence is:

```text
Mathematical Tools
    ↓
Simple Oscillator
    ↓
Damped / Driven Oscillator
    ↓
Coupled Oscillators
    ↓
Normal Modes
    ↓
Continuous Systems
    ↓
Wave Equation
    ↓
Standing Waves
    ↓
Fourier Analysis
    ↓
Wave Packets
    ↓
Dispersion
    ↓
Electromagnetic Waves
    ↓
Propagation in Matter
    ↓
Reflection / Refraction
    ↓
Polarization
    ↓
Interference
    ↓
Coherence
    ↓
Diffraction
    ↓
Geometrical Optics
    ↓
Fourier Optics
    ↓
Imaging
    ↓
Gaussian Beams
    ↓
Resonators
    ↓
Lasers
    ↓
Waveguides / Fibers
    ↓
Advanced Photonics
```

---

# 39. Relationship to the Broader Physics Curriculum

The course should become the conceptual bridge between other planned physics courses.

```text
Classical Mechanics
        ↓
Oscillations
        ↓
Coupled Oscillators
        ↓
Normal Modes
        ↓
Waves
   ↙           ↘
Optics        Quantum Mechanics
   ↓
Electromagnetism / Photonics
```

Important concepts introduced here reappear later:

- eigenvalues,
- eigenvectors,
- boundary conditions,
- Fourier transforms,
- dispersion relations,
- wave packets,
- interference,
- eigenmodes,
- Green functions,
- spectral decomposition.

---

# 40. Guiding Design Principle

The finished environment should feel less like:

> an interactive Hecht textbook

and more like:

> a virtual university physics laboratory that uses Hecht as one of its main theoretical backbones.

The student should not merely execute:

```python
plot_diffraction(...)
```

They should be able to ask:

> What happens if I halve the aperture?

Then:

1. make a prediction,
2. change the aperture,
3. observe the result,
4. measure the scaling,
5. derive the relationship,
6. compare numerical and analytical answers,
7. explain the physics.

That process is closer to how physics is actually practiced.

---

# 41. Final Recommended Course Identity

A suitable name is:

# **Waves, Oscillations & Optics — An Interactive Computational Physics Course**

Its academic identity would combine:

- **MIT** for the oscillations-and-waves progression,
- **Cambridge** for Fourier methods and unified waves/optics structure,
- **Hecht** for the main physical-optics backbone,
- **Goodman** for Fourier optics and imaging,
- **Caltech** for advanced optics, beams, resonators, and photonics,
- **Berkeley/Stanford** for computational and laboratory emphasis.

The result should be a course that is rigorous enough to resemble a strong university physics sequence while exploiting computational tools to make abstract wave phenomena directly observable and experimentally testable.

---

# 42. Recommended Next Development Step

The next planning artifact should convert this curriculum into a **notebook-by-notebook implementation specification**.

For every notebook define:

1. notebook ID,
2. title,
3. prerequisites,
4. learning objectives,
5. required mathematical background,
6. core derivations,
7. physical intuition goals,
8. interactive controls,
9. simulations,
10. virtual laboratory,
11. real experiment counterpart where applicable,
12. Hecht companion material,
13. primary references,
14. concept-check questions,
15. analytical exercises,
16. computational exercises,
17. challenge problems,
18. expected runtime/computational cost,
19. reusable library components required,
20. dependencies on earlier notebooks.

This would turn the curriculum into an actionable engineering and teaching plan.

---

# 43. Summary

The recommended architecture is:

$$
\boxed{
\text{rigorous wave foundations}
+
\text{Hecht-centered optics}
+
\text{Fourier/computational optics}
+
\text{virtual experimentation}
}
$$

with the following hierarchy:

$$
\boxed{
\text{Georgi/MIT/Cambridge}
\rightarrow
\text{Hecht}
\rightarrow
\text{Goodman}
\rightarrow
\text{Saleh \& Teich / Siegman}
}
$$

The course should preserve the analytical precision of a traditional physics curriculum while adding capabilities unavailable in a textbook:

- dynamic visualization,
- parameter exploration,
- numerical experiments,
- field propagation,
- Fourier-space visualization,
- synthetic measurement noise,
- data fitting,
- real experiment integration,
- computational capstone projects.

The central educational objective is not simply to teach formulas about waves and optics.

It is to teach students to **think in waves**.