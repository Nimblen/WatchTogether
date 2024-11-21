from fastapi import APIRouter, HTTPException
from services.chat_service import create_chat, get_chat

router = APIRouter()

@router.post("/")
async def create_new_chat(participants: list[int], chat_type: str = "private", name: str = None):
    if chat_type == "group" and not name:
        raise HTTPException(status_code=400, detail="Group chats require a name.")
    chat_id = await create_chat(participants, chat_type, name)
    return {"chat_id": chat_id}

@router.get("/{chat_id}")
async def fetch_chat(chat_id: int):
    chat = await get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found.")
    return chat
