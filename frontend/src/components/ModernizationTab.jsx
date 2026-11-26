import React, { useState, useEffect } from "react";
import { api } from "../services/api";
import { Sparkles, Check, X, BookOpen, Clock, Target, Layers } from "lucide-react";

export function ModernizationTab() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState("");

  useEffect(() => {
    loadRecommendations();
  }, [statusFilter]);

  async function loadRecommendations() {
    setLoading(true);
    try {
      const params = statusFilter ? { status: statusFilter } : {};
      const res = await api.getRecommendations(params);
      setRecommendations(res);
    } catch (e) {
      console.error("Failed to load recommendations:", e);
    } finally {
      setLoading(false);
    }
  }

  async function handleStatusChange(id, newStatus) {
    try {
      await api.updateRecommendationStatus(id, newStatus);
      setRecommendations((prev) =>
        prev.map((r) => (r.id === id ? { ...r, status: newStatus } : r))
      );
    } catch (e) {
      console.error("Failed to update status:", e);
    }
  }

  return (
    <div className="sp-tab-content">
      {/* Header Banner */}
      <div className="sp-card">
        <div className="sp-card-header">
          <div className="sp-card-title">
            <Sparkles size={20} className="text-purple" />
            Curriculum Modernization & Approval Hub (PRD Module 3)
          </div>
          <div className="sp-filter-bar">
            <select
              className="sp-select"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="">All Review Statuses</option>
              <option value="PENDING">Pending Review</option>
              <option value="APPROVED">Approved for Rollout</option>
              <option value="REJECTED">Archived / Rejected</option>
            </select>
          </div>
        </div>
        <p className="sp-card-desc">
          Automated syllabus modernisation units synthesized from detected industry skill deficits. Authorized administrators and institutional heads can review, approve, or reject proposed units.
        </p>
      </div>

      {loading ? (
        <div className="sp-loading-spinner">Loading curriculum recommendations...</div>
      ) : recommendations.length === 0 ? (
        <div className="sp-card sp-empty-card">
          <BookOpen size={40} className="sp-empty-icon" />
          <h3>No Recommendations Found</h3>
          <p>Run a Skill Gap Audit first to generate evidence-backed curriculum improvements.</p>
        </div>
      ) : (
        <div className="sp-recs-grid">
          {recommendations.map((rec) => (
            <div key={rec.id} className={`sp-rec-card ${rec.status.toLowerCase()}`}>
              <div className="sp-rec-header">
                <div>
                  <div className="sp-rec-badges">
                    <span className={`sp-priority-pill ${rec.priority.toLowerCase()}`}>
                      {rec.priority} Priority
                    </span>
                    <span className={`sp-status-pill-badge ${rec.status.toLowerCase()}`}>
                      {rec.status}
                    </span>
                  </div>
                  <h3 className="sp-rec-title">{rec.topic_title || "Proposed Course Module"}</h3>
                </div>

                <div className="sp-rec-actions">
                  {rec.status !== "APPROVED" && (
                    <button
                      className="sp-btn-action approve"
                      title="Approve for Course Syllabus"
                      onClick={() => handleStatusChange(rec.id, "APPROVED")}
                    >
                      <Check size={16} /> Approve
                    </button>
                  )}
                  {rec.status !== "REJECTED" && (
                    <button
                      className="sp-btn-action reject"
                      title="Reject Proposal"
                      onClick={() => handleStatusChange(rec.id, "REJECTED")}
                    >
                      <X size={16} /> Reject
                    </button>
                  )}
                </div>
              </div>

              <p className="sp-rec-desc">{rec.recommendation_text}</p>

              {/* Learning Outcomes */}
              {rec.learning_outcomes && rec.learning_outcomes.length > 0 && (
                <div className="sp-rec-section">
                  <div className="sp-rec-sec-title">
                    <Target size={14} /> Measurable Learning Outcomes:
                  </div>
                  <ul className="sp-rec-list">
                    {rec.learning_outcomes.map((lo, idx) => (
                      <li key={idx}>{lo}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Practical Exercises */}
              {rec.practical_exercises && rec.practical_exercises.length > 0 && (
                <div className="sp-rec-section">
                  <div className="sp-rec-sec-title">
                    <Layers size={14} /> Practical Workshop & Lab Exercises:
                  </div>
                  <ul className="sp-rec-list">
                    {rec.practical_exercises.map((pe, idx) => (
                      <li key={idx}>{pe}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Evidence Rationale */}
              {rec.rationale && (
                <div className="sp-rec-rationale">
                  <strong>Market Evidence:</strong> {rec.rationale}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
