# Wind Loading Calculator - Expansion Plan

## Current Status
✅ **Post-Mounted Signs** - COMPLETE
- Full 3D visualization with multiple posts (1-4)
- Wind loading calculations per EN 1991-1-4
- Post structural checks per EN 1993-1-1
- Panel deflection checks per BS 559
- Foundation embedment visualization
- Material selection (steel, aluminum, timber)

## Phase 1: Wall-Mounted Signs 🏢

### Structural Considerations
- **Mounting**: Direct to wall/building facade
- **Loading**: Wind pressure on sign face + eccentricity
- **Fixings**: Anchor bolts/chemical anchors into masonry/concrete
- **Checks Required**:
  - Wind force calculation
  - Fixing capacity (tension & shear)
  - Panel deflection
  - Wall/substrate capacity

### 3D Visualization
- Building wall representation
- Sign panel mounted flush to wall
- Mounting bracket/fixing points
- Wind arrow showing pressure

### Input Parameters
- Sign dimensions (width × height)
- Mounting height above ground
- Wall material (concrete, masonry, steel frame)
- Fixing type (mechanical anchors, chemical anchors, through-bolts)
- Number of fixing points
- Fixing spacing

### Calculations
1. Wind pressure (q_p) - EN 1991-1-4
2. Wind force on sign face
3. Fixing loads (per fixing):
   - Tension force (from wind + eccentricity)
   - Shear force (from self-weight)
4. Fixing capacity checks
5. Panel deflection between fixings

---

## Phase 2: Projecting Signs 🏪

### Structural Considerations
- **Mounting**: Cantilevered from wall
- **Loading**: Wind on both faces + torsion
- **Structure**: Bracket arms + back frame
- **Checks Required**:
  - Wind force (both faces)
  - Bracket bending & deflection
  - Wall fixing capacity
  - Torsional effects

### 3D Visualization
- Building wall
- Projecting sign perpendicular to wall
- Support brackets/arms
- Wind arrow (can hit either face)

### Input Parameters
- Sign dimensions (width × height × projection depth)
- Mounting height
- Bracket configuration (top/bottom, single/double)
- Bracket length (projection from wall)
- Bracket material & section
- Number of wall fixings per bracket

### Calculations
1. Wind pressure on both faces
2. Worst-case wind direction
3. Bracket bending moment
4. Bracket deflection
5. Wall fixing loads (tension + shear)
6. Torsional effects from eccentricity

---

## Phase 3: Monolith Signs 🗼

### Types
1. **Single-Leg Monolith**
   - One central support column
   - Sign panel at top
   - Deep foundation required

2. **Double-Leg Monolith**  
   - Two support columns
   - Sign panel spanning between
   - Lateral stability from spacing

### Structural Considerations
- **Height**: Typically 6-15m tall
- **Foundation**: Deep pile or mass concrete base
- **Loading**: 
  - Wind on sign
  - Column self-weight
  - Overturning moment
- **Checks Required**:
  - Column buckling
  - Foundation overturning
  - Foundation bearing capacity
  - Lateral deflection

### 3D Visualization
- Tall column(s) from ground
- Sign panel at top
- Foundation block (below ground)
- Height scale reference
- Wind arrow

### Input Parameters

#### Single-Leg:
- Sign dimensions
- Column height (ground to sign bottom)
- Column section (circular/square)
- Column diameter/width
- Foundation type (pile/mass concrete)
- Foundation depth
- Soil bearing capacity

#### Double-Leg:
- All above plus:
- Column spacing
- Cross-bracing (yes/no)
- Top beam section

### Calculations

#### Single-Leg:
1. Wind force on sign
2. Overturning moment at base
3. Column buckling check (Euler/Perry-Robertson)
4. Foundation moment capacity
5. Bearing pressure check
6. Lateral deflection at sign level

#### Double-Leg:
1. Wind force distribution between columns
2. Individual column checks
3. Top beam bending (if sign spans between)
4. Foundation checks for each leg
5. Frame stability

---

## Implementation Strategy

### Step 1: Wall-Mounted (Simplest)
- Reuse existing wind calculation logic
- Add fixing calculation module
- Simple 3D: wall plane + sign panel
- Estimated time: 2-3 hours

### Step 2: Projecting (Medium Complexity)
- Bidirectional wind checks
- Bracket structural analysis
- 3D: wall + cantilevered sign + brackets
- Estimated time: 3-4 hours

### Step 3: Monolith (Most Complex)
- Column buckling analysis
- Foundation design calculations
- Two variants (single/double leg)
- 3D: tall columns + foundation visualization
- Estimated time: 4-5 hours

### Total Estimated Time: 9-12 hours

---

## Technical Architecture

### Code Structure
```javascript
// Existing
const SIGN_TYPES = {
    post_mounted: { /* current implementation */ },
    
    // New additions
    wall_mounted: {
        calculate: function() { /* wind + fixings */ },
        render3D: function() { /* wall + sign */ },
        inputs: [ /* specific inputs */ ]
    },
    
    projecting: {
        calculate: function() { /* brackets + bidirectional wind */ },
        render3D: function() { /* cantilevered sign */ },
        inputs: [ /* specific inputs */ ]
    },
    
    monolith_single: {
        calculate: function() { /* column + foundation */ },
        render3D: function() { /* tall structure */ },
        inputs: [ /* specific inputs */ ]
    },
    
    monolith_double: {
        calculate: function() { /* frame + foundations */ },
        render3D: function() { /* two columns + beam */ },
        inputs: [ /* specific inputs */ ]
    }
};
```

### UI Updates
- Tab system already in place
- Add "Monolith" tab with sub-options
- Dynamic input panels per sign type
- Conditional display of relevant results

---

## Standards & References

### EN 1991-1-4 (Wind Actions)
- Clause 7.4.3: Signboards
- Clause 5.3: Wind force on structures
- Clause 7.6: Structural elements (for brackets/columns)

### EN 1993-1-1 (Steel Structures)
- Clause 6.2: Bending resistance
- Clause 6.3: Buckling resistance
- Clause 6.2.6: Shear resistance

### EN 1992-1-1 (Concrete - for foundations)
- Clause 6.1: Bending with axial force
- Clause 6.2: Shear

### BS 559 (Sign Design)
- Deflection limits (L/200)
- Construction requirements

---

## Next Steps

1. ✅ Complete post-mounted implementation
2. 🔄 Implement wall-mounted calculator
3. ⏳ Implement projecting sign calculator
4. ⏳ Implement monolith calculators
5. ⏳ Testing & validation
6. ⏳ Documentation & user guide

---

**Status**: Ready to begin Phase 1 (Wall-Mounted Signs)
**Last Updated**: December 5, 2024
