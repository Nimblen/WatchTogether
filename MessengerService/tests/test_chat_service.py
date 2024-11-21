import pytest
from datetime import datetime
from database.mongo import chats_collection
from services.chat_service import create_chat, get_chat, update_last_message


@pytest.fixture(autouse=True)
async def clear_database():
    """Очистка коллекции чатов перед каждым тестом."""
    await chats_collection.delete_many({})


@pytest.mark.asyncio
async def test_create_chat(mongodb):
    participants = [1, 2]
    chat_type = "private"
    name = "Test Chat"

    chat_id = await create_chat(participants, chat_type, name)
    chat = await mongodb.chats.find_one({"_id": chat_id})

    assert chat is not None
    assert chat["type"] == chat_type
    assert chat["name"] == name
    assert chat["participants"] == participants


@pytest.mark.asyncio
async def test_get_chat():
    participants = [1, 2]
    chat_type = "private"
    name = "Test Chat"

    # Создаём чат
    chat_id = await create_chat(participants, chat_type, name)

    # Получаем чат
    chat = await get_chat(chat_id)
    assert chat is not None
    assert chat["type"] == chat_type
    assert chat["name"] == name
    assert chat["participants"] == participants


@pytest.mark.asyncio
async def test_update_last_message():
    participants = [1, 2]
    chat_type = "private"
    name = "Test Chat"

    # Создаём чат
    chat_id = await create_chat(participants, chat_type, name)

    # Обновляем последнее сообщение
    sender_id = 1
    text = "Hello, world!"
    await update_last_message(chat_id, sender_id, text)

    # Проверяем обновление
    chat = await chats_collection.find_one({"_id": chat_id})
    assert chat is not None
    assert chat["last_message"] is not None
    assert chat["last_message"]["sender_id"] == sender_id
    assert chat["last_message"]["text"] == text
    assert "timestamp" in chat["last_message"]
