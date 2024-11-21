from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from services.message_service import save_message
from services.chat_service import update_last_message
from services.websocket_service import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws/messages/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    await manager.connect(chat_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            sender_id = data.get("sender_id")
            text = data.get("text")
            if not sender_id or not text:
                await websocket.send_text("Invalid message format")
                continue
            await save_message(chat_id, sender_id, text)
            await update_last_message(chat_id, sender_id, text)
            await manager.broadcast(chat_id, text)
    except WebSocketDisconnect:
        manager.disconnect(chat_id, websocket)
        await manager.broadcast(chat_id, "User disconnected")
