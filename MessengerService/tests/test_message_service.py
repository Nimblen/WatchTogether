import pytest
from datetime import datetime
from database.mongo import messages_collection
from services.message_service import save_message, get_messages

@pytest.mark.asyncio
async def test_save_message(mongodb):
    """
    Тестирует сохранение сообщения в MongoDB.
    """
    chat_id = 1
    sender_id = 123
    text = "Hello, MongoDB!"

    # Сохраняем сообщение
    await save_message(chat_id, sender_id, text)

    # Проверяем сохранение
    saved_message = await messages_collection.find_one({"chat_id": chat_id, "sender_id": sender_id})
    assert saved_message is not None
    assert saved_message["chat_id"] == chat_id
    assert saved_message["sender_id"] == sender_id
    assert saved_message["text"] == text
    assert isinstance(saved_message["timestamp"], datetime)


@pytest.mark.asyncio
async def test_get_messages(mongodb):
    """
    Тестирует получение сообщений из MongoDB.
    """
    chat_id = 1

    # Добавляем несколько сообщений
    await save_message(chat_id, 123, "Message 1")
    await save_message(chat_id, 456, "Message 2")

    # Получаем сообщения
    messages = await get_messages(chat_id)
    assert len(messages) == 2
    assert messages[0]["text"] == "Message 1"
    assert messages[1]["text"] == "Message 2"
