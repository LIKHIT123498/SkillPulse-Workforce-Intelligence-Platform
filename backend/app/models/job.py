from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship
from app.database.session import Base

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False) # Preserves original text for NLP traceability
    company_name = Column(String(150), index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True, index=True)
    sector = Column(String(100), index=True)
    posted_date = Column(DateTime, server_default=func.now())

    district = relationship("District")
    required_skills = relationship("JobSkill", back_populates="job", cascade="all, delete-orphan")

class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    importance = Column(Float, default=1.0) # Weight for gap calculations (0.0 - 1.0)
    proficiency = Column(String(50), nullable=True) # Beginner, Intermediate, Advanced

    job = relationship("JobPosting", back_populates="required_skills")
    skill = relationship("Skill", back_populates="job_associations")