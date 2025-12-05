# Quick Start Guide

## Get Started in 5 Minutes

### 1. Install Dependencies

```bash
cd "g:\My Drive\003 APPS\018 Structural Design\wind-loading-calculator"
pip install -r requirements.txt
```

### 2. Run Tests (Optional but Recommended)

```bash
python test_wind_calculator.py
```

You should see:
```
✓ Sheffield Bioincubator validation PASSED
ALL TESTS PASSED ✓
```

### 3. Start the Web Application

```bash
python api.py
```

You should see:
```
BS EN 1991-1-4 Wind Loading Calculator API
============================================================
Version: 1.0.0
Standard: BS EN 1991-1-4:2005+A1:2010
Reference: SCI Publication P394
============================================================
Starting Flask server...
API will be available at: http://localhost:5000
```

### 4. Open Your Browser

Navigate to: **http://localhost:5000**

### 5. Calculate Wind Loading

Fill in the form with your sign details:

**Example: Small Shop Fascia Sign**
- Sign Type: Wall-Mounted Fascia
- Width: 4.0 m
- Height: 1.5 m
- Depth: 0.3 m
- Height to top of sign: 5.0 m
- Postcode: NE66 2NT
- Altitude: 10 m
- Distance to shoreline: 5 km
- Terrain: Country

Click **"Calculate Wind Loading"**

### 6. Review Results

You'll see:
- Design Wind Speed (m/s)
- Peak Velocity Pressure (Pa)
- Design Wind Force (kN)
- Overturning Moment (kNm)
- All calculation factors

### 7. Generate PDF Report (Optional)

```python
from wind_calculator import WindLoadCalculator
from report_generator import generate_report

calculator = WindLoadCalculator()

inputs = {
    'sign_width': 4.0,
    'sign_height': 1.5,
    'sign_depth': 0.3,
    'building_height': 5.0,
    'site_altitude': 10,
    'postcode': 'NE66 2NT',
    'distance_to_shore': 5,
    'terrain_type': 'country',
    'distance_into_town': 0,
    'mounting_type': 'wall_mounted_fascia'
}

results = calculator.calculate_wind_loading(inputs)

project_info = {
    'name': 'Shop Fascia Sign',
    'reference': 'PROJ-001',
    'client': 'ABC Retail Ltd'
}

generate_report(results, inputs, 'wind_report.pdf', project_info)
print("PDF report generated: wind_report.pdf")
```

## Common Use Cases

### Case 1: High Street Shop Sign
```python
inputs = {
    'sign_width': 5.0,      # 5m wide
    'sign_height': 1.8,     # 1.8m high
    'sign_depth': 0.35,     # 0.35m projection
    'building_height': 6.0, # 6m above ground
    'site_altitude': 20,
    'postcode': 'B1 1AA',   # Birmingham
    'distance_to_shore': 100,
    'terrain_type': 'town',
    'distance_into_town': 3,
    'mounting_type': 'wall_mounted_fascia'
}
```

### Case 2: Coastal Retail Park
```python
inputs = {
    'sign_width': 8.0,      # 8m wide
    'sign_height': 3.0,     # 3m high
    'sign_depth': 0.5,      # 0.5m projection
    'building_height': 12.0,# 12m above ground
    'site_altitude': 5,
    'postcode': 'BN1 1AA',  # Brighton (coastal)
    'distance_to_shore': 1,
    'terrain_type': 'country',
    'distance_into_town': 0,
    'mounting_type': 'wall_mounted_fascia'
}
```

### Case 3: Industrial Unit Sign
```python
inputs = {
    'sign_width': 10.0,     # 10m wide
    'sign_height': 4.0,     # 4m high
    'sign_depth': 0.6,      # 0.6m projection
    'building_height': 15.0,# 15m above ground
    'site_altitude': 100,
    'postcode': 'S10 1AA',  # Sheffield
    'distance_to_shore': 100,
    'terrain_type': 'town',
    'distance_into_town': 2,
    'mounting_type': 'wall_mounted_fascia'
}
```

## Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Then restart
python api.py
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### Calculation Seems Wrong
1. Check all inputs are in correct units (meters, not mm)
2. Verify postcode is valid UK format
3. Check altitude is above sea level (not negative)
4. Run validation tests: `python test_wind_calculator.py`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Review [DEPLOY.md](DEPLOY.md) for production deployment
- Check calculation methodology in `wind_calculator.py`
- Explore API endpoints in `api.py`

## Support

**Email:** sales@nbnesigns.co.uk  
**Phone:** 01665 606 741

## Important Notes

⚠️ **This calculator provides indicative values only**

For building control submission or complex installations:
- Contact us for full certified calculations
- £350, 48-hour turnaround
- Includes foundation design verification
- Building control submission package

---

**Happy Calculating! 🎯**
