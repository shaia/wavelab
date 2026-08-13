"""Accuracy category 5: numerical convergence.

Velocity Verlet is second order, and the implicit closing kick keeps it second order when
damping and driving are switched on. These tests measure the order from the numbers rather
than trusting the textbook: halve the step, the error must fall fourfold.
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import fourier, oscillators
from wavelab.validation import convergence_study, scaling_exponent

pytestmark = pytest.mark.convergence

MASS = 0.5
STIFFNESS = 8.0
OMEGA0 = oscillators.natural_frequency(MASS, STIFFNESS)
PERIOD = 2.0 * np.pi / OMEGA0
REFINEMENTS = [100, 200, 400, 800]
N_PERIODS = 3


def _final_position(steps_per_period: int, **kwargs: float) -> float:
    dt = PERIOD / steps_per_period
    trajectory = oscillators.simulate(
        MASS, STIFFNESS, 0.1, 0.2, dt, N_PERIODS * steps_per_period, **kwargs
    )
    return float(trajectory.positions[-1])


def test_integrator_is_second_order_for_the_free_oscillator():
    exact = float(
        oscillators.position(np.array([N_PERIODS * PERIOD]), MASS, STIFFNESS, 0.1, 0.2)[0]
    )
    study = convergence_study(_final_position, REFINEMENTS, exact)
    assert abs(study.observed_order - 2.0) < 0.2


def test_integrator_is_second_order_with_damping():
    """The implicit velocity kick must not cost an order: checked against the closed form."""
    damping = 0.4
    exact = float(
        oscillators.damped_position(
            np.array([N_PERIODS * PERIOD]), MASS, STIFFNESS, damping, 0.1, 0.2
        )[0]
    )
    study = convergence_study(
        lambda n: _final_position(n, damping=damping), REFINEMENTS, exact
    )
    assert abs(study.observed_order - 2.0) < 0.2


def test_integrator_is_second_order_when_driven():
    """No closed form for the transient-plus-steady-state mix, so the reference is a much
    finer integration of the same scheme; the order estimate is unaffected."""
    kwargs = {"damping": 0.4, "drive_amplitude": 1.0, "drive_omega": 3.0}
    reference = _final_position(51_200, **kwargs)
    study = convergence_study(
        lambda n: _final_position(n, **kwargs), REFINEMENTS, reference
    )
    assert abs(study.observed_order - 2.0) < 0.2


def test_simulated_steady_state_converges_to_the_closed_form_at_second_order():
    """Integrate past the transient, measure the amplitude, refine the step: error ~ dt^2.

    The closed form `steady_state_response` is the exact answer here, so this is the test
    that lets module 02's resonance curves be drawn from the formula while the laboratory
    draws them from an integration and expects the same picture.
    """
    damping = 0.4
    drive_omega = 3.4
    exact = float(
        abs(oscillators.steady_state_response(drive_omega, MASS, STIFFNESS, damping, 1.0))
    )

    def measured_amplitude(steps_per_period: int) -> float:
        dt = PERIOD / steps_per_period
        # 40/gamma leaves e^{-20} of the transient behind, four orders below the smallest
        # discretisation error measured here — otherwise the leftover transient, not dt,
        # would set the error floor and the fitted order would come out near zero.
        settle = 40.0 / oscillators.damping_rate(MASS, damping)
        n_steps = int(round((settle + 6.0 * PERIOD) / dt))
        trajectory = oscillators.simulate(
            MASS, STIFFNESS, 0.0, 0.0, dt, n_steps,
            damping=damping, drive_amplitude=1.0, drive_omega=drive_omega,
        )
        keep = trajectory.times >= settle
        # x^2 + (v/omega)^2 is A^2 at every sample of a pure sinusoid, so this reads the
        # amplitude without the O(dt^2) bias that taking the largest *sample* would add.
        x = trajectory.positions[keep]
        v = trajectory.velocities[keep]
        return float(np.sqrt(np.mean(x**2 + (v / drive_omega) ** 2)))

    study = convergence_study(measured_amplitude, REFINEMENTS, exact)
    assert abs(study.observed_order - 2.0) < 0.35


def test_time_step_recommendation_sits_in_the_convergent_regime():
    """max_stable_dt must land where the error is already small and still second order:
    a run at that step and one at half that step must differ by about a factor of four."""
    dt = oscillators.max_stable_dt(MASS, STIFFNESS)
    steps_per_period = round(PERIOD / dt)
    exact = float(
        oscillators.position(np.array([N_PERIODS * PERIOD]), MASS, STIFFNESS, 0.1, 0.2)[0]
    )
    error_at_dt = abs(_final_position(steps_per_period) - exact)
    error_at_half = abs(_final_position(2 * steps_per_period) - exact)
    assert error_at_dt / error_at_half == pytest.approx(4.0, rel=0.25)


# Fourier series convergence. Orders are odd so a waveform built from odd harmonics always
# includes its top term, and they double so the effective term count doubles with them. The
# grid resolves the jump region at the highest order while keeping `partial_sum`'s dense
# order-by-time matrix small enough to stay quick.
ORDERS = [15, 31, 63, 127, 255]
PHASE = np.linspace(0.0, 2.0 * np.pi, 20001)


def _partial_sum_error(coefficients: np.ndarray, exact: np.ndarray) -> float:
    """RMS distance between a partial sum and the waveform it is approximating."""
    reconstruction = fourier.partial_sum(coefficients, 1.0, PHASE)
    return float(np.sqrt(np.mean((reconstruction - exact) ** 2)))


def test_smoothness_sets_the_rate_a_fourier_series_converges():
    """A jump converges as N^(-1/2) in energy, a corner as N^(-3/2) — one law, two waveforms.

    This is the numerical face of the integration-by-parts argument: each degree of smoothness
    buys one more power of 1/n in the coefficients, and the L2 error inherits it. Testing both
    waveforms together is the point — either exponent alone could be a coincidence of scale,
    but the *gap* between them is the physics.

    Both fitted exponents land a little inside their asymptotes (-0.49 and -1.47 here) because
    these orders are finite; carried out to 511 harmonics they tighten to -0.495 and -1.484.
    The window is wide enough to admit that approach and far too narrow to admit the wrong
    exponent, which is what it is for.
    """
    square = np.sign(np.sin(PHASE))
    triangle = (2.0 / np.pi) * np.arcsin(np.sin(PHASE))

    square_errors = [_partial_sum_error(fourier.square_coefficients(n), square) for n in ORDERS]
    triangle_errors = [
        _partial_sum_error(fourier.triangle_coefficients(n), triangle) for n in ORDERS
    ]

    assert abs(scaling_exponent(ORDERS, square_errors) - (-0.5)) < 0.05
    assert abs(scaling_exponent(ORDERS, triangle_errors) - (-1.5)) < 0.05


def test_the_gibbs_overshoot_refuses_to_shrink_as_terms_are_added():
    """The falsifier for `more-terms-always-converge`, as a test rather than an assertion.

    Everything else about the approximation improves with N: the energy error falls, the
    wiggles narrow, the overshoot moves in toward the discontinuity. Its *height* does not
    move. Nine percent of the jump is where it stays, and no number of terms removes it.

    The plateau is approached from above — 9.21% at 7 harmonics, 8.949% by 511 — so the band
    below is centred on the limit and sized to the residue at the smallest order tested. A
    shrinking overshoot, which is what the misconception predicts, would leave it immediately.
    """
    overshoots = [fourier.gibbs_overshoot(n) for n in ORDERS]
    for order, overshoot in zip(ORDERS, overshoots, strict=True):
        assert abs(overshoot - 0.0895) < 0.001, f"overshoot at N = {order} left the plateau"
    assert max(overshoots) - min(overshoots) < 0.001


def test_the_sampled_force_integrator_is_second_order():
    """`simulate_forced` must inherit `simulate`'s order, not merely its interface.

    The drive is a three-harmonic sum rather than a square wave on purpose: a sampled
    discontinuity moves with the grid, so a genuinely second-order integrator would still show
    first-order error and the measurement would say nothing about the scheme.
    """
    damping, omega0_drive = 0.4, 1.2
    duration = 6.0 * 2.0 * np.pi / omega0_drive

    def force(times: np.ndarray) -> np.ndarray:
        return sum(np.cos(n * omega0_drive * times) / n for n in (1, 3, 5))

    def final_position(steps: int) -> float:
        dt = duration / steps
        samples = force(np.arange(steps + 1) * dt)
        run = oscillators.simulate_forced(MASS, STIFFNESS, 0.0, 0.0, dt, samples, damping=damping)
        return float(run.positions[-1])

    reference = final_position(64_000)
    study = convergence_study(final_position, [500, 1000, 2000, 4000], reference)
    assert abs(study.observed_order - 2.0) < 0.2
