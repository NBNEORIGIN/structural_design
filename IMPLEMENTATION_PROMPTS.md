# Implementation Prompts - Wind Loading Calculator Expansion

Use these prompts in separate chat sessions to implement each feature systematically.

---

## 🏢 PROMPT 1: Wall-Mounted Signs - Basic Structure

**Copy this into a new chat:**

```
I'm working on a wind loading calculator (preview_3d.html) that currently has post-mounted signs working. I need to implement wall-mounted signs.

Current status:
- File: g:\My Drive\003 APPS\018 Structural Design\wind-loading-calculator\preview_3d.html
- Post-mounted signs are complete with 3D visualization
- Tabs exist for wall_mounted, projecting, and post_mounted
- Need to make wall_mounted tab functional

Task 1: Create the wall-mounted sign input panel
- Add a new section that shows when wall_mounted tab is clicked
- Hide post-mounted inputs when wall_mounted is selected
- Inputs needed:
  * Sign dimensions (width × height) - reuse existing
  * Mounting height above ground
  * Wall material (dropdown: Concrete, Masonry, Steel Frame)
  * Fixing type (dropdown: Mechanical Anchors, Chemical Anchors, Through-Bolts)
  * Number of fixing points (4, 6, 8, 12)
  * Fixing spacing (horizontal × vertical in mm)

Please implement the UI switching logic and input panel for wall-mounted signs.
```

---

## 🏢 PROMPT 2: Wall-Mounted Signs - 3D Visualization

**Copy this into a new chat:**

```
I'm implementing wall-mounted signs in preview_3d.html. The input panel is done, now I need the 3D visualization.

Context:
- Three.js scene is set up in updateScene() function
- Currently renders post-mounted signs
- Need to add wall-mounted visualization

Task 2: Create 3D visualization for wall-mounted signs
When sign type is 'wall_mounted':
1. Draw a vertical wall (gray plane, 6m wide × 4m tall)
2. Position sign panel flush against wall at mounting height
3. Add small spheres/cubes at fixing points (red dots)
4. Position wind arrow pointing at sign face
5. No posts or ground foundation needed

The scene should clearly show:
- Building wall
- Sign mounted flat against wall
- Fixing point locations
- Wind direction

Please implement the 3D rendering for wall-mounted signs.
```

---

## 🏢 PROMPT 3: Wall-Mounted Signs - Calculations

**Copy this into a new chat:**

```
I'm implementing wall-mounted sign calculations in preview_3d.html.

Context:
- Wind pressure calculation (q_p) already works
- Need to add fixing load calculations
- Results display at bottom of page

Task 3: Implement wall-mounted sign calculations
Calculate:
1. Wind force on sign: F_w = q_p × A_ref × c_f (c_f = 1.8 for signboards)
2. Moment per fixing (from eccentricity): M = F_w × e / n_fixings
3. Tension per fixing: T = M / spacing_vertical + F_w / n_fixings
4. Shear per fixing: V = (sign_weight × 1.5) / n_fixings (safety factor)
5. Combined utilization: η = √((T/T_capacity)² + (V/V_capacity)²)

Fixing capacities (typical values):
- Mechanical anchors: T = 15kN, V = 10kN
- Chemical anchors: T = 25kN, V = 15kN
- Through-bolts: T = 35kN, V = 20kN

Display results:
- Wind Force (kN)
- Tension per fixing (kN)
- Shear per fixing (kN)
- Fixing Utilization (%)
- Overall Status (ADEQUATE/INADEQUATE if η > 1.0)

Please implement the calculation logic for wall-mounted signs.
```

---

## 🏪 PROMPT 4: Projecting Signs - Basic Structure

**Copy this into a new chat:**

```
I'm implementing projecting signs in preview_3d.html. Wall-mounted signs are complete.

Context:
- Post-mounted and wall-mounted signs work
- Need to implement projecting sign functionality
- Tab exists but not functional

Task 4: Create projecting sign input panel
Inputs needed:
- Sign dimensions (width × height × depth/projection)
- Mounting height above ground
- Bracket configuration (dropdown: Top Only, Top & Bottom, Single Cantilever)
- Bracket length (projection from wall in mm)
- Bracket material (Steel, Aluminum)
- Bracket section (dropdown: 100×100 SHS, 150×150 SHS, 200×100 RHS)
- Number of wall fixings per bracket (2, 3, 4)

Add input validation:
- Projection depth should be ≤ 1500mm typically
- Bracket length = projection + 200mm clearance

Please implement the input panel for projecting signs with proper show/hide logic.
```

---

## 🏪 PROMPT 5: Projecting Signs - 3D Visualization

**Copy this into a new chat:**

```
I'm implementing 3D visualization for projecting signs in preview_3d.html.

Context:
- Wall-mounted and post-mounted visualizations work
- Need projecting sign 3D view

Task 5: Create 3D visualization for projecting signs
Render:
1. Vertical wall (same as wall-mounted)
2. Sign panel perpendicular to wall (projecting outward)
3. Support brackets:
   - If "Top & Bottom": Two horizontal arms from wall to sign
   - If "Top Only": Single arm at top
   - If "Single Cantilever": One central arm
4. Fixing points on wall (red spheres)
5. Wind arrow (can show from side - hitting edge of sign)

Key positions:
- Wall at x = 0
- Sign projects in +Z direction
- Brackets connect wall to sign back frame
- Show bracket as rectangular tubes

Please implement the 3D rendering for projecting signs.
```

---

## 🏪 PROMPT 6: Projecting Signs - Calculations

**Copy this into a new chat:**

```
I'm implementing projecting sign calculations in preview_3d.html.

Context:
- Wind pressure (q_p) calculation works
- Need bracket structural analysis

Task 6: Implement projecting sign calculations
Calculate:
1. Wind force: F_w = q_p × A_ref × c_f (c_f = 1.8)
2. Bracket bending moment: M = F_w × bracket_length / n_brackets
3. Bracket section modulus: W (from section properties)
4. Bracket stress: σ = M / W
5. Bracket utilization: η_bracket = σ / f_y
6. Bracket deflection: δ = (F × L³) / (3 × E × I)
7. Deflection limit: L / 200
8. Wall fixing loads:
   - Tension: T = M / (bracket_spacing × n_fixings)
   - Shear: V = F_w / (n_brackets × n_fixings)

Section properties (example):
- 100×100 SHS: W = 37.7 cm³, I = 188.5 cm⁴
- 150×150 SHS: W = 92.8 cm³, I = 696 cm⁴

Display results:
- Wind Force (kN)
- Bracket Moment (kNm)
- Bracket Utilization (%)
- Bracket Deflection (mm)
- Wall Fixing Tension (kN)
- Wall Fixing Shear (kN)
- Overall Status

Please implement the calculation logic for projecting signs.
```

---

## 🗼 PROMPT 7: Monolith Signs - Tab & Type Selection

**Copy this into a new chat:**

```
I'm adding monolith signs to preview_3d.html. Wall-mounted and projecting signs are complete.

Context:
- Three sign types work (post, wall, projecting)
- Need to add fourth tab for monoliths
- Monoliths have two variants: single-leg and double-leg

Task 7: Add monolith sign tab and variant selection
1. Add "Monolith" tab to header (after Post-Mounted)
2. When clicked, show sub-options:
   - Radio buttons: "Single Leg" or "Double Leg"
3. Create input panel structure for monoliths
4. Add basic inputs (common to both):
   - Sign dimensions (width × height)
   - Column height (ground to sign bottom) in meters
   - Column section type (Circular CHS, Square SHS)
   - Column diameter/width (mm)
   - Wall thickness (mm)
   - Foundation depth (m)
   - Soil bearing capacity (kN/m²)

Please implement the monolith tab, variant selection, and basic input panel.
```

---

## 🗼 PROMPT 8: Monolith Single-Leg - 3D & Calculations

**Copy this into a new chat:**

```
I'm implementing single-leg monolith signs in preview_3d.html.

Context:
- Monolith tab exists with variant selection
- Need single-leg implementation

Task 8A: 3D Visualization for single-leg monolith
Render:
1. Tall central column from ground (6-15m typical)
2. Sign panel at top of column
3. Foundation block below ground (semi-transparent)
4. Ground plane
5. Wind arrow at sign height
6. Scale reference (height markers)

Task 8B: Calculations for single-leg monolith
Calculate:
1. Wind force on sign: F_w = q_p × A_ref × c_f
2. Overturning moment at base: M_base = F_w × (h_column + h_sign/2)
3. Column buckling check (Euler): P_cr = (π² × E × I) / (L_eff²)
4. Column bending stress: σ = M / W
5. Column utilization: η = σ / f_y + P / P_cr
6. Foundation moment capacity check
7. Bearing pressure: q = (P + M/B) / A_foundation
8. Lateral deflection at top: δ = (F × H³) / (3 × E × I)

Display results:
- Wind Force (kN)
- Base Moment (kNm)
- Column Utilization (%)
- Bearing Pressure (kN/m²)
- Top Deflection (mm)
- Overall Status

Please implement single-leg monolith visualization and calculations.
```

---

## 🗼 PROMPT 9: Monolith Double-Leg - 3D & Calculations

**Copy this into a new chat:**

```
I'm implementing double-leg monolith signs in preview_3d.html.

Context:
- Single-leg monolith works
- Need double-leg variant

Task 9A: Additional inputs for double-leg
Add to input panel:
- Column spacing (m) - distance between columns
- Top beam section (dropdown: 150×150 SHS, 200×100 RHS, etc.)
- Cross-bracing (checkbox: Yes/No)

Task 9B: 3D Visualization for double-leg monolith
Render:
1. Two tall columns (spaced apart)
2. Sign panel spanning between columns at top
3. Top beam connecting columns
4. Optional cross-bracing (X-pattern between columns)
5. Two foundation blocks
6. Wind arrow

Task 9C: Calculations for double-leg monolith
Calculate:
1. Wind force distribution: F_per_column = F_w / 2
2. Individual column checks (same as single-leg)
3. Top beam bending: M_beam = (F_w × h_sign) / 2
4. Top beam stress and utilization
5. Frame stability factor
6. Foundation checks for each leg
7. Differential settlement consideration

Display results:
- Wind Force per Column (kN)
- Column Utilization (%)
- Top Beam Utilization (%)
- Bearing Pressure per Foundation (kN/m²)
- Frame Stability Factor
- Overall Status

Please implement double-leg monolith visualization and calculations.
```

---

## 🎨 PROMPT 10: UI Polish & Testing

**Copy this into a new chat:**

```
I'm finalizing the wind loading calculator with all sign types implemented.

Context:
- All sign types work: post-mounted, wall-mounted, projecting, single-leg monolith, double-leg monolith
- Need final polish and testing

Task 10: UI improvements and testing
1. Ensure smooth transitions between sign types
2. Add loading indicators during calculations
3. Improve result card styling consistency
4. Add tooltips to complex inputs
5. Ensure print functionality works for all sign types
6. Test edge cases:
   - Very small signs
   - Very large signs
   - Extreme wind speeds
   - Zero/minimum values
7. Add input validation messages
8. Ensure 3D camera resets properly between sign types
9. Check mobile responsiveness
10. Add "Export Results" button (CSV or PDF)

Please implement UI polish, validation, and comprehensive testing.
```

---

## 📚 PROMPT 11: Documentation & Examples

**Copy this into a new chat:**

```
I need comprehensive documentation for the wind loading calculator.

Context:
- All sign types implemented and working
- Need user guide and technical documentation

Task 11: Create documentation
1. USER_GUIDE.md:
   - How to use each sign type
   - Input descriptions
   - Result interpretations
   - Example calculations
   - Screenshots/diagrams

2. TECHNICAL_DOCUMENTATION.md:
   - Calculation methods
   - Code references (EN 1991-1-4, etc.)
   - Assumptions and limitations
   - Validation against hand calculations
   - Material properties used

3. EXAMPLES.md:
   - 5 worked examples (one per sign type)
   - Real-world scenarios
   - Step-by-step walkthroughs

4. FAQ.md:
   - Common questions
   - Troubleshooting
   - When to get professional calculations

Please create comprehensive documentation for the calculator.
```

---

## 🚀 Implementation Order

**Recommended sequence:**

1. ✅ **PROMPT 1-3**: Wall-Mounted (complete one sign type)
2. ✅ **PROMPT 4-6**: Projecting (build on wall-mounted concepts)
3. ✅ **PROMPT 7**: Monolith setup (prepare for complex types)
4. ✅ **PROMPT 8**: Single-leg monolith
5. ✅ **PROMPT 9**: Double-leg monolith
6. ✅ **PROMPT 10**: Polish & testing
7. ✅ **PROMPT 11**: Documentation

**Estimated time per prompt**: 30-60 minutes each

---

## 📝 Notes

- Each prompt is self-contained
- Can be done in any order (though sequential is recommended)
- Test thoroughly after each implementation
- Commit to git after each major feature
- Deploy to Vercel to test live

**Current Status**: Post-mounted signs complete ✅
**Next Step**: Start with PROMPT 1 (Wall-Mounted Basic Structure)

---

**Good luck with the implementation!** 🎉
