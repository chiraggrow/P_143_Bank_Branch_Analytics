from fastapi.testclient import TestClient
from api.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_get_branches():
    response = client.get("/branches")
    assert response.status_code == 200


def test_get_branch():
    response = client.get("/branches/101")
    assert response.status_code == 200
    assert response.json()["Branch_ID"] == 101


def test_overview():
    response = client.get("/analytics/overview")
    assert response.status_code == 200


def test_feedback():
    response = client.post(
        "/feedback/analyze",
        json={"feedback": "The staff was very helpful."}
    )

    assert response.status_code == 200
    assert "sentiment" in response.json()