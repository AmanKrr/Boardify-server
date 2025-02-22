from pydantic import BaseModel


class DrawingAction(BaseModel):
    type: str
    tool: str
    color: str
    strokeWidth: int
    x: float
    y: float
