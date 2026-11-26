import React, { useState, useEffect } from "react";
import { api } from "../services/api";
import { Search, Sparkles, MapPin, Building, Code } from "lucide-react";

export function LabourMarketTab() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sectorFilter, setSectorFilter] = useState("");
  const [nlpInput, setNlpInput] = useState(
    "Job Title: Senior Backend Software Engineer\nLocation: Bengaluru\nRequirements: 3+ years experience with Python or Go, building high-throughput microservices using FastAPI, Docker, and PostgreSQL. Hands-on experience with Redis caching, Kafka message streaming, and deploying on AWS Cloud. Strong grasp of System Design and CI/CD pipelines."
  );
  const [nlpResults, setNlpResults] = useState(null);
  const [nlpExtracting, setNlpExtracting] = useState(false);

  useEffect(() => {
    loadJobs();
  }, [sectorFilter]);

  async function loadJobs() {
    setLoading(true);
    try {
      const params = sectorFilter ? { sector: sectorFilter } : {};
      const res = await api.getJobs(params);
      setJobs(res);
    } catch (e) {
      console.error("Failed to load jobs:", e);
    } finally {
      setLoading(false);
    }
  }

  async function handleExtractSkills() {
    if (!nlpInput.trim()) return;
    setNlpExtracting(true);
    try {
      const res = await api.extractSkills(nlpInput);
      setNlpResults(res);
    } catch (e) {
      console.error("NLP extraction error:", e);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="sp-tab-content">
      {/* Interactive NLP Extraction Playground */}
      <div className="sp-card sp-nlp-card">
        <div className="sp-card-header">
          <div className="sp-card-title">
            <Sparkles size={20} className="text-purple" />
            Live NLP Skill Extraction & Hybrid Matcher Playground
          </div>
          <span className="sp-tag sp-tag-purple">Hybrid Word-Boundary & Semantic Parsing</span>
        </div>
        <p className="sp-card-desc">
          Paste any raw software engineering job posting, syllabus module, or internship requirement to extract canonical competencies, detect Course Outcomes (COs), and compute confidence weights in real time.
        </p>

        <div className="sp-nlp-controls">
          <textarea
            className="sp-textarea"
            rows={4}
            value={nlpInput}
            onChange={(e) => setNlpInput(e.target.value)}
            placeholder="Paste raw tech JD or university syllabus module text here..."
          />
          <button
            className="sp-btn-primary"
            onClick={handleExtractSkills}
            disabled={nlpExtracting}
          >
            {nlpExtracting ? "Extracting Competencies..." : "Extract Tech Competencies with NLP"}
          </button>
        </div>

        {nlpResults && (
          <div className="sp-nlp-results">
            <div className="sp-nlp-results-header">
              Extracted <strong>{nlpResults.total_skills_extracted}</strong> canonical software competencies:
            </div>
            <div className="sp-pill-group">
              {nlpResults.skills.map((s, idx) => (
                <div key={idx} className="sp-skill-chip">
                  <span className="sp-skill-chip-name">{s.canonical_name}</span>
                  <span className="sp-skill-chip-cat">{s.category}</span>
                  <span className="sp-skill-chip-weight">w: {s.importance}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Filterable Software Job Directory */}
      <div className="sp-card">
        <div className="sp-card-header">
          <div className="sp-card-title">
            <Search size={20} className="text-blue" />
            Ingested Software Job Market Records ({jobs.length})
          </div>
          <div className="sp-filter-bar">
            <select
              className="sp-select"
              value={sectorFilter}
              onChange={(e) => setSectorFilter(e.target.value)}
            >
              <option value="">All Engineering Domains</option>
              <option value="Product Engineering">Product Engineering</option>
              <option value="FinTech">FinTech</option>
              <option value="Cloud & Infrastructure">Cloud & Infrastructure</option>
              <option value="Artificial Intelligence">Artificial Intelligence</option>
              <option value="IT Services">IT Services</option>
              <option value="Quick Commerce">Quick Commerce</option>
              <option value="SaaS">SaaS</option>
            </select>
          </div>
        </div>

        {loading ? (
          <div className="sp-loading-spinner">Loading tech job market records...</div>
        ) : (
          <div className="sp-jobs-list">
            {jobs.map((job) => (
              <div key={job.id} className="sp-job-card">
                <div className="sp-job-header">
                  <div>
                    <h3 className="sp-job-title">{job.title}</h3>
                    <div className="sp-job-meta">
                      <span className="sp-meta-item">
                        <Building size={14} /> {job.company_name || "Tech Enterprise"}
                      </span>
                      <span className="sp-meta-item">
                        <MapPin size={14} /> {job.district?.district_name || "India Tech Hub"}
                      </span>
                      <span className="sp-badge-sector">{job.sector}</span>
                    </div>
                  </div>
                </div>
                <p className="sp-job-desc">{job.description}</p>
                <div className="sp-job-skills">
                  <span className="sp-skills-label">Required Tech Stack:</span>
                  <div className="sp-pill-group">
                    {job.required_skills?.map((js, idx) => (
                      <span key={idx} className="sp-badge-skill">
                        {js.skill.canonical_name || js.skill.skill_name}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
