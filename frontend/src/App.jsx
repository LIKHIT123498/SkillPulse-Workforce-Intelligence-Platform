import React, { useState, useEffect } from "react";
import { Navbar } from "./components/Navbar";
import { OverviewTab } from "./components/OverviewTab";
import { LabourMarketTab } from "./components/LabourMarketTab";
import { SkillGapTab } from "./components/SkillGapTab";
import { ModernizationTab } from "./components/ModernizationTab";
import { DistrictIntelTab } from "./components/DistrictIntelTab";
import { api } from "./services/api";
import "./App.css";

export default function App() {
  const [activeTab, setActiveTab] = useState("overview");
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    checkConnection();
    const interval = setInterval(checkConnection, 10000);
    return () => clearInterval(interval);
  }, []);

  async function checkConnection() {
    try {
      const res = await api.checkHealth();
      setIsConnected(res.status === "healthy");
    } catch {
      setIsConnected(false);
    }
  }

  return (
    <div className="sp-app-container">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isConnected={isConnected}
      />

      <main className="sp-main">
        {activeTab === "overview" && <OverviewTab setActiveTab={setActiveTab} />}
        {activeTab === "jobs" && <LabourMarketTab />}
        {activeTab === "gap" && <SkillGapTab setActiveTab={setActiveTab} />}
        {activeTab === "modernization" && <ModernizationTab />}
        {activeTab === "districts" && <DistrictIntelTab />}
      </main>

      <footer className="sp-footer">
        <div className="sp-footer-inner">
          <div>
            <strong>SkillPulse Academic – Computer Science Curriculum & Tech Talent Intelligence</strong>
            <p>SIH Problem Statement 26134 · Aligning Academic University Syllabi with Software Industry Demands</p>
          </div>
          <div className="sp-footer-credits">
            Benchmarking VTU, Mumbai University, SPPU, AKTU & Tier-1 Indian Tech Clusters
          </div>
        </div>
      </footer>
    </div>
  );
}
