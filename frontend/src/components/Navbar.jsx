import React from "react";
import { LayoutDashboard, Briefcase, GitCompare, Sparkles, MapPin, GraduationCap } from "lucide-react";

export function Navbar({ activeTab, setActiveTab, isConnected }) {
  const navItems = [
    { id: "overview", label: "Overview", icon: LayoutDashboard },
    { id: "jobs", label: "Tech Market Intel", icon: Briefcase },
    { id: "gap", label: "Curriculum Gap Audit", icon: GitCompare },
    { id: "modernization", label: "Board of Studies (BoS)", icon: Sparkles },
    { id: "districts", label: "India Tech Hubs", icon: MapPin },
  ];

  return (
    <header className="sp-header">
      <div className="sp-header-top">
        <div className="sp-brand">
          <div className="sp-logo">
            <GraduationCap className="sp-logo-icon" size={24} />
          </div>
          <div>
            <div className="sp-brand-title">SkillPulse Academic</div>
            <div className="sp-brand-sub">B.Tech CSE Curriculum & Tech Talent Intelligence Platform</div>
          </div>
        </div>

        <div className="sp-header-meta">
          <div className="sp-badge-gov">Engineering Higher Ed & Industry Alignment</div>
          <div className={`sp-status-pill ${isConnected ? "online" : "offline"}`}>
            <span className="sp-status-dot"></span>
            {isConnected ? "Engine Connected" : "Connecting to API..."}
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
