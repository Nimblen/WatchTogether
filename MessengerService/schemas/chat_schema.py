from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatCreate(BaseModel):
    participants: List[int]
    type: str = "private"
    name: Optional[str] = None

class ChatResponse(BaseModel):
    chat_id: int
    type: str
    name: Optional[str]
    participants: List[int]
    created_at: datetime
    last_message: Optional[dict]
