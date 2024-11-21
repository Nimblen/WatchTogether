from datetime import datetime
from database.mongo import messages_collection

async def save_message(chat_id: int, sender_id: int, text: str):
    await messages_collection.insert_one({
        "chat_id": chat_id,
        "sender_id": sender_id,
        "text": text,
        "timestamp": datetime.utcnow()
    })

async def get_messages(chat_id: int):
    return await messages_collection.find({"chat_id": chat_id}).to_list(100)



