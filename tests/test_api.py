from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_evaluate_and_retrieve():
    payload = {
        "age": 70,
        "has_chronic_pain": True,
        "bmi": 28,
        "had_recent_surgery": False
    }

    # Evaluate
    response = client.post("/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommendation_id" in data
    assert data["recommendation"] == "Physical Therapy"

    # Retrieve
    rec_id = data["recommendation_id"]
    response = client.get(f"/recommendation/{rec_id}")
    assert response.status_code == 200
    assert response.json()["recommendation"] == "Physical Therapy"
