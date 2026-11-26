from fastapi.testclient import TestClient
from app.main import app
import io
import pypdf

client = TestClient(app)

def test_vtu_cse_vs_senior_backend_engineer():
    res_courses = client.get("/api/v1/courses")
    assert res_courses.status_code == 200
    courses = res_courses.json()
    assert len(courses) > 0
    
    # Pick VTU or Computer Science course
    target_course = next((c for c in courses if "VTU" in c["course_name"] or "Software Engineering" in c["course_name"]), courses[0])
    course_id = target_course["id"]

    payload = {
        "course_id": course_id,
        "target_role": "Senior Backend Engineer"
    }
    res = client.post("/api/v1/analysis/skill-gap", json=payload)
    assert res.status_code == 200, res.text
    report = res.json()

    print(f"✓ B.Tech CSE Gap Analysis generated for '{target_course['course_name']}' vs 'Senior Backend Engineer'")
    print(f"  - Alignment Score: {report['alignment_score']}%")
    print(f"  - Covered Skills: {[s['canonical_name'] for s in report['covered_skills']]}")
    print(f"  - Missing Skills: {[s['canonical_name'] for s in report['missing_skills']]}")
    
    assert report["alignment_score"] >= 0.0 and report["alignment_score"] <= 100.0
    assert report["total_required_skills"] > 0
    assert len(report["recommendations"]) > 0
    print(f"  - BoS Curriculum Recommendations: {len(report['recommendations'])}")

    report_id = report["id"]

    # Test GET analysis report by ID
    res_get = client.get(f"/api/v1/analysis/{report_id}")
    assert res_get.status_code == 200
    assert res_get.json()["id"] == report_id
    print("✓ GET /api/v1/analysis/{id} verified successfully")

    # Test BoS recommendations listing & approval
    res_recs = client.get(f"/api/v1/recommendations?course_id={course_id}")
    assert res_recs.status_code == 200
    recs = res_recs.json()
    assert len(recs) > 0
    first_rec = recs[0]
    rec_id = first_rec["id"]
    print(f"✓ Board of Studies Proposal: '{first_rec['topic_title']}' [Priority: {first_rec['priority']}]")

    # Faculty BoS Approval
    patch_payload = {"status": "APPROVED"}
    res_patch = client.patch(f"/api/v1/recommendations/{rec_id}", json=patch_payload)
    assert res_patch.status_code == 200
    assert res_patch.json()["status"] == "APPROVED"
    print(f"✓ PATCH /api/v1/recommendations/{rec_id} status updated to APPROVED by BoS")

def test_syllabus_pdf_import():
    # Build a simulated syllabus PDF in memory
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    
    pdf_bytes = io.BytesIO()
    writer.write(pdf_bytes)
    pdf_bytes.seek(0)

    res = client.post(
        "/api/v1/courses/import-pdf",
        files={"file": ("vtu_bcs601_cloud_native.pdf", pdf_bytes, "application/pdf")},
        data={"institution": "Visvesvaraya Technological University (VTU)", "qualification": "B.Tech CSE Semester VI"}
    )
    assert res.status_code == 200, res.text
    data = res.json()
    assert "course_id" in data
    print(f"✓ PDF Syllabus Ingestion verified: '{data['course_name']}' created via PDF upload")

if __name__ == "__main__":
    test_vtu_cse_vs_senior_backend_engineer()
    test_syllabus_pdf_import()
    print("\n🎉 ALL BTECH CSE SKILL GAP & SYLLABUS PDF TESTS PASSED SUCCESSFULLY!")
