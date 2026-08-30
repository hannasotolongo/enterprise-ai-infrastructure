from fastapi.testclient import TestClient

from src.inference.app import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "enterprise-ai-inference"
    assert "device" in data


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


def test_prediction_response_types():
    response = client.post(
        "/predict",
        json={
            "features": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["prediction"], int)
    assert isinstance(data["device"], str)


def test_invalid_prediction_input():
    response = client.post(
        "/predict",
        json={
            "features": "invalid"
        },
    )

    assert response.status_code == 422


def test_wrong_feature_count():
    response = client.post(
        "/predict",
        json={
            "features": [1, 2, 3]
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert data["detail"] == "Model requires exactly 10 features."


def test_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200

    data = response.json()

    assert "prediction_requests" in data
    assert "successful_predictions" in data
    assert "average_prediction_latency_seconds" in data
    assert "device" in data

    assert data["prediction_requests"] >= 0
    assert data["successful_predictions"] >= 0
    assert data["average_prediction_latency_seconds"] >= 0


def test_prometheus_metrics_endpoint():
    response = client.get("/metrics/prometheus")

    assert response.status_code == 200
    assert "inference_requests_total" in response.text
    assert "inference_latency_seconds" in response.text