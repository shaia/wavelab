"""Accuracy category 3: analytic limits.

Every numerical result the module produces is pinned to a closed form somewhere in its
parameter space: the integrator to the exact solution, the damped branches to each other at
their boundary, the driven response to its low-frequency, resonance, and peak formulas, and
phasor addition to the interference law it will become in the optics modules.
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import coupled, fourier, oscillators, phasors, waves
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


def test_the_fixed_chain_reproduces_its_closed_form_at_every_size():
    """omega_p = 2 sqrt(k_s/m) sin(p pi / (2(N+1))), and shapes that are sampled sine waves.

    The whole of module 07 rests on a formula nobody solves a determinant for. It is verified
    instead, against the same general eigensolver that handled module 06's pair, at sizes from
    one mass to a hundred — agreement at 3.5e-15 relative, which is the eigensolver's own
    precision and not a physics tolerance.

    The single fixed mass is included because it catches a builder error nothing else would.
    One mass between two walls has *two* springs on it, so it oscillates at sqrt(2 k_s/m), not
    sqrt(k_s/m); a chain assembled by writing 2 k_s down the diagonal and forgetting why gets
    every other size right and this one wrong.

    Shapes are compared up to sign. Eigenvectors are only defined up to one, the solver's
    convention (largest entry positive) and the closed form's (the sine's own) genuinely
    disagree for some modes, and a mode drawn upside down is the same motion.
    """
    for n in (1, 2, 3, 5, 20, 100):
        matrices = coupled.chain_matrices(n, MASS, STIFFNESS)
        modes = coupled.normal_mode_solve(*matrices)
        closed_form = coupled.chain_mode_frequencies(n, MASS, STIFFNESS)

        assert np.allclose(modes.frequencies, closed_form, rtol=1e-12)
        assert np.allclose(
            np.abs(modes.shapes),
            np.abs(coupled.chain_mode_shapes(n)) / np.sqrt(MASS),
            atol=1e-12,
        )

    single = coupled.normal_mode_solve(*coupled.chain_matrices(1, MASS, STIFFNESS))
    assert np.isclose(single.frequencies[0], np.sqrt(2.0 * STIFFNESS / MASS), rtol=1e-12)

    # And the top of the band saturates: a hundred masses are no faster than five.
    top = [
        coupled.chain_mode_frequencies(n, MASS, STIFFNESS)[-1] for n in (5, 20, 100)
    ]
    assert np.all(np.diff(top) > 0.0)
    assert np.all(np.array(top) < 2.0 * np.sqrt(STIFFNESS / MASS))


def test_a_free_chain_has_one_zero_mode_and_it_is_a_rigid_translation():
    """Momentum conservation, arriving as an eigenvalue rather than as a theorem.

    Take the walls away and the chain can drift bodily without stretching any spring, so one
    motion costs no energy at all. Its shape is uniform — every mass moving together — and its
    frequency is zero.

    The frequency is tested against a tolerance and never against equality. The eigenvalue
    lands within rounding of zero on either side and `normal_mode_solve` clips it before the
    square root, so what comes back is somewhere below 1e-7 rather than at 0 — a square root
    turns an eigenvalue's absolute error into a much larger relative one. Measured here: 8.5e-8
    at N = 5 and exactly 0.0 at N = 20, which is precisely why equality is the wrong test.
    """
    for n in (5, 20):
        matrices = coupled.chain_matrices(n, MASS, STIFFNESS, boundary="free")
        modes = coupled.normal_mode_solve(*matrices)

        assert modes.frequencies[0] < 1e-6 * modes.frequencies[-1]

        uniform = np.full(n, 1.0 / np.sqrt(n * MASS))
        assert np.allclose(np.abs(modes.shapes[:, 0]), uniform, atol=1e-12)

        # Exactly one zero mode, and the rest are the free chain's own closed form —
        # cos-shaped rather than sin-shaped, so N in the denominator where the fixed chain
        # has N + 1, and the count runs p = 0 .. N-1 with p = 0 being the drift itself.
        # The drift itself is excluded from the comparison rather than compared against zero,
        # for the reason above: 8.5e-8 is not close to 0.0 in any relative sense.
        p = np.arange(1, n)
        free_form = 2.0 * np.sqrt(STIFFNESS / MASS) * np.sin(p * np.pi / (2.0 * n))
        assert np.allclose(modes.frequencies[1:], free_form, rtol=1e-12)

    # A ring has the same zero mode, and pairs above it: rotational symmetry means a wave
    # running one way round and the same wave running the other way must cost the same.
    ring = coupled.normal_mode_solve(*coupled.chain_matrices(6, MASS, STIFFNESS, "periodic"))
    assert ring.frequencies[0] < 1e-6 * ring.frequencies[-1]
    assert np.isclose(ring.frequencies[1], ring.frequencies[2], rtol=1e-12)
    assert np.isclose(ring.frequencies[3], ring.frequencies[4], rtol=1e-12)


def test_evolving_the_modes_reproduces_the_integrated_motion():
    """Two routes to the same trajectory: solve once and sum, or step ten thousand times.

    `evolve` assembles the motion from the eigensolution and never integrates; the trajectory
    it is compared against is the reverse. They agree to 6.5e-6 of the amplitude over three
    slow periods of a twelve-mass chain, which is the integrator's error and not `evolve`'s —
    `evolve` has none to accumulate.

    The starting state is random rather than a mode, because starting on a mode would test
    only the one term that is easy. A random state spreads itself over every mode, so the
    projection, the twelve independent evolutions and the resummation all have to be right.
    """
    n = 12
    matrices = coupled.chain_matrices(n, MASS, STIFFNESS)
    modes = coupled.normal_mode_solve(*matrices)
    generator = np.random.default_rng(7)
    x0 = generator.normal(0.0, 0.02, n)
    v0 = generator.normal(0.0, 0.05, n)

    # Round trip at t = 0: projecting a state onto the modes and rebuilding it loses nothing.
    assert np.max(np.abs(coupled.evolve(modes, x0, v0, 0.0) - x0)) < 1e-14

    dt = (2.0 * np.pi / modes.frequencies[-1]) / 400.0
    run = coupled.simulate_coupled(*matrices, x0, v0, dt, 4000)
    exact = coupled.evolve(modes, x0, v0, run.times)
    assert np.max(np.abs(exact - run.positions)) < 1e-4 * np.max(np.abs(run.positions))

    # A free chain's zero mode drifts instead of oscillating: the centre of mass travels at
    # constant speed for ever, and nothing internal happens at all.
    free = coupled.normal_mode_solve(*coupled.chain_matrices(6, MASS, STIFFNESS, "free"))
    drifting = coupled.evolve(free, np.zeros(6), np.full(6, 0.3), np.linspace(0.0, 5.0, 51))
    assert np.isclose(drifting[-1].mean(), 0.3 * 5.0, rtol=1e-12)
    assert np.ptp(drifting[-1]) < 1e-12


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


# The string. Tension and density give v = 20 m/s; every exact solution below lives on an
# unbounded line, so the grids that are compared with them keep their pulses far from the ends.
STRING_TENSION = 4.0
STRING_MU = 0.01
STRING_SPEED = waves.wave_speed(STRING_TENSION, STRING_MU)


def test_the_leapfrog_string_is_the_mass_chain_it_came_from():
    """Discretising the wave equation rebuilds module 07's chain, to rounding.

    Grid point i of `simulate_string` carries mass mu dx and is tied to its neighbours by
    springs of stiffness T / dx; a fixed end is a wall. Handed to `coupled.simulate_coupled` as
    exactly that chain, the same start produces the same motion step for step — positions to
    1.0e-14 of the largest displacement and velocities to 4.1e-14, over 2000 steps.

    The two codes share nothing but the scheme. One builds a stiffness matrix and knows nothing
    about grids; the other applies a stencil and knows nothing about matrices. Agreement is the
    module's closing loop made literal: the continuum limit, run backwards by the computer.
    """
    n = 201
    dx = 1.0 / (n - 1)
    x = np.arange(n) * dx
    y0 = 0.01 * np.exp(-(((x - 0.4) / 0.05) ** 2))
    v0 = 0.05 * np.exp(-(((x - 0.7) / 0.05) ** 2))
    dt = 0.7 * dx / STRING_SPEED

    string = waves.simulate_string(y0, v0, dx, dt, STRING_TENSION, STRING_MU, 2000)
    matrices = coupled.chain_matrices(n - 2, STRING_MU * dx, STRING_TENSION / dx)
    chain = coupled.simulate_coupled(*matrices, y0[1:-1], v0[1:-1], dt, 2000)

    assert np.max(np.abs(string.y[:, 1:-1] - chain.positions)) < 1e-12 * np.max(np.abs(string.y))
    assert np.max(np.abs(string.dydt[:, 1:-1] - chain.velocities)) < 1e-12 * np.max(
        np.abs(string.dydt)
    )
    assert np.all(string.y[:, [0, -1]] == 0.0)


def test_the_chain_and_the_string_meet_at_one_wave_speed():
    """Both derivations of the wave equation land on the same v — the module's first lesson.

    Route (a) reads the speed off the chain: at long wavelengths the dispersion relation is a
    straight line of slope a sqrt(k_s/m). Route (b) is Newton on a string element, giving
    sqrt(T/mu). The dictionary mu = m/a, T = k_s a turns one into the other, and it has to do so
    for any chain at all, not for a lucky choice of numbers.
    """
    for mass, stiffness, spacing in ((0.02, 50.0, 0.01), (1.0, 3.0, 0.5), (1e-3, 800.0, 2e-3)):
        k = 1e-6 / spacing  # k a = 1e-6: the (ka)^2/24 curvature is below rounding
        chain_slope = float(coupled.chain_dispersion(k, spacing, mass, stiffness)) / k
        string = waves.wave_speed(stiffness * spacing, mass / spacing)
        assert np.isclose(chain_slope, string, rtol=1e-12)
        assert np.isclose(string, spacing * np.sqrt(stiffness / mass), rtol=1e-12)


def test_a_pluck_splits_into_two_copies_of_half_the_height():
    """Released from rest, one hump becomes two, each half as tall, running apart at v.

    It must split: a single copy moving one way would need a velocity from the start, and a
    pluck has none. So each direction gets half, and once the halves separate their peaks are
    exactly 1/2 of the original, centred at x0 - vt and x0 + vt.
    """
    x = np.linspace(-3.0, 3.0, 6001)
    width = 0.2

    def hump(s: np.ndarray) -> np.ndarray:
        return np.exp(-((s / width) ** 2))

    t = 0.1  # vt = 2 m, ten widths: the two halves no longer overlap
    y = waves.dalembert_solution(hump, STRING_SPEED, x, t)
    left, right = x < 0.0, x > 0.0
    assert np.isclose(y[left].max(), 0.5, rtol=1e-10)
    assert np.isclose(y[right].max(), 0.5, rtol=1e-10)
    assert np.isclose(x[left][np.argmax(y[left])], -STRING_SPEED * t, atol=1e-9)
    assert np.isclose(x[right][np.argmax(y[right])], STRING_SPEED * t, atol=1e-9)


def test_a_strike_spreads_into_a_plateau_whose_edges_run_at_the_wave_speed():
    """A flat string struck over [-a, a] with speed w rises to w a / v and stays there.

    The plateau grows while the struck region still feeds it, at w per second, until t = a/v;
    after that its height is frozen at w a / v and only its width changes, the half-height
    edges running outward at exactly v. The string is left permanently displaced — nothing
    pulls it back, because a uniform displacement costs a string no energy.

    The strike is rectangular, so its velocity jumps, and `dalembert_solution` still gives the
    exact answer because it takes the velocity's antiderivative rather than integrating it.
    """
    speed, half_width = 5.0, 0.3
    x = np.linspace(-3.0, 3.0, 6001)

    def struck_integral(s: np.ndarray) -> np.ndarray:
        return 2.0 * np.clip(s + half_width, 0.0, 2.0 * half_width)

    for t in (0.02, 0.1, 0.3):
        y = waves.dalembert_solution(
            lambda s: np.zeros_like(s), speed, x, t, v0_integral=struck_integral
        )
        assert np.isclose(y.max(), min(2.0 * t, 2.0 * half_width / speed), rtol=1e-12)
        if t > half_width / speed:
            above = x[y >= 0.5 * y.max()]
            # The half-height points fall on grid points, so either may land just inside or
            # just outside the set: three spacings is the resolution of the reading.
            assert np.isclose(np.ptp(above), 2.0 * speed * t, atol=3.0 * (x[1] - x[0]))


def test_dalembert_solves_the_wave_equation_and_meets_its_initial_data():
    """y_tt = v^2 y_xx, y(x, 0) = y0 and y_t(x, 0) = v0 — checked, not assumed.

    Finite differences stand in for the derivatives, so both residuals are small rather than
    zero, and both are the O(h^2) of the differences themselves at h = 1e-3: 2.0e-4 of y_tt
    for the wave equation, 2.1e-4 of the peak velocity for the starting velocity. The initial
    shape is reproduced exactly. The velocity has an antiderivative in closed form,
    sech^2 -> tanh, so nothing numerical hides inside the solution being tested.
    """
    speed, h = 5.0, 1e-3
    x = np.linspace(-1.0, 1.0, 201)

    def shape(s: np.ndarray) -> np.ndarray:
        return np.exp(-((s / 0.3) ** 2))

    def velocity(s: np.ndarray) -> np.ndarray:
        return 0.7 / np.cosh(s / 0.2) ** 2

    def velocity_integral(s: np.ndarray) -> np.ndarray:
        return 0.7 * 0.2 * np.tanh(s / 0.2)

    def y(t: float, positions: np.ndarray) -> np.ndarray:
        return waves.dalembert_solution(
            shape, speed, positions, t, v0_integral=velocity_integral
        )

    t0 = 0.05
    y_tt = (y(t0 + h, x) - 2.0 * y(t0, x) + y(t0 - h, x)) / h**2
    y_xx = (y(t0, x + h) - 2.0 * y(t0, x) + y(t0, x - h)) / h**2
    assert np.max(np.abs(y_tt - speed**2 * y_xx)) < 1e-3 * np.max(np.abs(y_tt))

    assert np.max(np.abs(y(0.0, x) - shape(x))) < 1e-15
    y_t = (y(h, x) - y(-h, x)) / (2.0 * h)
    assert np.max(np.abs(y_t - velocity(x))) < 1e-3 * np.max(velocity(x))


def test_a_travelling_sinusoid_is_the_course_convention_with_omega_equal_to_vk():
    """Re[A e^{i(kx - omega t)}] solves the wave equation exactly when omega = v k.

    Started as A cos(kx) with the velocity a right-mover needs, d'Alembert returns the
    convention's travelling wave to rounding, moving toward +x as the convention says positive
    k must. Reverse the starting velocity and the same shape runs the other way, as
    Re[A e^{i(-kx - omega t)}]: the direction of travel lives in the velocity, not the shape.
    """
    amplitude, k = 0.3, 4.0
    omega = STRING_SPEED * k
    x = np.linspace(-1.0, 1.0, 201)
    t = np.linspace(0.0, 0.5, 11)

    def start(s: np.ndarray) -> np.ndarray:
        return amplitude * np.cos(k * s)

    def rightward(s: np.ndarray) -> np.ndarray:
        return -amplitude * STRING_SPEED * np.cos(k * s)

    phase = k * x[np.newaxis, :] - omega * t[:, np.newaxis]
    moving_right = waves.dalembert_solution(start, STRING_SPEED, x, t, v0_integral=rightward)
    assert np.max(np.abs(moving_right - np.real(amplitude * np.exp(1j * phase)))) < 1e-12

    mirrored = -k * x[np.newaxis, :] - omega * t[:, np.newaxis]
    moving_left = waves.dalembert_solution(
        start, STRING_SPEED, x, t, v0_integral=lambda s: -rightward(s)
    )
    assert np.max(np.abs(moving_left - np.real(amplitude * np.exp(1j * mirrored)))) < 1e-12


# Energy on the string (module 09). The helpers below build the three states the module
# contrasts: a right-moving pulse, a wave train long enough to average over, and a standing mode.


def _travelling_pulse(
    cells: int = 1600, length: float = 4.0, courant: float = 0.5, direction: float = 1.0
) -> tuple[waves.StringEvolution, float]:
    """A Gaussian pulse launched one way, with y_t = -/+ v y_x making it purely travelling."""
    dx = length / cells
    x = np.arange(cells + 1) * dx
    centre, width = (1.0 if direction > 0 else length - 1.0), 0.15

    def shape(s: np.ndarray) -> np.ndarray:
        return 0.01 * np.exp(-(((s - centre) / width) ** 2))

    slope = -2.0 * (x - centre) / width**2 * shape(x)
    dt = courant * dx / STRING_SPEED
    steps = int(round(1.0 / STRING_SPEED / dt))
    run = waves.simulate_string(
        shape(x), -direction * STRING_SPEED * slope, dx, dt, STRING_TENSION, STRING_MU, steps
    )
    return run, dx


def _densities(
    run: waves.StringEvolution, dx: float, step: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """u_K, u_P and P at one saved step, the way a laboratory reads them off a record."""
    slope = np.gradient(run.y[step], dx)
    return (
        waves.kinetic_density(run.dydt[step], STRING_MU),
        waves.potential_density(slope, STRING_TENSION),
        waves.energy_flux(slope, run.dydt[step], STRING_TENSION),
    )


def test_a_travelling_wave_carries_equal_kinetic_and_potential_energy_at_every_point():
    """u_K = u_P point by point, not merely on average — the module's surprise, measured.

    For a right-mover y = f(x - vt) the chain rule gives y_t = -v y_x, so
    u_K = (1/2) mu v^2 y_x^2 = (1/2) T y_x^2 = u_P at every point and every instant. Nothing is
    averaged and nothing cancels: the two densities are the same function of position. On a
    1600-cell grid the largest pointwise gap is 1.1e-4 of the peak density and the two
    integrated totals agree to 1.6e-4, both falling fourfold for every halving of the spacing —
    the disagreement is the grid's, not the physics'.

    An oscillator does not do this. Module 01's mass holds all its energy as potential at the
    turning points and all of it as kinetic at the middle, and equipartition there is a
    statement about time averages. Every element of a travelling wave is a little behind its
    neighbour, so what the single mass does in sequence the string does all at once.
    """
    run, dx = _travelling_pulse()
    kinetic, potential, _ = _densities(run, dx, run.times.size // 2)
    peak = float((kinetic + potential).max())

    assert np.max(np.abs(kinetic - potential)) < 2e-4 * peak
    total_kinetic = float(np.trapezoid(kinetic, dx=dx))
    total_potential = float(np.trapezoid(potential, dx=dx))
    assert abs(total_kinetic - total_potential) < 3e-4 * total_potential


def test_the_energy_of_a_travelling_wave_moves_at_the_wave_speed_and_in_its_direction():
    """P = v (u_K + u_P), with the sign of the flux following the direction of travel.

    Substituting y_t = -v y_x into P = -T y_x y_t gives P = T v y_x^2, while u_K + u_P is
    T y_x^2: the flux is the density times v, which is what "the energy travels at v" has to
    mean for a quantity that is spread out rather than located. Measured on the grid, P/u is
    within 1.1e-6 of v across the pulse.

    Both signs occur and both are right. A right-mover has P >= 0 everywhere, a left-mover
    P <= 0 everywhere, and in each case the energy goes the way the pattern goes — whether the
    string at that point happens to be rising or falling.
    """
    for direction in (1.0, -1.0):
        run, dx = _travelling_pulse(cells=800, direction=direction)
        kinetic, potential, flux = _densities(run, dx, run.times.size // 2)
        density = kinetic + potential
        carrying = density > 1e-3 * density.max()

        velocity = flux[carrying] / density[carrying]
        assert np.all(np.abs(velocity / (direction * STRING_SPEED) - 1.0) < 1e-5)
        # Away from the pulse the flux is arithmetic dust of either sign; what has to hold is
        # that none of it amounts to anything — the backwards-signed part carries 2.5e-8 of the
        # total, and its largest single value is 3.4e-8 of the peak.
        assert np.all(direction * flux >= -1e-6 * np.abs(flux).max())
        backwards = flux[direction * flux < 0.0]
        assert np.abs(backwards).sum() < 1e-6 * np.abs(flux).sum()


def test_a_pluck_holds_only_potential_energy_until_it_splits_in_two():
    """Released from rest a pluck is pure u_P; a moment later each half is half and half.

    This is d'Alembert's splitting read as an energy budget. At t = 0 the string is bent and
    still, so u_K vanishes identically — exactly, since the solver was handed zeros — and all
    the energy is in the stretch. As the two half-height copies separate, each becomes a
    travelling wave and must obey the equality above, so the total divides evenly between the
    two kinds: measured, K/U = 1.00016 on a 1600-cell grid, and closer as the grid refines.

    Half the height means a quarter of the energy density; two copies make half the original
    energy. The missing half is not missing — it is the kinetic energy the two copies now have,
    and the books balance only because both densities are quadratic in what they measure.
    """
    cells, length = 1600, 4.0
    dx = length / cells
    x = np.arange(cells + 1) * dx

    def bump(s: np.ndarray) -> np.ndarray:
        return 0.01 * np.exp(-(((s - 2.0) / 0.15) ** 2))

    dt = 0.5 * dx / STRING_SPEED
    steps = int(round(1.2 / STRING_SPEED / dt))
    run = waves.simulate_string(
        bump(x), np.zeros_like(x), dx, dt, STRING_TENSION, STRING_MU, steps, save_every=steps
    )
    start_energy = waves.total_energy(run.y[0], run.dydt[0], dx, STRING_TENSION, STRING_MU)

    kinetic, potential, _ = _densities(run, dx, 0)
    assert np.all(kinetic == 0.0)
    assert abs(float(np.trapezoid(potential, dx=dx)) - start_energy) < 1e-3 * start_energy

    kinetic, potential, _ = _densities(run, dx, -1)
    total_kinetic = float(np.trapezoid(kinetic, dx=dx))
    total_potential = float(np.trapezoid(potential, dx=dx))
    assert abs(total_kinetic / total_potential - 1.0) < 1e-3
    assert abs(total_kinetic + total_potential - start_energy) < 1e-3 * start_energy


def _wave_train(
    amplitude: float, wavelength: float, cells: int = 3200, length: float = 8.0
) -> tuple[float, float, np.ndarray]:
    """A right-moving sinusoidal train with a flat top, and the gate record it produces.

    A pure sine cannot travel on a string with fixed ends — it would have to move the ends — so
    the train is windowed, with raised-cosine shoulders and a middle flat enough that a gate at
    4 m sees whole cycles of an unmodulated wave between t = 0.06 s and t = 0.17 s. Launching it
    with y_t = -v y_x makes it exactly a right-mover, so d'Alembert carries the window along
    untouched and the flat part stays flat.
    """
    dx = length / cells
    x = np.arange(cells + 1) * dx
    k = 2.0 * np.pi / wavelength
    omega = STRING_SPEED * k
    low, high, shoulder = 0.4, 3.0, 0.4

    def window(s: np.ndarray) -> np.ndarray:
        ramp = np.clip((s - (low - shoulder)) / shoulder, 0.0, 1.0) * np.clip(
            ((high + shoulder) - s) / shoulder, 0.0, 1.0
        )
        return 0.5 * (1.0 - np.cos(np.pi * ramp))

    y0 = amplitude * np.sin(k * x) * window(x)
    dt = 0.5 * dx / STRING_SPEED
    run = waves.simulate_string(
        y0, -STRING_SPEED * np.gradient(y0, dx), dx, dt, STRING_TENSION, STRING_MU,
        int(round(0.20 / dt)),
    )
    gate = int(round(4.0 / dx))
    slope = np.gradient(run.y, dx, axis=1)[:, gate]
    flux = waves.energy_flux(slope, run.dydt[:, gate], STRING_TENSION)

    first = int(np.searchsorted(run.times, 0.06))
    whole_cycles = int((0.17 - 0.06) / (2.0 * np.pi / omega)) * 2.0 * np.pi / omega
    last = int(np.searchsorted(run.times, run.times[first] + whole_cycles))
    return float(flux[first:last].mean()), omega, run.dydt[:, gate]


def test_a_sinusoidal_train_delivers_half_mu_v_omega_squared_amplitude_squared():
    """The mean power through a gate matches (1/2) mu v omega^2 A^2 to better than 0.2%.

    The instantaneous flux is mu v omega^2 A^2 cos^2(kx - omega t), and the average of cos^2
    over whole cycles is one half. Measured at a gate with the train's flat top passing:
    0.99966 of the closed form at each of three amplitudes, and 0.99879 to 0.99992 across a
    factor of four in frequency, the residual being the grid's.

    This is the course's first intensity law. Power goes as the square of the amplitude and as
    the square of the frequency, and both squares come from one place — the flux is quadratic
    in the transverse velocity A omega, not in the displacement.
    """
    for amplitude in (1e-3, 2e-3, 4e-3):
        measured, omega, _ = _wave_train(amplitude, 0.5)
        expected = waves.sinusoidal_mean_power(amplitude, omega, STRING_TENSION, STRING_MU)
        assert abs(measured / expected - 1.0) < 2e-3

    for wavelength in (1.0, 0.5, 0.25):
        measured, omega, _ = _wave_train(2e-3, wavelength)
        expected = waves.sinusoidal_mean_power(2e-3, omega, STRING_TENSION, STRING_MU)
        assert abs(measured / expected - 1.0) < 2e-3


def test_the_transverse_speed_and_the_wave_speed_are_independent_knobs():
    """A omega is set by the sender, v by the medium, and neither constrains the other.

    The three velocities of this module are not ranked. The pattern moves at v = sqrt(T/mu);
    the energy moves at v as well; but a piece of string moves at y_t = -v y_x, which whoever
    made the wave chose through the slope. On the train above the ratio is 0.025, and a real
    string never approaches 1 — but only because the small-slope model gives out first, not
    because anything in the equation forbids it.

    The test states that arithmetic rather than simulating a string outside its model: the
    amplitude that would make A omega exceed v also makes the slope order one, which is the
    boundary of everything this module derives.
    """
    _, omega, transverse = _wave_train(2e-3, 0.5)
    assert np.isclose(np.abs(transverse).max(), 2e-3 * omega, rtol=2e-3)
    assert np.abs(transverse).max() < 0.03 * STRING_SPEED

    # A omega = v and the slope amplitude A k = A omega / v = 1 are the same statement, so a
    # string whose pieces keep up with its wave is a string bent at 45 degrees.
    outrunning = STRING_SPEED / omega
    assert np.isclose(outrunning * omega, STRING_SPEED)
    assert np.isclose(outrunning * (omega / STRING_SPEED), 1.0)
    assert outrunning > 30.0 * 2e-3  # ... at forty times the train's amplitude, on a 0.5 m wave


def test_a_standing_wave_stores_energy_without_transporting_any():
    """Its flux is large at every instant and zero on average, everywhere along the string.

    A mode y = A sin(kx) cos(omega t) has P = T A^2 k omega sin(kx) cos(kx) sin(omega t)
    cos(omega t), which is odd in time about every half period, so its average over a cycle
    vanishes at every x. Measured over four periods of the third mode, the largest
    time-averaged flux anywhere is 5.7e-7 of the largest instantaneous flux: energy sloshes a
    quarter wavelength each way and none of it goes anywhere.

    The contrast with the travelling wave reaches the densities too. Here u_K and u_P are not
    equal pointwise — at the moment of release the string is all potential, and a quarter period
    later all kinetic, so their largest pointwise difference is the whole density. Only after
    averaging over a cycle do the totals match, to 6e-4. Equipartition at every point and
    instant belongs to a travelling wave, not to waves in general; module 11 builds the full
    standing-wave budget on this seed.
    """
    cells, length, mode = 800, 1.0, 3
    dx = length / cells
    x = np.arange(cells + 1) * dx
    k = mode * np.pi / length
    omega = STRING_SPEED * k
    amplitude = 2e-3

    dt = 0.5 * dx / STRING_SPEED
    per_period = int(round((2.0 * np.pi / omega) / dt))
    run = waves.simulate_string(
        amplitude * np.sin(k * x), np.zeros_like(x), dx, dt,
        STRING_TENSION, STRING_MU, 4 * per_period,
    )
    slope = np.gradient(run.y, dx, axis=1)
    flux = waves.energy_flux(slope, run.dydt, STRING_TENSION)
    averaged = flux[: 4 * per_period].mean(axis=0)

    assert np.abs(averaged).max() < 1e-5 * np.abs(flux).max()
    assert np.abs(flux).max() > 1e-3  # the instantaneous flux is not itself small

    kinetic = waves.kinetic_density(run.dydt, STRING_MU)
    potential = waves.potential_density(slope, STRING_TENSION)
    assert np.max(np.abs(kinetic - potential)) > 0.9 * np.max(kinetic + potential)

    mean_kinetic = float(np.trapezoid(kinetic, dx=dx, axis=1)[: 4 * per_period].mean())
    mean_potential = float(np.trapezoid(potential, dx=dx, axis=1)[: 4 * per_period].mean())
    assert abs(mean_kinetic / mean_potential - 1.0) < 2e-3


# The junction (module 10). A pulse is launched in the first medium, allowed to split at a jump
# in density, and the two pieces are read off the record. Each run's geometry is scaled to its
# own two wave speeds: the transmitted pulse is stretched by v_2/v_1, so the far side is made
# that much longer to hold it, and the grid is fine enough to resolve whichever pulse is
# narrower.

JUNCTION_AMPLITUDE = 0.01
JUNCTION_WIDTH = 0.2
JUNCTION_APPROACH = 1.2  # metres of the first medium crossed before the junction is reached
JUNCTION_CLEARANCE = 3.0  # pulse widths of separation insisted on before anything is measured


def _junction_run(
    ratio: float, points_per_width: int = 30, courant: float = 0.5
) -> tuple[waves.StringEvolution, float, np.ndarray, float]:
    """A Gaussian pulse in medium 1 meeting a jump to a density `ratio` times its own."""
    speed_2 = waves.wave_speed(STRING_TENSION, STRING_MU * ratio)
    width_2 = JUNCTION_WIDTH * speed_2 / STRING_SPEED
    dx = min(JUNCTION_WIDTH, width_2) / points_per_width
    clearance = JUNCTION_CLEARANCE * JUNCTION_WIDTH / STRING_SPEED

    junction = JUNCTION_APPROACH + STRING_SPEED * clearance + 2.0 * JUNCTION_WIDTH
    length = junction + speed_2 * clearance + 2.0 * width_2
    cells = int(round(length / dx))
    dx = length / cells

    x = np.arange(cells + 1) * dx
    mu = np.where(x < junction, STRING_MU, STRING_MU * ratio)
    centre = junction - JUNCTION_APPROACH

    def shape(s: np.ndarray) -> np.ndarray:
        return JUNCTION_AMPLITUDE * np.exp(-(((s - centre) / JUNCTION_WIDTH) ** 2))

    slope = -2.0 * (x - centre) / JUNCTION_WIDTH**2 * shape(x)
    dt = courant * dx / max(STRING_SPEED, speed_2)
    steps = int(round((JUNCTION_APPROACH / STRING_SPEED + clearance) / dt))
    run = waves.simulate_string(shape(x), -STRING_SPEED * slope, dx, dt, STRING_TENSION, mu, steps)
    return run, dx, mu, junction


def _split_amplitudes(ratio: float, points_per_width: int = 30) -> tuple[float, float]:
    """Reflected and transmitted amplitudes of a split pulse, as fractions of the incident one.

    Signed, and taken as the extremum on each side well clear of the junction, which is what a
    frame-by-frame reading of a filmed rope measures.
    """
    run, _, _, junction = _junction_run(ratio, points_per_width=points_per_width)
    speed_2 = waves.wave_speed(STRING_TENSION, STRING_MU * ratio)
    final = run.y[-1]

    def extremum(mask: np.ndarray) -> float:
        segment = final[mask]
        return float(segment[np.argmax(np.abs(segment))] / JUNCTION_AMPLITUDE)

    return (
        extremum(run.x < junction - JUNCTION_WIDTH),
        extremum(run.x > junction + JUNCTION_WIDTH * speed_2 / STRING_SPEED),
    )


def test_the_junction_coefficients_carry_their_own_limits_and_identities():
    """r = 0 at a match, and (-1, 0) and (+1, 2) are approached as the far side hardens or softens.

    Four statements, all of them algebra rather than simulation, and each one a physical claim
    the module makes. At Z_2 = Z_1 the pair is exactly (0, 1): nothing comes back. Let the far
    side grow heavy and r falls toward -1 while t falls toward 0 — at a hundredfold density the
    coefficients are already -0.8182 and 0.1818, at a ten-thousandfold -0.9802 and 0.0198,
    converging on the wall. Let it grow light and the same formula rises to +0.9802 and 1.9802,
    converging on a free end whose displacement doubles.

    Underneath both limits sits 1 + r = t, which is the continuity of the string itself and not
    a separate result: it holds to rounding across twelve decades of impedance ratio, so any
    numbers claiming to be r and t can be checked against it in one line.
    """
    assert waves.junction_coefficients(0.2, 0.2) == (0.0, 1.0)

    z1 = waves.impedance(STRING_TENSION, STRING_MU)
    for ratio, expected_r, expected_t in (
        (1e2, -0.818182, 0.181818),
        (1e4, -0.980198, 0.019802),
        (1e-2, +0.818182, 1.818182),
        (1e-4, +0.980198, 1.980198),
    ):
        z2 = waves.impedance(STRING_TENSION, STRING_MU * ratio)
        assert waves.junction_coefficients(z1, z2) == pytest.approx(
            (expected_r, expected_t), abs=1e-6
        )

    hard_r, hard_t = waves.junction_coefficients(1.0, np.array([1e6, 1e8, 1e10]))
    soft_r, soft_t = waves.junction_coefficients(1.0, np.array([1e-6, 1e-8, 1e-10]))
    assert np.all(np.diff(hard_r) < 0.0) and hard_r[-1] < -1.0 + 1e-9
    assert np.all(np.diff(soft_r) > 0.0) and soft_r[-1] > 1.0 - 1e-9
    assert hard_t[-1] < 1e-9 and abs(soft_t[-1] - 2.0) < 1e-9

    reflection, transmission = waves.junction_coefficients(1.0, np.logspace(-6.0, 6.0, 61))
    assert np.max(np.abs(1.0 + reflection - transmission)) < 1e-15


def test_the_junction_divides_the_power_into_two_fractions_that_sum_to_one():
    """R + T = 1 across twelve decades, and the division is the same from either side.

    R = r^2 and T = (Z_2/Z_1) t^2 are not two independent quantities that happen to agree.
    Substituting the coefficients puts (Z_1 - Z_2)^2 + 4 Z_1 Z_2 over (Z_1 + Z_2)^2, which is 1
    identically — so conservation of energy at the junction was already contained in the two
    matching conditions, and this sweep confirms it to 1e-15 rather than discovering it.

    The second identity is less obvious and just as exact: R(Z_1, Z_2) = R(Z_2, Z_1). A junction
    that sends back 44.4% of the power arriving from the heavy side sends back 44.4% of what
    arrives from the light side too, though its r has the opposite sign there and its t is five
    times larger. Energy cannot tell which way the wave was going; the displacement can.
    """
    ratios = np.logspace(-6.0, 6.0, 121)
    reflected, transmitted = waves.power_coefficients(1.0, ratios)
    assert np.max(np.abs(reflected + transmitted - 1.0)) < 1e-15
    assert np.all(reflected >= 0.0) and np.all(transmitted > 0.0)

    assert np.max(np.abs(reflected - waves.power_coefficients(ratios, 1.0)[0])) < 1e-15


def test_a_wall_and_a_free_end_are_the_two_ends_of_one_formula():
    """A fixed end returns -1.000003 A and a free end +1.000003 A, peaking at 2.000006 A.

    The solver knows nothing of impedance: `boundary="fixed"` holds a point at zero and
    `boundary="free"` gives it a ghost neighbour. Yet the pulses that come back are the ones
    `junction_coefficients` predicts in its two limits, to three parts in a million — the wall
    inverting the pulse, and the free end returning it upright while the end itself swings to
    twice the incident amplitude, where incident and reflected pulses overlap on it.

    Neither end takes any energy: both runs keep every joule to 1e-6, which is what makes them
    limits of a lossless junction rather than new physics. A wall is a second medium too heavy
    to move, and a free end one too light to resist.
    """
    length, cells = 2.0, 2000
    dx = length / cells
    x = np.arange(cells + 1) * dx
    centre, width = length - 0.8, 0.15

    def shape(s: np.ndarray) -> np.ndarray:
        return 0.01 * np.exp(-(((s - centre) / width) ** 2))

    slope = -2.0 * (x - centre) / width**2 * shape(x)
    dt = 0.5 * dx / STRING_SPEED
    steps = int(round((1.6 / STRING_SPEED) / dt))

    returned = {}
    for far_end in ("fixed", "free"):
        run = waves.simulate_string(
            shape(x),
            -STRING_SPEED * slope,
            dx,
            dt,
            STRING_TENSION,
            STRING_MU,
            steps,
            boundary=("free", far_end),
        )
        final = run.y[-1]
        returned[far_end] = float(final[np.argmax(np.abs(final))] / 0.01)
        energy = waves.total_energy(run.y, run.dydt, dx, STRING_TENSION, STRING_MU)
        assert abs(energy[-1] / energy[0] - 1.0) < 1e-6
        if far_end == "free":
            assert abs(run.y[:, -1].max() / 0.01 - 2.0) < 1e-4

    assert abs(returned["fixed"] + 1.0) < 1e-4
    assert abs(returned["free"] - 1.0) < 1e-4


def test_a_pulse_splits_as_the_impedances_say_and_inverts_only_off_the_harder_side():
    """Measured amplitude ratios match r and t to 3e-4 over a 625-fold range of density.

    The module in one table. A pulse is fired at a jump in density and the two pieces it becomes
    are measured off the final frame; the formulas are never consulted by the solver, which
    integrates displacements and has no notion of an amplitude ratio.

        mu_2/mu_1     r (formula / measured)      t (formula / measured)
          0.04        +0.6667 / +0.6668            1.6667 / 1.6664
          0.25        +0.3333 / +0.3334            1.3333 / 1.3332
          1.00         0.0000 / +0.0001            1.0000 / 1.0001
          4.00        -0.3333 / -0.3334            0.6667 / 0.6667
         25.00        -0.6667 / -0.6667            0.3333 / 0.3333

    The sign column is the misconception `reflection-always-inverts` being falsified. The
    reflected pulse comes back upside down for mu_2 > mu_1 and right side up for mu_2 < mu_1,
    and it changes over at the match rather than at some threshold of "hard enough". A rope tied
    to a wall and a rope tied to a thread are the two ends of that column, not two different
    rules.
    """
    z1 = waves.impedance(STRING_TENSION, STRING_MU)
    for ratio, expected_r, expected_t in (
        (0.04, +2.0 / 3.0, 5.0 / 3.0),
        (0.25, +1.0 / 3.0, 4.0 / 3.0),
        (1.00, 0.0, 1.0),
        (4.00, -1.0 / 3.0, 2.0 / 3.0),
        (25.00, -2.0 / 3.0, 1.0 / 3.0),
    ):
        z2 = waves.impedance(STRING_TENSION, STRING_MU * ratio)
        assert waves.junction_coefficients(z1, z2) == pytest.approx((expected_r, expected_t))

        measured_r, measured_t = _split_amplitudes(ratio)
        assert abs(measured_r - expected_r) < 3e-4, f"r at mu_2/mu_1 = {ratio}"
        assert abs(measured_t - expected_t) < 3e-4, f"t at mu_2/mu_1 = {ratio}"
        if expected_r != 0.0:
            assert np.sign(measured_r) == np.sign(expected_r)


def test_a_transmitted_pulse_can_stand_taller_than_the_wave_that_made_it():
    """Onto a string a hundred times lighter, t = 1.82 — carrying a third of the power.

    The paradox the module has to defuse, measured rather than argued. At mu_2/mu_1 = 0.01 the
    far side swings 1.818 times as far as the incident pulse did, which looks like amplification
    and is not: the light string is cheap to move, its impedance is a tenth of the first
    string's, and the flux factor Z_2/Z_1 turns a squared amplitude ratio of 3.31 into a power
    fraction of 0.331. The reflected pulse, upright and 0.818 as tall, keeps the other 0.669.

    A displacement ratio answers "how far does it swing"; a power ratio answers "how much did it
    cost". The junction conserves the second and has no reason to conserve the first.
    """
    reflected, transmitted = _split_amplitudes(0.01)
    assert transmitted > 1.0
    assert abs(transmitted - 1.818182) < 2e-3
    assert abs(reflected - 0.818182) < 2e-3

    z1 = waves.impedance(STRING_TENSION, STRING_MU)
    z2 = waves.impedance(STRING_TENSION, 0.01 * STRING_MU)
    power_reflected, power_transmitted = waves.power_coefficients(z1, z2)
    assert power_transmitted < 0.34 < power_reflected
    assert abs(power_transmitted - (z2 / z1) * transmitted**2) < 1e-2
    assert power_reflected + power_transmitted == pytest.approx(1.0)
