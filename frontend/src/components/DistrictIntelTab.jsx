import React, { useState, useEffect } from "react";
import { api } from "../services/api";
import { MapPin, Building2, TrendingUp, AlertCircle, BarChart3 } from "lucide-react";

export function DistrictIntelTab() {
  const [districts, setDistricts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDistrictData();
  }, []);

  async function loadDistrictData() {
    setLoading(true);
    try {
      const res = await api.getDistrictDemand();
      setDistricts(res);
    } catch (e) {
      console.error("Failed to load district intelligence:", e);
    } finally {
      setLoading(false);
    }
  }

  // District profiles with industry specializations across Maharashtra
  const districtProfiles = {
    "Pune": {
      focus: "Automotive, Engineering & Information Technology",
      keySkills: ["Python", "CNC Machining", "AutoCAD", "Machine Learning"],
      status: "High Tech Growth Hub"
    },
    "Mumbai City": {
      focus: "Financial Services, Enterprise IT & Digital Media",
      keySkills: ["SQL", "React", "Data Analysis", "JavaScript"],
      status: "Services & Financial Capital"
    },
    "Mumbai Suburban": {
      focus: "Analytics, Logistics & Software Development",
      keySkills: ["Data Analysis", "Python", "Cloud Computing"],
      status: "High Demand Density"
    },
    "Nashik": {
      focus: "Automotive Component Manufacturing & Electrical",
      keySkills: ["Industrial Wiring", "PLC Programming", "Quality Control"],
      status: "Manufacturing Corridor"
    },
    "Nagpur": {
      focus: "Logistics Hub, Multimodal Cargo & Heavy Engineering",
      keySkills: ["Logistics", "Electrical Maintenance", "Supply Chain"],
      status: "Central Logistics Gateway"
    },
    "Chhatrapati Sambhajinagar": {
      focus: "Industrial Automation, Metallurgy & Machine Tooling",
      keySkills: ["PLC Programming", "Industrial Automation", "Welding"],
      status: "Emerging Automation Zone"
    }
  };

  return (
    <div className="sp-tab-content">
      {/* Intro Banner */}
      <div className="sp-card">
        <div className="sp-card-header">
          <div className="sp-card-title">
            <MapPin size={20} className="text-amber" />
            Maharashtra District-Level Workforce Intelligence (PRD Module 4)
          </div>
          <span className="sp-tag sp-tag-amber">Spatial Demand Telemetry</span>
        </div>
        <p className="sp-card-desc">
          Geographically attributed workforce demand across Maharashtra districts. Helps state planners avoid generic curriculum policies by tailoring vocational training to local industrial clusters.
        </p>
      </div>

      {loading ? (
        <div className="sp-loading-spinner">Loading district workforce telemetry...</div>
      ) : (
        <div className="sp-grid-2">
          {/* Active Demand Clusters */}
          <div className="sp-card">
            <div className="sp-card-header">
              <div className="sp-card-title">
                <BarChart3 size={18} className="text-blue" />
                Active District Demand Rankings
              </div>
            </div>

            <div className="sp-district-rankings">
              {districts.map((d, idx) => {
                const profile = districtProfiles[d.district] || {
                  focus: "General Regional Industries",
                  keySkills: ["Technical Basics", "Safety"],
                  status: "Developing Cluster"
                };

                return (
                  <div key={idx} className="sp-dist-card">
                    <div className="sp-dist-header">
                      <div>
                        <span className="sp-dist-rank">#{idx + 1}</span>
                        <h4 className="sp-dist-name">{d.district}</h4>
                      </div>
                      <div className="sp-dist-jobs">
                        <strong>{d.jobs_count}</strong> Postings Analyzed
                      </div>
                    </div>

                    <div className="sp-dist-focus">
                      <Building2 size={13} /> {profile.focus}
                    </div>

                    <div className="sp-dist-skills">
                      <span className="sp-dist-skills-label">Top Skills:</span>
                      <div className="sp-pill-group">
                        {profile.keySkills.map((sk, sidx) => (
                          <span key={sidx} className="sp-dist-skill-pill">
                            {sk}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Regional Policy & Shortage Insights */}
          <div className="sp-card">
            <div className="sp-card-header">
              <div className="sp-card-title">
                <TrendingUp size={18} className="text-emerald" />
                District Skill Shortage & Policy Advisory
              </div>
            </div>

            <div className="sp-policy-insights">
              <div className="sp-insight-item">
                <div className="sp-insight-badge blue">Pune Cluster</div>
                <h4>Automotive to Mechatronics Shift</h4>
                <p>
                  Severe shortage of candidates combining mechanical machining with software automation (PLC & Python). Recommended: Modernize ITI Fitter trades with 20% automation lab hours.
                </p>
              </div>

              <div className="sp-insight-item">
                <div className="sp-insight-badge amber">Nagpur Multi-Modal Zone</div>
                <h4>Logistics & Automated Warehousing</h4>
                <p>
                  High influx of logistics hubs around MIHAN corridor. Local ITIs lack modern supply chain inventory management certifications. Recommended: Introduce specialized 6-month Logistics Operator courses.
                </p>
              </div>

              <div className="sp-insight-item">
                <div className="sp-insight-badge purple">Nashik & Sambhajinagar</div>
                <h4>Industrial Safety (OSHA) & Smart Wiring</h4>
                <p>
                  Tier-1 tier automotive suppliers require ISO/OSHA certified electrical technicians. Traditional electrician courses teach domestic wiring; urgent upgrade needed for industrial panel wiring.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
