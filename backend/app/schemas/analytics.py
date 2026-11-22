from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class SkillExtractRequest(BaseModel):
    text: str

class ExtractedSkillItem(BaseModel):
    skill_name: str
    canonical_name: str
    category: str
    frequency: int
    importance: float
    sections_found: List[str] = []

class SkillExtractResponse(BaseModel):
    text_length: int
    total_skills_extracted: int
    skills: List[ExtractedSkillItem]

class SectorDemandItem(BaseModel):
    sector: str
    skill: str
    category: str
    demand_count: int

class DistrictDemandItem(BaseModel):
    district: str
    jobs_count: int

class OverviewMetricItem(BaseModel):
    skill: str
    count: int

class SectorMetricItem(BaseModel):
    sector: str
    jobs_count: int

class MarketOverviewResponse(BaseModel):
    total_jobs_analyzed: int
    unique_skills_identified: int
    districts_covered: int
    top_demanded_skills: List[OverviewMetricItem]
    sector_distribution: List[SectorMetricItem]
