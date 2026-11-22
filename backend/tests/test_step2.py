from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    print("✓ Health check passed")

def test_districts():
    res = client.get("/api/v1/districts")
    assert res.status_code == 200
    districts = res.json()
    assert len(districts) >= 36
    print(f"✓ Districts verified: {len(districts)} districts")

def test_skills_and_courses():
    res_s = client.get("/api/v1/skills")
    assert res_s.status_code == 200
    assert len(res_s.json()) > 0
    print(f"✓ Skills verified: {len(res_s.json())} skills")

    res_c = client.get("/api/v1/courses")
    assert res_c.status_code == 200
    assert len(res_c.json()) > 0
    print(f"✓ Courses verified: {len(res_c.json())} courses")

def test_csv_import():
    with open("../datasets/sample_jobs_maharashtra.csv", "rb") as f:
        res = client.post("/api/v1/jobs/import", files={"file": ("sample.csv", f, "text/csv")})
    assert res.status_code == 200
    data = res.json()
    assert data["imported"] >= 10
    print(f"✓ CSV Import verified: {data['imported']} jobs imported")

def test_job_query_and_top_skills():
    res = client.get("/api/v1/jobs?sector=Information+Technology")
    assert res.status_code == 200
    jobs = res.json()
    assert len(jobs) > 0
    print(f"✓ IT Sector Jobs query verified: {len(jobs)} jobs found")

    res_top = client.get("/api/v1/skills/top-demanded")
    assert res_top.status_code == 200
    top_skills = res_top.json()
    assert len(top_skills) > 0
    print(f"✓ Top Demanded Skills verified: {[s['skill'] for s in top_skills[:5]]}")

if __name__ == "__main__":
    test_health()
    test_districts()
    test_skills_and_courses()
    test_csv_import()
    test_job_query_and_top_skills()
    print("\n🎉 ALL STEP 2 TESTS PASSED SUCCESSFULLY!")
