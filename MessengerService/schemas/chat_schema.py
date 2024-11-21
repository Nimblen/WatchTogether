from pydantic import BaseModel
from typing import List

class ChatCreate(BaseModel):
    name: str | None = None  # Имя для группового чата
    is_group: bool = False  # Указывает, групповой это чат или индивидуальный
    members: List[int]  # Список ID участников чата

class ChatRead(BaseModel):
    id: int
    name: str | None
    is_group: bool
    members: List[int]
