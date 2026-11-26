import React, { useState, useEffect } from "react";
import { api } from "../services/api";
import { GitCompare, CheckCircle2, AlertCircle, XCircle, Sparkles, ArrowRight } from "lucide-react";

export function SkillGapTab({ setActiveTab }) {
  const [courses, setCourses] = useState([]);
  const [selectedCourseId, setSelectedCourseId] = useState("");
  const [targetRole, setTargetRole] = useState("Junior Python Developer");
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);

  useEffect(() => {
    loadCourses();
  }, []);

  async function loadCourses() {
    try {
      const res = await api.getCourses();
      setCourses(res);
      if (res.length > 0) {
        setSelectedCourseId(res[0].id);
      }
    } catch (e) {
      console.error("Failed to load courses:", e);
    }
  }

  async function handleRunAnalysis() {
    if (!selectedCourseId || !targetRole.trim()) return;
    setLoading(true);
    try {
      const res = await api.runGapAnalysis(Number(selectedCourseId), targetRole);
      setReport(res);
    } catch (e) {
      console.error("Skill gap analysis error:", e);
    } finally {
      setLoading(false);
    }
  }

  const roleSuggestions = [
    "Junior Python Developer",
    "Full Stack Web Developer",
    "CNC Milling Machine Operator",
    "Industrial Electrician",
    "Data Analyst",
    "AI / ML Associate",
  ];

  return (
    <div className="sp-tab-content">
      {/* Control Panel */}
      <div className="sp-card">
        <div className="sp-card-header">
          <div className="sp-card-title">
            <GitCompare size={20} className="text-emerald" />
            Curriculum Alignment Audit Matrix (PRD Module 2)
          </div>
          <span className="sp-tag">Deterministic Weighted Coverage</span>
        </div>

        <div className="sp-form-grid">
          <div>
            <label className="sp-label">Select Training Programme / ITI Course:</label>
            <select
              className="sp-select"
              value={selectedCourseId}
              onChange={(e) => setSelectedCourseId(e.target.value)}
            >
              {courses.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.course_name} ({c.qualification})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="sp-label">Target Industry Job Role:</label>
            <input
              type="text"
              className="sp-input"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g. Junior Python Developer"
            />
          </div>
        </div>

        {/* Suggestion tags */}
        <div className="sp-suggestions">
          <span className="sp-suggestion-label">Quick Benchmarks:</span>
          {roleSuggestions.map((role) => (
            <button
              key={role}
              className={`sp-btn-chip ${targetRole === role ? "active" : ""}`}
              onClick={() => setTargetRole(role)}
            >
              {role}
            </button>
          ))}
        </div>

        <div className="sp-form-actions">
          <button
            className="sp-btn-primary"
            onClick={handleRunAnalysis}
            disabled={loading}
          >
            {loading ? "Computing Weighted Alignment..." : "Generate Skill Gap Audit"}
          </button>
        </div>
      </div>

      {/* Analysis Results */}
      {report && (
        <div className="sp-report-section">
          {/* Header Metric Card */}
          <div className="sp-card sp-score-card">
            <div className="sp-score-main">
              <div
                className={`sp-score-badge ${
                  report.alignment_score >= 70
                    ? "high"
                    : report.alignment_score >= 40
                    ? "medium"
                    : "low"
                }`}
              >
                <div className="sp-score-num">{report.alignment_score}%</div>
                <div className="sp-score-title">Skill Alignment Score</div>
              </div>

              <div className="sp-score-meta">
                <h3>{report.course_name}</h3>
                <p>
                  Target Role: <strong>{report.target_role}</strong> · Audited against live Maharashtra job demand.
                </p>
                <div className="sp-score-stats">
                  <span>Required Competencies: <strong>{report.total_required_skills}</strong></span>
                  <span>Covered: <strong className="text-emerald">{report.total_covered_skills}</strong></span>
                  <span>Missing Gaps: <strong className="text-red">{report.total_missing_skills}</strong></span>
                </div>
              </div>
            </div>

            <button
              className="sp-btn-secondary"
              onClick={() => setActiveTab("modernization")}
            >
              <Sparkles size={16} /> View Modernization Proposals ({report.recommendations?.length || 0})
            </button>
          </div>

          {/* Detailed Competency Lists */}
          <div className="sp-grid-3">
            {/* Covered */}
            <div className="sp-card sp-col-covered">
              <div className="sp-col-header">
                <CheckCircle2 size={18} className="text-emerald" />
                <h4>Covered Competencies ({report.covered_skills?.length || 0})</h4>
              </div>
              <div className="sp-col-list">
                {report.covered_skills?.length === 0 ? (
                  <p className="sp-empty-text">No direct competencies covered.</p>
                ) : (
                  report.covered_skills.map((s, idx) => (
                    <div key={idx} className="sp-competency-item covered">
                      <span className="sp-comp-name">{s.canonical_name}</span>
                      <span className="sp-comp-badge">100% Weight</span>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Partially Covered */}
            <div className="sp-card sp-col-partial">
              <div className="sp-col-header">
                <AlertCircle size={18} className="text-amber" />
                <h4>Partially Covered ({report.partially_covered_skills?.length || 0})</h4>
              </div>
              <div className="sp-col-list">
                {report.partially_covered_skills?.length === 0 ? (
                  <p className="sp-empty-text">None partially covered.</p>
                ) : (
                  report.partially_covered_skills.map((s, idx) => (
                    <div key={idx} className="sp-competency-item partial">
                      <span className="sp-comp-name">{s.canonical_name}</span>
                      <span className="sp-comp-badge">50% Weight</span>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Missing */}
            <div className="sp-card sp-col-missing">
              <div className="sp-col-header">
                <XCircle size={18} className="text-red" />
                <h4>Missing Competencies ({report.missing_skills?.length || 0})</h4>
              </div>
              <div className="sp-col-list">
                {report.missing_skills?.length === 0 ? (
                  <p className="sp-empty-text">All competencies covered!</p>
                ) : (
                  report.missing_skills.map((s, idx) => (
                    <div key={idx} className="sp-competency-item missing">
                      <div>
                        <div className="sp-comp-name">{s.canonical_name}</div>
                        <div className="sp-comp-cat">{s.category} · Demanded in {s.demand_count} jobs</div>
                      </div>
                      <span className="sp-comp-badge red">Missing Gap</span>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
