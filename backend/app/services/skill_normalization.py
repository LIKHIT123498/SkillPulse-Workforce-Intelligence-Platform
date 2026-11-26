"""
Skill Normalization Engine: Standardizes variations, synonyms, and abbreviations
into canonical skill entities according to the SkillPulse Computer Science & Tech taxonomy.
"""
from typing import Dict, Optional, Tuple
import difflib

# Canonical taxonomy mapping: alias/variant -> (canonical_name, category)
SYNONYM_TAXONOMY: Dict[str, Tuple[str, str]] = {
    # Core Programming Languages
    "python": ("Python", "Programming"),
    "python3": ("Python", "Programming"),
    "py": ("Python", "Programming"),
    "java": ("Java", "Programming"),
    "core java": ("Java", "Programming"),
    "c++": ("C++", "Programming"),
    "cpp": ("C++", "Programming"),
    "c language": ("C", "Programming"),
    "javascript": ("JavaScript", "Programming"),
    "js": ("JavaScript", "Programming"),
    "ecmascript": ("JavaScript", "Programming"),
    "typescript": ("TypeScript", "Programming"),
    "ts": ("TypeScript", "Programming"),
    "golang": ("Go", "Programming"),
    "go": ("Go", "Programming"),
    "rust": ("Rust", "Programming"),
    "sql": ("SQL", "Database"),
    "structured query language": ("SQL", "Database"),

    # Modern Web Frameworks & Frontend
    "react": ("React", "Web Development"),
    "react.js": ("React", "Web Development"),
    "reactjs": ("React", "Web Development"),
    "next.js": ("Next.js", "Web Development"),
    "nextjs": ("Next.js", "Web Development"),
    "next": ("Next.js", "Web Development"),
    "vue": ("Vue.js", "Web Development"),
    "vue.js": ("Vue.js", "Web Development"),
    "angular": ("Angular", "Web Development"),
    "html": ("HTML/CSS", "Web Development"),
    "css": ("HTML/CSS", "Web Development"),
    "html5": ("HTML/CSS", "Web Development"),
    "css3": ("HTML/CSS", "Web Development"),
    "html/css": ("HTML/CSS", "Web Development"),
    "tailwind": ("Tailwind CSS", "Web Development"),
    "tailwindcss": ("Tailwind CSS", "Web Development"),

    # Backend, Frameworks & APIs
    "node": ("Node.js", "Web Development"),
    "node.js": ("Node.js", "Web Development"),
    "nodejs": ("Node.js", "Web Development"),
    "express": ("Express.js", "Backend"),
    "express.js": ("Express.js", "Backend"),
    "expressjs": ("Express.js", "Backend"),
    "fastapi": ("FastAPI", "Backend"),
    "fast-api": ("FastAPI", "Backend"),
    "django": ("Django", "Backend"),
    "flask": ("Flask", "Backend"),
    "spring": ("Spring Boot", "Backend"),
    "spring boot": ("Spring Boot", "Backend"),
    "springboot": ("Spring Boot", "Backend"),
    "rest": ("REST APIs", "APIs"),
    "rest api": ("REST APIs", "APIs"),
    "rest apis": ("REST APIs", "APIs"),
    "restful apis": ("REST APIs", "APIs"),
    "graphql": ("GraphQL", "APIs"),

    # Databases, Caching & Message Queues
    "postgresql": ("PostgreSQL", "Database"),
    "postgres": ("PostgreSQL", "Database"),
    "psql": ("PostgreSQL", "Database"),
    "mysql": ("SQL", "Database"),
    "mongodb": ("MongoDB", "Database"),
    "mongo": ("MongoDB", "Database"),
    "redis": ("Redis", "Distributed Systems"),
    "kafka": ("Kafka", "Distributed Systems"),
    "apache kafka": ("Kafka", "Distributed Systems"),
    "rabbitmq": ("Distributed Systems", "Distributed Systems"),

    # Cloud, DevOps & Infrastructure
    "docker": ("Docker", "DevOps & Containers"),
    "docker container": ("Docker", "DevOps & Containers"),
    "containerization": ("Docker", "DevOps & Containers"),
    "kubernetes": ("Kubernetes", "DevOps & Containers"),
    "k8s": ("Kubernetes", "DevOps & Containers"),
    "aws": ("AWS Cloud", "Cloud & Infrastructure"),
    "aws cloud": ("AWS Cloud", "Cloud & Infrastructure"),
    "amazon web services": ("AWS Cloud", "Cloud & Infrastructure"),
    "aws ec2": ("AWS Cloud", "Cloud & Infrastructure"),
    "s3": ("AWS Cloud", "Cloud & Infrastructure"),
    "azure": ("Cloud Computing", "Cloud & Infrastructure"),
    "gcp": ("Cloud Computing", "Cloud & Infrastructure"),
    "cloud computing": ("Cloud Computing", "Cloud & Infrastructure"),
    "cloud native": ("Cloud Computing", "Cloud & Infrastructure"),
    "ci/cd": ("CI/CD Pipelines", "DevOps"),
    "cicd": ("CI/CD Pipelines", "DevOps"),
    "github actions": ("CI/CD Pipelines", "DevOps"),
    "jenkins": ("CI/CD Pipelines", "DevOps"),
    "terraform": ("Infrastructure as Code", "DevOps"),
    "linux": ("Linux/Shell", "Operating Systems"),
    "bash": ("Linux/Shell", "Operating Systems"),
    "shell scripting": ("Linux/Shell", "Operating Systems"),
    "git": ("Git", "Tools"),
    "github": ("Git", "Tools"),
    "gitlab": ("Git", "Tools"),

    # AI, ML, Data Science & Generative AI
    "machine learning": ("Machine Learning", "AI/ML"),
    "ml": ("Machine Learning", "AI/ML"),
    "deep learning": ("Deep Learning", "AI/ML"),
    "artificial intelligence": ("Machine Learning", "AI/ML"),
    "ai": ("Machine Learning", "AI/ML"),
    "data analysis": ("Data Analysis", "Analytics"),
    "data analytics": ("Data Analysis", "Analytics"),
    "scikit-learn": ("Machine Learning", "AI/ML"),
    "sklearn": ("Machine Learning", "AI/ML"),
    "pandas": ("Data Analysis", "Analytics"),
    "numpy": ("Data Analysis", "Analytics"),
    "pytorch": ("PyTorch", "AI/ML"),
    "torch": ("PyTorch", "AI/ML"),
    "tensorflow": ("Deep Learning", "AI/ML"),
    "llm": ("Generative AI & LLMs", "AI/ML"),
    "llms": ("Generative AI & LLMs", "AI/ML"),
    "large language models": ("Generative AI & LLMs", "AI/ML"),
    "generative ai": ("Generative AI & LLMs", "AI/ML"),
    "genai": ("Generative AI & LLMs", "AI/ML"),
    "langchain": ("Generative AI & LLMs", "AI/ML"),
    "llamaindex": ("Generative AI & LLMs", "AI/ML"),
    "rag": ("RAG Systems", "AI/ML"),
    "retrieval augmented generation": ("RAG Systems", "AI/ML"),
    "vector database": ("Generative AI & LLMs", "AI/ML"),
    "vector db": ("Generative AI & LLMs", "AI/ML"),
    "chromadb": ("Generative AI & LLMs", "AI/ML"),
    "pinecone": ("Generative AI & LLMs", "AI/ML"),

    # Architecture & Core Computer Science
    "system design": ("System Design & Microservices", "Architecture"),
    "microservices": ("System Design & Microservices", "Architecture"),
    "microservice architecture": ("System Design & Microservices", "Architecture"),
    "hld": ("System Design & Microservices", "Architecture"),
    "lld": ("System Design & Microservices", "Architecture"),
    "data structures": ("Data Structures & Algorithms", "Core CS"),
    "algorithms": ("Data Structures & Algorithms", "Core CS"),
    "dsa": ("Data Structures & Algorithms", "Core CS"),
    "data structures and algorithms": ("Data Structures & Algorithms", "Core CS"),
    "oop": ("Object-Oriented Programming", "Core CS"),
    "oops": ("Object-Oriented Programming", "Core CS"),
    "object-oriented programming": ("Object-Oriented Programming", "Core CS"),
    "operating systems": ("Operating Systems", "Core CS"),
    "os": ("Operating Systems", "Core CS"),
    "computer networks": ("Computer Networks", "Core CS"),
    "networking": ("Computer Networks", "Core CS"),
    "dbms": ("Database Management Systems", "Core CS"),
    "database management systems": ("Database Management Systems", "Core CS"),
    "software testing": ("Software Testing", "Software Engineering"),
    "unit testing": ("Software Testing", "Software Engineering"),
    "agile": ("Agile Methodologies", "Software Engineering"),
    "scrum": ("Agile Methodologies", "Software Engineering"),
    "agile methodologies": ("Agile Methodologies", "Software Engineering"),

    # Manufacturing / Engineering & Legacy Support
    "cnc": ("CNC Machining", "Manufacturing"),
    "cnc machining": ("CNC Machining", "Manufacturing"),
    "vmc": ("CNC Machining", "Manufacturing"),
    "plc": ("PLC Programming", "Electrical"),
    "plc programming": ("PLC Programming", "Electrical"),
    "industrial automation": ("Industrial Automation", "Manufacturing"),
    "industrial wiring": ("Industrial Wiring", "Electrical"),
    "panel wiring": ("Industrial Wiring", "Electrical"),
    "electrical maintenance": ("Electrical Maintenance", "Electrical"),
    "welding": ("Welding", "Mechanical"),
    "tig welding": ("Welding", "Mechanical"),
    "autocad": ("AutoCAD", "Design"),
    "quality control": ("Quality Control", "Quality"),
    "workplace safety": ("Workplace Safety", "Safety"),
    "logistics": ("Logistics", "Supply Chain"),

    # Soft & Interpersonal Skills
    "communication": ("Communication Skills", "Soft Skills"),
    "communication skills": ("Communication Skills", "Soft Skills"),
    "problem solving": ("Problem Solving", "Soft Skills"),
    "analytical skills": ("Problem Solving", "Soft Skills"),
    "teamwork": ("Team Collaboration", "Soft Skills"),
}

class SkillNormalizer:
    """Normalizes raw terms to canonical skill taxonomy."""

    @classmethod
    def normalize(cls, raw_skill: str) -> Optional[Tuple[str, str]]:
        if not raw_skill:
            return None
        cleaned = raw_skill.strip().lower()

        # 1. Direct dictionary match
        if cleaned in SYNONYM_TAXONOMY:
            return SYNONYM_TAXONOMY[cleaned]

        # 2. Strip trailing versions (e.g. 'python 3.12' -> 'python')
        simplified = " ".join([w for w in cleaned.split() if not w.replace(".", "").isdigit()])
        if simplified in SYNONYM_TAXONOMY:
            return SYNONYM_TAXONOMY[simplified]

        # 3. Fuzzy similarity fallback (cutoff=0.85)
        closest_matches = difflib.get_close_matches(cleaned, SYNONYM_TAXONOMY.keys(), n=1, cutoff=0.85)
        if closest_matches:
            return SYNONYM_TAXONOMY[closest_matches[0]]

        return None
