from fastapi import FastAPI
from database.engine import engine
from database.models.core import Base
from routers import message, chat

app = FastAPI(title="Messenger Service")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(message.router, prefix="/api", tags=["Messages"])
app.include_router(chat.router, prefix="/api", tags=["Chats"])
