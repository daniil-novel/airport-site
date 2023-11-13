
function getFlightInfo() {
    const flightNumber = document.getElementById("flightNumber").value;

    // Fetch data for the specific flight
    const backendApiUrl = `http://127.0.0.1:5000/api/flight_info/${flightNumber}`;

    fetch(backendApiUrl)
        .then((response) => response.json())
        .then((data) => {
            // Display flight information
            displayFlightInfo(data);
        })
        .catch((error) => {
            console.error("Error fetching flight data:", error);
        });
}

function displayFlightInfo(data) {
    const flightStatus = document.getElementById("flightStatus");
    const flightTime = document.getElementById("flightTime");
    const flightRoute = document.getElementById("flightRoute");
    const flightDispatcher = document.getElementById("flightDispatcher");

    flightStatus.textContent = `Status: ${data.Status}`;
    flightTime.textContent = `Time: ${data.Time}`;
    flightRoute.textContent = `Route: ${data.Route}`;
    flightDispatcher.textContent = `Dispatcher: ${data.Dispatcher}`;
}
