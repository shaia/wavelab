"""Accuracy category 5: numerical convergence.

Velocity Verlet is second order, and the implicit closing kick keeps it second order when
damping and driving are switched on. These tests measure the order from the numbers rather
than trusting the textbook: halve the step, the error must fall fourfold.
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import oscillators
from wavelab.validation import convergence_study

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
