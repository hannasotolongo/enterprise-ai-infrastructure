from fastapi.testclient import TestClient

from src.inference.app import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "enterprise-ai-inference"
def test_prediction():
    response = client.post(
        "/predict",
        json={
            "features": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "device" in data