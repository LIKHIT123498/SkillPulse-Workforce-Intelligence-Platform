from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import relationship
from app.database.session import Base

class SkillGapReport(Base):
    __tablename__ = "skill_gap_reports"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    target_role = Column(String(150), nullable=False, index=True)
    alignment_score = Column(Float, nullable=False) # (Covered / Total Required) * 100
    covered_skills = Column(JSON, nullable=True)    # [{skill: str, weight: float, level: str}]
    missing_skills = Column(JSON, nullable=True)    # [{skill: str, weight: float, demand_count: int}]
    partially_covered_skills = Column(JSON, nullable=True)
    detailed_breakdown = Column(JSON, nullable=True)
    generated_at = Column(DateTime, server_default=func.now())

    course = relationship("Course")
    recommendations = relationship("Recommendation", back_populates="gap_report", cascade="all, delete-orphan")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    gap_report_id = Column(Integer, ForeignKey("skill_gap_reports.id", ondelete="CASCADE"), nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
    
    topic_title = Column(String(200), nullable=True)
    recommendation_text = Column(Text, nullable=False) # Grounded syllabus upgrade suggestion
    learning_outcomes = Column(JSON, nullable=True)    # Specific measurable learning outcomes
    practical_exercises = Column(JSON, nullable=True)  # Lab / workshop tasks
    rationale = Column(Text, nullable=True)            # Evidence backing this change
    priority = Column(String(50), default="HIGH")      # HIGH, MEDIUM, LOW
    status = Column(String(50), default="PENDING")     # PENDING, APPROVED, REJECTED
    created_at = Column(DateTime, server_default=func.now())

    gap_report = relationship("SkillGapReport", back_populates="recommendations")
    course = relationship("Course")
    skill = relationship("Skill")
