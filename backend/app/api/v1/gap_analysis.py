from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.gap_analysis import SkillGapReport
from app.models.course import Course
from app.schemas.gap_analysis import SkillGapRequest, SkillGapReportResponse
from app.services.gap_analysis import calculate_skill_gap
from app.services.curriculum_engine import generate_curriculum_recommendations

router = APIRouter(prefix="/analysis", tags=["Skill Gap Analysis"])

def format_report_response(report: SkillGapReport, course_name: str) -> dict:
    covered = report.covered_skills or []
    partially = report.partially_covered_skills or []
    missing = report.missing_skills or []
    return {
        "id": report.id,
        "course_id": report.course_id,
        "course_name": course_name,
        "target_role": report.target_role,
        "alignment_score": report.alignment_score,
        "total_required_skills": len(covered) + len(partially) + len(missing),
        "total_covered_skills": len(covered),
        "total_missing_skills": len(missing) + len(partially),
        "covered_skills": covered,
        "partially_covered_skills": partially,
        "missing_skills": missing,
        "recommendations": report.recommendations or [],
        "generated_at": report.generated_at
    }

@router.post("/skill-gap", response_model=SkillGapReportResponse)
def generate_gap_analysis(payload: SkillGapRequest, auto_recommend: bool = True, db: Session = Depends(get_db)):
    """
    Computes deterministic weighted skill alignment between an existing course
    and industry demand for a target job role.
    """
    try:
        report = calculate_skill_gap(db, payload.course_id, payload.target_role)
        if auto_recommend:
            generate_curriculum_recommendations(db, report.id)
            db.refresh(report)
        course = db.query(Course).filter(Course.id == report.course_id).first()
        return format_report_response(report, course.course_name if course else "Unknown")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{report_id}", response_model=SkillGapReportResponse)
def get_gap_report(report_id: int, db: Session = Depends(get_db)):
    """Retrieves an existing skill gap analysis report."""
    report = db.query(SkillGapReport).filter(SkillGapReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Skill gap report not found")
    course = db.query(Course).filter(Course.id == report.course_id).first()
    return format_report_response(report, course.course_name if course else "Unknown")

@router.get("", response_model=List[SkillGapReportResponse])
def list_gap_reports(
    course_id: int = Query(None, description="Filter by course ID"),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Lists recent skill gap reports."""
    query = db.query(SkillGapReport)
    if course_id:
        query = query.filter(SkillGapReport.course_id == course_id)
    reports = query.order_by(SkillGapReport.generated_at.desc()).offset(skip).limit(limit).all()
    
    results = []
    for r in reports:
        course = db.query(Course).filter(Course.id == r.course_id).first()
        results.append(format_report_response(r, course.course_name if course else "Unknown"))
    return results
