from fastapi.testclient import TestClient

from jose import jwt
from main import app
from datetime import datetime, timedelta

client = TestClient(app)


def generate_test_token():
    payload = {
        "sub": "testuser",
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, "mysecret", algorithm="HS256")

def test_evaluate_and_retrieve():
    payload = {
        "age": 70,
        "has_chronic_pain": True,
        "bmi": 28,
        "had_recent_surgery": False
    }

    token = generate_test_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Evaluate
    response = client.post("/evaluate", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "recommendation_id" in data
    assert data["recommendation"] == "Physical Therapy"

    # Retrieve
    rec_id = data["recommendation_id"]
    response = client.get(f"/recommendation/{rec_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["recommendation"] == "Physical Therapy"
