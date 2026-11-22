"""
Skill Matcher: Extracts skills and competencies from unstructured job descriptions
using taxonomy-grounded regex patterns and multi-tier n-gram matching.
"""
import re
from typing import Dict, List, Set, Any
from app.ml.nlp_pipeline import TextPreprocessor
from app.services.skill_normalization import SYNONYM_TAXONOMY, SkillNormalizer

class SkillExtractor:
    """Extracts, normalizes, and ranks skills from unstructured job descriptions."""
    
    def __init__(self):
        # Precompile regex patterns for each known alias to ensure strict word boundaries
        # Sort by length descending so longer phrases match first ("cloud computing" before "cloud")
        sorted_aliases = sorted(SYNONYM_TAXONOMY.keys(), key=lambda x: len(x), reverse=True)
        self.patterns = []
        for alias in sorted_aliases:
            # Escape special characters (e.g. c++, html/css, node.js)
            escaped = re.escape(alias)
            # Match strictly on word boundaries or non-alphanumeric boundaries
            pattern = re.compile(rf"(?<![a-zA-Z0-9_]){escaped}(?![a-zA-Z0-9_])", re.IGNORECASE)
            self.patterns.append((alias, pattern))

    def extract_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Extracts all canonical skills from raw job text.
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

        # 2. Pattern matching across sections
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
                                "sections_found": set()
                            }
                        extracted_skills[canon_name]["frequency"] += len(matches)
                        extracted_skills[canon_name]["sections_found"].add(sec_name)
                        extracted_skills[canon_name]["importance"] = max(
                            extracted_skills[canon_name]["importance"], weight
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
