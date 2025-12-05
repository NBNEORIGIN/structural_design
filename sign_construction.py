"""
Sign Construction Module
Calculates panel deflection, stress, and required channel spacing
Based on BS 8442:2015 and EN 1999-1-1
"""

import numpy as np
from typing import Dict, Any, List


class SignConstructionCalculator:
    """
    Calculates structural adequacy of sign panel construction
    """
    
    # Material properties database
    MATERIALS = {
        'acm_3mm': {
            'name': '3mm Aluminium Composite (ACM/Dibond)',
            'thickness': 3.0,  # mm
            't_face': 0.3,  # mm (aluminium skin thickness)
            't_core': 2.4,  # mm (PE core)
            'E_face': 70000,  # MPa (aluminium)
            'E_core': 500,  # MPa (polyethylene - very low)
            'f_y_face': 100,  # MPa (1050 aluminium, annealed)
            'density': 5.0,  # kg/m²
            # Sandwich panel: I ≈ 2 × E_face × t_face × (d/2)² where d = total thickness
            # I = 2 × 70000 × 0.3 × (3/2)² = 94500 mm⁴ per 1000mm width = 94.5 mm⁴/mm
            'I_per_width': 94.5,  # mm⁴/mm (effective, per unit width)
            # W = I / (d/2) = 94.5 / 1.5 = 63 mm³/mm
            'W_per_width': 63.0,  # mm³/mm (section modulus per unit width)
        },
        'aluminium_3mm': {
            'name': '3mm Solid Aluminium 1050',
            'thickness': 3.0,  # mm
            'E': 70000,  # MPa
            'f_y': 100,  # MPa (1050-H14)
            'density': 8.1,  # kg/m²
            'I_per_width': 2.25,  # mm⁴/mm (t³/12 per unit width)
            'W_per_width': 1.5,  # mm³/mm (t²/6 per unit width)
        },
        'steel_composite_3mm': {
            'name': '3mm Steel Composite Panel',
            'thickness': 3.0,  # mm
            't_face': 0.5,  # mm (steel skin thickness - typically thicker than ACM)
            't_core': 2.0,  # mm (core material)
            'E_face': 210000,  # MPa (steel)
            'E_core': 500,  # MPa (polymer core)
            'f_y_face': 235,  # MPa (mild steel)
            'density': 12.0,  # kg/m² (heavier than aluminium)
            # Sandwich panel: I = 2 × E_face × t_face × (d/2)²
            # I = 2 × 210000 × 0.5 × (3/2)² = 472500 mm⁴ per 1000mm width = 472.5 mm⁴/mm
            'I_per_width': 472.5,  # mm⁴/mm (much stiffer than ACM due to steel)
            # W = I / (d/2) = 472.5 / 1.5 = 315 mm³/mm
            'W_per_width': 315.0,  # mm³/mm (section modulus per unit width)
        },
        'aluminium_4mm': {
            'name': '4mm Solid Aluminium 1050',
            'thickness': 4.0,  # mm
            'E': 70000,  # MPa
            'f_y': 100,  # MPa
            'density': 10.8,  # kg/m²
            'I_per_width': 5.33,  # mm⁴/mm
            'W_per_width': 2.67,  # mm³/mm
        },
    }
    
    def __init__(self):
        self.warnings = []
    
    def calculate_panel_adequacy(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate panel deflection and stress between sign channels
        
        Args:
            inputs: Dictionary containing:
                - panel_material: Material key from MATERIALS dict
                - channel_spacing: Spacing between horizontal channels (mm)
                - wind_pressure: Peak velocity pressure (Pa)
                - sign_height: Total sign height (m) - for calculating number of channels
                - sign_width: Total sign width (m) - for panel width
        
        Returns:
            Dictionary with panel check results and recommendations
        """
        self.warnings = []
        
        # Get material properties
        material_key = inputs.get('panel_material', 'acm_3mm')
        if material_key not in self.MATERIALS:
            raise ValueError(f"Unknown material: {material_key}")
        
        material = self.MATERIALS[material_key]
        
        # Extract inputs
        L = inputs['channel_spacing']  # mm
        q_p = inputs['wind_pressure']  # Pa
        sign_height = inputs.get('sign_height', 2.0) * 1000  # m to mm
        sign_width = inputs.get('sign_width', 3.0) * 1000  # m to mm
        
        # Panel properties
        if 'composite' in material_key or 'acm' in material_key:
            # Composite panel - use effective properties
            I_per_width = material['I_per_width']
            W_per_width = material['W_per_width']
            E = material['E_face']  # Use face material modulus
            f_y = material['f_y_face']
        else:
            # Solid panel
            I_per_width = material['I_per_width']
            W_per_width = material['W_per_width']
            E = material['E']
            f_y = material['f_y']
        
        # Calculate for 1m wide strip of panel
        strip_width = 1000  # mm
        I = I_per_width * strip_width  # mm⁴
        W = W_per_width * strip_width  # mm³
        
        # Distributed load on panel strip (N/mm)
        # q_p is in Pa = N/m²
        # For 1m wide strip: load = q_p N/m² × 1 m = q_p N/m
        # Convert to N/mm: q_p N/m ÷ 1000 mm/m = q_p/1000 N/mm
        w = q_p / 1000  # N/mm
        
        # Simply supported beam between channels
        # Maximum deflection (center of span)
        delta = (5 * w * L**4) / (384 * E * I)  # mm
        
        # Maximum bending moment
        M_max = (w * L**2) / 8  # Nmm
        
        # Maximum bending stress
        sigma = M_max / W if W > 0 else 999999  # MPa
        
        # Deflection limit (aesthetic)
        delta_limit = L / 200  # mm (BS 8442 recommendation)
        
        # Stress limit
        sigma_limit = f_y  # MPa
        
        # Check results
        deflection_ok = delta <= delta_limit
        stress_ok = sigma <= sigma_limit
        overall_ok = deflection_ok and stress_ok
        
        # Calculate recommended maximum spacing
        if not deflection_ok:
            # Work backwards from deflection limit
            L_max_deflection = ((384 * E * I * delta_limit) / (5 * w)) ** 0.25
        else:
            L_max_deflection = L
        
        if not stress_ok:
            # Work backwards from stress limit
            L_max_stress = ((8 * W * sigma_limit) / w) ** 0.5
        else:
            L_max_stress = L
        
        L_max_recommended = min(L_max_deflection, L_max_stress)
        
        # Calculate number of channels required
        num_channels_current = self._calculate_num_channels(sign_height, L)
        num_channels_recommended = self._calculate_num_channels(sign_height, L_max_recommended)
        
        # Generate warnings and recommendations
        recommendations = []
        if not deflection_ok:
            recommendations.append(
                f"Deflection exceeds limit. Reduce spacing to {L_max_deflection:.0f}mm or less."
            )
        if not stress_ok:
            recommendations.append(
                f"Stress exceeds yield. Reduce spacing to {L_max_stress:.0f}mm or less."
            )
        if not overall_ok:
            recommendations.append(
                f"Recommended: {num_channels_recommended} channels (spacing ~{L_max_recommended:.0f}mm)"
            )
            recommendations.append(
                "OR upgrade to thicker/stiffer panel material"
            )
        
        # Add construction quality note
        if L <= 300:
            quality_note = "Highway/Professional grade construction"
        elif L <= 450:
            quality_note = "Good quality construction"
        elif L <= 600:
            quality_note = "Budget construction - marginal for high wind areas"
        else:
            quality_note = "Amateur construction - not recommended"
        
        return {
            'material': material['name'],
            'channel_spacing': L,
            'wind_pressure': q_p,
            'deflection': {
                'calculated': delta,
                'limit': delta_limit,
                'status': 'PASS' if deflection_ok else 'FAIL',
                'utilization': delta / delta_limit if delta_limit > 0 else 999
            },
            'stress': {
                'calculated': sigma,
                'limit': sigma_limit,
                'status': 'PASS' if stress_ok else 'FAIL',
                'utilization': sigma / sigma_limit if sigma_limit > 0 else 999
            },
            'overall_status': 'ADEQUATE' if overall_ok else 'INADEQUATE',
            'num_channels_current': num_channels_current,
            'num_channels_recommended': num_channels_recommended,
            'max_spacing_recommended': L_max_recommended,
            'quality_note': quality_note,
            'recommendations': recommendations,
            'warnings': self.warnings
        }
    
    def _calculate_num_channels(self, sign_height: float, spacing: float) -> int:
        """
        Calculate number of horizontal channels required
        
        Args:
            sign_height: Total sign height (mm)
            spacing: Channel spacing (mm)
        
        Returns:
            Number of channels required
        """
        # Channels at top and bottom edges, plus intermediate channels
        # Number of spans = height / spacing
        # Number of channels = spans + 1
        
        num_spans = np.ceil(sign_height / spacing)
        num_channels = int(num_spans + 1)
        
        # Minimum 2 channels (top and bottom)
        return max(num_channels, 2)
    
    def recommend_channel_spacing(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend optimal channel spacing for given conditions
        
        Args:
            inputs: Dictionary containing:
                - panel_material: Material key
                - wind_pressure: Peak velocity pressure (Pa)
                - sign_height: Total sign height (m)
                - target_quality: 'highway', 'professional', 'budget' (optional)
        
        Returns:
            Dictionary with recommended spacing and number of channels
        """
        material_key = inputs.get('panel_material', 'acm_3mm')
        q_p = inputs['wind_pressure']
        sign_height = inputs.get('sign_height', 2.0)
        target_quality = inputs.get('target_quality', 'professional')
        
        # Quality-based spacing targets
        quality_targets = {
            'highway': 300,  # mm
            'professional': 400,  # mm
            'budget': 600,  # mm
        }
        
        target_spacing = quality_targets.get(target_quality, 400)
        
        # Check if target spacing is adequate
        check_inputs = {
            'panel_material': material_key,
            'channel_spacing': target_spacing,
            'wind_pressure': q_p,
            'sign_height': sign_height,
        }
        
        result = self.calculate_panel_adequacy(check_inputs)
        
        if result['overall_status'] == 'ADEQUATE':
            return {
                'recommended_spacing': target_spacing,
                'num_channels': result['num_channels_current'],
                'status': 'ADEQUATE',
                'quality': target_quality
            }
        else:
            # Use the calculated maximum spacing
            return {
                'recommended_spacing': result['max_spacing_recommended'],
                'num_channels': result['num_channels_recommended'],
                'status': 'REQUIRES_CLOSER_SPACING',
                'quality': 'custom',
                'note': f"Target {target_quality} spacing inadequate, using calculated maximum"
            }


if __name__ == '__main__':
    # Test the calculator
    calc = SignConstructionCalculator()
    
    print("="*70)
    print("SIGN CONSTRUCTION CALCULATOR - TEST")
    print("="*70)
    
    # Test case 1: 3mm ACM with 600mm spacing
    print("\nTest 1: 3mm ACM, 600mm spacing, 828 Pa")
    inputs1 = {
        'panel_material': 'acm_3mm',
        'channel_spacing': 600,
        'wind_pressure': 828,
        'sign_height': 2.0,
        'sign_width': 3.0
    }
    result1 = calc.calculate_panel_adequacy(inputs1)
    print(f"  Deflection: {result1['deflection']['calculated']:.2f}mm (limit: {result1['deflection']['limit']:.2f}mm) - {result1['deflection']['status']}")
    print(f"  Stress: {result1['stress']['calculated']:.1f} MPa (limit: {result1['stress']['limit']:.1f} MPa) - {result1['stress']['status']}")
    print(f"  Overall: {result1['overall_status']}")
    print(f"  Current: {result1['num_channels_current']} channels")
    print(f"  Recommended: {result1['num_channels_recommended']} channels @ {result1['max_spacing_recommended']:.0f}mm spacing")
    
    # Test case 2: 3mm Steel Composite with 400mm spacing
    print("\nTest 2: 3mm Steel Composite, 400mm spacing, 828 Pa")
    inputs2 = {
        'panel_material': 'steel_composite_3mm',
        'channel_spacing': 400,
        'wind_pressure': 828,
        'sign_height': 2.0,
        'sign_width': 3.0
    }
    result2 = calc.calculate_panel_adequacy(inputs2)
    print(f"  Deflection: {result2['deflection']['calculated']:.2f}mm (limit: {result2['deflection']['limit']:.2f}mm) - {result2['deflection']['status']}")
    print(f"  Stress: {result2['stress']['calculated']:.1f} MPa (limit: {result2['stress']['limit']:.1f} MPa) - {result2['stress']['status']}")
    print(f"  Overall: {result2['overall_status']}")
    print(f"  Quality: {result2['quality_note']}")
    
    # Test case 3: Recommendation engine
    print("\nTest 3: Recommend spacing for 3mm ACM, 828 Pa, highway quality")
    inputs3 = {
        'panel_material': 'acm_3mm',
        'wind_pressure': 828,
        'sign_height': 2.0,
        'target_quality': 'highway'
    }
    result3 = calc.recommend_channel_spacing(inputs3)
    print(f"  Recommended spacing: {result3['recommended_spacing']:.0f}mm")
    print(f"  Number of channels: {result3['num_channels']}")
    print(f"  Status: {result3['status']}")
