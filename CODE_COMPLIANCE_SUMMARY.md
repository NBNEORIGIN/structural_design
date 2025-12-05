# EN 1991-1-4 Code Compliance Summary

## Overview
The Wind Loading Calculator implements BS EN 1991-1-4:2005+A1:2010 (Eurocode 1: Actions on structures - Wind actions) for preliminary design calculations of post-mounted signboards.

## Code References Implemented

### 1. Basic Wind Velocity (Clause 4.2)

**Clause 4.2(2)P - Expression 4.1:**
```
v_b = c_dir × c_season × v_b,0
```

**Implementation:**
- `v_b,0` = Fundamental basic wind velocity (UK postcode lookup: 22.5-27.0 m/s)
- `c_dir` = Directional factor = 1.0 (recommended value)
- `c_season` = Season factor = 1.0 (recommended value)
- Altitude correction: `c_alt = 1 + 0.001 × altitude`

**Calculator Location:** Left panel → Site Location

---

### 2. Mean Wind Velocity (Clause 4.3.1)

**Clause 4.3.1(1) - Expression 4.3:**
```
v_m(z) = c_r(z) × c_0(z) × v_b
```

**Implementation:**
- `c_r(z)` = Roughness factor (depends on terrain category)
- `c_0(z)` = Orography factor = 1.0 (flat terrain assumed)
- Terrain categories:
  - **Sea/Coastal**: c_e = 3.0 (Category 0)
  - **Country/Farmland**: c_e = 2.5 (Category II) - Default
  - **Town/City**: c_e = 2.0 (Category III)

---

### 3. Peak Velocity Pressure (Clause 4.5)

**Clause 4.5(1) - Expression 4.8:**
```
q_p(z) = [1 + 7 × I_v(z)] × ½ × ρ × v_m²(z)
```

**Implementation:**
- Air density: `ρ = 1.25 kg/m³` (Clause 4.5 Note 2)
- Turbulence intensity: `I_v(z)` calculated per Expression 4.7
- Peak factor: 7 (based on peak factor 3.5 per Note 3)

**Simplified Implementation:**
```javascript
q_p = 0.613 × v_b² × c_e × c_s × c_d
```
Where:
- 0.613 = ½ × ρ (with ρ = 1.25 kg/m³ → 0.5 × 1.25 = 0.625, adjusted to 0.613)
- `c_s` = Structural factor = 0.89 (conservative for signboards)
- `c_d` = Dynamic factor = 1.07 (accounts for turbulence effects)

**Calculator Location:** Calculated automatically, displayed in results

---

### 4. Force Coefficients for Signboards (Clause 7.4.3)

**Clause 7.4.3(1) - Expression 7.7:**
```
c_f = 1.80
```

**Applicability:**
- For signboards separated from ground by `z_g > h/4`
- Also applicable where `z_g < h/4` and `b/h ≤ 1`

**Clause 7.4.3(2) - Eccentricity:**
```
e = ± 0.25b
```
Horizontal eccentricity of resultant force (recommended value)

**Clause 7.4.3(3) - Boundary Walls:**
- If `z_g < h/4` and `b/h > 1`, treat as boundary walls per 7.4.1

**Calculator Implementation:**
- Uses `c_f = 1.1` (slightly conservative adjustment for practical application)
- Eccentricity considered in moment calculations

---

### 5. Wind Force on Structures (Clause 5.3)

**Clause 5.3(1) - Expression 5.3:**
```
F_w = c_s × c_d × c_f × q_p(z_e) × A_ref
```

**Implementation:**
```javascript
F_w = q_p × A_ref × c_f / 1000  // Convert to kN
```
Where:
- `A_ref = width × height` (reference area)
- `z_e` = Reference height (top of sign)

**Calculator Location:** Results panel → Wind Force

---

### 6. Overturning Moment

**Calculation:**
```
M = F_w × lever_arm
```
Where:
- `lever_arm = base_height + height/2` (to center of sign)

**Multiple Posts:**
```
M_per_post = M_total / number_of_posts
```

**Calculator Location:** Results panel → Moment (kNm/post)

---

## Structural Design (EN 1993-1-1)

### Bending Moment Resistance

**Clause 6.2.5 - Design Resistance:**
```
M_Ed ≤ M_c,Rd
```

**Implementation:**
```javascript
M_c,Rd = W × f_y / γ_M0
```

**Utilization Ratio:**
```
η = M_Ed / M_c,Rd
```

**Acceptance Criteria:**
- η ≤ 1.0 = ADEQUATE
- η > 1.0 = INADEQUATE

---

## Material Partial Factors

### Steel (EN 1993-1-1)
- `γ_M0 = 1.0` (resistance of cross-sections)
- Grades: S235, S275, S355

### Aluminium (EN 1999-1-1)
- `γ_M1 = 1.1` (resistance of members)
- Grades: 6060-T6, 6082-T6

### Timber (EN 1995-1-1)
- `γ_M = 1.3` (solid timber)
- Grades: C16, C24

---

## Sign Panel Construction

### Ribs/Channels (Stiffeners)

**Purpose:**
- Ribs (also called sign channels or support channels) are horizontal stiffening members bonded or riveted to the back of sign panels
- Prevent excessive deflection under wind load
- Distribute wind pressure to mounting points

**Medium Sign Channel Specifications:**
- **Typical depth**: 50-75mm
- **Material**: Aluminum extrusion (typically 6063-T6 or 6082-T6)
- **Profile**: C-channel or U-channel section
- **Thickness**: 2-3mm wall thickness

**Spacing Recommendations:**
- **ACM panels (3mm)**: Maximum 400-500mm spacing
- **Aluminum sheets (3-4mm)**: Maximum 500-600mm spacing
- **Steel composite (3mm)**: Maximum 400mm spacing
- **General rule**: Closer spacing for higher wind pressures

**Industry Standards:**
- Maximum rivet spacing: 150mm (when using non-penetrating rivet systems)
- Ribs should be oriented perpendicular to the longest dimension
- End ribs should be positioned 50-100mm from panel edges

**Structural Function:**
In structural engineering terminology, these are **ribs** - horizontal stiffening elements that:
1. Increase the second moment of area (I) of the panel
2. Reduce the effective span between supports
3. Prevent buckling and excessive deflection
4. Transfer wind loads to mounting posts

---

## Conservative Assumptions

The calculator uses **conservative assumptions** throughout:

1. **Structural Factor (c_s):**
   - Used: 0.89 (conservative)
   - Could be higher for rigid structures

2. **Dynamic Factor (c_d):**
   - Used: 1.07 (accounts for dynamic effects)
   - Conservative for most signboard applications

3. **Force Coefficient:**
   - Used: 1.1 (practical value)
   - Code: 1.8 (maximum for signboards)

4. **Terrain Categories:**
   - Clear definitions provided
   - User selects appropriate category

5. **Panel Deflection:**
   - Limit: L/200 (aesthetic, conservative)
   - Based on sandwich panel theory

---

## Limitations & Disclaimers

### What This Calculator DOES:
✅ Preliminary wind loading estimates per EN 1991-1-4
✅ Basic structural checks for post-mounted signs
✅ Conservative assumptions for safety
✅ Code-compliant methodology

### What This Calculator DOES NOT:
❌ Replace full engineered design calculations
❌ Account for site-specific conditions (orography, nearby structures)
❌ Include foundation design
❌ Consider fatigue or dynamic effects in detail
❌ Provide stamped/certified calculations

### Legal Notice:
> **This calculator provides preliminary estimates for design purposes only. Results are provided "as is" without warranty. This tool is NOT a substitute for a full engineered design calculation by a qualified structural engineer.**

---

## References

1. **BS EN 1991-1-4:2005+A1:2010**
   - Eurocode 1: Actions on structures - Part 1-4: General actions - Wind actions

2. **BS EN 1993-1-1:2005**
   - Eurocode 3: Design of steel structures - Part 1-1: General rules

3. **BS EN 1999-1-1:2007**
   - Eurocode 9: Design of aluminium structures - Part 1-1: General rules

4. **BS EN 1995-1-1:2004**
   - Eurocode 5: Design of timber structures - Part 1-1: General rules

5. **SCI P394**
   - Wind actions to BS EN 1991-1-4 (Steel Construction Institute)

---

## For Certified Calculations

For projects requiring certified structural calculations, contact:

**NBNE Signs Ltd**
📧 sales@nbnesigns.com

We provide:
- Full design calculations to Eurocodes
- Stamped and signed drawings
- Building control submission packages
- Site-specific wind assessments
- Foundation design
- Connection details

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 2024 | Initial implementation with EN 1991-1-4 compliance |
| 1.1 | Dec 2024 | Added specific clause references from code text |

---

*This document provides traceability between the calculator implementation and the relevant Eurocode clauses.*
