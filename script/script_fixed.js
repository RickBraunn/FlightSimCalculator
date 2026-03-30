// Aircraft Profiles System
let aircraftProfiles = null;

// Safe Modal System
function safeShowModal(message) {
    const modal = document.getElementById('custom-alert');
    const messageEl = document.getElementById('alert-message');
    const closeBtn = document.querySelector('.close-btn');
    const okBtn = document.getElementById('ok-btn');

    if (!modal || !messageEl || !closeBtn || !okBtn) {
        console.warn('Modal elements not found. Skipping modal.');
        return;
    }

    messageEl.textContent = message;
    modal.style.display = 'block';

    const closeModal = () => {
        modal.style.display = 'none';
    };

    closeBtn.onclick = closeModal;
    okBtn.onclick = closeModal;
}
let selectedAircraft = 'Custom';
let lastCalculatedFuelUSG = 0;
let lastTotalTripFuelUSG = 0;
let lastFuelConsumptionUSG = 0;
let lastCalculatedTimeHours = 0;
let lastCalculatedTimeMinutes = 0;

document.addEventListener('DOMContentLoaded', () => {
    // Safe non-blocking modal with localStorage
    setTimeout(() => {
        try {
            if (!localStorage.getItem('modalShown')) {
                safeShowModal('Disclaimer: This fuel calculator is designed exclusively for flight simulation purposes. It is not intended for actual flight planning or navigation. Please consult official resources and professionals for real-world flight operations.');
                localStorage.setItem('modalShown', 'true');
            }
        } catch (e) {
            console.warn('Modal error:', e);
        }
    }, 100);
    
    loadAircraftProfiles(); // Always runs first, unblocked
});

// Load aircraft profiles from JSON
const loadAircraftProfiles = async () => {
    try {
        const response = await fetch('data/aircraftProfiles.json');
        if (!response.ok) throw new Error('JSON load failed');
        aircraftProfiles = await response.json();
        populateAircraftDropdown();
    } catch (error) {
        console.warn('Aircraft profiles failed to load:', error);
        document.getElementById('aircraft-summary').textContent = 'Aircraft presets unavailable - using manual input';
    }
};

// Populate dropdown with aircraft options
const populateAircraftDropdown = () => {
    const select = document.getElementById('aircraft-select');
    select.innerHTML = '<option value="Custom">Custom (Manual Input)</option>';
    if (aircraftProfiles) {
        Object.keys(aircraftProfiles).forEach(name => {
            const option = document.createElement('option');
            option.value = name;
            option.textContent = name;
            select.appendChild(option);
        });
    }
    select.addEventListener('change', onAircraftChange);
};

// Handle aircraft selection change
const onAircraftChange = () => {
    const aircraftName = document.getElementById('aircraft-select').value;
    selectedAircraft = aircraftName;
    const summaryDiv = document.getElementById('aircraft-summary');
    
    if (aircraftName === 'Custom' || !aircraftProfiles || !aircraftProfiles[aircraftName]) {
        summaryDiv.textContent = '';
        // Enable manual editing (already enabled)
        return;
    }
    
    const profile = aircraftProfiles[aircraftName];
    
    // Auto-fill fields (allow overrides)
    document.getElementById('cruise-speed').value = profile.cruiseSpeed;
    document.getElementById('fuel-consumption').value = profile.fuelBurn;
    document.getElementById('fuel-consumption-unit').value = 'USG'; // GPH = USG/hr
    document.getElementById('fuel-consumption-label').textContent = `Average fuel consumption (${profile.fuelUnit}/hr)`; 
    document.getElementById('taxi-time').value = 0; // Use taxiFuel directly
    
    // Update summary display
    summaryDiv.innerHTML = `
        <strong>${aircraftName}</strong><br>
        Cruise: ${profile.cruiseSpeed} kts | Fuel: ${profile.fuelBurn} ${profile.fuelUnit}/hr | 
        Taxi: ${profile.taxiFuel} USG | Reserve: ${profile.reserveMinutes} min
    `;
};

// Unit selection for fuel consumption
const fuelConsumptionUnitSelect = document.getElementById('fuel-consumption-unit');
const fuelConsumptionLabel = document.getElementById('fuel-consumption-label');
const fuelConsumptionInput = document.getElementById('fuel-consumption');
let previousFuelConsumptionUnit = 'USG'; // Track previous unit for conversion

// Function to update fuel consumption label based on selected unit
const updateFuelConsumptionLabel = () => {
    const selectedUnit = fuelConsumptionUnitSelect.value;
    fuelConsumptionLabel.textContent = `Average fuel consumption (${selectedUnit}/hr)`;
};

// Function to convert fuel consumption value in real-time
const convertFuelConsumption = () => {
    const currentValue = parseFloat(fuelConsumptionInput.value);
    if (isNaN(currentValue)) return;

    // Convert from previous unit to USG
    let valueInUSG = currentValue;
    if (previousFuelConsumptionUnit === 'LBS') {
        valueInUSG = currentValue / 6.7;
    } else if (previousFuelConsumptionUnit === 'L') {
        valueInUSG = currentValue / 3.785;
    } else if (previousFuelConsumptionUnit === 'KG') {
        valueInUSG = currentValue / 3.04;
    }
    // Now convert to new unit
    const newUnit = fuelConsumptionUnitSelect.value;
    let newValue = valueInUSG;
    if (newUnit === 'LBS') {
        newValue = valueInUSG * 6.7;
    } else if (newUnit === 'L') {
        newValue = valueInUSG * 3.785;
    } else if (newUnit === 'KG') {
        newValue = valueInUSG * 3.04;
    }
    fuelConsumptionInput.value = newValue.toFixed(2);
    previousFuelConsumptionUnit = newUnit; // Update previous unit
};

// Event listener for fuel consumption unit change
fuelConsumptionUnitSelect.addEventListener('change', () => {
    convertFuelConsumption();
    updateFuelConsumptionLabel();
});

// Initialize label on load
updateFuelConsumptionLabel();

const formatEndurance = (totalHours) => {
    const hours = Math.floor(totalHours);
    const minutes = Math.round((totalHours - hours) * 60);
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
};

const calculateFuel = () => {
    // Get input values and parse as floats
    const distanceAB = parseFloat(document.getElementById('distance-ab').value);
    const distanceBC = parseFloat(document.getElementById('distance-bc').value);
    const headwind = parseFloat(document.getElementById('headwind').value);
    const fuelMode = document.getElementById('fuel-mode').value;
    const fuelConsumptionUnit = document.getElementById('fuel-consumption-unit').value;
    const resultUnit = document.getElementById('result-unit').value;

    // Aircraft preset overrides (Plan B: input values take precedence if edited)
    let cruiseSpeed = parseFloat(document.getElementById('cruise-speed').value);
    let fuelConsumptionInput = parseFloat(document.getElementById('fuel-consumption').value);
    let taxiTime = parseFloat(document.getElementById('taxi-time').value);
    
    let taxiFuelOverride = 0;
    let reserveMinutesOverride = 45;
    
    if (selectedAircraft !== 'Custom' && aircraftProfiles && aircraftProfiles[selectedAircraft]) {
        const profile = aircraftProfiles[selectedAircraft];
        // Use input if edited, else preset
        cruiseSpeed = isNaN(cruiseSpeed) ? profile.cruiseSpeed : cruiseSpeed;
        fuelConsumptionInput = isNaN(fuelConsumptionInput) ? profile.fuelBurn : fuelConsumptionInput;
        taxiTime = isNaN(taxiTime) || taxiTime === 0 ? 0 : taxiTime; // Prefer preset taxiFuel if time=0
        taxiFuelOverride = profile.taxiFuel;
        reserveMinutesOverride = profile.reserveMinutes;
    }

    // For custom mode, get contingency and reserve inputs (override with preset if applicable)
    let contingencyPercent = 5;
    let reserveMinutes = reserveMinutesOverride;
    if (fuelMode === 'custom') {
        contingencyPercent = parseFloat(document.getElementById('contingency').value) || 5;
        reserveMinutes = parseFloat(document.getElementById('reserve-minutes').value) || reserveMinutesOverride;
    }

    // Validate inputs (relaxed for auto-filled)
    if (
        isNaN(distanceAB) || distanceAB < 0 ||
        isNaN(distanceBC) || distanceBC < 0 ||
        isNaN(cruiseSpeed) || cruiseSpeed <= 0 ||
        isNaN(fuelConsumptionInput) || fuelConsumptionInput <= 0 ||
        isNaN(headwind) || headwind < 0
    ) {
        document.getElementById('result').innerText = 'Please enter valid positive numbers for required inputs.';
        return;
    }

    // Convert fuel consumption to USG/hr for calculation
    let fuelConsumption = fuelConsumptionInput;
    if (fuelConsumptionUnit === 'LBS') {
        fuelConsumption = fuelConsumptionInput / 6.7; // LBS to USG
    } else if (fuelConsumptionUnit === 'L') {
        fuelConsumption = fuelConsumptionInput / 3.785; // L to USG
    } else if (fuelConsumptionUnit === 'KG') {
        fuelConsumption = fuelConsumptionInput / 3.04; // KG to USG
    }
    // USG remains as is
    lastFuelConsumptionUSG = fuelConsumption;

    // Calculate effective speed
    const speed = cruiseSpeed - headwind;
    if (speed <= 0) {
        document.getElementById('result').innerText = 'Effective speed must be greater than zero. Please check cruise speed and headwind values.';
        return;
    }

    // Helper function to calculate fuel for a leg with buffer
    const calculateLegFuel = (distance, speed, consumption, bufferPercent) => {
        const time = distance / speed;
        const fuel = time * consumption;
        return fuel * (1 + bufferPercent / 100);
    };

    let totalTripFuel = 0;
    let reserveFuel = 0;

    if (fuelMode === 'custom') {
        // Use user inputs for contingency and reserve
        const totalFuelAB = calculateLegFuel(distanceAB, speed, fuelConsumption, contingencyPercent);
        const totalFuelBC = calculateLegFuel(distanceBC, speed, fuelConsumption, contingencyPercent);
        totalTripFuel = totalFuelAB + totalTripFuelBC;
        reserveFuel = (reserveMinutes / 60) * fuelConsumption;
    } else if (fuelMode === 'faa') {
        // FAA mode: Use FAA fuel requirements based on flight type
        const flightType = document.getElementById('flight-type').value;

        if (flightType === 'IFR') {
            // IFR: Fuel for trip + fuel to alternate + 45 minutes reserve
            // For demonstration, assume alternate fuel equals 10% of trip fuel
            const tripFuelAB = calculateLegFuel(distanceAB, speed, fuelConsumption, 0);
            const tripFuelBC = calculateLegFuel(distanceBC, speed, fuelConsumption, 0);
            const tripFuel = tripFuelAB + tripFuelBC;
            const alternateFuel = tripFuel * 0.10;
            const reserve = (45 / 60) * fuelConsumption;
            totalTripFuel = tripFuel + alternateFuel;
            reserveFuel = reserve;
        } else if (flightType === 'VFR') {
            // VFR: Fuel for trip + 30 minutes reserve
            const tripFuelAB = calculateLegFuel(distanceAB, speed, fuelConsumption, 0);
            totalTripFuel = tripFuelAB + calculateLegFuel(distanceBC, speed, fuelConsumption, 0);
            reserveFuel = (30 / 60) * fuelConsumption;
        } else {
            // Default fallback
            const totalFuelAB = calculateLegFuel(distanceAB, speed, fuelConsumption, 10);
            const totalFuelBC = calculateLegFuel(distanceBC, speed, fuelConsumption, 10);
            totalTripFuel = totalFuelAB + totalFuelBC;
            reserveFuel = (45 / 60) * fuelConsumption;
        }
    }

    // Taxi fuel: preset override if applicable, else time-based
    let taxiFuel = taxiFuelOverride || (taxiTime / 60) * fuelConsumption;
    let totalFuelRequiredUSG = totalTripFuel + reserveFuel + taxiFuel;
    lastCalculatedFuelUSG = totalFuelRequiredUSG; // Store for result unit changes
    lastTotalTripFuelUSG = totalTripFuel;

    // Endurance calculations
    const enduranceTakeoffHours = totalFuelRequiredUSG / fuelConsumption;
    const enduranceLandingHours = (totalFuelRequiredUSG - totalTripFuel) / fuelConsumption;
    const enduranceTakeoff = formatEndurance(enduranceTakeoffHours);
    const enduranceLanding = formatEndurance(enduranceLandingHours);

    // Calculate estimated time A to B
    const timeHours = distanceAB / speed;
    const hours = Math.floor(timeHours);
    const minutes = Math.round((timeHours - hours) * 60);
    lastCalculatedTimeHours = hours; // Store for result unit changes
    lastCalculatedTimeMinutes = minutes; // Store for result unit changes

    // Convert total fuel back to selected result unit for display
    let totalFuelRequired = totalFuelRequiredUSG;
    let unitName = 'gallons';
    if (resultUnit === 'LBS') {
        totalFuelRequired *= 6.7; // USG to LBS
        unitName = 'lbs';
    } else if (resultUnit === 'L') {
        totalFuelRequired *= 3.785; // USG to L
        unitName = 'liters';
    } else if (resultUnit === 'KG') {
        totalFuelRequired *= 3.04; // USG to KG
        unitName = 'kg';
    }
    // USG remains as gallons

    document.getElementById('result').innerText = `Total Fuel Required: ${totalFuelRequired.toFixed(2)} ${unitName}\nEstimated Time A to B: ${hours} hours ${minutes} minutes\nEndurance at takeoff: ${enduranceTakeoff}\nEndurance at landing: ${enduranceLanding}`;
};

const fuelCalculatorForm = document.getElementById('fuel-calculator');

const fuelModeSelect = document.getElementById('fuel-mode');
const customInputsDiv = document.getElementById('custom-inputs');
const flightTypeDiv = document.getElementById('flight-type-div');

const toggleInputs = () => {
    if (fuelModeSelect.value === 'faa') {
        customInputsDiv.style.display = 'none';
        flightTypeDiv.style.display = 'block';
    } else {
        customInputsDiv.style.display = 'block';
        flightTypeDiv.style.display = 'none';
    }
};
toggleInputs();
fuelModeSelect.addEventListener('change', toggleInputs);

// Result unit change: re-display result in new unit without recalculating
const resultUnitSelect = document.getElementById('result-unit'); // Globals already defined at top

const updateResultDisplay = () => {
    if (lastCalculatedFuelUSG === 0) return; // No calculation done yet

    const resultUnit = resultUnitSelect.value;
    let totalFuelRequired = lastCalculatedFuelUSG;
    let unitName = 'gallons';
    if (resultUnit === 'LBS') {
        totalFuelRequired *= 6.7;
        unitName = 'lbs';
    } else if (resultUnit === 'L') {
        totalFuelRequired *= 3.785;
        unitName = 'liters';
    } else if (resultUnit === 'KG') {
        totalFuelRequired *= 3.04;
        unitName = 'kg';
    }

    // Reconstruct endurance using stored fuelConsumption
    const enduranceTakeoff = formatEndurance(lastCalculatedFuelUSG / lastFuelConsumptionUSG);
    const enduranceLanding = formatEndurance((lastCalculatedFuelUSG - lastTotalTripFuelUSG) / lastFuelConsumptionUSG);
    document.getElementById('result').innerText = `Total Fuel Required: ${totalFuelRequired.toFixed(2)} ${unitName}\nEstimated Time A to B: ${lastCalculatedTimeHours} hours ${lastCalculatedTimeMinutes} minutes\nAutonomia na decolagem: ${enduranceTakeoff}\nAutonomia no pouso: ${enduranceLanding}`;
};

resultUnitSelect.addEventListener('change', updateResultDisplay);

fuelCalculatorForm.addEventListener('submit', (event) => {
    event.preventDefault();
    calculateFuel();
});
