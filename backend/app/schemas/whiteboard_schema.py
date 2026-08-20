from pydantic import BaseModel, Field
from typing import List, Optional

class StrokePoint(BaseModel):
    x: float
    y: float

class DrawEvent(BaseModel):
    room_id: str
    client_id: str
    color: str = "#000000"
    line_width: int = 3
    points: List[StrokePoint]

class WhiteboardState(BaseModel):
    room_id: str
    active_users: int
    total_strokes: int
