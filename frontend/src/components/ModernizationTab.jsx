import React, { useState, useEffect } from "react";
import { api } from "../services/api";
import { Sparkles, Check, X, BookOpen, Target, Layers, GraduationCap } from "lucide-react";

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
            <GraduationCap size={20} className="text-purple" />
            Board of Studies (BoS) Curriculum Modernization Portal (PRD Module 3)
          </div>
          <div className="sp-filter-bar">
            <select
              className="sp-select"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="">All Review Statuses</option>
              <option value="PENDING">Pending Faculty Review</option>
              <option value="APPROVED">Approved for Syllabus Rollout</option>
              <option value="REJECTED">Archived / Rejected</option>
            </select>
          </div>
        </div>
        <p className="sp-card-desc">
          Evidence-backed curriculum modernisation proposals synthesized from detected software industry skill deficits. Board of Studies (BoS) members, university faculty, and academic directors can review, endorse, or archive proposed laboratory modules and theory units.
        </p>
      </div>

      {loading ? (
        <div className="sp-loading-spinner">Loading BoS curriculum modernization proposals...</div>
      ) : recommendations.length === 0 ? (
        <div className="sp-card sp-empty-card">
          <BookOpen size={40} className="sp-empty-icon" />
          <h3>No Curriculum Proposals Available</h3>
          <p>Run a Curriculum Gap Audit on a university syllabus to generate actionable modernization units.</p>
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
                      {rec.status === "APPROVED" ? "BoS Approved" : rec.status}
                    </span>
                  </div>
                  <h3 className="sp-rec-title">{rec.topic_title || "Proposed Academic Module"}</h3>
                </div>

                <div className="sp-rec-actions">
                  {rec.status !== "APPROVED" && (
                    <button
                      className="sp-btn-action approve"
                      title="Endorse for University Syllabus (BoS)"
                      onClick={() => handleStatusChange(rec.id, "APPROVED")}
                    >
                      <Check size={16} /> Approve (BoS)
                    </button>
                  )}
                  {rec.status !== "REJECTED" && (
                    <button
                      className="sp-btn-action reject"
                      title="Archive / Reject Proposal"
                      onClick={() => handleStatusChange(rec.id, "REJECTED")}
                    >
                      <X size={16} /> Archive
                    </button>
                  )}
                </div>
              </div>

              <p className="sp-rec-desc">{rec.recommendation_text}</p>

              {/* Measurable Learning Outcomes */}
              {rec.learning_outcomes && rec.learning_outcomes.length > 0 && (
                <div className="sp-rec-section">
                  <div className="sp-rec-sec-title">
                    <Target size={14} /> Course Outcomes (COs) & Measurable Objectives:
                  </div>
                  <ul className="sp-rec-list">
                    {rec.learning_outcomes.map((lo, idx) => (
                      <li key={idx}>{lo}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Practical Hands-on Exercises */}
              {rec.practical_exercises && rec.practical_exercises.length > 0 && (
                <div className="sp-rec-section">
                  <div className="sp-rec-sec-title">
                    <Layers size={14} /> Laboratory Curriculum & Hands-on Workshop Assignments:
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
                  <strong>Academic & Industry Evidence:</strong> {rec.rationale}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
