from pydantic import BaseModel
from datetime import datetime

class MessageResponse(BaseModel):
    chat_id: int
    sender_id: int
    text: str
    timestamp: datetime
