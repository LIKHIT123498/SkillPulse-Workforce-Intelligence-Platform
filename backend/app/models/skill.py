from sqlalchemy import Column, DateTime,Integer, String, func
from sqlalchemy.orm import relationship
from app.database.session import Base

class Skill(Base):
    __tablename__="skills"
    id=Column(Integer,primary_key=True,index=True)
    skill_name = Column(String(100), unique=True, nullable=False, index=True)
    canonical_name = Column(String(100), index=True) # Normalized name for deduplication
    category = Column(String(50), index=True)        # Technical, Soft, Tool, Framework
    created_at = Column(DateTime, server_default=func.now())
    job_associations = relationship("JobSkill", back_populates="skill")
    course_associations = relationship("CourseSkill", back_populates="skill")