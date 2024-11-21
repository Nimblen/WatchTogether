from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import Message

class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_message(self, sender_id: int, chat_id: int, text: str) -> Message:
        """
        Creates a new message.
        """
        message = Message(sender_id=sender_id, chat_id=chat_id, text=text)
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_messages(self, chat_id: int) -> List[Message]:
        """
        Retrieves all messages for a given chat.
        """
        query = select(Message).where(Message.chat_id == chat_id).order_by(Message.timestamp)
        result = await self.session.execute(query)
        return result.scalars().all()
