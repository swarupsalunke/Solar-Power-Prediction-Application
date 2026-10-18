
const API_URL = "https://solar-power-prediction-application.onrender.com"

async function fetchJson(endpoint) {
    const response = await fetch(`${API_URL}${endpoint}`);

    if (!response.ok) {
        let message = `API request failed: ${response.status}`;

        try {
            const errorData = await response.json();
            message = errorData.detail || message;
        } catch {
            // Keep the default error message.
        }

        throw new Error(message);
    }

    return response.json();
}

export function getSolarHistory() {
    return fetchJson("/api/history");
}

export function getSolarPredictions(location = "Pune, Maharashtra, India") {
    const params = new URLSearchParams({ location });

    return fetchJson(`/api/predictions?${params.toString()}`);
}
