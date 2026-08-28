from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class StrokePoint(BaseModel):
    x: float
    y: float
    color: Optional[str] = "#000000"
    width: Optional[int] = 2

class StrokeBroadcast(BaseModel):
    room_id: str
    user_id: str
    action: str = "DRAW_STROKE"
    points: List[StrokePoint]

class RoomStateResponse(BaseModel):
    room_id: str
    active_connections: int
    total_strokes_recorded: int
    last_updated: str
