"""
Skill Matcher: Extracts skills and competencies from unstructured job descriptions
and academic syllabi using hybrid taxonomy-grounded regex patterns and conceptual semantic mapping.
"""
import re
from typing import Dict, List, Set, Any
from app.ml.nlp_pipeline import TextPreprocessor
from app.services.skill_normalization import SYNONYM_TAXONOMY, SkillNormalizer

# Conceptual syllabus patterns: maps academic curriculum phrases to industry competency nodes
CONCEPTUAL_SYLLABUS_MAP = [
    (re.compile(r"(?:distributed consensus|virtualization|hypervisor|multi-tenant architecture)", re.IGNORECASE), "Cloud Computing", "Cloud & Infrastructure"),
    (re.compile(r"(?:acid transactions|b\+ trees|relational algebra|query optimization|er modeling|normalization 3nf)", re.IGNORECASE), "Database Management Systems", "Core CS"),
    (re.compile(r"(?:osi (?:7 )?layers?|tcp/ip stack|sliding window|routing protocols?|socket programming|subnetting)", re.IGNORECASE), "Computer Networks", "Core CS"),
    (re.compile(r"(?:process synchronization|virtual memory|paging algorithms?|deadlock detection|cpu scheduling)", re.IGNORECASE), "Operating Systems", "Core CS"),
    (re.compile(r"(?:supervised regression|gradient descent|backpropagation|cost function optimization|decision tree learning)", re.IGNORECASE), "Machine Learning", "AI/ML"),
    (re.compile(r"(?:automated build pipelines?|continuous delivery|continuous integration|integration triggers?)", re.IGNORECASE), "CI/CD Pipelines", "DevOps"),
    (re.compile(r"(?:asymptotic complexity|dynamic programming|divide and conquer|graph traversals?|binary search trees?)", re.IGNORECASE), "Data Structures & Algorithms", "Core CS"),
    (re.compile(r"(?:polymorphism|inheritance|encapsulation|design patterns?|solid principles)", re.IGNORECASE), "Object-Oriented Programming", "Core CS"),
    (re.compile(r"(?:retrieval augmented|vector embeddings?|cosine similarity search|prompt engineering|context retrieval)", re.IGNORECASE), "RAG Systems", "AI/ML"),
    (re.compile(r"(?:service mesh|api gateway|decoupled microservices|event-driven architecture|distributed cache)", re.IGNORECASE), "System Design & Microservices", "Architecture"),
]

class SkillExtractor:
    """Extracts, normalizes, and ranks skills from unstructured job descriptions and university syllabi."""
    
    def __init__(self):
        # Precompile regex patterns for each known alias to ensure strict word boundaries
        sorted_aliases = sorted(SYNONYM_TAXONOMY.keys(), key=lambda x: len(x), reverse=True)
        self.patterns = []
        for alias in sorted_aliases:
            escaped = re.escape(alias)
            pattern = re.compile(rf"(?<![a-zA-Z0-9_]){escaped}(?![a-zA-Z0-9_])", re.IGNORECASE)
            self.patterns.append((alias, pattern))

    def extract_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Extracts all canonical skills from raw job or syllabus text.
        Returns a list of extracted skills with canonical name, category, confidence, and frequency.
        """
        if not text:
            return []

        # 1. Segment text into sections
        sections = TextPreprocessor.segment_sections(text)
        
        extracted_skills: Dict[str, Dict[str, Any]] = {}

        # Weights by section type
        section_weights = {
            "requirements": 1.0,
            "preferred": 0.6,
            "responsibilities": 0.8,
            "general": 0.7
        }

        # 2. Pattern matching across sections for explicit tool / technology mentions
        for sec_name, content in sections.items():
            if not content.strip():
                continue
            
            weight = section_weights.get(sec_name, 0.7)
            
            for alias, pattern in self.patterns:
                matches = pattern.findall(content)
                if matches:
                    norm = SkillNormalizer.normalize(alias)
                    if norm:
                        canon_name, category = norm
                        if canon_name not in extracted_skills:
                            extracted_skills[canon_name] = {
                                "skill_name": canon_name,
                                "canonical_name": canon_name,
                                "category": category,
                                "frequency": 0,
                                "importance": weight,
                                "sections_found": set(),
                                "match_type": "EXACT_TOOL"
                            }
                        extracted_skills[canon_name]["frequency"] += len(matches)
                        extracted_skills[canon_name]["sections_found"].add(sec_name)
                        extracted_skills[canon_name]["importance"] = max(
                            extracted_skills[canon_name]["importance"], weight
                        )

        # 3. Layer in Hybrid Conceptual Matching for Academic Course Descriptions
        full_cleaned = TextPreprocessor.clean_text(text)
        for pattern, canon_name, category in CONCEPTUAL_SYLLABUS_MAP:
            concept_matches = pattern.findall(full_cleaned)
            if concept_matches:
                if canon_name not in extracted_skills:
                    extracted_skills[canon_name] = {
                        "skill_name": canon_name,
                        "canonical_name": canon_name,
                        "category": category,
                        "frequency": len(concept_matches),
                        "importance": 0.85,
                        "sections_found": {"curriculum_module"},
                        "match_type": "CONCEPTUAL_SEMANTIC"
                    }
                else:
                    extracted_skills[canon_name]["frequency"] += len(concept_matches)
                    extracted_skills[canon_name]["importance"] = max(
                        extracted_skills[canon_name]["importance"], 0.85
                    )

        # Convert set to list for JSON serialization
        results = []
        for s in extracted_skills.values():
            s_copy = dict(s)
            s_copy["sections_found"] = sorted(list(s_copy["sections_found"]))
            results.append(s_copy)

        # Sort by importance and frequency
        results.sort(key=lambda x: (x["importance"], x["frequency"]), reverse=True)
        return results

# Singleton instance for high performance
skill_extractor = SkillExtractor()
