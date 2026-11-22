"""
Analytics Service: Computes skill demand aggregations, sector breakdowns,
geographical distribution across Maharashtra districts, and emerging trends.
"""
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models.job import JobPosting, JobSkill
from app.models.skill import Skill
from app.models.location import District

def get_market_overview(db: Session) -> Dict[str, Any]:
    """Provides high-level platform KPIs for the dashboard."""
    total_jobs = db.query(JobPosting).count()
    total_skills = db.query(Skill).count()
    total_districts_covered = (
        db.query(JobPosting.district_id)
        .filter(JobPosting.district_id.isnot(None))
        .distinct()
        .count()
    )
    
    # Top 5 most demanded skills overall
    top_skills_query = (
        db.query(Skill.canonical_name, func.count(JobSkill.job_id).label("count"))
        .join(JobSkill, Skill.id == JobSkill.skill_id)
        .group_by(Skill.canonical_name)
        .order_by(desc("count"))
        .limit(5)
        .all()
    )
    top_skills = [{"skill": s[0], "count": s[1]} for s in top_skills_query]

    # Sector breakdown
    sectors_query = (
        db.query(JobPosting.sector, func.count(JobPosting.id).label("count"))
        .group_by(JobPosting.sector)
        .order_by(desc("count"))
        .all()
    )
    sector_distribution = [{"sector": sec[0] or "Other", "jobs_count": sec[1]} for sec in sectors_query]

    return {
        "total_jobs_analyzed": total_jobs,
        "unique_skills_identified": total_skills,
        "districts_covered": total_districts_covered,
        "top_demanded_skills": top_skills,
        "sector_distribution": sector_distribution
    }

def get_skill_demand_by_sector(db: Session, sector: str = None) -> List[Dict[str, Any]]:
    """Retrieves top skills demanded within a specific industry sector or across all sectors."""
    query = (
        db.query(
            JobPosting.sector,
            Skill.canonical_name,
            Skill.category,
            func.count(JobSkill.job_id).label("demand_count")
        )
        .join(JobSkill, JobPosting.id == JobSkill.job_id)
        .join(Skill, JobSkill.skill_id == Skill.id)
    )
    if sector:
        query = query.filter(JobPosting.sector.ilike(f"%{sector}%"))
    
    results = (
        query.group_by(JobPosting.sector, Skill.canonical_name, Skill.category)
        .order_by(desc("demand_count"))
        .limit(50)
        .all()
    )
    return [
        {
            "sector": r[0] or "General",
            "skill": r[1],
            "category": r[2],
            "demand_count": r[3]
        }
        for r in results
    ]

def get_district_demand_distribution(db: Session) -> List[Dict[str, Any]]:
    """Aggregates job and skill demand across Maharashtra districts."""
    results = (
        db.query(
            District.district_name,
            func.count(JobPosting.id).label("jobs_count")
        )
        .join(JobPosting, District.id == JobPosting.district_id)
        .group_by(District.district_name)
        .order_by(desc("jobs_count"))
        .all()
    )
    return [{"district": r[0], "jobs_count": r[1]} for r in results]
