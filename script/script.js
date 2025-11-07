document.addEventListener('DOMContentLoaded', () => {
    showModal('Disclaimer: This fuel calculator is designed exclusively for flight simulation purposes. It is not intended for actual flight planning or navigation. Please consult official resources and professionals for real-world flight operations.');
});

// Modal elements
const modal = document.getElementById('custom-alert');
const alertMessage = document.getElementById('alert-message');
const learnMoreText = document.getElementById('learn-more');
const closeButton = document.querySelector('.close-btn');
const okButton = document.getElementById('ok-btn');

// Show modal with message
const showModal = (message) => {
    alertMessage.innerText = message;
    modal.style.display = 'flex';
};

// Hide modal
const hideModal = () => {
    modal.style.display = 'none';
};

// Event listeners for modal buttons and learn more text
learnMoreText.addEventListener('click', () => {
    showModal('This calculator currently uses 5% fuel for contingency and 45 minutes for final reserve. In the future, it will match the FAA fuel requirements.');
});
closeButton.addEventListener('click', hideModal);
okButton.addEventListener('click', hideModal);
const calculateFuel = () => {
    // Get input values and parse as floats
    const distanceAB = parseFloat(document.getElementById('distance-ab').value);
    const distanceBC = parseFloat(document.getElementById('distance-bc').value);
    const cruiseSpeed = parseFloat(document.getElementById('cruise-speed').value);
    const fuelConsumption = parseFloat(document.getElementById('fuel-consumption').value);
    const headwind = parseFloat(document.getElementById('headwind').value);
    const taxiTime = parseFloat(document.getElementById('taxi-time').value);
    const fuelMode = document.getElementById('fuel-mode').value;

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
        isNaN(fuelConsumption) || fuelConsumption <= 0 ||
        isNaN(headwind) || headwind < 0 ||
        isNaN(taxiTime) || taxiTime < 0 ||
        isNaN(contingencyPercent) || contingencyPercent < 0 ||
        isNaN(reserveMinutes) || reserveMinutes < 0
    ) {
        document.getElementById('result').innerText = 'Please enter valid positive numbers for all inputs.';
        return;
    }

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
    const totalFuelRequired = totalTripFuel + reserveFuel + taxiFuel;

    document.getElementById('result').innerText = `Total Fuel Required: ${totalFuelRequired.toFixed(2)} gallons`;
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

fuelCalculatorForm.addEventListener('submit', (event) => {
    event.preventDefault();
    calculateFuel();
});
