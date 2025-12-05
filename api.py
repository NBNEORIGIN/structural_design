"""
Flask API for BS EN 1991-1-4 Wind Loading Calculator
Provides REST endpoints for the web interface
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import re
from wind_calculator import WindLoadCalculator
from projecting_sign_calculator import ProjectingSignCalculator
from post_mounted_calculator import PostMountedCalculator

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Initialize calculators
wall_calculator = WindLoadCalculator()
projecting_calculator = ProjectingSignCalculator()
post_calculator = PostMountedCalculator()


@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')


@app.route('/api/calculate-wind-loading', methods=['POST'])
def calculate_wind_loading():
    """
    API endpoint for wind loading calculations
    
    Request body:
    {
        "sign_width": float,
        "sign_height": float,
        "sign_depth": float,
        "building_height": float,
        "postcode": string,
        "altitude": float,
        "distance_to_shore": string/float,
        "terrain_type": string,
        "distance_into_town": float,
        "sign_type": string
    }
    
    Response:
    {
        "design_wind_speed": float,
        "peak_pressure": float,
        "wind_force": float,
        "overturning_moment": float,
        "calculation_summary": {...},
        "warnings": [...],
        "methodology": string,
        "reference": string
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'sign_width', 'sign_height', 'sign_depth',
            'building_height', 'altitude'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Validate numeric ranges
        if data['sign_width'] <= 0 or data['sign_width'] > 50:
            return jsonify({'error': 'Sign width must be between 0 and 50 meters'}), 400
        
        if data['sign_height'] <= 0 or data['sign_height'] > 30:
            return jsonify({'error': 'Sign height must be between 0 and 30 meters'}), 400
        
        if data['sign_depth'] <= 0 or data['sign_depth'] > 10:
            return jsonify({'error': 'Sign depth must be between 0 and 10 meters'}), 400
        
        if data['building_height'] < 2 or data['building_height'] > 200:
            return jsonify({'error': 'Building height must be between 2 and 200 meters'}), 400
        
        if data['altitude'] < 0 or data['altitude'] > 2000:
            return jsonify({'error': 'Altitude must be between 0 and 2000 meters'}), 400
        
        # Get sign type
        sign_type = data.get('sign_type', 'wall_mounted')
        
        # Route to appropriate calculator
        if sign_type == 'projecting':
            calc_inputs = {
                'sign_width': float(data['sign_width']),
                'sign_height': float(data['sign_height']),
                'projection': float(data.get('projection', 0.5)),
                'mounting_height': float(data.get('mounting_height', data['building_height'])),
                'terrain_category': data.get('terrain_category', 'III'),
                'v_b_0': float(data.get('v_map', 22.5)),
                'sign_weight': float(data.get('sign_weight', 0.15)),
                'n_brackets': int(data.get('n_brackets', 2)),
                'bracket_spacing': float(data.get('bracket_spacing', 1.0)),
                'n_fixings_per_bracket': int(data.get('n_fixings_per_bracket', 4)),
                'fixing_pitch_vertical': float(data.get('fixing_pitch_vertical', 0.15)),
                'anchor_tension_capacity': float(data.get('anchor_tension_capacity', 12.0)),
                'anchor_shear_capacity': float(data.get('anchor_shear_capacity', 8.0)),
                'anchor_gamma_M': float(data.get('anchor_gamma_M', 1.5)),
                'bracket_width': float(data.get('bracket_width', 80)),
                'bracket_depth': float(data.get('bracket_depth', 60)),
                'bracket_thickness': float(data.get('bracket_thickness', 5)),
                'bracket_steel_grade': float(data.get('bracket_steel_grade', 275))
            }
            results = projecting_calculator.calculate_wind_loading(calc_inputs)
            
        elif sign_type == 'post_mounted':
            calc_inputs = {
                'sign_width': float(data['sign_width']),
                'sign_height': float(data['sign_height']),
                'sign_depth': float(data['sign_depth']),
                'sign_base_height': float(data.get('sign_base_height', 2.0)),
                'post_height': float(data.get('post_height', data['building_height'])),
                'site_altitude': float(data['altitude']),
                'v_map': float(data.get('v_map', 22.5)),
                'distance_to_shore': data.get('distance_to_shore', 100),
                'terrain_type': data.get('terrain_type', 'country'),
                'distance_into_town': float(data.get('distance_into_town', 0)),
                'post_diameter': float(data.get('post_diameter', 150)),
                'post_thickness': float(data.get('post_thickness', 8)),
                'post_section_type': data.get('post_section_type', 'circular'),
                'post_material': data.get('post_material', 'steel'),
                'post_steel_grade': float(data.get('post_steel_grade', 275)),
                'foundation_type': data.get('foundation_type', 'concrete'),
                'embedment_depth': float(data.get('embedment_depth', 1.5))
            }
            results = post_calculator.calculate_wind_loading(calc_inputs)
            
        else:  # wall_mounted (default)
            calc_inputs = {
                'sign_width': float(data['sign_width']),
                'sign_height': float(data['sign_height']),
                'sign_depth': float(data['sign_depth']),
                'building_height': float(data['building_height']),
                'site_altitude': float(data['altitude']),
                'postcode': data.get('postcode', ''),
                'distance_to_shore': data.get('distance_to_shore', 100),
                'terrain_type': data.get('terrain_type', 'country'),
                'distance_into_town': float(data.get('distance_into_town', 0)),
                'mounting_type': 'wall_mounted_fascia'
            }
            results = wall_calculator.calculate_wind_loading(calc_inputs)
        
        # Format response based on sign type
        response = {
            'sign_type': sign_type,
            'peak_pressure': round(results['q_p'], 1),
            'wind_force': round(results.get('force_kN', results.get('F_w_k', 0)), 2),
            'warnings': results.get('warnings', []),
            'methodology': results.get('methodology', 'BS EN 1991-1-4'),
            'version': results.get('version', '1.0.0')
        }
        
        # Add sign-type specific fields
        if sign_type == 'projecting':
            response.update({
                'design_wind_force': round(results.get('F_w_Ed', 0), 2),
                'bracket_forces': results.get('bracket_forces', {}),
                'anchor_check': results.get('anchor_check', {}),
                'bracket_check': results.get('bracket_check', {}),
                'deflection_check': results.get('deflection_check', {}),
                'overall_status': results.get('overall_status', 'UNKNOWN'),
                'reference': results.get('methodology', 'EN 1991-1-4')
            })
        elif sign_type == 'post_mounted':
            response.update({
                'design_wind_speed': round(results.get('design_wind_speed', 0), 2),
                'overturning_moment': round(results.get('moment_kNm', 0), 2),
                'post_check': results.get('post_check', {}),
                'foundation_check': results.get('foundation_check', {}),
                'overall_status': results.get('overall_status', 'UNKNOWN'),
                'calculation_summary': {
                    'v_map': round(results.get('v_map', 0), 1),
                    'c_alt': round(results.get('c_alt', 1), 3),
                    'c_f': round(results.get('c_f', 1), 3),
                    'A_ref': round(results.get('A_ref', 0), 2)
                },
                'reference': results.get('reference', 'P394')
            })
        else:  # wall_mounted
            response.update({
                'design_wind_speed': round(results['design_wind_speed'], 2),
                'overturning_moment': round(results['moment_kNm'], 2),
                'calculation_summary': {
                    'v_map': round(results['v_map'], 1),
                    'c_alt': round(results['c_alt'], 3),
                    'c_dir': round(results['c_dir'], 2),
                    'c_e': round(results['c_e'], 3),
                    'c_e_T': round(results['c_e_T'], 3),
                    'c_o': round(results['c_o'], 2),
                    'c_s': round(results['c_s'], 3),
                    'c_d': round(results['c_d'], 3),
                    'c_f': round(results['c_f'], 3),
                    'zone': results['zone'],
                    'A_ref': round(results['A_ref'], 2)
                },
                'assessment': results.get('assessment', {}),
                'reference': results['reference']
            })
        
        return jsonify(response), 200
        
    except ValueError as e:
        return jsonify({
            'error': f'Invalid input: {str(e)}'
        }), 400
    except KeyError as e:
        return jsonify({
            'error': f'Missing field: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'error': f'Calculation error: {str(e)}'
        }), 500


@app.route('/api/validate-postcode', methods=['POST'])
def validate_postcode():
    """
    Validate UK postcode and return estimated wind speed
    
    Request body:
    {
        "postcode": string
    }
    
    Response:
    {
        "valid": boolean,
        "v_map": float,
        "area": string,
        "note": string
    }
    """
    try:
        data = request.get_json()
        postcode = data.get('postcode', '').strip()
        
        if not postcode:
            return jsonify({
                'valid': False,
                'error': 'Postcode is required'
            }), 400
        
        # UK postcode validation pattern
        postcode_pattern = r'^[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}$'
        
        if not re.match(postcode_pattern, postcode.upper()):
            return jsonify({
                'valid': False,
                'error': 'Invalid UK postcode format'
            }), 400
        
        # Lookup wind speed
        v_map = wall_calculator.lookup_wind_speed(postcode)
        
        # Extract area
        area = ''.join([c for c in postcode.upper()[:2] if c.isalpha()])
        
        return jsonify({
            'valid': True,
            'v_map': round(v_map, 1),
            'area': area,
            'note': 'Wind speed is approximate based on regional data from BS EN 1991-1-4 wind map'
        }), 200
        
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': wall_calculator.VERSION,
        'standard': wall_calculator.STANDARD,
        'service': 'Wind Loading Calculator API'
    }), 200


@app.route('/api/info', methods=['GET'])
def info():
    """Return API information"""
    return jsonify({
        'name': 'BS EN 1991-1-4 Wind Loading Calculator',
        'version': wall_calculator.VERSION,
        'standard': wall_calculator.STANDARD,
        'reference': 'SCI Publication P394 + EN 1991-1-4',
        'developer': 'Toby Fletcher, CEng MIMechE',
        'company': 'North By North East Print & Sign Ltd',
        'supported_sign_types': [
            'wall_mounted',
            'projecting',
            'post_mounted'
        ],
        'limitations': [
            'Orography not considered',
            'Non-directional approach (conservative)',
            'Simplified terrain classification',
            'Not suitable for complex geometries'
        ]
    }), 200


if __name__ == '__main__':
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    print("="*60)
    print("BS EN 1991-1-4 Wind Loading Calculator API")
    print("="*60)
    print(f"Version: {wall_calculator.VERSION}")
    print(f"Standard: {wall_calculator.STANDARD}")
    print(f"Reference: SCI Publication P394 + EN 1991-1-4")
    print(f"Supported Sign Types: Wall-Mounted, Projecting, Post-Mounted")
    print("="*60)
    print("Starting Flask server...")
    print("API will be available at: http://localhost:5000")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
