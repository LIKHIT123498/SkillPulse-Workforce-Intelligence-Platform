"""
Curriculum Recommendation Engine: Generates grounded, evidence-backed curriculum
modernization proposals based on detected skill gaps and market demand (PRD Module 3).
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.models.gap_analysis import SkillGapReport, Recommendation
from app.models.course import Course
from app.models.skill import Skill

# Knowledge base of syllabus modules and learning outcomes for key technical/vocational competencies
CURRICULUM_KNOWLEDGE_BASE = {
    "Machine Learning": {
        "title": "Module: Fundamentals of Applied Machine Learning",
        "description": "Introduce foundational supervised and unsupervised ML workflows using Python scikit-learn.",
        "outcomes": [
            "Prepare, normalize, and split dataset features for predictive modeling.",
            "Implement linear regression, classification trees, and clustering algorithms.",
            "Evaluate model performance using accuracy, precision, recall, and ROC curves."
        ],
        "exercises": [
            "Hands-on lab: Predict industrial equipment failure times using sensor telemetry datasets.",
            "Workshop: End-to-end model pipeline deployment with FastAPI."
        ]
    },
    "Data Analysis": {
        "title": "Module: Exploratory Data Analysis & Business Intelligence",
        "description": "Practical data wrangling, statistical aggregation, and interactive dashboard creation.",
        "outcomes": [
            "Import and clean real-world tabular data using Pandas and NumPy.",
            "Write complex SQL group-by and window functions for business analytics.",
            "Construct clear visualization dashboards using Tableau or PowerBI."
        ],
        "exercises": [
            "Lab exercise: Clean and analyze district-level manufacturing output data.",
            "Case study: Present quarterly operational metrics to stakeholders."
        ]
    },
    "Cloud Computing": {
        "title": "Module: Cloud Infrastructure & Deployment Fundamentals",
        "description": "Introduction to cloud hosting, virtual machines, containerization, and serverless compute.",
        "outcomes": [
            "Configure cloud virtual machines, VPC networking, and security firewalls.",
            "Containerize web services using Docker for uniform runtime environments.",
            "Deploy containerized microservices to managed cloud services."
        ],
        "exercises": [
            "Lab: Containerize a Python/FastAPI web API with Docker and deploy to cloud VM.",
            "Workshop: Configure automated health checks and log monitoring."
        ]
    },
    "Docker": {
        "title": "Module: Containerization with Docker & DevOps Practices",
        "description": "Building reproducible software environments and CI/CD basics.",
        "outcomes": [
            "Write multi-stage Dockerfiles for optimized container images.",
            "Manage multi-container applications using docker-compose.",
            "Understand CI/CD pipeline triggers and artifact publishing."
        ],
        "exercises": [
            "Hands-on: Write Dockerfile and docker-compose.yml for backend + database setup."
        ]
    },
    "PLC Programming": {
        "title": "Module: Industrial PLC Programming & Ladder Logic",
        "description": "Programming, wiring, and troubleshooting Programmable Logic Controllers in manufacturing lines.",
        "outcomes": [
            "Design ladder logic diagrams for sequential industrial automation processes.",
            "Interface digital and analog sensors/actuators with industrial PLC racks.",
            "Diagnose wiring faults and signal latency in production automation lines."
        ],
        "exercises": [
            "Workshop: Program a bottle-capping conveyor line simulation using Siemens/Allen-Bradley PLC.",
            "Lab: Debug relay failure and emergency stop interlock circuits."
        ]
    },
    "CNC Machining": {
        "title": "Module: Advanced CNC Programming & Multi-Axis Machining",
        "description": "G-code/M-code programming, CNC lathe/milling operations, and tool calibration.",
        "outcomes": [
            "Generate accurate 3-axis CNC toolpaths from CAD drawings.",
            "Calibrate spindle feeds, speeds, and workpiece zero offsets.",
            "Inspect machined parts against engineering tolerances with micrometer gauges."
        ],
        "exercises": [
            "Workshop: Mill a precision automotive flange bracket to ±0.02mm tolerance.",
            "Lab: Tool wear compensation and emergency stop procedure drill."
        ]
    },
    "Industrial Automation": {
        "title": "Module: SCADA & Industrial Automation Systems",
        "description": "Supervisory control, data acquisition, and human-machine interface (HMI) integration.",
        "outcomes": [
            "Configure SCADA graphic displays and real-time operational tags.",
            "Connect plant telemetry through Modbus/Industrial Ethernet protocols.",
            "Implement automated warning thresholds and alarm acknowledgement logs."
        ],
        "exercises": [
            "Lab: Build an interactive HMI screen for monitoring boiler temperature and pressure."
        ]
    },
    "React": {
        "title": "Module: Modern Frontend Development with React",
        "description": "Component-driven single page application development with TypeScript and state management.",
        "outcomes": [
            "Build reusable interactive UI components with React hooks and TypeScript.",
            "Manage asynchronous REST API state and data caching.",
            "Design responsive layouts using Tailwind CSS."
        ],
        "exercises": [
            "Project: Build a real-time job application tracking portal with responsive design."
        ]
    }
}

def generate_curriculum_recommendations(db: Session, report_id: int) -> List[Recommendation]:
    """
    Generates actionable, grounded curriculum recommendations for all missing
    competencies identified in a skill gap report.
    """
    report = db.query(SkillGapReport).filter(SkillGapReport.id == report_id).first()
    if not report:
        raise ValueError(f"Skill gap report {report_id} not found")

    course = db.query(Course).filter(Course.id == report.course_id).first()
    if not course:
        raise ValueError("Associated course not found")

    missing_skills = report.missing_skills or []
    partially_covered = report.partially_covered_skills or []
    all_gaps = missing_skills + partially_covered

    recommendations_created = []

    # Calculate potential alignment gain per skill
    total_gaps = len(all_gaps)
    potential_boost = round((100.0 - report.alignment_score) / max(total_gaps, 1), 1)

    for item in all_gaps:
        canonical_name = item.get("canonical_name") or item.get("skill_name")
        demand_count = item.get("demand_count", 1)
        importance_weight = item.get("importance_weight", 1.0)
        coverage_level = item.get("coverage_level", "MISSING")

        # Find skill in database
        skill = db.query(Skill).filter(
            (Skill.canonical_name.ilike(canonical_name)) | (Skill.skill_name.ilike(canonical_name))
        ).first()
        skill_id = skill.id if skill else None

        # Determine priority
        if importance_weight >= 0.7 or demand_count >= 3:
            priority = "HIGH"
        elif importance_weight >= 0.4 or demand_count >= 2:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        # Rationale grounded in calculated data
        rationale = (
            f"Required in {demand_count} verified job postings for '{report.target_role}'. "
            f"Currently {coverage_level.lower()} in '{course.course_name}'. "
            f"Adopting this unit increases curriculum alignment by approximately +{potential_boost}%."
        )

        # Retrieve knowledge base template or generate dynamic module
        if canonical_name in CURRICULUM_KNOWLEDGE_BASE:
            kb = CURRICULUM_KNOWLEDGE_BASE[canonical_name]
            topic_title = kb["title"]
            rec_text = kb["description"]
            outcomes = kb["outcomes"]
            exercises = kb["exercises"]
        else:
            topic_title = f"Module: Applied {canonical_name} Competency"
            rec_text = f"Incorporate hands-on training and theoretical principles of {canonical_name} into the curriculum."
            outcomes = [
                f"Understand core principles, industry standards, and tooling for {canonical_name}.",
                f"Apply {canonical_name} to solve industry-standard practical problems.",
                f"Follow safety, documentation, and quality guidelines for {canonical_name}."
            ]
            exercises = [
                f"Practical lab: Introductory workflow and tooling exercises for {canonical_name}.",
                f"Applied project: Real-world task demonstrating proficiency in {canonical_name}."
            ]

        # Check if recommendation already exists for this report and skill
        existing = db.query(Recommendation).filter(
            Recommendation.gap_report_id == report.id,
            Recommendation.skill_id == skill_id
        ).first()

        if not existing:
            rec = Recommendation(
                gap_report_id=report.id,
                course_id=course.id,
                skill_id=skill_id,
                topic_title=topic_title,
                recommendation_text=rec_text,
                learning_outcomes=outcomes,
                practical_exercises=exercises,
                rationale=rationale,
                priority=priority,
                status="PENDING"
            )
            db.add(rec)
            recommendations_created.append(rec)
        else:
            recommendations_created.append(existing)

    db.commit()
    for r in recommendations_created:
        db.refresh(r)

    return recommendations_created

def update_recommendation_status(db: Session, rec_id: int, new_status: str) -> Recommendation:
    """Updates administrative approval status (PENDING, APPROVED, REJECTED)."""
    rec = db.query(Recommendation).filter(Recommendation.id == rec_id).first()
    if not rec:
        raise ValueError(f"Recommendation {rec_id} not found")
    valid_statuses = ["PENDING", "APPROVED", "REJECTED"]
    clean_status = new_status.upper().strip()
    if clean_status not in valid_statuses:
        raise ValueError(f"Status must be one of {valid_statuses}")
    
    rec.status = clean_status
    db.commit()
    db.refresh(rec)
    return rec
