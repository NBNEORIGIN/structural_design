"""
PDF Report Generator for Wind Loading Calculations
Generates professional PDF reports per BS EN 1991-1-4
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime
import os


class WindLoadingReport:
    """
    Generate professional PDF report for wind loading calculations
    """
    
    def __init__(self, results, inputs, project_info=None):
        """
        Initialize report generator
        
        Args:
            results: Dictionary of calculation results from WindLoadCalculator
            inputs: Dictionary of input parameters
            project_info: Optional dictionary with project details (name, reference, etc.)
        """
        self.results = results
        self.inputs = inputs
        self.project_info = project_info or {}
        
    def generate_pdf(self, filename):
        """
        Create PDF report
        
        Args:
            filename: Output PDF filename
        """
        doc = SimpleDocTemplate(
            filename, 
            pagesize=A4,
            rightMargin=20*mm, 
            leftMargin=20*mm,
            topMargin=20*mm, 
            bottomMargin=20*mm
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=10,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#7f8c8d'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=10,
            spaceBefore=15
        )
        
        # Title Page
        story.append(Spacer(1, 30*mm))
        story.append(Paragraph('Wind Loading Calculation Report', title_style))
        story.append(Paragraph('BS EN 1991-1-4:2005+A1:2010', subtitle_style))
        
        # Project Details
        story.append(Paragraph('Project Details', heading_style))
        
        project_data = [
            ['Project Name:', self.project_info.get('name', 'Signage Installation')],
            ['Project Reference:', self.project_info.get('reference', 'N/A')],
            ['Client:', self.project_info.get('client', 'N/A')],
            ['Date:', datetime.now().strftime('%d %B %Y')],
            ['', ''],
            ['Sign Type:', self._format_sign_type(self.inputs.get('mounting_type', 'wall_mounted_fascia'))],
            ['Sign Dimensions:', f"{self.inputs['sign_width']}m (W) × {self.inputs['sign_height']}m (H) × {self.inputs['sign_depth']}m (D)"],
            ['Installation Height:', f"{self.inputs['building_height']}m above ground level"],
            ['Location:', self.inputs.get('postcode', 'N/A')],
            ['Site Altitude:', f"{self.inputs['site_altitude']}m ASL"],
        ]
        
        project_table = Table(project_data, colWidths=[60*mm, 90*mm])
        project_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ]))
        
        story.append(project_table)
        story.append(Spacer(1, 15*mm))
        
        # Calculation Results
        story.append(Paragraph('Calculation Results', heading_style))
        
        results_data = [
            ['Parameter', 'Value', 'Unit'],
            ['Design Wind Speed', f"{self.results['design_wind_speed']:.1f}", 'm/s'],
            ['Peak Velocity Pressure (q_p)', f"{self.results['q_p']:.0f}", 'Pa'],
            ['Characteristic Wind Force', f"{self.results['force_kN']:.1f}", 'kN'],
            ['Overturning Moment', f"{self.results['moment_kNm']:.1f}", 'kNm'],
        ]
        
        results_table = Table(results_data, colWidths=[80*mm, 40*mm, 30*mm])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e3f2fd')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ]))
        
        story.append(results_table)
        story.append(Spacer(1, 10*mm))
        
        # Calculation Factors
        story.append(Paragraph('Calculation Factors (BS EN 1991-1-4)', heading_style))
        
        factors_data = [
            ['Factor', 'Symbol', 'Value', 'Description'],
            ['Fundamental wind speed', 'v_map', f"{self.results['v_map']:.1f} m/s", 'From UK wind map'],
            ['Altitude factor', 'c_alt', f"{self.results['c_alt']:.3f}", 'Site altitude correction'],
            ['Directional factor', 'c_dir', f"{self.results['c_dir']:.2f}", 'Wind direction'],
            ['Exposure factor', 'c_e', f"{self.results['c_e']:.3f}", f"Zone {self.results['zone']}"],
            ['Town correction', 'c_e,T', f"{self.results['c_e_T']:.3f}", 'Urban terrain'],
            ['Orography factor', 'c_o', f"{self.results['c_o']:.2f}", 'Topography'],
            ['Size factor', 'c_s', f"{self.results['c_s']:.3f}", 'Structure size'],
            ['Dynamic factor', 'c_d', f"{self.results['c_d']:.3f}", 'Dynamic response'],
            ['Force coefficient', 'c_f', f"{self.results['c_f']:.3f}", 'Shape factor'],
        ]
        
        factors_table = Table(factors_data, colWidths=[45*mm, 25*mm, 30*mm, 50*mm])
        factors_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (1, 1), (1, -1), 'Courier'),
        ]))
        
        story.append(factors_table)
        story.append(Spacer(1, 10*mm))
        
        # Warnings
        if self.results.get('warnings'):
            story.append(Paragraph('Calculation Warnings', heading_style))
            
            warning_text = '<br/>'.join([f"• {w}" for w in self.results['warnings']])
            warning_para = Paragraph(
                f'<font color="#856404">{warning_text}</font>',
                styles['Normal']
            )
            story.append(warning_para)
            story.append(Spacer(1, 10*mm))
        
        # Important Notes
        story.append(Paragraph('Important Notes', heading_style))
        
        notes_text = """
        <b>1. Characteristic Values:</b> These are characteristic (unfactored) wind loading values.<br/>
        <br/>
        <b>2. Partial Factors:</b> For ultimate limit state design, apply partial factors per EN 1990:
        <br/>• Permanent actions: γ_G = 1.35 (unfavourable) or 1.0 (favourable)
        <br/>• Variable actions: γ_Q = 1.5 (wind loading)
        <br/>
        <b>3. Limitations:</b> This calculation is indicative and does not account for:
        <br/>• Orographic effects (hills, cliffs, escarpments)
        <br/>• Complex building geometries or local sheltering
        <br/>• Dynamic effects for flexible structures
        <br/>• Fatigue considerations
        <br/>
        <b>4. Structural Design:</b> Foundation design, fixings, and connections must be verified 
        by a qualified structural engineer. This calculation provides wind loading only.
        <br/>
        <b>5. Building Control:</b> For building control submission, a full certified structural 
        calculation may be required depending on local authority requirements.
        """
        
        story.append(Paragraph(notes_text, styles['Normal']))
        story.append(Spacer(1, 10*mm))
        
        # Methodology
        story.append(Paragraph('Calculation Methodology', heading_style))
        
        methodology_text = f"""
        <b>Standard:</b> {self.results['methodology']}<br/>
        <b>Reference:</b> {self.results['reference']}<br/>
        <b>Calculator Version:</b> {self.results['version']}<br/>
        <br/>
        This calculation follows the simplified procedure for wind actions on buildings 
        as documented in SCI Publication P394 "Wind Actions to BS EN 1991-1-4".
        """
        
        story.append(Paragraph(methodology_text, styles['Normal']))
        story.append(Spacer(1, 15*mm))
        
        # Certification
        cert_text = f"""
        <b>Prepared by:</b><br/>
        Toby Fletcher, CEng MIMechE<br/>
        North By North East Print & Sign Ltd<br/>
        <br/>
        <b>Date:</b> {datetime.now().strftime('%d %B %Y')}<br/>
        <br/>
        <i>This report is provided for indicative purposes. For certified structural calculations 
        suitable for building control submission, please contact us directly.</i>
        """
        
        story.append(Paragraph(cert_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        return filename
    
    def _format_sign_type(self, sign_type):
        """Format sign type for display"""
        type_map = {
            'wall_mounted_fascia': 'Wall-Mounted Fascia Sign',
            'projecting_sign': 'Projecting Sign',
            'post_mounted': 'Post-Mounted Sign'
        }
        return type_map.get(sign_type, sign_type)


def generate_report(results, inputs, output_filename, project_info=None):
    """
    Convenience function to generate PDF report
    
    Args:
        results: Calculation results dictionary
        inputs: Input parameters dictionary
        output_filename: Output PDF filename
        project_info: Optional project information dictionary
    
    Returns:
        Path to generated PDF file
    """
    report = WindLoadingReport(results, inputs, project_info)
    return report.generate_pdf(output_filename)


if __name__ == '__main__':
    # Example usage
    from wind_calculator import WindLoadCalculator
    
    calculator = WindLoadCalculator()
    
    # Example inputs
    inputs = {
        'sign_width': 5.0,
        'sign_height': 2.0,
        'sign_depth': 0.4,
        'building_height': 8.0,
        'site_altitude': 50,
        'postcode': 'NE66 2NT',
        'distance_to_shore': 5,
        'terrain_type': 'country',
        'distance_into_town': 0,
        'mounting_type': 'wall_mounted_fascia'
    }
    
    # Calculate
    results = calculator.calculate_wind_loading(inputs)
    
    # Generate report
    project_info = {
        'name': 'Example Signage Installation',
        'reference': 'PROJ-2024-001',
        'client': 'Example Client Ltd'
    }
    
    output_file = 'wind_loading_report_example.pdf'
    generate_report(results, inputs, output_file, project_info)
    
    print(f"Report generated: {output_file}")
