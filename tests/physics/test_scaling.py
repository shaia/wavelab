"""Accuracy category 4: large-N scaling.

Two scaling laws anchor Milestone 1. Random-phase phasors add like a random walk — the
resultant amplitude grows as sqrt(N), so intensity grows as N — which is why incoherent
sources add in intensity while coherent ones add in amplitude. And averaging N independent
noisy measurements shrinks the scatter of a fitted parameter as N^(-1/2).
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import coupled, fourier, measurement, oscillators, phasors
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


def test_quality_factor_is_invariant_under_uniform_scaling():
    """Scale (m, k, b) together by alpha and nothing about the response changes shape.

    Q is the only dimensionless number the driven oscillator has, so a scaling that leaves it
    alone must leave the whole normalised response alone. That is why the course can talk
    about "a Q = 10 system" without naming a mass.
    """
    damping = 0.4
    reference = oscillators.quality_factor(MASS, STIFFNESS, damping)
    for alpha in (0.1, 3.0, 250.0):
        scaled = oscillators.quality_factor(
            alpha * MASS, alpha * STIFFNESS, alpha * damping
        )
        assert np.isclose(scaled, reference, rtol=1e-12)
        assert np.isclose(
            oscillators.natural_frequency(alpha * MASS, alpha * STIFFNESS), OMEGA0, rtol=1e-12
        )


def test_response_curves_collapse_onto_one_at_fixed_q():
    """Plotted as |X| k / F0 against omega/omega0, every oscillator of a given Q is the same
    curve — the reason a single figure on the module page can stand for all of them."""
    ratio = np.linspace(0.05, 2.5, 601)
    curves = []
    for mass, stiffness, damping in ((0.5, 8.0, 0.4), (2.0, 32.0, 1.6), (0.05, 0.8, 0.04)):
        omega0 = oscillators.natural_frequency(mass, stiffness)
        response = oscillators.steady_state_response(
            ratio * omega0, mass, stiffness, damping, 1.0
        )
        curves.append(np.abs(response) * stiffness)
    for other in curves[1:]:
        assert np.allclose(other, curves[0], rtol=1e-10)


def test_half_power_bandwidth_narrows_as_one_over_q():
    """Delta omega = omega0 / Q: doubling Q halves the width. Measured off swept curves, so
    it is the bandwidth *estimator* being held to the law, not just the algebra."""
    # Q >= 10 throughout: the half-power width of |X| is gamma only in the high-Q limit, and
    # its O(1/Q^2) bias reaches 0.5% at Q = 10 (see q_from_bandwidth). Reaching lower would
    # test the approximation's failure, which test_limits already does deliberately.
    qs, widths = [], []
    for damping in (0.025, 0.05, 0.1, 0.2):
        omegas = np.linspace(0.5 * OMEGA0, 1.5 * OMEGA0, 200_001)
        amplitude = np.abs(
            oscillators.steady_state_response(omegas, MASS, STIFFNESS, damping, 1.0)
        )
        qs.append(oscillators.quality_factor(MASS, STIFFNESS, damping))
        widths.append(OMEGA0 / oscillators.q_from_bandwidth(omegas, amplitude))
    assert abs(scaling_exponent(qs, widths) - (-1.0)) < 0.02
    for q, width in zip(qs, widths, strict=True):
        assert np.isclose(width, OMEGA0 / q, rtol=1e-2)


def test_ringdown_length_grows_linearly_with_q():
    """Struck once, a high-Q oscillator rings for about Q/pi periods before dropping to 1/e.

    The amplitude envelope is e^{-gamma t/2}, so the 1/e time is 2/gamma = 2Q/omega0, which
    is Q/pi periods — the "a wine glass rings for thousands of cycles" intuition, measured.
    """
    qs, cycles = [], []
    for damping in (0.05, 0.1, 0.2, 0.4):
        gamma = oscillators.damping_rate(MASS, damping)
        t = np.linspace(0.0, 8.0 / gamma, 200_001)
        x = oscillators.damped_position(t, MASS, STIFFNESS, damping, 0.1, 0.0)
        # A running maximum taken from the right is the decaying upper envelope: |x| itself
        # touches zero every half period, so reading a threshold crossing off |x| would time
        # the first zero crossing, not the decay. The staircase is then fitted rather than
        # thresholded, so the answer is not quantised to half a period.
        envelope = np.maximum.accumulate(np.abs(x)[::-1])[::-1]
        # The last period of the running max sits below the true envelope — there is no
        # later peak for it to hold — so it is dropped before fitting the e-folding time.
        usable = t <= t[-1] - 2.0 * np.pi / OMEGA0
        slope = float(np.polyfit(t[usable], np.log(envelope[usable]), 1)[0])
        decay_time = -1.0 / slope
        qs.append(oscillators.quality_factor(MASS, STIFFNESS, damping))
        cycles.append(decay_time / (2.0 * np.pi / OMEGA0))
    assert abs(scaling_exponent(qs, cycles) - 1.0) < 0.02
    for q, cycle_count in zip(qs, cycles, strict=True):
        assert np.isclose(cycle_count, q / np.pi, rtol=0.05)


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


def test_exchange_time_falls_as_one_over_the_coupling():
    """Stiffer coupling, faster trading: T_ex goes as 1/k_c while the coupling stays weak.

    The chain of reasoning is the module's, and each link is checkable. Weak coupling splits
    the two mode frequencies by roughly omega0 k_c / k; the exchange is the beat between them,
    so its period is 2 pi over that splitting; therefore doubling the coupling halves the time.
    The exponent is measured rather than assumed.

    The range matters and is not decoration. Over k_c/k in [0.005, 0.05] the fitted exponent is
    -0.991; widen it to 0.5 and it drifts to -0.965; run it over [0.2, 2] and it reaches -0.830,
    because sqrt(k + 2 k_c) stops being linear in k_c once k_c is comparable with k. The law is
    a weak-coupling law, and a test that swept the strong regime would be testing its failure.
    """
    couplings = np.geomspace(0.005 * STIFFNESS, 0.05 * STIFFNESS, 12)
    times = []
    for coupling in couplings:
        matrices = coupled.two_mass_matrices(MASS, STIFFNESS, coupling)
        modes = coupled.normal_mode_solve(*matrices)
        times.append(coupled.exchange_time(*modes.frequencies))

    assert abs(scaling_exponent(couplings, times) - (-1.0)) < 0.05

    # The same statement without the fit: ten times the coupling, a tenth of the time.
    weak = coupled.normal_mode_solve(*coupled.two_mass_matrices(MASS, STIFFNESS, 0.005 * STIFFNESS))
    stiff = coupled.normal_mode_solve(*coupled.two_mass_matrices(MASS, STIFFNESS, 0.05 * STIFFNESS))
    ratio = coupled.exchange_time(*weak.frequencies) / coupled.exchange_time(*stiff.frequencies)
    assert np.isclose(ratio, 10.0, rtol=0.05)


def test_the_mode_splitting_estimate_holds_only_while_the_coupling_is_weak():
    """Delta omega approx omega0 k_c / k — good to a percent at k_c/k = 0.02, useless at 0.5.

    A negative control for the module's own estimate. It is derived by expanding
    sqrt(k + 2 k_c) to first order, so it must fail once k_c is not small, and the page says
    so; this pins where. Measured: 1% low at k_c/k = 0.02, 5% at 0.1, 17% at 0.5.
    """
    errors = {}
    for ratio in (0.02, 0.1, 0.5):
        matrices = coupled.two_mass_matrices(MASS, STIFFNESS, ratio * STIFFNESS)
        modes = coupled.normal_mode_solve(*matrices)
        splitting = modes.frequencies[1] - modes.frequencies[0]
        errors[ratio] = abs(splitting - OMEGA0 * ratio) / splitting

    assert errors[0.02] < 0.02
    assert errors[0.1] > 0.03
    assert errors[0.5] > 0.15
    assert errors[0.02] < errors[0.1] < errors[0.5]


def test_chains_of_every_size_collapse_onto_one_dispersion_curve():
    """omega(k) = 2 sqrt(k_s/m) |sin(k a / 2)| — the course's first dispersion relation.

    Five masses, twenty, a hundred: three different systems with three different spectra, and
    every one of their modes lands on the same curve to 1.1e-16. That collapse is what makes
    the relation worth naming. It is not a fit to a chain of some particular length; it is a
    property of the medium, and the length only decides which points on it are allowed.

    Two features are then checked because the module's quiz asks about both. At small ka the
    curve is straight, with slope c = a sqrt(k_s/m) — the wave speed, and the reason long
    waves on a chain behave like waves on a string. At k = pi/a it flattens onto
    2 sqrt(k_s/m), a hard ceiling: neighbouring masses in exact antiphase is the fastest
    arrangement a chain of springs has, and adding masses does not raise it.

    The slope is read from the lowest mode alone rather than fitted over a range. The curve
    bends downwards, so a straight-line fit over ka < 0.5 comes out 1.0% low and would be
    measuring the curvature as much as the slope. Even the lowest mode only approaches the
    slope as the chain lengthens, by (k_1 a)^2/24 = (pi/(N+1))^2/24 — 1.1% at N = 5 and
    4.0e-5 at N = 100 — and that shortfall is asserted rather than tolerated, because it is
    the same expansion the continuum limit runs on.
    """
    length = 1.0
    for n in (5, 20, 100):
        spacing = length / (n + 1)
        wavenumbers = np.arange(1, n + 1) * np.pi / length
        frequencies = coupled.chain_mode_frequencies(n, MASS, STIFFNESS)
        curve = coupled.chain_dispersion(wavenumbers, spacing, MASS, STIFFNESS)

        assert np.allclose(frequencies, curve, atol=1e-12)

        speed = spacing * np.sqrt(STIFFNESS / MASS)
        measured = frequencies[0] / wavenumbers[0]
        shortfall = (speed - measured) / speed
        assert np.isclose(shortfall, (np.pi / (n + 1)) ** 2 / 24.0, rtol=0.02)

    # The ceiling: the band edge value, approached from below and never passed.
    ceiling = 2.0 * np.sqrt(STIFFNESS / MASS)
    assert np.isclose(coupled.chain_dispersion(np.pi, 1.0, MASS, STIFFNESS), ceiling, rtol=1e-12)
    for n in (5, 20, 100, 1000):
        assert coupled.chain_mode_frequencies(n, MASS, STIFFNESS)[-1] < ceiling

    # Beyond the band edge the formula repeats rather than continuing to climb: k and
    # k + 2 pi/a displace the masses identically, so a chain cannot tell them apart.
    spacing = 0.05
    k = np.linspace(0.0, np.pi / spacing, 41)
    aliased = k + 2.0 * np.pi / spacing
    assert np.allclose(
        coupled.chain_dispersion(k, spacing, MASS, STIFFNESS),
        coupled.chain_dispersion(aliased, spacing, MASS, STIFFNESS),
        atol=1e-12,
    )


# The bandwidth theorem's scaling content: squeezing a signal in time stretches its spectrum
# by exactly the reciprocal factor, so their product is a scale-invariant number with a floor.
FOURIER_SAMPLES = 4096
FOURIER_DT = 0.01
FOURIER_TIMES = (np.arange(FOURIER_SAMPLES) - FOURIER_SAMPLES // 2) * FOURIER_DT


def test_squeezing_a_pulse_in_time_stretches_its_spectrum_by_the_same_factor():
    """The time-scaling theorem: f(a t) transforms to F(omega / a) / |a|.

    Both halves matter. The width scales, which is the part everyone remembers, and the height
    scales inversely, which is what keeps the area — the signal's zero-frequency content —
    fixed. A transform that got only the width right would pass a sketch and fail here.
    """
    sigma = 0.4
    for factor in (2.0, 4.0):
        squeezed = fourier.gaussian_pulse(FOURIER_TIMES, sigma / factor)
        omega, transform = fourier.spectrum(squeezed, FOURIER_DT)
        predicted = fourier.gaussian_spectrum(omega / factor, sigma) / factor
        assert np.max(np.abs(transform - predicted)) < 1e-10


def test_the_uncertainty_product_is_invariant_under_time_scaling():
    """Delta t times Delta omega is a pure number: it cannot depend on the clock's units."""
    products = []
    for sigma in (0.2, 0.4, 0.8):
        duration, bandwidth = fourier.rms_widths(
            fourier.gaussian_pulse(FOURIER_TIMES, sigma), FOURIER_DT
        )
        products.append(duration * bandwidth)
    for product in products:
        assert np.isclose(product, 0.5, rtol=1e-9)


def test_the_gaussian_alone_reaches_the_bandwidth_minimum():
    """Delta t Delta omega >= 1/2 for every signal, with equality for the Gaussian only.

    The chirped pulse is the sharpest of the comparisons: chirping does not touch |f|^2, so
    its duration is identical to the plain Gaussian's, and the entire excess comes from a
    spectrum broadened by phase alone. Bandwidth is not a property of the envelope.
    """
    plain = fourier.gaussian_pulse(FOURIER_TIMES, 0.4)
    chirped = plain * np.exp(1j * 3.0 * FOURIER_TIMES**2)
    beating = plain * np.cos(8.0 * FOURIER_TIMES)

    plain_product = np.prod(fourier.rms_widths(plain, FOURIER_DT))
    assert np.isclose(plain_product, 0.5, rtol=1e-9)

    for name, signal in (("chirped", chirped), ("modulated", beating)):
        product = np.prod(fourier.rms_widths(signal, FOURIER_DT))
        assert product > 0.5, f"the {name} pulse cannot beat the bound"
        assert product > plain_product
