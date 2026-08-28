import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_room_status_and_stroke_post():
    room_id = "test_design_room"
    # Fetch room status
    status_res = client.get(f"/api/v1/whiteboard/rooms/{room_id}")
    assert status_res.status_code == 200
    assert status_res.json()["room_id"] == room_id

    # Post stroke event
    payload = {
        "room_id": room_id,
        "user_id": "test_user",
        "action": "DRAW_STROKE",
        "points": [{"x": 10.0, "y": 20.0, "color": "#FF0000", "width": 2}]
    }
    stroke_res = client.post(f"/api/v1/whiteboard/rooms/{room_id}/stroke", json=payload)
    assert stroke_res.status_code == 200
    assert stroke_res.json()["status"] == "BROADCASTED"
