from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import relationship
from app.database.session import Base

class SkillGapReport(Base):
    __tablename__ = "skill_gap_reports"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    target_role = Column(String(150), nullable=False)
    alignment_score = Column(Float, nullable=False) # (Covered / Total Required) * 100
    missing_skills = Column(JSON, nullable=True)    # List of missing skill names
    partially_covered_skills = Column(JSON, nullable=True)
    generated_at = Column(DateTime, server_default=func.now())

    course = relationship("Course")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
    recommendation_text = Column(Text, nullable=False) # Grounded syllabus upgrade suggestion
    status = Column(String(50), default="PENDING")     # PENDING, APPROVED, REJECTED
    created_at = Column(DateTime, server_default=func.now())

    course = relationship("Course")
    skill = relationship("Skill")