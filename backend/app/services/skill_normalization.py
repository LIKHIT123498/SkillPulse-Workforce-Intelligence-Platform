"""
Skill Normalization Engine: Standardizes variations, synonyms, and abbreviations
into canonical skill entities according to the SkillPulse taxonomy.
"""
from typing import Dict, Optional, Tuple
import difflib

# Canonical taxonomy mapping: alias/variant -> (canonical_name, category)
SYNONYM_TAXONOMY: Dict[str, Tuple[str, str]] = {
    # Software & IT
    "python": ("Python", "Programming"),
    "python3": ("Python", "Programming"),
    "py": ("Python", "Programming"),
    "javascript": ("JavaScript", "Programming"),
    "js": ("JavaScript", "Programming"),
    "ecmascript": ("JavaScript", "Programming"),
    "typescript": ("TypeScript", "Programming"),
    "ts": ("TypeScript", "Programming"),
    "react": ("React", "Web Development"),
    "react.js": ("React", "Web Development"),
    "reactjs": ("React", "Web Development"),
    "node": ("Node.js", "Web Development"),
    "node.js": ("Node.js", "Web Development"),
    "nodejs": ("Node.js", "Web Development"),
    "html": ("HTML/CSS", "Web Development"),
    "css": ("HTML/CSS", "Web Development"),
    "html5": ("HTML/CSS", "Web Development"),
    "css3": ("HTML/CSS", "Web Development"),
    "html/css": ("HTML/CSS", "Web Development"),
    "sql": ("SQL", "Database"),
    "postgresql": ("SQL", "Database"),
    "postgres": ("SQL", "Database"),
    "mysql": ("SQL", "Database"),
    "mongodb": ("MongoDB", "Database"),
    "docker": ("Docker", "DevOps"),
    "docker container": ("Docker", "DevOps"),
    "kubernetes": ("Kubernetes", "DevOps"),
    "k8s": ("Kubernetes", "DevOps"),
    "aws": ("Cloud Computing", "Infrastructure"),
    "amazon web services": ("Cloud Computing", "Infrastructure"),
    "azure": ("Cloud Computing", "Infrastructure"),
    "gcp": ("Cloud Computing", "Infrastructure"),
    "cloud computing": ("Cloud Computing", "Infrastructure"),
    "git": ("Git", "Tools"),
    "github": ("Git", "Tools"),
    "gitlab": ("Git", "Tools"),
    "version control": ("Git", "Tools"),
    
    # AI / Data Science
    "machine learning": ("Machine Learning", "AI/ML"),
    "ml": ("Machine Learning", "AI/ML"),
    "deep learning": ("Machine Learning", "AI/ML"),
    "artificial intelligence": ("Machine Learning", "AI/ML"),
    "ai": ("Machine Learning", "AI/ML"),
    "data analysis": ("Data Analysis", "Analytics"),
    "data analytics": ("Data Analysis", "Analytics"),
    "scikit-learn": ("Machine Learning", "AI/ML"),
    "pandas": ("Data Analysis", "Analytics"),
    "numpy": ("Data Analysis", "Analytics"),
    "tableau": ("Data Visualization", "Analytics"),
    "power bi": ("Data Visualization", "Analytics"),
    "powerbi": ("Data Visualization", "Analytics"),
    "data visualization": ("Data Visualization", "Analytics"),

    # Manufacturing / Engineering / ITI
    "cnc": ("CNC Machining", "Manufacturing"),
    "cnc machining": ("CNC Machining", "Manufacturing"),
    "cnc milling": ("CNC Machining", "Manufacturing"),
    "cnc turning": ("CNC Machining", "Manufacturing"),
    "cnc programming": ("CNC Machining", "Manufacturing"),
    "vmc": ("CNC Machining", "Manufacturing"),
    "plc": ("PLC Programming", "Electrical"),
    "plc programming": ("PLC Programming", "Electrical"),
    "scada": ("Industrial Automation", "Manufacturing"),
    "industrial automation": ("Industrial Automation", "Manufacturing"),
    "wiring": ("Industrial Wiring", "Electrical"),
    "industrial wiring": ("Industrial Wiring", "Electrical"),
    "panel wiring": ("Industrial Wiring", "Electrical"),
    "electrical maintenance": ("Electrical Maintenance", "Electrical"),
    "substation maintenance": ("Electrical Maintenance", "Electrical"),
    "welding": ("Welding", "Mechanical"),
    "tig welding": ("Welding", "Mechanical"),
    "mig welding": ("Welding", "Mechanical"),
    "arc welding": ("Welding", "Mechanical"),
    "autocad": ("AutoCAD", "Design"),
    "cad": ("AutoCAD", "Design"),
    "solidworks": ("CAD/CAM", "Design"),
    "quality control": ("Quality Control", "Quality"),
    "qc": ("Quality Control", "Quality"),
    "qa/qc": ("Quality Control", "Quality"),
    "quality inspection": ("Quality Control", "Quality"),
    "osha": ("Workplace Safety", "Safety"),
    "industrial safety": ("Workplace Safety", "Safety"),
    "workplace safety": ("Workplace Safety", "Safety"),
    "hse": ("Workplace Safety", "Safety"),
    "logistics": ("Logistics", "Supply Chain"),
    "supply chain": ("Logistics", "Supply Chain"),
    "inventory management": ("Logistics", "Supply Chain"),
    "warehouse management": ("Logistics", "Supply Chain"),

    # Soft / Interpersonal Skills
    "communication": ("Communication Skills", "Soft Skills"),
    "communication skills": ("Communication Skills", "Soft Skills"),
    "verbal communication": ("Communication Skills", "Soft Skills"),
    "problem solving": ("Problem Solving", "Soft Skills"),
    "analytical skills": ("Problem Solving", "Soft Skills"),
    "teamwork": ("Team Collaboration", "Soft Skills"),
    "collaboration": ("Team Collaboration", "Soft Skills"),
}

class SkillNormalizer:
    """Normalizes raw terms to canonical skill taxonomy."""

    @classmethod
    def normalize(cls, raw_skill: str) -> Optional[Tuple[str, str]]:
        """
        Normalizes a raw skill string.
        Returns (canonical_name, category) if matched, otherwise None.
        """
        if not raw_skill:
            return None
        
        cleaned = raw_skill.strip().lower()
        
        # 1. Direct dictionary match
        if cleaned in SYNONYM_TAXONOMY:
            return SYNONYM_TAXONOMY[cleaned]
        
        # 2. Strip trailing versions (e.g. 'python 3.9' -> 'python')
        simplified = " ".join([w for w in cleaned.split() if not w.replace(".", "").isdigit()])
        if simplified in SYNONYM_TAXONOMY:
            return SYNONYM_TAXONOMY[simplified]
            
        # 3. Fuzzy similarity fallback (cutoff=0.85)
        closest_matches = difflib.get_close_matches(cleaned, SYNONYM_TAXONOMY.keys(), n=1, cutoff=0.85)
        if closest_matches:
            return SYNONYM_TAXONOMY[closest_matches[0]]
            
        return None
