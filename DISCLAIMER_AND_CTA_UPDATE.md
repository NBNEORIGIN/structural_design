# Disclaimer Banner & CTA Update

## ✅ Changes Completed

### 1. **Prominent Disclaimer Banner Added**
- **Location**: Top of page (above header)
- **Style**: Professional red gradient banner with animation
- **Visibility**: Always visible, cannot be dismissed
- **Content**: Clear legal disclaimer

### 2. **CTA Button Relocated**
- **Old location**: Left panel (removed)
- **New location**: Top banner (prominent position)
- **Style**: White button with hover effects
- **Action**: Opens your enquiry form in new tab

## 📋 Disclaimer Text

The banner displays:

> **IMPORTANT DISCLAIMER**
> 
> **This tool is provided "as is" with no warranties or guarantees.** No liability is accepted for its use. This calculator provides preliminary estimates only and is NOT a substitute for professional engineered calculations. Results are not acceptable for insurance, building control, or certification purposes. For verified structural calculations and certified designs, please contact our engineering team.

## 🎨 Visual Features

### Banner Design:
- ⚠️ **Warning icon** with pulsing animation
- **Red gradient background** (#ff6b6b to #ee5a6f)
- **Slide-down animation** on page load
- **Professional typography** with bold emphasis
- **Responsive layout** adapts to screen size

### CTA Button:
- **White background** with red text
- **Hover effect**: Lifts up with shadow
- **Clear label**: "📧 Get Professional Calculation"
- **Opens in new tab** to avoid losing calculator state

## 🔧 Action Required: Update Enquiry Form URL

**Line 1240** in `preview_3d.html` needs your actual enquiry form URL:

```javascript
const enquiryFormUrl = 'https://www.nbnesigns.com/contact'; // CHANGE THIS
```

### Please provide:
1. **Your enquiry form URL** (e.g., `https://www.nbnesigns.com/enquiry`)
2. **Does your form accept URL parameters?** (e.g., pre-filling fields)
3. **What parameters does it accept?** (if any)

### Current Implementation:
The button passes these parameters to your form:
- `source=wind-calculator` - Identifies where enquiry came from
- `service=structural-engineering` - Pre-selects service type
- `sign_width` - Sign width from calculator
- `sign_height` - Sign height from calculator
- `postcode` - Location from calculator
- `num_posts` - Number of posts

**Example URL generated:**
```
https://www.nbnesigns.com/contact?source=wind-calculator&service=structural-engineering&sign_width=3&sign_height=2&postcode=NE66+2NT&num_posts=2
```

If your form doesn't support parameters, the button will simply open your form page.

## 📱 Responsive Behavior

### Desktop (>1200px):
- Full banner with icon, text, and button side-by-side
- Button on right side

### Tablet (768px-1200px):
- Banner stacks vertically
- Button below text

### Mobile (<768px):
- Compact layout
- Smaller text
- Full-width button

## 🎯 Legal Protection

The disclaimer covers:
- ✅ **"As is" provision** - No warranties
- ✅ **No liability** - Clear statement
- ✅ **Not professional substitute** - Explicit warning
- ✅ **Insurance exclusion** - Not acceptable for insurance
- ✅ **Building control exclusion** - Not for submissions
- ✅ **Certification exclusion** - Not certified calculations
- ✅ **Professional referral** - Directs to your services

## 🔄 User Flow

1. **User arrives** → Sees prominent disclaimer immediately
2. **User reads warning** → Understands limitations
3. **User uses calculator** → Gets preliminary estimates
4. **User needs certification** → Clicks CTA button
5. **Opens enquiry form** → In new tab (calculator stays open)
6. **User submits enquiry** → Your team receives request

## 📊 Benefits

### Legal:
- Clear liability protection
- Professional disclaimer language
- Explicit scope limitations
- Insurance/certification exclusions

### Business:
- Prominent CTA placement
- Drives enquiries to your team
- Maintains calculator as lead generation tool
- Professional appearance builds trust

### User Experience:
- Clear expectations set upfront
- Easy path to professional services
- Calculator remains accessible
- No confusion about tool purpose

## 🎨 Customization Options

If you want to adjust the banner:

### Change Colors:
```css
background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
```

### Change Animation:
```css
animation: slideDown 0.5s ease-out;
```

### Change Button Style:
```css
.cta-button {
    background: white;
    color: #ee5a6f;
}
```

## 📝 Next Steps

1. **Provide your enquiry form URL**
2. **Confirm parameter support** (if any)
3. **Test the button** after URL update
4. **Review disclaimer text** (adjust if needed)
5. **Deploy to production**

## 🚀 Deployment

Once you provide the enquiry form URL:

1. I'll update line 1240 with your URL
2. Commit changes to GitHub
3. Vercel will auto-deploy (30 seconds)
4. Test on live site
5. Ready to use!

---

**Please provide your enquiry form URL so I can complete the integration!**
