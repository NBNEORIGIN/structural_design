# Internal Print Feature - Usage Guide

## Overview
The 3D Wind Loading Calculator includes a **hidden print feature** for internal NBNE Signs use only. This feature is NOT accessible to public users.

## How to Use (Internal Staff Only)

### Keyboard Shortcut
Press **`Ctrl + Shift + P`** to print the calculation report.

> **Note:** Regular `Ctrl + P` will not work - the special shortcut prevents accidental printing by users.

## What Gets Printed

### 1. **Company Header**
- NBNE Signs Ltd branding
- Contact: sales@nbnesigns.com
- Standard reference: BS EN 1991-1-4:2005+A1:2010
- Current date (auto-generated)

### 2. **Legal Disclaimer**
⚠️ Prominent warning that this is:
- Preliminary calculation only
- NOT a certified structural design
- NOT for construction without engineer verification

### 3. **Input Parameters Table**
Organized summary of all inputs:
- **Sign Dimensions**: Width, height, base height
- **Location**: Postcode, altitude, wind speed, terrain
- **Post Configuration**: Number of posts, section type, dimensions, embedment
- **Material**: Post material, grade, wall thickness, panel type

### 4. **Calculation Results**
All result cards with:
- Peak Pressure (Pa)
- Wind Force (kN)
- Moment per post (kNm/post)
- Post Utilization (%)
- Channels Required
- Overall Status (ADEQUATE/INADEQUATE)

## Print Layout

The print output is:
- ✅ Clean white background
- ✅ Black text for clarity
- ✅ Professional table formatting
- ✅ Page-break friendly
- ✅ Hides 3D canvas and input panels
- ✅ Shows only relevant calculation data

## Why Hidden from Users?

1. **Legal Protection**: Prevents users from treating preliminary calcs as certified designs
2. **Professional Service**: Encourages users to request full engineered calculations
3. **Quality Control**: Ensures only qualified staff generate reports
4. **Revenue Protection**: Maintains value of professional engineering services

## Email Integration

Users can still request full calculations via:
- **"📧 Request Engineered Design Calculation"** button
- Auto-fills email to: sales@nbnesigns.com
- Includes all current inputs
- Lists required deliverables

## For Developers

### To Enable Print Button (if needed)
Add this HTML to the right panel:
```html
<button class="calculate-btn" onclick="window.print()" style="background: #28a745;">
    🖨️ Print Report (Internal)
</button>
```

### To Change Email
Update line 1056 in `preview_3d.html`:
```javascript
window.location.href = `mailto:sales@nbnesigns.com?subject=${subject}&body=${body}`;
```

### Print Styles
Located in `<style>` section at top of file:
- `@media print { ... }` controls print layout
- `.print-header` class shows/hides print-only content
- `.no-print` class can be added to hide elements when printing

## Best Practices

1. **Always calculate first** before printing
2. **Review results** for adequacy before sharing
3. **Add handwritten notes** if needed for context
4. **File with project documentation**
5. **Never share as final design** - always mark as preliminary

## Support

For questions about the print feature:
- Contact: Internal development team
- File: `preview_3d.html`
- Lines: 8-46 (print styles), 559-590 (print header), 1074-1080 (keyboard shortcut)
