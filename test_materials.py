"""Test different post materials: Steel, Aluminium, Timber"""

from post_mounted_calculator import PostMountedCalculator

calc = PostMountedCalculator()

# Base inputs
base_inputs = {
    'sign_width': 3.0,
    'sign_height': 2.0,
    'sign_depth': 0.3,
    'sign_base_height': 2.5,
    'post_height': 4.5,
    'site_altitude': 50,
    'v_map': 22.5,
    'distance_to_shore': 20,
    'terrain_type': 'country',
    'post_thickness': 8,
    'foundation_type': 'concrete',
    'embedment_depth': 1.5
}

print("="*70)
print("POST MATERIAL COMPARISON")
print("="*70)

# Test 1: Steel CHS 150×8, S275
print("\n1. STEEL - CHS 150×8, S275")
inputs_steel = base_inputs.copy()
inputs_steel.update({
    'post_diameter': 150,
    'post_section_type': 'circular',
    'post_material': 'steel',
    'post_steel_grade': 275
})
results_steel = calc.calculate_wind_loading(inputs_steel)
print(f"   Design resistance:   {results_steel['post_check']['sigma_Rd']:.1f} N/mm²")
print(f"   Bending stress:      {results_steel['post_check']['sigma_Ed']:.1f} N/mm²")
print(f"   Utilization:         {results_steel['post_check']['eta_bending']:.3f}")
print(f"   Status:              {results_steel['post_check']['bending_status']}")

# Test 2: Aluminium CHS 150×8, 6061-T6
print("\n2. ALUMINIUM - CHS 150×8, 6061-T6")
inputs_alu = base_inputs.copy()
inputs_alu.update({
    'post_diameter': 150,
    'post_section_type': 'circular',
    'post_material': 'aluminium',
    'post_steel_grade': 240  # 6061-T6 yield strength
})
results_alu = calc.calculate_wind_loading(inputs_alu)
print(f"   Design resistance:   {results_alu['post_check']['sigma_Rd']:.1f} N/mm² (γ_M1 = 1.1)")
print(f"   Bending stress:      {results_alu['post_check']['sigma_Ed']:.1f} N/mm²")
print(f"   Utilization:         {results_alu['post_check']['eta_bending']:.3f}")
print(f"   Status:              {results_alu['post_check']['bending_status']}")

# Test 3: Timber SHS 150×150, C24
print("\n3. TIMBER - Square 150×150, C24")
inputs_timber = base_inputs.copy()
inputs_timber.update({
    'post_diameter': 150,
    'post_section_type': 'square',
    'post_material': 'timber',
    'post_steel_grade': 24  # C24 bending strength
})
results_timber = calc.calculate_wind_loading(inputs_timber)
print(f"   Design resistance:   {results_timber['post_check']['sigma_Rd']:.1f} N/mm² (k_mod=0.9, γ_M=1.3)")
print(f"   Bending stress:      {results_timber['post_check']['sigma_Ed']:.1f} N/mm²")
print(f"   Utilization:         {results_timber['post_check']['eta_bending']:.3f}")
print(f"   Status:              {results_timber['post_check']['bending_status']}")

# Comparison
print("\n" + "="*70)
print("COMPARISON")
print("="*70)
print(f"Steel utilization:     {results_steel['post_check']['eta_bending']:.3f}")
print(f"Aluminium utilization: {results_alu['post_check']['eta_bending']:.3f} ({results_alu['post_check']['eta_bending']/results_steel['post_check']['eta_bending']:.2f}x)")
print(f"Timber utilization:    {results_timber['post_check']['eta_bending']:.3f} ({results_timber['post_check']['eta_bending']/results_steel['post_check']['eta_bending']:.2f}x)")

print("\nKEY INSIGHTS:")
print("- Steel: Highest strength, lowest partial factor (γ_M0 = 1.0)")
print("- Aluminium: Lower strength, higher partial factor (γ_M1 = 1.1)")
print("- Timber: Lowest strength, highest partial factor (γ_M = 1.3), but k_mod helps")
print("- Square timber section has better geometry than circular steel/alu")
print("\n✓ All three materials now supported!")
