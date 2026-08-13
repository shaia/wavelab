"""Harmonic analysis: Fourier series, the transform, and the DFT bridge to sampled data.

MODEL SPECIFICATION
    System:        real time-signals — periodic ones carried as coefficient arrays, aperiodic
                   ones as samples at spacing dt — together with their complex spectra
    Dynamics:      none; this module analyses and synthesises given signals rather than
                   evolving them
    Boundary:      periodic signals repeat exactly; a sampled record is treated by the DFT as
                   one period of a periodic signal, and that fiction is the central caveat
    Ensemble:      deterministic; callers add measurement noise through `wavelab.measurement`
    Ignored:       distribution-theory rigour — delta functions are used operationally — and
                   convergence questions beyond piecewise-smooth signals
    Valid when:    the signal's content lies below Nyquist (|omega| < pi/dt) and the record is
                   long against the features being resolved
    Failure modes: aliasing, spectral leakage mistaken for physics, and any attempt to
                   reconstruct a signal from the magnitude of its spectrum alone

One kernel runs the whole file. Analysis carries e^{-i omega t} and synthesis carries
e^{+i omega t}, with the 1/(2 pi) on the inverse — the `numpy.fft` sign, and the one
`constants.SIGN_CONVENTION` fixes. That choice is what lets module 04 take the T -> infinity
limit of the series and land on the transform without a sign appearing from nowhere.

It has a consequence worth stating rather than hiding. The course phasor of module 00 is
x_hat = A e^{-i phi}, attached to a time factor e^{-i omega t}; under the kernel above that
factor is the *negative*-frequency half. So the nth harmonic's phasor is 2 c_{-n} = 2 c_n^*,
and `spectrum` puts pi x_hat at -omega0 for a real cosine, not at +omega0. This is the
analytic-signal thread module 00 opens and module 04 closes, and it is a fact about the
convention, not an accident of the implementation.

Coefficient arrays are stored with an explicit offset: `c` has length 2 n_max + 1 and `c[k]`
holds the harmonic of index n = k - n_max, so `c[n_max]` is the mean and `c[n_max + n]` is
c_n. Real signals give conjugate-symmetric arrays, c_{-n} = c_n^*.
"""

from __future__ import annotations

import numpy as np


def fourier_coefficients(samples: np.ndarray, n_max: int) -> np.ndarray:
    """Complex Fourier coefficients c_n of one period, for |n| <= n_max.

    `samples` is one full period on a uniform grid that starts at t = 0 and excludes the
    endpoint, `t_j = j T / N`. On such a grid the trapezoid rule over a period is exactly the
    plain average, so this evaluates c_n = (1/T) integral f(t) e^{-i n omega0 t} dt as a mean
    with no quadrature error beyond what sampling a non-band-limited signal already costs.

    Returned in the offset layout of the module docstring: index `n_max + n` holds c_n. The
    kernel is `spectrum`'s, so for one period c_n = F(n omega0) / T — the same number the
    transform reports, divided by the period.
    """
    values = np.asarray(samples, dtype=float)
    if values.ndim != 1:
        raise ValueError("samples must be a one-dimensional record of a single period")
    if n_max < 0:
        raise ValueError("n_max must be non-negative")
    if 2 * n_max >= values.size:
        raise ValueError(
            "n_max must stay below half the sample count — harmonics at or above the "
            "Nyquist index alias onto lower ones and cannot be recovered"
        )

    count = values.size
    orders = np.arange(-n_max, n_max + 1)
    positions = np.arange(count)
    kernel = np.exp(-2j * np.pi * np.outer(orders, positions) / count)
    return kernel @ values / count


def partial_sum(c: np.ndarray, omega0: float, t: np.ndarray) -> np.ndarray:
    """The signal rebuilt from its coefficients, Re[sum_n c_n e^{+i n omega0 t}].

    The real part is taken because the physical signal always is one — module 00's rule. For
    the conjugate-symmetric arrays a real signal produces, the imaginary part is zero to
    roundoff anyway and the projection costs nothing.
    """
    coefficients = np.asarray(c, dtype=complex)
    if coefficients.ndim != 1 or coefficients.size % 2 == 0:
        raise ValueError("c must be a one-dimensional array of odd length, 2 n_max + 1")
    if omega0 <= 0:
        raise ValueError("omega0 must be positive")

    n_max = (coefficients.size - 1) // 2
    orders = np.arange(-n_max, n_max + 1)
    time = np.asarray(t, dtype=float)
    phases = np.exp(1j * omega0 * np.outer(orders, time))
    return np.real(coefficients @ phases)


def square_coefficients(n_max: int) -> np.ndarray:
    """Coefficients of the unit square wave sign(sin omega0 t): c_n = 2/(i pi n), odd n only.

    Odd harmonics with 1/n decay — the slowest decay in this file, and the price of a jump.
    """
    orders = _orders(n_max)
    c = np.zeros(orders.size, dtype=complex)
    odd = orders % 2 != 0
    c[odd] = 2.0 / (1j * np.pi * orders[odd])
    return c


def triangle_coefficients(n_max: int) -> np.ndarray:
    """Coefficients of the unit triangle wave (2/pi) arcsin(sin omega0 t).

    Odd harmonics again, but decaying as 1/n^2: the waveform has no jump, only a corner, and
    each extra degree of smoothness buys one more power of 1/n.
    """
    orders = _orders(n_max)
    c = np.zeros(orders.size, dtype=complex)
    odd = orders % 2 != 0
    n = orders[odd]
    c[odd] = 4.0 * (-1.0) ** ((np.abs(n) - 1) // 2) * np.sign(n) / (1j * np.pi**2 * n**2)
    return c


def sawtooth_coefficients(n_max: int) -> np.ndarray:
    """Coefficients of the unit sawtooth ramp, t/(T/2) on one period centred at t = 0.

    Every harmonic is present, decaying as 1/n — a jump once per period, like the square, but
    without the even-harmonic cancellation that the square wave's half-wave symmetry forces.
    """
    orders = _orders(n_max)
    c = np.zeros(orders.size, dtype=complex)
    nonzero = orders != 0
    n = orders[nonzero]
    c[nonzero] = 1j * (-1.0) ** n / (np.pi * n)
    return c


def pulse_train_coefficients(duty: float, n_max: int) -> np.ndarray:
    """Coefficients of a unit pulse train of the given duty cycle, each pulse centred on t = 0.

    c_n = duty * sinc(n * duty) with the normalised sinc, so the envelope of the comb is the
    transform of one pulse — the comb-times-envelope structure module 04 rebuilds as
    rect <-> sinc, and module 31 later reads off a diffraction grating.
    """
    if not 0.0 < duty < 1.0:
        raise ValueError("duty must lie strictly between 0 and 1")
    orders = _orders(n_max)
    return (duty * np.sinc(orders * duty)).astype(complex)


def spectrum(samples: np.ndarray, dt: float) -> tuple[np.ndarray, np.ndarray]:
    """Angular-frequency axis and scaled spectrum of a sampled signal, as `(omega, F)`.

    The record is taken on a grid centred on t = 0, `t = (arange(n) - n // 2) * dt`, which is
    what makes an even signal transform to a real spectrum instead of one wrapped in a linear
    phase ramp. Output is `fftshift`ed, so `omega` runs from -pi/dt up to just below +pi/dt
    and the zero-frequency bin sits in the middle.

    Scaling by dt makes this an approximation to the continuous integral
    F(omega) = integral f(t) e^{-i omega t} dt [signal units times seconds], not a bare DFT,
    so the analytic pairs in this module overlay it directly.
    """
    values = np.asarray(samples)
    if values.ndim != 1:
        raise ValueError("samples must be a one-dimensional record")
    if values.size < 2:
        raise ValueError("samples must hold at least two points")
    if dt <= 0:
        raise ValueError("dt must be positive")

    transform = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(values))) * dt
    omega = np.fft.fftshift(np.fft.fftfreq(values.size, d=dt)) * 2.0 * np.pi
    return omega, transform


def inverse_spectrum(F: np.ndarray, dt: float) -> np.ndarray:
    """The signal behind a spectrum, inverting `spectrum` to machine precision.

    Complex on return, because the general inverse is: a conjugate-symmetric spectrum gives a
    real signal to roundoff, while the one-sided spectra of module 04's analytic-signal
    section deliberately do not. Callers holding a real signal take the real part.
    """
    values = np.asarray(F)
    if values.ndim != 1:
        raise ValueError("F must be a one-dimensional spectrum")
    if dt <= 0:
        raise ValueError("dt must be positive")
    return np.fft.fftshift(np.fft.ifft(np.fft.ifftshift(values))) / dt


def rect_pulse(t: np.ndarray, width: float) -> np.ndarray:
    """Unit rectangular pulse of the given full width, centred on t = 0."""
    if width <= 0:
        raise ValueError("width must be positive")
    time = np.asarray(t, dtype=float)
    return np.where(np.abs(time) <= width / 2.0, 1.0, 0.0)


def sinc_spectrum(omega: np.ndarray, width: float) -> np.ndarray:
    """Transform of `rect_pulse`: width * sinc(omega * width / 2), unnormalised.

    Zeros at omega = 2 pi k / width — the narrower the pulse, the wider the spacing. Module 29
    meets this same curve on a screen, where `width` is a slit and omega is an angle.
    """
    if width <= 0:
        raise ValueError("width must be positive")
    return width * np.sinc(np.asarray(omega, dtype=float) * width / (2.0 * np.pi))


def gaussian_pulse(t: np.ndarray, sigma: float) -> np.ndarray:
    """Unit-height Gaussian pulse exp(-t^2 / (2 sigma^2)), centred on t = 0."""
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    time = np.asarray(t, dtype=float)
    return np.exp(-(time**2) / (2.0 * sigma**2))


def gaussian_spectrum(omega: np.ndarray, sigma: float) -> np.ndarray:
    """Transform of `gaussian_pulse`: sqrt(2 pi) sigma exp(-sigma^2 omega^2 / 2).

    A Gaussian again, of width 1/sigma — the only shape in the zoo that transforms into
    itself, and the one that meets the bandwidth theorem with equality.
    """
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    frequency = np.asarray(omega, dtype=float)
    return np.sqrt(2.0 * np.pi) * sigma * np.exp(-(sigma**2) * frequency**2 / 2.0)


def exp_decay(t: np.ndarray, tau: float) -> np.ndarray:
    """One-sided decaying exponential e^{-t/tau} for t >= 0, zero before — a ringdown."""
    if tau <= 0:
        raise ValueError("tau must be positive")
    time = np.asarray(t, dtype=float)
    return np.where(time >= 0.0, np.exp(-np.clip(time, 0.0, None) / tau), 0.0)


def lorentzian_spectrum(omega: np.ndarray, tau: float) -> np.ndarray:
    """Transform of `exp_decay`: 1/(1/tau + i omega), of half-width 1/tau [signal units * s].

    The same complex curve as module 02's driven response, and later the linewidth of module
    27 and the cavity line of module 26 — a decay in time is a Lorentzian in frequency, and
    the faster the decay the broader the line.
    """
    if tau <= 0:
        raise ValueError("tau must be positive")
    return 1.0 / (1.0 / tau + 1j * np.asarray(omega, dtype=float))


def convolve(f: np.ndarray, g: np.ndarray, dt: float) -> np.ndarray:
    """Convolution of two sampled signals, normalised so spectra simply multiply.

    Scaled so that `spectrum(convolve(f, g, dt))` equals the product of the two spectra to
    roundoff, which is the convolution theorem in the form the rest of the course uses.

    This is *circular* convolution on the DFT's periodic extension of both records, not the
    linear convolution `numpy.convolve` computes: contributions running off one end reappear
    at the other. That is the same periodic fiction this module's boundary bullet names, and
    the fix is the usual one — pad both records with zeros until the wraparound cannot reach.
    Real inputs give a real result; a complex input anywhere gives a complex one.
    """
    first = np.asarray(f)
    second = np.asarray(g)
    if first.ndim != 1 or second.ndim != 1:
        raise ValueError("f and g must be one-dimensional records")
    if first.size != second.size:
        raise ValueError("f and g must have the same length — pad the shorter record first")
    if dt <= 0:
        raise ValueError("dt must be positive")

    product = np.fft.fft(np.fft.ifftshift(first)) * np.fft.fft(np.fft.ifftshift(second))
    result = np.fft.fftshift(np.fft.ifft(product)) * dt
    if np.isrealobj(first) and np.isrealobj(second):
        return result.real
    return result


def gibbs_overshoot(n_max: int) -> float:
    """Peak overshoot of the square wave's partial sum, as a fraction of the jump height.

    Measured, not asserted: the partial sum through harmonic `n_max` is evaluated on a grid
    fine enough to resolve its first maximum, and the excess over the true value is divided by
    the jump of 2. The answer is about 0.0895 and — this is the whole point — does not shrink
    as n_max grows. The overshoot rides in toward the discontinuity instead.

    That approach is also the trap in measuring it. The first maximum sits at roughly
    pi/(n_max + 1) of a period, so a grid fixed in absolute time misses it entirely for large
    n_max and reports a comfortable, wrong, shrinking number. The window here shrinks with
    n_max for exactly that reason.
    """
    if n_max < 1:
        raise ValueError("n_max must be at least 1 — a partial sum needs a harmonic")

    c = square_coefficients(n_max)
    # The first horn sits near pi/(n_max + 1) in phase; four times that is a window wide
    # enough to contain it whatever the parity of n_max, and narrow enough to resolve it.
    edge = 4.0 * np.pi / (n_max + 1)
    phase = np.linspace(0.0, edge, 20001)
    reconstruction = partial_sum(c, 1.0, phase)
    return float((reconstruction.max() - 1.0) / 2.0)


def rms_widths(samples: np.ndarray, dt: float) -> tuple[float, float]:
    """RMS duration and RMS bandwidth of a sampled signal, as `(dt_rms, domega_rms)` [s, rad/s].

    Each is the second moment of |f|^2 about its own centroid, in time and in angular
    frequency. Defined this way the product obeys dt_rms * domega_rms >= 1/2 for every signal,
    with equality for a Gaussian — the bandwidth theorem, and the same inequality that returns
    as coherence length in module 27 and beam divergence in module 43.
    """
    values = np.asarray(samples)
    if values.ndim != 1:
        raise ValueError("samples must be a one-dimensional record")
    if dt <= 0:
        raise ValueError("dt must be positive")

    time = (np.arange(values.size) - values.size // 2) * dt
    omega, transform = spectrum(values, dt)
    return _rms_width(time, values), _rms_width(omega, transform)


def _orders(n_max: int) -> np.ndarray:
    """The harmonic indices -n_max .. n_max of a coefficient array."""
    if n_max < 0:
        raise ValueError("n_max must be non-negative")
    return np.arange(-n_max, n_max + 1)


def _rms_width(axis: np.ndarray, values: np.ndarray) -> float:
    """Second moment of |values|^2 about its centroid along `axis`."""
    weight = np.abs(values) ** 2
    total = weight.sum()
    if total <= 0:
        raise ValueError("signal carries no energy — its width is undefined")
    centre = float((axis * weight).sum() / total)
    return float(np.sqrt(((axis - centre) ** 2 * weight).sum() / total))
