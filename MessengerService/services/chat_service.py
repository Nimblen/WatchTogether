from repositories.chat_repository import ChatRepository
from schemas.chat_schema import ChatCreate, ChatRead

class ChatService:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    async def create_chat(self, chat_data: ChatCreate) -> ChatRead:
        chat = await self.chat_repository.create_chat(
            name=chat_data.name, is_group=chat_data.is_group
        )
        await self.chat_repository.add_members(chat.id, chat_data.members)
        return ChatRead(id=chat.id, name=chat.name, is_group=chat.is_group, members=chat_data.members)
