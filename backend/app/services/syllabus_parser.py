"""
Syllabus Parser Service: Ingests university syllabus PDFs (VTU, Mumbai University, SPPU, AKTU, etc.),
extracts course structure, modules, Course Outcomes (COs), and runs hybrid skill extraction to populate CourseSkills.
"""
import io
import re
from typing import Dict, Any, List
import pypdf
from sqlalchemy.orm import Session

from app.models.course import Course, CourseSkill
from app.models.skill import Skill
from app.ml.skill_matcher import skill_extractor
from app.services.skill_normalization import SkillNormalizer

def parse_syllabus_pdf(pdf_bytes: bytes) -> Dict[str, Any]:
    """Reads PDF bytes using pypdf and extracts structured text, modules, and Course Outcomes."""
    reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
    full_text_pages = []
    for idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        full_text_pages.append(page_text)

    full_text = "\n".join(full_text_pages)

    # 1. Detect Course Code & Name
    # Patterns: e.g. "BCS501: Software Engineering", "Course Title: Cloud Computing", "Subject Code: CS401"
    course_code_match = re.search(r"\b([A-Z]{2,4}\d{3,4}[A-Z]?)\b", full_text)
    course_code = course_code_match.group(1) if course_code_match else "CSE-SPEC"

    # Search for course title near course code or headers
    title_match = re.search(r"(?:Course Title|Subject|Name of the Course)[:\s]+([^\n\r]{4,80})", full_text, re.IGNORECASE)
    if title_match:
        course_name = f"{course_code}: {title_match.group(1).strip()}"
    else:
        # Fallback title from first page non-empty lines
        first_lines = [l.strip() for l in full_text_pages[0].split("\n") if len(l.strip()) > 5][:5]
        course_name = f"{course_code}: {first_lines[0]}" if first_lines else f"{course_code}: Computer Science Course"

    # 2. Extract Course Outcomes (COs)
    # e.g., "CO1: Understand...", "CO2: Implement..."
    co_matches = re.findall(r"\b(CO\d+[:\s]+[^\n\r]{10,150})", full_text)
    course_outcomes = [c.strip() for c in co_matches][:6]

    # 3. Extract Syllabus Modules / Units
    # e.g., "Module-1", "Unit I", "Module 2:"
    module_matches = re.findall(r"\b(?:Module|Unit)[\s\-]+([1-5|I|V|X]+)[:\s]+([^\n\r]{5,80})", full_text, re.IGNORECASE)
    modules = [f"Unit {m[0]}: {m[1].strip()}" for m in module_matches][:6]

    return {
        "course_name": course_name,
        "course_code": course_code,
        "total_pages": len(reader.pages),
        "full_text": full_text,
        "course_outcomes": course_outcomes,
        "modules": modules
    }

def ingest_syllabus_pdf(db: Session, pdf_bytes: bytes, institution: str = "Technical University", qualification: str = "B.Tech CSE") -> Dict[str, Any]:
    """Parses a university syllabus PDF and persists the Course and CourseSkill records."""
    parsed = parse_syllabus_pdf(pdf_bytes)
    
    # Run hybrid skill extractor across full syllabus text
    extracted_skills = skill_extractor.extract_from_text(parsed["full_text"])

    # Create Course Record
    course = Course(
        course_name=parsed["course_name"],
        qualification=qualification,
        institution=institution
    )
    db.add(course)
    db.flush()

    saved_skills = []
    for item in extracted_skills:
        canonical_name = item["canonical_name"]
        cat = item["category"]
        importance = item.get("importance", 0.7)
        coverage_level = "COVERED" if importance >= 0.8 else "PARTIALLY_COVERED"

        # Check or create Skill
        skill = db.query(Skill).filter(
            (Skill.canonical_name.ilike(canonical_name)) | (Skill.skill_name.ilike(canonical_name))
        ).first()

        if not skill:
            skill = Skill(skill_name=canonical_name, canonical_name=canonical_name, category=cat)
            db.add(skill)
            db.flush()

        # Add CourseSkill association
        cs = CourseSkill(
            course_id=course.id,
            skill_id=skill.id,
            coverage_level=coverage_level
        )
        db.add(cs)
        saved_skills.append({
            "skill_name": canonical_name,
            "category": cat,
            "coverage_level": coverage_level,
            "importance": importance
        })

    db.commit()
    db.refresh(course)

    return {
        "course_id": course.id,
        "course_name": course.course_name,
        "qualification": course.qualification,
        "institution": course.institution,
        "total_skills_mapped": len(saved_skills),
        "skills": saved_skills,
        "course_outcomes": parsed["course_outcomes"],
        "modules": parsed["modules"]
    }
