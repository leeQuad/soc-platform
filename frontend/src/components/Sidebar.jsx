import { Link } from "react-router-dom";

function Sidebar({ onLogout }) {
  return (
    <div style={{ width: "200px", padding: "16px", borderRight: "1px solid #ccc" }}>
      <h3>SOC Platform</h3>
      <nav style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
        <Link to="/">Dashboard</Link>
        <Link to="/scan">Port Scanner</Link>
        <Link to="/logs">Log Parser</Link>
        <Link to="/integrity">File Integrity</Link>
      </nav>
      <button onClick={onLogout} style={{ marginTop: "16px" }}>
        Log Out
      </button>
    </div>
  );
}

export default Sidebar;