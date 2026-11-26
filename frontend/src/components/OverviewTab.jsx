import React, { useEffect, useState } from "react";
import { api } from "../services/api";
import { Briefcase, Cpu, Award, MapPin, TrendingUp, ArrowRight, BookOpen } from "lucide-react";

export function OverviewTab({ setActiveTab }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadOverview();
  }, []);

  async function loadOverview() {
    setLoading(true);
    try {
      const res = await api.getOverview();
      setData(res);
    } catch (e) {
      console.error("Failed to load overview data:", e);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div className="sp-loading-spinner">Loading tech curriculum & hiring intelligence...</div>;
  }

  const kpis = [
    { label: "Software Job Postings", value: data?.total_jobs_analyzed || 0, icon: Briefcase, color: "blue" },
    { label: "CSE Skills & Stacks", value: data?.unique_skills_identified || 0, icon: Cpu, color: "emerald" },
    { label: "Active Tech Hubs", value: data?.districts_covered || 0, icon: MapPin, color: "amber" },
    { label: "University Syllabi", value: 9, icon: Award, color: "purple" },
  ];

  return (
    <div className="sp-tab-content">
      {/* Banner */}
      <div className="sp-hero-banner">
        <div>
          <h2>Bridging Computer Science Syllabi with Real-World Tech Hiring Demand</h2>
          <p>
            Equipping university Board of Studies (BoS), CSE academic heads, and engineering students with real-time telemetry from India's premier tech clusters (Bengaluru, Hyderabad, Pune, Gurugram, Noida).
          </p>
        </div>
        <div className="sp-banner-actions">
          <button className="sp-btn-primary" onClick={() => setActiveTab("gap")}>
            Audit University Syllabus Gap <ArrowRight size={16} />
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="sp-kpi-grid">
        {kpis.map((kpi, idx) => {
          const Icon = kpi.icon;
          return (
            <div key={idx} className={`sp-kpi-card sp-kpi-${kpi.color}`}>
              <div className="sp-kpi-header">
                <span className="sp-kpi-label">{kpi.label}</span>
                <Icon size={20} className="sp-kpi-icon" />
              </div>
              <div className="sp-kpi-value">{kpi.value}</div>
            </div>
          );
        })}
      </div>

      <div className="sp-grid-2">
        {/* Top Demanded Skills */}
        <div className="sp-card">
          <div className="sp-card-header">
            <div className="sp-card-title">
              <TrendingUp size={20} className="text-emerald" />
              Highest-Demanded Tech Competencies
            </div>
            <span className="sp-tag">Calculated from Live Indian Postings</span>
          </div>
          <div className="sp-skill-bars">
            {data?.top_demanded_skills?.map((item, i) => (
              <div key={i} className="sp-bar-item">
                <div className="sp-bar-meta">
                  <span className="sp-bar-name">{item.skill}</span>
                  <span className="sp-bar-count">{item.count} postings</span>
                </div>
                <div className="sp-progress-track">
                  <div
                    className="sp-progress-fill"
                    style={{ width: `${Math.min(item.count * 8, 100)}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Sector / Tech Specialization Breakdown */}
        <div className="sp-card">
          <div className="sp-card-header">
            <div className="sp-card-title">
              <BookOpen size={20} className="text-blue" />
              Hiring Sector & Engineering Domain Breakdown
            </div>
            <span className="sp-tag">Tier-1 Tech Companies</span>
          </div>
          <div className="sp-sector-list">
            {data?.sector_distribution?.map((sec, i) => (
              <div key={i} className="sp-sector-row">
                <span className="sp-sector-name">{sec.sector}</span>
                <div className="sp-sector-badge">{sec.jobs_count} Postings</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
