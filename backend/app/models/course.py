from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database.session import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(200), nullable=False, index=True)
    qualification = Column(String(100)) # ITI Certificate, Diploma, Degree
    institution = Column(String(200))   # e.g., ITI Aundh Pune, Govt Polytechnic
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    covered_skills = relationship("CourseSkill", back_populates="course", cascade="all, delete-orphan")

class CourseSkill(Base):
    __tablename__ = "course_skills"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    coverage_level = Column(String(50), default="COVERED") # COVERED, PARTIALLY_COVERED

    course = relationship("Course", back_populates="covered_skills")
    skill = relationship("Skill", back_populates="course_associations")