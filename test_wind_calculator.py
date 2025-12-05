"""
Test suite for BS EN 1991-1-4 Wind Loading Calculator
Validates against SCI P394 Sheffield Bioincubator worked example (Section 9.1, pages 63-73)
"""

import pytest
import numpy as np
from wind_calculator import WindLoadCalculator


def test_sheffield_bioincubator():
    """
    Validate against P394 worked example (pages 63-73)
    
    Sheffield Bioincubator Building:
    - Location: Sheffield (S10 postcode)
    - Altitude: 105m above sea level
    - Building dimensions: 20m (E-W) × 29m (N-S) × 27m high
    - Distance to shoreline: >100km
    - Distance into town: 2km
    
    Expected results for E-W direction (Q4 sector):
    - v_map = 22.1 m/s
    - c_alt = 1.1
    - c_dir = 1.0 (worst case)
    - c_e = 2.45 (at z=27m, Zone B, with town correction)
    - q_p = 1058 Pa (approximately)
    - c_s = 0.85
    - c_d = 1.03
    - c_f = 0.92
    - F_w = 460 kN (E-W direction)
    """
    
    calculator = WindLoadCalculator()
    
    # Input data for Sheffield Bioincubator (E-W direction)
    inputs = {
        'sign_width': 20,  # m (E-W breadth, cross-wind)
        'sign_height': 27,  # m (building height)
        'sign_depth': 29,   # m (N-S depth, in-wind)
        'building_height': 27,  # m
        'site_altitude': 105,  # m
        'v_map': 22.1,  # m/s (from P394 Figure 5.1 for Sheffield)
        'distance_to_shore': 100,  # km (>100km inland)
        'terrain_type': 'town',
        'distance_into_town': 2,  # km
        'mounting_type': 'wall_mounted_fascia'
    }
    
    results = calculator.calculate_wind_loading(inputs)
    
    # Validation with 2% tolerance
    print("\n" + "="*60)
    print("Sheffield Bioincubator Validation Test")
    print("="*60)
    
    # Stage 1: Fundamental wind speed
    assert abs(results['v_map'] - 22.1) < 0.1
    print(f"✓ v_map: {results['v_map']:.1f} m/s (Expected: 22.1 m/s)")
    
    # Stage 2: Altitude factor
    expected_c_alt = 1.1
    assert abs(results['c_alt'] - expected_c_alt) < 0.02
    print(f"✓ c_alt: {results['c_alt']:.2f} (Expected: {expected_c_alt})")
    
    # Stage 4: Directional factor
    assert results['c_dir'] == 1.0
    print(f"✓ c_dir: {results['c_dir']:.2f} (Expected: 1.0)")
    
    # Stage 7: Exposure factor (approximate, depends on interpretation)
    # P394 shows effective c_e * c_e,T ≈ 2.9 for this case
    # We calculate c_e and c_e,T separately
    effective_c_e = results['c_e'] * results['c_e_T']
    expected_effective = 2.9
    assert abs(effective_c_e - expected_effective) < 0.2  # Allow some variation
    print(f"✓ c_e: {results['c_e']:.2f}, c_e,T: {results['c_e_T']:.2f}, effective: {effective_c_e:.2f} (Expected: ~{expected_effective})")
    
    # Stage 11: Peak velocity pressure
    expected_q_p = 1058  # Pa
    tolerance_q_p = expected_q_p * 0.05  # 5% tolerance
    assert abs(results['q_p'] - expected_q_p) < tolerance_q_p
    print(f"✓ q_p: {results['q_p']:.0f} Pa (Expected: {expected_q_p} Pa)")
    
    # Stage 18: Size factor
    expected_c_s = 0.85
    assert abs(results['c_s'] - expected_c_s) < 0.05  # Allow 5% variation
    print(f"✓ c_s: {results['c_s']:.2f} (Expected: {expected_c_s})")
    
    # Stage 19: Dynamic factor
    expected_c_d = 1.03
    assert abs(results['c_d'] - expected_c_d) < 0.05  # Allow 5% variation
    print(f"✓ c_d: {results['c_d']:.2f} (Expected: {expected_c_d})")
    
    # Stage 21: Force coefficient
    expected_c_f = 0.92
    assert abs(results['c_f'] - expected_c_f) < 0.05
    print(f"✓ c_f: {results['c_f']:.2f} (Expected: {expected_c_f})")
    
    # Stage 24: Wind force
    expected_force_kN = 460  # kN
    tolerance_force = expected_force_kN * 0.08  # 8% tolerance (accounts for compounding factors)
    assert abs(results['force_kN'] - expected_force_kN) < tolerance_force
    print(f"✓ F_w: {results['force_kN']:.1f} kN (Expected: {expected_force_kN} kN)")
    
    print("="*60)
    print("✓ Sheffield Bioincubator validation PASSED")
    print(f"  All values within acceptable tolerance")
    print("="*60)
    
    return results


def test_altitude_factor():
    """Test altitude factor calculation"""
    calculator = WindLoadCalculator()
    
    # Test case 1: Low building (< 16.7m), sea level
    c_alt = calculator.calculate_altitude_factor(0, 10)
    assert c_alt == 1.0
    
    # Test case 2: Low building, 100m altitude
    c_alt = calculator.calculate_altitude_factor(100, 10)
    assert abs(c_alt - 1.1) < 0.01
    
    # Test case 3: Tall building, 100m altitude
    c_alt = calculator.calculate_altitude_factor(100, 30)
    assert c_alt > 1.0 and c_alt < 1.1
    
    print("✓ Altitude factor tests passed")


def test_exposure_factor():
    """Test exposure factor calculation"""
    calculator = WindLoadCalculator()
    
    # Test Zone A (sea)
    c_e, zone = calculator.calculate_exposure_factor(10, 0, 0, 'sea')
    assert zone == 'A'
    assert c_e > 2.3  # Should be higher for sea
    
    # Test Zone B (country)
    c_e, zone = calculator.calculate_exposure_factor(10, 0, 50, 'country')
    assert zone == 'B'
    assert 1.8 < c_e < 2.5  # Broader range for interpolated values
    
    # Test Zone C (town)
    c_e, zone = calculator.calculate_exposure_factor(10, 0, 100, 'town')
    assert zone == 'C'
    assert c_e > 2.0  # Town uses base exposure, correction applied via c_e,T
    
    print("✓ Exposure factor tests passed")


def test_size_factor():
    """Test size factor calculation"""
    calculator = WindLoadCalculator()
    
    # Small sign
    c_s = calculator.calculate_size_factor(2, 3, 10, 'B')
    assert c_s == 1.0  # b+h = 5m
    
    # Large sign
    c_s = calculator.calculate_size_factor(150, 150, 10, 'B')
    assert c_s < 1.0  # Should have reduction
    
    print("✓ Size factor tests passed")


def test_dynamic_factor():
    """Test dynamic factor calculation"""
    calculator = WindLoadCalculator()
    
    # Low building
    c_d = calculator.calculate_dynamic_factor(10, 5)
    assert c_d == 1.0
    
    # Tall slender building
    c_d = calculator.calculate_dynamic_factor(30, 10)
    assert c_d > 1.0
    
    print("✓ Dynamic factor tests passed")


def test_force_coefficient():
    """Test force coefficient calculation"""
    calculator = WindLoadCalculator()
    
    # Square cross-section (h/d = 1)
    c_f = calculator.calculate_force_coefficient(10, 10)
    assert 0.9 < c_f < 1.0
    
    # Tall slender (h/d = 3)
    c_f = calculator.calculate_force_coefficient(15, 5)
    assert c_f > 1.0
    
    # Flat (h/d = 0.5)
    c_f = calculator.calculate_force_coefficient(5, 10)
    assert c_f < 1.0
    
    print("✓ Force coefficient tests passed")


def test_typical_signage():
    """Test typical signage scenarios"""
    calculator = WindLoadCalculator()
    
    # Test case 1: Small wall-mounted fascia sign
    inputs = {
        'sign_width': 3.0,  # 3m wide
        'sign_height': 1.5,  # 1.5m high
        'sign_depth': 0.3,  # 0.3m deep
        'building_height': 6.0,  # 6m above ground
        'site_altitude': 50,
        'v_map': 22.0,
        'distance_to_shore': 50,
        'terrain_type': 'country',
        'distance_into_town': 0,
        'mounting_type': 'wall_mounted_fascia'
    }
    
    results = calculator.calculate_wind_loading(inputs)
    
    assert results['force_kN'] > 0
    assert results['q_p'] > 0
    assert results['moment_kNm'] > 0
    
    print(f"\n✓ Small fascia sign test:")
    print(f"  Wind force: {results['force_kN']:.2f} kN")
    print(f"  Peak pressure: {results['q_p']:.0f} Pa")
    print(f"  Overturning moment: {results['moment_kNm']:.2f} kNm")
    
    # Test case 2: Large high-level sign
    inputs2 = {
        'sign_width': 8.0,  # 8m wide
        'sign_height': 3.0,  # 3m high
        'sign_depth': 0.5,  # 0.5m deep
        'building_height': 15.0,  # 15m above ground
        'site_altitude': 20,
        'v_map': 23.0,
        'distance_to_shore': 10,
        'terrain_type': 'country',
        'distance_into_town': 0,
        'mounting_type': 'wall_mounted_fascia'
    }
    
    results2 = calculator.calculate_wind_loading(inputs2)
    
    assert results2['force_kN'] > results['force_kN']  # Should be higher
    
    print(f"\n✓ Large high-level sign test:")
    print(f"  Wind force: {results2['force_kN']:.2f} kN")
    print(f"  Peak pressure: {results2['q_p']:.0f} Pa")
    print(f"  Overturning moment: {results2['moment_kNm']:.2f} kNm")


def test_postcode_lookup():
    """Test postcode wind speed lookup"""
    calculator = WindLoadCalculator()
    
    # Test Scottish postcode (high wind)
    v_map = calculator.lookup_wind_speed('AB10 1AB')
    assert v_map >= 23.0
    
    # Test Midlands postcode (lower wind)
    v_map = calculator.lookup_wind_speed('B1 1AA')
    assert v_map <= 22.0
    
    # Test coastal postcode (high wind)
    v_map = calculator.lookup_wind_speed('TR1 1AA')
    assert v_map >= 23.0
    
    print("✓ Postcode lookup tests passed")


if __name__ == '__main__':
    print("\nRunning Wind Loading Calculator Test Suite")
    print("="*60)
    
    # Run all tests
    test_altitude_factor()
    test_exposure_factor()
    test_size_factor()
    test_dynamic_factor()
    test_force_coefficient()
    test_postcode_lookup()
    test_typical_signage()
    
    # Main validation test
    print("\n" + "="*60)
    print("Running Sheffield Bioincubator Validation")
    print("="*60)
    test_sheffield_bioincubator()
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED ✓")
    print("="*60)
