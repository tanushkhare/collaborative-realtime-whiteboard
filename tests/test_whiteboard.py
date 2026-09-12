import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_http_stroke_ingest_and_room_stats():
    payload = {
        "room_id": "test-room-99",
        "user_id": "usr_tester",
        "color": "#ff0000",
        "stroke_width": 4,
        "points": [{"x": 10.0, "y": 20.0}, {"x": 15.0, "y": 25.0}]
    }
    res = client.post("/api/v1/whiteboard/stroke", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["room_id"] == "test-room-99"
    assert data["persisted_strokes"] >= 1

def test_websocket_canvas_connection_and_malformed_handling():
    with client.websocket_connect("/api/v1/whiteboard/ws/test-ws-room") as ws:
        # Malformed frame protection
        ws.send_text("MALFORMED_NON_JSON")
        reply = ws.receive_json()
        assert "error" in reply
        assert reply["error"] == "MALFORMED_JSON_FRAME"
