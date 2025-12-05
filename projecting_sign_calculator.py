"""
EN 1991-1-4 Projecting Sign Wind Loading Calculator

This module implements wind loading calculations for projecting signs
according to EN 1991-1-4 (Eurocode) methodology.

Author: Toby Fletcher, CEng MIMechE
Company: North By North East Print & Sign Ltd
Standard: EN 1991-1-4:2005 + UK National Annex
Version: 1.0.0
"""

import numpy as np
from typing import Dict, List, Tuple, Any


class ProjectingSignCalculator:
    """
    Calculate wind loading and structural verification for projecting signs
    
    Based on EN 1991-1-4 Eurocode methodology with:
    - Wind pressure calculations (§4.3, §4.5)
    - Force coefficients for flat plates (Table 7.13)
    - Bracket force analysis
    - Anchor/fixing design verification
    - Bracket member stress checks
    - Serviceability deflection limits
    """
    
    # Constants
    AIR_DENSITY = 1.25  # kg/m³ (EN 1991-1-4 recommended)
    GRAVITY = 9.81  # m/s²
    STEEL_E_MODULUS = 210000  # N/mm² (EN 1993-1-1)
    
    # Terrain parameters (EN 1991-1-4 Table 4.1)
    TERRAIN_PARAMS = {
        '0': {'z_0': 0.003, 'z_min': 1, 'k_r': 0.17, 'description': 'Sea or coastal area'},
        'II': {'z_0': 0.05, 'z_min': 2, 'k_r': 0.19, 'description': 'Low vegetation, isolated obstacles'},
        'III': {'z_0': 0.3, 'z_min': 5, 'k_r': 0.22, 'description': 'Suburban/industrial'},
        'IV': {'z_0': 1.0, 'z_min': 10, 'k_r': 0.24, 'description': 'Urban centres'}
    }
    
    # Partial factors (EN 1990)
    GAMMA_G_UNFAV = 1.35  # Permanent actions (unfavorable)
    GAMMA_G_FAV = 1.0     # Permanent actions (favorable)
    GAMMA_Q = 1.5         # Variable actions (wind)
    
    def __init__(self):
        """Initialize calculator with empty warnings list"""
        self.warnings = []
        self.methodology = "EN 1991-1-4:2005"
        self.version = "1.0.0"
    
    def calculate_wind_loading(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main calculation method for projecting sign wind loading
        
        Args:
            inputs: Dictionary containing:
                - sign_width (b): Width parallel to wall (m)
                - sign_height (h): Height (m)
                - projection (e): Distance from wall to sign centroid (m)
                - mounting_height (z): Height to sign centroid (m)
                - terrain_category: '0', 'II', 'III', or 'IV'
                - v_b_0: Fundamental basic wind velocity (m/s)
                - c_dir: Directional factor (default 1.0)
                - c_season: Seasonal factor (default 1.0)
                - sign_weight: Self-weight of sign (kN)
                - n_brackets: Number of brackets
                - bracket_spacing: Vertical spacing between brackets (m)
                - n_fixings_per_bracket: Number of fixings per bracket
                - fixing_pitch_vertical: Vertical pitch between fixing rows (m)
                - anchor_tension_capacity: N_Rk (kN)
                - anchor_shear_capacity: V_Rk (kN)
                - anchor_gamma_M: Partial factor for anchors
                - bracket_width: b_out (mm)
                - bracket_depth: h_out (mm)
                - bracket_thickness: t (mm)
                - bracket_steel_grade: f_y (N/mm²)
        
        Returns:
            Dictionary with all calculation results and verification checks
        """
        self.warnings = []
        
        # Extract inputs
        b = inputs['sign_width']
        h = inputs['sign_height']
        e = inputs['projection']
        z = inputs['mounting_height']
        terrain = inputs['terrain_category']
        v_b_0 = inputs['v_b_0']
        c_dir = inputs.get('c_dir', 1.0)
        c_season = inputs.get('c_season', 1.0)
        
        # Stage 1: Basic wind velocity
        v_b = self.calculate_basic_wind_velocity(v_b_0, c_dir, c_season)
        
        # Stage 2: Peak velocity pressure at sign height
        terrain_params = self.TERRAIN_PARAMS[terrain]
        z_0 = terrain_params['z_0']
        z_min = terrain_params['z_min']
        k_r = terrain_params['k_r']
        
        z_eff = max(z, z_min)
        c_r = self.calculate_roughness_factor(z_eff, z_0, k_r)
        I_v = self.calculate_turbulence_intensity(z_eff, z_0)
        v_m = c_r * v_b  # c_0 = 1.0 (flat terrain)
        q_p = self.calculate_peak_pressure(v_m, I_v)
        
        # Stage 3: Wind force on sign
        A = b * h
        c_f = 2.0  # Force coefficient for flat plate perpendicular to wind
        F_w_k = c_f * q_p * A  # Characteristic wind force (kN)
        
        # Stage 4: ULS design actions
        G_k = inputs['sign_weight']
        G_Ed = self.GAMMA_G_UNFAV * G_k
        F_w_Ed = self.GAMMA_Q * F_w_k
        
        # Stage 5: Bracket forces
        n_brackets = inputs['n_brackets']
        s = inputs['bracket_spacing']
        
        bracket_forces = self.calculate_bracket_forces(
            F_w_Ed, e, n_brackets, s, G_Ed
        )
        
        # Stage 6: Anchor verification
        n_fix = inputs['n_fixings_per_bracket']
        p_v = inputs['fixing_pitch_vertical']
        N_Rk = inputs['anchor_tension_capacity']
        V_Rk = inputs['anchor_shear_capacity']
        gamma_M = inputs['anchor_gamma_M']
        
        anchor_check = self.calculate_anchor_utilization(
            bracket_forces['V_per_bracket'],
            bracket_forces['M_per_bracket'],
            bracket_forces['N_vertical'],
            n_fix, p_v, N_Rk, V_Rk, gamma_M
        )
        
        # Stage 7: Bracket member verification
        b_out = inputs['bracket_width']
        h_out = inputs['bracket_depth']
        t = inputs['bracket_thickness']
        f_y = inputs['bracket_steel_grade']
        
        section = {'b_out': b_out, 'h_out': h_out, 't': t}
        bracket_check = self.calculate_bracket_stresses(
            bracket_forces['V_per_bracket'], e, section, f_y
        )
        
        # Stage 8: Deflection check (SLS)
        I = bracket_check['I']
        deflection_check = self.calculate_deflection(
            F_w_k, n_brackets, e, self.STEEL_E_MODULUS, I
        )
        
        # Overall assessment
        overall_pass = (
            anchor_check['eta_combined'] <= 1.0 and
            bracket_check['eta_bending'] <= 1.0 and
            bracket_check['eta_shear'] <= 1.0 and
            deflection_check['eta_deflection'] <= 1.0
        )
        
        # Compile results
        results = {
            # Input summary
            'sign_type': 'projecting',
            'sign_area': A,
            'projection': e,
            'mounting_height': z,
            'terrain': terrain,
            'terrain_description': terrain_params['description'],
            
            # Wind calculations
            'v_b': v_b,
            'v_b_ref': 'EN 1991-1-4 §4.2',
            'z_eff': z_eff,
            'c_r': c_r,
            'c_r_ref': 'EN 1991-1-4 Eq 4.4',
            'I_v': I_v,
            'I_v_ref': 'EN 1991-1-4 Eq 4.7',
            'v_m': v_m,
            'v_m_ref': 'EN 1991-1-4 Eq 4.3',
            'q_p': q_p,
            'q_p_ref': 'EN 1991-1-4 Eq 4.8',
            
            # Force calculations
            'c_f': c_f,
            'c_f_ref': 'EN 1991-1-4 Table 7.13',
            'F_w_k': F_w_k,
            'F_w_k_ref': 'EN 1991-1-4 Eq 5.3',
            'F_w_Ed': F_w_Ed,
            'F_w_Ed_ref': 'EN 1990 §6.4.3',
            'G_Ed': G_Ed,
            
            # Bracket forces
            'bracket_forces': bracket_forces,
            
            # Verification checks
            'anchor_check': anchor_check,
            'bracket_check': bracket_check,
            'deflection_check': deflection_check,
            
            # Overall result
            'overall_pass': overall_pass,
            'overall_status': 'ADEQUATE' if overall_pass else 'INADEQUATE',
            
            # Metadata
            'warnings': self.warnings,
            'methodology': self.methodology,
            'version': self.version
        }
        
        return results
    
    def calculate_basic_wind_velocity(self, v_b_0: float, c_dir: float, c_season: float) -> float:
        """
        Calculate basic wind velocity
        EN 1991-1-4 §4.2, Equation 4.1
        
        Args:
            v_b_0: Fundamental basic wind velocity (m/s)
            c_dir: Directional factor (-)
            c_season: Seasonal factor (-)
        
        Returns:
            Basic wind velocity v_b (m/s)
        """
        return v_b_0 * c_dir * c_season
    
    def calculate_roughness_factor(self, z: float, z_0: float, k_r: float) -> float:
        """
        Calculate roughness factor
        EN 1991-1-4 Equation 4.4
        
        Args:
            z: Height above ground (m)
            z_0: Roughness length (m)
            k_r: Terrain factor (-)
        
        Returns:
            Roughness factor c_r(z)
        """
        return k_r * np.log(z / z_0)
    
    def calculate_turbulence_intensity(self, z: float, z_0: float, 
                                      k_I: float = 1.0, c_0: float = 1.0) -> float:
        """
        Calculate turbulence intensity
        EN 1991-1-4 Equation 4.7
        
        Args:
            z: Height above ground (m)
            z_0: Roughness length (m)
            k_I: Turbulence factor (default 1.0 for UK)
            c_0: Orography factor (default 1.0 for flat terrain)
        
        Returns:
            Turbulence intensity I_v(z)
        """
        return k_I / (c_0 * np.log(z / z_0))
    
    def calculate_peak_pressure(self, v_m: float, I_v: float) -> float:
        """
        Calculate peak velocity pressure
        EN 1991-1-4 Equation 4.8
        
        Args:
            v_m: Mean wind velocity (m/s)
            I_v: Turbulence intensity (-)
        
        Returns:
            Peak velocity pressure q_p (kN/m²)
        """
        q_p_Pa = 0.5 * self.AIR_DENSITY * v_m**2 * (1 + 7 * I_v)
        return q_p_Pa / 1000  # Convert Pa to kN/m²
    
    def calculate_bracket_forces(self, F_w_Ed: float, e: float, 
                                n_brackets: int, s: float, G_Ed: float) -> Dict[str, float]:
        """
        Calculate forces in brackets
        
        Args:
            F_w_Ed: Design wind force (kN)
            e: Projection distance (m)
            n_brackets: Number of brackets
            s: Vertical spacing between brackets (m)
            G_Ed: Design self-weight (kN)
        
        Returns:
            Dictionary with bracket forces
        """
        # Shear force per bracket (equal distribution)
        V_per_bracket = F_w_Ed / n_brackets
        
        # Moment at wall
        M_wall = F_w_Ed * e
        
        # Moment per bracket
        M_per_bracket = V_per_bracket * e
        
        # Vertical load per bracket
        N_vertical = G_Ed / n_brackets
        
        # Tension/compression from moment couple
        if n_brackets >= 2:
            N_moment = M_wall / s
        else:
            N_moment = 0
            self.warnings.append("Single bracket: no moment couple resistance")
        
        # Maximum tension in top bracket
        N_tension_max = N_moment + N_vertical
        
        return {
            'V_per_bracket': V_per_bracket,
            'M_wall': M_wall,
            'M_per_bracket': M_per_bracket,
            'N_vertical': N_vertical,
            'N_moment': N_moment,
            'N_tension_max': N_tension_max
        }
    
    def calculate_anchor_utilization(self, V_per_bracket: float, M_per_bracket: float,
                                    N_vertical: float, n_fix: int, p_v: float,
                                    N_Rk: float, V_Rk: float, gamma_M: float) -> Dict[str, float]:
        """
        Calculate anchor utilization
        
        Args:
            V_per_bracket: Shear force per bracket (kN)
            M_per_bracket: Moment per bracket (kNm)
            N_vertical: Vertical load per bracket (kN)
            n_fix: Number of fixings per bracket
            p_v: Vertical pitch between fixing rows (m)
            N_Rk: Characteristic tension resistance (kN)
            V_Rk: Characteristic shear resistance (kN)
            gamma_M: Partial factor for anchors
        
        Returns:
            Dictionary with anchor checks
        """
        # Shear force per fixing
        V_Ed = V_per_bracket / n_fix
        
        # Tension force per fixing (conservative approach)
        # Moment creates tension in half the fixings
        N_Ed = M_per_bracket / (p_v * (n_fix / 2)) + N_vertical / n_fix
        
        # Design resistances
        N_Rd = N_Rk / gamma_M
        V_Rd = V_Rk / gamma_M
        
        # Utilization ratios
        eta_tension = N_Ed / N_Rd if N_Rd > 0 else 999
        eta_shear = V_Ed / V_Rd if V_Rd > 0 else 999
        eta_combined = eta_tension + eta_shear  # Linear interaction (conservative)
        
        return {
            'N_Ed': N_Ed,
            'V_Ed': V_Ed,
            'N_Rd': N_Rd,
            'V_Rd': V_Rd,
            'eta_tension': eta_tension,
            'eta_shear': eta_shear,
            'eta_combined': eta_combined,
            'tension_status': 'PASS' if eta_tension <= 1.0 else 'FAIL',
            'shear_status': 'PASS' if eta_shear <= 1.0 else 'FAIL',
            'combined_status': 'PASS' if eta_combined <= 1.0 else 'FAIL'
        }
    
    def calculate_bracket_stresses(self, V_per_bracket: float, L: float,
                                   section: Dict[str, float], f_y: float) -> Dict[str, float]:
        """
        Calculate bracket member stresses
        EN 1993-1-1
        
        Args:
            V_per_bracket: Shear force (kN)
            L: Projection length (m)
            section: {'b_out', 'h_out', 't'} in mm
            f_y: Yield strength (N/mm²)
        
        Returns:
            Dictionary with stress checks
        """
        b_out = section['b_out']
        h_out = section['h_out']
        t = section['t']
        
        # Inner dimensions
        b_in = b_out - 2 * t
        h_in = h_out - 2 * t
        
        # Second moment of area (mm⁴)
        I = (b_out * h_out**3 - b_in * h_in**3) / 12
        
        # Elastic section modulus (mm³)
        W_el = 2 * I / h_out
        
        # Bending moment (Nmm)
        M_Ed = V_per_bracket * L * 1e6  # kN·m to N·mm
        
        # Bending stress (N/mm²)
        sigma_Ed = M_Ed / W_el if W_el > 0 else 999999
        
        # Design resistance (N/mm²)
        gamma_M0 = 1.0
        sigma_Rd = f_y / gamma_M0
        
        # Bending utilization
        eta_bending = sigma_Ed / sigma_Rd if sigma_Rd > 0 else 999
        
        # Shear area (mm²)
        A_v = 2 * h_out * t
        
        # Shear stress (N/mm²)
        V_Ed_N = V_per_bracket * 1000  # kN to N
        tau_Ed = V_Ed_N / A_v if A_v > 0 else 999999
        
        # Shear resistance (N/mm²)
        tau_Rd = (f_y / np.sqrt(3)) / gamma_M0
        
        # Shear utilization
        eta_shear = tau_Ed / tau_Rd if tau_Rd > 0 else 999
        
        return {
            'I': I,
            'W_el': W_el,
            'M_Ed': M_Ed / 1e6,  # Back to kNm for display
            'sigma_Ed': sigma_Ed,
            'sigma_Rd': sigma_Rd,
            'eta_bending': eta_bending,
            'tau_Ed': tau_Ed,
            'tau_Rd': tau_Rd,
            'eta_shear': eta_shear,
            'bending_status': 'PASS' if eta_bending <= 1.0 else 'FAIL',
            'shear_status': 'PASS' if eta_shear <= 1.0 else 'FAIL'
        }
    
    def calculate_deflection(self, F_w_k: float, n_brackets: int, L: float,
                           E: float, I: float) -> Dict[str, float]:
        """
        Calculate serviceability deflection
        
        Args:
            F_w_k: Characteristic wind force (kN)
            n_brackets: Number of brackets
            L: Projection length (m)
            E: Elastic modulus (N/mm²)
            I: Second moment of area (mm⁴)
        
        Returns:
            Dictionary with deflection check
        """
        # Force per bracket (N)
        F_SLS = (F_w_k / n_brackets) * 1000
        
        # Length in mm
        L_mm = L * 1000
        
        # Deflection (mm) - cantilever with point load at tip
        delta = (F_SLS * L_mm**3) / (3 * E * I) if I > 0 else 999999
        
        # Deflection limit (mm)
        delta_limit = min(L_mm / 150, 20)
        
        # Utilization
        eta_deflection = delta / delta_limit if delta_limit > 0 else 999
        
        return {
            'delta': delta,
            'delta_limit': delta_limit,
            'eta_deflection': eta_deflection,
            'deflection_status': 'PASS' if eta_deflection <= 1.0 else 'FAIL'
        }


if __name__ == "__main__":
    # Example calculation
    calc = ProjectingSignCalculator()
    
    # Example inputs (from methodology document)
    inputs = {
        'sign_width': 2.0,  # m
        'sign_height': 1.5,  # m
        'projection': 0.6,  # m
        'mounting_height': 4.5,  # m
        'terrain_category': 'III',
        'v_b_0': 22.5,  # m/s (London)
        'c_dir': 1.0,
        'c_season': 1.0,
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
    
    print("="*60)
    print("PROJECTING SIGN CALCULATION EXAMPLE")
    print("="*60)
    print(f"\nWind Pressure: {results['q_p']:.3f} kN/m²")
    print(f"Characteristic Force: {results['F_w_k']:.2f} kN")
    print(f"Design Force: {results['F_w_Ed']:.2f} kN")
    print(f"\nAnchor Combined Utilization: {results['anchor_check']['eta_combined']:.2f}")
    print(f"Bracket Bending Utilization: {results['bracket_check']['eta_bending']:.2f}")
    print(f"Deflection Utilization: {results['deflection_check']['eta_deflection']:.2f}")
    print(f"\nOverall Status: {results['overall_status']}")
