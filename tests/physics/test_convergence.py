"""Accuracy category 5: numerical convergence.

Velocity Verlet is second order, and the implicit closing kick keeps it second order when
damping and driving are switched on. These tests measure the order from the numbers rather
than trusting the textbook: halve the step, the error must fall fourfold.
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import coupled, fourier, measurement, oscillators, waves
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


def _convolution_step_error(steps_per_period: int) -> float:
    """Worst-case distance between the convolved step response and its closed form."""
    dt = PERIOD / steps_per_period
    n = 6 * steps_per_period
    t = np.arange(n) * dt
    convolved = oscillators.convolution_response(np.ones(n), dt, MASS, STIFFNESS, 0.4)
    return float(np.max(np.abs(convolved - oscillators.step_response(t, MASS, STIFFNESS, 0.4))))


def test_convolving_a_step_converges_on_the_closed_form_at_second_order():
    """(G * F) against the analytic step response: halve the step, quarter the error.

    Second order is not what the discrete convolution gives by default. The FFT product is a
    rectangle-rule quadrature of the convolution integral, and its leading error term,
    -(dt/2) G(t) F(0), is first order — measurably so, falling only from 4.4e-3 to 5.6e-4 as
    the step is quartered. `convolution_response` gives the force's first sample the
    trapezoidal rule's half weight, which cancels that term; what remains is the O(dt^2) this
    test measures. The upper endpoint needs no matching correction because G(0) = 0.
    """
    errors = np.array([_convolution_step_error(n) for n in REFINEMENTS])
    ratios = errors[:-1] / errors[1:]
    assert np.all(np.abs(ratios - 4.0) < 1.0), f"error ratios {ratios} are not fourfold"


def test_convolution_and_verlet_agree_on_a_burst_as_the_step_refines():
    """Two unrelated routes to the same motion: superposition of kicks, and integration.

    `simulate_forced` knows nothing about Green functions and `convolution_response` knows
    nothing about time stepping, so their agreement is a real check on both — and it must
    improve at second order, since that is the order each of them separately claims.
    """
    damping = 0.4
    errors = []
    for steps_per_period in REFINEMENTS:
        dt = PERIOD / steps_per_period
        n = 6 * steps_per_period
        t = np.arange(n) * dt
        force = np.where(t < 3.0 * PERIOD, np.cos(1.9 * t), 0.0)
        integrated = oscillators.simulate_forced(
            MASS, STIFFNESS, 0.0, 0.0, dt, force, damping=damping
        )
        convolved = oscillators.convolution_response(force, dt, MASS, STIFFNESS, damping)
        errors.append(float(np.max(np.abs(convolved - integrated.positions))))

    ratios = np.array(errors[:-1]) / np.array(errors[1:])
    assert np.all(np.abs(ratios - 4.0) < 1.0), f"error ratios {ratios} are not fourfold"


def test_the_lti_bridge_is_limited_by_the_record_before_it_is_limited_by_the_step():
    """Two error sources sit under `spectrum(impulse_response)`, and the record wins first.

    Refining the grid cannot fix a ringdown that has not finished ringing: the DFT's periodic
    extension wraps whatever is left at the end of the record back onto the start. Measured at
    Q = 20, holding dt fixed at 0.01 and doubling the record, the relative error against the
    conjugate swept response tracks the surviving tail amplitude e^{-gamma T / 4} almost
    exactly — 2.9e-4 at 8.2 amplitude e-foldings, 6.8e-6 at 16.4 — and then stops falling,
    pinned at the 6.7e-6 the grid alone can support.

    This is why the identity test in `test_limits.py` asserts a floor rather than an
    algebraic equality, and why a laboratory reading a short record should expect the same.
    """
    damping = 0.1  # Q = 20
    dt = 0.01
    gamma = oscillators.damping_rate(MASS, damping)

    errors = {}
    for n in (2**14, 2**15, 2**16):
        t = (np.arange(n) - n // 2) * dt
        omega, kicked = fourier.spectrum(
            oscillators.impulse_response(t, MASS, STIFFNESS, damping), dt
        )
        band = (omega >= 0.0) & (omega < 3.0 * OMEGA0)
        swept = oscillators.steady_state_response(omega[band], MASS, STIFFNESS, damping, 1.0)
        errors[n] = float(
            np.max(np.abs(kicked[band] - np.conj(swept))) / np.max(np.abs(swept))
        )

    # Truncation-limited: the error is the tail the record failed to contain.
    tail = np.exp(-gamma * (2**14 * dt) / 4.0)
    assert errors[2**14] == pytest.approx(tail, rel=0.25)

    # Doubling the record clears the tail; doubling it again changes nothing, because the
    # grid is now what is left.
    assert errors[2**15] < errors[2**14] / 10.0
    assert errors[2**16] == pytest.approx(errors[2**15], rel=0.05)


# A chain of masses becoming a string. This is the only convergence in the file that is not
# about an integrator: the refinement is physical — more masses, closer together — and what
# converges is the model rather than the arithmetic. Refinement is counted in springs, N + 1,
# because that is the mesh: N + 1 springs span the length L = (N + 1) a, and fitting against N
# instead reports 1.95 where the mathematics says 2.
CHAIN_SIZES = [10, 20, 40, 80, 160]


def _continuum_ratio(springs: int, mode: int) -> float:
    """Mode `mode` of a chain with `springs` springs, over the string frequency it tends to."""
    n = springs - 1
    return float(
        coupled.chain_mode_frequencies(n, MASS, STIFFNESS)[mode - 1]
        / coupled.chain_continuum_frequencies(n, MASS, STIFFNESS)[mode - 1]
    )


def test_the_chains_low_modes_converge_on_the_string_at_second_order():
    """omega_p -> p pi c / L, with the error falling as 1/N^2 — the module's headline number.

    The continuum limit is a claim about a model, so the honest way to state it is with a
    rate. Expanding sin x = x - x^3/6 in the closed form predicts a relative error of
    (p pi)^2 / (24 (N+1)^2): second order, and the measurement returns 2.000, 1.999, 1.997 for
    the first three modes. The prediction is not merely of the right order — it is right to
    three figures in the errors themselves, 3.40e-3 against 3.40e-3 at N = 10.

    Independence of the physical constants is worth noting: the *relative* error is
    sin(x)/x - 1 with x = p pi / (2(N+1)), so it carries no mass and no stiffness at all. A
    chain of any material converges at the same rate.
    """
    for mode in (1, 2, 3):
        study = convergence_study(
            lambda springs, p=mode: _continuum_ratio(springs, p),
            [n + 1 for n in CHAIN_SIZES],
            1.0,
        )
        assert abs(study.observed_order - 2.0) < 0.05

        predicted = (mode * np.pi) ** 2 / (24.0 * study.refinements**2)
        assert np.allclose(study.errors, predicted, rtol=0.02)


def test_the_continuum_error_grows_as_the_square_of_the_mode_number():
    """Which is why "N masses represent a string" has an upper edge, not just a rate.

    The same expansion that gives the 1/N^2 also gives a p^2, so the accuracy runs out from
    the top of the band downwards. At N = 100 mode 1 is right to 4.0e-5 and mode 16 to 1.0e-2,
    a factor of 256 for a factor of 16 in p — fitted exponent 1.999. The band edge never
    converges at all: mode 100 of a 100-chain sits 36% below the string frequency it is
    supposed to be approaching, however large N grows, because there the chain's discreteness
    is the whole story.
    """
    n = 100
    chain = coupled.chain_mode_frequencies(n, MASS, STIFFNESS)
    string = coupled.chain_continuum_frequencies(n, MASS, STIFFNESS)
    modes = np.array([1, 2, 4, 8, 16])
    errors = np.abs(chain[modes - 1] - string[modes - 1]) / string[modes - 1]

    assert abs(scaling_exponent(modes, errors) - 2.0) < 0.05
    assert errors[0] < 1e-4
    assert abs(chain[-1] - string[-1]) / string[-1] > 0.3


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


# The string, refined. A 4 m string at v = 20 m/s with a Gaussian pluck of width 0.1 m at its
# centre. Runs last 0.05 s, so each half travels 1 m and stays ten widths clear of the walls,
# which keeps d'Alembert's unbounded-line solution the exact answer for the whole run. The
# Courant number S = v dt / dx is held fixed while the grid refines, so dt refines with dx.
STRING_TENSION = 4.0
STRING_MU = 0.01
STRING_SPEED = waves.wave_speed(STRING_TENSION, STRING_MU)
STRING_LENGTH = 4.0
STRING_RUN = 0.05
STRING_AMPLITUDE = 0.01


def _pluck(s: np.ndarray) -> np.ndarray:
    return STRING_AMPLITUDE * np.exp(-(((s - 2.0) / 0.1) ** 2))


def _moving(s: np.ndarray) -> np.ndarray:
    """A right-moving pulse's shape, started at 1.5 m."""
    return STRING_AMPLITUDE * np.exp(-(((s - 1.5) / 0.1) ** 2))


def _moving_slope(s: np.ndarray) -> np.ndarray:
    return -2.0 * (s - 1.5) / 0.1**2 * _moving(s)


def _string_errors(
    cells: int, courant: float, moving: bool = False, steps: list[int] | None = None
) -> np.ndarray:
    """Largest error at each of `steps` (default: all) against d'Alembert, per unit amplitude."""
    dx = STRING_LENGTH / cells
    x = np.arange(cells + 1) * dx
    dt = courant * dx / STRING_SPEED
    n_steps = int(round(STRING_RUN / dt))
    if moving:
        # A right-mover starts with y_t = -v y_x, whose antiderivative is -v y itself.
        shape, integral = _moving, lambda s: -STRING_SPEED * _moving(s)
        run = waves.simulate_string(
            _moving(x), -STRING_SPEED * _moving_slope(x), dx, dt, STRING_TENSION, STRING_MU,
            n_steps,
        )
    else:
        shape, integral = _pluck, None
        run = waves.simulate_string(
            _pluck(x), np.zeros_like(x), dx, dt, STRING_TENSION, STRING_MU, n_steps
        )
    rows = slice(None) if steps is None else steps
    exact = waves.dalembert_solution(
        shape, STRING_SPEED, x, run.times[rows], v0_integral=integral
    )
    return np.max(np.abs(run.y[rows] - exact), axis=1) / STRING_AMPLITUDE


def test_the_string_solver_converges_on_dalembert_at_second_order():
    """Halve the grid spacing at fixed Courant number and the error falls fourfold.

    The error here is grid dispersion — short wavelengths travelling slightly too slowly — and
    its size is (k dx)^2 (1 - S^2) / 24 in the phase, second order in dx for any S below one.
    Measured against the exact solution in the L2 norm, the ratios between successive grids are
    3.996, 4.002, 4.001, 4.000, and the fitted exponent is -2.000.

    This is the gate the plan puts in front of every published frame: nothing is rendered from
    a solver that has not first been shown to converge on the answer.
    """
    cells = [200, 400, 800, 1600, 3200]
    errors = []
    for n in cells:
        dx = STRING_LENGTH / n
        x = np.arange(n + 1) * dx
        dt = 0.5 * dx / STRING_SPEED
        n_steps = int(round(STRING_RUN / dt))
        run = waves.simulate_string(
            _pluck(x), np.zeros_like(x), dx, dt, STRING_TENSION, STRING_MU, n_steps
        )
        exact = waves.dalembert_solution(_pluck, STRING_SPEED, x, run.times[-1])
        errors.append(float(np.linalg.norm(run.y[-1] - exact) / np.linalg.norm(exact)))

    assert abs(scaling_exponent(cells, errors) - (-2.0)) < 0.02
    ratios = np.array(errors[:-1]) / np.array(errors[1:])
    assert np.all(np.abs(ratios - 4.0) < 0.1), f"error ratios {ratios} are not fourfold"


def test_at_the_magic_step_a_pluck_is_exact_and_nothing_else_is():
    """S = 1 transports the pluck with no error at all; S = 0.99 and a moving start do not.

    At S = 1 the stencil reads y_i^{n+1} = y_{i+1}^n + y_{i-1}^n - y_i^{n-1}, which carries any
    travelling shape exactly one grid spacing per step, provided the first two steps are exact.
    A pluck supplies them, and 400 steps later its two halves match d'Alembert to 5.9e-15 of
    the amplitude. At S = 0.99 on the same grid the error is 1.0e-5: ten orders of magnitude for
    a one-percent change in the step, which is why this is a special step and not a good one.

    A pulse started moving is the honest limit of the trick. Its second step is off by O(dt^3)
    — 8.1e-5, 1.0e-5, 1.3e-6 on successive grids, eightfold — and the exact transport then
    spreads that defect into a second-order error that stops growing: 4.2e-4, 1.0e-4, 2.6e-5
    at the end of the run. Still 7.5 times smaller than S = 0.5 gives on each grid, but no longer
    exact, and the module does not claim it is.
    """
    assert _string_errors(1600, 1.0).max() < 1e-13
    assert _string_errors(1600, 0.99).max() > 1e-6

    grids = [800, 1600, 3200]
    first, final = np.array([_string_errors(n, 1.0, True, [1, -1]) for n in grids]).T
    assert np.all(np.abs(first[:-1] / first[1:] - 8.0) < 1.0)
    assert np.all(np.abs(final[:-1] / final[1:] - 4.0) < 0.3)

    below_magic = np.array([_string_errors(n, 0.5, True, [-1])[0] for n in grids])
    assert np.all(below_magic / final > 5.0)


def test_past_the_courant_limit_the_grid_scale_grows_at_the_von_neumann_rate():
    """Cross S = 1 and the shortest wave the grid holds multiplies itself every step.

    Substituting y_i^n = g^n e^{i k i dx} into the stencil gives
    g^2 - 2(1 - 2 S^2 sin^2(k dx / 2)) g + 1 = 0, whose roots stay on the unit circle for S <= 1
    and leave it for S > 1, worst at k dx = pi, where |g| = (2S^2 - 1) + sqrt((2S^2 - 1)^2 - 1).
    The instability grows from rounding error and nothing else, so the smooth pulse is
    irrelevant to it: at S = 1.01 the displacement passes ten times the pulse's amplitude after
    140 steps, and the growth measured from the run matches the formula to 0.3-0.4% at
    S = 1.01, 1.05 and 1.1. At S = 0.99 two thousand steps leave the amplitude where it was.

    This is a numerics statement, not physics — the string itself is perfectly stable — and the
    solver refuses the step unless told that watching it fail is the point.
    """
    cells = 400
    dx = 1.0 / cells
    x = np.arange(cells + 1) * dx
    pluck = STRING_AMPLITUDE * np.exp(-(((x - 0.5) / 0.05) ** 2))
    still = np.zeros_like(x)

    for courant in (1.01, 1.05, 1.1):
        dt = courant * dx / STRING_SPEED
        run = waves.simulate_string(
            pluck, still, dx, dt, STRING_TENSION, STRING_MU, 400, allow_unstable=True
        )
        peak = np.max(np.abs(run.y), axis=1)
        # Past a hundred times the pulse, the grid-scale mode is all there is; before overflow.
        growing = np.nonzero(np.isfinite(peak) & (peak > 1.0) & (peak < 1e100))[0][:60]
        measured = float(np.exp(np.polyfit(growing, np.log(peak[growing]), 1)[0]))
        b = 2.0 * courant**2 - 1.0
        assert np.isclose(measured, b + np.sqrt(b**2 - 1.0), rtol=0.01)

    stable = waves.simulate_string(
        pluck, still, dx, 0.99 * dx / STRING_SPEED, STRING_TENSION, STRING_MU, 2000
    )
    assert np.max(np.abs(stable.y)) <= STRING_AMPLITUDE * (1.0 + 1e-9)

    with pytest.raises(ValueError, match="Courant"):
        waves.simulate_string(
            pluck, still, dx, 1.01 * dx / STRING_SPEED, STRING_TENSION, STRING_MU, 10
        )
    # The bound's own step must be accepted, though v dt / dx lands a rounding away from 1.
    bound = waves.cfl_max_dt(dx, STRING_SPEED)
    waves.simulate_string(pluck, still, dx, bound, STRING_TENSION, STRING_MU, 10)


# Two photogates on a 2 m string. The pluck at 0.8 m has width 0.05 m, twenty grid spacings, and
# its right-moving half passes gates at 1.2 m and 1.6 m before anything reflected can arrive.
GATE_CELLS = 800
GATE_DX = 2.0 / GATE_CELLS
GATE_A, GATE_B = 480, 640
GATE_WIDTH = 0.05


def _gate_records(courant: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.arange(GATE_CELLS + 1) * GATE_DX
    dt = courant * GATE_DX / STRING_SPEED
    n_steps = int(np.ceil(1.1 / STRING_SPEED / dt))
    pluck = STRING_AMPLITUDE * np.exp(-(((x - 0.8) / GATE_WIDTH) ** 2))
    run = waves.simulate_string(
        pluck, np.zeros_like(x), GATE_DX, dt, STRING_TENSION, STRING_MU, n_steps
    )
    return run.times, run.y[:, GATE_A], run.y[:, GATE_B]


def _peak_time(times: np.ndarray, record: np.ndarray) -> float:
    """The top of the record, refined between samples by the three-point parabola vertex."""
    i = int(np.argmax(record))
    before, top, after = record[i - 1 : i + 2]
    return float(
        times[i] + 0.5 * (before - after) / (before - 2.0 * top + after) * (times[1] - times[0])
    )


def test_grid_dispersion_slows_the_peak_of_a_pulse_but_not_its_centroid():
    """A photogate on a computed string reads slow if it times the peak — by a predictable amount.

    Leapfrog's dispersion relation, sin(omega dt / 2) = S sin(k dx / 2), makes short waves lag.
    For a Gaussian pulse of width sigma that drags the peak back at the relative rate
    (1 - S^2)(dx / sigma)^2 / 4, derived by expanding the relation to third order in k; the
    peak-timed speeds match it to 0.12%, 0.07% and 0.38% at S = 0.25, 0.5 and 0.75, and at
    S = 1, where the scheme has no dispersion at all, they read v exactly.

    Timing the centroid instead reads v to 3e-9 at every S. That is not luck: the first moment
    of the displacement only responds to the dispersion relation's slope at k = 0, and there the
    grid is exact. It is also the reason the laboratory times its photogates by centroid, and a
    trap worth knowing about — the same pulse, the same grid, and two answers that disagree in
    the fourth figure depending on which feature of the pulse is called its arrival.
    """
    distance = (GATE_B - GATE_A) * GATE_DX
    half_window = 4.0 * GATE_WIDTH / STRING_SPEED
    for courant in (0.25, 0.5, 0.75, 1.0):
        times, first, second = _gate_records(courant)

        by_peak = distance / (_peak_time(times, second) - _peak_time(times, first))
        predicted = -(1.0 - courant**2) * (GATE_DX / GATE_WIDTH) ** 2 / 4.0
        bias = by_peak / STRING_SPEED - 1.0
        if courant < 1.0:
            assert np.isclose(bias, predicted, rtol=0.01)
        else:
            assert abs(bias) < 1e-12

        by_centroid = distance / (
            measurement.pulse_arrival_time(times, second, half_window)
            - measurement.pulse_arrival_time(times, first, half_window)
        )
        assert abs(by_centroid / STRING_SPEED - 1.0) < 1e-7
