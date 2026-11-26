"""
Skill Gap Analysis Service: Implements deterministic, weighted competency alignment
between training course curricula and industry labour-market demand (PRD Module 2).
"""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.course import Course, CourseSkill
from app.models.job import JobPosting, JobSkill
from app.models.skill import Skill
from app.models.gap_analysis import SkillGapReport
from app.services.skill_normalization import SkillNormalizer

def calculate_skill_gap(db: Session, course_id: int, target_role: str) -> SkillGapReport:
    """
    Compares the competencies covered by an existing course against the industry requirements
    for a target job role. Computes a deterministic weighted alignment score and stores the report.
    """
    # 1. Retrieve the course
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise ValueError(f"Course with ID {course_id} not found")

    # 2. Retrieve Course Skills (Canonicalized)
    course_skills_query = (
        db.query(Skill.canonical_name, Skill.skill_name, CourseSkill.coverage_level)
        .join(CourseSkill, Skill.id == CourseSkill.skill_id)
        .filter(CourseSkill.course_id == course_id)
        .all()
    )
    
    course_skills_map: Dict[str, str] = {}
    for canon, sname, level in course_skills_query:
        norm_key = (canon or sname).strip().lower()
        course_skills_map[norm_key] = level or "COVERED"

    # 3. Retrieve Industry Required Skills for target role
    # Query job postings matching the target role (title or sector)
    jobs_query = db.query(JobPosting).filter(JobPosting.title.ilike(f"%{target_role}%")).all()
    if not jobs_query:
        # Fallback: broaden search by words in target role
        words = [w for w in target_role.split() if len(w) > 3]
        if words:
            filters = [JobPosting.title.ilike(f"%{w}%") for w in words]
            from sqlalchemy import or_
            jobs_query = db.query(JobPosting).filter(or_(*filters)).all()

    # If still no jobs matched, take all jobs in the closest sector
    if not jobs_query:
        jobs_query = db.query(JobPosting).limit(10).all()

    job_ids = [j.id for j in jobs_query]

    # Aggregate required skills from matching jobs
    required_skills_query = (
        db.query(
            Skill.id,
            Skill.skill_name,
            Skill.canonical_name,
            Skill.category,
            func.count(JobSkill.job_id).label("freq"),
            func.avg(JobSkill.importance).label("avg_importance")
        )
        .join(JobSkill, Skill.id == JobSkill.skill_id)
        .filter(JobSkill.job_id.in_(job_ids))
        .group_by(Skill.id, Skill.skill_name, Skill.canonical_name, Skill.category)
        .all()
    )

    if not required_skills_query:
        # If no skills mapped in jobs, query top general skills
        required_skills_query = (
            db.query(
                Skill.id,
                Skill.skill_name,
                Skill.canonical_name,
                Skill.category,
                func.count(JobSkill.job_id).label("freq"),
                func.avg(JobSkill.importance).label("avg_importance")
            )
            .join(JobSkill, Skill.id == JobSkill.skill_id)
            .group_by(Skill.id, Skill.skill_name, Skill.canonical_name, Skill.category)
            .limit(6)
            .all()
        )

    # 4. Perform Weighted Alignment Scoring
    total_weighted_points = 0.0
    covered_weighted_points = 0.0

    covered_list = []
    partial_list = []
    missing_list = []
    detailed_breakdown = []

    # Calculate max frequency for relative weight scaling
    max_freq = max([r[4] for r in required_skills_query], default=1) or 1

    for s_id, s_name, canon_name, category, freq, avg_imp in required_skills_query:
        canonical = canon_name or s_name
        norm_key = canonical.strip().lower()
        
        # Skill weight combines market demand frequency and role importance
        raw_weight = (freq / max_freq) * (avg_imp or 1.0)
        skill_weight = round(raw_weight, 2)
        total_weighted_points += skill_weight

        skill_detail = {
            "skill_name": s_name,
            "canonical_name": canonical,
            "category": category or "General",
            "importance_weight": skill_weight,
            "demand_count": freq
        }

        # Check coverage against course syllabus
        if norm_key in course_skills_map:
            cov_level = course_skills_map[norm_key]
            if cov_level == "COVERED":
                covered_weighted_points += skill_weight
                skill_detail["coverage_level"] = "COVERED"
                covered_list.append(skill_detail)
            else:
                # Partially covered counts as 50%
                covered_weighted_points += (skill_weight * 0.5)
                skill_detail["coverage_level"] = "PARTIALLY_COVERED"
                partial_list.append(skill_detail)
        else:
            skill_detail["coverage_level"] = "MISSING"
            missing_list.append(skill_detail)

        detailed_breakdown.append(skill_detail)

    # 5. Calculate Final Score (Percentage 0.0 - 100.0)
    if total_weighted_points > 0:
        alignment_score = round((covered_weighted_points / total_weighted_points) * 100, 1)
    else:
        alignment_score = 0.0

    # Sort missing skills by importance descending
    missing_list.sort(key=lambda x: (x["importance_weight"], x["demand_count"]), reverse=True)

    # 6. Save Report to Database
    report = SkillGapReport(
        course_id=course.id,
        target_role=target_role,
        alignment_score=alignment_score,
        covered_skills=covered_list,
        partially_covered_skills=partial_list,
        missing_skills=missing_list,
        detailed_breakdown=detailed_breakdown
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return report
