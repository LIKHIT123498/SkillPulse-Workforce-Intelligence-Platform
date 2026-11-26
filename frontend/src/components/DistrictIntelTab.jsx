import React, { useState, useEffect } from "react";
import { api } from "../services/api";
import { MapPin, Building2, TrendingUp, BarChart3, Code2 } from "lucide-react";

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
      console.error("Failed to load tech hub telemetry:", e);
    } finally {
      setLoading(false);
    }
  }

  // Premier Indian Tech Hub Profiles & Hiring Stack Focus
  const techHubProfiles = {
    "Bengaluru": {
      focus: "High-Throughput Microservices, AI/ML, Cloud Native & FinTech",
      keySkills: ["Go", "Python", "Kubernetes", "Redis", "Kafka", "Generative AI & LLMs"],
      tier: "Tier-1 Primary Tech Cluster (Silicon Valley of India)"
    },
    "Hyderabad": {
      focus: "Enterprise Cloud Platforms, Big Tech R&D & Distributed Systems",
      keySkills: ["AWS Cloud", "Docker", "CI/CD Pipelines", "Java", "Python"],
      tier: "Tier-1 Cloud & Enterprise Engineering Hub"
    },
    "Pune": {
      focus: "Product Consulting, Automotive Tech & Cloud Native Backend",
      keySkills: ["Python", "FastAPI", "Docker", "PostgreSQL", "Machine Learning"],
      tier: "Tier-1 Software Engineering & Research Center"
    },
    "Gurugram": {
      focus: "High-Scale E-Commerce, Quick Commerce & Event-Driven Systems",
      keySkills: ["Java", "Spring Boot", "Kafka", "Redis", "System Design & Microservices"],
      tier: "Tier-1 Product & Startup Engineering Hub"
    },
    "Noida": {
      focus: "FinTech, Payments Systems & Modern Frontend Engineering",
      keySkills: ["React", "Next.js", "TypeScript", "Node.js", "REST APIs"],
      tier: "Tier-1 Software Development Hub"
    },
    "Chennai": {
      focus: "Multi-Tenant SaaS Engineering, Deep Tech & Enterprise Infrastructure",
      keySkills: ["Java", "PostgreSQL", "React", "REST APIs", "Cloud Computing"],
      tier: "Tier-1 Global SaaS Capital"
    },
    "Mumbai": {
      focus: "FinTech Banking Platforms, Enterprise IT Services & Analytics",
      keySkills: ["Java", "Spring Boot", "Data Analysis", "SQL", "Cloud Computing"],
      tier: "Tier-1 Financial Technology Gateway"
    }
  };

  return (
    <div className="sp-tab-content">
      {/* Intro Banner */}
      <div className="sp-card">
        <div className="sp-card-header">
          <div className="sp-card-title">
            <MapPin size={20} className="text-amber" />
            India Tech Hub Hiring Telemetry & Academic Specialization (PRD Module 4)
          </div>
          <span className="sp-tag sp-tag-amber">Spatial Tech Demand Telemetry</span>
        </div>
        <p className="sp-card-desc">
          Geographically attributed software engineering demand across India's premier tech hiring clusters. Helps university academic councils and placement cells align regional elective offerings with city-level hiring stacks.
        </p>
      </div>

      {loading ? (
        <div className="sp-loading-spinner">Loading tech hub hiring telemetry...</div>
      ) : (
        <div className="sp-grid-2">
          {/* Active Demand Clusters */}
          <div className="sp-card">
            <div className="sp-card-header">
              <div className="sp-card-title">
                <BarChart3 size={18} className="text-blue" />
                Active Tech Hub Hiring Volume
              </div>
            </div>

            <div className="sp-district-rankings">
              {districts.map((d, idx) => {
                const profile = techHubProfiles[d.district] || {
                  focus: "General IT Services & Digital Engineering",
                  keySkills: ["Java", "SQL", "Python", "Git"],
                  tier: "Emerging Tech Hub"
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
                      <span className="sp-dist-skills-label">Dominant Stacks:</span>
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

          {/* Regional Academic & Placement Insights */}
          <div className="sp-card">
            <div className="sp-card-header">
              <div className="sp-card-title">
                <TrendingUp size={18} className="text-emerald" />
                Graduate Placement & Academic Specialization Insights
              </div>
            </div>

            <div className="sp-policy-insights">
              <div className="sp-insight-item">
                <div className="sp-insight-badge blue">Bengaluru Cluster</div>
                <h4>High-Scale Microservices & Generative AI</h4>
                <p>
                  High hiring premium for graduating engineers who understand asynchronous architectures (Go/FastAPI), vector retrieval (RAG), and Kubernetes container deployments over legacy monoliths.
                </p>
              </div>

              <div className="sp-insight-item">
                <div className="sp-insight-badge amber">Hyderabad & Pune Corridor</div>
                <h4>Cloud Native & DevSecOps</h4>
                <p>
                  Accelerated hiring for enterprise cloud migrations. Colleges in these regions should mandate Docker and automated CI/CD lab exercises in 6th semester Computer Networks and Cloud electives.
                </p>
              </div>

              <div className="sp-insight-item">
                <div className="sp-insight-badge purple">Gurugram & Noida Zone</div>
                <h4>Event Streaming & High-Availability Databases</h4>
                <p>
                  Consumer tech unicorns (Zomato, Blinkit, Paytm) prioritize engineers proficient with message queues (Kafka), distributed cache invalidation (Redis), and PostgreSQL indexing.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
