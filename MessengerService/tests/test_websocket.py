import pytest
from unittest.mock import AsyncMock
from fastapi import WebSocket
from services.websocket_service import ConnectionManager


@pytest.mark.asyncio
async def test_connect_and_disconnect():
    manager = ConnectionManager()
    websocket = AsyncMock(spec=WebSocket)
    user_id = 1

    # Подключаем WebSocket
    await manager.connect(user_id, websocket)
    assert user_id in manager.active_connections
    assert websocket in manager.active_connections[user_id]

    # Отключаем WebSocket
    manager.disconnect(user_id, websocket)
    assert user_id not in manager.active_connections


@pytest.mark.asyncio
async def test_send_personal_message():
    manager = ConnectionManager()
    websocket = AsyncMock(spec=WebSocket)
    user_id = 1
    message = "Personal message"

    # Подключаем WebSocket
    await manager.connect(user_id, websocket)

    # Отправляем личное сообщение
    await manager.send_personal_message(user_id, message)

    # Проверяем отправку
    websocket.send_text.assert_called_once_with(message)


@pytest.mark.asyncio
async def test_broadcast():
    manager = ConnectionManager()
    websocket1 = AsyncMock(spec=WebSocket)
    websocket2 = AsyncMock(spec=WebSocket)
    message = "Broadcast message"

    # Подключаем два WebSocket
    await manager.connect(1, websocket1)
    await manager.connect(2, websocket2)

    # Отправляем сообщение всем
    await manager.broadcast(message)

    # Проверяем отправку
    websocket1.send_text.assert_called_once_with(message)
    websocket2.send_text.assert_called_once_with(message)
