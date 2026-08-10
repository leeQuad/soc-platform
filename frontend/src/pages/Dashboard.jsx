import { useEffect, useState } from "react";
import api from "../utils/api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";


function Dashboard({ onLogout }) {
  const [alerts, setAlerts] = useState([]);
  const [threats, setThreats] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);


 useEffect(() => {
  const fetchData = async () => {
      try {
        const [alertsRes, threatsRes] = await Promise.all([
          api.get("/alerts/"),
          api.get("/threats/"),
         ]);

        setAlerts(alertsRes.data);
        setThreats(threatsRes.data);
      } catch (err) {
        setError("Could not load dashboard data. Try logging in again.");
      } finally {
        setLoading(false);
      } 
    };

    fetchData();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    onLogout();
  };
  const severityCounts = ["HIGH", "MEDIUM", "LOW"].map((level) => ({
    severity: level,
    count: alerts.filter((a) => a.severity === level).length,
 }));

  const severityColors = { HIGH: "#c1553f", MEDIUM: "#c99a4a", LOW: "#7c9473" };
  return (
    <div>
      <div className="page-header">
        <h2>SOC Dashboard</h2>
      </div>
       {error && <p style={{ color: "red" }}>{error}</p>}

      {loading ? (
        <p>Loading dashboard data...</p>
      ) : (
        <>
          <h3>Alerts by Severity</h3>

       <ResponsiveContainer width="100%" height={200}>
        <BarChart data={severityCounts}>
          <XAxis dataKey="severity" stroke="#999" />
          <YAxis allowDecimals={false} stroke="#999" />
          <Tooltip
            contentStyle={{ backgroundColor: "#111", border: "1px solid #2a2a2a" }}
          />
          <Bar dataKey="count">
            {severityCounts.map((entry) => (
              <Cell key={entry.severity} fill={severityColors[entry.severity]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

    <h3>Escalated Threats</h3>
      {threats.length > 0 ? (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Reason</th>
                <th>Linked Alert ID</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {threats.map((threat) => (
                <tr key={threat.id}>
                  <td>{threat.reason}</td>
                  <td>#{threat.alert_id}</td>
                  <td>{new Date(threat.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>No threats currently escalated.</p>
      )}

      <h3>Recent Alerts</h3>
      <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Severity</th>
            <th>Source</th>
            <th>Message</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((alert) => (
            <tr key={alert.id}>
              <td>{alert.severity}</td>
              <td>{alert.source}</td>
              <td>{alert.message}</td>
              <td>{new Date(alert.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
        </>
      )}
    </div>
  );
}
export default Dashboard;