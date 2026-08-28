import json
from datetime import datetime, timezone
from typing import Dict, List, Any

class WhiteboardRoomManager:
    def __init__(self):
        self.rooms: Dict[str, List[Dict[str, Any]]] = {}
        self.active_users: Dict[str, set] = {}

    def get_or_create_room(self, room_id: str):
        if room_id not in self.rooms:
            self.rooms[room_id] = []
            self.active_users[room_id] = set()

    def record_stroke(self, room_id: str, stroke_data: dict) -> bool:
        self.get_or_create_room(room_id)
        # Bounded history to prevent memory leak
        if len(self.rooms[room_id]) >= 1000:
            self.rooms[room_id].pop(0)
        self.rooms[room_id].append(stroke_data)
        return True

    def get_room_state(self, room_id: str) -> Dict[str, Any]:
        self.get_or_create_room(room_id)
        return {
            "room_id": room_id,
            "active_connections": len(self.active_users.get(room_id, set())),
            "total_strokes_recorded": len(self.rooms.get(room_id, [])),
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

room_manager = WhiteboardRoomManager()
