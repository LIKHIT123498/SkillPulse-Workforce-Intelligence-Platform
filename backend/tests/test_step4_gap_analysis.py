from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_skill_gap_analysis_copa_vs_python_dev():
    # Retrieve courses first to get COPA course ID
    res_courses = client.get("/api/v1/courses")
    assert res_courses.status_code == 200
    courses = res_courses.json()
    assert len(courses) > 0
    copa_course = next((c for c in courses if "COPA" in c["course_name"] or "Computer" in c["course_name"]), courses[0])
    course_id = copa_course["id"]

    # Post skill gap analysis
    payload = {
        "course_id": course_id,
        "target_role": "Junior Python Developer"
    }
    res = client.post("/api/v1/analysis/skill-gap", json=payload)
    assert res.status_code == 200, res.text
    report = res.json()

    print(f"✓ Skill Gap Analysis generated for '{copa_course['course_name']}' vs 'Junior Python Developer'")
    print(f"  - Alignment Score: {report['alignment_score']}%")
    print(f"  - Covered Skills: {[s['canonical_name'] for s in report['covered_skills']]}")
    print(f"  - Missing Skills: {[s['canonical_name'] for s in report['missing_skills']]}")
    
    assert report["alignment_score"] >= 0.0 and report["alignment_score"] <= 100.0
    assert report["total_required_skills"] > 0
    assert len(report["recommendations"]) > 0
    print(f"  - Auto-generated Recommendations: {len(report['recommendations'])}")

    report_id = report["id"]

    # Test GET analysis report by ID
    res_get = client.get(f"/api/v1/analysis/{report_id}")
    assert res_get.status_code == 200
    assert res_get.json()["id"] == report_id
    print("✓ GET /api/v1/analysis/{id} verified successfully")

    # Test recommendations listing
    res_recs = client.get(f"/api/v1/recommendations?course_id={course_id}")
    assert res_recs.status_code == 200
    recs = res_recs.json()
    assert len(recs) > 0
    first_rec = recs[0]
    rec_id = first_rec["id"]
    print(f"✓ Curriculum Modernization Proposal: '{first_rec['topic_title']}' [Priority: {first_rec['priority']}]")
    print(f"  - Learning Outcomes: {len(first_rec['learning_outcomes'])} outcomes defined")
    print(f"  - Practical Exercises: {len(first_rec['practical_exercises'])} exercises defined")
    print(f"  - Evidence Rationale: {first_rec['rationale']}")

    # Test PATCH recommendation status (Admin approval workflow)
    patch_payload = {"status": "APPROVED"}
    res_patch = client.patch(f"/api/v1/recommendations/{rec_id}", json=patch_payload)
    assert res_patch.status_code == 200
    assert res_patch.json()["status"] == "APPROVED"
    print(f"✓ PATCH /api/v1/recommendations/{rec_id} status updated to APPROVED")

def test_machinist_vs_cnc_operator():
    res_courses = client.get("/api/v1/courses")
    courses = res_courses.json()
    machinist_course = next((c for c in courses if "Machinist" in c["course_name"] or "CNC" in c["course_name"]), courses[0])

    payload = {
        "course_id": machinist_course["id"],
        "target_role": "CNC Milling Machine Operator"
    }
    res = client.post("/api/v1/analysis/skill-gap", json=payload)
    assert res.status_code == 200
    report = res.json()
    print(f"✓ Industrial Trade Skill Gap: '{machinist_course['course_name']}' vs 'CNC Milling Operator'")
    print(f"  - Alignment Score: {report['alignment_score']}%")
    print(f"  - Covered Skills: {[s['canonical_name'] for s in report['covered_skills']]}")
    assert report["alignment_score"] > 0.0

if __name__ == "__main__":
    test_skill_gap_analysis_copa_vs_python_dev()
    test_machinist_vs_cnc_operator()
    print("\n🎉 ALL STEP 4 (SKILL GAP ANALYSIS & RECOMMENDATION ENGINE) TESTS PASSED SUCCESSFULLY!")
