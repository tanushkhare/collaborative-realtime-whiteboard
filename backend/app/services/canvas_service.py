from fastapi import WebSocket
from typing import Dict, List, Any
import json

class ConnectionManager:
    def __init__(self):
        # room_id -> List of active WebSocket connections
        self.active_rooms: Dict[str, List[WebSocket]] = {}
        # room_id -> List of drawn stroke history
        self.room_history: Dict[str, List[Dict[str, Any]]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.active_rooms:
            self.active_rooms[room_id] = []
            self.room_history[room_id] = []
        self.active_rooms[room_id].append(websocket)
        
        # Replay canvas stroke history to the newly connected peer
        if self.room_history[room_id]:
            await websocket.send_text(json.dumps({
                "type": "HISTORY_SYNC",
                "strokes": self.room_history[room_id]
            }))

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.active_rooms and websocket in self.active_rooms[room_id]:
            self.active_rooms[room_id].remove(websocket)
            if not self.active_rooms[room_id]:
                del self.active_rooms[room_id]

    async def broadcast_stroke(self, room_id: str, sender: WebSocket, stroke_data: Dict[str, Any]):
        if room_id in self.room_history:
            self.room_history[room_id].append(stroke_data)
        
        if room_id in self.active_rooms:
            for connection in self.active_rooms[room_id]:
                if connection != sender:
                    await connection.send_text(json.dumps({
                        "type": "REMOTE_STROKE",
                        "data": stroke_data
                    }))

manager = ConnectionManager()
