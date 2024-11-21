from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models.chat import Chat, ChatMember



class ChatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_chat(self, name: str, is_group: bool) -> Chat:
        chat = Chat(name=name, is_group=is_group)
        self.session.add(chat)
        await self.session.commit()
        await self.session.refresh(chat)
        return chat

    async def add_members(self, chat_id: int, user_ids: List[int]):
        members = [ChatMember(chat_id=chat_id, user_id=user_id) for user_id in user_ids]
        self.session.add_all(members)
        await self.session.commit()

    async def get_chat_members(self, chat_id: int) -> List[int]:
        query = select(ChatMember.user_id).where(ChatMember.chat_id == chat_id)
        result = await self.session.execute(query)
        return [row[0] for row in result.fetchall()]
