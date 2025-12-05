import openpyxl

# Load the workbook
wb = openpyxl.load_workbook('Wind_Loading_Validation_CORRECTED_20251203_1804.xlsx')

print("Fixing Calculations sheet references...")

# Fix Calculations sheet
ws_calc = wb['Calculations']

# Fix c_f: Row 62 should reference Inputs!C18 (h/d is in row 18, not C16)
print(f"Current C62: {ws_calc['C62'].value}")
ws_calc['C62'].value = '=Inputs!C18'
ws_calc['C62'].number_format = '0.000'
print(f"✓ Fixed C62 to: =Inputs!C18 (h/d)")

# Fix F_w: Row 74 formula
print(f"\nCurrent C74: {ws_calc['C74'].value}")
ws_calc['C74'].value = '=C68*C69*C70*C71*C72/1000'
ws_calc['C74'].number_format = '0.0'
print(f"✓ Fixed C74 to: =C68*C69*C70*C71*C72/1000")

# Also need to check what C68-C72 reference
print("\nChecking C68-C72 references:")
for row in range(68, 73):
    print(f"C{row}: {ws_calc[f'C{row}'].value}")

# Save
filename = 'Wind_Loading_Validation_FINAL_20251203.xlsx'
wb.save(filename)
print(f"\n✅ Saved to: {filename}")
print("\nOpen in Excel and check if validations pass!")
