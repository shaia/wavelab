"""Synthetic measurement noise and parameter recovery — simulation treated as experiment.

MODEL SPECIFICATION
    System:        a clean simulated signal plus additive Gaussian noise; the observables are
                   fitted parameters (amplitude, frequency, phase, offset) with uncertainties
    Dynamics:      none of its own — this module corrupts and analyses signals produced by
                   the physics modules; nothing here evolves anything
    Boundary:      not applicable; arrays in, numbers out
    Ensemble:      noise samples are independent Gaussians of one standard deviation, drawn
                   from a seeded generator passed in explicitly
    Ignored:       every structured error a real instrument has — drift, quantisation,
                   correlated noise, dead time, miscalibration, outliers
    Valid when:    the noise really is additive, independent, and Gaussian, and the model
                   being fitted really generated the underlying signal
    Failure modes: noise large enough that the fit finds a wrong local minimum (a bad
                   frequency guess is the usual cause), zero-crossing counting on strongly
                   noisy data (every wiggle near zero is a spurious crossing), non-Gaussian
                   corruption, and reading the reported 1-sigma errors as truth rather than
                   as model-conditional

The course rule this module exists to enforce: a simulated measurement is never quoted as
lambda = 632.800000 nm; it is quoted as (633 +/- 4) nm, and the uncertainty comes from here.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import curve_fit


@dataclass(frozen=True)
class CosineFit:
    """Parameters of a fitted `A cos(omega t + phi) + C`, each with its 1-sigma error.

    Normalised so `amplitude >= 0`, `omega > 0`, and `phase` lies in (-pi, pi]. The errors
    are square roots of the diagonal of the fit covariance: conditional on the model and on
    the noise being independent and Gaussian — see the module's failure modes.
    """

    amplitude: float
    omega: float
    phase: float
    offset: float
    amplitude_err: float
    omega_err: float
    phase_err: float
    offset_err: float


def add_noise(values: np.ndarray, sigma: float, rng: np.random.Generator) -> np.ndarray:
    """`values` plus independent Gaussian noise of standard deviation `sigma`."""
    if sigma < 0:
        raise ValueError("sigma must be non-negative")
    data = np.asarray(values, dtype=float)
    return data + rng.normal(0.0, sigma, size=data.shape)


def fit_cosine(
    times: np.ndarray, values: np.ndarray, omega_guess: float | None = None
) -> CosineFit:
    """Least-squares fit of `A cos(omega t + phi) + C` to a noisy signal.

    When `omega_guess` is omitted it is taken from the peak of the signal's discrete Fourier
    transform — good enough whenever the record holds at least about one full period. A
    cosine fit's other three parameters are benign; the frequency is the one with local
    minima, which is why it is the one that accepts a guess.
    """
    t = np.asarray(times, dtype=float)
    y = np.asarray(values, dtype=float)
    if t.shape != y.shape:
        raise ValueError("times and values must have the same shape")
    if t.size < 5:
        raise ValueError("need at least five samples to fit four parameters")

    if omega_guess is None:
        omega_guess = _spectral_peak_omega(t, y)
    if omega_guess <= 0:
        raise ValueError("omega_guess must be positive")

    offset0 = float(np.mean(y))
    amplitude0 = float(np.sqrt(2.0) * np.std(y))

    def model(t_, amplitude, omega, phase, offset):
        return amplitude * np.cos(omega * t_ + phase) + offset

    popt, pcov = curve_fit(
        model, t, y, p0=[amplitude0, float(omega_guess), 0.0, offset0], maxfev=10_000
    )
    errors = np.sqrt(np.diag(pcov))
    amplitude, omega, phase, offset = (float(p) for p in popt)

    # Normalise to the canonical parameter region; cos is even in (omega t + phi).
    if amplitude < 0:
        amplitude, phase = -amplitude, phase + np.pi
    if omega < 0:
        omega, phase = -omega, -phase
    phase = float(np.arctan2(np.sin(phase), np.cos(phase)))

    return CosineFit(
        amplitude=amplitude,
        omega=omega,
        phase=phase,
        offset=offset,
        amplitude_err=float(errors[0]),
        omega_err=float(errors[1]),
        phase_err=float(errors[2]),
        offset_err=float(errors[3]),
    )


def frequency_from_zero_crossings(times: np.ndarray, values: np.ndarray) -> float:
    """Estimate omega from the mean spacing of a signal's zero crossings.

    Subtracts the mean, finds sign changes, refines each crossing by linear interpolation,
    and reads consecutive crossings as half periods: omega = pi / (mean spacing). Cruder
    than `fit_cosine` and immune to its local-minimum failure — which is exactly the pair of
    properties that makes it the standard sanity check on a fit. Clean or mildly noisy
    signals only: strong noise plants spurious crossings on every approach to zero and the
    estimate collapses (see the module's failure modes).
    """
    t = np.asarray(times, dtype=float)
    y = np.asarray(values, dtype=float) - float(np.mean(values))
    if t.shape != y.shape:
        raise ValueError("times and values must have the same shape")

    sign_change = np.nonzero(np.diff(np.signbit(y)))[0]
    if sign_change.size < 2:
        raise ValueError("need at least two zero crossings; record too short?")
    fractions = y[sign_change] / (y[sign_change] - y[sign_change + 1])
    crossing_times = t[sign_change] + fractions * (t[sign_change + 1] - t[sign_change])
    half_period = float(np.mean(np.diff(crossing_times)))
    return float(np.pi / half_period)


def _spectral_peak_omega(t: np.ndarray, y: np.ndarray) -> float:
    """The angular frequency of the largest nonzero bin of the signal's rFFT."""
    dt = float(np.mean(np.diff(t)))
    spectrum = np.abs(np.fft.rfft(y - np.mean(y)))
    frequencies = np.fft.rfftfreq(y.size, d=dt)
    peak = int(np.argmax(spectrum[1:])) + 1  # skip the DC bin
    return float(2.0 * np.pi * frequencies[peak])
