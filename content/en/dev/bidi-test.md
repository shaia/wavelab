# Bidi rendering test page

This page exists to stress mixed-direction rendering. The English copy is the control; the
Hebrew copy is the test. Every construct below must render with correctly ordered math on
both site copies. Do not delete — it is the upgrade canary for theme/mystmd changes.

## Inline math in prose

The ideal gas law $PV = N\kB T$ sits inside a sentence. A ratio like $V_2/V_1 = 2$ and a
signed quantity $\Delta U = -3\,\mathrm{J}$ must keep their order. Mixed digits: at
$T = 300\,\mathrm{K}$ with $N = 10^{4}$ particles.

## Display math

$$
W = \int_{V_1}^{V_2} P\,dV = N\kB T \ln\frac{V_2}{V_1}
$$

$$
dU = \dbar Q + \dbar \Won
$$

## Lists with math

- First: $P = N\kB T/V$ at fixed $T$.
- Second: fluctuations scale as $N^{-1/2}$.
- Third: efficiency bound $\eta \le 1 - T_c/T_h$.

## Table with math

| Quantity | Symbol | Ideal-gas value |
|---|---|---|
| Pressure | $P$ | $N\kB T/V$ |
| Mean kinetic energy | $\langle E_k \rangle$ | $\tfrac{3}{2}\kB T$ |

## Code span and block

Inline code `thermolab.kinetics.simulate(n=100, rng=rng)` inside a sentence, then a block:

```python
import numpy as np
rng = np.random.default_rng(42)
```
