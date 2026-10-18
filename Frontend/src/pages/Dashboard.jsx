import { useEffect, useState } from "react";

import PageHeader from "../components/PageHeader";
import SummaryCards from "../components/SummaryCards";
import SolarOutputChart from "../components/SolarOutputChart";
import PredictionsTable from "../components/PredictionsTable";

import { getSolarHistory, getSolarPredictions } from "../services/solarService";

const STATES = [
  "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
  "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
  "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
  "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
  "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
  "Andaman and Nicobar Islands", "Chandigarh",
  "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir",
  "Ladakh", "Lakshadweep", "Puducherry",
];

const DISTRICTS = {
  Maharashtra: [
    "Pune", "Mumbai City", "Mumbai Suburban", "Nashik", "Nagpur", "Thane",
    "Kolhapur", "Satara", "Sangli", "Solapur", "Chhatrapati Sambhajinagar",
    "Ratnagiri", "Raigad", "Ahmednagar", "Jalgaon", "Amravati", "Akola",
    "Nanded",
  ],
};

const DEFAULT_LOCATION = "Pune, Maharashtra, India";

function Dashboard() {
  const [history, setHistory] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [selectedState, setSelectedState] = useState("Maharashtra");
  const [selectedDistrict, setSelectedDistrict] = useState("Pune");
  const [activeLocation, setActiveLocation] = useState(DEFAULT_LOCATION);

  const districtOptions = DISTRICTS[selectedState] || [];

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [historyData, predictionData] = await Promise.all([
          getSolarHistory(),
          getSolarPredictions(DEFAULT_LOCATION),
        ]);

        setHistory(historyData);
        setPredictions(predictionData);
      } catch (err) {
        setError(err.message || "Unable to load dashboard data.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  async function loadLocation(location) {
    setSearching(true);
    setError("");

    try {
      const predictionData = await getSolarPredictions(location);
      setPredictions(predictionData);
      setActiveLocation(location);
    } catch (err) {
      setError(err.message || "Unable to fetch predictions for this location.");
    } finally {
      setSearching(false);
    }
  }

  async function handleSearch(event) {
    event.preventDefault();

    const location = search.trim()
      ? `${search.trim()}, India`
      : `${selectedDistrict || selectedState}, India`;

    await loadLocation(location);
  }

  async function handleFilterSearch() {
    const location = selectedDistrict
      ? `${selectedDistrict}, ${selectedState}, India`
      : `${selectedState}, India`;

    setSearch("");
    await loadLocation(location);
  }

  if (loading) {
    return <div className="message-card">Loading solar dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <PageHeader />

      <main className="main-content">
        <section className="location-panel">
          <h2>Search location</h2>

          <form className="location-search-form" onSubmit={handleSearch}>
            <input
              type="text"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search city, district or state..."
              aria-label="Search city, district or state"
            />
            <button type="submit" disabled={searching}>
              {searching ? "Searching..." : "Search"}
            </button>
          </form>

          <div className="location-filters">
            <label>
              State
              <select
                value={selectedState}
                onChange={(event) => {
                  setSelectedState(event.target.value);
                  setSelectedDistrict("");
                }}
              >
                {STATES.map((state) => (
                  <option key={state} value={state}>
                    {state}
                  </option>
                ))}
              </select>
            </label>

            <label>
              District
              <select
                value={selectedDistrict}
                onChange={(event) => setSelectedDistrict(event.target.value)}
                disabled={districtOptions.length === 0}
              >
                <option value="">
                  {districtOptions.length === 0
                    ? "No districts listed"
                    : "Select district"}
                </option>
                {districtOptions.map((district) => (
                  <option key={district} value={district}>
                    {district}
                  </option>
                ))}
              </select>
            </label>

            <button
              type="button"
              onClick={handleFilterSearch}
              disabled={searching}
            >
              {searching ? "Loading..." : "Apply filters"}
            </button>
          </div>

          <p className="active-location">
            Showing forecast for: <strong>{activeLocation}</strong>
          </p>

          {error && (
            <div className="error-message" role="alert">
              {error}
            </div>
          )}
        </section>

        <SummaryCards history={history} predictions={predictions} />

        <SolarOutputChart history={history} predictions={predictions} />

        <PredictionsTable predictions={predictions} />
      </main>

      <footer className="footer">Solar Power Prediction Application</footer>
    </div>
  );
}

export default Dashboard;