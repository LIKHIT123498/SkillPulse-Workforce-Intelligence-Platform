from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.course import Course, CourseSkill
from app.models.skill import Skill
from app.models.location import District
from app.schemas.course import CourseResponse, CourseCreate

router = APIRouter(prefix="/courses", tags=["Courses & Curricula"])

@router.get("", response_model=List[CourseResponse])
def get_courses(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Course).offset(skip).limit(limit).all()

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("", response_model=CourseResponse)
def create_course(course_in: CourseCreate, db: Session = Depends(get_db)):
    district_id = None
    if course_in.district_name:
        dist = db.query(District).filter(District.district_name.ilike(course_in.district_name)).first()
        if dist:
            district_id = dist.id

    course = Course(
        course_name=course_in.course_name,
        qualification=course_in.qualification,
        institution=course_in.institution,
        district_id=district_id
    )
    db.add(course)
    db.flush()

    for s_name in course_in.skills:
        skill = db.query(Skill).filter(Skill.skill_name.ilike(s_name.strip())).first()
        if not skill:
            skill = Skill(skill_name=s_name.strip(), canonical_name=s_name.strip(), category="General")
            db.add(skill)
            db.flush()
        cs = CourseSkill(course_id=course.id, skill_id=skill.id, coverage_level="COVERED")
        db.add(cs)

    db.commit()
    db.refresh(course)
    return course
