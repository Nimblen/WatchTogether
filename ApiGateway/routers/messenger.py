import logging 
from typing import List
import httpx
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from core.config import settings
from utils.http_client import make_request 
from schemas.messenger import MessageRead

logger = logging.getLogger(__name__)



router = APIRouter()

MESSENGER_SERVICE_URL = settings.MESSENGER_SERVICE_URL

@router.websocket("/ws/messages/{chat_id}")
async def websocket_endpoint(chat_id: int, websocket: WebSocket):
    """
    Routes WebSocket connections to the MessengerService.
    """
    await websocket.accept()
    try:
        async with httpx.AsyncClient() as client:
            async with client.ws_connect(f"{MESSENGER_SERVICE_URL}/ws/messages/{chat_id}") as ws:
                while True:
                    message = await websocket.receive_text()
                    await ws.send_text(message)
                    response = await ws.receive_text()
                    await websocket.send_text(response)
    except WebSocketDisconnect:
        logger.info(f"WebSocket for chat {chat_id} disconnected.")

@router.get("/messages/{chat_id}", response_model=List[MessageRead])
async def get_messages(chat_id: int):
    return await make_request(
        method="GET",
        url=f"{MESSENGER_SERVICE_URL}/messages/{chat_id}",
    )


@router.post("/chats")
async def create_chat(chat_data: dict):
    return await make_request(
        method="POST",
        url=f"{MESSENGER_SERVICE_URL}/chats",
        json=chat_data,
    )


@router.get("/chats/{chat_id}")
async def get_chat(chat_id: int):
    return await make_request(
        method="GET",
        url=f"{MESSENGER_SERVICE_URL}/chats/{chat_id}",
    )
