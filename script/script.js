document.addEventListener('DOMContentLoaded', () => {
    showModal('Disclaimer: This fuel calculator is designed exclusively for flight simulation purposes. It is not intended for actual flight planning or navigation. Please consult official resources and professionals for real-world flight operations.');
});

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
const calculateFuel = () => {
    // Get input values and parse as floats
    const distanceAB = parseFloat(document.getElementById('distance-ab').value);
    const distanceBC = parseFloat(document.getElementById('distance-bc').value);
    const cruiseSpeed = parseFloat(document.getElementById('cruise-speed').value);
    const fuelConsumptionInput = parseFloat(document.getElementById('fuel-consumption').value);
    const headwind = parseFloat(document.getElementById('headwind').value);
    const taxiTime = parseFloat(document.getElementById('taxi-time').value);
    const fuelMode = document.getElementById('fuel-mode').value;
    const fuelConsumptionUnit = document.getElementById('fuel-consumption-unit').value;
    const resultUnit = document.getElementById('result-unit').value;

    // For custom mode, get contingency and reserve inputs
    let contingencyPercent = 5;
    let reserveMinutes = 45;
    if (fuelMode === 'custom') {
        contingencyPercent = parseFloat(document.getElementById('contingency').value);
        reserveMinutes = parseFloat(document.getElementById('reserve-minutes').value);
    }

    // Validate inputs
    if (
        isNaN(distanceAB) || distanceAB < 0 ||
        isNaN(distanceBC) || distanceBC < 0 ||
        isNaN(cruiseSpeed) || cruiseSpeed <= 0 ||
        isNaN(fuelConsumptionInput) || fuelConsumptionInput <= 0 ||
        isNaN(headwind) || headwind < 0 ||
        isNaN(taxiTime) || taxiTime < 0 ||
        isNaN(contingencyPercent) || contingencyPercent < 0 ||
        isNaN(reserveMinutes) || reserveMinutes < 0
    ) {
        document.getElementById('result').innerText = 'Please enter valid positive numbers for all inputs.';
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
        totalTripFuel = totalFuelAB + totalFuelBC;
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
            const tripFuelBC = calculateLegFuel(distanceBC, speed, fuelConsumption, 0);
            totalTripFuel = tripFuelAB + tripFuelBC;
            reserveFuel = (30 / 60) * fuelConsumption;
        } else {
            // Default fallback
            const totalFuelAB = calculateLegFuel(distanceAB, speed, fuelConsumption, 10);
            const totalFuelBC = calculateLegFuel(distanceBC, speed, fuelConsumption, 10);
            totalTripFuel = totalFuelAB + totalFuelBC;
            reserveFuel = (45 / 60) * fuelConsumption;
        }
    }

    const taxiFuel = (taxiTime / 60) * fuelConsumption;
    let totalFuelRequiredUSG = totalTripFuel + reserveFuel + taxiFuel;
    lastCalculatedFuelUSG = totalFuelRequiredUSG; // Store for result unit changes

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

    document.getElementById('result').innerText = `Total Fuel Required: ${totalFuelRequired.toFixed(2)} ${unitName}`;
};

const fuelCalculatorForm = document.getElementById('fuel-calculator');

const fuelModeSelect = document.getElementById('fuel-mode');
const customInputsDiv = document.getElementById('custom-inputs');
const flightTypeDiv = document.getElementById('flight-type-div');

const toggleInputs = () => {
    if (fuelModeSelect.value === 'custom') {
        customInputsDiv.style.display = 'block';
        flightTypeDiv.style.display = 'none';
    } else if (fuelModeSelect.value === 'faa') {
        customInputsDiv.style.display = 'none';
        flightTypeDiv.style.display = 'block';
    } else {
        customInputsDiv.style.display = 'none';
        flightTypeDiv.style.display = 'none';
    }
};
toggleInputs();
fuelModeSelect.addEventListener('change', toggleInputs);

// Result unit change: re-display result in new unit without recalculating
const resultUnitSelect = document.getElementById('result-unit');
let lastCalculatedFuelUSG = 0; // Store the last calculated fuel in USG

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
    document.getElementById('result').innerText = `Total Fuel Required: ${totalFuelRequired.toFixed(2)} ${unitName}`;
};

resultUnitSelect.addEventListener('change', updateResultDisplay);

fuelCalculatorForm.addEventListener('submit', (event) => {
    event.preventDefault();
    calculateFuel();
});
