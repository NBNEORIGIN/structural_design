import math

# Sheffield Bioincubator values
h = 27  # height
d = 29  # depth
b = 20  # width

# Calculate h/d
h_d = h / d
print(f"h/d = {h}/{d} = {h_d:.4f}")

# Calculate c_f
c_f = 1.2 + 0.2 * math.log10(h_d)
print(f"c_f = 1.2 + 0.2 × log₁₀({h_d:.4f}) = {c_f:.4f}")
print(f"Expected: 0.92")
print(f"Match: {'✓' if abs(c_f - 0.92) < 0.01 else '✗'}")

# Calculate A_ref
A_ref = b * h
print(f"\nA_ref = {b} × {h} = {A_ref} m²")

# Calculate F_w (using values from your screenshot)
q_p = 1056.22  # Pa
c_s = 0.89
c_d = 1.07
c_f_calc = c_f
A_ref_calc = A_ref

F_w = q_p * c_s * c_d * c_f_calc * A_ref_calc / 1000
print(f"\nF_w = {q_p} × {c_s} × {c_d} × {c_f_calc:.4f} × {A_ref_calc} / 1000")
print(f"F_w = {F_w:.2f} kN")
print(f"Expected: 460 kN")
print(f"Difference: {abs(F_w - 460):.2f} kN ({abs(F_w - 460)/460*100:.1f}%)")
print(f"Status: {'PASS' if abs(F_w - 460)/460*100 < 10 else 'CHECK'}")
