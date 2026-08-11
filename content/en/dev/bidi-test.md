# Bidi rendering test page

This page exists to stress mixed-direction rendering. The English copy is the control; the
Hebrew copy is the test. Every construct below must render with correctly ordered math on
both site copies. Do not delete — it is the upgrade canary for theme/mystmd changes.

## Inline math in prose

The plane wave $\psi(x,t) = \Real[A\,e^{\ii(kx - \omega t)}]$ sits inside a sentence. A ratio
like $\lambda_2/\lambda_1 = 2$ and a signed quantity $\Delta\varphi = -3\,\mathrm{rad}$ must
keep their order. Mixed digits: at $\lambda = 633\,\mathrm{nm}$ with $N = 10^{4}$ grating
lines.

## Display math

$$
\frac{\partial^{2}\psi}{\partial x^{2}} = \frac{1}{v^{2}}\frac{\partial^{2}\psi}{\partial t^{2}}
$$

$$
I(\theta) = I_0\left[\frac{\sin\beta}{\beta}\right]^{2}, \qquad \beta = \frac{\pi a \sin\theta}{\lambda}
$$

## Lists with math

- First: $k = 2\pi/\lambda$ at fixed $\lambda$.
- Second: $N$ random phasors sum to a resultant of length $\sim N^{1/2}$.
- Third: total internal reflection above $\theta_c = \arcsin(n_2/n_1)$.

## Table with math

| Quantity | Symbol | Plane-wave value |
|---|---|---|
| Wavenumber | $k$ | $2\pi/\lambda$ |
| Time-averaged intensity | $\langle I \rangle$ | $\tfrac{1}{2}c\epsilon_0 n E_0^2$ |

## Code span and block

Inline code `wavelab.phasors.random_phasor_sum(n=100, rng=rng)` inside a sentence, then a block:

```python
import numpy as np
rng = np.random.default_rng(42)
```
