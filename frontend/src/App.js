import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/api/data")
      .then((response) => setData(response.data))
      .catch((err) => {
        setError("Failed to load data. Please try again later.");
        console.error("API Error:", err);
      });
  }, []);

  if (error) return <div className="error">{error}</div>;
  if (!data) return <div className="loading">Loading...</div>;

  return (
    <div className="dashboard">
      <h1 className="title">Server Access Analytics</h1>

      <div className="grid-container">
        <div className="card ip-histogram">
          <h2>Distinct IP Address Frequency</h2>
          <pre>{data.ip_histogram}</pre>
        </div>

        <div className="card hourly-traffic">
          <h2>Hourly Traffic in a given day</h2>
          <pre>{data.hourly_traffic}</pre>
        </div>

        <div className="card top-contributors">
          <h2>Top IPs (85% Traffic)</h2>
          <pre>{data.top_ips}</pre>
        </div>

        <div className="card top-hours">
          <h2>Peak Hours (70% Traffic)</h2>
          <pre>{data.top_hours}</pre>
        </div>
      </div>
    </div>
  );
}

export default App;
