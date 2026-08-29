"""The harmonic oscillator: free, damped, driven — closed forms and a numerical integrator.

MODEL SPECIFICATION
    System:        a point mass on a massless linear spring, moving in one dimension; the
                   observables are position, velocity, and the kinetic/potential energies
    Dynamics:      Newton's second law with force -k x - b v + F(t); closed-form solutions
                   where they exist, velocity-Verlet integration or convolution elsewhere
    Boundary:      none — the mass moves on an infinite line and nothing is exchanged
    Ensemble:      a single deterministic trajectory per choice of initial conditions; no
                   randomness anywhere in this module
    Ignored:       spring mass, nonlinearity at large extension, static friction, and every
                   microscopic mechanism behind the damping coefficient b
    Valid when:    displacements stay in the linear regime of the real spring and the time
                   step stays well below the oscillation period
    Failure modes: amplitudes that feel the spring's nonlinearity, time steps near the
                   stability limit, and any question about where the dissipated energy goes

Closed forms follow the project phase convention (constants.SIGN_CONVENTION): the driven
steady state is the complex amplitude X = (F0/m) / (omega0^2 - omega^2 - i gamma omega),
whose argument is the angle by which the displacement *lags* the drive.

The `q_from_*` functions are the other direction: they extract Q from *data* — a ringdown
record, a swept amplitude curve, a swept phase curve — the way a laboratory does. All three
estimate the same number by different routes, which is the point: agreement between them is
an experimental result, not an identity, once noise is in the record.

`impulse_response`, `step_response` and `convolution_response` view the same oscillator as a
linear time-invariant system — a map from force history to displacement history. The Green
function G(t) is the response to a unit kick, an arbitrary force is a train of kicks, and the
answer is their superposition. Its transform is the complex frequency response,
G-hat(omega) = (1/m) / (omega0^2 - omega^2 + i gamma omega), which is the conjugate of
`steady_state_response`: the sweep and the kick are one fact told in two domains.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import fourier


@dataclass(frozen=True)
class Trajectory:
    """A numerically integrated trajectory, initial state included.

    `times[0] == 0` with the given initial conditions; all three arrays share one length.
    """

    times: np.ndarray
    positions: np.ndarray
    velocities: np.ndarray


def natural_frequency(mass: float, stiffness: float) -> float:
    """The undamped angular frequency, omega0 = sqrt(k / m) [rad/s]."""
    _validate_oscillator(mass, stiffness)
    return float(np.sqrt(stiffness / mass))


def amplitude_phase(x0: float, v0: float, omega0: float) -> tuple[float, float]:
    """Amplitude and phase of the free oscillation with the given initial conditions.

    Returns `(A, phi)` such that `x(t) = A cos(omega0 t + phi)`. Starting at rest from x0
    gives phi = 0; starting at the origin moving in +x gives phi = -pi/2.
    """
    if omega0 <= 0:
        raise ValueError("omega0 must be positive")
    amplitude = float(np.hypot(x0, v0 / omega0))
    phase = float(np.arctan2(-v0 / omega0, x0))
    return amplitude, phase


def position(
    t: np.ndarray, mass: float, stiffness: float, x0: float, v0: float
) -> np.ndarray:
    """Closed-form position of the undamped oscillator, x(t) = A cos(omega0 t + phi)."""
    omega0 = natural_frequency(mass, stiffness)
    amplitude, phase = amplitude_phase(x0, v0, omega0)
    return amplitude * np.cos(omega0 * np.asarray(t) + phase)


def velocity(
    t: np.ndarray, mass: float, stiffness: float, x0: float, v0: float
) -> np.ndarray:
    """Closed-form velocity of the undamped oscillator, the time derivative of `position`."""
    omega0 = natural_frequency(mass, stiffness)
    amplitude, phase = amplitude_phase(x0, v0, omega0)
    return -amplitude * omega0 * np.sin(omega0 * np.asarray(t) + phase)


def energies(
    positions: np.ndarray, velocities: np.ndarray, mass: float, stiffness: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Kinetic, potential, and total energy along a trajectory, in that order [J]."""
    _validate_oscillator(mass, stiffness)
    kinetic = 0.5 * mass * np.asarray(velocities) ** 2
    potential = 0.5 * stiffness * np.asarray(positions) ** 2
    return kinetic, potential, kinetic + potential


def damping_rate(mass: float, damping: float) -> float:
    """The damping rate gamma = b / m [1/s]; amplitude decays as e^{-gamma t / 2}."""
    _validate_oscillator(mass, 1.0)
    if damping < 0:
        raise ValueError("damping must be non-negative")
    return damping / mass


def quality_factor(mass: float, stiffness: float, damping: float) -> float:
    """The quality factor Q = sqrt(m k) / b = omega0 / gamma, dimensionless."""
    _validate_oscillator(mass, stiffness)
    if damping <= 0:
        raise ValueError("damping must be positive — an undamped oscillator has no Q")
    return float(np.sqrt(mass * stiffness) / damping)


def damping_regime(mass: float, stiffness: float, damping: float) -> str:
    """Which of the three regimes: 'underdamped', 'critical', or 'overdamped'.

    The boundary is b = 2 sqrt(m k), i.e. gamma = 2 omega0. Floating point makes exact
    criticality a measure-zero event; this reports 'critical' only on exact equality and is
    meant for labelling, not for choosing numerical branches — `damped_position` handles the
    near-critical region continuously.
    """
    _validate_oscillator(mass, stiffness)
    if damping < 0:
        raise ValueError("damping must be non-negative")
    critical = 2.0 * np.sqrt(mass * stiffness)
    if damping < critical:
        return "underdamped"
    if damping > critical:
        return "overdamped"
    return "critical"


def damped_position(
    t: np.ndarray, mass: float, stiffness: float, damping: float, x0: float, v0: float
) -> np.ndarray:
    """Closed-form position of the damped free oscillator, in all three regimes.

    Underdamped: e^{-gamma t/2} (C cos omega_d t + D sin omega_d t) with
    omega_d = sqrt(omega0^2 - gamma^2/4); critical: (C + D t) e^{-omega0 t}; overdamped: the
    sum of two decaying exponentials. The three branches agree in the limit, and a test
    approaches the critical boundary from both sides to hold this function to that.
    """
    omega0 = natural_frequency(mass, stiffness)
    gamma = damping_rate(mass, damping)
    time = np.asarray(t, dtype=float)
    discriminant = omega0**2 - gamma**2 / 4.0

    if discriminant > 0:  # underdamped
        omega_d = np.sqrt(discriminant)
        c1 = x0
        c2 = (v0 + gamma * x0 / 2.0) / omega_d
        return np.exp(-gamma * time / 2.0) * (
            c1 * np.cos(omega_d * time) + c2 * np.sin(omega_d * time)
        )
    if discriminant == 0:  # critical
        return (x0 + (v0 + omega0 * x0) * time) * np.exp(-omega0 * time)
    # overdamped: real roots r = -gamma/2 +/- sqrt(gamma^2/4 - omega0^2)
    root = np.sqrt(-discriminant)
    r_plus = -gamma / 2.0 + root
    r_minus = -gamma / 2.0 - root
    c_plus = (v0 - r_minus * x0) / (r_plus - r_minus)
    c_minus = x0 - c_plus
    return c_plus * np.exp(r_plus * time) + c_minus * np.exp(r_minus * time)


def driven_amplitude(
    omega_drive: float,
    mass: float,
    stiffness: float,
    damping: float,
    force_amplitude: float,
) -> complex:
    """The steady-state complex amplitude of the driven, damped oscillator.

    With drive F0 cos(omega t) and the course's e^{-i omega t} time factor, the steady state
    is x(t) = Re[X e^{-i omega t}] with

        X = (F0 / m) / (omega0^2 - omega^2 - i gamma omega).

    |X| is the response amplitude and arg(X) the angle by which the displacement lags the
    drive: +pi/2 exactly at omega0, and the *amplitude* peak sits below omega0, at
    omega^2 = omega0^2 - gamma^2/2, whenever there is damping.

    The scalar face of `steady_state_response`; both share one closed form, so a change to
    the physics cannot reach one without the other.
    """
    return complex(
        steady_state_response(omega_drive, mass, stiffness, damping, force_amplitude)
    )


def steady_state_response(
    omega: np.ndarray,
    mass: float,
    stiffness: float,
    damping: float,
    force_amplitude: float = 1.0,
) -> np.ndarray:
    """The complex steady-state amplitude X(omega), vectorized over the drive frequency.

        X(omega) = (F0 / m) / (omega0^2 - omega^2 - i gamma omega)

    This is the whole resonance curve in one call: `abs(X)` is the amplitude response and
    `angle(X)` the phase lag, rising 0 -> pi/2 -> pi as the drive is swept through omega0.
    Module 03 uses it to weight each harmonic of a periodic drive, which is why it takes an
    array where `driven_amplitude` takes a number.
    """
    omega0 = natural_frequency(mass, stiffness)
    gamma = damping_rate(mass, damping)
    frequencies = np.asarray(omega, dtype=float)
    if np.any(frequencies < 0):
        raise ValueError("drive frequencies must be non-negative")
    denominator = omega0**2 - frequencies**2 - 1j * gamma * frequencies
    if np.any(denominator == 0):
        raise ValueError("undamped oscillator driven exactly at resonance has no steady state")
    return (force_amplitude / mass) / denominator


def resonance_peak_omega(mass: float, stiffness: float, damping: float) -> float:
    """Where |X(omega)| is largest: omega0 sqrt(1 - 1/(2 Q^2)), or 0.0 if there is no peak.

    Minimising the denominator's modulus gives omega_peak^2 = omega0^2 - gamma^2/2, which is
    *below* omega0 for any damping at all — the falsifier for the `resonance-peak-at-omega0`
    misconception. Below Q = 1/sqrt(2) the interior maximum does not exist: the response
    falls monotonically from its static value F0/k and the oscillator is a low-pass filter
    with no resonance. That case returns 0.0, the frequency at which the response really is
    largest, rather than raising — a sweep across the threshold is a plot, not an error.
    """
    omega0 = natural_frequency(mass, stiffness)
    gamma = damping_rate(mass, damping)
    discriminant = omega0**2 - gamma**2 / 2.0
    return float(np.sqrt(discriminant)) if discriminant > 0 else 0.0


def power_absorbed(
    omega: np.ndarray,
    mass: float,
    stiffness: float,
    damping: float,
    force_amplitude: float = 1.0,
) -> np.ndarray:
    """Cycle-averaged power the drive delivers in the steady state, (1/2) gamma m omega^2 |X|^2 [W].

    In the steady state every joule the drive supplies is dissipated, so this single
    expression is both <F v> and <b v^2>; the conservation tests check that identity against
    an integration rather than assuming it.

    Unlike the *amplitude*, this peaks at exactly omega0 whatever the damping — the
    denominator can be written ((omega0^2 - omega^2)/omega)^2 + gamma^2, which is minimal
    there. Displacement resonance and power resonance are different frequencies, and the
    difference is the whole content of the advanced section on module 02's page.
    """
    gamma = damping_rate(mass, damping)
    frequencies = np.asarray(omega, dtype=float)
    response = steady_state_response(frequencies, mass, stiffness, damping, force_amplitude)
    return 0.5 * gamma * mass * frequencies**2 * np.abs(response) ** 2


def impulse_response(
    t: np.ndarray, mass: float, stiffness: float, damping: float
) -> np.ndarray:
    """The Green function G(t): the motion after a unit impulse at t = 0 [m / (N s)].

    A spike of force changes the velocity and nothing else — the mass has no time to move
    while it acts — so a unit impulse leaves the oscillator at x = 0 with v = 1/m, and G is
    the free decay launched from there. Underdamped that reads
    e^{-gamma t/2} sin(omega_d t) / (m omega_d), but what is written below is
    `damped_position` itself, so the critical and overdamped regimes come out right with no
    second branch to keep in step. Hit anything and it rings at *its own* frequency: the kick
    sets the amplitude, never the pitch.

    Causality is imposed here rather than left to the caller. G = 0 for t < 0 because nothing
    moves before the kick, and the gate is load-bearing rather than decorative:
    `damped_position` solves the equation of motion on the whole line, and run backwards its
    underdamped branch *grows* as e^{+gamma|t|/2}. The negative half is clipped before the
    exponential is evaluated, so a record that starts well before the kick cannot overflow.
    """
    time = np.asarray(t, dtype=float)
    causal = np.clip(time, 0.0, None)
    launched = damped_position(causal, mass, stiffness, damping, 0.0, 1.0 / mass)
    return np.where(time >= 0.0, launched, 0.0)


def step_response(
    t: np.ndarray,
    mass: float,
    stiffness: float,
    damping: float,
    force_amplitude: float = 1.0,
) -> np.ndarray:
    """Motion after a constant force F0 is switched on at t = 0, from rest [m].

    The particular solution is the new equilibrium F0/k and the homogeneous part is whatever
    takes the mass there from the old one, so the whole answer is F0/k times a free decay
    started at unit displacement:

        x(t) = (F0/k) [1 - damped_position(t, x0 = 1, v0 = 0)].

    Written that way it needs no regime analysis of its own. Underdamped it is the familiar
    (F0/k)[1 - e^{-gamma t/2}(cos omega_d t + (gamma/2 omega_d) sin omega_d t)], and the
    agreement is exact rather than close, which a limits test pins.

    A featureless force produces overshoot and ringing: 92% above the final value at Q = 20,
    44% at Q = 2, and none at all at critical damping. That is the falsifier for the
    `response-follows-force-shape` misconception — the response does not copy the shape of
    what caused it.
    """
    time = np.asarray(t, dtype=float)
    causal = np.clip(time, 0.0, None)
    relaxation = damped_position(causal, mass, stiffness, damping, 1.0, 0.0)
    return np.where(time >= 0.0, (force_amplitude / stiffness) * (1.0 - relaxation), 0.0)


def convolution_response(
    force: np.ndarray, dt: float, mass: float, stiffness: float, damping: float
) -> np.ndarray:
    """Displacement under an arbitrary sampled force, as the causal convolution (G * F) [m].

    `force[i]` is F(i dt) [N] on the same grid `simulate_forced` uses, and the result has the
    same length, so the two can be compared sample for sample. Every force is a train of
    kicks and the oscillator answers each one identically, which is all linearity and time
    invariance amount to; this function is that sentence evaluated.

    Two details of the discrete version are not optional, and both are arithmetic rather than
    taste:

    `fourier.convolve` is circular on the DFT's periodic extension, so the record is padded
    to the next power of two at or above twice its length before transforming. Without the
    padding the tail of the response wraps around and reappears at t = 0, which reads as an
    oscillator that started moving before it was pushed.

    The force's first sample is given half weight. The FFT product is a rectangle-rule
    quadrature of the convolution integral, whose leading error is -(dt/2) G(t) F(0) — first
    order in dt, and visible: 4.4e-3 against the closed-form step response at dt = 0.02,
    falling only to 5.6e-4 as dt is quartered. The half weight is the trapezoidal rule's
    endpoint correction and restores second order (5.99e-5 to 9.37e-7 over the same
    refinement). The upper endpoint needs no such correction because G(0) = 0.
    """
    _validate_oscillator(mass, stiffness)
    if damping < 0:
        raise ValueError("damping must be non-negative")
    if dt <= 0:
        raise ValueError("dt must be positive")

    forces = np.asarray(force, dtype=float)
    if forces.ndim != 1:
        raise ValueError("force must be a one-dimensional record")
    if forces.size < 2:
        raise ValueError("force must hold at least two points — one interval needs both ends")

    n = forces.size
    padded_size = 1 << int(np.ceil(np.log2(2 * n)))
    origin = padded_size // 2

    # `convolve` and `spectrum` read their records on a grid centred on t = 0, while the
    # caller's force starts there; the offset is what translates between the two.
    centred_time = (np.arange(padded_size) - origin) * dt
    green = impulse_response(centred_time, mass, stiffness, damping)

    padded_force = np.zeros(padded_size)
    padded_force[origin : origin + n] = forces
    padded_force[origin] *= 0.5

    return fourier.convolve(green, padded_force, dt)[origin : origin + n]


def q_from_ringdown(
    times: np.ndarray, positions: np.ndarray, threshold: float = 0.1
) -> float:
    """Q measured from a free decay: the envelope gives gamma, the crossings give omega_d.

    Zero crossings are half periods, so omega_d = pi / (mean spacing), and the amplitude of
    each half cycle in between is a point on the decaying envelope, whose logarithm falls as
    -gamma t / 2. Q is then omega0 / gamma with omega0 recovered from
    omega0^2 = omega_d^2 + gamma^2/4. (The shorthand Q = omega_d/gamma is the high-Q limit
    of that and disagrees with `quality_factor` at the percent level around Q ~ 2, which is
    exactly the region module 02's regime sweep explores, so the exact form is used.)

    Two choices make this survive a noisy record, which is the only kind a laboratory has:

    `threshold` is a hysteresis, as a fraction of the largest excursion. A crossing is
    registered between two samples of *opposite* sign that both exceed it, so noise wobbling
    around zero cannot be counted as a dozen crossings — the failure that makes naive
    crossing counting useless. It also ends the analysis by itself: once the ringing has
    decayed below the threshold the record stops contributing, which is the same judgement
    an experimenter makes by eye about where a trace becomes noise.

    Each half cycle's amplitude is read as sqrt(2 <x^2>) over that window rather than as its
    largest sample. Both estimate the same thing on clean data; on noisy data the largest
    sample is biased upward by roughly the noise's extreme value, while the RMS is biased by
    sigma^2/A^2 — a hundred times smaller on the late, small cycles that set the fitted decay
    rate.

    The record must be a free decay about equilibrium: no drive, no offset.
    """
    t = np.asarray(times, dtype=float)
    x = np.asarray(positions, dtype=float)
    if t.shape != x.shape:
        raise ValueError("times and positions must have the same shape")
    if not 0.0 < threshold < 1.0:
        raise ValueError("threshold must be a fraction of the peak excursion, in (0, 1)")

    level = threshold * float(np.max(np.abs(x)))
    strong = np.nonzero(np.abs(x) > level)[0]
    if strong.size < 2:
        raise ValueError("record never rises above the hysteresis threshold")
    turns = np.nonzero(np.diff(np.sign(x[strong])))[0]
    if turns.size < 3:
        raise ValueError("need at least three zero crossings above the threshold")

    before, after = strong[turns], strong[turns + 1]
    fractions = x[before] / (x[before] - x[after])
    crossings = t[before] + fractions * (t[after] - t[before])
    omega_d = float(np.pi / np.mean(np.diff(crossings)))

    # Windows are bounded by the *interpolated crossing times*, not by the threshold-crossing
    # sample indices: as the ringing decays toward the threshold, the strong samples retreat
    # toward each peak, and windows cut at them would no longer be half cycles. That misalign-
    # ment biases the late amplitudes and, through them, the fitted decay rate.
    bounds = np.searchsorted(t, crossings)
    centres: list[float] = []
    amplitudes: list[float] = []
    for index, (start, stop) in enumerate(zip(bounds[:-1], bounds[1:], strict=True)):
        window = x[start:stop]
        if window.size < 2:
            continue
        centres.append(float(0.5 * (crossings[index] + crossings[index + 1])))
        amplitudes.append(float(np.sqrt(2.0 * np.mean(window**2))))

    envelope = np.asarray(amplitudes)
    if envelope.size < 3 or np.any(envelope <= 0.0):
        raise ValueError(
            "could not extract a usable decay envelope — a low-Q ringdown may need a "
            "smaller threshold, since it has few cycles above any given fraction of its peak"
        )
    slope = float(np.polyfit(np.asarray(centres), np.log(envelope), 1)[0])
    gamma = -2.0 * slope
    if gamma <= 0.0:
        raise ValueError("the envelope does not decay — is this a ringdown?")
    omega0 = float(np.sqrt(omega_d**2 + gamma**2 / 4.0))
    return omega0 / gamma


def q_from_bandwidth(omega: np.ndarray, amplitude: np.ndarray) -> float:
    """Q measured from a swept resonance curve: peak frequency over half-power width.

    The two frequencies where the amplitude has fallen to its maximum over sqrt(2) — half
    the power — are located by linear interpolation on the supplied grid, and
    Q = omega_peak / (omega_high - omega_low).

    Exact only in the high-Q limit, by two separate roads: the half-power width of |X|
    approaches gamma, and omega_peak approaches omega0. Both corrections are O(1/Q^2), so
    at Q = 20 this agrees with `quality_factor` to about a part in 10^3 and at Q = 2 it does
    not. The sweep must bracket both half-power points; a curve that never falls far enough
    on one side raises rather than quietly reporting the edge of the grid.
    """
    w = np.asarray(omega, dtype=float)
    a = np.asarray(amplitude, dtype=float)
    if w.shape != a.shape:
        raise ValueError("omega and amplitude must have the same shape")
    if w.size < 5:
        raise ValueError("need at least five sweep points to locate a half-power width")

    peak = int(np.argmax(a))
    half_power = a[peak] / np.sqrt(2.0)
    if a[0] > half_power or a[-1] > half_power:
        raise ValueError("sweep does not bracket both half-power points — widen the range")

    low = _crossing(w[: peak + 1], a[: peak + 1], half_power)
    high = _crossing(w[peak:][::-1], a[peak:][::-1], half_power)
    return float(w[peak] / (high - low))


def q_from_linewidth(omega: np.ndarray, amplitude: np.ndarray) -> float:
    """Q measured by *fitting* a Lorentzian line: Q = omega_c tau / 2 from A |L(omega - omega_c)|.

    Same inputs as `q_from_bandwidth` and the same number out, obtained by fitting the whole
    lineshape instead of interpolating two crossings on it. Use this one whenever the
    frequency grid is not the experimenter's to choose — above all on the spectrum of a
    ringdown, where `q_from_bandwidth` is a trap rather than a type error: it will accept FFT
    bins without complaint and return a plausible wrong number.

    The trap is arithmetic, not noise. A record holding n amplitude e-foldings has bin
    spacing 2 pi / T and a linewidth gamma, so it puts gamma T / 2 pi = n / pi bins across the
    full width *whatever Q is* — 1.6 bins at five e-foldings. Measured against a true Q = 10:
    at three e-foldings (1.9 bins across the width) `q_from_bandwidth` reads 8.10 while this
    reads 9.26; at five, 9.59 against 9.77. Recording for longer is not the escape it looks
    like — ten bins needs thirty-one e-foldings, where the signal is 1e-14 of where it
    started — and zero-padding only interpolates the lineshape, adding no information.

    Fitting works where crossings do not because every point constrains the same three
    numbers, so an under-resolved line is still a well-determined one. Note that
    `fourier.lorentzian_spectrum` is centred on zero — it is the transform of a decay, a
    low-pass curve, not a resonance — so the fitted model carries an explicit offset
    omega_c, and it is that offset, not the largest bin, which becomes the peak frequency.

    `amplitude` is |X| or |G-hat| on a band bracketing one resonance at positive frequency.
    The band is a real choice, because the true response is only asymptotically a Lorentzian:
    fitted over omega0 +/- 2 gamma this reads 0.26% low at Q = 20, over +/- 10 gamma 0.97%
    low. Wide bands buy points and pay for them in bias; a few linewidths either side is the
    sweet spot, and is what module 05's laboratory uses.
    """
    from scipy.optimize import curve_fit

    w = np.asarray(omega, dtype=float)
    a = np.asarray(amplitude, dtype=float)
    if w.shape != a.shape:
        raise ValueError("omega and amplitude must have the same shape")
    if w.size < 5:
        raise ValueError("need at least five points to fit a lineshape")
    if np.any(w < 0):
        raise ValueError("fit one resonance at positive frequency — pass the band, not both halves")

    peak = int(np.argmax(a))
    if peak == 0 or peak == a.size - 1:
        raise ValueError("the band does not contain the peak — centre it on the resonance")

    # A crude half-power width seeds tau; the fit is what actually determines it.
    guess_width = max(float(np.ptp(w)) / 10.0, float(w[1] - w[0]))
    guesses = (float(a[peak] * 2.0 / guess_width), float(w[peak]), float(2.0 / guess_width))

    def lineshape(x: np.ndarray, scale: float, centre: float, tau: float) -> np.ndarray:
        return scale * np.abs(fourier.lorentzian_spectrum(x - centre, tau))

    (_, centre, tau), _ = curve_fit(lineshape, w, a, p0=guesses, maxfev=10_000)
    if centre <= 0.0 or tau <= 0.0:
        raise ValueError("the fit did not converge on a resonance — check the band")
    return float(centre * tau / 2.0)


def q_from_phase_slope(omega: np.ndarray, phase_lag: np.ndarray) -> float:
    """Q measured from how fast the phase lag turns through pi/2: Q = (omega0/2) dphi/domega.

    Differentiating phi(omega) = atan2(gamma omega, omega0^2 - omega^2) at omega0 gives
    exactly 2/gamma, so half the resonant frequency times the slope is omega0/gamma — no
    high-Q approximation anywhere, which is what makes this the estimator that stays honest
    where the bandwidth route drifts.

    The slope is not taken by differencing the sweep. A numerical derivative of measured
    phases divides the noise by the grid spacing and multiplies it into the answer; on a
    realistically noisy sweep that alone put a 17% scatter on Q. Instead the phase relation
    is rearranged into the line it exactly is,

        omega * tan(phi - pi/2) = (1/gamma) omega^2 - omega0^2/gamma,

    and fitted over the half-power band pi/4 <= phi <= 3 pi/4, where the tangent is bounded
    by one and every point carries information about the same two numbers. The fit gives
    gamma = 1/slope and omega0^2 = -intercept/slope, hence Q = sqrt(-intercept * slope). On a
    noiseless sweep this returns (omega0/2) dphi/domega to the last digit; on a noisy one it
    averages instead of amplifying.

    `phase_lag` must be the *lag* in radians, rising through pi/2 — `np.angle` of
    `steady_state_response` under this project's phase convention.
    """
    w = np.asarray(omega, dtype=float)
    phi = np.asarray(phase_lag, dtype=float)
    if w.shape != phi.shape:
        raise ValueError("omega and phase_lag must have the same shape")
    if w.size < 5:
        raise ValueError("need at least five sweep points to measure a phase slope")

    band = (phi >= np.pi / 4.0) & (phi <= 3.0 * np.pi / 4.0)
    if int(np.count_nonzero(band)) < 5:
        raise ValueError(
            "fewer than five sweep points lie in the half-power phase band pi/4..3pi/4 — "
            "the sweep either misses resonance or is too coarse across it"
        )

    ordinate = w[band] * np.tan(phi[band] - np.pi / 2.0)
    slope, intercept = np.polyfit(w[band] ** 2, ordinate, 1)
    if slope <= 0.0 or intercept >= 0.0:
        raise ValueError("phase sweep does not have the shape of a resonance")
    return float(np.sqrt(-intercept * slope))


def _crossing(x: np.ndarray, y: np.ndarray, level: float) -> float:
    """The first x at which y crosses `level`, by linear interpolation between samples."""
    below = y < level
    index = np.nonzero(np.diff(below))[0]
    if index.size == 0:
        raise ValueError(f"no crossing of level {level}")
    i = int(index[0])
    span = y[i + 1] - y[i]
    fraction = 0.0 if span == 0 else (level - y[i]) / span
    return float(x[i] + fraction * (x[i + 1] - x[i]))


def max_stable_dt(mass: float, stiffness: float) -> float:
    """A time step comfortably inside the integrator's accurate regime: T0 / 100.

    Velocity Verlet only becomes unstable near dt = 2/omega0, but accuracy degrades long
    before that; one hundred steps per period keeps the phase error per period below a
    fraction of a percent. Mirrors the role of the same-named function in courses' other
    simulation modules.
    """
    omega0 = natural_frequency(mass, stiffness)
    return 2.0 * np.pi / omega0 / 100.0


def simulate(
    mass: float,
    stiffness: float,
    x0: float,
    v0: float,
    dt: float,
    n_steps: int,
    damping: float = 0.0,
    drive_amplitude: float = 0.0,
    drive_omega: float = 0.0,
) -> Trajectory:
    """Integrate m x'' = -k x - b x' + F0 cos(omega t) by velocity Verlet.

    Kick-drift-kick. The closing kick is implicit in the velocity — for a force linear in v
    that is one division, `(1 + gamma dt / 2)` — which keeps the scheme second order with
    damping and reduces *exactly* to standard velocity Verlet when b = 0, where it is
    symplectic: the energy error stays bounded over arbitrarily many periods instead of
    drifting. The conservation and convergence test categories pin both properties.
    """
    _validate_oscillator(mass, stiffness)
    if damping < 0:
        raise ValueError("damping must be non-negative")
    if dt <= 0:
        raise ValueError("dt must be positive")
    if n_steps < 1:
        raise ValueError("n_steps must be positive")

    gamma = damping_rate(mass, damping)
    omega0_sq = stiffness / mass
    force_per_mass = drive_amplitude / mass

    times = np.arange(n_steps + 1) * dt
    positions = np.empty(n_steps + 1)
    velocities = np.empty(n_steps + 1)
    positions[0] = x0
    velocities[0] = v0

    x = float(x0)
    v = float(v0)
    for step in range(n_steps):
        t_now = step * dt
        t_next = t_now + dt
        accel_now = -omega0_sq * x - gamma * v + force_per_mass * np.cos(drive_omega * t_now)
        v_half = v + 0.5 * dt * accel_now
        x = x + dt * v_half
        conservative_next = -omega0_sq * x + force_per_mass * np.cos(drive_omega * t_next)
        v = (v_half + 0.5 * dt * conservative_next) / (1.0 + 0.5 * dt * gamma)
        positions[step + 1] = x
        velocities[step + 1] = v

    return Trajectory(times=times, positions=positions, velocities=velocities)


def simulate_forced(
    mass: float,
    stiffness: float,
    x0: float,
    v0: float,
    dt: float,
    force_samples: np.ndarray,
    damping: float = 0.0,
) -> Trajectory:
    """Integrate m x'' = -k x - b x' + F(t) for a drive supplied as samples, by velocity Verlet.

    `simulate` drives with a single cosine, which is all modules 01 and 02 ask for. Module 03
    needs the other case — a periodic drive that is not a sinusoid — so that its harmonic-sum
    prediction can be tested against an integration that knows nothing about harmonics. Adding
    up separate `simulate` runs would assume exactly the superposition under test, so the force
    arrives here as a sampled record instead.

    `force_samples[i]` is F(i dt) [N], and the returned trajectory has the same length: an
    array of n + 1 samples integrates n steps. The scheme is the one `simulate` uses, closing
    kick and all, so it stays second order in the presence of damping.
    """
    _validate_oscillator(mass, stiffness)
    if damping < 0:
        raise ValueError("damping must be non-negative")
    if dt <= 0:
        raise ValueError("dt must be positive")

    forces = np.asarray(force_samples, dtype=float)
    if forces.ndim != 1:
        raise ValueError("force_samples must be a one-dimensional record")
    if forces.size < 2:
        raise ValueError("force_samples must hold at least two points — one step needs both ends")

    gamma = damping_rate(mass, damping)
    omega0_sq = stiffness / mass
    n_steps = forces.size - 1

    times = np.arange(forces.size) * dt
    positions = np.empty(forces.size)
    velocities = np.empty(forces.size)
    positions[0] = x0
    velocities[0] = v0

    x = float(x0)
    v = float(v0)
    for step in range(n_steps):
        accel_now = -omega0_sq * x - gamma * v + forces[step] / mass
        v_half = v + 0.5 * dt * accel_now
        x = x + dt * v_half
        conservative_next = -omega0_sq * x + forces[step + 1] / mass
        v = (v_half + 0.5 * dt * conservative_next) / (1.0 + 0.5 * dt * gamma)
        positions[step + 1] = x
        velocities[step + 1] = v

    return Trajectory(times=times, positions=positions, velocities=velocities)


def _validate_oscillator(mass: float, stiffness: float) -> None:
    if mass <= 0:
        raise ValueError("mass must be positive")
    if stiffness <= 0:
        raise ValueError("stiffness must be positive")
