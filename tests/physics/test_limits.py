"""Accuracy category 3: analytic limits.

Every numerical result the module produces is pinned to a closed form somewhere in its
parameter space: the integrator to the exact solution, the damped branches to each other at
their boundary, the driven response to its low-frequency, resonance, and peak formulas, and
phasor addition to the interference law it will become in the optics modules.
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import oscillators, phasors

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
