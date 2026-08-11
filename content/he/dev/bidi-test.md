% en_source_hash: eb9a4a8696da88c4137409172adeeade528fc89b4e47409eb17753c602b79d66

# עמוד בדיקת רינדור דו-כיווני

העמוד הזה קיים כדי להעמיס על רינדור מעורב-כיוונים. העותק האנגלי הוא הביקורת; העותק העברי
הוא המבחן. כל מבנה למטה חייב להתרנדר עם מתמטיקה בסדר נכון בשני עותקי האתר. לא למחוק —
זהו גלאי הרגרסיות לשדרוגי ערכת העיצוב ו-mystmd.

## מתמטיקה בתוך שורה בפרוזה

הגל המישורי $\psi(x,t) = \Real[A\,e^{\ii(kx - \omega t)}]$ יושב בתוך משפט. יחס כמו
$\lambda_2/\lambda_1 = 2$ וגודל בעל סימן $\Delta\varphi = -3\,\mathrm{rad}$ חייבים לשמור על
סדרם. ספרות מעורבות: באורך גל $\lambda = 633\,\mathrm{nm}$ עם $N = 10^{4}$ קווי סריג.

## מתמטיקה בתצוגה

$$
\frac{\partial^{2}\psi}{\partial x^{2}} = \frac{1}{v^{2}}\frac{\partial^{2}\psi}{\partial t^{2}}
$$

$$
I(\theta) = I_0\left[\frac{\sin\beta}{\beta}\right]^{2}, \qquad \beta = \frac{\pi a \sin\theta}{\lambda}
$$

## רשימות עם מתמטיקה

- ראשון: $k = 2\pi/\lambda$ באורך גל $\lambda$ קבוע.
- שני: $N$ פאזורים אקראיים מסתכמים לשקול שאורכו $\sim N^{1/2}$.
- שלישי: החזרה פנימית מלאה מעל $\theta_c = \arcsin(n_2/n_1)$.

## טבלה עם מתמטיקה

| גודל | סמל | ערך עבור גל מישורי |
|---|---|---|
| מספר גל | $k$ | $2\pi/\lambda$ |
| עוצמה ממוצעת בזמן | $\langle I \rangle$ | $\tfrac{1}{2}c\epsilon_0 n E_0^2$ |

## מקטע קוד ובלוק קוד

קוד בתוך שורה `wavelab.phasors.random_phasor_sum(n=100, rng=rng)` בתוך משפט, ואז בלוק:

```python
import numpy as np
rng = np.random.default_rng(42)
```
