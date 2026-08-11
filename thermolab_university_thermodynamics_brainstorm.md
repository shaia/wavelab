# ThermoLab: Interactive University-Level Thermodynamics Environment

## Recommended direction

Build it as an **interactive computational textbook and virtual laboratory**, rather than simply a folder of notebooks.

Each topic should connect four views:

1. **Macroscopic:** pressure, temperature, volume, entropy, free energy.
2. **Microscopic:** particles, states, collisions, distributions, multiplicity.
3. **Mathematical:** derivatives, integrals, differentials, probability, asymptotics.
4. **Computational:** simulation, numerical experiment, parameter exploration and data analysis.

This mirrors the strongest aspects of leading courses. MIT and Stanford explicitly connect probability and microscopic models to thermodynamics; Cambridge gives a particularly systematic treatment of classical thermodynamics; Oxford tightly connects kinetic theory, transport, thermodynamic equilibrium and statistical foundations; Harvard and Caltech extend the subject through quantum gases, condensed matter, radiation and phase transitions.

Reference: [MIT OCW — Statistical Physics I](https://ocw.mit.edu/courses/8-044-statistical-physics-i-spring-2013/pages/syllabus/)

I would give the project a working concept such as:

> **ThermoLab: Explore, derive and simulate thermal physics**

---

# 1. Decide exactly what course you are building

“University thermodynamics” can mean three rather different courses:

- Engineering thermodynamics: cycles, turbines, compressors, properties and control volumes.
- Classical physics thermodynamics: laws, entropy, potentials, equilibrium and phase changes.
- Statistical and thermal physics: microstates, ensembles, partition functions, quantum gases and critical phenomena.

For a physics audience, I recommend the third interpretation, with classical thermodynamics as a rigorous foundation.

## Intended audience

A good primary target would be:

- Second- or third-year physics students.
- Comfortable with single-variable calculus.
- Some multivariable calculus and partial derivatives.
- Basic mechanics.
- Elementary Python.
- No previous probability course required.
- Quantum mechanics required only for the advanced quantum-statistics section.

Berkeley’s upper-division thermal physics course now explicitly expects some Python for homework, while MIT, Stanford and Harvard place probability early enough that it can be taught as part of thermal physics rather than treated solely as a prerequisite.

Reference: [UC Berkeley Student Learning Center — Physics 110A/110B](https://slc.berkeley.edu/physics-110a-110b)

---

# 2. Use a spiral curriculum

There are two traditional orders:

## Thermodynamics-first

Begin with equilibrium, heat, work, laws, entropy and thermodynamic potentials. Then explain their microscopic origin.

This is close to Cambridge’s structure. Its syllabus progresses through state variables, exact and inexact differentials, the laws, entropy, potentials, phase changes, radiation and kinetic theory.

Reference: [University of Cambridge — Thermodynamics](https://www-teach.phy.cam.ac.uk/students/courses/thermodynamics/80)

## Statistical-mechanics-first

Begin with probability, multiplicity, random walks and microstates. Then derive temperature, entropy and thermodynamics.

This is visible in MIT, Stanford, Harvard and parts of Caltech’s approach. Stanford, for example, moves from combinatorics and the central limit theorem to microstates, entropy, equilibrium, model systems and quantum statistics.

Reference: [MIT OCW — Statistical Physics I](https://ocw.mit.edu/courses/8-044-statistical-physics-i-spring-2013/pages/syllabus/)

## My recommendation: alternate the two

Do not postpone microscopic interpretation until the end, but do not attempt to derive the entire subject from ensembles before students understand what thermodynamics is trying to describe.

For example:

1. Observe pressure macroscopically.
2. Reproduce it with particle collisions.
3. Introduce internal energy and work.
4. Show how energy is distributed among microstates.
5. Introduce entropy macroscopically.
6. Reinterpret it statistically.
7. Introduce free energy.
8. Derive it from the canonical ensemble.

This gives students repeated contact with difficult ideas rather than one high-stakes introduction.

---

# 3. Proposed curriculum

I would build **12 core modules** and **6 advanced modules**. The core can form one semester; the advanced modules can form a second term or an honours extension.

## Core thermal physics

| Module | Main content | Interactive centrepiece |
|---|---|---|
| 0. Orientation | Units, conventions, derivatives, probability diagnostic | Diagnostic concept map and readiness quiz |
| 1. Thermal equilibrium | Systems, boundaries, equilibrium, state variables, zeroth law | Two bodies exchanging energy |
| 2. Equations of state | Ideal gas, real gases, intensive and extensive variables | Interactive \(P\)-\(V\)-\(T\) surface |
| 3. Probability and emergence | Random variables, multiplicity, random walks, central limit theorem | Thousands of random walkers converging toward a Gaussian |
| 4. Kinetic theory | Microscopic pressure, temperature, molecular speeds, equipartition | Particles colliding with a movable piston |
| 5. First law | Internal energy, heat, work, path dependence, heat capacities | Draw a path in the \(P\)-\(V\) plane and calculate work |
| 6. Thermodynamic processes | Isothermal, adiabatic, isobaric, quasistatic and irreversible processes | Compare paths with identical endpoints |
| 7. Second law | Kelvin and Clausius statements, Carnot theorem, engines and refrigerators | Construct a heat engine and explore efficiency bounds |
| 8. Entropy | Clausius entropy, entropy production, mixing and irreversibility | Gas mixing and multiplicity simulation |
| 9. Fundamental relation | \(S(U,V,N)\), extensivity, Euler relation, Gibbs–Duhem relation and stability | Explore entropy surfaces and equilibrium as constrained maximization |
| 10. Thermodynamic potentials | Enthalpy, Helmholtz and Gibbs free energies, Legendre transforms, Maxwell relations | Interactive “natural variables” map |
| 11. Statistical ensembles | Microcanonical and canonical ensembles, Boltzmann distribution | Small system coupled to a finite heat bath |
| 12. Partition functions | Thermodynamic quantities from \(Z\), ideal gas, paramagnet, harmonic oscillators | Numerically reconstruct \(U\), \(S\), \(F\) and \(C_V\) from \(Z\) |

This core combines the classical coverage emphasized at Cambridge with the probability, ensembles and model-system approach found at MIT and Stanford. Oxford’s current course is especially useful as a model for connecting thermodynamic, kinetic and statistical definitions of temperature and pressure rather than presenting them as unrelated formulas.

Reference: [University of Cambridge — Thermodynamics](https://www-teach.phy.cam.ac.uk/students/courses/thermodynamics/80)

## Advanced thermal and statistical physics

| Module | Main content | Interactive centrepiece |
|---|---|---|
| 13. Chemical potential | Particle exchange, grand canonical ensemble, reactions and osmotic equilibrium | Two systems exchanging particles |
| 14. Phase equilibrium | Gibbs phase rule, latent heat, Clausius–Clapeyron, van der Waals fluid | Phase diagram with movable coexistence point |
| 15. Phase transitions | Order parameters, symmetry breaking, Ising model, critical behaviour | Monte Carlo Ising simulation |
| 16. Thermal radiation and solids | Planck spectrum, photons, Einstein and Debye solids | Blackbody and heat-capacity explorers |
| 17. Quantum statistics | Bose–Einstein and Fermi–Dirac distributions, BEC, degenerate Fermi gas | Compare classical, Bose and Fermi occupation functions |
| 18. Fluctuations and transport | Response functions, fluctuations, diffusion, viscosity, thermal conductivity and local equilibrium | Random walk → diffusion equation experiment |

These extensions are strongly represented in Caltech, Harvard and Berkeley thermal-physics offerings. Current Caltech material also explicitly includes fluctuations, linear response, classical fluids and computer simulation methods; Harvard’s 2026 statistical mechanics course includes classical and quantum gases, phase transitions, critical points and Bose–Einstein condensation.

Reference: [Caltech — ChE/Ch 164](https://cce.caltech.edu/academics/courses/chech-164)

---

# 4. Structure every notebook as a learning experience

A notebook should not begin with two pages of definitions followed by code.

Use the same rhythm throughout the series:

## 1. A physical puzzle

Examples:

- Why does pressure remain nearly constant despite individual molecular collisions being violent and irregular?
- Can two processes have identical initial and final states but transfer different amounts of heat?
- Why can no clever engine exceed Carnot efficiency?
- Why does an isolated gas almost never spontaneously gather into one corner?
- Why does a solid’s heat capacity vanish at low temperature?

## 2. Predict before calculating

Ask students to commit to a prediction:

- Which curve will be steeper?
- Will entropy increase, decrease or remain constant?
- What happens as the number of particles increases?
- Which distribution is broader?
- Does doubling the system double the fluctuation?

Store the prediction before showing the simulation.

## 3. Manipulate the model

Use sliders, draggable points, buttons and direct graphical manipulation. Jupyter Widgets currently provides standard browser controls as well as support for more advanced visual components.

Reference: [ipywidgets Documentation](https://ipywidgets.readthedocs.io/en/latest/)

## 4. Derive the result

After exploration, present the precise derivation.

The derivation should always identify:

- System and boundary.
- Independent variables.
- Constraints.
- Sign convention.
- Approximation.
- Limiting regime.
- Whether a differential is exact.
- Whether the argument is thermodynamic, statistical or kinetic.

## 5. Verify computationally

Students should test the result against:

- Numerical integration.
- Simulation.
- Experimental data.
- Dimensional analysis.
- Limiting cases.
- Conservation laws.

## 6. Transfer the idea

Change the physical context.

For example, after deriving the Boltzmann distribution for a two-level system, apply it to:

- A paramagnet.
- Molecular excitation.
- Atmospheric density.
- Defect concentrations.
- A simplified chemical equilibrium.

## 7. End with an explanation

Ask for a short response such as:

> Explain why heat is not a property contained in a system.

That is often more revealing than another numerical calculation.

---

# 5. Build interactions that reveal physics

The simulation should have a specific conceptual purpose. It should not merely animate something already understood.

## Particularly valuable interactive laboratories

### Particle pressure laboratory

Students vary \(N\), \(T\), particle mass and container volume. The environment shows individual impulses, time-averaged pressure and pressure fluctuations.

The important lesson is not only \(PV=Nk_BT\), but that a stable macroscopic variable emerges from noisy microscopic events.

### Thermodynamic path editor

Students draw curves in a \(P\)-\(V\) diagram. The notebook computes

\[
W=\int P\,dV
\]

and compares different paths between the same states.

This makes the distinction between path functions and state functions visually unavoidable.

### Entropy and multiplicity laboratory

Use coins, spins or particles distributed between boxes. Students see how overwhelmingly probable equilibrium macrostates become as \(N\) grows.

### Finite heat-bath experiment

A small system exchanges energy with baths of different sizes. This shows how the canonical ensemble emerges and why an infinite bath is an approximation.

### Maxwell-relation explorer

Students manipulate a model fundamental relation and numerically verify cross derivatives. This is much more useful than memorizing a thermodynamic square.

### Phase-transition laboratory

Start with van der Waals isotherms and coexistence, then introduce the Ising model. Students should see hysteresis, finite-size effects and critical slowing down rather than being shown only a smooth textbook curve.

### Blackbody laboratory

Allow variation of temperature while separately showing spectral radiance by frequency and wavelength. This is a good place to demonstrate that the peak depends on which spectral variable is being plotted.

### Fluctuation laboratory

Plot relative fluctuations against system size and verify their typical \(N^{-1/2}\) scaling where applicable.

---

# 6. Treat common misconceptions as design requirements

Thermal physics remains conceptually difficult even for upper-level students. Research has documented persistent confusion about internal energy, heat, work, entropy and the first and second laws, including among students who have completed traditional instruction.

Reference: [Physical Review Physics Education Research — Thermodynamics Conceptual Understanding](https://link.aps.org/doi/10.1103/PhysRevPhysEducRes.20.020110)

Your environment should therefore deliberately target statements such as:

- Heat and temperature are the same kind of quantity.
- Heat is stored inside a body.
- Temperature measures total internal energy.
- Entropy always means “disorder.”
- An adiabatic process must have constant temperature.
- A reversible process is simply one that can run backward.
- Entropy of every subsystem must increase.
- Equilibrium means that microscopic motion stops.
- The canonical ensemble means every microstate is equally probable.
- \(dQ\) and \(dW\) are ordinary exact differentials.
- Negative temperature means colder than absolute zero.

Do not merely label these as wrong. Construct experiments where the incorrect model makes a visibly incorrect prediction.

A validated conceptual survey covering thermodynamic processes and the first and second laws can provide a model for your diagnostic and post-course assessment, although you should check permissions before reproducing assessment questions.

Reference: [Physical Review Physics Education Research — Thermodynamics Concept Inventory](https://link.aps.org/doi/10.1103/PhysRevPhysEducRes.17.010104)

---

# 7. Scientific-accuracy framework

Every simulation should include a small **model specification**.

For example:

> **System:** \(N\) noninteracting point particles  
> **Dynamics:** elastic collisions  
> **Boundary:** rigid two-dimensional container  
> **Ensemble:** approximately microcanonical  
> **Ignored:** intermolecular forces, quantum effects, gravity  
> **Valid when:** dilute classical regime  
> **Failure modes:** high density, low temperature, strong interactions

Also establish these project-wide rules:

## Fixed conventions

Choose one work convention and keep it everywhere:

\[
dU=\delta Q-\delta W_{\text{by system}}
\]

or

\[
dU=\delta Q+\delta W_{\text{on system}}.
\]

Never switch silently between them.

## Automated correctness checks

Each notebook should test:

- Dimensional consistency.
- Conservation of energy or particle number.
- Known analytic special cases.
- High- and low-temperature limits.
- Large-\(N\) behaviour.
- Numerical convergence.
- Independence from arbitrary simulation seeds, within statistical uncertainty.

## Separate exact statements from approximations

Visually distinguish:

- Definition.
- Empirical law.
- Theorem.
- Model assumption.
- Approximation.
- Numerical observation.
- Open interpretive issue.

## Never let simulation substitute for reasoning

A Monte Carlo result can support intuition, but it does not prove a thermodynamic identity. Students should know what follows from mathematics, what follows from a model and what follows from numerical evidence.

## Independent review

Before publication, each module should receive:

- Physics review.
- Mathematical review.
- Computational review.
- Student usability review.

---

# 8. Assessment design

Active learning has consistently outperformed lecture-only instruction across STEM courses, so the notebooks should require students to predict, calculate, discuss and explain rather than passively run cells.

Reference: [PNAS — Active learning increases student performance in science, engineering, and mathematics](https://www.pnas.org/doi/10.1073/pnas.1319030111)

A balanced module might contain:

| Activity | Purpose |
|---|---|
| Prediction question | Expose initial mental model |
| Concept checkpoint | Test qualitative understanding |
| Hand derivation | Establish mathematical fluency |
| Computational task | Explore nontrivial or large systems |
| Interpretation question | Connect output to physics |
| Challenge problem | Transfer to a new situation |
| Reflection | Explain what changed in the student’s reasoning |

Do not autograde everything. Numerical code, units and limiting cases can be automatically checked. Explanations, diagrams and derivations require human or rubric-based evaluation.

`nbgrader` supports notebook assignments containing code exercises and written responses, along with automatic and manual grading workflows.

Reference: [nbgrader Documentation](https://nbgrader.readthedocs.io/en/stable/)

---

# 9. Suggested technical architecture

## Authoring and publication

Use **Jupyter Book 2 with MyST Markdown** as the main publication layer.

Keep long explanations in `.md` or `.myst` documents and use notebooks for genuinely computational sections. Jupyter Book 2 supports executable content, equations, figures, cross-references and citations without forcing every page to be a large notebook file.

Reference: [Jupyter Book Documentation](https://jupyterbook.org/latest/)

## Interactivity

Use:

- NumPy and SciPy for computation.
- Matplotlib for standard plots.
- `ipywidgets` for sliders, buttons and selectors.
- SymPy for selected symbolic checks.
- Pint or an equivalent units library for dimensional quantities.
- Numba only when simulations genuinely require acceleration.

Avoid hiding all physics inside a large framework. Core model functions should be plain, readable Python that students can inspect.

## Delivery modes

### JupyterLite

Zero-install browser demonstrations and smaller exercises.

Reference: [JupyterLite Documentation](https://jupyterlite.readthedocs.io/en/stable/)

### JupyterHub

A controlled multi-user environment for a real class, with separate environments for students.

Reference: [JupyterHub Documentation](https://jupyterhub.readthedocs.io/en/latest/)

### Voilà

Selected polished experiments that should feel like applications rather than editable notebooks.

Reference: [Voilà Documentation](https://voila.readthedocs.io/en/latest/)

Do not force every learner into one mode. A public reader may want a five-minute browser simulation, while an enrolled student needs editable notebooks, saved work and graded assignments.

## Suggested repository structure

```text
thermolab/
├── book/
│   ├── index.md
│   ├── foundations/
│   ├── thermodynamics/
│   ├── statistical-mechanics/
│   └── advanced/
├── notebooks/
│   ├── explorations/
│   ├── laboratories/
│   └── assignments/
├── src/
│   └── thermolab/
│       ├── gases.py
│       ├── ensembles.py
│       ├── cycles.py
│       ├── phase_transitions.py
│       └── visualization.py
├── tests/
├── data/
├── instructor/
└── environment.yml
```

Keep physics implementations in `src/thermolab` rather than duplicating them across notebooks. The notebook should orchestrate the lesson, not become the entire software system.

---

# 10. Start with a vertical slice

Do not begin by writing all 18 modules.

Build three excellent prototypes:

## Prototype A: Microscopic origin of pressure

This tests animation, simulation, averaging and the micro-to-macro connection.

## Prototype B: Work and thermodynamic paths

This tests mathematical interactivity, graphical manipulation and exact versus inexact differentials.

## Prototype C: Entropy and multiplicity

This tests probability, conceptual explanation and one of the hardest topics in the course.

Each prototype should include:

- Student notebook.
- Instructor version.
- Short problem set.
- Conceptual pre/post questions.
- Automated physics checks.
- Published static version.
- Browser-runnable experiment where practical.

Test these with a small group before designing the remainder. Measure where students stop, which controls they ignore, what predictions they make and whether they can explain the result without referring to the animation.

---

# 11. Reference spine

A useful set of reference roles would be:

- **Blundell & Blundell, _Concepts in Thermal Physics_** — broad undergraduate spine; Cambridge explicitly uses it as its main course text.  
  Reference: [University of Cambridge — Thermodynamics](https://www-teach.phy.cam.ac.uk/students/courses/thermodynamics/80)

- **Schroeder, _An Introduction to Thermal Physics_** — accessible student-facing explanations and problems.

- **Callen, _Thermodynamics and an Introduction to Thermostatistics_** — precise thermodynamic structure.

- **Reif, _Fundamentals of Statistical and Thermal Physics_** — detailed statistical reasoning.

- **Kardar, _Statistical Physics of Particles_** — advanced and graduate extensions.

- **David Tong’s statistical physics notes** — clean supplementary exposition from Cambridge.  
  Reference: [David Tong — Statistical Physics](https://www.damtp.cam.ac.uk/user/tong/statphys.html)

Use multiple references rather than following one book page by page. Different texts are strongest at different layers of the subject.

---

# The central design principle

The environment should repeatedly ask:

> **How does predictable macroscopic behaviour emerge from uncertain microscopic behaviour?**

That question can unify ideal gases, entropy, ensembles, thermodynamic potentials, radiation, phase transitions, quantum statistics and transport. It gives the course a coherent intellectual story rather than making thermodynamics feel like a collection of unrelated identities.
