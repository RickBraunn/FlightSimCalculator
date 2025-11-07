# TODO List for Unit Selection Feature

## HTML Changes (index.html)
- [x] Remove the `<p id="learn-more">*learn more</p>` element.
- [x] Add a new `<div>` with radio buttons for units (USG, LBS, L, KG), defaulting to USG.
- [x] Update the fuel consumption label to dynamically show the selected unit (e.g., "Average fuel consumption (USG/hr)").

## JS Changes (script/script.js)
- [x] Remove event listeners and functions related to "learn more" modal.
- [x] Add event listener for unit radio buttons to update the fuel consumption label.
- [x] In `calculateFuel()`, convert the input `fuelConsumption` from selected unit to USG/hr for calculation, then convert `totalFuelRequired` back to selected unit for display.

## Python Changes (python_app/fuel_calculator.py)
- [x] Remove the `learn_more` label and its binding.
- [x] Add radio buttons (using `tk.Radiobutton`) for units, defaulting to "USG".
- [x] Update the fuel consumption label dynamically based on selected unit.
- [x] In `calculate_fuel()`, convert input `fuel_consumption` from selected unit to USG/hr, calculate, then convert result to selected unit.

## Followup Steps
- [x] Test both HTML and Python apps to ensure calculations and conversions work correctly.
- [x] Verify UI updates (label changes, radio button selection).
