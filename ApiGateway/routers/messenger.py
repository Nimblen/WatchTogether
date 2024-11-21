from fastapi import APIRouter
from typing import List
from core.config import settings
from utils.http_client import make_request 
from schemas.messenger import MessageCreate, MessageRead

router = APIRouter()

MESSENGER_SERVICE_URL = settings.MESSENGER_SERVICE_URL


@router.post("/messages", response_model=MessageRead)
async def send_message(message: MessageCreate):
    return await make_request(
        method="POST",
        url=f"{MESSENGER_SERVICE_URL}/messages",
        json=message.dict(),
    )


@router.get("/messages/{chat_id}", response_model=List[MessageRead])
async def get_messages(chat_id: int):
    return await make_request(
        method="GET",
        url=f"{MESSENGER_SERVICE_URL}/messages/{chat_id}",
    )


@router.post("/chats")
async def create_chat(chat_data: dict):
    return await make_request(
        method="POST",
        url=f"{MESSENGER_SERVICE_URL}/chats",
        json=chat_data,
    )


@router.get("/chats/{chat_id}")
async def get_chat(chat_id: int):
    return await make_request(
        method="GET",
        url=f"{MESSENGER_SERVICE_URL}/chats/{chat_id}",
    )
