"""Accuracy category 2: conservation.

The undamped oscillator conserves energy exactly; its symplectic integrator must keep the
energy error *bounded* — oscillating with amplitude (omega0 dt)^2 / 4 — rather than letting
it drift. Damping must only ever remove energy, and a driven steady state must not run away.
"""

from __future__ import annotations

import numpy as np
import pytest

from wavelab import coupled, fourier, oscillators, waves

pytestmark = pytest.mark.conservation

MASS = 0.5
STIFFNESS = 8.0
OMEGA0 = oscillators.natural_frequency(MASS, STIFFNESS)
PERIOD = 2.0 * np.pi / OMEGA0


def _long_run(n_periods: int = 100) -> tuple[oscillators.Trajectory, int]:
    dt = oscillators.max_stable_dt(MASS, STIFFNESS)
    steps_per_period = round(PERIOD / dt)
    trajectory = oscillators.simulate(
        MASS, STIFFNESS, 0.1, 0.0, dt, n_periods * steps_per_period
    )
    return trajectory, steps_per_period


def test_energy_error_stays_bounded_over_a_hundred_periods():
    """Velocity Verlet's energy error oscillates at (omega0 dt)^2/4 and must not exceed it."""
    trajectory, _ = _long_run()
    _, _, total = oscillators.energies(
        trajectory.positions, trajectory.velocities, MASS, STIFFNESS
    )
    bound = (OMEGA0 * oscillators.max_stable_dt(MASS, STIFFNESS)) ** 2 / 4.0
    assert (total.max() - total.min()) / total[0] < 1.5 * bound


def test_energy_shows_no_secular_drift():
    """Bounded oscillation is symplecticity's promise; the *mean* energy must not walk.

    A non-symplectic scheme (plain Euler, RK4 at this step size) fails this by orders of
    magnitude: its energy error accumulates monotonically instead of averaging out.
    """
    trajectory, steps_per_period = _long_run()
    _, _, total = oscillators.energies(
        trajectory.positions, trajectory.velocities, MASS, STIFFNESS
    )
    first_period = total[:steps_per_period].mean()
    last_period = total[-steps_per_period:].mean()
    assert abs(last_period - first_period) / total[0] < 1e-7


def test_phase_space_trajectory_stays_on_its_ellipse():
    """omega0^2 x^2 + v^2 is energy in disguise; the orbit must not spiral in or out."""
    trajectory, _ = _long_run()
    radius_sq = OMEGA0**2 * trajectory.positions**2 + trajectory.velocities**2
    bound = (OMEGA0 * oscillators.max_stable_dt(MASS, STIFFNESS)) ** 2 / 4.0
    assert (radius_sq.max() - radius_sq.min()) / radius_sq[0] < 1.5 * bound


def test_closed_form_conserves_energy_to_roundoff():
    """The analytic solution has no excuse: its energy is constant to machine precision."""
    t = np.linspace(0.0, 50.0 * PERIOD, 20001)
    x = oscillators.position(t, MASS, STIFFNESS, 0.1, 0.3)
    v = oscillators.velocity(t, MASS, STIFFNESS, 0.1, 0.3)
    _, _, total = oscillators.energies(x, v, MASS, STIFFNESS)
    assert (total.max() - total.min()) / total[0] < 1e-12


def test_damping_only_removes_energy():
    """With b > 0 and no drive, dE/dt = -b v^2 <= 0: the energy must never increase."""
    dt = oscillators.max_stable_dt(MASS, STIFFNESS)
    trajectory = oscillators.simulate(
        MASS, STIFFNESS, 0.1, 0.0, dt, 5000, damping=0.4
    )
    _, _, total = oscillators.energies(
        trajectory.positions, trajectory.velocities, MASS, STIFFNESS
    )
    increases = np.diff(total)
    assert increases.max() <= total[0] * 1e-12


def test_steady_state_input_power_equals_dissipated_power():
    """In the steady state the books balance: <F v> = <b v^2> = `power_absorbed`.

    Both averages are taken from an integration, not from the formula, so the closed form is
    on trial here rather than being assumed. This is where module 02's "the energy has to go
    somewhere" claim stops being rhetoric.
    """
    damping = 0.4
    drive_omega = 3.4
    force_amplitude = 1.0
    dt = PERIOD / 800.0
    trajectory = oscillators.simulate(
        MASS, STIFFNESS, 0.0, 0.0, dt, 80_000,
        damping=damping, drive_amplitude=force_amplitude, drive_omega=drive_omega,
    )

    # Whole cycles only, well past the 2/gamma transient, so the means are unbiased.
    cycle_steps = round(2.0 * np.pi / drive_omega / dt)
    tail = slice(-40 * cycle_steps, None)
    times = trajectory.times[tail]
    velocities = trajectory.velocities[tail]
    drive = force_amplitude * np.cos(drive_omega * times)

    input_power = float(np.mean(drive * velocities))
    dissipated = float(np.mean(damping * velocities**2))
    predicted = float(
        oscillators.power_absorbed(drive_omega, MASS, STIFFNESS, damping, force_amplitude)
    )

    assert np.isclose(input_power, dissipated, rtol=2e-3)
    assert np.isclose(input_power, predicted, rtol=2e-3)


def test_ringdown_energy_decays_at_gamma():
    """A free damped oscillation loses energy as e^{-gamma t}: amplitude decays at half that.

    Measured from the integration by fitting the log of the per-period energy, so it tests
    the integrator and the closed-form damping rate against each other.
    """
    damping = 0.2
    gamma = oscillators.damping_rate(MASS, damping)
    dt = oscillators.max_stable_dt(MASS, STIFFNESS)
    steps_per_period = round(PERIOD / dt)
    trajectory = oscillators.simulate(
        MASS, STIFFNESS, 0.1, 0.0, dt, 20 * steps_per_period, damping=damping
    )
    _, _, total = oscillators.energies(
        trajectory.positions, trajectory.velocities, MASS, STIFFNESS
    )

    n_periods = 20
    per_period = np.array(
        [total[i * steps_per_period : (i + 1) * steps_per_period].mean() for i in range(n_periods)]
    )
    period_times = (np.arange(n_periods) + 0.5) * PERIOD
    measured_gamma = -float(np.polyfit(period_times, np.log(per_period), 1)[0])
    assert np.isclose(measured_gamma, gamma, rtol=1e-2)


def test_driven_oscillator_energy_stays_bounded():
    """The damped driven oscillator settles into a steady state instead of running away."""
    dt = oscillators.max_stable_dt(MASS, STIFFNESS)
    trajectory = oscillators.simulate(
        MASS,
        STIFFNESS,
        0.0,
        0.0,
        dt,
        40_000,
        damping=0.4,
        drive_amplitude=1.0,
        drive_omega=OMEGA0,
    )
    _, _, total = oscillators.energies(
        trajectory.positions, trajectory.velocities, MASS, STIFFNESS
    )
    steady_state = abs(
        oscillators.driven_amplitude(OMEGA0, MASS, STIFFNESS, 0.4, 1.0)
    )
    energy_cap = 0.5 * STIFFNESS * (2.0 * steady_state) ** 2
    assert total.max() < energy_cap


def test_a_kick_deposits_exactly_the_kinetic_energy_it_carries():
    """An impulse J leaves J^2/2m in the oscillator, all of it kinetic, none of it potential.

    This is the energy face of the Green function's initial condition. The kick changes the
    velocity and nothing else, so at t = 0+ the spring is still slack: every joule is kinetic,
    and the total is (1/2) m v^2 with v = J/m. Read off the response itself rather than
    asserted about it, so that a mis-scaled G would fail here as well as in the limits file.
    """
    damping = 0.4
    impulse = 3.0
    dt = PERIOD / 20_000.0
    t = np.arange(4) * dt

    green = oscillators.impulse_response(t, MASS, STIFFNESS, damping)
    velocity = float(np.gradient(green, dt)[0]) * impulse
    assert np.isclose(velocity, impulse / MASS, rtol=1e-3)

    kinetic, potential, total = oscillators.energies(
        np.array([0.0]), np.array([impulse / MASS]), MASS, STIFFNESS
    )
    assert np.isclose(float(total[0]), impulse**2 / (2.0 * MASS), rtol=1e-12)
    assert float(kinetic[0]) == float(total[0])
    assert float(potential[0]) == 0.0


def test_the_convolved_response_never_outlasts_the_energy_put_into_it():
    """Damping only removes: a bounded force cannot leave the oscillator gaining energy.

    A burst is applied and then switched off, and from that moment the mechanical energy of
    the convolved response must decrease monotonically over whole half cycles. It is the
    check that `convolution_response`'s zero padding really did stop the DFT's periodic
    extension from wrapping the tail back onto the start, which would show up here as energy
    reappearing after the force has gone.
    """
    damping = 0.4
    dt = PERIOD / 400.0
    n = 4000
    t = np.arange(n) * dt
    force = np.where(t < 3.0 * PERIOD, np.cos(OMEGA0 * t), 0.0)

    x = oscillators.convolution_response(force, dt, MASS, STIFFNESS, damping)
    v = np.gradient(x, dt)
    _, _, total = oscillators.energies(x, v, MASS, STIFFNESS)

    after = t > 3.5 * PERIOD
    per_half_cycle = total[after][: (total[after].size // 200) * 200].reshape(-1, 200).max(axis=1)
    assert np.all(np.diff(per_half_cycle) < 0.0)


def test_modal_energies_hold_still_while_site_energies_slosh():
    """The whole point of a normal mode, as one assertion pair.

    Two identical oscillators are released with only the first displaced, and the same
    trajectory is read twice. In the site picture the energy travels: mass 1's share runs the
    full range from essentially all of it to essentially none. In the mode picture nothing
    happens at all — each mode holds its energy to a part in 10^5, for as long as the
    integration runs.

    Neither statement is an identity being restated. `simulate_coupled` steps the coupled
    equations and knows nothing about modes; the modal energies are computed afterwards, by
    projection. That they come out constant is a fact about the physics.

    The tolerance is set by the integrator, not by the physics. Velocity Verlet is symplectic,
    so its modal-energy error is a bounded oscillation of order (omega dt)^2 rather than a
    drift: 1.5e-5 at dt = T_fast/800, and 9.6e-7 at T_fast/3200 for anyone who wants it
    tighter at four times the cost. The bound not growing with run length is checked below,
    and matters more than its size.
    """
    coupling = 0.05 * STIFFNESS
    matrices = coupled.two_mass_matrices(MASS, STIFFNESS, coupling)
    modes = coupled.normal_mode_solve(*matrices)
    period = coupled.exchange_time(*modes.frequencies)
    dt = (2.0 * np.pi / modes.frequencies[-1]) / 800.0

    trajectory = coupled.simulate_coupled(
        *matrices, [1.0, 0.0], [0.0, 0.0], dt, int(3.0 * period / dt)
    )
    site = coupled.site_energies(*matrices, trajectory.positions, trajectory.velocities)
    modal = np.array(
        [
            coupled.modal_energies(modes, x, v)
            for x, v in zip(trajectory.positions, trajectory.velocities, strict=True)
        ]
    )

    reference = modal[0].sum()
    assert np.max(np.abs(modal - modal[0])) / reference < 1e-4

    # ... while the site energies traverse essentially the whole total.
    share = site[:, 0] / site.sum(axis=1)
    assert share.max() - share.min() > 0.95


# The same statement on a chain, where there are twenty modes rather than two and no pair of
# them is in any privileged relationship. CHAIN_STIFFNESS is the spring between neighbours;
# the fastest mode of a fixed chain runs at 2 sqrt(k_s/m) whatever its length.
CHAIN_SIZE = 20
CHAIN_STIFFNESS = 8.0


def _chain_run(steps_per_fast_period: int, slow_periods: float):
    """A seeded random start on the N = 20 chain, integrated and read both ways.

    The start is random rather than a pluck on purpose. A plucked shape is symmetric, so
    every even mode gets exactly zero energy, and "this mode's energy is unchanged" then says
    nothing about half the spectrum — worse, the relative drift of a mode holding 1e-31 of the
    total is meaningless and enormous. A random state gives every mode a real share (the
    smallest here is 0.2% of the total), which is what makes a *per-mode* claim checkable.
    """
    matrices = coupled.chain_matrices(CHAIN_SIZE, MASS, CHAIN_STIFFNESS)
    modes = coupled.normal_mode_solve(*matrices)
    generator = np.random.default_rng(11)
    x0 = generator.normal(0.0, 0.02, CHAIN_SIZE)
    v0 = generator.normal(0.0, 0.05, CHAIN_SIZE)

    dt = (2.0 * np.pi / modes.frequencies[-1]) / steps_per_fast_period
    slowest = 2.0 * np.pi / modes.frequencies[0]
    run = coupled.simulate_coupled(*matrices, x0, v0, dt, int(slow_periods * slowest / dt))
    modal = coupled.modal_energies(modes, run.positions, run.velocities)
    site = coupled.site_energies(*matrices, run.positions, run.velocities)
    return modal, site


def test_every_mode_of_the_chain_keeps_its_energy_while_the_masses_trade_theirs():
    """Twenty modes, twenty constants — and twenty masses that share nothing of the kind.

    Module 06 showed this for two oscillators, where "the modes do not exchange" could still
    be read as a curiosity of a small system. It is not: `simulate_coupled` steps twenty
    coupled equations with no notion of a mode in it, and every one of the twenty modal
    energies computed afterwards by projection comes back unchanged.

    The tolerance is the integrator's and is quoted per mode rather than against the total,
    which is the stricter of the two readings: 2.5e-4 of each mode's own energy at
    dt = T_fast/200, falling fourfold with the step, against 8.5e-5 of the total. The total's
    own wobble is 1.6e-4, larger than either, because it is the sum of twenty contributions
    that do not conspire to cancel. Meanwhile the site energies swing across a third of the
    total, so the two pictures are being read off one and the same trajectory and disagreeing
    completely about what is constant.
    """
    modal, site = _chain_run(steps_per_fast_period=200, slow_periods=3.0)
    initial = modal[0]

    assert np.max(np.abs(modal - initial) / initial) < 1e-3

    shares = site / site.sum(axis=1, keepdims=True)
    assert np.max(np.ptp(shares, axis=0)) > 0.2
    assert np.ptp(site.sum(axis=1)) / site.sum(axis=1)[0] < 1e-3


def test_the_chains_modal_energy_error_is_bounded_rather_than_drifting():
    """Four times the run, the same bound — the symplectic guarantee at twenty degrees of freedom.

    This is the check that licenses the module's long experiments. A drifting integrator would
    turn the module's central claim into an artefact that merely takes a while to appear, and
    the only way to tell the two apart is to run longer and look again.
    """
    bounds = [
        float(np.max(np.abs(modal - modal[0])) / modal[0].sum())
        for modal, _ in (_chain_run(200, periods) for periods in (2.0, 8.0))
    ]
    assert bounds[1] < 1.5 * bounds[0], f"error grows with run length: {bounds}"


def test_the_modal_energy_error_is_bounded_rather_than_drifting():
    """Run four times as long and the error must not grow — the symplectic guarantee.

    A non-symplectic integrator of the same order would look fine over one exchange period and
    leak steadily over twenty. Measuring the bound at two run lengths is what tells the two
    apart, and it is the reason this integrator can be trusted for the long exchange
    experiments the module's laboratory asks for.
    """
    matrices = coupled.two_mass_matrices(MASS, STIFFNESS, 0.05 * STIFFNESS)
    modes = coupled.normal_mode_solve(*matrices)
    period = coupled.exchange_time(*modes.frequencies)
    dt = (2.0 * np.pi / modes.frequencies[-1]) / 400.0

    bounds = []
    for periods in (2.0, 8.0):
        run = coupled.simulate_coupled(
            *matrices, [1.0, 0.0], [0.0, 0.0], dt, int(periods * period / dt)
        )
        modal = np.array(
            [
                coupled.modal_energies(modes, x, v)
                for x, v in zip(run.positions, run.velocities, strict=True)
            ]
        )
        bounds.append(float(np.max(np.abs(modal - modal[0])) / modal[0].sum()))

    assert bounds[1] < 1.5 * bounds[0], f"error grows with run length: {bounds}"


# Harmonic analysis conserves energy too: changing representation must not create or destroy
# any. Parseval is that statement, and it holds in both the periodic and the sampled worlds.
FOURIER_SAMPLES = 4096
FOURIER_DT = 0.01


def test_parseval_holds_for_the_fourier_coefficients():
    """Mean square in time equals the sum of |c_n|^2 — the harmonics carry all the power.

    The signal is built from a finite coefficient set, so it is exactly band-limited and the
    identity is exact rather than approximate: nothing is hiding above the cutoff. That makes
    a failure here unambiguous, which a truncated waveform could not.
    """
    coefficients = fourier.triangle_coefficients(9)
    phase = 2.0 * np.pi * np.arange(FOURIER_SAMPLES) / FOURIER_SAMPLES
    signal = fourier.partial_sum(coefficients, 1.0, phase)

    assert np.isclose(np.sum(np.abs(coefficients) ** 2), np.mean(signal**2), rtol=1e-12)
    recovered = fourier.fourier_coefficients(signal, 9)
    assert np.max(np.abs(recovered - coefficients)) < 1e-12


def test_parseval_holds_for_a_sampled_spectrum():
    """Energy in the record equals energy in its spectrum, once the 1/(2 pi) is respected.

    This is the identity that lets a later module read a spectrum panel as an energy budget
    rather than a picture, and it is where a wrong transform scaling would show up first.
    """
    times = (np.arange(FOURIER_SAMPLES) - FOURIER_SAMPLES // 2) * FOURIER_DT
    signal = fourier.gaussian_pulse(times, 0.3) * np.cos(12.0 * times)
    omega, transform = fourier.spectrum(signal, FOURIER_DT)

    time_energy = np.sum(np.abs(signal) ** 2) * FOURIER_DT
    spectral_energy = np.sum(np.abs(transform) ** 2) * (omega[1] - omega[0]) / (2.0 * np.pi)
    assert np.isclose(time_energy, spectral_energy, rtol=1e-10)


def test_the_spectrum_round_trips_through_its_inverse():
    """Analysis then synthesis returns the signal to machine precision, losing nothing.

    Module 12 propagates wave packets by transforming, multiplying by a phase, and
    transforming back, so any loss here would accumulate into that calculation rather than
    announcing itself.
    """
    times = (np.arange(FOURIER_SAMPLES) - FOURIER_SAMPLES // 2) * FOURIER_DT
    signal = fourier.gaussian_pulse(times, 0.4) * np.cos(9.0 * times)
    _, transform = fourier.spectrum(signal, FOURIER_DT)
    restored = fourier.inverse_spectrum(transform, FOURIER_DT)

    assert np.max(np.abs(restored - signal)) < 1e-12
    assert np.max(np.abs(restored.imag)) < 1e-12


# The string between two walls. A metre of it at v = 20 m/s on 400 cells, plucked with a
# Gaussian twenty cells wide, and run for ten transits and more so that the pulses hit the
# ends — and each other — over and over. Energy is read at up to 4000 evenly spaced samples;
# the wobble repeats every transit, so a longer run would measure the same numbers slower.
STRING_TENSION = 4.0
STRING_MU = 0.01
STRING_CELLS = 400
STRING_DX = 1.0 / STRING_CELLS


def _string_energy(
    courant: float,
    transits: float,
    boundary: tuple[str, str] = ("fixed", "fixed"),
    mu: float | np.ndarray = STRING_MU,
    centre: float = 0.5,
) -> tuple[waves.StringEvolution, np.ndarray]:
    x = np.arange(STRING_CELLS + 1) * STRING_DX
    fastest = float(np.max(waves.wave_speed(STRING_TENSION, np.asarray(mu))))
    dt = courant * STRING_DX / fastest
    n_steps = int(round(transits / fastest / dt))
    pluck = 0.01 * np.exp(-(((x - centre) / 0.05) ** 2))
    run = waves.simulate_string(
        pluck, np.zeros_like(x), STRING_DX, dt, STRING_TENSION, mu, n_steps,
        boundary=boundary, save_every=max(1, n_steps // 4000),
    )
    return run, np.asarray(waves.total_energy(run.y, run.dydt, STRING_DX, STRING_TENSION, mu))


def test_the_string_energy_error_is_second_order_in_the_step_and_does_not_drift():
    """Ten transits between walls: the energy wobbles by (v dt)^2 and never walks.

    The solver is velocity Verlet on the chain the grid is, so it inherits that scheme's
    guarantee: the error in the energy oscillates with an amplitude set by the step and does
    not accumulate. Measured, the peak-to-peak wobble is 1.2e-3, 3.0e-4 and 7.5e-5 of the total
    at S = 0.8, 0.4 and 0.2 — fourfold for every halving of dt, exactly as second order
    requires — while the energy averaged over the first and last tenths of the run agrees to a
    few parts in 10^9.
    """
    spreads = []
    for courant in (0.8, 0.4, 0.2):
        _, energy = _string_energy(courant, 10.0)
        spreads.append(float(np.ptp(energy) / energy[0]))
        tenth = energy.size // 10
        assert abs(energy[-tenth:].mean() - energy[:tenth].mean()) / energy[0] < 1e-6

    ratios = np.array(spreads[:-1]) / np.array(spreads[1:])
    assert np.all(np.abs(ratios - 4.0) < 0.2), f"energy error ratios {ratios} are not fourfold"
    assert spreads[1] < 5e-4


def test_the_string_energy_error_is_bounded_rather_than_growing():
    """Four times the run, the same wobble to three figures — 4.68e-4 after 4 transits and 16.

    The check that licenses long experiments on the string, the same one module 07's chain
    passed: a slowly leaking scheme looks perfect for a few transits and only reveals itself
    when the run is extended.
    """
    bounds = [float(np.ptp(energy) / energy[0]) for _, energy in (
        _string_energy(0.5, transits) for transits in (4.0, 16.0)
    )]
    assert bounds[1] < 1.05 * bounds[0], f"energy error grows with run length: {bounds}"


def test_a_free_end_carries_half_a_cell_of_string():
    """With free ends the conserved energy weights the end points by half — and only then.

    A free end has zero slope, which the solver imposes with a mirror ghost point. That makes
    the end move as a mass of mu dx / 2 would, tied to its one neighbour, so the energy the
    scheme keeps is the trapezoid rule's, half weight at each end. Read that way, a pluck
    bouncing between two free ends holds its energy to 4.1e-4 over ten transits.

    Give the end points a whole cell of kinetic energy instead and the same run appears to lose
    and regain 1.7e-2 of it, forty times worse, in spikes at every reflection — the moment a
    free end moves fastest. That is a bookkeeping error, not physics, and the negative control
    is here so that nobody "simplifies" the weights.
    """
    run, energy = _string_energy(0.5, 10.0, boundary=("free", "free"), centre=0.3)
    assert np.ptp(energy) / energy[0] < 1e-3

    full_weights = np.full(STRING_CELLS + 1, STRING_DX)
    kinetic = 0.5 * STRING_MU * np.sum(full_weights * run.dydt**2, axis=1)
    potential = 0.5 * STRING_TENSION * np.sum(np.diff(run.y, axis=1) ** 2, axis=1) / STRING_DX
    miscounted = kinetic + potential
    assert np.ptp(miscounted) / miscounted[0] > 1e-2


def test_a_jump_in_density_leaves_the_total_energy_conserved():
    """A string four times heavier on its right half still keeps its energy to 4.1e-4.

    The pulse now partly reflects and partly crosses at the junction every time it arrives, so
    the energy is carried by several pulses of different sizes on two media at once. How it
    divides between them is module 10's question; that the total survives the division is the
    solver's promise, and it has to hold before the division can be measured at all.
    """
    x = np.arange(STRING_CELLS + 1) * STRING_DX
    density = np.where(x < 0.5, STRING_MU, 4.0 * STRING_MU)
    _, energy = _string_energy(0.5, 10.0, mu=density, centre=0.25)
    assert np.ptp(energy) / energy[0] < 1e-3
