import json
from typing import Dict, List, Any
from fastapi import WebSocket, WebSocketDisconnect

class CollaborativeCanvasManager:
    def __init__(self):
        # Active in-memory WebSocket connections: room_id -> List[WebSocket]
        self.rooms: Dict[str, List[WebSocket]] = {}
        # Stroke history for session recovery upon reconnect
        self.room_history: Dict[str, List[Dict[str, Any]]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = []
            self.room_history[room_id] = []
        self.rooms[room_id].append(websocket)

        # Synchronize existing canvas history to the newly connected peer
        if self.room_history[room_id]:
            await websocket.send_text(json.dumps({
                "type": "CANVAS_HISTORY_RECOVERY",
                "room_id": room_id,
                "strokes": self.room_history[room_id]
            }))

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.rooms and websocket in self.rooms[room_id]:
            self.rooms[room_id].remove(websocket)
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def broadcast_stroke(self, room_id: str, sender: WebSocket, raw_stroke: Dict[str, Any]):
        if room_id not in self.room_history:
            self.room_history[room_id] = []
        self.room_history[room_id].append(raw_stroke)

        # Non-blocking peer broadcast
        if room_id in self.rooms:
            message = json.dumps({
                "type": "STROKE_EVENT",
                "room_id": room_id,
                "data": raw_stroke
            })
            for peer in list(self.rooms[room_id]):
                if peer != sender:
                    try:
                        await peer.send_text(message)
                    except Exception:
                        self.disconnect(room_id, peer)

    def get_room_stats(self, room_id: str) -> Dict[str, Any]:
        peers = len(self.rooms.get(room_id, []))
        strokes = len(self.room_history.get(room_id, []))
        return {
            "room_id": room_id,
            "active_peers": peers,
            "persisted_strokes": strokes,
            "status": "ACTIVE_ROOM" if peers > 0 else "IDLE_ROOM"
        }

canvas_manager = CollaborativeCanvasManager()
