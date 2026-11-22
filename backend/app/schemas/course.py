from typing import List, Optional
from pydantic import BaseModel
from app.schemas.skill import SkillResponse

class CourseSkillCreate(BaseModel):
    skill_name: str
    coverage_level: str = "COVERED" # COVERED, PARTIALLY_COVERED

class CourseSkillResponse(BaseModel):
    id: int
    coverage_level: str
    skill: SkillResponse

    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    course_name: str
    qualification: Optional[str] = None
    institution: Optional[str] = None
    district_name: Optional[str] = None
    skills: List[str] = []

class CourseResponse(BaseModel):
    id: int
    course_name: str
    qualification: Optional[str]
    institution: Optional[str]
    district_id: Optional[int]
    covered_skills: List[CourseSkillResponse] = []

    class Config:
        from_attributes = True
