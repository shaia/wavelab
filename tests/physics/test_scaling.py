"""Accuracy category 4: large-N scaling.

Two scaling laws anchor Milestone 1. Random-phase phasors add like a random walk — the
resultant amplitude grows as sqrt(N), so intensity grows as N — which is why incoherent
sources add in intensity while coherent ones add in amplitude. And averaging N independent
noisy measurements shrinks the scatter of a fitted parameter as N^(-1/2).
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import measurement, oscillators, phasors
from wavelab.validation import scaling_exponent

pytestmark = pytest.mark.large_n

MASS = 0.5
STIFFNESS = 8.0
OMEGA0 = oscillators.natural_frequency(MASS, STIFFNESS)


def _rms_resultants(sizes: list[int], n_seeds: int = 64) -> list[float]:
    rms = []
    for n in sizes:
        seeds = np.random.SeedSequence(42).spawn(n_seeds)
        magnitudes = [
            abs(phasors.random_phasor_sum(n, np.random.default_rng(seed)))
            for seed in seeds
        ]
        rms.append(float(np.sqrt(np.mean(np.square(magnitudes)))))
    return rms


def test_random_phasor_amplitude_grows_as_sqrt_n():
    """The resultant of N unit phasors with random phases has RMS amplitude ~ N^0.5."""
    sizes = [10, 100, 1000]
    exponent = scaling_exponent(sizes, _rms_resultants(sizes))
    assert abs(exponent - 0.5) < 0.1


def test_random_phasor_intensity_grows_as_n():
    """|sum|^2 ~ N: incoherent addition is linear in intensity, not in amplitude.

    Coherent (equal-phase) addition of the same N phasors gives amplitude N and intensity
    N^2 — the contrast the interference modules are built on, checked here exactly.
    """
    sizes = [10, 100, 1000]
    mean_intensities = [rms**2 for rms in _rms_resultants(sizes)]
    exponent = scaling_exponent(sizes, mean_intensities)
    assert abs(exponent - 1.0) < 0.2
    coherent = abs(phasors.superpose(np.ones(1000, dtype=complex)))
    assert np.isclose(coherent, 1000.0)


def test_averaging_n_records_shrinks_fit_scatter_as_inverse_sqrt_n():
    """The scatter of the fitted frequency across seeds falls as (number of averaged
    records)^(-1/2) — the N^(-1/2) law in the form every virtual laboratory relies on."""
    t = np.linspace(0.0, 8.0 * 2.0 * np.pi / OMEGA0, 1601)
    clean = oscillators.position(t, MASS, STIFFNESS, 0.1, 0.0)
    sigma = 0.03

    def fitted_omega_spread(n_averaged: int, n_trials: int = 12) -> float:
        fitted = []
        for trial_seed in np.random.SeedSequence(n_averaged).spawn(n_trials):
            rng = np.random.default_rng(trial_seed)
            records = [
                measurement.add_noise(clean, sigma, rng) for _ in range(n_averaged)
            ]
            averaged = np.mean(records, axis=0)
            fitted.append(measurement.fit_cosine(t, averaged, OMEGA0).omega)
        return float(np.std(fitted))

    sizes = [1, 4, 16]
    spreads = [fitted_omega_spread(n) for n in sizes]
    exponent = scaling_exponent(sizes, spreads)
    assert abs(exponent - (-0.5)) < 0.2


def test_reported_fit_error_shrinks_with_record_length():
    """Doubling the record twice must shrink fit_cosine's own 1-sigma frequency error;
    the covariance-based error bar has to know that more data pins omega down harder."""
    sigma = 0.02
    errors = []
    for n_periods in [4, 8, 16]:
        t = np.linspace(0.0, n_periods * 2.0 * np.pi / OMEGA0, n_periods * 200 + 1)
        rng = np.random.default_rng(7)
        noisy = measurement.add_noise(
            oscillators.position(t, MASS, STIFFNESS, 0.1, 0.0), sigma, rng
        )
        errors.append(measurement.fit_cosine(t, noisy, OMEGA0).omega_err)
    assert errors[0] > errors[1] > errors[2]
