from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="candidate") # admin, institution, employer, candidate
    created_at = Column(DateTime, server_default=func.now())

class EmployerSurvey(Base):
    __tablename__ = "employer_surveys"

    id = Column(Integer, primary_key=True, index=True)
    employer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_role = Column(String(150), nullable=False, index=True)
    submitted_at = Column(DateTime, server_default=func.now())

    employer = relationship("User")
    survey_skills = relationship("SurveySkill", back_populates="survey", cascade="all, delete-orphan")

class SurveySkill(Base):
    __tablename__ = "survey_skills"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("employer_surveys.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    proficiency = Column(String(50), nullable=True) # Beginner, Intermediate, Advanced

    survey = relationship("EmployerSurvey", back_populates="survey_skills")
    skill = relationship("Skill")

class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)

    user = relationship("User")
    district = relationship("District")
    candidate_skills = relationship("CandidateSkill", back_populates="candidate", cascade="all, delete-orphan")

class CandidateSkill(Base):
    __tablename__ = "candidate_skills"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    proficiency = Column(String(50), nullable=True)

    candidate = relationship("CandidateProfile", back_populates="candidate_skills")
    skill = relationship("Skill")
