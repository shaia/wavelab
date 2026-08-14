---
title: Problem set — the Fourier transform and convolution
short_title: 04 · Problems
---

# Problem set: the Fourier transform and convolution

Exam-style problems. Work them with a pen before touching a computer; the last three are meant
to be finished numerically. Solutions and marking rubrics live with the instructor material and
are deliberately not on this site.

Throughout, the course convention holds: the forward transform is
$F(\omega) = \int f(t)\, e^{-\ii\omega t}\,\mathrm{d}t$, and the inverse carries the opposite
sign together with the $1/2\pi$ — see [the conventions page](../conventions.md). RMS widths are
second moments of $|f|^2$ and $|F|^2$ about their centroids.

## Problem 1 — the Gaussian pair, honestly

<!-- objectives: OBJ-04-1, OBJ-04-4 -->

(a) Transform $f(t) = e^{-t^2/2\sigma^2}$ by completing the square in the exponent, and obtain
$F(\omega) = \sqrt{2\pi}\,\sigma\,e^{-\sigma^2\omega^2/2}$. State clearly where you used the
standard Gaussian integral and why the shift into the complex plane is legitimate.

(b) Compute $\Delta t_{\text{rms}}$ and $\Delta\omega_{\text{rms}}$ for this pair. Show that
each is smaller than the width of the curve it describes by a factor of $\sqrt{2}$, and that
their product is exactly $\tfrac12$.

(c) Explain, without proving it, why equality singles out the Gaussian: what is special about a
function whose transform has the same shape?

## Problem 2 — the theorems that move things

<!-- objectives: OBJ-04-1, OBJ-04-2 -->

(a) Prove the scaling theorem: if $g(t) = f(at)$ for $a > 0$, then
$G(\omega) = F(\omega/a)/a$. Say in one sentence what happens to the *area* under $|F|$ and why
that had to be so.

(b) Prove the shift theorem: delaying a signal by $t_0$ multiplies its transform by
$e^{-\ii\omega t_0}$. Deduce that $|F(\omega)|$ is completely blind to when a signal happened,
and comment on what that implies for reconstructing a signal from its magnitude alone.

(c) Prove the modulation theorem: multiplying by $\cos\omega_c t$ splits the spectrum into two
copies at $\pm\omega_c$, each at half height. This is amplitude modulation, and it is how the
radio stations of the opening puzzle share the air.

(d) Using only the zoo and these three theorems — no integrals — sketch the spectra of: a
rectangular pulse of width $a$ delayed by $3a$; a Gaussian multiplied by $\cos\omega_c t$; and
two rectangular pulses of width $a$ separated by $d$.

## Problem 3 — linewidths and lifetimes

<!-- objectives: OBJ-04-2, OBJ-04-3 -->

(a) For the one-sided exponential $e^{-t/\tau}\,\Theta(t)$, show that $|F(\omega)|^2$ is a
Lorentzian and that its full width at half maximum is $2/\tau$.

(b) An excited atomic state decays with a lifetime of $2.0\ \mathrm{ns}$. What is the minimum
linewidth of the light it emits, in MHz? Compare this with the Doppler width of a room
temperature gas and say which dominates.

(c) Use Parseval to evaluate $\int_{-\infty}^{\infty} \mathrm{d}\omega/(1/\tau^2 + \omega^2)$
without contour integration.

(d) A measured line is the true lineshape convolved with the instrument's response. If both are
Lorentzian, what is the shape and width of the result? If both are Gaussian? (One of these
answers generalises easily and the other does not — say which.)

## Problem 4 — hunting the minimum product, numerically

<!-- objectives: OBJ-04-4 -->

Using `wavelab.fourier` (in the browser laboratory or locally):

(a) Build the supergaussian family $f(t) = \exp(-|t/\sigma|^{p})$ for $p$ from $1$ to $8$, and
compute $\Delta t_{\text{rms}}\Delta\omega_{\text{rms}}$ for each with `rms_widths`. Plot the
product against $p$.

(b) Confirm the minimum sits at $p = 2$ with value $\tfrac12$, and that every other member of
the family is above it. Confirm also that the product does not change when $\sigma$ does.

(c) As $p$ grows the pulse approaches a rectangle. Explain what happens to the measured product,
and why a hard-edged rectangle is a badly behaved member of this family. (Consider how the sinc
tails contribute to the second moment of $|F|^2$.)

## Problem 5 — leakage on trial

<!-- objectives: OBJ-04-5, OBJ-04-3 -->

Using `wavelab.fourier`:

(a) Take a pure cosine whose frequency lands exactly on a grid frequency of your record, and
compute its spectrum. Then shift the frequency by half a grid spacing and recompute. Report the
peak height in both cases and describe where the missing energy went.

(b) Repeat with a Hann window applied to the record. Report the sidelobe level and the main-lobe
width in both cases, and state the trade in one sentence.

(c) Show that zero-padding the record by a factor of eight makes the plotted spectrum smoother
but does not separate two tones that were unresolved before. Then find, by experiment, the
record length that does separate two tones $1.5$ grid spacings apart, and compare it with
$2\pi/\Delta\omega$.

## Problem 6 — challenge: putting the samples back together

<!-- objectives: OBJ-04-5, OBJ-04-6 -->

(a) Implement sinc interpolation: reconstruct a continuous signal from samples taken at spacing
$\Delta t$ by summing $\operatorname{sinc}$ functions centred on each sample. Verify that for a
signal band-limited below Nyquist the reconstruction is exact to machine precision at points
*between* the samples, not merely at them.

(b) Break it. Feed the same routine a chirp that sweeps up through the Nyquist frequency, and
plot reconstruction against truth. Explain the failure in terms of the comb picture, and say
precisely at what moment the reconstruction stops being recoverable.

(c) Take any signal, keep $|F(\omega)|$, replace every phase by a random one, and invert.
Compare with the original. Then do the reverse — keep the phases and flatten every magnitude to
one — and compare again. Which reconstruction is more recognisable, and what does the pair of
experiments say about where a signal's information actually sits?
