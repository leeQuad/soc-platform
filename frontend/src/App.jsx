import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import PortScanner from "./pages/PortScanner";
import LogParser from "./pages/LogParser";
import FileIntegrity from "./pages/FileIntegrity";
import Sidebar from "./components/Sidebar";
import NotFound from "./pages/NotFound";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"));

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
  };

  if (!isLoggedIn) {
    return <Login onLoginSuccess={() => setIsLoggedIn(true)} />;
  }

  return (
    <BrowserRouter>
      <div style={{ display: "flex" }}>
        <Sidebar onLogout={handleLogout} />
        <div style={{ padding: "16px", flex: 1 }}>
          <Routes>
            <Route path="/" element={<Dashboard onLogout={handleLogout} />} />
            <Route path="/scan" element={<PortScanner />} />
            <Route path="/logs" element={<LogParser />} />
            <Route path="/integrity" element={<FileIntegrity />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;