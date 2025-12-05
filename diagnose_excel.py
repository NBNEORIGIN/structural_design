import openpyxl

# Load with formulas
wb = openpyxl.load_workbook('Wind_Loading_Validation_CORRECTED_20251203_1804.xlsx')
ws_calc = wb['Calculations']

print("CALCULATIONS SHEET - Looking for c_f and F_w issues:")
print("="*80)

# Find c_f section
print("\nSearching for c_f (Force Coefficient)...")
for row in range(1, 100):
    cell_value = ws_calc[f'B{row}'].value
    if cell_value and 'Force Coefficient' in str(cell_value):
        print(f"\nFound at row {row}: {cell_value}")
        # Print next 10 rows
        for i in range(row, min(row+10, 100)):
            print(f"Row {i}: B={ws_calc[f'B{i}'].value} | C={ws_calc[f'C{i}'].value} | D={ws_calc[f'D{i}'].value}")
        break

# Find F_w section
print("\n\nSearching for F_w (Wind Force)...")
for row in range(1, 100):
    cell_value = ws_calc[f'B{row}'].value
    if cell_value and 'Wind Force' in str(cell_value):
        print(f"\nFound at row {row}: {cell_value}")
        # Print next 15 rows
        for i in range(row, min(row+15, 100)):
            print(f"Row {i}: B={ws_calc[f'B{i}'].value} | C={ws_calc[f'C{i}'].value} | D={ws_calc[f'D{i}'].value}")
        break

# Check Inputs sheet
print("\n\nINPUTS SHEET:")
print("="*80)
ws_inputs = wb['Inputs']
print(f"C16 (h/d): {ws_inputs['C16'].value}")
print(f"C17 (h/b): {ws_inputs['C17'].value}")
print(f"C15 (A_ref): {ws_inputs['C15'].value}")

# Check what h/d should be
print(f"\nC6 (h): {ws_inputs['C6'].value}")
print(f"C7 (d): {ws_inputs['C7'].value}")
print(f"h/d = {ws_inputs['C6'].value}/{ws_inputs['C7'].value} = {ws_inputs['C6'].value/ws_inputs['C7'].value}")
