from fastapi import APIRouter
from services.message_service import get_messages
from schemas.message_schema import MessageResponse
from typing import List

router = APIRouter()

@router.get("/{chat_id}", response_model=List[MessageResponse])
async def fetch_messages(chat_id: int):
    return await get_messages(chat_id)
