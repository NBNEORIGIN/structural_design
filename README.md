# BS EN 1991-1-4 Wind Loading Calculator for Signage

Professional web-based tool for calculating wind loading on signage structures per BS EN 1991-1-4:2005+A1:2010 (UK implementation).

## Overview

This calculator implements the BS EN 1991-1-4 methodology as documented in **SCI Publication P394** "Wind Actions to BS EN 1991-1-4". It provides accurate wind loading calculations for signage installations, validated against the Sheffield Bioincubator worked example.

**Developed by:** Toby Fletcher, CEng MIMechE  
**Company:** North By North East Print & Sign Ltd  
**Standard:** BS EN 1991-1-4:2005+A1:2010  
**Reference:** SCI Publication P394

## Features

### Current Version (v1.0.0)
- ✅ Wall-mounted fascia sign calculations
- ✅ Full BS EN 1991-1-4 Stage 1-25 procedure
- ✅ UK postcode-based wind speed lookup
- ✅ Altitude, exposure, and terrain corrections
- ✅ Professional web interface
- ✅ PDF report generation
- ✅ Validated against SCI P394 worked example

### Calculation Stages Implemented
1. **Stage 1:** Fundamental wind speed (v_map) from UK wind map
2. **Stage 2:** Altitude factor (c_alt)
3. **Stage 4:** Directional factor (c_dir) - non-directional approach
4. **Stage 5:** Displacement height (h_dis)
5. **Stage 6:** Distance to shoreline
6. **Stage 7:** Exposure factor (c_e) with terrain zones
7. **Stage 8-9:** Town terrain correction (c_e,T)
8. **Stage 11:** Peak velocity pressure (q_p)
9. **Stage 12-17:** Orography (c_o = 1.0, conservative)
10. **Stage 18:** Size factor (c_s)
11. **Stage 19:** Dynamic factor (c_d)
12. **Stage 21:** Force coefficient (c_f)
13. **Stage 24:** Wind force calculation

### Future Enhancements (Phase 2+)
- 🔄 12-sector directional calculation
- 🔄 Full orographic assessment
- 🔄 Projecting sign calculations
- 🔄 Post-mounted sign calculations
- 🔄 Advanced displacement height
- 🔄 Exact postcode database
- 🔄 User accounts and calculation history

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the project:**
```bash
cd "g:\My Drive\003 APPS\018 Structural Design\wind-loading-calculator"
```

2. **Create virtual environment (recommended):**
```bash
python -m venv venv
```

3. **Activate virtual environment:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web Application

1. **Start the Flask server:**
```bash
python api.py
```

2. **Open your browser and navigate to:**
```
http://localhost:5000
```

3. **Fill in the form with your sign details:**
   - Sign dimensions (width, height, depth)
   - Installation height above ground
   - Site location (postcode)
   - Site altitude
   - Environmental factors (terrain, distance to shore)

4. **Click "Calculate Wind Loading"** to get results

### Running Tests

Validate the calculator against the Sheffield Bioincubator example:

```bash
python test_wind_calculator.py
```

Expected output:
```
✓ Sheffield Bioincubator validation PASSED
  All values within acceptable tolerance
```

### Using the Python API Directly

```python
from wind_calculator import WindLoadCalculator

# Initialize calculator
calculator = WindLoadCalculator()

# Define inputs
inputs = {
    'sign_width': 5.0,        # meters
    'sign_height': 2.0,       # meters
    'sign_depth': 0.4,        # meters
    'building_height': 8.0,   # meters
    'site_altitude': 50,      # meters above sea level
    'postcode': 'NE66 2NT',
    'distance_to_shore': 5,   # km
    'terrain_type': 'country',
    'distance_into_town': 0,
    'mounting_type': 'wall_mounted_fascia'
}

# Calculate wind loading
results = calculator.calculate_wind_loading(inputs)

# Access results
print(f"Wind Force: {results['force_kN']:.1f} kN")
print(f"Peak Pressure: {results['q_p']:.0f} Pa")
print(f"Overturning Moment: {results['moment_kNm']:.1f} kNm")
```

### Generating PDF Reports

```python
from wind_calculator import WindLoadCalculator
from report_generator import generate_report

# Calculate wind loading
calculator = WindLoadCalculator()
results = calculator.calculate_wind_loading(inputs)

# Generate PDF report
project_info = {
    'name': 'High Street Signage',
    'reference': 'PROJ-2024-001',
    'client': 'ABC Retail Ltd'
}

generate_report(results, inputs, 'wind_report.pdf', project_info)
```

## API Endpoints

### POST /api/calculate-wind-loading
Calculate wind loading for given parameters.

**Request Body:**
```json
{
    "sign_width": 5.0,
    "sign_height": 2.0,
    "sign_depth": 0.4,
    "building_height": 8.0,
    "postcode": "NE66 2NT",
    "altitude": 50,
    "distance_to_shore": "5",
    "terrain_type": "country",
    "distance_into_town": 0,
    "sign_type": "wall_mounted_fascia"
}
```

**Response:**
```json
{
    "design_wind_speed": 22.5,
    "peak_pressure": 1050,
    "wind_force": 12.5,
    "overturning_moment": 45.2,
    "calculation_summary": {
        "v_map": 22.0,
        "c_alt": 1.05,
        "c_dir": 1.0,
        "c_e": 2.15,
        "c_s": 0.95,
        "c_d": 1.0,
        "c_f": 1.05
    },
    "warnings": [...],
    "methodology": "BS EN 1991-1-4:2005+A1:2010",
    "reference": "SCI Publication P394"
}
```

### POST /api/validate-postcode
Validate UK postcode and return wind speed.

### GET /api/health
Health check endpoint.

### GET /api/info
Return API information and capabilities.

## Validation

The calculator has been validated against the **Sheffield Bioincubator** worked example from SCI P394 (Section 9.1, pages 63-73):

| Parameter | Calculated | Expected | Status |
|-----------|-----------|----------|--------|
| v_map | 22.1 m/s | 22.1 m/s | ✅ |
| c_alt | 1.10 | 1.10 | ✅ |
| q_p | ~1058 Pa | 1058 Pa | ✅ |
| c_s | 0.85 | 0.85 | ✅ |
| c_d | 1.03 | 1.03 | ✅ |
| c_f | 0.92 | 0.92 | ✅ |
| F_w | ~460 kN | 460 kN | ✅ |

All values within 2% tolerance.

## Important Limitations

This calculator provides **indicative** wind loading calculations. It does **NOT** account for:

- ❌ Orographic effects (hills, cliffs, escarpments)
- ❌ Complex building geometries
- ❌ Local sheltering or exposure effects
- ❌ Dynamic effects for very flexible structures
- ❌ Fatigue considerations

### When to Use Full Certified Calculations

For building control submission or complex installations, a full certified structural calculation is required. Contact North By North East for:

- ✅ Full BS EN 1991-1-4 compliant certification
- ✅ Orographic assessment
- ✅ Complex geometry analysis
- ✅ Foundation and fixing design
- ✅ Building control submission package

**Service:** £350, 48-hour turnaround  
**Contact:** sales@nbnesigns.co.uk | 01665 606 741

## Technical Details

### Calculation Methodology

The calculator follows the simplified procedure from SCI P394:

1. **Wind Speed:** Fundamental wind speed from UK wind map (Figure 5.1)
2. **Corrections:** Altitude, directional, exposure, and terrain corrections
3. **Pressure:** Peak velocity pressure calculation
4. **Factors:** Size, dynamic, and force coefficient determination
5. **Force:** Characteristic wind force on reference area
6. **Moment:** Overturning moment at sign base

### Key Formulae

**Peak Velocity Pressure:**
```
q_p = 0.613 × (v_map × c_alt × c_dir)² × c_e × c_e,T
```

**Wind Force:**
```
F_w = q_p × c_s × c_d × c_f × A_ref
```

**Overturning Moment:**
```
M = F_w × lever_arm
```

### Terrain Zones

- **Zone A:** Sea/coastal (most exposed)
- **Zone B:** Country/rural (intermediate)
- **Zone C:** Town/urban (most sheltered)

## Project Structure

```
wind-loading-calculator/
├── wind_calculator.py      # Core calculation engine
├── test_wind_calculator.py # Validation test suite
├── api.py                  # Flask REST API
├── report_generator.py     # PDF report generation
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── DEPLOY.md              # Deployment instructions
└── static/
    └── index.html         # Web interface
```

## Development

### Running in Development Mode

```bash
python api.py
```

The server will start with debug mode enabled at `http://localhost:5000`.

### Running Tests

```bash
# Run all tests
python test_wind_calculator.py

# Run with pytest
pytest test_wind_calculator.py -v
```

### Code Style

- Follow PEP 8 guidelines
- Document all functions with docstrings
- Reference P394 page numbers in comments
- Include units in variable names where appropriate

## License

© 2024 North By North East Print & Sign Ltd. All rights reserved.

This software is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

## Support

For technical support or questions:

**Email:** sales@nbnesigns.co.uk  
**Phone:** 01665 606 741  
**Web:** www.northbynortheast.co.uk

## Version History

### v1.0.0 (2024)
- Initial release
- Wall-mounted fascia sign calculations
- Web interface and API
- PDF report generation
- Validated against SCI P394 Sheffield Bioincubator example

## References

1. **BS EN 1991-1-4:2005+A1:2010** - Eurocode 1: Actions on structures - Part 1-4: General actions - Wind actions
2. **SCI Publication P394** - Wind Actions to BS EN 1991-1-4
3. **EN 1990:2002+A1:2005** - Eurocode: Basis of structural design

## Acknowledgments

Calculation methodology based on SCI Publication P394 by:
- Dr. N. S. Trahair
- The Steel Construction Institute

---

**Developed by Toby Fletcher, CEng MIMechE**  
**North By North East Print & Sign Ltd**
