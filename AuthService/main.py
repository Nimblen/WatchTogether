from fastapi import FastAPI
from database.sessions import engine
from database.models import Base
from routers import auth


app = FastAPI(
    title="Authentication Service",
    description="Service for Authentication and Authorization",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
