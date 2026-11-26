from fastapi.testclient import TestClient
from app.main import app
from app.ml.nlp_pipeline import TextPreprocessor
from app.services.skill_normalization import SkillNormalizer
from app.ml.skill_matcher import skill_extractor

client = TestClient(app)

def test_text_preprocessor():
    raw_html = "<p>Looking for a <b>Full Stack Engineer</b>.</p><ul><li>Strong Python &amp; SQL skills.</li><li>Experience in React.js</li></ul>"
    cleaned = TextPreprocessor.clean_text(raw_html)
    assert "<" not in cleaned and ">" not in cleaned
    assert "&amp;" not in cleaned
    assert "Python" in cleaned and "SQL" in cleaned
    print("✓ Text Preprocessor: HTML & formatting cleaning verified")

    sectioned_text = """
    About Company:
    Leading industrial manufacturing firm in Pune.
    
    Requirements:
    - 3+ years in CNC Machining and AutoCAD.
    - Solid understanding of Workplace Safety (OSHA).
    
    Responsibilities:
    - Operate 5-axis milling center.
    """
    sections = TextPreprocessor.segment_sections(sectioned_text)
    assert "CNC Machining" in sections["requirements"]
    assert "responsibilities" in sections
    print("✓ Text Preprocessor: Section segmentation verified")

def test_skill_normalization():
    test_cases = [
        ("py", "Python", "Programming"),
        ("python3", "Python", "Programming"),
        ("k8s", "Kubernetes", "DevOps & Containers"),
        ("react.js", "React", "Web Development"),
        ("vmc", "CNC Machining", "Manufacturing"),
        ("tig welding", "Welding", "Mechanical"),
        ("panel wiring", "Industrial Wiring", "Electrical"),
        ("pythn", "Python", "Programming"), # Fuzzy match typo
    ]
    for term, expected_name, expected_cat in test_cases:
        res = SkillNormalizer.normalize(term)
        assert res is not None, f"Failed to normalize {term}"
        assert res[0] == expected_name, f"Expected {expected_name}, got {res[0]} for term {term}"
        assert res[1] == expected_cat, f"Expected {expected_cat}, got {res[1]}"
    print("✓ Skill Normalizer: Synonyms, abbreviations, and fuzzy matching verified")

def test_skill_extraction():
    unstructured_desc = """
    Job Title: Senior Automation & Electrical Technician
    Location: Chhatrapati Sambhajinagar, Maharashtra
    
    We are looking for an experienced technician to join our manufacturing plant.
    Requirements:
    - Extensive hands-on experience in PLC Programming (Siemens/Allen Bradley).
    - Proven expertise in Industrial Wiring and Industrial Automation.
    - Knowledge of electrical maintenance and workplace safety standards.
    - Excellent problem solving and communication skills.
    """
    extracted = skill_extractor.extract_from_text(unstructured_desc)
    extracted_names = [e["canonical_name"] for e in extracted]
    
    assert "PLC Programming" in extracted_names
    assert "Industrial Wiring" in extracted_names
    assert "Industrial Automation" in extracted_names
    assert "Electrical Maintenance" in extracted_names
    assert "Workplace Safety" in extracted_names
    assert "Problem Solving" in extracted_names
    
    # Check section detection and weight
    plc_item = next(e for e in extracted if e["canonical_name"] == "PLC Programming")
    assert "requirements" in plc_item["sections_found"]
    assert plc_item["importance"] >= 0.8
    print(f"✓ Skill Extraction: Successfully extracted {len(extracted)} canonical skills from unstructured job text")

def test_extract_endpoint():
    payload = {
        "text": "Seeking a Data Scientist with skills in Python, Machine Learning, Data Analysis, and SQL database querying."
    }
    res = client.post("/api/v1/skills/extract", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["total_skills_extracted"] >= 4
    extracted_names = [s["canonical_name"] for s in data["skills"]]
    assert "Python" in extracted_names
    assert "Machine Learning" in extracted_names
    assert "SQL" in extracted_names
    print(f"✓ API Endpoint POST /api/v1/skills/extract verified: {extracted_names}")

def test_analytics_endpoints():
    res_overview = client.get("/api/v1/analytics/overview")
    assert res_overview.status_code == 200
    ov = res_overview.json()
    assert ov["total_jobs_analyzed"] > 0
    assert len(ov["top_demanded_skills"]) > 0
    print(f"✓ Analytics Overview verified: {ov['total_jobs_analyzed']} jobs analyzed")

    res_sec = client.get("/api/v1/analytics/skills")
    assert res_sec.status_code == 200
    assert len(res_sec.json()) > 0
    print(f"✓ Sector Skill Demand verified: {len(res_sec.json())} sector skill mappings")

    res_dist = client.get("/api/v1/analytics/districts")
    assert res_dist.status_code == 200
    assert len(res_dist.json()) > 0
    print(f"✓ District Demand Distribution verified: {len(res_dist.json())} districts active")

if __name__ == "__main__":
    test_text_preprocessor()
    test_skill_normalization()
    test_skill_extraction()
    test_extract_endpoint()
    test_analytics_endpoints()
    print("\n🎉 ALL STEP 3 (NLP PIPELINE & ANALYTICS) TESTS PASSED SUCCESSFULLY!")
