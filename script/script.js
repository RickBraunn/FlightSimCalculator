document.addEventListener('DOMContentLoaded', function() {
    // Show the custom alert when the page loads
    showDisclaimerAlert();
});

function showDisclaimerAlert() {
    const alertBox = document.getElementById('custom-alert');
    const alertMessage = document.getElementById('alert-message');
    alertMessage.innerText = "Disclaimer: This fuel calculator is designed exclusively for flight simulation purposes. It is not intended for actual flight planning or navigation. Please consult official resources and professionals for real-world flight operations.";
    
    alertBox.style.display = "flex"; // Show the modal
}

// Close the alert box when the user clicks the close button or the OK button
document.querySelector('.close-btn').addEventListener('click', closeAlert);
document.getElementById('ok-btn').addEventListener('click', closeAlert);

function closeAlert() {
    document.getElementById('custom-alert').style.display = "none"; // Hide the modal
}
// Function to calculate the total fuel required for a trip
function calculateFuel() {
    // Get input values from the form and parse them as floating-point numbers
    const distanceAB = parseFloat(document.getElementById('distance-ab').value); // Distance from A to B
    const distanceBC = parseFloat(document.getElementById('distance-bc').value); // Distance from B to C
    const cruiseSpeed = parseFloat(document.getElementById('cruise-speed').value); // Cruise speed of the vehicle
    const fuelConsumption = parseFloat(document.getElementById('fuel-consumption').value); // Fuel consumption per hour
    const headwind = parseFloat(document.getElementById('headwind').value); // Speed of the headwind

    // Calculate effective speed by subtracting headwind from cruise speed
    const speed = cruiseSpeed - headwind;

    // Calculate time taken to travel from A to B and from B to C
    const timeA = distanceAB / speed; // Time from A to B
    const timeB = distanceBC / speed; // Time from B to C

    // Calculate fuel required for each leg of the trip
    const fuelAB = timeA * fuelConsumption; // Fuel required for A to B
    const fuelBC = timeB * fuelConsumption; // Fuel required for B to C

    // Add a 5%  to the fuel required for each leg
    const totalFuelAB = fuelAB * 1.05; // Total fuel for A to B with buffer
    const totalFuelBC = fuelBC * 1.05; // Total fuel for B to C with buffer

    // Calculate total fuel required for the entire trip
    const totalTripFuel = totalFuelAB + totalFuelBC;

    // Calculate reserve fuel (75% of fuel consumption)
    const reserveFuel = 0.75 * fuelConsumption;

    // Calculate the grand total fuel required including reserve
    const totalFuelRequired = totalTripFuel + reserveFuel;

    // Display the result in the designated HTML element
    document.getElementById('result').innerText = `Total Fuel Required: ${totalFuelRequired.toFixed(2)} gallons`;
}

// Add event listener to the fuel calculator form
document.getElementById('fuel-calculator').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission behavior
    calculateFuel(); // Call the calculateFuel function
});

// Get the modal elements
var modal = document.getElementById('custom-alert');
var learnMoreText = document.getElementById('learn-more');
var closeButton = document.querySelector('.close-btn');
var okButton = document.getElementById('ok-btn');

// Function to show the modal
function showModal(message) {
    var alertMessage = document.getElementById('alert-message');
    alertMessage.innerText = message;
    modal.style.display = 'block';
}

// Function to hide the modal
function hideModal() {
    modal.style.display = 'none';
}

// Add event listeners to the learn more text and buttons
learnMoreText.addEventListener('click', function() {
    showModal('This calculator currently uses 5% fuel for contingency and 45 minutes for final reserve. In the future, it will match the FAA fuel requirements.');
});

closeButton.addEventListener('click', hideModal);
okButton.addEventListener('click', hideModal);

// Show the "Flight Simulator Only" message when the page loads
document.addEventListener('DOMContentLoaded', function() {
    showModal('Disclaimer: This fuel calculator is designed exclusively for flight simulation purposes. It is not intended for actual flight planning or navigation. Please consult official resources and professionals for real-world flight operations.');
});