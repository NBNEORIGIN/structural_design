# 🌬️ Wind Loading Calculator - Interactive 3D

A comprehensive tool for calculating wind loads on post-mounted signs according to BS EN 1991-1-4:2005+A1:2010 (Eurocode 1).

## 🚀 Live Demo

Visit the live calculator: **https://structural-design.vercel.app**

## ✨ Features

- **Interactive 3D Preview**: Real-time visualization of sign structure with Three.js
- **EN 1991-1-4 Compliant**: Full code compliance with specific clause references
- **UK Postcode Lookup**: Automatic wind speed calculation based on location
- **Multiple Post Support**: Configure 1-4 posts with dynamic spacing
- **Material Options**: Steel, aluminum, and timber with various grades
- **Live Calculations**: Instant results as you adjust parameters
- **Professional Reports**: Print-ready calculation summaries (internal use)

## 📋 What It Calculates

- Peak velocity pressure (q_p)
- Wind force on sign face
- Overturning moment per post
- Post utilization ratio
- Required number of ribs/channels
- Panel deflection checks

## 🎯 Use Cases

- Preliminary design estimates for post-mounted signs
- Quick feasibility checks
- Material selection guidance
- Structural adequacy verification

## ⚠️ Important Disclaimers

This calculator provides **preliminary estimates only** and is NOT a substitute for:
- Full engineered design calculations
- Certified structural engineer review
- Building control submissions
- Site-specific assessments

For certified calculations, contact: **sales@nbnesigns.com**

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **3D Graphics**: Three.js
- **Standards**: BS EN 1991-1-4, BS EN 1993-1-1
- **Hosting**: Vercel

## 📦 Repository Structure

```
wind-loading-calculator/
├── preview_3d.html              # Main 3D calculator interface
├── preview.html                 # Alternative 2D interface
├── index.html                   # Landing page redirect
├── CODE_COMPLIANCE_SUMMARY.md   # Eurocode compliance documentation
├── SIGN_CHANNEL_SPECIFICATIONS.md # Technical specifications
├── INTERNAL_PRINT_FEATURE.md    # Internal documentation
└── vercel.json                  # Deployment configuration
```

## 🚀 Deployment

This project is deployed on Vercel and automatically updates when changes are pushed to the `main` branch.

### Deploy Your Own

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/NBNEORIGIN/structural_design)

## 📞 Contact

**NBNE Signs Ltd**
- Email: sales@nbnesigns.com
- Services: Engineered design calculations, stamped drawings, building control submissions

## 📄 License

© 2024 NBNE Signs Ltd. All rights reserved.

---

*Built with precision engineering and modern web technologies.*
