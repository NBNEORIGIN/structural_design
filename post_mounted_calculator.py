"""
BS EN 1991-1-4 Post-Mounted Sign Wind Loading Calculator

This module implements wind loading calculations for post-mounted signs
according to BS EN 1991-1-4 + UK National Annex + SCI P394 methodology.

Author: Toby Fletcher, CEng MIMechE
Company: North By North East Print & Sign Ltd
Standard: BS EN 1991-1-4:2005+A1:2010 + SCI P394
Version: 1.0.0
"""

import numpy as np
from typing import Dict, List, Tuple, Any
from wind_calculator import WindLoadCalculator


class PostMountedCalculator(WindLoadCalculator):
    """
    Calculate wind loading for post-mounted (free-standing) signs
    
    Inherits from WindLoadCalculator and extends for post-mounted configuration:
    - Similar wind pressure methodology to wall-mounted
    - Different force coefficients (free-standing vs wall-mounted)
    - Post/foundation design checks
    - Overturning moment analysis
    """
    
    def __init__(self):
        """Initialize post-mounted calculator"""
        super().__init__()
        self.sign_type = "post_mounted"
    
    def calculate_wind_loading(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main calculation method for post-mounted sign wind loading
        
        Args:
            inputs: Dictionary containing:
                - sign_width (b): Width (m)
                - sign_height (h): Height (m)
                - sign_depth (d): Depth/thickness (m)
                - sign_base_height: Height from ground to sign bottom (m)
                - post_height: Total post height above ground (m)
                - site_altitude: Altitude above sea level (m)
                - v_map: Fundamental wind speed (m/s)
                - distance_to_shore: Distance to coast (km)
                - terrain_type: 'sea', 'country', 'town'
                - distance_into_town: Distance into town (km) if terrain='town'
                - post_diameter: Post outer diameter (mm) for circular, or width for square
                - post_thickness: Post wall thickness (mm)
                - post_section_type: 'circular' or 'square' (default: 'circular')
                - post_material: 'steel', 'aluminium', or 'timber' (default: 'steel')
                - post_steel_grade: Material strength (N/mm²) - yield for steel/alu, bending for timber
                - foundation_type: 'concrete', 'steel_base'
                - embedment_depth: Foundation depth (m)
        
        Returns:
            Dictionary with all calculation results
        """
        self.warnings = []
        
        # Extract inputs
        b = inputs['sign_width']
        h = inputs['sign_height']
        d = inputs['sign_depth']
        z_base = inputs['sign_base_height']
        z_top = z_base + h
        z_centroid = z_base + h / 2
        
        # Calculate wind loading using parent class methodology
        # Use centroid height for wind pressure
        wind_inputs = {
            'sign_width': b,
            'sign_height': h,
            'sign_depth': d,
            'building_height': z_centroid,  # Use centroid for pressure
            'site_altitude': inputs['site_altitude'],
            'v_map': inputs['v_map'],
            'distance_to_shore': inputs['distance_to_shore'],
            'terrain_type': inputs['terrain_type'],
            'distance_into_town': inputs.get('distance_into_town', 0),
            'mounting_type': 'post_mounted'
        }
        
        # Get base wind loading calculation
        base_results = super().calculate_wind_loading(wind_inputs)
        
        # Extract key values (q_p is in Pa from parent class)
        q_p = base_results['q_p']  # Pa
        c_s = base_results['c_s']
        c_d = base_results['c_d']
        
        # Force coefficient for free-standing sign
        # P394 Table 5.3 - similar to wall-mounted but may need adjustment
        h_over_d = h / d if d > 0 else 999
        c_f = self.calculate_force_coefficient_freestanding(h, d, b)
        
        # Reference area
        A_ref = b * h
        
        # Wind force on sign (N, then convert to kN)
        F_w_sign = q_p * c_s * c_d * c_f * A_ref / 1000  # Pa * m² = N, /1000 = kN
        
        # Wind force on post (if significant)
        post_size = inputs.get('post_diameter', 0) / 1000  # mm to m (diameter or width)
        post_height = inputs.get('post_height', z_top)
        post_section_type = inputs.get('post_section_type', 'circular')
        
        if post_size > 0:
            # Force coefficient depends on section type
            if post_section_type == 'square':
                c_f_post = 2.0  # Sharp-edged square section (conservative)
            else:  # circular
                c_f_post = 0.7  # Circular cylinder (P394 Table 5.4)
            
            A_post = post_size * post_height
            
            # Use average wind pressure over post height
            z_post_avg = post_height / 2
            wind_inputs_post = wind_inputs.copy()
            wind_inputs_post['building_height'] = z_post_avg
            post_results = super().calculate_wind_loading(wind_inputs_post)
            q_p_post = post_results['q_p']  # Pa
            
            F_w_post = q_p_post * c_f_post * A_post / 1000  # Pa * m² = N, /1000 = kN
        else:
            F_w_post = 0
            self.warnings.append("Post diameter not specified - post wind force neglected")
        
        # Total wind force
        F_w_total = F_w_sign + F_w_post
        
        # Overturning moment at ground level
        M_sign = F_w_sign * z_centroid
        M_post = F_w_post * (post_height / 2) if F_w_post > 0 else 0
        M_total = M_sign + M_post
        
        # Post stress check (if details provided)
        post_check = None
        if 'post_diameter' in inputs and 'post_thickness' in inputs:
            post_check = self.calculate_post_stresses(
                M_total,
                F_w_total,
                inputs['post_diameter'],
                inputs['post_thickness'],
                inputs.get('post_steel_grade', 275),
                inputs.get('post_section_type', 'circular'),
                inputs.get('post_material', 'steel')
            )
        
        # Foundation check (simplified)
        foundation_check = None
        if 'embedment_depth' in inputs:
            foundation_check = self.calculate_foundation_requirements(
                M_total,
                F_w_total,
                inputs['embedment_depth'],
                inputs.get('foundation_type', 'concrete')
            )
        
        # Overall assessment
        checks_pass = True
        if post_check:
            checks_pass = checks_pass and post_check['bending_status'] == 'PASS'
        if foundation_check:
            checks_pass = checks_pass and foundation_check['status'] == 'ADEQUATE'
        
        # Compile results
        results = {
            # Sign type
            'sign_type': 'post_mounted',
            'mounting_type': 'post_mounted',
            
            # Inherit base results
            **base_results,
            
            # Override/add specific values
            'q_p': q_p,  # Keep in Pa for consistency
            'c_f': c_f,
            'c_f_ref': 'P394 Table 5.3 (free-standing)',
            'A_ref': A_ref,
            'z_centroid': z_centroid,
            
            # Forces
            'F_w_sign': F_w_sign,
            'F_w_post': F_w_post,
            'force_N': F_w_total * 1000,
            'force_kN': F_w_total,
            
            # Moments
            'M_sign': M_sign,
            'M_post': M_post,
            'M_total': M_total,
            'moment_kNm': M_total,
            
            # Checks
            'post_check': post_check,
            'foundation_check': foundation_check,
            
            # Assessment
            'overall_pass': checks_pass,
            'overall_status': 'ADEQUATE' if checks_pass else 'REQUIRES REVIEW',
            
            # Warnings
            'warnings': self.warnings
        }
        
        return results
    
    def calculate_force_coefficient_freestanding(self, height: float, 
                                                 depth: float, width: float) -> float:
        """
        Calculate force coefficient for free-standing sign
        P394 Table 5.3 with adjustments for free-standing
        
        Args:
            height: Sign height (m)
            depth: Sign depth (m)
            width: Sign width (m)
        
        Returns:
            Force coefficient c_f
        """
        h_over_d = height / depth if depth > 0 else 999
        
        # Use similar formula to wall-mounted but slightly higher
        # Free-standing signs experience slightly higher forces
        if 0.25 <= h_over_d <= 1:
            c_f = 0.935 + 0.1839 * np.log(h_over_d)
            c_f *= 1.1  # 10% increase for free-standing
        elif 1 < h_over_d <= 5:
            c_f = (0.8125 + 0.0375 * h_over_d) * (1.1 + 0.1243 * np.log(h_over_d))
            c_f *= 1.1  # 10% increase for free-standing
        elif h_over_d < 0.25:
            c_f = 0.68 * 1.1
        else:
            c_f = 1.0 * 1.1
            self.warnings.append(f"h/d = {h_over_d:.2f} > 5. Using conservative c_f.")
        
        return c_f
    
    def calculate_post_stresses(self, M: float, F: float, size_out: float, 
                               t: float, f_y: float, section_type: str = 'circular',
                               material: str = 'steel') -> Dict[str, Any]:
        """
        Calculate stresses in hollow section post (circular or square)
        EN 1993-1-1 (steel/aluminium), EN 1995-1-1 (timber)
        
        Args:
            M: Bending moment at base (kNm)
            F: Shear force (kN)
            size_out: Outer diameter (circular) or width (square) (mm)
            t: Wall thickness (mm)
            f_y: Material strength (N/mm²) - yield for steel/alu, bending for timber
            section_type: 'circular' or 'square'
            material: 'steel', 'aluminium', or 'timber'
        
        Returns:
            Dictionary with stress checks
        """
        # Check if solid section (timber) or hollow (steel/aluminium)
        is_solid = (material == 'timber')
        
        if section_type == 'square':
            b_out = size_out
            
            if is_solid:
                # Solid square section
                I = b_out**4 / 12
                W_el = b_out**3 / 6
                A = b_out**2
            else:
                # Square hollow section (SHS)
                b_in = b_out - 2 * t
                I = (b_out**4 - b_in**4) / 12
                W_el = I / (b_out / 2)
                A = b_out**2 - b_in**2
            
        else:  # circular
            D_out = size_out
            
            if is_solid:
                # Solid circular section
                I = np.pi * D_out**4 / 64
                W_el = np.pi * D_out**3 / 32
                A = np.pi * D_out**2 / 4
            else:
                # Circular hollow section (CHS)
                D_in = D_out - 2 * t
                I = np.pi * (D_out**4 - D_in**4) / 64
                W_el = I / (D_out / 2)
                A = np.pi * (D_out**2 - D_in**2) / 4
        
        # Bending stress (N/mm²)
        M_Nmm = M * 1e6  # kNm to Nmm
        sigma_Ed = M_Nmm / W_el if W_el > 0 else 999999
        
        # Design resistance depends on material
        if material == 'steel':
            gamma_M0 = 1.0
            sigma_Rd = f_y / gamma_M0
            tau_Rd = (f_y / np.sqrt(3)) / gamma_M0
        elif material == 'aluminium':
            gamma_M1 = 1.1  # EN 1999-1-1
            sigma_Rd = f_y / gamma_M1
            tau_Rd = (f_y / np.sqrt(3)) / gamma_M1
        else:  # timber
            gamma_M = 1.3  # EN 1995-1-1
            k_mod = 0.9  # Medium-term loading (wind)
            sigma_Rd = (f_y * k_mod) / gamma_M
            # For timber, shear strength is different (typically ~3-4 N/mm² for softwood)
            f_v_k = 4.0  # Conservative for C24
            tau_Rd = (f_v_k * k_mod) / gamma_M
        
        # Utilization
        eta_bending = sigma_Ed / sigma_Rd if sigma_Rd > 0 else 999
        
        # Shear stress (simplified)
        tau_Ed = (F * 1000) / A if A > 0 else 999999
        eta_shear = tau_Ed / tau_Rd if tau_Rd > 0 else 999
        
        return {
            'I': I,
            'W_el': W_el,
            'sigma_Ed': sigma_Ed,
            'sigma_Rd': sigma_Rd,
            'eta_bending': eta_bending,
            'tau_Ed': tau_Ed,
            'tau_Rd': tau_Rd,
            'eta_shear': eta_shear,
            'bending_status': 'PASS' if eta_bending <= 1.0 else 'FAIL',
            'shear_status': 'PASS' if eta_shear <= 1.0 else 'FAIL'
        }
    
    def calculate_foundation_requirements(self, M: float, F: float, 
                                         embedment: float, 
                                         foundation_type: str) -> Dict[str, Any]:
        """
        Simplified foundation adequacy check
        
        Args:
            M: Overturning moment (kNm)
            F: Horizontal force (kN)
            embedment: Embedment depth (m)
            foundation_type: 'concrete' or 'steel_base'
        
        Returns:
            Dictionary with foundation check
        """
        # Very simplified check - proper foundation design needed
        # This is indicative only
        
        if foundation_type == 'concrete':
            # Rule of thumb: embedment should be at least 1/10 of post height
            # and provide adequate moment resistance
            
            # Assume soil bearing capacity ~100 kN/m² (conservative)
            # Required foundation width to resist overturning
            required_width = np.sqrt(M / 50)  # Very simplified
            
            # Check embedment provides adequate fixity
            # Typically need embedment > 1.5m for significant posts
            if embedment < 1.0:
                status = 'INADEQUATE'
                message = 'Embedment depth too shallow - minimum 1.0m recommended'
            elif embedment < 1.5:
                status = 'MARGINAL'
                message = 'Embedment adequate but consider deeper foundation'
            else:
                status = 'ADEQUATE'
                message = 'Embedment depth appears adequate'
        
        else:  # steel_base
            # Bolted base plate - requires detailed design
            status = 'REQUIRES DESIGN'
            message = 'Base plate and anchor bolt design required'
            required_width = 0
        
        return {
            'embedment': embedment,
            'required_width': required_width,
            'status': status,
            'message': message,
            'warning': 'Foundation design is simplified - detailed design by structural engineer required'
        }


if __name__ == "__main__":
    # Example calculation
    calc = PostMountedCalculator()
    
    # Example inputs
    inputs = {
        'sign_width': 3.0,  # m
        'sign_height': 2.0,  # m
        'sign_depth': 0.3,  # m
        'sign_base_height': 2.5,  # m (bottom of sign above ground)
        'post_height': 4.5,  # m (total post height)
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
    
    print("="*60)
    print("POST-MOUNTED SIGN CALCULATION EXAMPLE")
    print("="*60)
    print(f"\nWind Pressure: {results['q_p']:.1f} Pa ({results['q_p']/1000:.3f} kN/m²)")
    print(f"Force on Sign: {results['F_w_sign']:.2f} kN")
    print(f"Force on Post: {results['F_w_post']:.2f} kN")
    print(f"Total Force: {results['force_kN']:.2f} kN")
    print(f"\nOverturning Moment: {results['M_total']:.2f} kNm")
    
    if results['post_check']:
        print(f"\nPost Bending Utilization: {results['post_check']['eta_bending']:.2f}")
        print(f"Post Status: {results['post_check']['bending_status']}")
    
    if results['foundation_check']:
        print(f"\nFoundation Status: {results['foundation_check']['status']}")
        print(f"Message: {results['foundation_check']['message']}")
    
    print(f"\nOverall Status: {results['overall_status']}")
