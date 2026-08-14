---
title: The Fourier transform and convolution
short_title: 04 · Fourier transform
module: 04-fourier-transform
objectives:
  - id: OBJ-04-1
    text: State the transform pair — forward integral of f(t) e^(-i omega t) dt, inverse (1/2 pi) times the integral of F(omega) e^(+i omega t) d omega — derive it as the T to infinity limit of the series, and say where the course phasor lands in the spectrum.
  - id: OBJ-04-2
    text: Use the pair zoo (rect and sinc, Gaussian and Gaussian, one-sided exponential and Lorentzian, comb and comb) to sketch spectra without evaluating an integral.
  - id: OBJ-04-3
    text: State and apply the convolution theorem in both directions — convolving in time multiplies spectra, multiplying in time convolves them.
  - id: OBJ-04-4
    text: Use Delta t times Delta omega >= 1/2 to estimate bandwidth from duration and duration from bandwidth, and name the shape that achieves equality.
  - id: OBJ-04-5
    text: Compute a correctly scaled spectrum of sampled data with the FFT and diagnose aliasing, spectral leakage, and what zero-padding does and does not buy.
  - id: OBJ-04-6
    text: Explain what the complex phase of a spectrum carries, and why reconstructing a signal from its magnitude spectrum alone fails.
---

# The Fourier transform and convolution

(04-fourier-transform-puzzle)=
## The puzzle: what frequency is a hand-clap?

A whistle has a pitch. Ask anyone to hum it back and they can. A hand-clap has no pitch at all —
nobody has ever hummed a clap — and yet a microphone and an FFT will report that the clap
contains energy at *every* frequency from a few hertz to well past the top of your hearing.

That should be uncomfortable. Module 03 was built entirely on periodicity: a signal repeats with
period $T$, and only the harmonics of $2\pi/T$ are allowed. A clap never repeats. There is no
$T$, so there are no harmonics, so there is no comb — and yet the spectrum is not empty. It is
fuller than any musical note's.

:::{important} The question
What is the frequency content of something that never repeats? And if the answer is "a
continuum", what happened to the discrete comb of module 03 — where did the gaps between the
harmonics go?
:::

The second version of the puzzle is sitting in the air around you. Hundreds of radio stations
broadcast simultaneously into the same volume of space, and the total field at your antenna is a
single messy voltage against time. Somehow a receiver pulls one station out of that. Whatever
lets it do so is what this module builds.

(04-fourier-transform-predict)=
## Predict before you calculate

Commit to an answer for each of these *before* running anything. Write them down.

1. A pulse is made half as long, keeping its shape. Its spectrum becomes wider, narrower, or
   stays the same — and by what factor?
2. Two recordings have *identical* magnitude spectra, $|F(\omega)|$ the same at every frequency.
   Must they be the same signal? If not, how different can they be?
3. A 60 Hz sine wave is sampled 100 times a second. What frequency does the recorded data
   appear to show, and is there anything in the data that warns you?
4. Is there a signal that is both very short in time *and* very narrow in frequency? If not, is
   that a limitation of our instruments or something stronger?

:::{note} Why we ask first
Question 4 is the one worth arguing about before you know the answer, because the honest reply
is stronger than most people expect: it is not that short-and-narrow signals are hard to build,
it is that the words describe nothing. Question 2 quietly decides whether a spectrum is a
complete description of a signal or only half of one.
:::

(04-fourier-transform-explore)=
## Explore the model

The laboratory gives you a pulse sculptor: choose a shape, set its width, add a chirp, and watch
the signal and its spectrum side by side with the analytic pair drawn over the numerics. A
sampling control lets you make the grid too coarse on purpose, and a live meter reports
$\Delta t_{\text{rms}} \Delta\omega_{\text{rms}}$ against the floor it is not allowed to cross.

:::{figure} ../media/fourier-uncertainty.mp4
:width: 100%

A Gaussian pulse squeezed in time while its spectrum widens by exactly the reciprocal factor.
The shaded bands are the RMS widths in each domain, and the gauge along the top carries their
product against the line at $\tfrac12$. Both panels keep fixed axes throughout: if either
rescaled itself, narrowing in time would stop looking like widening in frequency. The marker
never leaves the line, in either direction of the sweep — that is the theorem, not an
illustration of it.
:::

:::{figure} ../media/fourier-aliasing-wheel.mp4
:width: 100%

A wheel filmed by a strobe. The true rotation rate ramps up from rest; the strobed marker
follows it, slows, freezes when the two rates match, and then turns *backwards* while the wheel
itself keeps speeding up. Every flash adds a point to the diagram on the right, so the
characteristic folding is measured by the wheel rather than asserted beside it. Nothing in the
strobed record reveals that anything has gone wrong.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** square-integrable real signals and their complex spectra; numerically, $N$ samples at spacing $\Delta t$ and the discrete spectrum computed from them.
- **Dynamics:** none — a change of representation; convolution models the action of a linear time-invariant system when it is used that way.
- **Boundary:** signals decay at large $|t|$ or are windowed to a finite record, and the discrete transform silently imposes periodicity on whatever window it is given.
- **Ensemble:** deterministic; noise appears only in the measurement cells, where it is Gaussian, independent and seeded.
- **Ignored:** the rigour of distribution theory — delta functions are used operationally and flagged where they appear — and convergence pathologies beyond piecewise-smooth signals.
- **Valid when:** the signal's content lies below the Nyquist frequency $\pi/\Delta t$, and the record is long compared with the features being resolved.
- **Failure modes:** aliasing, spectral leakage read as physics, reasoning from the magnitude spectrum alone, and dropping either the $1/2\pi$ or the sign of the forward transform.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 04 — the Fourier transform](/lite/lab/index.html?path=en/labs/04-fourier-transform.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/04-fourier-transform.ipynb`.
:::

Run the laboratory now, then come back. Three things are worth doing before you read on:

- Sweep the pulse width across two decades and watch the product meter rather than the curves.
  Find a shape that beats $\tfrac12$. You will not.
- Load the chirp and the plain pulse that share a magnitude spectrum, and look at them in the
  time domain. Then decide what question 2 above was really asking.
- Push a tone slowly up through the Nyquist frequency with the sampling control on, and watch
  the peak turn around and come back down.

(04-fourier-transform-derive)=
## Derive the result

**Letting the period go to infinity.** A signal that never repeats can be treated as one that
repeats after a very long time — and then the time is sent to infinity. Start from module 03's
pair, with $\omega_0 = 2\pi/T$ the spacing between neighbouring harmonics, and define

$$
F(n\omega_0) \equiv T\, c_n = \int_{T} f(t)\, e^{-\ii n \omega_0 t}\,\mathrm{d}t .
$$

The synthesis sum then reads $f(t) = \sum_n \frac{1}{T} F(n\omega_0)\, e^{\ii n \omega_0 t}$,
and writing $1/T = \omega_0/2\pi = \Delta\omega/2\pi$ turns it into

$$
f(t) = \frac{1}{2\pi}\sum_{n} F(n\omega_0)\, e^{\ii n \omega_0 t}\, \Delta\omega .
$$

That is a Riemann sum. As $T \to \infty$ the spacing $\Delta\omega$ goes to zero, the comb of
allowed frequencies fills in, and the sum becomes an integral.

:::{admonition} The Fourier transform pair
:class: theorem
$$
F(\omega) = \int_{-\infty}^{\infty} f(t)\, e^{-\ii\omega t}\,\mathrm{d}t,
\qquad
f(t) = \frac{1}{2\pi}\int_{-\infty}^{\infty} F(\omega)\, e^{+\ii\omega t}\,\mathrm{d}\omega .
$$
<!-- sign-convention-exception -->

The forward transform carries the minus sign — the same sign `numpy.fft` uses, and the one
[the conventions page](../conventions.md) fixes for the whole course. The $1/2\pi$ sits on the
inverse alone, which is what keeps $F(0) = \int f\,\mathrm{d}t$ equal to the signal's area.
:::

The comb has become a continuum, and that answers the puzzle. A clap has no harmonics because it
has no period; it has a continuous *density* of frequency content instead, and $F(\omega)$ is
that density. Asking "what frequency is a clap" presumes a comb with one tooth. The well-posed
replacement is "what does its spectrum look like", and the answer is: broad, because it is
short.

**Where the phasor lands.** Module 00 attached the phasor $\hat{x} = A e^{-\ii\varphi}$ to the
time factor $e^{-\ii\omega_0 t}$. Under the forward transform above, that clockwise factor lives
at *negative* frequency. Writing a real cosine as the two exponentials module 00 already
identified,

$$
x(t) = \Real\!\left[\hat{x}\,e^{-\ii\omega_0 t}\right]
     = \tfrac12 \hat{x}\, e^{-\ii\omega_0 t} + \tfrac12 \hat{x}^{*}\, e^{+\ii\omega_0 t},
$$

and transforming term by term with the sifting property of the delta function,

$$
F(\omega) = \pi\hat{x}\,\delta(\omega + \omega_0)
          + \pi\hat{x}^{*}\,\delta(\omega - \omega_0) .
$$

:::{admonition} The delta function, used operationally
:class: model-assumption
$\delta(\omega)$ is not a function; it is defined by what it does inside an integral,
$\int g(\omega)\delta(\omega - a)\,\mathrm{d}\omega = g(a)$. Everything this course does with it
is legitimate, and none of it is proved here. The rigorous object is a distribution, and the
theory is worth meeting eventually — but not before the physics that motivates it.
:::

So the course phasor sits at $-\omega_0$ and its conjugate at $+\omega_0$. This is not an
artefact to be tidied away. A real signal *must* have $F(-\omega) = F(\omega)^{*}$ — that is
exactly the condition for the inverse transform to come out real — so the two halves are not
independent, and neither is redundant. Delete the negative half and invert, and you do not
recover the signal: you get a complex object whose real part is half the original. That object
has a name, the analytic signal, and it is the subject of the advanced section.

**The pair zoo.** Four transforms do most of the work in this course, and each is worth deriving
once so that it can be recognised forever.

*Rectangle and sinc.* A pulse of height 1 and full width $a$, centred on $t = 0$:

$$
F(\omega) = \int_{-a/2}^{a/2} e^{-\ii\omega t}\,\mathrm{d}t
          = \frac{2\sin(\omega a/2)}{\omega}
          = a\,\operatorname{sinc}\!\left(\frac{\omega a}{2}\right),
$$

with zeros wherever $\omega a/2$ is a multiple of $\pi$. Halve the pulse width and every zero
moves twice as far out: the spectrum is stretched by exactly the factor the pulse was squeezed.
Module `29-fraunhofer` meets this same curve on a screen, with a slit in place of $a$.

*Gaussian and Gaussian.* For $f(t) = e^{-t^2/2\sigma^2}$, completing the square in the exponent
gives

$$
F(\omega) = \sqrt{2\pi}\,\sigma\, e^{-\sigma^2\omega^2/2} .
$$

A Gaussian of width $\sigma$ transforms to a Gaussian of width $1/\sigma$. It is the only shape
in the zoo that keeps its form, and — not coincidentally — the one that meets the bandwidth
theorem with equality.

*One-sided exponential and Lorentzian.* A decay switched on at $t = 0$,
$f(t) = e^{-t/\tau}$ for $t \ge 0$ and zero before:

$$
F(\omega) = \int_{0}^{\infty} e^{-t/\tau}\,e^{-\ii\omega t}\,\mathrm{d}t
          = \frac{1}{1/\tau + \ii\omega},
$$

whose magnitude is a Lorentzian of half-width $1/\tau$. This is module 02's resonance curve
again, and the statement it makes is the one physicists call the linewidth-lifetime relation: a
state that decays quickly has a broad line. It returns as the laser linewidth of module
`45-lasers` and the cavity line of module `26-fabry-perot`.

*Comb and comb.* A train of impulses spaced $T$ apart transforms to a train of impulses spaced
$2\pi/T$ apart. Module 03 has already proved it: the comb is periodic, so it has a Fourier
series, and every one of its coefficients is $1/T$ — equal weight on every harmonic. Fine
spacing in time means coarse spacing in frequency, and this pair is the engine of the sampling
discussion below.

**The convolution theorem.** Define the convolution
$(f * g)(t) = \int f(\tau) g(t - \tau)\,\mathrm{d}\tau$ — one signal smeared with the shape of
the other. Transform it, swap the order of integration, and substitute $u = t - \tau$:

$$
\int\!\!\int f(\tau) g(t-\tau) e^{-\ii\omega t}\,\mathrm{d}\tau\,\mathrm{d}t
= \int f(\tau) e^{-\ii\omega \tau}\,\mathrm{d}\tau \int g(u) e^{-\ii\omega u}\,\mathrm{d}u .
$$

:::{admonition} The convolution theorem
:class: theorem
Convolution in one domain is multiplication in the other:
$\mathcal{F}[f * g] = F \cdot G$, and $\mathcal{F}[f \cdot g] = \frac{1}{2\pi} F * G$.

Both directions earn their keep. The first says that any linear time-invariant system — a
filter, a lens, an instrument — acts by multiplying the spectrum, which is why frequency
response is a useful idea at all. The second says that multiplying a signal in time smears its
spectrum, which is where sampling and windowing get their consequences.
:::

**Parseval.** Taking the conjugate of the inverse transform and substituting once gives

$$
\int_{-\infty}^{\infty} |f(t)|^2\,\mathrm{d}t
= \frac{1}{2\pi}\int_{-\infty}^{\infty} |F(\omega)|^2\,\mathrm{d}\omega .
$$

The energy is the same whichever way you count it. That is what licenses reading a spectrum
panel as an energy budget rather than as a picture.

**The bandwidth theorem.** Define the RMS widths as the second moments of $|f|^2$ and $|F|^2$
about their centroids. Then, for every signal,

:::{admonition} Duration times bandwidth has a floor
:class: theorem
$$
\Delta t_{\text{rms}}\,\Delta\omega_{\text{rms}} \ge \tfrac12 ,
$$

with equality if and only if the signal is a Gaussian. Short and broadband are the same
statement; there is no signal that is both brief and pure.
:::

This is a theorem, not an engineering limit, and it is the same inequality — with different
names on the axes — as the coherence length of module `27-coherence`, the divergence of a
focused beam in module `43-gaussian-beams`, and the position-momentum uncertainty of quantum
mechanics. A femtosecond laser pulse of 10 fs duration cannot have a linewidth narrower than
about $5 \times 10^{13}$ rad/s, which is why ultrafast lasers are necessarily broadband.

**The bridge to sampled data.** Every measurement is a finite list of numbers, and two things
happen on the way there — both of them corollaries of the convolution theorem.

*Sampling multiplies by a comb.* Recording at spacing $\Delta t$ multiplies the signal by an
impulse train, so by the convolution theorem the spectrum is *convolved* with a comb: it is
copied, endlessly, at spacing $2\pi/\Delta t$. If the signal's content is confined below
$\omega_{\text{Nyq}} = \pi/\Delta t$ the copies do not overlap and nothing is lost. If it is
not, the copies overlap and add, and content above Nyquist reappears folded down below it,
indistinguishable from content that was genuinely there.

:::{admonition} Sampling represents the continuous signal
:class: model-assumption
Every claim made from sampled data assumes the samples stand for the signal between them. The
assumption has a sharp edge — content must lie below $\pi/\Delta t$ — and no amount of care with
the data can detect a violation after the fact. Aliasing is not noise, and it does not look like
an error: it looks like a clean peak at the wrong frequency.
:::

*A finite record multiplies by a rectangle.* Recording for a finite time multiplies by a rect,
so the spectrum is convolved with that rect's transform, a sinc. A pure tone therefore appears
not as a spike but as a sinc, with sidelobes that spill across neighbouring frequencies. This is
**spectral leakage**, and its width is set by the record length: $\Delta\omega \sim 2\pi/T$.
Leakage is a property of your window, not of the signal, which is why it is a mistake to read
structure in the sidelobes as physics.

Finally, the transform the computer actually evaluates is the discrete sum
$X_k = \sum_n x_n\, e^{-2\pi\ii k n/N}$, and multiplying it by $\Delta t$ approximates
$F(\omega_k)$ — that scaling is what `wavelab.fourier.spectrum` applies so that the analytic
pairs above can be drawn straight over the numerics. Padding the record with zeros puts more
points on the same underlying curve; it interpolates the spectrum, it does not resolve anything
new. Resolution comes from recording longer, and from nothing else.

(04-fourier-transform-verify)=
## Verify computationally

Each check below is also a test in the project's suite, so these claims cannot silently rot.

**1. The zoo against the FFT.** The Gaussian pair agrees with its closed form to $3\times
10^{-16}$ — machine precision. The rect does *not*, and the reason is the same smoothness story
module 03 told: a sampled discontinuity costs accuracy, and the error here falls only as
$\Delta t$, measured at $2.4\times10^{-2}$, $1.2\times10^{-2}$ and $5.9\times10^{-3}$ as the
grid is halved twice. Zero-padding does not repair it, because padding interpolates the
transform of the *sampled* rect rather than converting it into the continuous sinc.

**2. The round trip.** `inverse_spectrum(spectrum(f))` returns the signal to $3\times10^{-16}$,
and Parseval balances to one part in $10^{13}$.

**3. Where the phasor lands.**

:::{admonition} The measured location of the phasor
:class: numerical-observation
For $x(t) = \Real[\hat{x} e^{-\ii\omega_0 t}]$ the computed spectrum returns exactly $\pi\hat{x}$
at $-\omega_0$ and $\pi\hat{x}^{*}$ at $+\omega_0$, to fifteen digits, with leakage elsewhere at
the $5\times10^{-15}$ level — *provided* $\omega_0$ lands exactly on a grid frequency. Placed
between two grid points the same cosine reads about a fifth low at the nearest bin, with the
missing energy spread across the rest of the axis. That is not an error in the transform. It is
leakage, arriving uninvited in the simplest possible example, and it is worth meeting here
rather than in a measurement that matters.
:::

**4. The convolution theorem.** The spectrum of a numerically convolved pair matches the product
of their spectra to a relative $4\times10^{-16}$.

**5. The bandwidth floor.** RMS products are measured across shapes. The Gaussian returns
$0.500000$; a chirped Gaussian, whose $|f|^2$ is *identical* to the plain one, returns more —
the excess coming entirely from phase. No shape returns less.

(04-fourier-transform-transfer)=
## Transfer the idea

- **Impulse response (module `05-impulse-response`).** The transform of a system's Green
  function *is* its frequency response. The convolution theorem is what turns "integrate the
  response to every past kick" into "multiply by a curve", and it is the reason engineers speak
  of systems in the frequency domain at all.
- **Wave packets (modules `12-wave-packets`, `13-dispersion`).** The same theorem with $x$ and
  $k$ in place of $t$ and $\omega$: a packet localised in space is a superposition spread in
  wavenumber, and the bandwidth theorem becomes the statement that a short pulse must spread.
- **Coherence (module `27-coherence`).** A source's spectral width sets how long its
  interference fringes survive. Coherence time is $1/\Delta\omega$, which is the bandwidth
  theorem wearing an optics costume.
- **Diffraction (module `29-fraunhofer`).** The far-field pattern of an aperture is the Fourier
  transform of the aperture. The zoo becomes hardware: a slit gives a sinc, a Gaussian beam
  gives a Gaussian, a grating gives a comb.
- **Every later laboratory.** The spectrum panel in each of them is this module's `spectrum()`
  call, with this module's scaling and this module's caveats.

:::{admonition} Convolution
:class: definition
The **convolution** of two signals, $(f*g)(t) = \int f(\tau)g(t-\tau)\,\mathrm{d}\tau$, is what
you get by smearing one with the shape of the other. Every linear time-invariant system acts on
its input by convolution, and every convolution becomes a multiplication in the frequency
domain. When a course later says "the image is the object convolved with the point spread
function", this is the operation being named.
:::

(04-fourier-transform-quiz)=
## Check your understanding

```{include} ../_generated/quiz-04-fourier-transform.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](04-fourier-transform-problems.md).

(04-fourier-transform-explain)=
## Explain it in your own words

Answer in a few sentences each. These are the questions that reveal whether the ideas landed;
no number will save you.

1. Why is "what frequency is a hand-clap?" the wrong question, and what is the right one? Your
   answer should say what changed between module 03 and this one.
2. A piano note's character depends heavily on how it is struck, yet the magnitude spectrum of
   the sustained part barely changes. Where in the transform does the attack live?
3. Explain aliasing to a film-maker who has noticed that wagon wheels sometimes turn backwards,
   without using the words Fourier, spectrum or Nyquist.
4. A colleague reports a sharp spectral peak measured from a two-second recording and claims it
   resolves two lines 0.1 Hz apart. Which model-specification bullet should you point at, and
   what would you ask them to do?

(04-fourier-transform-advanced)=
## Advanced: one-sided signals, windows, and the spectrogram

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section.
:::

**The analytic signal.** Keeping only one half of a real signal's spectrum and inverting gives a
complex signal whose real part is half the original and whose magnitude is the original's
envelope — an extremely convenient object for anything that has an envelope and a carrier. Under
the course convention the half to keep is the *negative*-frequency one, because that is where
the clockwise phasor $e^{-\ii\omega_0 t}$ lives; engineering texts, rotating the other way, keep
the positive half and call the same object by the same name. This closes the thread module 00
opened in its own advanced section, and the two conventions describe identical physics with
mirrored bookkeeping.

**Windows, and what they cost.** Leakage comes from the abrupt ends of a finite record, so it
can be reduced by tapering them — multiplying by a window that goes smoothly to zero, such as
the Hann window. The sidelobes drop by orders of magnitude. The cost is paid in the main lobe,
which roughly doubles in width: leakage control is bought with resolution, one for the other,
and no window escapes the trade. It is module 03's Fejér sum in a new domain, making the same
bargain.

:::{admonition} Is there a best window?
:class: open-question
There is no universally optimal window, and the literature contains dozens, each optimal against
a different figure of merit — narrowest main lobe, lowest first sidelobe, fastest sidelobe
decay, least scalloping loss. Which to use is a question about what you intend to measure, and
answering it well is a genuine skill rather than a lookup.
:::

**Trading one for the other, deliberately.** The bandwidth theorem forbids perfect resolution in
both domains at once, but it does not forbid *choosing* where to spend the budget. Cut a long
record into short overlapping pieces, transform each, and stack the results into a
time-frequency image: the spectrogram. Short pieces give sharp timing and blurred frequency;
long pieces the reverse. Every spectrogram you have ever seen is a choice about that trade, made
explicit in the length of one window, and the theorem above is the reason the choice cannot be
avoided.
