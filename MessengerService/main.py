from fastapi import FastAPI
from routers import websocket, message, chat
from database.mongo import client
app = FastAPI()

app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])
app.include_router(message.router, prefix="/messages", tags=["Messages"])
app.include_router(chat.router, prefix="/chats", tags=["Chats"])





@app.on_event("shutdown")
async def shutdown_event():
    client.close()
