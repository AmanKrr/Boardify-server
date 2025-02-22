from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# Room Schema
class RoomSchema(BaseModel):
    name: str
    is_private: bool
    password_hash: Optional[str] = None
    max_users: int = 50
    users: List[str] = []
    created_at: datetime = datetime.utcnow()
