import { useState } from "react";
import api from "../utils/api";

function PortScanner() {
  const [target, setTarget] = useState("");
  const [startPort, setStartPort] = useState(1);
  const [endPort, setEndPort] = useState(1000);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleScan = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const response = await api.post("/scan/", null, {
        params: { target, start_port: startPort, end_port: endPort },
      });

      setResult(response.data);
    } catch (err) {
      setError("Scan failed. Check your target and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
     <div>
      <div className="page-header">
        <h2>Port Scanner</h2>
      </div>
      <form onSubmit={handleScan}>
        <div>
          <label>Target IP</label>
          <input value={target} onChange={(e) => setTarget(e.target.value)} required />
        </div>
        <div>
          <label>Start Port</label>
          <input
            type="number"
            value={startPort}
            onChange={(e) => setStartPort(Number(e.target.value))}
          />
        </div>
        <div>
          <label>End Port</label>
          <input
            type="number"
            value={endPort}
            onChange={(e) => setEndPort(Number(e.target.value))}
          />
        </div>
        <button type="submit" disabled={loading || !target}>
          {loading ? "Scanning..." : "Start Scan"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div>
          <h3>Results for {result.target}</h3>
          <p>
            Scanned ports {result.start_port}–{result.end_port}
          </p>
          {result.open_ports.length > 0 ? (
            <ul>
              {result.open_ports.map((port) => (
                <li key={port}>Port {port} is OPEN</li>
              ))}
            </ul>
          ) : (
            <p>No open ports found.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default PortScanner;
