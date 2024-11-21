from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

async def get_mongo_client() -> AsyncIOMotorClient:
    try:
        yield client
    finally:
        client.close()


messages_collection = db.messages
chats_collection = db.chats
