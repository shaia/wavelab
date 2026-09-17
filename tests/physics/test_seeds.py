"""Accuracy category 6: seed independence.

Stochastic results must be reproducible under a fixed seed, genuinely different across
seeds, and — the point of the category — statistically identical across independent seed
families. The final test turns the guard rail on itself: a biased measurement must FAIL the
agreement check, or the check is decoration.
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import coupled, fourier, measurement, oscillators, phasors, waves
from wavelab.validation import scaling_exponent, seed_study

pytestmark = pytest.mark.seed_independence

MASS = 0.5
STIFFNESS = 8.0
OMEGA0 = oscillators.natural_frequency(MASS, STIFFNESS)
TIMES = np.linspace(0.0, 8.0 * 2.0 * np.pi / OMEGA0, 1601)
CLEAN = oscillators.position(TIMES, MASS, STIFFNESS, 0.1, 0.0)
NOISE_SIGMA = 0.02


def _measure_omega(rng: np.random.Generator) -> float:
    noisy = measurement.add_noise(CLEAN, NOISE_SIGMA, rng)
    return measurement.fit_cosine(TIMES, noisy, OMEGA0).omega


def test_same_seed_reproduces_the_same_noise_exactly():
    first = measurement.add_noise(CLEAN, NOISE_SIGMA, np.random.default_rng(123))
    second = measurement.add_noise(CLEAN, NOISE_SIGMA, np.random.default_rng(123))
    assert np.array_equal(first, second)


def test_different_seeds_give_different_noise():
    first = measurement.add_noise(CLEAN, NOISE_SIGMA, np.random.default_rng(123))
    second = measurement.add_noise(CLEAN, NOISE_SIGMA, np.random.default_rng(124))
    assert not np.array_equal(first, second)


def test_random_phasor_sum_is_reproducible_under_a_fixed_seed():
    first = phasors.random_phasor_sum(500, np.random.default_rng(9))
    second = phasors.random_phasor_sum(500, np.random.default_rng(9))
    assert first == second


def test_fitted_frequency_agrees_with_truth_across_seeds():
    """The virtual laboratory's central claim: a noisy measurement pipeline recovers the
    true natural frequency within its scatter, whatever the seed."""
    study = seed_study(_measure_omega, n_seeds=8, base_seed=0)
    assert study.agrees_with(OMEGA0, n_sigma=3.0)
    assert study.relative_spread < 1e-3


def test_two_independent_seed_families_agree_with_each_other():
    """Statistical results must not depend on which family of seeds produced them."""
    family_a = seed_study(_measure_omega, n_seeds=8, base_seed=0)
    family_b = seed_study(_measure_omega, n_seeds=8, base_seed=10_000)
    combined_error = float(
        np.hypot(family_a.standard_error, family_b.standard_error)
    )
    assert abs(family_a.mean - family_b.mean) < 3.0 * combined_error


RINGDOWN_DAMPING = 0.1  # Q = 20
RINGDOWN_TIMES = np.linspace(0.0, 30.0 * 2.0 * np.pi / OMEGA0, 12_001)
RINGDOWN_CLEAN = oscillators.damped_position(
    RINGDOWN_TIMES, MASS, STIFFNESS, RINGDOWN_DAMPING, 0.1, 0.0
)
TRUE_Q = oscillators.quality_factor(MASS, STIFFNESS, RINGDOWN_DAMPING)


def _q_from_noisy_ringdown(rng: np.random.Generator) -> float:
    noisy = measurement.add_noise(RINGDOWN_CLEAN, 1e-3, rng)
    return oscillators.q_from_ringdown(RINGDOWN_TIMES, noisy)


def test_three_q_estimators_agree_on_noisy_data_within_one_percent():
    """Module 02's punchline as a test: measure Q three ways from noisy apparatus and get
    one number.

    Each route sees its own noisy record — a ringdown, an amplitude sweep, a phase sweep —
    so agreement here is a statement about the physics, not about shared arithmetic.

    The tolerance is a *total* uncertainty of 1%, not a 3-sigma statistical band, and that is
    the physics rather than a loosened assertion. Each estimator carries a small systematic
    bias on top of its scatter: the bandwidth route is O(1/Q^2) low because the half-power
    width of |X| is only asymptotically gamma, and the ringdown route is O(sigma^2/A^2) high
    because a noisy record's mean square is its signal's plus its noise's. At this noise
    level both biases exceed the seed-to-seed scatter, so an assertion phrased purely in
    standard errors would be testing the noise and ignoring the systematics. Separating the
    two is the lesson the laboratory teaches with the same three numbers.
    """
    omegas = np.linspace(0.5 * OMEGA0, 1.5 * OMEGA0, 4001)
    clean_response = oscillators.steady_state_response(
        omegas, MASS, STIFFNESS, RINGDOWN_DAMPING, 1.0
    )

    def q_from_noisy_sweep(rng: np.random.Generator) -> float:
        amplitude = measurement.add_noise(np.abs(clean_response), 2e-4, rng)
        return oscillators.q_from_bandwidth(omegas, amplitude)

    def q_from_noisy_phase(rng: np.random.Generator) -> float:
        phase = measurement.add_noise(np.angle(clean_response), 2e-3, rng)
        return oscillators.q_from_phase_slope(omegas, phase)

    studies = {
        "ringdown": seed_study(_q_from_noisy_ringdown, n_seeds=8, base_seed=3),
        "bandwidth": seed_study(q_from_noisy_sweep, n_seeds=8, base_seed=3),
        "phase slope": seed_study(q_from_noisy_phase, n_seeds=8, base_seed=3),
    }
    for name, study in studies.items():
        assert abs(study.mean - TRUE_Q) / TRUE_Q < 0.01, f"{name} is off by more than 1%"
        assert study.relative_spread < 0.01, f"{name} is not reproducible across seeds"

    measured = [study.mean for study in studies.values()]
    assert (max(measured) - min(measured)) / TRUE_Q < 0.01


def test_one_kick_and_its_envelope_agree_on_q_across_seeds():
    """Module 05's punchline as a test: a single ringdown yields Q twice, two different ways.

    The same noisy record is read in the time domain, where Q comes from how fast the
    envelope decays, and in the frequency domain, where it comes from how wide the line is.
    Nothing is shared between the two routes but the data, so their agreement is the
    experimental content of the module — a decay in time *is* a Lorentzian in frequency.

    The linewidth route fits the lineshape rather than interpolating half-power crossings on
    it. That is not a refinement: this record holds about eight amplitude e-foldings, which
    puts under three bins across the full width no matter what Q is, and `q_from_bandwidth`
    would happily read those bins and return a number several percent low. The band is kept
    to a few linewidths either side, where the Lorentzian is still a good description of the
    true response.

    Tolerances are total uncertainties rather than statistical bands, for the reason the
    module-02 test above sets out: each route carries a systematic larger than its scatter.
    """
    dt = 0.01
    n = 2**14
    centred = (np.arange(n) - n // 2) * dt
    clean_kick = oscillators.impulse_response(centred, MASS, STIFFNESS, RINGDOWN_DAMPING)
    gamma = oscillators.damping_rate(MASS, RINGDOWN_DAMPING)
    noise = 2e-4 * float(np.max(np.abs(clean_kick)))

    def q_from_kick_linewidth(rng: np.random.Generator) -> float:
        omega, transform = fourier.spectrum(
            measurement.add_noise(clean_kick, noise, rng), dt
        )
        band = (omega > OMEGA0 - 4.0 * gamma) & (omega < OMEGA0 + 4.0 * gamma)
        return oscillators.q_from_linewidth(omega[band], np.abs(transform[band]))

    def q_from_kick_envelope(rng: np.random.Generator) -> float:
        noisy = measurement.add_noise(clean_kick, noise, rng)
        return oscillators.q_from_ringdown(centred[n // 2 :], noisy[n // 2 :])

    linewidth = seed_study(q_from_kick_linewidth, n_seeds=8, base_seed=5)
    envelope = seed_study(q_from_kick_envelope, n_seeds=8, base_seed=5)

    for name, study in (("linewidth", linewidth), ("envelope", envelope)):
        assert abs(study.mean - TRUE_Q) / TRUE_Q < 0.02, f"{name} is off by more than 2%"
        assert study.relative_spread < 0.02, f"{name} is not reproducible across seeds"

    assert abs(linewidth.mean - envelope.mean) / TRUE_Q < 0.02


def test_ringdown_q_scatter_shrinks_as_inverse_sqrt_of_seed_count():
    """More repeats, tighter answer: the standard error of measured Q falls as M^(-1/2).

    The N^(-1/2) law from module 00, now doing the job it exists for — telling a student how
    many ringdowns to record before quoting a Q to a given precision. Note what it cannot do:
    the systematic offset the test above budgets for is untouched by any number of repeats.
    """
    counts = [4, 16, 64]
    errors = [
        seed_study(_q_from_noisy_ringdown, n_seeds=n, base_seed=11).standard_error
        for n in counts
    ]
    assert abs(scaling_exponent(counts, errors) - (-0.5)) < 0.2


def test_seed_study_detects_a_genuinely_biased_measurement():
    """The guard rail must guard: fitting a signal whose true frequency is 2% off must
    fail the agreement check against OMEGA0, loudly, or every passing test above is vacuous."""
    biased_clean = oscillators.position(TIMES, MASS, STIFFNESS * 1.04, 0.1, 0.0)

    def biased_measure(rng: np.random.Generator) -> float:
        noisy = measurement.add_noise(biased_clean, NOISE_SIGMA, rng)
        return measurement.fit_cosine(TIMES, noisy, OMEGA0).omega

    study = seed_study(biased_measure, n_seeds=8, base_seed=0)
    assert not study.agrees_with(OMEGA0, n_sigma=3.0)


# Reading a chain's modes out of one noisy record. CHAIN_* mirror the module's own numbers:
# five masses between fixed walls, one of them pulled aside and released, and the motion of
# that same mass watched for five and a half minutes.
CHAIN_SIZE = 5
CHAIN_DT = 0.02
CHAIN_SAMPLES = 8192
CHAIN_MATRICES = coupled.chain_matrices(CHAIN_SIZE, MASS, STIFFNESS)
CHAIN_MODES = coupled.normal_mode_solve(*CHAIN_MATRICES)
CHAIN_EXACT = coupled.chain_mode_frequencies(CHAIN_SIZE, MASS, STIFFNESS)
# `spectrum` reads a record centred on t = 0, and a chain released from rest moves evenly in
# time, so evaluating `evolve` on the centred grid gives a genuinely even record with no
# mirroring trick anywhere.
CHAIN_TIMES = (np.arange(CHAIN_SAMPLES) - CHAIN_SAMPLES // 2) * CHAIN_DT
CHAIN_CLEAN = coupled.evolve(
    CHAIN_MODES, np.array([1.0, 0.0, 0.0, 0.0, 0.0]), np.zeros(CHAIN_SIZE), CHAIN_TIMES
)[:, 0]


def _read_chain_modes(record: np.ndarray) -> np.ndarray:
    """The five strongest spectral peaks of a record, in ascending frequency.

    Peaks are located to sub-bin precision by the usual three-point vertex, which matters:
    the bins here are 0.038 rad/s apart and the answers are wanted to a part in a thousand.
    """
    omega, transform = fourier.spectrum(record, CHAIN_DT)
    band = (omega > 0.0) & (omega < 1.3 * CHAIN_EXACT[-1])
    magnitude, frequencies = np.abs(transform[band]), omega[band]
    peaks = [
        i
        for i in range(1, magnitude.size - 1)
        if magnitude[i] > magnitude[i - 1] and magnitude[i] > magnitude[i + 1]
    ]
    peaks.sort(key=lambda i: magnitude[i], reverse=True)
    vertex = [
        frequencies[i]
        + 0.5
        * (magnitude[i - 1] - magnitude[i + 1])
        / (magnitude[i - 1] - 2.0 * magnitude[i] + magnitude[i + 1])
        * (frequencies[1] - frequencies[0])
        for i in peaks[:CHAIN_SIZE]
    ]
    return np.array(sorted(vertex))


def test_a_random_state_decomposes_and_reassembles_whatever_the_seed():
    """Project onto the modes, evolve each one, add them up — and get the state back exactly.

    Modal decomposition is an identity, not an approximation, and the way to test an identity
    is to throw arbitrary input at it. Eight seeded random states on a twelve-mass chain round
    trip to 1e-14, and every one of them then agrees with an independent velocity-Verlet run
    to the integrator's own accuracy. A projection that dropped the mass matrix, or shapes
    normalised in the ordinary dot product rather than under M, would pass neither.
    """
    n = 12
    matrices = coupled.chain_matrices(n, MASS, STIFFNESS)
    modes = coupled.normal_mode_solve(*matrices)
    dt = (2.0 * np.pi / modes.frequencies[-1]) / 400.0

    def round_trip_error(rng: np.random.Generator) -> float:
        x0 = rng.normal(0.0, 0.02, n)
        v0 = rng.normal(0.0, 0.05, n)
        return float(np.max(np.abs(coupled.evolve(modes, x0, v0, 0.0) - x0)))

    def integration_error(rng: np.random.Generator) -> float:
        x0 = rng.normal(0.0, 0.02, n)
        v0 = rng.normal(0.0, 0.05, n)
        run = coupled.simulate_coupled(*matrices, x0, v0, dt, 2000)
        exact = coupled.evolve(modes, x0, v0, run.times)
        return float(np.max(np.abs(exact - run.positions)) / np.max(np.abs(run.positions)))

    assert seed_study(round_trip_error, n_seeds=8, base_seed=4).values.max() < 1e-14
    assert seed_study(integration_error, n_seeds=8, base_seed=4).values.max() < 5e-4


def test_chain_frequencies_read_from_a_noisy_record_are_limited_by_its_length():
    """All five modes recovered to 0.21% — the same 0.21% at 2% noise and at 30%.

    This is the module's measurement lesson, and it is the opposite of module 06's. There,
    timing an energy minimum asked the data its weakest question and fell apart as the noise
    grew. Here the spectrum averages the whole record, so noise moves a peak barely at all:
    the statistical error grows twentyfold across this range and remains four times smaller
    than the bias that does not move.

    That bias is the record's, not the noise's. A finite record has a finite resolution, and
    the three-point vertex that interpolates between bins is exact only for a parabola. Halve
    the record and the error doubles; double it and the error halves — 1.65% at 20 s, 0.21% at
    164 s, 0.11% at 328 s. A student who quoted the +/- from the seed scatter alone would be
    claiming four significant figures on a number good to three, which is the honest reason
    this test asserts against a total error and checks the scatter separately.
    """
    for sigma in (0.02, 0.30):
        studies = [
            seed_study(
                lambda rng, p=mode, s=sigma: float(
                    _read_chain_modes(measurement.add_noise(CHAIN_CLEAN, s, rng))[p]
                ),
                n_seeds=8,
                base_seed=11,
            )
            for mode in range(CHAIN_SIZE)
        ]
        measured = np.array([study.mean for study in studies])
        assert np.max(np.abs(measured - CHAIN_EXACT) / CHAIN_EXACT) < 0.005
        assert max(study.relative_spread for study in studies) < 0.01

    # The bias is set by the record and shrinks with it, while the noise level does not enter.
    # Noiseless records, so what is left is only what the finite record costs.
    biases = []
    for samples in (2048, 16384):
        times = (np.arange(samples) - samples // 2) * CHAIN_DT
        clean = coupled.evolve(
            CHAIN_MODES, np.array([1.0, 0.0, 0.0, 0.0, 0.0]), np.zeros(CHAIN_SIZE), times
        )[:, 0]
        found = _read_chain_modes(clean)
        biases.append(float(np.max(np.abs(found - CHAIN_EXACT) / CHAIN_EXACT)))

    assert biases[0] < 0.02
    assert biases[1] < biases[0] / 3.0


# Averaging spectra: a single periodogram of noise is a famously bad estimator — its scatter
# does not fall as the record lengthens, only its frequency resolution improves. Averaging
# independent records is what buys precision, and it buys it at the usual rate.
PERIODOGRAM_SAMPLES = 1024
PERIODOGRAM_DT = 0.01


def _periodogram_scatter(n_averages: int, base_seed: int = 0) -> float:
    """Relative scatter of a noise periodogram averaged over `n_averages` records."""
    seeds = np.random.SeedSequence(base_seed).spawn(n_averages)
    total = np.zeros(PERIODOGRAM_SAMPLES)
    for seed in seeds:
        noise = np.random.default_rng(seed).normal(size=PERIODOGRAM_SAMPLES)
        _, transform = fourier.spectrum(noise, PERIODOGRAM_DT)
        total += np.abs(transform) ** 2
    averaged = total / n_averages
    return float(np.std(averaged) / np.mean(averaged))


def test_averaging_periodograms_shrinks_the_noise_floor_as_one_over_root_m():
    """The scatter of an averaged noise spectrum falls as M^(-1/2), not the record length.

    This is the rule behind every later laboratory that reports a spectral measurement with an
    error bar: one long record and many short ones are not interchangeable, and only averaging
    independent realisations pushes the floor down. A single periodogram has relative scatter
    of order one however many samples it holds.
    """
    counts = [1, 4, 16, 64]
    scatters = [_periodogram_scatter(m) for m in counts]
    assert abs(scaling_exponent(counts, scatters) - (-0.5)) < 0.2
    assert scatters[0] > scatters[-1]


# Module 08's measurement: two photogates 0.4 m apart on a 2 m string at v = 20 m/s, a pluck
# sending a pulse of height 5 mm past both, and detector noise of 5% of that height added to
# each gate's record independently. The string is computed once; only the noise is redrawn.
GATE_TENSION = 4.0
GATE_MU = 0.01
GATE_SPEED = waves.wave_speed(GATE_TENSION, GATE_MU)
GATE_DX = 2.0 / 800
GATE_WIDTH = 0.05
GATE_NOISE = 0.05 * 0.005


def _gate_records() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.arange(801) * GATE_DX
    dt = 0.5 * GATE_DX / GATE_SPEED
    n_steps = int(np.ceil((0.8 + 8.0 * GATE_WIDTH) / GATE_SPEED / dt))
    pluck = 0.01 * np.exp(-(((x - 0.8) / GATE_WIDTH) ** 2))
    run = waves.simulate_string(
        pluck, np.zeros_like(x), GATE_DX, dt, GATE_TENSION, GATE_MU, n_steps
    )
    return run.times, run.y[:, 480], run.y[:, 640]


GATE_TIMES, GATE_FIRST, GATE_SECOND = _gate_records()
GATE_DISTANCE = 160 * GATE_DX


def _speed_by_centroid(rng: np.random.Generator) -> float:
    half_window = 4.0 * GATE_WIDTH / GATE_SPEED
    first = measurement.add_noise(GATE_FIRST, GATE_NOISE, rng)
    second = measurement.add_noise(GATE_SECOND, GATE_NOISE, rng)
    return GATE_DISTANCE / (
        measurement.pulse_arrival_time(GATE_TIMES, second, half_window)
        - measurement.pulse_arrival_time(GATE_TIMES, first, half_window)
    )


def _speed_by_peak(rng: np.random.Generator) -> float:
    def peak_time(record: np.ndarray) -> float:
        i = int(np.argmax(record))
        before, top, after = record[i - 1 : i + 2]
        step = GATE_TIMES[1] - GATE_TIMES[0]
        return float(GATE_TIMES[i] + 0.5 * (before - after) / (before - 2.0 * top + after) * step)

    first = measurement.add_noise(GATE_FIRST, GATE_NOISE, rng)
    second = measurement.add_noise(GATE_SECOND, GATE_NOISE, rng)
    return GATE_DISTANCE / (peak_time(second) - peak_time(first))


def test_a_noisy_photogate_pair_recovers_the_wave_speed_whatever_the_seed():
    """v +/- sigma_v from two noisy gates agrees with sqrt(T/mu) — the laboratory's last cell.

    Timed by centroid, eight seeds give a scatter of 0.6% and a mean within one standard error
    of 20 m/s, and a second, independent family of seeds agrees with the first. There is no
    systematic to budget for here, unlike the module-02 estimators: the centroid of a pulse on
    this grid travels at exactly v (test_convergence), so the only error left is the noise, and
    a statistical band is the honest tolerance.

    Timing the peak of the same records instead scatters about three times as much, 1.35%
    against 0.49% over 32 seeds. The peak is decided by the three highest samples, the centroid
    by every sample of the pulse, and that is the whole difference — which is why the
    laboratory asks the student to use the whole pulse.
    """
    family_a = seed_study(_speed_by_centroid, n_seeds=8, base_seed=0)
    family_b = seed_study(_speed_by_centroid, n_seeds=8, base_seed=10_000)
    assert family_a.agrees_with(GATE_SPEED, n_sigma=3.0)
    assert family_b.agrees_with(GATE_SPEED, n_sigma=3.0)
    assert family_a.relative_spread < 0.01

    combined_error = float(np.hypot(family_a.standard_error, family_b.standard_error))
    assert abs(family_a.mean - family_b.mean) < 3.0 * combined_error

    by_centroid = seed_study(_speed_by_centroid, n_seeds=32, base_seed=3)
    by_peak = seed_study(_speed_by_peak, n_seeds=32, base_seed=3)
    assert by_peak.relative_spread > 2.0 * by_centroid.relative_spread


# The wattmeter, watched through a camera. A right-moving sinusoidal train passes a gate, and
# all that is recorded is the displacement of three neighbouring points over time — the patch a
# camera would actually see. Everything else, the slope and the transverse velocity, has to be
# differenced out of it, and the noise goes along for the ride.
WATT_TENSION = 4.0
WATT_MU = 0.01
WATT_SPEED = waves.wave_speed(WATT_TENSION, WATT_MU)
WATT_AMPLITUDE = 2e-3
WATT_WAVELENGTH = 0.5
WATT_OMEGA = WATT_SPEED * 2.0 * np.pi / WATT_WAVELENGTH
WATT_EXACT = waves.sinusoidal_mean_power(WATT_AMPLITUDE, WATT_OMEGA, WATT_TENSION, WATT_MU)
WATT_NOISE = 0.05 * WATT_AMPLITUDE


def _watt_patch() -> tuple[np.ndarray, float, float, slice]:
    cells, length = 3200, 8.0
    dx = length / cells
    x = np.arange(cells + 1) * dx
    k = 2.0 * np.pi / WATT_WAVELENGTH
    low, high, shoulder = 0.4, 3.0, 0.4
    ramp = np.clip((x - (low - shoulder)) / shoulder, 0.0, 1.0) * np.clip(
        ((high + shoulder) - x) / shoulder, 0.0, 1.0
    )
    y0 = WATT_AMPLITUDE * np.sin(k * x) * 0.5 * (1.0 - np.cos(np.pi * ramp))

    dt = 0.5 * dx / WATT_SPEED
    run = waves.simulate_string(
        y0, -WATT_SPEED * np.gradient(y0, dx), dx, dt, WATT_TENSION, WATT_MU,
        int(round(0.20 / dt)),
    )
    gate = int(round(4.0 / dx))
    first = int(np.searchsorted(run.times, 0.06))
    cycles = int((0.17 - 0.06) / (2.0 * np.pi / WATT_OMEGA)) * 2.0 * np.pi / WATT_OMEGA
    last = int(np.searchsorted(run.times, run.times[first] + cycles))
    return run.y[:, gate - 1 : gate + 2], dx, dt, slice(first, last)


WATT_PATCH, WATT_DX, WATT_DT, WATT_WINDOW = _watt_patch()


def _power_by_cross_differencing(rng: np.random.Generator) -> float:
    """The honest wattmeter: slope from the neighbours in space, velocity from those in time."""
    noisy = measurement.add_noise(WATT_PATCH, WATT_NOISE, rng)
    slope = (noisy[:, 2] - noisy[:, 0]) / (2.0 * WATT_DX)
    velocity = (noisy[2:, 1] - noisy[:-2, 1]) / (2.0 * WATT_DT)
    flux = waves.energy_flux(slope[1:-1], velocity, WATT_TENSION)
    return float(flux[WATT_WINDOW].mean())


def _power_by_slope_squared(rng: np.random.Generator) -> float:
    """The tempting shortcut: for a right-mover P = T v y_x^2, so measure only the slope."""
    noisy = measurement.add_noise(WATT_PATCH, WATT_NOISE, rng)
    slope = (noisy[:, 2] - noisy[:, 0]) / (2.0 * WATT_DX)
    return float((WATT_TENSION * WATT_SPEED * slope**2)[WATT_WINDOW].mean())


def test_a_noisy_wattmeter_recovers_the_mean_power_only_if_it_differences_two_ways():
    """Cross-differencing agrees with (1/2) mu v omega^2 A^2; squaring one record does not.

    Both estimators are honest arithmetic on the same noisy pictures of the same string, and
    they differ by a factor of three and a half. Over 32 seeds the cross-differenced wattmeter
    reads (0.0248 +/- 0.0007) W against the closed form's 0.02527 W — agreement within its own
    error bar. The slope-squared wattmeter reads 0.0886 W, and `agrees_with` rejects it.

    The reason is the difference between a product and a square. P = -T y_x y_t takes its slope
    from the two neighbours in space and its velocity from the two neighbours in time, so the
    two noises are drawn from disjoint samples, independent, and their cross term averages
    away. P = T v y_x^2 takes both from the same numbers, so the noise multiplies itself:
    <(y_x + d)^2> = <y_x^2> + sigma_d^2, and the estimator is biased high by T v sigma_d^2 no
    matter how long anyone averages. That predicted offset is 0.0640 W, which is 253% of the
    signal; the measured excess is 251%.

    A bias that survives averaging is the hardest kind to catch, and it is *generic* to
    measuring anything quadratic — intensity, power, variance. Every later part of the course
    measures something proportional to the square of an amplitude; this is where the course
    says once that the square of a noisy number is not the noisy number's square.
    """
    honest = seed_study(_power_by_cross_differencing, n_seeds=32, base_seed=9)
    assert honest.agrees_with(WATT_EXACT, n_sigma=3.0)
    assert honest.relative_spread < 0.2

    biased = seed_study(_power_by_slope_squared, n_seeds=32, base_seed=9)
    assert not biased.agrees_with(WATT_EXACT, n_sigma=3.0)

    sigma_slope = WATT_NOISE * np.sqrt(2.0) / (2.0 * WATT_DX)
    predicted_offset = WATT_TENSION * WATT_SPEED * sigma_slope**2
    assert abs((biased.mean - honest.mean) / predicted_offset - 1.0) < 0.05

    other_family = seed_study(_power_by_cross_differencing, n_seeds=32, base_seed=77)
    combined = float(np.hypot(honest.standard_error, other_family.standard_error))
    assert abs(honest.mean - other_family.mean) < 3.0 * combined
