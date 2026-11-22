from typing import Optional
from pydantic import BaseModel

class SkillBase(BaseModel):
    skill_name: str
    canonical_name: Optional[str] = None
    category: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: int

    class Config:
        from_attributes = True
