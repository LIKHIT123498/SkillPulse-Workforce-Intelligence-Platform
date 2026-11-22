from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.schemas.skill import SkillResponse
from app.schemas.district import DistrictResponse

class JobSkillCreate(BaseModel):
    skill_name: str
    importance: float = 1.0
    proficiency: Optional[str] = "Intermediate"

class JobSkillResponse(BaseModel):
    id: int
    importance: float
    proficiency: Optional[str]
    skill: SkillResponse

    class Config:
        from_attributes = True

class JobCreate(BaseModel):
    title: str
    description: str
    company_name: Optional[str] = None
    district_name: Optional[str] = None
    sector: Optional[str] = None
    skills: List[str] = []

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    company_name: Optional[str]
    sector: Optional[str]
    district: Optional[DistrictResponse] = None
    posted_date: Optional[datetime]
    required_skills: List[JobSkillResponse] = []

    class Config:
        from_attributes = True

class JobImportResult(BaseModel):
    total_processed: int
    imported: int
    errors: List[str] = []
