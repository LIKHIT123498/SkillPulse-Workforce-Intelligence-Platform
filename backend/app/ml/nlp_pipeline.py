"""
NLP Pipeline: Text Preprocessing and Section Segmentation for Job Descriptions.
"""
import re
import html
import unicodedata
from typing import Dict, List, Tuple

class TextPreprocessor:
    """Preprocesses and normalizes raw, unstructured job descriptions."""
    
    # Section header patterns common in Indian and global job postings
    SECTION_PATTERNS = {
        "requirements": re.compile(r"(?:requirements|required\s+skills|qualifications|what\s+you\s+need|must\s+have|eligibility|prerequisites)[:\n]", re.IGNORECASE),
        "responsibilities": re.compile(r"(?:responsibilities|key\s+responsibilities|role|duties|what\s+you\s+will\s+do|job\s+scope)[:\n]", re.IGNORECASE),
        "preferred": re.compile(r"(?:preferred|nice\s+to\s+have|good\s+to\s+have|bonus|desired\s+skills)[:\n]", re.IGNORECASE),
    }

    @staticmethod
    def clean_text(text: str) -> str:
        """Removes HTML tags, normalizes whitespace and standardizes special characters."""
        if not text:
            return ""
        
        # 1. Unescape HTML entities (e.g. &amp;, &lt;)
        text = html.unescape(text)
        
        # 2. Strip HTML tags if present
        text = re.sub(r"<[^>]+>", " ", text)
        
        # 3. Standardize unicode characters
        text = unicodedata.normalize("NFKD", text)
        
        # 4. Standardize bullets and punctuation
        text = re.sub(r"[\u2022\u2023\u25E6\u2043\u2219•·\*\-]", " ", text)
        
        # 5. Normalize multiple spaces, tabs, and newlines
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n\s*\n+", "\n", text)
        
        return text.strip()

    @classmethod
    def segment_sections(cls, text: str) -> Dict[str, str]:
        """Segments text into requirements, responsibilities, and general content."""
        cleaned = cls.clean_text(text)
        sections = {"general": cleaned, "requirements": "", "preferred": "", "responsibilities": ""}
        
        # Find positions of all matched section headers
        matches: List[Tuple[str, int, int]] = []
        for sec_name, pattern in cls.SECTION_PATTERNS.items():
            for m in pattern.finditer(cleaned):
                matches.append((sec_name, m.start(), m.end()))
        
        # Sort by start offset
        matches.sort(key=lambda x: x[1])
        
        if not matches:
            sections["requirements"] = cleaned
            return sections
        
        # Split text into segments
        for i, (name, start, end) in enumerate(matches):
            next_start = matches[i+1][1] if i + 1 < len(matches) else len(cleaned)
            content = cleaned[end:next_start].strip()
            if content:
                sections[name] = sections.get(name, "") + " " + content
                
        return sections

    @staticmethod
    def extract_ngrams(tokens: List[str], n: int) -> List[str]:
        """Generates n-grams from a list of tokens."""
        return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
