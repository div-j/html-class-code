from fastapi.testclient import TestClient
from app.main import app, APP_VERSION

client = TestClient(app)


def test_health_details():
    resp = client.get("/health-details")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok"
    assert data.get("version") == APP_VERSION
    assert isinstance(data.get("uptime_seconds"), int)
    assert data.get("uptime_seconds") >= 0
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}