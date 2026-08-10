import { useState } from "react";
import api from "../utils/api";

function LogParser() {
  const [logFilePath, setLogFilePath] = useState("mock_logs.txt");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleParse = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const response = await api.post("/logs/parse", null, {
        params: { log_file_path: logFilePath },
      });
      
      setResult(response.data);
    } catch (err) {
      setError("Could not parse log file. Check the file path and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
  < div>
      <div className="page-header">
        <h2>Log Parser</h2>
       </div>
      <form onSubmit={handleParse}>
        <div>
          <label>Log File Path</label>
          <input value={logFilePath} onChange={(e) => setLogFilePath(e.target.value)} required />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Parsing..." : "Parse Logs"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div>
          <h3>Summary</h3>
          <ul>
            <li>Successful logins: {result.success_count}</li>
            <li>Failed logins: {result.failed_count}</li>
            <li>Success rate: {result.success_rate}%</li>
            <li>Most attacked IP: {result.most_attacked_ip || "None"}</li>
          </ul>

          <h3>Suspicious IPs</h3>
          {result.suspicious_ips.length > 0 ? (
            <table border="1" cellPadding="8">
              <thead>
                <tr>
                  <th>IP</th>
                  <th>Failed Attempts</th>
                  <th>Severity</th>
                  <th>First Seen</th>
                </tr>
              </thead>
              <tbody>
                {result.suspicious_ips.map((ip, index) => (
                  <tr key={index}>
                    <td>{ip.ip}</td>
                    <td>{ip.count}</td>
                    <td>{ip.level}</td>
                    <td>{ip.first_seen}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No suspicious activity found.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default LogParser;