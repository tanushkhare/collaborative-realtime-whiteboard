import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from backend.app.schemas.whiteboard_schema import StrokePayload, WhiteboardRoomStatus
from backend.app.services.whiteboard_service import canvas_manager

router = APIRouter(prefix="/api/v1/whiteboard", tags=["Collaborative Whiteboard Canvas"])

@router.websocket("/ws/{room_id}")
async def websocket_canvas_endpoint(websocket: WebSocket, room_id: str):
    await canvas_manager.connect(room_id, websocket)
    try:
        while True:
            raw_text = await websocket.receive_text()
            try:
                frame_data = json.loads(raw_text)
                await canvas_manager.broadcast_stroke(room_id, websocket, frame_data)
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "MALFORMED_JSON_FRAME"}))
    except WebSocketDisconnect:
        canvas_manager.disconnect(room_id, websocket)

@router.post("/stroke", response_model=WhiteboardRoomStatus)
async def post_stroke_http(payload: StrokePayload):
    stroke_dict = payload.model_dump()
    if payload.room_id not in canvas_manager.room_history:
        canvas_manager.room_history[payload.room_id] = []
    canvas_manager.room_history[payload.room_id].append(stroke_dict)
    return WhiteboardRoomStatus(**canvas_manager.get_room_stats(payload.room_id))

@router.get("/rooms/{room_id}", response_model=WhiteboardRoomStatus)
async def get_room_status(room_id: str):
    return WhiteboardRoomStatus(**canvas_manager.get_room_stats(room_id))
