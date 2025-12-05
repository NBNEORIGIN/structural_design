import math

h_d = 27/29
print(f'h/d = {h_d:.4f}')

# Correct formula from wind_calculator.py
cf = 0.935 + 0.1839 * math.log(h_d)
print(f'c_f = 0.935 + 0.1839 × ln({h_d:.4f}) = {cf:.4f}')
print(f'Expected: 0.92')
print(f'Match: {"✓" if abs(cf - 0.92) < 0.01 else "✗"}')
