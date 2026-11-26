from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class SkillGapRequest(BaseModel):
    course_id: int
    target_role: str

class SkillCoverageDetail(BaseModel):
    skill_name: str
    canonical_name: str
    category: str
    importance_weight: float
    coverage_level: str  # COVERED, PARTIALLY_COVERED, MISSING
    demand_count: int = 1

class RecommendationResponse(BaseModel):
    id: int
    course_id: int
    skill_id: Optional[int] = None
    topic_title: Optional[str] = None
    recommendation_text: str
    learning_outcomes: Optional[List[str]] = []
    practical_exercises: Optional[List[str]] = []
    rationale: Optional[str] = None
    priority: str = "HIGH"
    status: str = "PENDING"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RecommendationStatusUpdate(BaseModel):
    status: str  # PENDING, APPROVED, REJECTED

class SkillGapReportResponse(BaseModel):
    id: int
    course_id: int
    course_name: str
    target_role: str
    alignment_score: float
    total_required_skills: int
    total_covered_skills: int
    total_missing_skills: int
    covered_skills: List[SkillCoverageDetail]
    partially_covered_skills: List[SkillCoverageDetail]
    missing_skills: List[SkillCoverageDetail]
    recommendations: List[RecommendationResponse] = []
    generated_at: datetime

    class Config:
        from_attributes = True
