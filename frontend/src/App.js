// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;

// import React, { useEffect, useState } from "react";
// import axios from "axios";
// import "./App.css";

// function App() {
//   const [data, setData] = useState(null);

//   useEffect(() => {
//     // Fetch data from Flask backend
//     axios
//       .get("http://127.0.0.1:5000/api/data")
//       .then((response) => setData(response.data))
//       .catch((error) => console.error(error));
//   }, []);

//   if (!data) return <div>Loading...</div>;

//   return (
//     <div className="App">
//       <h1>Log Parser Dashboard</h1>
//       <pre>{JSON.stringify(data, null, 2)}</pre>
//     </div>
//   );
// }

// export default App;

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
