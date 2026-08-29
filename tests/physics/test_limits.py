"""Accuracy category 3: analytic limits.

Every numerical result the module produces is pinned to a closed form somewhere in its
parameter space: the integrator to the exact solution, the damped branches to each other at
their boundary, the driven response to its low-frequency, resonance, and peak formulas, and
phasor addition to the interference law it will become in the optics modules.
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import coupled, fourier, oscillators, phasors
from wavelab.validation import scaling_exponent

pytestmark = pytest.mark.analytic_limit

MASS = 0.5
STIFFNESS = 8.0
OMEGA0 = oscillators.natural_frequency(MASS, STIFFNESS)
PERIOD = 2.0 * np.pi / OMEGA0
CRITICAL_DAMPING = 2.0 * np.sqrt(MASS * STIFFNESS)


def test_integrator_matches_the_closed_form():
    """Twenty periods at a thousand steps each: numerical and exact positions agree."""
    dt = PERIOD / 1000.0
    trajectory = oscillators.simulate(MASS, STIFFNESS, 0.1, 0.2, dt, 20_000)
    exact = oscillators.position(trajectory.times, MASS, STIFFNESS, 0.1, 0.2)
    amplitude, _ = oscillators.amplitude_phase(0.1, 0.2, OMEGA0)
    assert np.max(np.abs(trajectory.positions - exact)) / amplitude < 1e-3


def test_closed_form_velocity_is_the_position_derivative():
    t = np.linspace(0.0, 3.0 * PERIOD, 4001)
    x = oscillators.position(t, MASS, STIFFNESS, 0.1, 0.2)
    v = oscillators.velocity(t, MASS, STIFFNESS, 0.1, 0.2)
    numerical_v = np.gradient(x, t)
    # np.gradient is first order at the two endpoints; compare the interior only.
    assert np.max(np.abs(numerical_v[1:-1] - v[1:-1])) < 1e-4 * np.max(np.abs(v))


def test_amplitude_phase_special_cases():
    """Released from rest: phi = 0. Kicked from the origin toward +x: phi = -pi/2."""
    amplitude, phase = oscillators.amplitude_phase(0.1, 0.0, OMEGA0)
    assert np.isclose(amplitude, 0.1) and np.isclose(phase, 0.0)
    amplitude, phase = oscillators.amplitude_phase(0.0, 0.4, OMEGA0)
    assert np.isclose(amplitude, 0.4 / OMEGA0) and np.isclose(phase, -np.pi / 2.0)


def test_damped_solution_approaches_undamped_as_b_vanishes():
    t = np.linspace(0.0, 5.0 * PERIOD, 2001)
    damped = oscillators.damped_position(t, MASS, STIFFNESS, 1e-9, 0.1, 0.2)
    undamped = oscillators.position(t, MASS, STIFFNESS, 0.1, 0.2)
    assert np.max(np.abs(damped - undamped)) < 1e-6


def test_damped_branches_agree_at_the_critical_boundary():
    """Approach b = 2 sqrt(mk) from both sides: all three formulas must be one function."""
    t = np.linspace(0.0, 3.0 * PERIOD, 601)
    critical = oscillators.damped_position(
        t, MASS, STIFFNESS, CRITICAL_DAMPING, 0.1, 0.2
    )
    from_below = oscillators.damped_position(
        t, MASS, STIFFNESS, CRITICAL_DAMPING * (1.0 - 1e-9), 0.1, 0.2
    )
    from_above = oscillators.damped_position(
        t, MASS, STIFFNESS, CRITICAL_DAMPING * (1.0 + 1e-9), 0.1, 0.2
    )
    scale = np.max(np.abs(critical))
    assert np.max(np.abs(from_below - critical)) / scale < 1e-6
    assert np.max(np.abs(from_above - critical)) / scale < 1e-6


def test_damping_regime_labels():
    assert oscillators.damping_regime(MASS, STIFFNESS, 0.1 * CRITICAL_DAMPING) == "underdamped"
    assert oscillators.damping_regime(MASS, STIFFNESS, CRITICAL_DAMPING) == "critical"
    assert oscillators.damping_regime(MASS, STIFFNESS, 10.0 * CRITICAL_DAMPING) == "overdamped"


def test_quality_factor_is_omega0_over_gamma():
    damping = 0.4
    q = oscillators.quality_factor(MASS, STIFFNESS, damping)
    gamma = oscillators.damping_rate(MASS, damping)
    assert np.isclose(q, OMEGA0 / gamma)


def test_driven_amplitude_low_frequency_limit_is_static_response():
    """omega -> 0: the mass follows the force quasistatically, X -> F0 / k, in phase."""
    response = oscillators.driven_amplitude(1e-6, MASS, STIFFNESS, 0.4, 1.0)
    assert np.isclose(abs(response), 1.0 / STIFFNESS, rtol=1e-6)
    assert abs(np.angle(response)) < 1e-6


def test_displacement_lags_drive_by_quarter_cycle_at_omega0():
    """arg X(omega0) = +pi/2 under the e^{-i omega t} convention — the sign the conventions
    page promises, and the one a student comparing with an engineering text will question."""
    response = oscillators.driven_amplitude(OMEGA0, MASS, STIFFNESS, 0.4, 1.0)
    assert np.isclose(np.angle(response), np.pi / 2.0)


def test_amplitude_peak_sits_below_omega0():
    """The resonance-curve maximum is at omega^2 = omega0^2 - gamma^2/2, not at omega0.

    This is the falsifying computation for the resonance-peak-at-omega0 misconception; the
    damping here is heavy enough that the shift is far larger than the grid spacing.
    """
    damping = 1.2
    gamma = oscillators.damping_rate(MASS, damping)
    expected_peak = np.sqrt(OMEGA0**2 - gamma**2 / 2.0)
    omegas = np.linspace(0.2 * OMEGA0, 1.5 * OMEGA0, 20_001)
    magnitudes = np.abs(
        [oscillators.driven_amplitude(w, MASS, STIFFNESS, damping, 1.0) for w in omegas]
    )
    measured_peak = omegas[np.argmax(magnitudes)]
    assert abs(measured_peak - expected_peak) < omegas[1] - omegas[0]
    assert measured_peak < OMEGA0


def test_steady_state_response_agrees_with_the_scalar_driven_amplitude():
    """One closed form, two faces: the vectorized sweep must equal the scalar call exactly.

    Module 03 weights each harmonic of a periodic drive with `steady_state_response` while
    module 02's page quotes `driven_amplitude`; if the two ever disagreed, the course would
    be teaching two different oscillators under one name.
    """
    omegas = np.linspace(0.0, 3.0 * OMEGA0, 41)
    swept = oscillators.steady_state_response(omegas, MASS, STIFFNESS, 0.4, 1.0)
    scalar = [oscillators.driven_amplitude(w, MASS, STIFFNESS, 0.4, 1.0) for w in omegas]
    assert np.allclose(swept, scalar, rtol=0.0, atol=0.0)


def test_steady_state_response_low_and_high_frequency_limits():
    """Slow drive: the mass tracks the force at F0/k, in phase. Fast drive: pure inertia,
    amplitude F0/(m omega^2) and a lag of pi — the mass moves *against* the force."""
    slow = oscillators.steady_state_response(np.array([1e-6]), MASS, STIFFNESS, 0.4, 1.0)[0]
    assert np.isclose(abs(slow), 1.0 / STIFFNESS, rtol=1e-6)
    assert abs(np.angle(slow)) < 1e-6

    fast_omega = 1e5
    fast = oscillators.steady_state_response(
        np.array([fast_omega]), MASS, STIFFNESS, 0.4, 1.0
    )[0]
    assert np.isclose(abs(fast), 1.0 / (MASS * fast_omega**2), rtol=1e-6)
    assert np.isclose(np.angle(fast), np.pi, atol=1e-4)


def test_resonance_peak_omega_matches_the_measured_maximum():
    """The closed form against a brute-force sweep, at three very different dampings."""
    omegas = np.linspace(1e-6, 2.0 * OMEGA0, 200_001)
    for damping in (0.05, 0.4, 1.2):
        amplitude = np.abs(
            oscillators.steady_state_response(omegas, MASS, STIFFNESS, damping, 1.0)
        )
        measured = omegas[np.argmax(amplitude)]
        predicted = oscillators.resonance_peak_omega(MASS, STIFFNESS, damping)
        assert abs(measured - predicted) < omegas[1] - omegas[0]
        assert predicted < OMEGA0


def test_resonance_peak_omega_limits():
    """As damping vanishes the peak climbs to omega0; below Q = 1/sqrt(2) it is gone."""
    assert np.isclose(
        oscillators.resonance_peak_omega(MASS, STIFFNESS, 1e-9), OMEGA0, rtol=1e-12
    )
    threshold_damping = np.sqrt(2.0 * MASS * STIFFNESS)  # Q = 1/sqrt(2) exactly
    assert oscillators.resonance_peak_omega(MASS, STIFFNESS, threshold_damping) == 0.0
    assert oscillators.resonance_peak_omega(MASS, STIFFNESS, 2.0 * threshold_damping) == 0.0
    just_below = oscillators.resonance_peak_omega(
        MASS, STIFFNESS, threshold_damping * (1.0 - 1e-6)
    )
    assert 0.0 < just_below < 0.01 * OMEGA0  # the peak leaves through zero, not through omega0


def test_power_absorbed_peaks_exactly_at_omega0():
    """Displacement resonance sits below omega0; *power* resonance sits on it, at any damping.

    The distinction the advanced section makes, pinned numerically: the same sweep whose
    amplitude peak moves with damping has a power peak that does not move at all.
    """
    omegas = np.linspace(1e-6, 2.0 * OMEGA0, 200_001)
    for damping in (0.05, 0.4, 1.2):
        power = oscillators.power_absorbed(omegas, MASS, STIFFNESS, damping, 1.0)
        assert abs(omegas[np.argmax(power)] - OMEGA0) < omegas[1] - omegas[0]


def test_three_q_extractors_agree_on_clean_data():
    """Q from a ringdown, from a bandwidth, and from a phase slope: one number three ways.

    Even without noise the three carry different residuals, and the tolerances say which:
    the phase-slope route is exact, the bandwidth route is O(1/Q^2) low because the half-power
    width of |X| is only asymptotically gamma, and the ringdown route is O((gamma P)^2) low
    because it reads each half cycle's amplitude as its root mean square. Checked at Q = 20,
    where the last two are a part in 10^3 and two parts in 10^3.
    """
    damping = 0.1  # Q = 20
    expected = oscillators.quality_factor(MASS, STIFFNESS, damping)

    t = np.linspace(0.0, 30.0 * PERIOD, 60_001)
    ringdown = oscillators.damped_position(t, MASS, STIFFNESS, damping, 0.1, 0.0)
    assert np.isclose(oscillators.q_from_ringdown(t, ringdown), expected, rtol=3e-3)

    omegas = np.linspace(0.5 * OMEGA0, 1.5 * OMEGA0, 100_001)
    response = oscillators.steady_state_response(omegas, MASS, STIFFNESS, damping, 1.0)
    assert np.isclose(
        oscillators.q_from_bandwidth(omegas, np.abs(response)), expected, rtol=2e-3
    )
    assert np.isclose(
        oscillators.q_from_phase_slope(omegas, np.angle(response)), expected, rtol=1e-6
    )


def test_phase_slope_stays_exact_where_the_bandwidth_estimator_drifts():
    """At Q = 2.5 the half-power width is no longer gamma; the phase slope still is.

    Worth pinning because it is the one place the three faces of Q visibly come apart, and
    the laboratory asks students to notice it.
    """
    damping = 0.8  # Q = 2.5
    expected = oscillators.quality_factor(MASS, STIFFNESS, damping)
    omegas = np.linspace(1e-6, 4.0 * OMEGA0, 200_001)
    response = oscillators.steady_state_response(omegas, MASS, STIFFNESS, damping, 1.0)

    assert np.isclose(
        oscillators.q_from_phase_slope(omegas, np.angle(response)), expected, rtol=1e-6
    )
    from_bandwidth = oscillators.q_from_bandwidth(omegas, np.abs(response))
    assert abs(from_bandwidth - expected) / expected > 0.05


def test_driven_simulation_reaches_the_predicted_steady_state():
    """After the transient dies, the simulated amplitude equals |X(omega)|."""
    damping = 0.8
    drive_omega = 3.0
    dt = PERIOD / 400.0
    trajectory = oscillators.simulate(
        MASS, STIFFNESS, 0.0, 0.0, dt, 60_000,
        damping=damping, drive_amplitude=1.0, drive_omega=drive_omega,
    )
    predicted = abs(
        oscillators.driven_amplitude(drive_omega, MASS, STIFFNESS, damping, 1.0)
    )
    tail = trajectory.positions[-8000:]
    assert np.isclose(tail.max(), predicted, rtol=1e-2)


def test_the_impulse_response_is_a_free_decay_launched_by_a_kick():
    """G(t) IS `damped_position` started at x = 0 with v = 1/m, and is zero before the kick.

    A spike of force changes the velocity and nothing else, so the Green function is not a
    new solution of anything — it is the free decay of module 01 with a particular initial
    condition. Checked in all three regimes because `impulse_response` delegates to
    `damped_position` rather than writing out the underdamped closed form, which is what lets
    it survive critical damping at all: the textbook expression divides by omega_d.
    """
    t = np.linspace(-2.0 * PERIOD, 6.0 * PERIOD, 1601)
    after = t >= 0.0
    for damping in (0.4, CRITICAL_DAMPING, 3.0 * CRITICAL_DAMPING):
        green = oscillators.impulse_response(t, MASS, STIFFNESS, damping)
        launched = oscillators.damped_position(
            t[after], MASS, STIFFNESS, damping, 0.0, 1.0 / MASS
        )
        assert np.allclose(green[after], launched, rtol=0.0, atol=0.0)
        assert np.all(green[~after] == 0.0)

    # The kick sets a velocity, so G starts at zero and leaves the origin as t/m. Read off
    # the closed form rather than differenced from it: the small-t limit is the statement,
    # and a finite difference would only add its own truncation error to it.
    # The window is short enough that the leading correction, a factor (1 - gamma t / 4), is
    # itself below the tolerance; over a whole period it would not be.
    early = np.linspace(0.0, PERIOD / 100_000.0, 5)
    green = oscillators.impulse_response(early, MASS, STIFFNESS, 0.4)
    assert green[0] == 0.0
    assert np.allclose(green[1:], early[1:] / MASS, rtol=1e-5)


def test_the_impulse_response_does_not_overflow_far_before_the_kick():
    """The discarded branch of `damped_position` grows as e^{+gamma|t|/2}; clip it, don't run it.

    A laboratory record that starts well before t = 0 is ordinary, and the causal gate has to
    be applied to the argument rather than to the answer — evaluating the exponential first
    and masking afterwards overflows and returns nan.
    """
    early = np.array([-1e4, -1e2, -1.0, 0.0, 1.0])
    green = oscillators.impulse_response(early, MASS, STIFFNESS, 0.4)
    assert np.all(np.isfinite(green))
    assert np.all(green[:3] == 0.0)


def test_the_step_response_settles_at_the_new_equilibrium():
    """A constant force switched on at t = 0 ends at F0/k, having overshot on the way.

    The closed form is written as F0/k times a free decay from unit displacement, so it needs
    no regime analysis of its own; this pins it against the underdamped textbook expression
    where that exists, and against the static limit everywhere.
    """
    late = np.array([200.0 * PERIOD])
    for damping in (0.1, 0.4, CRITICAL_DAMPING, 3.0 * CRITICAL_DAMPING):
        settled = oscillators.step_response(late, MASS, STIFFNESS, damping, 2.0)
        assert np.isclose(settled[0], 2.0 / STIFFNESS, rtol=1e-9)

    damping = 0.4
    t = np.linspace(0.0, 8.0 * PERIOD, 2001)
    gamma = oscillators.damping_rate(MASS, damping)
    omega_d = np.sqrt(OMEGA0**2 - gamma**2 / 4.0)
    textbook = (1.0 / STIFFNESS) * (
        1.0
        - np.exp(-gamma * t / 2.0)
        * (np.cos(omega_d * t) + (gamma / (2.0 * omega_d)) * np.sin(omega_d * t))
    )
    assert np.allclose(
        oscillators.step_response(t, MASS, STIFFNESS, damping, 1.0), textbook, rtol=0.0, atol=1e-15
    )

    # Overshoot grows with Q, and critical damping has none: the falsifier for
    # `response-follows-force-shape`, since a featureless force produces a ringing answer.
    overshoot = {
        d: oscillators.step_response(t, MASS, STIFFNESS, d, 1.0).max() * STIFFNESS - 1.0
        for d in (0.1, 1.0, CRITICAL_DAMPING)
    }
    assert overshoot[0.1] > overshoot[1.0] > overshoot[CRITICAL_DAMPING]
    assert np.isclose(overshoot[CRITICAL_DAMPING], 0.0, atol=1e-12)


def test_the_kick_spectrum_is_the_conjugate_of_the_swept_response():
    """The LTI bridge: FFT one ringdown and you have module 02's entire resonance curve.

    Under the course's e^{-i omega t} kernel the transform of G is
    G-hat = (1/m)/(omega0^2 - omega^2 + i gamma omega), while `steady_state_response` carries
    the opposite sign on the damping term — so the two are conjugates, not equals, and
    reversing that would flip every phase lag in the module. Part XI's plan cites this test
    as the guarantee behind G -> point spread function and G-hat -> optical transfer function.

    Compared on the non-negative half only: `steady_state_response` rejects negative drive
    frequencies, which is physically right for a sweep and simply not the question here.
    The tolerance is set in the next file — the error is truncation of the ringdown or
    discretisation of the grid, whichever is larger — so 1e-5 here is a floor with the record
    chosen long enough (33 amplitude e-foldings) that only the grid is left.
    """
    damping = 0.4
    dt = 0.005
    n = 2**15
    t = (np.arange(n) - n // 2) * dt
    omega, kicked = fourier.spectrum(
        oscillators.impulse_response(t, MASS, STIFFNESS, damping), dt
    )
    band = (omega >= 0.0) & (omega < 3.0 * OMEGA0)
    swept = oscillators.steady_state_response(omega[band], MASS, STIFFNESS, damping, 1.0)

    error = np.max(np.abs(kicked[band] - np.conj(swept))) / np.max(np.abs(swept))
    assert error < 1e-5

    # The conjugation is the content: taking the swept curve at face value fails loudly.
    assert np.max(np.abs(kicked[band] - swept)) / np.max(np.abs(swept)) > 0.5


def test_fitting_the_line_beats_crossing_it_on_an_under_resolved_ringdown():
    """The trap module 05's laboratory is built to avoid, pinned so it cannot quietly return.

    `q_from_bandwidth` and `q_from_linewidth` take the same arguments and answer the same
    question, and on a swept resonance curve — where the experimenter chooses the grid — they
    agree. On the spectrum of a ringdown nobody chooses the grid: bin spacing is 2 pi / T
    while the linewidth is gamma, so a record of n amplitude e-foldings puts n / pi bins
    across the full width whatever Q is. Here that is under two bins, and the crossing route
    reads 18% low while the fit stays within 6%. A negative control, in the spirit of the
    aliasing and biased-seed tests: an estimator that fails silently is worse than one that
    raises, so its failure is written down.
    """
    damping = 0.1  # Q = 20
    gamma = oscillators.damping_rate(MASS, damping)
    dt = 0.01
    n = 2 * int((3.0 * 2.0 / gamma) / dt)  # a record holding three amplitude e-foldings
    t = (np.arange(n) - n // 2) * dt
    omega, transform = fourier.spectrum(
        oscillators.impulse_response(t, MASS, STIFFNESS, damping), dt
    )
    band = (omega > 0.5 * OMEGA0) & (omega < 1.5 * OMEGA0)
    expected = oscillators.quality_factor(MASS, STIFFNESS, damping)

    assert gamma / (omega[1] - omega[0]) < 2.0, "the line is meant to be under-resolved here"

    crossings = oscillators.q_from_bandwidth(omega[band], np.abs(transform[band]))
    fitted = oscillators.q_from_linewidth(omega[band], np.abs(transform[band]))
    assert abs(crossings - expected) / expected > 0.15
    assert abs(fitted - expected) / expected < 0.06


def test_the_coupled_pair_has_the_two_modes_solved_by_hand():
    """omega_s = sqrt(k/m) and omega_a = sqrt((k + 2 k_c)/m), with shapes (1, 1) and (1, -1).

    The module derives these from a 2x2 determinant with a pen; this holds the numerical
    solver to the same answer, so the page and the library cannot drift apart. Agreement is at
    the last bit — 1e-15 — because both are doing the same small piece of algebra.

    The symmetric frequency is the interesting one: it equals the *uncoupled* natural
    frequency for every coupling strength, because in that motion the two masses move together
    and the spring between them never changes length. A spring that never stretches cannot
    affect the period, and the page turns on exactly that sentence.
    """
    for coupling in (0.05, 0.4, 4.0, 40.0):
        matrices = coupled.two_mass_matrices(MASS, STIFFNESS, coupling)
        modes = coupled.normal_mode_solve(*matrices)
        symmetric = np.sqrt(STIFFNESS / MASS)
        antisymmetric = np.sqrt((STIFFNESS + 2.0 * coupling) / MASS)

        assert np.allclose(modes.frequencies, [symmetric, antisymmetric], rtol=1e-12)
        assert np.isclose(modes.frequencies[0], OMEGA0, rtol=1e-12)

        expected = np.array([[1.0, 1.0], [1.0, -1.0]]) / np.sqrt(2.0 * MASS)
        assert np.allclose(modes.shapes, expected, atol=1e-12)


def test_starting_one_pendulum_empties_it_completely():
    """The falsifier: start one mass and its energy does not stay there — it all leaves.

    This is the experiment behind `energy-stays-in-excited-pendulum`. Released from rest with
    only the first mass displaced, its share of the energy falls to 5.7e-4 of the total within
    half an exchange period, then comes back. Nothing is lost anywhere; there is no damping in
    the model at all. The energy is simply somewhere else.

    Weak coupling is part of the claim, not a convenience. The transfer is complete only when
    the two mode amplitudes are equal, and at k_c/k = 0.05 they are equal to a part in a
    thousand. Push the coupling to k_c = k and 7.4% of the energy never leaves the first mass —
    checked below, because a module that promised "all of it" at any coupling would be wrong.
    """
    coupling = 0.05 * STIFFNESS
    matrices = coupled.two_mass_matrices(MASS, STIFFNESS, coupling)
    modes = coupled.normal_mode_solve(*matrices)
    period = coupled.exchange_time(*modes.frequencies)

    dt = (2.0 * np.pi / modes.frequencies[-1]) / 200.0
    trajectory = coupled.simulate_coupled(
        *matrices, [1.0, 0.0], [0.0, 0.0], dt, int(period / dt)
    )
    energies = coupled.site_energies(
        *matrices, trajectory.positions, trajectory.velocities
    )
    share = energies[:, 0] / energies.sum(axis=1)

    # It starts with 97.6%, not 100%: the coupling spring is stretched at t = 0 and
    # `site_energies` splits every spring's energy between the masses it joins, so the
    # undisplaced mass is credited with half of that. The bookkeeping is a convention, and
    # this is where it shows.
    assert share[0] > 0.97
    assert share.min() < 0.01  # and is emptied
    assert share[-1] > 0.97  # and gets it all back one exchange period later

    # The total never moves: this is a transfer, not a loss.
    total = energies.sum(axis=1)
    assert np.ptp(total) / total[0] < 1e-3

    strong = coupled.two_mass_matrices(MASS, STIFFNESS, STIFFNESS)
    strong_modes = coupled.normal_mode_solve(*strong)
    strong_dt = (2.0 * np.pi / strong_modes.frequencies[-1]) / 200.0
    strong_period = coupled.exchange_time(*strong_modes.frequencies)
    strong_run = coupled.simulate_coupled(
        *strong, [1.0, 0.0], [0.0, 0.0], strong_dt, int(strong_period / strong_dt)
    )
    strong_share = coupled.site_energies(
        *strong, strong_run.positions, strong_run.velocities
    )
    fraction = strong_share[:, 0] / strong_share.sum(axis=1)
    assert fraction.min() > 0.05  # strong coupling leaves a real remainder behind


def test_the_exchange_is_the_beat_between_the_two_mode_frequencies():
    """The sloshing is module 00's beat, carrying energy between two visible objects.

    Started with one mass displaced, the first mass's motion is the sum of two equal-amplitude
    cosines at the mode frequencies — which is exactly what `phasors.beat_signal` builds. The
    integrator knows nothing of either fact, so the agreement is a real check rather than an
    identity, and it is what licenses the module to reuse the beat envelope it already taught.
    """
    coupling = 0.05 * STIFFNESS
    matrices = coupled.two_mass_matrices(MASS, STIFFNESS, coupling)
    modes = coupled.normal_mode_solve(*matrices)
    period = coupled.exchange_time(*modes.frequencies)

    dt = (2.0 * np.pi / modes.frequencies[-1]) / 400.0
    trajectory = coupled.simulate_coupled(
        *matrices, [1.0, 0.0], [0.0, 0.0], dt, int(period / dt)
    )
    beat = phasors.beat_signal(0.5, 0.5, *modes.frequencies, trajectory.times)
    assert np.max(np.abs(trajectory.positions[:, 0] - beat)) < 5e-3

    # And the envelope's half-period is the moment of full transfer.
    envelope_zero = np.pi / (modes.frequencies[1] - modes.frequencies[0])
    assert np.isclose(envelope_zero, period / 2.0, rtol=1e-12)


def test_real_signal_reproduces_the_direct_cosine():
    """The phasor round trip Re[A e^{-i phi} e^{-i omega t}] IS A cos(omega t + phi).

    This is the convention test: with the phasor sign flipped, the two disagree in phase.
    """
    t = np.linspace(0.0, 5.0, 2001)
    via_phasor = phasors.real_signal(0.7, 3.0, 1.1, t)
    direct = 0.7 * np.cos(3.0 * t + 1.1)
    assert np.max(np.abs(via_phasor - direct)) < 1e-12


def test_resultant_limits_and_interference_law():
    """Equal-opposite phasors cancel; in-phase phasors double; the general two-oscillation
    amplitude obeys A^2 = A1^2 + A2^2 + 2 A1 A2 cos(delta) — module 8's interference law."""
    cancelled, _ = phasors.resultant([1.0, 1.0], [0.0, np.pi])
    assert cancelled < 1e-12
    doubled, phase = phasors.resultant([1.0, 1.0], [0.4, 0.4])
    assert np.isclose(doubled, 2.0) and np.isclose(phase, 0.4)
    a1, a2, delta = 0.8, 1.3, 0.9
    amplitude, _ = phasors.resultant([a1, a2], [0.0, delta])
    expected = np.sqrt(a1**2 + a2**2 + 2.0 * a1 * a2 * np.cos(delta))
    assert np.isclose(amplitude, expected)


def test_resultant_matches_a_time_domain_sum():
    """The phasor prediction against a brute-force sum of cosines, point by point."""
    t = np.linspace(0.0, 2.0 * np.pi / 3.0, 4001)
    omega = 3.0
    direct = 0.8 * np.cos(omega * t + 0.2) + 1.1 * np.cos(omega * t + 2.0)
    amplitude, phase = phasors.resultant([0.8, 1.1], [0.2, 2.0])
    predicted = amplitude * np.cos(omega * t + phase)
    assert np.max(np.abs(direct - predicted)) < 1e-12


def test_beats_factor_into_carrier_and_envelope():
    """a [cos w1 t + cos w2 t] = 2a cos(dw t / 2) cos(wbar t), the beat identity."""
    t = np.linspace(0.0, 20.0, 8001)
    omega1, omega2 = 3.0, 3.4
    signal = phasors.beat_signal(0.6, 0.6, omega1, omega2, t)
    envelope_form = (
        2.0 * 0.6
        * np.cos(0.5 * (omega1 - omega2) * t)
        * np.cos(0.5 * (omega1 + omega2) * t)
    )
    assert np.max(np.abs(signal - envelope_form)) < 1e-12


# Harmonic analysis. The grid is centred on t = 0, which is what `spectrum` assumes and what
# makes an even signal transform to a real spectrum instead of one wrapped in a phase ramp.
SAMPLES = 4096
SAMPLE_DT = 0.01
SAMPLE_TIMES = (np.arange(SAMPLES) - SAMPLES // 2) * SAMPLE_DT
PHASE_GRID = 2.0 * np.pi * np.arange(SAMPLES) / SAMPLES


def test_closed_form_coefficients_match_the_numerical_integrals():
    """Every waveform in the zoo, its closed form against the coefficient integral.

    The residuals are the lesson as much as the agreement: the continuous triangle lands near
    machine precision, while the three waveforms carrying a jump stall at about 1/N, because
    no finite sample grid resolves a discontinuity. That is the same smoothness-buys-accuracy
    statement the coefficient decay rates make, seen from the numerical side.
    """
    smooth = (2.0 / np.pi) * np.arcsin(np.sin(PHASE_GRID))
    assert np.max(
        np.abs(fourier.fourier_coefficients(smooth, 9) - fourier.triangle_coefficients(9))
    ) < 1e-6

    wrapped = (PHASE_GRID + np.pi) % (2.0 * np.pi) - np.pi
    jumping = {
        "square": (np.sign(np.sin(PHASE_GRID)), fourier.square_coefficients(9)),
        "sawtooth": (wrapped / np.pi, fourier.sawtooth_coefficients(9)),
        "pulse train": (
            np.where(np.abs(wrapped) <= 0.25 * np.pi, 1.0, 0.0),
            fourier.pulse_train_coefficients(0.25, 9),
        ),
    }
    for name, (signal, closed_form) in jumping.items():
        error = np.max(np.abs(fourier.fourier_coefficients(signal, 9) - closed_form))
        assert error < 5.0 / SAMPLES, f"{name} coefficients are off by more than one part in N"


def test_gaussian_transforms_into_a_gaussian():
    """The only shape in the zoo that is its own transform — and numerically it is exact."""
    sigma = 0.3
    pulse = fourier.gaussian_pulse(SAMPLE_TIMES, sigma)
    omega, transform = fourier.spectrum(pulse, SAMPLE_DT)
    assert np.max(np.abs(transform - fourier.gaussian_spectrum(omega, sigma))) < 1e-10


def test_a_decaying_exponential_has_a_lorentzian_half_width_of_one_over_tau():
    """The ringdown pair, tested where it is meant to be read: the width of the line.

    Pointwise agreement is not available here — `exp_decay` jumps at t = 0, and a sampled jump
    costs first-order accuracy — so the claim under test is the physical one the course makes
    everywhere from module 02 to module 27: a decay of time constant tau shows a line of
    half-width 1/tau, and a faster decay a broader line.

    The half-power point is located by which bins clear the threshold, so the tolerance is one
    bin of the frequency axis — the resolution of the measurement, not a fudge factor.
    """
    for tau in (0.25, 0.5, 1.0):
        decay = fourier.exp_decay(SAMPLE_TIMES, tau)
        omega, transform = fourier.spectrum(decay, SAMPLE_DT)
        magnitude = np.abs(transform)
        half_power = magnitude >= magnitude.max() / np.sqrt(2.0)
        measured = (omega[half_power].max() - omega[half_power].min()) / 2.0
        assert abs(measured - 1.0 / tau) < omega[1] - omega[0]


def test_the_rect_spectrum_approaches_the_sinc_only_as_the_grid_refines():
    """A discontinuous pulse costs first-order accuracy — the Gaussian's exactness is earned.

    The error does not fall to roundoff at any fixed grid and zero-padding cannot rescue it:
    padding interpolates the transform of the *sampled* rect, which is not the continuous
    sinc. What is true, and what this pins, is that the discrepancy is O(dt).
    """
    steps = [0.02, 0.01, 0.005]
    errors = []
    for dt in steps:
        count = int(round(40.0 / dt))
        times = (np.arange(count) - count // 2) * dt
        omega, transform = fourier.spectrum(fourier.rect_pulse(times, 1.0), dt)
        errors.append(float(np.max(np.abs(transform - fourier.sinc_spectrum(omega, 1.0)))))
    assert abs(scaling_exponent(steps, errors) - 1.0) < 0.05


def test_a_real_cosine_puts_its_phasor_in_the_negative_half_of_the_spectrum():
    """Module 00's phasor, located exactly: pi x_hat at -omega0 and pi x_hat* at +omega0.

    The drive frequency is placed *on a grid bin* on purpose. Off-bin the same cosine leaks
    across neighbouring bins and the peak reads about a fifth low — not an error in the
    transform, but the leakage module 04 teaches, and a trap for anyone testing this casually.
    """
    spacing = 2.0 * np.pi / (SAMPLES * SAMPLE_DT)
    omega0 = 130 * spacing
    phasor = 2.0 * np.exp(-1j * 0.7)
    signal = np.real(phasor * np.exp(-1j * omega0 * SAMPLE_TIMES))

    omega, transform = fourier.spectrum(signal, SAMPLE_DT)
    negative = int(np.argmin(np.abs(omega + omega0)))
    positive = int(np.argmin(np.abs(omega - omega0)))
    assert np.isclose(transform[negative] * spacing / np.pi, phasor, rtol=1e-9)
    assert np.isclose(transform[positive] * spacing / np.pi, np.conj(phasor), rtol=1e-9)


def test_a_tone_above_nyquist_is_reported_as_a_different_frequency():
    """The negative control: below Nyquist the spectrum tells the truth, above it, it lies.

    A validator that can only ever pass is worse than none, so this asserts both halves. The
    folded tone does not merely become inaccurate — it is reported *confidently* at the wrong
    frequency, with nothing in the record to warn of it. That is why Nyquist is a validity
    edge in this module's model specification rather than a quality setting.
    """
    dt = 0.01
    nyquist = np.pi / dt
    times = np.arange(4096) * dt

    def apparent(true_omega: float) -> float:
        omega, transform = fourier.spectrum(np.cos(true_omega * times), dt)
        half = omega >= 0.0
        return float(omega[half][np.argmax(np.abs(transform[half]))])

    honest = 0.6 * nyquist
    assert np.isclose(apparent(honest), honest, rtol=2e-2)

    aliased = 1.4 * nyquist
    assert not np.isclose(apparent(aliased), aliased, rtol=2e-2)
    assert np.isclose(apparent(aliased), 2.0 * nyquist - aliased, rtol=2e-2)


def test_the_forced_integrator_reproduces_the_cosine_drive_it_generalises():
    """`simulate_forced` fed a sampled cosine must return `simulate`'s trajectory exactly.

    Module 03 trusts the sampled-force integrator to check a harmonic sum against physics that
    knows nothing of harmonics, so it has to be the same integrator, not merely a similar one.
    """
    damping, drive_omega, dt, n_steps = 0.4, 3.4, 1e-3, 20_000
    times = np.arange(n_steps + 1) * dt
    reference = oscillators.simulate(
        MASS, STIFFNESS, 0.0, 0.0, dt, n_steps,
        damping=damping, drive_amplitude=1.0, drive_omega=drive_omega,
    )
    sampled = oscillators.simulate_forced(
        MASS, STIFFNESS, 0.0, 0.0, dt, np.cos(drive_omega * times), damping=damping
    )
    assert np.max(np.abs(reference.positions - sampled.positions)) < 1e-12
    assert np.max(np.abs(reference.velocities - sampled.velocities)) < 1e-12
