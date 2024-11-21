from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    sender_id: int
    chat_id: int
    text: str



class MessageRead(BaseModel):
    id: int
    sender_id: int
    chat_id: int
    text: str
    timestamp: datetime

    class Config:
        orm_mode = True