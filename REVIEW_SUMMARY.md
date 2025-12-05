# Review Summary - New Sign Calculators

**Date**: December 4, 2024  
**Reviewer**: Toby Fletcher, CEng MIMechE  
**Status**: Ready for Review

---

## Quick Summary

✅ **Projecting Sign Calculator**: Fully functional and verified  
✅ **Post-Mounted Calculator**: Fully functional and verified  
✅ **API Integration**: Complete and tested  
⏳ **Frontend**: Pending  
⏳ **Documentation**: Pending

---

## What to Review

### 1. **Technical Review Document** 📄
**File**: `CENG_REVIEW_NEW_CALCULATORS.md`

**Contents**:
- Complete methodology review for both calculators
- Hand calculations verifying all formulas
- Worked examples with step-by-step verification
- Assumptions and limitations clearly identified
- Recommendations for deployment

**Key Findings**:
- ✅ Projecting sign: Methodology sound, calculations verified
- ⚠️ Post-mounted: Needs validation of 10% c_f increase
- ⚠️ Both: Need disclaimers about foundation design and fatigue

**Action Required**:
- Review methodology sections (Sections 1 & 2)
- Check hand calculations (Sections 1.3 & 2.3)
- Review assumptions (Sections 1.4 & 2.4)
- Approve or request changes (Section 7)

---

### 2. **Test Results** 🧪
**File**: `test_new_calculators.py`

**Test Results**:
```
Projecting Sign Calculator:
  ✅ Wind force: 2.537 kN (matches hand calc)
  ✅ Design force: 3.805 kN (matches hand calc)
  ✅ Anchor utilization: 0.568 (matches hand calc)
  ✅ Overall status: ADEQUATE

Post-Mounted Calculator:
  ✅ Force on sign: 5.46 kN (matches hand calc)
  ✅ Total moment: 20.01 kNm (matches hand calc)
  ✅ Post utilization: 0.605 (matches hand calc)
  ✅ Overall status: ADEQUATE
```

**Action Required**:
- Run `python test_new_calculators.py` to verify
- Check that all calculations match expectations
- Review edge case behavior

---

### 3. **Code Review** 💻

**Files to Review**:
1. `projecting_sign_calculator.py` (600 lines)
2. `post_mounted_calculator.py` (400 lines)
3. `api.py` (updated)

**What to Check**:
- Code is well-commented with standard references
- Formulas match the standards (EN 1991-1-4, P394)
- Error handling is appropriate
- Warnings are clear and helpful

**Quick Code Spot Checks**:

#### Projecting Sign - Force Coefficient:
```python
# Line ~169 in projecting_sign_calculator.py
c_f = 2.0  # Force coefficient for flat plate perpendicular to wind
```
✅ Correct per EN 1991-1-4 Table 7.13

#### Projecting Sign - Peak Pressure:
```python
# Line ~285 in projecting_sign_calculator.py
q_p_Pa = 0.5 * self.AIR_DENSITY * v_m**2 * (1 + 7 * I_v)
return q_p_Pa / 1000  # Convert Pa to kN/m²
```
✅ Correct per EN 1991-1-4 Equation 4.8

#### Post-Mounted - Force Coefficient Adjustment:
```python
# Line ~195 in post_mounted_calculator.py
c_f = 0.935 + 0.1839 * np.log(h_over_d)
c_f *= 1.1  # 10% increase for free-standing
```
⚠️ Needs validation (see review document)

---

## Key Questions for Your Review

### 1. Methodology Approval

**Question**: Do you approve the EN 1991-1-4 Eurocode approach for projecting signs?

**Context**:
- Different from P394 (which is UK-specific)
- More comprehensive (includes structural verification)
- Well-established methodology

**Your Decision**: [ ] Approve [ ] Modify [ ] Reject

---

### 2. Force Coefficient for Post-Mounted

**Question**: Do you approve the 10% increase in c_f for free-standing signs?

**Context**:
- Based on engineering judgment
- Conservative approach
- Needs literature validation

**Options**:
- [ ] Approve as-is (conservative)
- [ ] Require literature validation before deployment
- [ ] Use different factor (specify: ___%)
- [ ] Remove adjustment (use P394 values directly)

**Your Decision**: _________________

---

### 3. Disclaimers

**Question**: Are the proposed disclaimers adequate?

**Proposed for Projecting Signs**:
```
IMPORTANT NOTICES:
1. Foundation/wall fixings design by structural engineer required
2. Substrate condition and capacity must be verified on site
3. Fatigue not assessed - regular inspection required
4. Installation must comply with manufacturer's specifications
5. This is a preliminary design - final design requires CEng sign-off
```

**Proposed for Post-Mounted**:
```
IMPORTANT NOTICES:
1. Foundation design by structural engineer required
2. Soil investigation and bearing capacity verification required
3. For posts > 6m, consider dynamic wind effects
4. Fatigue not assessed - regular inspection required
5. This is a preliminary design - final design requires CEng sign-off
```

**Your Decision**: [ ] Approve [ ] Modify (see notes below)

**Modifications needed**: _________________

---

### 4. Deployment Strategy

**Question**: Which deployment approach do you prefer?

**Option A**: Deploy both calculators now
- Pros: Full functionality immediately
- Cons: Post-mounted c_f needs validation

**Option B**: Deploy projecting only, validate post-mounted
- Pros: More conservative
- Cons: Delayed full functionality

**Option C**: Deploy both with strong disclaimers
- Pros: Functionality available, users warned
- Cons: Relies on disclaimers

**Your Decision**: [ ] Option A [ ] Option B [ ] Option C

---

### 5. Insurance Notification

**Question**: Should we notify insurers before deploying?

**Context**:
- New calculation types
- Different standards (Eurocode vs P394)
- Structural verification included

**Your Decision**: [ ] Yes, notify first [ ] No, deploy then notify [ ] Unsure

---

## Action Items Based on Review

### Before Deployment:

**High Priority** (Must Complete):
- [ ] Review and approve methodologies
- [ ] Decide on c_f adjustment for post-mounted
- [ ] Finalize disclaimers
- [ ] Choose deployment strategy

**Medium Priority** (Should Complete):
- [ ] Validate 10% c_f increase (if using)
- [ ] Create validation test cases
- [ ] Update Excel validation workbook
- [ ] Notify insurers

**Low Priority** (Can Do Later):
- [ ] Add aspect ratio refinement for c_f
- [ ] Add dynamic effects check
- [ ] Add fatigue assessment option

---

## Recommended Next Steps

### If Approved:

1. **Immediate** (Today):
   - Add disclaimers to calculator outputs
   - Update `INSURANCE_NOTIFICATION.md`
   - Create validation test suite

2. **Short-term** (This Week):
   - Update frontend with sign type selector
   - Create user documentation
   - Perform integration testing

3. **Before Launch**:
   - External CEng peer review
   - Insurance confirmation
   - Final testing

### If Changes Needed:

1. Document required changes
2. Implement modifications
3. Re-test and re-review
4. Proceed with deployment

---

## Files for Your Review

### Primary Documents:
1. ✅ `CENG_REVIEW_NEW_CALCULATORS.md` - **START HERE**
2. ✅ `INTEGRATION_PROGRESS.md` - Technical progress
3. ✅ This file - `REVIEW_SUMMARY.md`

### Code Files:
4. ✅ `projecting_sign_calculator.py`
5. ✅ `post_mounted_calculator.py`
6. ✅ `api.py`

### Test Files:
7. ✅ `test_new_calculators.py`

### Supporting:
8. ✅ `PROJECTING_SIGN_INTEGRATION_PLAN.md` - Original plan

---

## Sign-Off

**I have reviewed**:
- [ ] Methodology document
- [ ] Test results
- [ ] Code implementation
- [ ] Assumptions and limitations

**My decision**:
- [ ] Approved for deployment
- [ ] Approved with modifications (see notes)
- [ ] Requires further work (see notes)

**Notes**:
_________________
_________________
_________________

**Signature**: _________________  
**Date**: _________________

---

## Quick Reference

### Run Tests:
```bash
cd "g:\My Drive\003 APPS\018 Structural Design\wind-loading-calculator"
python test_new_calculators.py
```

### Test Individual Calculators:
```bash
python projecting_sign_calculator.py
python post_mounted_calculator.py
```

### Start API Server:
```bash
python api.py
```

---

**Questions?** Review the detailed methodology document first, then contact if clarification needed.

**Ready to proceed?** Complete the sign-off section and we'll implement your decisions.
