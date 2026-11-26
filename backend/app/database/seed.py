"""
Seed script to pre-populate India's major IT Hiring Hubs, foundational modern software
skill taxonomy, and authentic university B.Tech / B.E. Computer Science & Engineering syllabi.
"""
from sqlalchemy.orm import Session
from app.database.session import SessionLocal, engine, Base
import app.models  # Register all models
from app.models.location import District
from app.models.skill import Skill
from app.models.course import Course, CourseSkill

# India's Major IT / Tech Hiring Hubs & Key Regional Centers
TECH_HUBS_AND_REGIONS = [
    # Top Tier-1 & Tier-2 Indian Tech Hubs
    {"name": "Bengaluru", "state": "Karnataka"},
    {"name": "Hyderabad", "state": "Telangana"},
    {"name": "Pune", "state": "Maharashtra"},
    {"name": "Gurugram", "state": "Haryana"},
    {"name": "Noida", "state": "Uttar Pradesh"},
    {"name": "Chennai", "state": "Tamil Nadu"},
    {"name": "Mumbai", "state": "Maharashtra"},
    {"name": "Mumbai City", "state": "Maharashtra"},
    {"name": "Mumbai Suburban", "state": "Maharashtra"},
    {"name": "Nashik", "state": "Maharashtra"},
    {"name": "Nagpur", "state": "Maharashtra"},
    {"name": "Chhatrapati Sambhajinagar", "state": "Maharashtra"},
    {"name": "Kolkata", "state": "West Bengal"},
    {"name": "Ahmedabad", "state": "Gujarat"},
    {"name": "Kochi", "state": "Kerala"},
    {"name": "Thiruvananthapuram", "state": "Kerala"},
    {"name": "Coimbatore", "state": "Tamil Nadu"},
    {"name": "Indore", "state": "Madhya Pradesh"},
    {"name": "Bhubaneswar", "state": "Odisha"},
    {"name": "Chandigarh", "state": "Punjab / Chandigarh"},
    {"name": "Jaipur", "state": "Rajasthan"},
    {"name": "Thane", "state": "Maharashtra"},
    {"name": "Solapur", "state": "Maharashtra"},
    {"name": "Kolhapur", "state": "Maharashtra"},
    {"name": "Amravati", "state": "Maharashtra"},
    {"name": "Aurangabad", "state": "Maharashtra"},
    {"name": "Ahmednagar", "state": "Maharashtra"},
    {"name": "Akola", "state": "Maharashtra"},
    {"name": "Nanded", "state": "Maharashtra"},
    {"name": "Jalgaon", "state": "Maharashtra"},
    {"name": "Latur", "state": "Maharashtra"},
    {"name": "Dhule", "state": "Maharashtra"},
    {"name": "Sangli", "state": "Maharashtra"},
    {"name": "Satara", "state": "Maharashtra"},
    {"name": "Wardha", "state": "Maharashtra"},
    {"name": "Yavatmal", "state": "Maharashtra"},
    {"name": "Palghar", "state": "Maharashtra"},
    {"name": "Raigad", "state": "Maharashtra"}
]

FOUNDATIONAL_CSE_SKILLS = [
    # Core Languages
    {"skill_name": "Python", "canonical_name": "Python", "category": "Programming"},
    {"skill_name": "Java", "canonical_name": "Java", "category": "Programming"},
    {"skill_name": "C++", "canonical_name": "C++", "category": "Programming"},
    {"skill_name": "JavaScript", "canonical_name": "JavaScript", "category": "Programming"},
    {"skill_name": "TypeScript", "canonical_name": "TypeScript", "category": "Programming"},
    {"skill_name": "Go", "canonical_name": "Go", "category": "Programming"},
    {"skill_name": "Rust", "canonical_name": "Rust", "category": "Programming"},
    {"skill_name": "SQL", "canonical_name": "SQL", "category": "Database"},

    # Modern Web, Frameworks & APIs
    {"skill_name": "React", "canonical_name": "React", "category": "Web Development"},
    {"skill_name": "Next.js", "canonical_name": "Next.js", "category": "Web Development"},
    {"skill_name": "Node.js", "canonical_name": "Node.js", "category": "Web Development"},
    {"skill_name": "FastAPI", "canonical_name": "FastAPI", "category": "Backend"},
    {"skill_name": "Spring Boot", "canonical_name": "Spring Boot", "category": "Backend"},
    {"skill_name": "Django", "canonical_name": "Django", "category": "Backend"},
    {"skill_name": "HTML/CSS", "canonical_name": "HTML/CSS", "category": "Web Development"},
    {"skill_name": "GraphQL", "canonical_name": "GraphQL", "category": "APIs"},
    {"skill_name": "REST APIs", "canonical_name": "REST APIs", "category": "APIs"},

    # Cloud, DevOps & Infrastructure
    {"skill_name": "AWS Cloud", "canonical_name": "AWS Cloud", "category": "Cloud & Infrastructure"},
    {"skill_name": "Cloud Computing", "canonical_name": "Cloud Computing", "category": "Cloud & Infrastructure"},
    {"skill_name": "Docker", "canonical_name": "Docker", "category": "DevOps & Containers"},
    {"skill_name": "Kubernetes", "canonical_name": "Kubernetes", "category": "DevOps & Containers"},
    {"skill_name": "CI/CD Pipelines", "canonical_name": "CI/CD Pipelines", "category": "DevOps"},
    {"skill_name": "Linux/Shell", "canonical_name": "Linux/Shell", "category": "Operating Systems"},
    {"skill_name": "Git", "canonical_name": "Git", "category": "Tools"},

    # Databases, Distributed Systems & Caching
    {"skill_name": "PostgreSQL", "canonical_name": "PostgreSQL", "category": "Database"},
    {"skill_name": "MongoDB", "canonical_name": "MongoDB", "category": "Database"},
    {"skill_name": "Redis", "canonical_name": "Redis", "category": "Distributed Systems"},
    {"skill_name": "Kafka", "canonical_name": "Kafka", "category": "Distributed Systems"},
    {"skill_name": "System Design & Microservices", "canonical_name": "System Design & Microservices", "category": "Architecture"},

    # AI, ML, Data & Generative AI
    {"skill_name": "Machine Learning", "canonical_name": "Machine Learning", "category": "AI/ML"},
    {"skill_name": "Deep Learning", "canonical_name": "Deep Learning", "category": "AI/ML"},
    {"skill_name": "Generative AI & LLMs", "canonical_name": "Generative AI & LLMs", "category": "AI/ML"},
    {"skill_name": "RAG Systems", "canonical_name": "RAG Systems", "category": "AI/ML"},
    {"skill_name": "PyTorch", "canonical_name": "PyTorch", "category": "AI/ML"},
    {"skill_name": "Data Analysis", "canonical_name": "Data Analysis", "category": "Analytics"},

    # Core Computer Science
    {"skill_name": "Data Structures & Algorithms", "canonical_name": "Data Structures & Algorithms", "category": "Core CS"},
    {"skill_name": "Object-Oriented Programming", "canonical_name": "Object-Oriented Programming", "category": "Core CS"},
    {"skill_name": "Operating Systems", "canonical_name": "Operating Systems", "category": "Core CS"},
    {"skill_name": "Computer Networks", "canonical_name": "Computer Networks", "category": "Core CS"},
    {"skill_name": "Database Management Systems", "canonical_name": "Database Management Systems", "category": "Core CS"},
    {"skill_name": "Software Testing", "canonical_name": "Software Testing", "category": "Software Engineering"},
    {"skill_name": "Agile Methodologies", "canonical_name": "Agile Methodologies", "category": "Software Engineering"},

    # Professional & Engineering Practice
    {"skill_name": "Problem Solving", "canonical_name": "Problem Solving", "category": "Soft Skills"},
    {"skill_name": "Communication Skills", "canonical_name": "Communication", "category": "Soft Skills"},
    {"skill_name": "Workplace Safety", "canonical_name": "Workplace Safety", "category": "Safety"},
    {"skill_name": "Quality Control", "canonical_name": "Quality Control", "category": "Quality"},
]

BTECH_CSE_COURSES = [
    {
        "course_name": "VTU 2022 Scheme - BCS501: Software Engineering & Agile Project Management",
        "qualification": "B.Tech Computer Science & Engineering (Semester V)",
        "institution": "Visvesvaraya Technological University (VTU), Belagavi",
        "district": "Bengaluru",
        "skills": ["Object-Oriented Programming", "Software Testing", "Agile Methodologies", "Git", "Problem Solving"]
    },
    {
        "course_name": "Mumbai University - CSC602: Cloud Computing & Virtualization",
        "qualification": "B.E. Computer Engineering (Semester VI)",
        "institution": "University of Mumbai, Vidyanagari Campus",
        "district": "Mumbai",
        "skills": ["Cloud Computing", "Linux/Shell", "Computer Networks", "Operating Systems"]
    },
    {
        "course_name": "SPPU Pune - 310242: Database Management Systems & Relational Modeling",
        "qualification": "B.E. Computer Engineering (Semester V)",
        "institution": "Savitribai Phule Pune University (SPPU)",
        "district": "Pune",
        "skills": ["SQL", "Database Management Systems", "Data Structures & Algorithms", "Problem Solving"]
    },
    {
        "course_name": "AKTU - KCS601: Web Technologies & Full-Stack Development",
        "qualification": "B.Tech Computer Science & Engineering (Semester VI)",
        "institution": "Dr. A.P.J. Abdul Kalam Technical University, Lucknow/Noida",
        "district": "Noida",
        "skills": ["HTML/CSS", "JavaScript", "SQL", "REST APIs", "Git"]
    },
    {
        "course_name": "JNTU Hyderabad - CS401: Applied Machine Learning & Data Analytics",
        "qualification": "B.Tech Computer Science & Engineering (Semester VII)",
        "institution": "Jawaharlal Nehru Technological University, Hyderabad",
        "district": "Hyderabad",
        "skills": ["Python", "Machine Learning", "Data Analysis", "Data Structures & Algorithms"]
    }
]

def seed_database(db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True

    try:
        # 1. Seed Tech Hubs & Districts
        print("Seeding Tech Hubs & Regional Centers...")
        district_map = {}
        for hub in TECH_HUBS_AND_REGIONS:
            district = db.query(District).filter(District.district_name == hub["name"]).first()
            if not district:
                district = District(district_name=hub["name"], state=hub["state"])
                db.add(district)
                db.flush()
            district_map[hub["name"]] = district.id

        # 2. Seed Modern CSE Skill Taxonomy
        print("Seeding Comprehensive Computer Science & Software Taxonomy...")
        skill_map = {}
        for s in FOUNDATIONAL_CSE_SKILLS:
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

        # 3. Seed Authentic BTech CSE University Syllabi
        print("Seeding B.Tech / B.E. Computer Science University Syllabi...")
        for c in BTECH_CSE_COURSES:
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

                # Map Course Competencies
                for skill_name in c["skills"]:
                    s_id = skill_map.get(skill_name)
                    if s_id:
                        cs = CourseSkill(course_id=course.id, skill_id=s_id, coverage_level="COVERED")
                        db.add(cs)

        db.commit()
        print("Database successfully seeded with Tech Hubs, CSE Skills, and University Syllabi!")
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
