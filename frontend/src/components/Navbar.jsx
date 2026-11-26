import React from "react";
import { LayoutDashboard, Briefcase, GitCompare, Sparkles, MapPin, Activity } from "lucide-react";

export function Navbar({ activeTab, setActiveTab, isConnected }) {
  const navItems = [
    { id: "overview", label: "Overview", icon: LayoutDashboard },
    { id: "jobs", label: "Labour Market Intel", icon: Briefcase },
    { id: "gap", label: "Skill Gap Analyzer", icon: GitCompare },
    { id: "modernization", label: "Curriculum Modernizer", icon: Sparkles },
    { id: "districts", label: "District Intel", icon: MapPin },
  ];

  return (
    <header className="sp-header">
      <div className="sp-header-top">
        <div className="sp-brand">
          <div className="sp-logo">
            <Activity className="sp-logo-icon" />
          </div>
          <div>
            <div className="sp-brand-title">SkillPulse</div>
            <div className="sp-brand-sub">Workforce Intelligence & Curriculum Alignment Platform</div>
          </div>
        </div>

        <div className="sp-header-meta">
          <div className="sp-badge-gov">Govt. of Maharashtra · MSInS</div>
          <div className={`sp-status-pill ${isConnected ? "online" : "offline"}`}>
            <span className="sp-status-dot"></span>
            {isConnected ? "Backend API Connected" : "Connecting to API..."}
          </div>
        </div>
      </div>

      <nav className="sp-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`sp-nav-tab ${isActive ? "active" : ""}`}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>
    </header>
  );
}
