import React, { useState, useEffect, useRef } from "react";
import { api } from "../services/api";
import { GitCompare, CheckCircle2, AlertCircle, XCircle, Sparkles, Upload, FileText, Check } from "lucide-react";

export function SkillGapTab({ setActiveTab }) {
  const [courses, setCourses] = useState([]);
  const [selectedCourseId, setSelectedCourseId] = useState("");
  const [targetRole, setTargetRole] = useState("Senior Backend Engineer");
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);

  // PDF Upload States
  const [uploadingPdf, setUploadingPdf] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    loadCourses();
  }, []);

  async function loadCourses(autoSelectId = null) {
    try {
      const res = await api.getCourses();
      setCourses(res);
      if (autoSelectId) {
        setSelectedCourseId(autoSelectId);
      } else if (res.length > 0 && !selectedCourseId) {
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

  async function handlePdfUpload(e) {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadingPdf(true);
    setUploadSuccess(null);
    try {
      const res = await api.importSyllabusPdf(file, "Technical University Board", "B.Tech CSE");
      setUploadSuccess(`Successfully parsed syllabus: ${res.course_name} (${res.total_skills_mapped} competencies mapped)`);
      await loadCourses(res.course_id);
    } catch (err) {
      alert("Error parsing syllabus PDF: " + err.message);
    } finally {
      setUploadingPdf(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  }

  const roleSuggestions = [
    "Senior Backend Engineer",
    "Full Stack Software Engineer",
    "DevOps & Cloud Platform Engineer",
    "Generative AI & ML Engineer",
    "Cloud Native Backend Developer",
    "Distributed Systems Software Engineer"
  ];

  return (
    <div className="sp-tab-content">
      {/* Syllabus Ingestion & Control Panel */}
      <div className="sp-card">
        <div className="sp-card-header">
          <div className="sp-card-title">
            <GitCompare size={20} className="text-emerald" />
            University Syllabus & Tech Hiring Audit Matrix (PRD Module 2)
          </div>
          <div className="sp-pdf-upload-btn-wrapper">
            <input
              type="file"
              ref={fileInputRef}
              accept=".pdf"
              style={{ display: "none" }}
              onChange={handlePdfUpload}
            />
            <button
              className="sp-btn-secondary"
              onClick={() => fileInputRef.current?.click()}
              disabled={uploadingPdf}
            >
              <Upload size={15} />
              {uploadingPdf ? "Parsing Syllabus PDF..." : "Upload Syllabus PDF"}
            </button>
          </div>
        </div>

        {uploadSuccess && (
          <div className="sp-alert-success">
            <Check size={16} /> {uploadSuccess}
          </div>
        )}

        <div className="sp-form-grid">
          <div>
            <label className="sp-label">Select University Syllabus / Academic Scheme:</label>
            <select
              className="sp-select"
              value={selectedCourseId}
              onChange={(e) => setSelectedCourseId(e.target.value)}
            >
              {courses.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.course_name} ({c.institution || "University"})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="sp-label">Target Industry Tech Job Role (India Tech Hubs):</label>
            <input
              type="text"
              className="sp-input"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g. Senior Backend Engineer"
            />
          </div>
        </div>

        {/* Suggestion tags */}
        <div className="sp-suggestions">
          <span className="sp-suggestion-label">Industry Benchmarks:</span>
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
            {loading ? "Computing Weighted Competency Alignment..." : "Generate Syllabus Gap Audit"}
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
                <div className="sp-score-title">Curriculum Alignment</div>
              </div>

              <div className="sp-score-meta">
                <h3>{report.course_name}</h3>
                <p>
                  Target Role: <strong>{report.target_role}</strong> · Audited against tier-1 tech hiring standards.
                </p>
                <div className="sp-score-stats">
                  <span>Industry Requirements: <strong>{report.total_required_skills}</strong></span>
                  <span>Covered in Syllabus: <strong className="text-emerald">{report.total_covered_skills}</strong></span>
                  <span>Industry Gaps: <strong className="text-red">{report.total_missing_skills}</strong></span>
                </div>
              </div>
            </div>

            <button
              className="sp-btn-secondary"
              onClick={() => setActiveTab("modernization")}
            >
              <Sparkles size={16} /> Board of Studies Proposals ({report.recommendations?.length || 0})
            </button>
          </div>

          {/* Detailed Competency Lists */}
          <div className="sp-grid-3">
            {/* Covered */}
            <div className="sp-card sp-col-covered">
              <div className="sp-col-header">
                <CheckCircle2 size={18} className="text-emerald" />
                <h4>Covered in Syllabus ({report.covered_skills?.length || 0})</h4>
              </div>
              <div className="sp-col-list">
                {report.covered_skills?.length === 0 ? (
                  <p className="sp-empty-text">No direct competencies covered in current syllabus.</p>
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
                <h4>Partially Covered / Conceptual ({report.partially_covered_skills?.length || 0})</h4>
              </div>
              <div className="sp-col-list">
                {report.partially_covered_skills?.length === 0 ? (
                  <p className="sp-empty-text">No partially covered skills.</p>
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

            {/* Missing Gaps */}
            <div className="sp-card sp-col-missing">
              <div className="sp-col-header">
                <XCircle size={18} className="text-red" />
                <h4>Industry Skill Gaps ({report.missing_skills?.length || 0})</h4>
              </div>
              <div className="sp-col-list">
                {report.missing_skills?.length === 0 ? (
                  <p className="sp-empty-text">Zero gaps! Syllabus matches 100% of industry requirements.</p>
                ) : (
                  report.missing_skills.map((s, idx) => (
                    <div key={idx} className="sp-competency-item missing">
                      <div>
                        <div className="sp-comp-name">{s.canonical_name}</div>
                        <div className="sp-comp-cat">{s.category} · Demanded in {s.demand_count} tech postings</div>
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
