from projecting_sign_calculator import ProjectingSignCalculator

calc = ProjectingSignCalculator()
inputs = {
    'sign_width': 2.0,
    'sign_height': 1.5,
    'projection': 0.6,
    'mounting_height': 4.5,
    'terrain_category': 'III',
    'v_b_0': 22.5,
    'sign_weight': 0.15,
    'n_brackets': 2,
    'bracket_spacing': 1.2,
    'n_fixings_per_bracket': 4,
    'fixing_pitch_vertical': 0.15,
    'anchor_tension_capacity': 12.0,
    'anchor_shear_capacity': 8.0,
    'anchor_gamma_M': 1.5,
    'bracket_width': 80,
    'bracket_depth': 60,
    'bracket_thickness': 5,
    'bracket_steel_grade': 275
}

results = calc.calculate_wind_loading(inputs)
print(f"q_p = {results['q_p']} (should be ~422.8 Pa)")
print(f"F_w_k = {results['F_w_k']} kN (should be ~2.537 kN)")
