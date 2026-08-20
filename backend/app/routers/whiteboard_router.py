from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from backend.app.services.canvas_service import manager
from backend.app.schemas.whiteboard_schema import WhiteboardState
import json

router = APIRouter(prefix="/api/v1/whiteboard", tags=["Collaborative Whiteboard"])

@router.websocket("/ws/{room_id}")
async def websocket_canvas_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(room_id, websocket)
    try:
        while True:
            raw_data = await websocket.receive_text()
            event = json.loads(raw_data)
            await manager.broadcast_stroke(room_id, websocket, event)
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)

@router.get("/rooms/{room_id}", response_model=WhiteboardState)
async def get_room_state(room_id: str):
    active_count = len(manager.active_rooms.get(room_id, []))
    stroke_count = len(manager.room_history.get(room_id, []))
    return WhiteboardState(
        room_id=room_id,
        active_users=active_count,
        total_strokes=stroke_count
    )
