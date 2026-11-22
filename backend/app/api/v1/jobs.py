from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.job import JobPosting
from app.schemas.job import JobResponse, JobImportResult, JobCreate
from app.services.job_ingestion import ingest_jobs_from_csv, ingest_job_record

router = APIRouter(prefix="/jobs", tags=["Jobs & Ingestion"])

@router.get("", response_model=List[JobResponse])
def get_jobs(
    sector: Optional[str] = Query(None, description="Filter by sector"),
    district_id: Optional[int] = Query(None, description="Filter by district ID"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(JobPosting)
    if sector:
        query = query.filter(JobPosting.sector.ilike(f"%{sector}%"))
    if district_id:
        query = query.filter(JobPosting.district_id == district_id)
    return query.offset(skip).limit(limit).all()

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    return job

@router.post("", response_model=JobResponse)
def create_job(job_in: JobCreate, db: Session = Depends(get_db)):
    record = job_in.model_dump()
    job = ingest_job_record(db, record)
    db.commit()
    db.refresh(job)
    return job

@router.post("/import", response_model=JobImportResult)
async def import_jobs_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    content = await file.read()
    csv_text = content.decode("utf-8", errors="ignore")
    result = ingest_jobs_from_csv(db, csv_text)
    return result
