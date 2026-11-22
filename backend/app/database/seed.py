"""
Seed script to pre-populate Maharashtra districts, foundational skill taxonomy,
and representative ITI/vocational courses as specified in PRD Section 8 & 14.
"""
from sqlalchemy.orm import Session
from app.database.session import SessionLocal, engine, Base
import app.models  # Register all models
from app.models.location import District
from app.models.skill import Skill
from app.models.course import Course, CourseSkill

MAHARASHTRA_DISTRICTS = [
    "Ahmednagar", "Akola", "Amravati", "Chhatrapati Sambhajinagar", "Beed",
    "Bhandara", "Buldhana", "Chandrapur", "Dhule", "Gadchiroli", "Gondia",
    "Hingoli", "Jalgaon", "Jalna", "Kolhapur", "Latur", "Mumbai City",
    "Mumbai Suburban", "Nagpur", "Nanded", "Nandurbar", "Nashik", "Dharashiv",
    "Parbhani", "Pune", "Raigad", "Ratnagiri", "Sangli", "Satara",
    "Sindhudurg", "Solapur", "Thane", "Wardha", "Washim", "Yavatmal", "Palghar"
]

FOUNDATIONAL_SKILLS = [
    # Technical / IT Skills
    {"skill_name": "Python", "canonical_name": "Python", "category": "Programming"},
    {"skill_name": "SQL", "canonical_name": "SQL", "category": "Database"},
    {"skill_name": "JavaScript", "canonical_name": "JavaScript", "category": "Programming"},
    {"skill_name": "React", "canonical_name": "React", "category": "Web Development"},
    {"skill_name": "HTML/CSS", "canonical_name": "HTML/CSS", "category": "Web Development"},
    {"skill_name": "Machine Learning", "canonical_name": "Machine Learning", "category": "AI/ML"},
    {"skill_name": "Data Analysis", "canonical_name": "Data Analysis", "category": "Analytics"},
    {"skill_name": "Cloud Computing", "canonical_name": "Cloud Computing", "category": "Infrastructure"},
    {"skill_name": "Docker", "canonical_name": "Docker", "category": "DevOps"},
    {"skill_name": "Git", "canonical_name": "Git", "category": "Tools"},
    
    # Manufacturing / Engineering / ITI Skills
    {"skill_name": "CNC Programming", "canonical_name": "CNC Machining", "category": "Manufacturing"},
    {"skill_name": "CNC Milling", "canonical_name": "CNC Machining", "category": "Manufacturing"},
    {"skill_name": "Industrial Automation", "canonical_name": "Industrial Automation", "category": "Manufacturing"},
    {"skill_name": "PLC Programming", "canonical_name": "PLC Programming", "category": "Electrical"},
    {"skill_name": "Industrial Wiring", "canonical_name": "Industrial Wiring", "category": "Electrical"},
    {"skill_name": "TIG/MIG Welding", "canonical_name": "Welding", "category": "Mechanical"},
    {"skill_name": "AutoCAD", "canonical_name": "AutoCAD", "category": "Design"},
    {"skill_name": "Quality Inspection", "canonical_name": "Quality Control", "category": "Quality"},
    {"skill_name": "Electrical Maintenance", "canonical_name": "Electrical Maintenance", "category": "Electrical"},
    {"skill_name": "Inventory Management", "canonical_name": "Logistics", "category": "Supply Chain"},

    # Soft / Foundational Skills
    {"skill_name": "Communication Skills", "canonical_name": "Communication", "category": "Soft Skills"},
    {"skill_name": "Problem Solving", "canonical_name": "Problem Solving", "category": "Soft Skills"},
    {"skill_name": "Industrial Safety (OSHA)", "canonical_name": "Workplace Safety", "category": "Safety"},
]

SAMPLE_COURSES = [
    {
        "course_name": "Computer Operator and Programming Assistant (COPA)",
        "qualification": "National Trade Certificate (NTC)",
        "institution": "Government ITI, Aundh, Pune",
        "district": "Pune",
        "skills": ["HTML/CSS", "JavaScript", "SQL", "Communication Skills"]
    },
    {
        "course_name": "Electrician Trade",
        "qualification": "National Trade Certificate (NTC)",
        "institution": "Government ITI, Nagpur",
        "district": "Nagpur",
        "skills": ["Industrial Wiring", "Electrical Maintenance", "Workplace Safety"]
    },
    {
        "course_name": "Machinist & CNC Operator",
        "qualification": "National Trade Certificate (NTC)",
        "institution": "Government ITI, Nashik",
        "district": "Nashik",
        "skills": ["CNC Machining", "AutoCAD", "Quality Control", "Workplace Safety"]
    },
    {
        "course_name": "Diploma in Computer Technology",
        "qualification": "Polytechnic Diploma",
        "institution": "Government Polytechnic, Mumbai",
        "district": "Mumbai City",
        "skills": ["Python", "SQL", "HTML/CSS", "JavaScript", "Git"]
    }
]

def seed_database(db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True

    try:
        # 1. Seed Districts
        print("Seeding Maharashtra Districts...")
        district_map = {}
        for d_name in MAHARASHTRA_DISTRICTS:
            district = db.query(District).filter(District.district_name == d_name).first()
            if not district:
                district = District(district_name=d_name, state="Maharashtra")
                db.add(district)
                db.flush()
            district_map[d_name] = district.id

        # 2. Seed Skills
        print("Seeding Foundational Skill Taxonomy...")
        skill_map = {}
        for s in FOUNDATIONAL_SKILLS:
            skill = db.query(Skill).filter(Skill.skill_name == s["skill_name"]).first()
            if not skill:
                skill = Skill(
                    skill_name=s["skill_name"],
                    canonical_name=s["canonical_name"],
                    category=s["category"]
                )
                db.add(skill)
                db.flush()
            skill_map[s["skill_name"]] = skill.id
            skill_map[s["canonical_name"]] = skill.id

        # 3. Seed Courses
        print("Seeding Sample ITI / Vocational Courses...")
        for c in SAMPLE_COURSES:
            course = db.query(Course).filter(Course.course_name == c["course_name"]).first()
            if not course:
                course = Course(
                    course_name=c["course_name"],
                    qualification=c["qualification"],
                    institution=c["institution"],
                    district_id=district_map.get(c["district"])
                )
                db.add(course)
                db.flush()

                # Add Course Skills
                for skill_name in c["skills"]:
                    s_id = skill_map.get(skill_name)
                    if s_id:
                        cs = CourseSkill(course_id=course.id, skill_id=s_id, coverage_level="COVERED")
                        db.add(cs)

        db.commit()
        print("Database successfully seeded with districts, skills, and courses!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        if own_session:
            db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_database()
