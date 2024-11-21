from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.chat_service import ChatService
from repositories.chat_repository import ChatRepository
from schemas.chat_schema import ChatCreate, ChatRead
from database.engine import get_db_session

router = APIRouter()

@router.post("/chats", response_model=ChatRead)
async def create_chat(
    chat_data: ChatCreate, db_session: AsyncSession = Depends(get_db_session)
):
    """
    Creates new chat
    """
    chat_service = ChatService(ChatRepository(db_session))
    return await chat_service.create_chat(chat_data)

@router.get("/chats/{chat_id}/members", response_model=list[int])
async def get_chat_members(
    chat_id: int, db_session: AsyncSession = Depends(get_db_session)
):
    """
    Returns list of chat members
    """
    chat_service = ChatService(ChatRepository(db_session))
    return await chat_service.chat_repository.get_chat_members(chat_id)
