from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.gap_analysis import Recommendation
from app.schemas.gap_analysis import RecommendationResponse, RecommendationStatusUpdate
from app.services.curriculum_engine import generate_curriculum_recommendations, update_recommendation_status

router = APIRouter(prefix="/recommendations", tags=["Curriculum Recommendations"])

@router.post("/generate/{report_id}", response_model=List[RecommendationResponse])
def generate_recommendations(report_id: int, db: Session = Depends(get_db)):
    """Generates structured, actionable curriculum modernization proposals for a gap report."""
    try:
        return generate_curriculum_recommendations(db, report_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("", response_model=List[RecommendationResponse])
def get_recommendations(
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    status: Optional[str] = Query(None, description="Filter by status: PENDING, APPROVED, REJECTED"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Retrieves curriculum modernization recommendations."""
    query = db.query(Recommendation)
    if course_id:
        query = query.filter(Recommendation.course_id == course_id)
    if status:
        query = query.filter(Recommendation.status == status.upper())
    return query.order_by(Recommendation.created_at.desc()).offset(skip).limit(limit).all()

@router.patch("/{rec_id}", response_model=RecommendationResponse)
def update_status(rec_id: int, payload: RecommendationStatusUpdate, db: Session = Depends(get_db)):
    """Updates approval status of a curriculum modernization recommendation."""
    try:
        return update_recommendation_status(db, rec_id, payload.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
