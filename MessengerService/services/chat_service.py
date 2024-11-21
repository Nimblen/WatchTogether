from datetime import datetime, timezone
from pymongo.errors import PyMongoError
from database.mongo import chats_collection

async def create_chat(participants: list[int], chat_type: str = "private", name: str = None):
    try:
        chat_data = {
            "type": chat_type,
            "name": name,
            "participants": participants,
            "created_at": datetime.now(timezone.utc),
            "last_message": None,
        }
        result = await chats_collection.insert_one(chat_data)
        return str(result.inserted_id)
    except PyMongoError as e:
        raise RuntimeError(f"Failed to create chat: {e}")

async def get_chat(chat_id: int):
    try:
        return await chats_collection.find_one({"_id": chat_id})
    except PyMongoError as e:
        raise RuntimeError(f"Failed to retrieve chat: {e}")


async def update_last_message(chat_id: int, sender_id: int, text: str):
    last_message = {
        "sender_id": sender_id,
        "text": text,
        "timestamp": datetime.utcnow()
    }
    await chats_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"last_message": last_message}}
    )
