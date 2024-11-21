from repositories.message_repository import MessageRepository
from schemas.message_schema import MessageCreate, MessageRead

class MessageService:
    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository

    async def send_message(self, message_data: MessageCreate) -> MessageRead:
        message = await self.message_repository.create_message(
            sender_id=message_data.sender_id,
            chat_id=message_data.chat_id,
            text=message_data.text,
        )
        return MessageRead.from_orm(message)
