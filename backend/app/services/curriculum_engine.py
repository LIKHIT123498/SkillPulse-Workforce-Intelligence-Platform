"""
Curriculum Recommendation Engine: Generates grounded, evidence-backed curriculum
modernization proposals for Board of Studies (BoS) and university CSE faculties (PRD Module 3).
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.models.gap_analysis import SkillGapReport, Recommendation
from app.models.course import Course
from app.models.skill import Skill

# Knowledge base of syllabus modules and learning outcomes for modern Computer Science & Engineering
CURRICULUM_KNOWLEDGE_BASE = {
    "Docker": {
        "title": "Lab Module: Containerization & Microservice Deployment with Docker",
        "description": "Hands-on containerization fundamentals, multi-stage builds, and local service orchestration.",
        "outcomes": [
            "Write production-grade multi-stage Dockerfiles optimizing image size and security.",
            "Orchestrate multi-container microservice environments using Docker Compose.",
            "Implement container health checks, network isolation, and volume persistence."
        ],
        "exercises": [
            "Lab 1: Containerize a decoupled FastAPI backend and PostgreSQL database with persistent volumes.",
            "Lab 2: Implement automated container image vulnerability scanning in a local build."
        ]
    },
    "Kubernetes": {
        "title": "Elective Unit: Cloud-Native Orchestration with Kubernetes",
        "description": "Production container management, declarative manifests, autoscaling, and service routing.",
        "outcomes": [
            "Deploy and scale stateful and stateless applications using Pods, Deployments, and StatefulSets.",
            "Configure Ingress controllers, ClusterIP, and NodePort services for microservice routing.",
            "Manage configuration secrets and automated rolling update deployments with zero downtime."
        ],
        "exercises": [
            "Lab: Deploy a 3-replica microservice cluster with Horizontal Pod Autoscaler (HPA) using Minikube.",
            "Workshop: Configure Helm charts for automated multi-environment staging deployments."
        ]
    },
    "Generative AI & LLMs": {
        "title": "Emerging Tech Unit: Generative AI, Retrieval-Augmented Generation & LLM Engineering",
        "description": "Building production AI agents, vector database indexing, and semantic search pipelines.",
        "outcomes": [
            "Understand Transformer self-attention architecture, tokenization, and temperature sampling.",
            "Implement Retrieval-Augmented Generation (RAG) pipelines using LangChain / LlamaIndex.",
            "Index and query dense vector embeddings using ChromaDB, Pinecone, or pgvector."
        ],
        "exercises": [
            "Capstone Project: Build an AI-assisted University Course QA Agent using document embeddings and RAG.",
            "Lab: Evaluate hallucination benchmarks and implement guardrails for structured JSON generation."
        ]
    },
    "System Design & Microservices": {
        "title": "Core Module: Scalable System Design & Distributed Microservice Architecture",
        "description": "High-level architectural patterns, horizontal scaling, caching strategies, and CAP theorem trade-offs.",
        "outcomes": [
            "Design fault-tolerant distributed architectures supporting 10k+ concurrent requests.",
            "Apply CQRS (Command Query Responsibility Segregation) and event-driven asynchronous messaging.",
            "Implement rate-limiting, circuit-breaker patterns, and distributed consensus mechanisms."
        ],
        "exercises": [
            "Design Workshop: Architectural blueprint for a high-concurrency payment gateway or URL shortener.",
            "Lab: Implement Redis distributed locks and token-bucket rate limiting."
        ]
    },
    "CI/CD Pipelines": {
        "title": "Industry Practice: DevSecOps & Automated CI/CD Pipelines",
        "description": "Continuous Integration, automated test verification, and automated cloud delivery.",
        "outcomes": [
            "Construct automated GitHub Actions workflows triggering on PR and branch merges.",
            "Incorporate automated unit testing, linting (oxlint/ruff), and coverage thresholds.",
            "Deploy build artifacts to AWS / cloud container registries upon successful pipeline execution."
        ],
        "exercises": [
            "Lab: Build an end-to-end GitHub Actions workflow deploying to cloud upon passing integration tests."
        ]
    },
    "PostgreSQL": {
        "title": "Advanced DBMS Unit: Relational Query Optimization & Indexing in PostgreSQL",
        "description": "Deep dive into execution plans, B-tree/GIN indexing, ACID concurrency, and connection pooling.",
        "outcomes": [
            "Analyze and optimize complex SQL queries using EXPLAIN ANALYZE execution trees.",
            "Implement partitioning, composite indexes, and full-text search vectors.",
            "Configure transaction isolation levels to prevent race conditions and dirty reads."
        ],
        "exercises": [
            "Lab: Benchmark a 1-million row query and optimize latency from 450ms to 8ms using indexing.",
            "Workshop: Configure connection pooling with PgBouncer."
        ]
    },
    "Next.js": {
        "title": "Modern Web Unit: Server-Side Rendering & Full-Stack React with Next.js",
        "description": "App Router architecture, React Server Components (RSC), and Edge runtime deployments.",
        "outcomes": [
            "Architect performant web applications utilizing Server and Client Component boundaries.",
            "Implement Server Actions for type-safe database mutations without boilerplate APIs.",
            "Optimize Core Web Vitals, dynamic Open Graph tags, and streaming SSR."
        ],
        "exercises": [
            "Project: Develop a real-time collaborative engineering portal using Next.js App Router."
        ]
    },
    "FastAPI": {
        "title": "Backend Engineering: High-Throughput Asynchronous APIs with FastAPI",
        "description": "Modern Python backend development with Pydantic v2 validation and async I/O.",
        "outcomes": [
            "Build asynchronous REST endpoints with non-blocking database queries.",
            "Implement dependency injection patterns for authentication, database sessions, and caching.",
            "Auto-generate OpenAPI (Swagger) specifications with comprehensive schema validation."
        ],
        "exercises": [
            "Lab: Build a high-throughput telemetry ingestion microservice handling 5,000 req/sec."
        ]
    },
    "Redis": {
        "title": "Distributed Systems: In-Memory Caching & Session Management with Redis",
        "description": "Cache-aside strategies, TTL invalidation, distributed locks, and pub/sub messaging.",
        "outcomes": [
            "Design multi-tier caching architectures with write-through and cache-aside patterns.",
            "Implement distributed rate limiters and session storage.",
            "Prevent cache stampede and cache penetration using bloom filters."
        ],
        "exercises": [
            "Lab: Implement sub-millisecond API response caching for an e-commerce catalog."
        ]
    },
    "Kafka": {
        "title": "Distributed Systems: Event Streaming & Message Queues with Apache Kafka",
        "description": "Event-driven microservices, consumer groups, partition offsets, and message durability.",
        "outcomes": [
            "Design pub/sub event topologies for decoupled microservice architectures.",
            "Manage consumer group rebalancing, partition keys, and offset commit strategies.",
            "Handle dead-letter queues and idempotent message processing."
        ],
        "exercises": [
            "Lab: Build an asynchronous order notification pipeline using Kafka producers and consumers."
        ]
    }
}

def generate_curriculum_recommendations(db: Session, report_id: int) -> List[Recommendation]:
    """
    Generates actionable, grounded curriculum recommendations for all missing
    competencies identified in a skill gap report for Board of Studies (BoS) review.
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

        # Evidence-backed rationale grounded in calculated data
        rationale = (
            f"Required in {demand_count} verified Indian Tech Hub job postings for '{report.target_role}'. "
            f"Currently {coverage_level.lower()} in '{course.course_name}'. "
            f"Incorporating this unit is projected to increase graduate curriculum alignment by approximately +{potential_boost}%."
        )

        # Retrieve knowledge base template or generate dynamic module
        if canonical_name in CURRICULUM_KNOWLEDGE_BASE:
            kb = CURRICULUM_KNOWLEDGE_BASE[canonical_name]
            topic_title = kb["title"]
            rec_text = kb["description"]
            outcomes = kb["outcomes"]
            exercises = kb["exercises"]
        else:
            topic_title = f"Module: Applied {canonical_name} & Industry Tooling"
            rec_text = f"Incorporate hands-on laboratory exercises, architectural design principles, and modern industry tooling for {canonical_name}."
            outcomes = [
                f"Master core principles, modern software frameworks, and industry best practices for {canonical_name}.",
                f"Design and implement production-ready solutions using {canonical_name}.",
                f"Perform automated testing, benchmarking, and code quality evaluations for {canonical_name}."
            ]
            exercises = [
                f"Hands-on Lab: Build a practical, test-driven application applying {canonical_name}.",
                f"Capstone Assignment: Deploy an end-to-end software module showcasing {canonical_name}."
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
    """Updates Board of Studies (BoS) faculty review status (PENDING, APPROVED, REJECTED)."""
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
