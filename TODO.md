# Endurance Calculation Implementation TODO

## Approved Plan Summary
Add two endurance lines to fuel results output in script/script.js:
- Autonomia na decolagem (takeoff fuel / cruise GPH → HH:MM)
- Autonomia no pouso (landing fuel / cruise GPH → HH:MM)
Using totalFuelRequiredUSG, totalTripFuel, fuelConsumption (USG/hr).

## Steps (Sequential)

- [ ] **Step 1**: Add formatEndurance helper function and endurance calcs in calculateFuel(), update result.innerText with 4 lines.
- [ ] **Step 2**: Update updateResultDisplay() to include endurance lines (store/add lastTotalTripFuelUSG).
- [ ] **Step 3**: Test: Open index.html, input values/preset, calculate → verify output.
- [ ] **Step 4**: attempt_completion.

**Current Progress**: Complete - endurance features implemented and tested.

