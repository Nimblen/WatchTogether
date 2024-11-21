from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.message_service import MessageService
from repositories.message_repository import MessageRepository
from schemas.message_schema import MessageCreate, MessageRead
from database.engine import get_db_session

router = APIRouter()

@router.post("/messages", response_model=MessageRead)
async def send_message(
    message_data: MessageCreate, db_session: AsyncSession = Depends(get_db_session)
):
    message_service = MessageService(MessageRepository(db_session))
    return await message_service.send_message(message_data)
