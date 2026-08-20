import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_room_state():
    res = client.get("/api/v1/whiteboard/rooms/unit-test-room")
    assert res.status_code == 200
    data = res.json()
    assert data["room_id"] == "unit-test-room"
    assert "active_users" in data
