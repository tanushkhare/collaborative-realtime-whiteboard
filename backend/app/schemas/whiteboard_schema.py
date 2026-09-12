from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class StrokePoint(BaseModel):
    x: float = Field(..., description="Canvas X coordinate")
    y: float = Field(..., description="Canvas Y coordinate")

class StrokePayload(BaseModel):
    room_id: str = Field(default="main-room")
    user_id: str = Field(..., description="Client identifier")
    color: str = Field(default="#38bdf8")
    stroke_width: int = Field(default=3, ge=1, le=20)
    points: List[StrokePoint] = Field(..., min_length=1)

class WhiteboardRoomStatus(BaseModel):
    room_id: str
    active_peers: int
    persisted_strokes: int
    status: str
