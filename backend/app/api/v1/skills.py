from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.session import get_db
from app.models.skill import Skill
from app.models.job import JobSkill
from app.schemas.skill import SkillResponse, SkillCreate

router = APIRouter(prefix="/skills", tags=["Skills & Taxonomy"])

@router.get("", response_model=List[SkillResponse])
def get_skills(
    category: Optional[str] = Query(None, description="Filter by skill category"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Skill)
    if category:
        query = query.filter(Skill.category.ilike(category))
    return query.offset(skip).limit(limit).all()

@router.post("", response_model=SkillResponse)
def create_skill(skill_in: SkillCreate, db: Session = Depends(get_db)):
    skill = Skill(
        skill_name=skill_in.skill_name,
        canonical_name=skill_in.canonical_name or skill_in.skill_name,
        category=skill_in.category or "General"
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill

@router.get("/top-demanded")
def get_top_demanded_skills(limit: int = 10, db: Session = Depends(get_db)):
    """Calculates top demanded skills across all ingested job postings."""
    results = (
        db.query(Skill.skill_name, Skill.category, func.count(JobSkill.job_id).label("demand_count"))
        .join(JobSkill, Skill.id == JobSkill.skill_id)
        .group_by(Skill.id)
        .order_by(func.count(JobSkill.job_id).desc())
        .limit(limit)
        .all()
    )
    return [{"skill": r[0], "category": r[1], "demand_count": r[2]} for r in results]
