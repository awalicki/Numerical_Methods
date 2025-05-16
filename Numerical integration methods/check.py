from sympy import symbols, integrate, Abs, sin
import math

x = symbols('x')
result = integrate(sin(x) + 0.5 *x, (x, -1, 3))

print(result)  # Wynik: 5

print(math.cos(1) - math.cos(3) + 2)

