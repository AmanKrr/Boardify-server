from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# User Schema
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password_hash: str
    current_room: Optional[str] = None
    role: str = "participant"
    created_at: datetime = datetime.utcnow()
