"""
Job Ingestion Service: Handles CSV and batch ingestion of job postings,
skill taxonomy mapping, and district normalization with NLP auto-extraction.
"""
import csv
import io
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.models.job import JobPosting, JobSkill
from app.models.location import District
from app.models.skill import Skill
from app.ml.skill_matcher import skill_extractor
from app.services.skill_normalization import SkillNormalizer

def get_or_create_district(db: Session, district_name: str) -> int:
    if not district_name or not district_name.strip():
        return None
    cleaned = district_name.strip().title()
    district = db.query(District).filter(District.district_name.ilike(cleaned)).first()
    if not district:
        district = District(district_name=cleaned, state="Maharashtra")
        db.add(district)
        db.flush()
    return district.id

def get_or_create_skill(db: Session, skill_name: str, category: str = "General") -> int:
    cleaned = skill_name.strip()
    if not cleaned:
        return None
    
    # Check if normalized canonical alias exists
    norm = SkillNormalizer.normalize(cleaned)
    canonical_name = norm[0] if norm else cleaned
    cat = norm[1] if norm else category

    skill = db.query(Skill).filter(
        (Skill.skill_name.ilike(cleaned)) | (Skill.canonical_name.ilike(canonical_name))
    ).first()
    
    if not skill:
        skill = Skill(skill_name=cleaned, canonical_name=canonical_name, category=cat)
        db.add(skill)
        db.flush()
    return skill.id

def ingest_job_record(db: Session, record: Dict[str, Any]) -> JobPosting:
    title = record.get("title", "").strip()
    description = record.get("description", "").strip()
    company_name = record.get("company_name", "").strip()
    sector = record.get("sector", "Other").strip()
    district_name = record.get("district_name") or record.get("location")

    if not title:
        raise ValueError("Job title is required")
    if not description:
        description = f"Job position for {title} at {company_name or 'Industry Partner'}"

    district_id = get_or_create_district(db, district_name) if district_name else None

    job = JobPosting(
        title=title,
        description=description,
        company_name=company_name or None,
        district_id=district_id,
        sector=sector
    )
    db.add(job)
    db.flush()

    # Process skills
    raw_skills = record.get("skills", [])
    if isinstance(raw_skills, str):
        # CSV string of skills separated by commas or pipes
        raw_skills = [s.strip() for s in raw_skills.replace("|", ",").split(",") if s.strip()]

    associated_skill_ids = set()

    # 1. Add provided skills
    for s_name in raw_skills:
        s_id = get_or_create_skill(db, s_name)
        if s_id and s_id not in associated_skill_ids:
            associated_skill_ids.add(s_id)
            job_skill = JobSkill(job_id=job.id, skill_id=s_id, importance=1.0)
            db.add(job_skill)

    # 2. NLP Auto-Extraction fallback or enrichment if skills were sparse
    if len(associated_skill_ids) < 3 and description:
        extracted = skill_extractor.extract_from_text(f"{title} {description}")
        for item in extracted:
            s_id = get_or_create_skill(db, item["canonical_name"], item["category"])
            if s_id and s_id not in associated_skill_ids:
                associated_skill_ids.add(s_id)
                job_skill = JobSkill(job_id=job.id, skill_id=s_id, importance=item["importance"])
                db.add(job_skill)

    return job

def ingest_jobs_from_csv(db: Session, csv_content: str) -> Dict[str, Any]:
    reader = csv.DictReader(io.StringIO(csv_content))
    imported_count = 0
    errors = []

    for idx, row in enumerate(reader, start=1):
        try:
            norm_row = {
                "title": row.get("title") or row.get("job_title") or row.get("Role") or "",
                "description": row.get("description") or row.get("job_description") or "",
                "company_name": row.get("company_name") or row.get("company") or row.get("Company") or "",
                "district_name": row.get("district") or row.get("location") or row.get("City") or "",
                "sector": row.get("sector") or row.get("industry") or "General",
                "skills": row.get("skills") or row.get("required_skills") or row.get("Skills") or ""
            }
            if norm_row["title"]:
                ingest_job_record(db, norm_row)
                imported_count += 1
            else:
                errors.append(f"Row {idx}: Missing job title")
        except Exception as e:
            errors.append(f"Row {idx}: {str(e)}")

    db.commit()
    return {
        "total_processed": imported_count + len(errors),
        "imported": imported_count,
        "errors": errors
    }
