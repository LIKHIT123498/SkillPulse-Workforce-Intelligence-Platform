/**
 * SkillPulse API Client: Connects React frontend with the FastAPI backend.
 */
const API_BASE = "http://127.0.0.1:8000/api/v1";

async function request(endpoint, options = {}) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {})
      },
      ...options
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || "API request failed");
    }
    return await res.json();
  } catch (err) {
    console.error(`API Error on ${endpoint}:`, err);
    throw err;
  }
}

export const api = {
  // System Health
  checkHealth: () => request("/health"),

  // Analytics & KPIs
  getOverview: () => request("/analytics/overview"),
  getSectorSkills: (sector) => request(`/analytics/skills${sector ? `?sector=${encodeURIComponent(sector)}` : ""}`),
  getDistrictDemand: () => request("/analytics/districts"),

  // Jobs
  getJobs: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return request(`/jobs${query ? `?${query}` : ""}`);
  },
  importJobsCsv: async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch(`${API_BASE}/jobs/import`, {
      method: "POST",
      body: formData
    });
    return await res.json();
  },

  // Skills & NLP
  getSkills: () => request("/skills"),
  getTopDemandedSkills: (limit = 10) => request(`/skills/top-demanded?limit=${limit}`),
  extractSkills: (text) => request("/skills/extract", {
    method: "POST",
    body: JSON.stringify({ text })
  }),

  // Courses
  getCourses: () => request("/courses"),

  // Districts
  getDistricts: () => request("/districts"),

  // Skill Gap Analysis
  runGapAnalysis: (courseId, targetRole) => request("/analysis/skill-gap", {
    method: "POST",
    body: JSON.stringify({ course_id: courseId, target_role: targetRole })
  }),
  getGapReport: (id) => request(`/analysis/${id}`),

  // Curriculum Recommendations
  getRecommendations: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return request(`/recommendations${query ? `?${query}` : ""}`);
  },
  updateRecommendationStatus: (id, status) => request(`/recommendations/${id}`, {
    method: "PATCH",
    body: JSON.stringify({ status })
  })
};
