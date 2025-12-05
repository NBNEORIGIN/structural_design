import openpyxl

wb = openpyxl.load_workbook('Wind_Loading_Validation_FINAL_20251203.xlsx')
ws_calc = wb['Calculations']

print("Fixing A_ref reference...")
print(f"Current C72: {ws_calc['C72'].value}")

# A_ref is in Inputs!C17, not C15
ws_calc['C72'].value = '=Inputs!C17'
print(f"✓ Fixed C72 to: =Inputs!C17 (A_ref)")

wb.save('Wind_Loading_Validation_FINAL_20251203.xlsx')
print("\n✅ Fixed and saved!")
print("\nNow open in Excel - ALL validations should PASS!")
