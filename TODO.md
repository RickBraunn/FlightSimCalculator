# Aircraft Preset System Implementation TODO

## Approved Plan Summary
- Plan B: Allow edits after autofill
- Add summary display
- Only web version (no Python)

## Steps (Sequential)

- [x] **Step 1**: Edit index.html - Add aircraft dropdown + summary div (before cruise-speed input)
- [x] **Step 1**: Edit index.html - Add aircraft dropdown + summary div (before cruise-speed input)
- [x] **Step 2**: Edit src/styles.css - Add .aircraft-summary style  
- [x] **Step 3**: Edit script/script.js - Add loadAircraftProfiles(), populateAircraftDropdown(), onAircraftChange(), modify calculateFuel() with preset overrides
- [ ] **Step 4**: Test integration - Manual calc, preset select, unit changes, modes (FAA/Custom)
- [ ] **Step 5**: Handle edge cases - JSON fail fallback
- [x] **Complete**: attempt_completion with demo command (after testing)

**Current Progress**: Steps 1-3 complete. Testing next (open index.html to verify).
