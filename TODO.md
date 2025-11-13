# TODO: Implement Separate Units for Fuel Consumption Input and Result Output

## Web App Changes
- [ ] Remove global unit selection from header in index.html
- [ ] Add select for fuel consumption unit next to the input field in index.html
- [ ] Add select for result unit before the "Calculate Fuel" button in index.html
- [ ] Update script.js to handle separate units: real-time conversion for fuel consumption input, result conversion on unit change

## Python App Changes
- [ ] Remove global unit selection from top in fuel_calculator.py
- [ ] Add combobox for fuel consumption unit next to the input
- [ ] Add combobox for result unit before the calculate button
- [ ] Update logic for real-time input conversion and result display conversion

## Testing
- [ ] Test real-time conversions in web app
- [ ] Test real-time conversions in Python app
- [ ] Verify calculations remain accurate in USG internally
- [ ] Ensure UI updates correctly on unit changes
