"""
Test script for new projecting and post-mounted sign calculators
Run this to verify calculations against hand calculations
"""

from projecting_sign_calculator import ProjectingSignCalculator
from post_mounted_calculator import PostMountedCalculator

def test_projecting_sign():
    """Test projecting sign calculator against worked example"""
    print("="*70)
    print("PROJECTING SIGN CALCULATOR TEST")
    print("="*70)
    
    calc = ProjectingSignCalculator()
    
    # Worked example from CALCULATION_METHODOLOGY.md
    inputs = {
        'sign_width': 2.0,  # m
        'sign_height': 1.5,  # m
        'projection': 0.6,  # m
        'mounting_height': 4.5,  # m
        'terrain_category': 'III',
        'v_b_0': 22.5,  # m/s (London)
        'sign_weight': 0.15,  # kN
        'n_brackets': 2,
        'bracket_spacing': 1.2,  # m
        'n_fixings_per_bracket': 4,
        'fixing_pitch_vertical': 0.15,  # m
        'anchor_tension_capacity': 12.0,  # kN
        'anchor_shear_capacity': 8.0,  # kN
        'anchor_gamma_M': 1.5,
        'bracket_width': 80,  # mm
        'bracket_depth': 60,  # mm
        'bracket_thickness': 5,  # mm
        'bracket_steel_grade': 275  # N/mm²
    }
    
    results = calc.calculate_wind_loading(inputs)
    
    # Expected values from hand calculations
    expected = {
        'q_p': 422.8,  # Pa
        'F_w_k': 2.537,  # kN
        'F_w_Ed': 3.806,  # kN
        'V_per_bracket': 1.903,  # kN
        'M_per_bracket': 1.142,  # kNm
        'eta_combined': 0.568,  # anchor utilization
    }
    
    print("\nWIND LOADING:")
    print(f"  Peak pressure:        {results['q_p']:.1f} Pa (expected: {expected['q_p']:.1f} Pa)")
    print(f"  Characteristic force: {results['F_w_k']:.3f} kN (expected: {expected['F_w_k']:.3f} kN)")
    print(f"  Design force:         {results['F_w_Ed']:.3f} kN (expected: {expected['F_w_Ed']:.3f} kN)")
    
    print("\nBRACKET FORCES:")
    print(f"  Shear per bracket:    {results['bracket_forces']['V_per_bracket']:.3f} kN (expected: {expected['V_per_bracket']:.3f} kN)")
    print(f"  Moment per bracket:   {results['bracket_forces']['M_per_bracket']:.3f} kNm (expected: {expected['M_per_bracket']:.3f} kNm)")
    
    print("\nANCHOR VERIFICATION:")
    print(f"  Tension Ed/Rd:        {results['anchor_check']['eta_tension']:.3f}")
    print(f"  Shear Ed/Rd:          {results['anchor_check']['eta_shear']:.3f}")
    print(f"  Combined:             {results['anchor_check']['eta_combined']:.3f} (expected: {expected['eta_combined']:.3f})")
    print(f"  Status:               {results['anchor_check']['combined_status']}")
    
    print("\nBRACKET MEMBER:")
    print(f"  Bending Ed/Rd:        {results['bracket_check']['eta_bending']:.3f}")
    print(f"  Shear Ed/Rd:          {results['bracket_check']['eta_shear']:.3f}")
    print(f"  Status:               {results['bracket_check']['bending_status']}")
    
    print("\nDEFLECTION:")
    print(f"  Deflection:           {results['deflection_check']['delta']:.2f} mm")
    print(f"  Limit:                {results['deflection_check']['delta_limit']:.2f} mm")
    print(f"  Utilization:          {results['deflection_check']['eta_deflection']:.3f}")
    print(f"  Status:               {results['deflection_check']['deflection_status']}")
    
    print(f"\nOVERALL STATUS: {results['overall_status']}")
    
    # Verify against expected values
    tolerance = 0.05  # 5% tolerance
    checks = []
    
    checks.append(('q_p', abs(results['q_p'] - expected['q_p']) / expected['q_p'] < tolerance))
    checks.append(('F_w_k', abs(results['F_w_k'] - expected['F_w_k']) / expected['F_w_k'] < tolerance))
    checks.append(('F_w_Ed', abs(results['F_w_Ed'] - expected['F_w_Ed']) / expected['F_w_Ed'] < tolerance))
    checks.append(('eta_combined', abs(results['anchor_check']['eta_combined'] - expected['eta_combined']) / expected['eta_combined'] < tolerance))
    
    print("\nVERIFICATION:")
    all_pass = True
    for name, passed in checks:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name}: {status}")
        all_pass = all_pass and passed
    
    if all_pass:
        print("\n✅ ALL CHECKS PASSED - Calculator verified!")
    else:
        print("\n⚠️ SOME CHECKS FAILED - Review required")
    
    return all_pass


def test_post_mounted():
    """Test post-mounted calculator"""
    print("\n" + "="*70)
    print("POST-MOUNTED SIGN CALCULATOR TEST")
    print("="*70)
    
    calc = PostMountedCalculator()
    
    inputs = {
        'sign_width': 3.0,  # m
        'sign_height': 2.0,  # m
        'sign_depth': 0.3,  # m
        'sign_base_height': 2.5,  # m
        'post_height': 4.5,  # m
        'site_altitude': 50,  # m
        'v_map': 22.5,  # m/s
        'distance_to_shore': 20,  # km
        'terrain_type': 'country',
        'post_diameter': 150,  # mm
        'post_thickness': 8,  # mm
        'post_steel_grade': 275,  # N/mm²
        'foundation_type': 'concrete',
        'embedment_depth': 1.5  # m
    }
    
    results = calc.calculate_wind_loading(inputs)
    
    # Expected values from hand calculations
    expected = {
        'q_p': 828,  # Pa (approximate)
        'F_w_sign': 5.46,  # kN
        'F_w_post': 0.39,  # kN
        'M_total': 20.0,  # kNm
        'eta_bending': 0.60,  # post utilization
    }
    
    print("\nWIND LOADING:")
    print(f"  Peak pressure:        {results['q_p']:.1f} Pa (expected: ~{expected['q_p']:.0f} Pa)")
    print(f"  Force on sign:        {results['F_w_sign']:.2f} kN (expected: {expected['F_w_sign']:.2f} kN)")
    print(f"  Force on post:        {results['F_w_post']:.2f} kN (expected: {expected['F_w_post']:.2f} kN)")
    print(f"  Total force:          {results['force_kN']:.2f} kN")
    
    print("\nMOMENTS:")
    print(f"  Sign moment:          {results['M_sign']:.2f} kNm")
    print(f"  Post moment:          {results['M_post']:.2f} kNm")
    print(f"  Total moment:         {results['M_total']:.2f} kNm (expected: ~{expected['M_total']:.1f} kNm)")
    
    if results['post_check']:
        print("\nPOST VERIFICATION:")
        print(f"  Bending Ed/Rd:        {results['post_check']['eta_bending']:.3f} (expected: {expected['eta_bending']:.2f})")
        print(f"  Shear Ed/Rd:          {results['post_check']['eta_shear']:.3f}")
        print(f"  Status:               {results['post_check']['bending_status']}")
    
    if results['foundation_check']:
        print("\nFOUNDATION:")
        print(f"  Embedment:            {results['foundation_check']['embedment']:.1f} m")
        print(f"  Status:               {results['foundation_check']['status']}")
        print(f"  Message:              {results['foundation_check']['message']}")
    
    print(f"\nOVERALL STATUS: {results['overall_status']}")
    
    # Verify against expected values
    tolerance = 0.10  # 10% tolerance (looser for post-mounted)
    checks = []
    
    checks.append(('F_w_sign', abs(results['F_w_sign'] - expected['F_w_sign']) / expected['F_w_sign'] < tolerance))
    checks.append(('M_total', abs(results['M_total'] - expected['M_total']) / expected['M_total'] < tolerance))
    if results['post_check']:
        checks.append(('eta_bending', abs(results['post_check']['eta_bending'] - expected['eta_bending']) / expected['eta_bending'] < tolerance))
    
    print("\nVERIFICATION:")
    all_pass = True
    for name, passed in checks:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name}: {status}")
        all_pass = all_pass and passed
    
    if all_pass:
        print("\n✅ ALL CHECKS PASSED - Calculator verified!")
    else:
        print("\n⚠️ SOME CHECKS FAILED - Review required")
    
    return all_pass


def test_edge_cases():
    """Test edge cases and warnings"""
    print("\n" + "="*70)
    print("EDGE CASE TESTS")
    print("="*70)
    
    # Test 1: Very small projecting sign
    print("\n1. Very small projecting sign (0.5m × 0.3m):")
    calc = ProjectingSignCalculator()
    inputs = {
        'sign_width': 0.5, 'sign_height': 0.3, 'projection': 0.3,
        'mounting_height': 3.0, 'terrain_category': 'III', 'v_b_0': 22.5,
        'sign_weight': 0.05, 'n_brackets': 1, 'bracket_spacing': 0,
        'n_fixings_per_bracket': 2, 'fixing_pitch_vertical': 0.1,
        'anchor_tension_capacity': 5.0, 'anchor_shear_capacity': 3.0,
        'anchor_gamma_M': 1.5, 'bracket_width': 50, 'bracket_depth': 40,
        'bracket_thickness': 3, 'bracket_steel_grade': 275
    }
    results = calc.calculate_wind_loading(inputs)
    print(f"   Wind force: {results['F_w_k']:.2f} kN")
    print(f"   Status: {results['overall_status']}")
    print(f"   Warnings: {len(results['warnings'])}")
    
    # Test 2: Tall post-mounted sign
    print("\n2. Tall post-mounted sign (8m high post):")
    calc = PostMountedCalculator()
    inputs = {
        'sign_width': 2.0, 'sign_height': 1.5, 'sign_depth': 0.2,
        'sign_base_height': 6.0, 'post_height': 8.0,
        'site_altitude': 100, 'v_map': 24.0, 'distance_to_shore': 50,
        'terrain_type': 'country', 'post_diameter': 200,
        'post_thickness': 10, 'post_steel_grade': 355,
        'foundation_type': 'concrete', 'embedment_depth': 2.0
    }
    results = calc.calculate_wind_loading(inputs)
    print(f"   Total force: {results['force_kN']:.2f} kN")
    print(f"   Moment: {results['M_total']:.2f} kNm")
    print(f"   Status: {results['overall_status']}")
    
    print("\n✅ Edge case tests completed")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("NEW SIGN CALCULATOR VALIDATION TESTS")
    print("="*70)
    print("\nThis script validates the new projecting and post-mounted")
    print("sign calculators against hand calculations.")
    print("\n" + "="*70)
    
    # Run tests
    projecting_pass = test_projecting_sign()
    post_pass = test_post_mounted()
    test_edge_cases()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Projecting Sign Calculator: {'✅ PASS' if projecting_pass else '⚠️ FAIL'}")
    print(f"Post-Mounted Calculator:    {'✅ PASS' if post_pass else '⚠️ FAIL'}")
    
    if projecting_pass and post_pass:
        print("\n✅ ALL CALCULATORS VERIFIED - Ready for deployment")
    else:
        print("\n⚠️ REVIEW REQUIRED - Check failed tests above")
    
    print("="*70)
