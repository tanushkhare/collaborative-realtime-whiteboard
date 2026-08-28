from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
import json
from backend.app.schemas.whiteboard_schema import StrokeBroadcast, RoomStateResponse
from backend.app.services.whiteboard_service import room_manager

router = APIRouter(prefix="/api/v1/whiteboard", tags=["Collaborative Realtime Whiteboard"])

@router.get("/rooms/{room_id}", response_model=RoomStateResponse)
async def fetch_room_status(room_id: str):
    return RoomStateResponse(**room_manager.get_room_state(room_id))

@router.post("/rooms/{room_id}/stroke")
async def post_stroke(room_id: str, payload: StrokeBroadcast):
    room_manager.record_stroke(room_id, payload.dict())
    return {"status": "BROADCASTED", "room_id": room_id}

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    room_manager.get_or_create_room(room_id)
    room_manager.active_users[room_id].add(id(websocket))
    try:
        while True:
            raw_data = await websocket.receive_text()
            try:
                event = json.loads(raw_data)
                room_manager.record_stroke(room_id, event)
                await websocket.send_text(json.dumps({"status": "ACK", "event": event}))
            except json.JSONDecodeError:
                # Discard malformed frames without crashing socket loop
                continue
    except WebSocketDisconnect:
        room_manager.active_users[room_id].discard(id(websocket))
