# Projecting Sign Integration Plan

## Overview

Integrate the projecting sign calculation methodology from `015 - LOADING CALCULATOR` into the main wind loading calculator at `018 Structural Design`.

---

## Current Status

### ✅ **Completed - Wall-Mounted Fascia Signs**
- Location: `g:\My Drive\003 APPS\018 Structural Design\wind-loading-calculator\`
- Standard: BS EN 1991-1-4 + SCI P394
- Features:
  - Python calculation engine (`wind_calculator.py`)
  - Flask API (`api.py`)
  - Web interface (`static/index.html`)
  - PDF report generation
  - Validation complete (Sheffield Bioincubator)
  - Excel validation workbook created

### ✅ **Completed - Projecting Signs**
- Location: `G:\My Drive\003 APPS\015 - LOADING CALCULATOR\`
- Standard: EN 1991-1-4 (Eurocode)
- Features:
  - Complete HTML calculator (`projecting_sign_calculator.html`)
  - Full methodology documented (`CALCULATION_METHODOLOGY.md`)
  - Includes:
    - Wind pressure calculations
    - Force coefficients for flat plates
    - Bracket force analysis
    - Anchor/fixing design
    - Bracket member verification
    - Deflection checks

---

## Key Differences Between Methodologies

### Wall-Mounted Fascia (Current)
- **Standard**: BS EN 1991-1-4 + UK NA + SCI P394
- **Approach**: UK-specific methodology with P394 guidance
- **Force Coefficient**: Variable based on h/d ratio (c_f = 0.935 + 0.1839×ln(h/d))
- **Exposure**: UK terrain zones (A, B, C) with town correction
- **Output**: Wind force on sign face

### Projecting Signs (To Integrate)
- **Standard**: EN 1991-1-4 (Eurocode)
- **Approach**: European terrain categories (0, II, III, IV)
- **Force Coefficient**: c_f = 2.0 (flat plate perpendicular to wind)
- **Exposure**: Terrain roughness factors (z_0, k_r)
- **Output**: Wind force + bracket forces + anchor design + deflection

---

## Integration Strategy

### Option 1: Unified Calculator (Recommended)
**Pros:**
- Single interface for all sign types
- Shared codebase and validation
- Consistent user experience
- Easier maintenance

**Cons:**
- More complex initial development
- Need to reconcile UK NA vs Eurocode approaches

### Option 2: Separate Calculators
**Pros:**
- Keep existing code intact
- Simpler to implement
- Each calculator optimized for its purpose

**Cons:**
- Duplicate code
- Inconsistent user experience
- More maintenance overhead

---

## Recommended Implementation: Option 1 (Unified)

### Phase 1: Backend Integration

#### 1.1 Extend `wind_calculator.py`

Add new class for projecting signs:

```python
class ProjectingSignCalculator:
    """
    EN 1991-1-4 Projecting Sign Calculator
    Based on Eurocode methodology
    """
    
    def calculate_wind_loading(self, inputs):
        """
        Main calculation method for projecting signs
        
        Inputs:
        - sign_width (b): m
        - sign_height (h): m
        - projection (e): m
        - mounting_height (z): m
        - terrain_category: 0, II, III, IV
        - v_b_0: fundamental wind velocity (m/s)
        - n_brackets: number of brackets
        - bracket_spacing (s): m
        - sign_weight: kN
        - n_fixings: fixings per bracket
        - fixing_pitch_v: vertical pitch (m)
        - anchor_capacity: {N_Rk, V_Rk, gamma_M}
        - bracket_section: {b_out, h_out, t, f_y}
        
        Returns:
        - Wind pressure calculations
        - Characteristic wind force
        - Design wind force (ULS)
        - Bracket forces (shear, moment, tension)
        - Anchor utilization
        - Bracket stress utilization
        - Deflection check
        - Overall pass/fail
        """
        pass
```

#### 1.2 Add Terrain Category Functions

```python
def get_terrain_parameters(category):
    """
    EN 1991-1-4 Table 4.1
    Returns: {z_0, z_min, k_r}
    """
    terrain_params = {
        '0': {'z_0': 0.003, 'z_min': 1, 'k_r': 0.17},
        'II': {'z_0': 0.05, 'z_min': 2, 'k_r': 0.19},
        'III': {'z_0': 0.3, 'z_min': 5, 'k_r': 0.22},
        'IV': {'z_0': 1.0, 'z_min': 10, 'k_r': 0.24}
    }
    return terrain_params.get(category)

def calculate_roughness_factor(z, z_0, k_r, z_min):
    """EN 1991-1-4 Equation 4.4"""
    z_eff = max(z, z_min)
    return k_r * np.log(z_eff / z_0)

def calculate_turbulence_intensity(z, z_0, z_min, k_I=1.0, c_0=1.0):
    """EN 1991-1-4 Equation 4.7"""
    z_eff = max(z, z_min)
    return k_I / (c_0 * np.log(z_eff / z_0))

def calculate_peak_pressure_eurocode(v_b, c_r, I_v, rho=1.25):
    """EN 1991-1-4 Equation 4.8"""
    v_m = c_r * v_b  # c_0 = 1.0 assumed
    return 0.5 * rho * v_m**2 * (1 + 7 * I_v)
```

#### 1.3 Add Bracket and Anchor Calculations

```python
def calculate_bracket_forces(F_w_Ed, e, n_brackets, s, G_Ed):
    """
    Calculate forces in brackets
    Returns: {V_per_bracket, M_per_bracket, M_wall, N_moment, N_tension_max}
    """
    pass

def calculate_anchor_utilization(V_per_bracket, M_per_bracket, N_vertical,
                                 n_fix, p_v, N_Rk, V_Rk, gamma_M):
    """
    Check anchor capacity
    Returns: {N_Ed, V_Ed, N_Rd, V_Rd, eta_tension, eta_shear, eta_combined}
    """
    pass

def calculate_bracket_stresses(V_per_bracket, e, section, f_y):
    """
    Check bracket member capacity
    Returns: {sigma_Ed, sigma_Rd, tau_Ed, tau_Rd, eta_bending, eta_shear}
    """
    pass

def calculate_deflection(F_w_k, n_brackets, e, E, I):
    """
    Serviceability deflection check
    Returns: {delta, delta_limit, eta_deflection}
    """
    pass
```

### Phase 2: API Integration

#### 2.1 Update `api.py`

Add new endpoint:

```python
@app.route('/api/calculate_projecting', methods=['POST'])
def calculate_projecting():
    """Calculate wind loading for projecting signs"""
    try:
        data = request.json
        calc = ProjectingSignCalculator()
        results = calc.calculate_wind_loading(data)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

### Phase 3: Frontend Integration

#### 3.1 Update `static/index.html`

Add sign type selector at top of form:

```html
<div class="input-group">
    <label>Sign Type:</label>
    <select id="signType" onchange="updateFormFields()">
        <option value="wall_mounted">Wall-Mounted Fascia</option>
        <option value="projecting">Projecting Sign</option>
    </select>
</div>
```

#### 3.2 Dynamic Form Fields

Show/hide fields based on sign type:

**Wall-Mounted Fields:**
- Width, Height, Depth
- Building height
- Postcode lookup
- Terrain (A, B, C)

**Projecting Sign Fields:**
- Width, Height, Projection
- Mounting height
- Terrain category (0, II, III, IV)
- Number of brackets
- Bracket details
- Anchor details

#### 3.3 Results Display

**Wall-Mounted Results:**
- Wind force
- Pass/fail assessment
- Recommendations

**Projecting Sign Results:**
- Wind pressure
- Characteristic force
- Design force
- Bracket forces
- Anchor utilization (with traffic light colors)
- Bracket stress utilization
- Deflection check
- Overall pass/fail

### Phase 4: Validation

#### 4.1 Create Test Cases

Use the worked example from `CALCULATION_METHODOLOGY.md`:
- Sign: 2.0m × 1.5m
- Projection: 0.6m
- Height: 4.5m
- Terrain III
- Expected results documented

#### 4.2 Update Excel Validation

Add new sheet for projecting sign validation with:
- All calculation stages
- Expected vs calculated values
- Pass/fail checks

### Phase 5: Documentation

#### 5.1 Update README

Add section on projecting signs:
- When to use each calculator
- Input requirements
- Interpretation of results

#### 5.2 Update Validation Checklist

Add projecting sign methodology review items

#### 5.3 Insurance Notification

Update to include projecting sign calculations

---

## Technical Considerations

### 1. Standard Compatibility

**Challenge**: Wall-mounted uses BS EN 1991-1-4 + UK NA + P394, Projecting uses EN 1991-1-4 (Eurocode)

**Solution**: 
- Keep both methodologies separate in code
- Clearly label which standard applies
- Add disclaimers about applicability

### 2. Terrain Categories

**Challenge**: Different terrain classification systems

**Solution**:
- Provide mapping guidance (e.g., UK Zone C ≈ Terrain III)
- Allow user to select appropriate category
- Document differences in methodology

### 3. Force Coefficients

**Challenge**: Different approaches (P394 vs Eurocode Table 7.13)

**Solution**:
- Use methodology appropriate to sign type
- Document assumptions clearly
- Validate against published examples

### 4. Output Complexity

**Challenge**: Projecting signs have much more detailed output (brackets, anchors, deflection)

**Solution**:
- Tabbed or collapsible results sections
- Summary view + detailed view
- Clear pass/fail indicators

---

## Timeline Estimate

### Immediate (1-2 days)
- ✅ Review existing projecting sign code
- ✅ Create integration plan (this document)
- ⏳ Set up development branch

### Short-term (3-5 days)
- Add `ProjectingSignCalculator` class
- Implement all calculation methods
- Add unit tests
- Validate against worked example

### Medium-term (5-7 days)
- Update API with new endpoint
- Modify frontend for sign type selection
- Implement dynamic form fields
- Style results display

### Final (2-3 days)
- Integration testing
- Update all documentation
- Create Excel validation for projecting signs
- Peer review

**Total: ~2 weeks**

---

## Next Steps

1. **Confirm approach**: Review this plan and approve Option 1 (Unified Calculator)
2. **Priority**: Decide if projecting signs needed before launch or can be Phase 2
3. **Validation**: Identify external CEng for peer review of projecting sign methodology
4. **Insurance**: Confirm projecting signs covered under same PI policy

---

## Files to Create/Modify

### New Files:
- `projecting_sign_calculator.py` - New calculation class
- `test_projecting_sign.py` - Unit tests
- `PROJECTING_SIGN_VALIDATION.md` - Validation documentation

### Modified Files:
- `wind_calculator.py` - Import projecting sign calculator
- `api.py` - Add new endpoint
- `static/index.html` - Add sign type selector and dynamic forms
- `README.md` - Document projecting sign functionality
- `VALIDATION_CHECKLIST.md` - Add projecting sign review items
- `requirements.txt` - Any new dependencies

---

**Document Version**: 1.0  
**Date**: December 2024  
**Status**: PLANNING - Awaiting approval to proceed
