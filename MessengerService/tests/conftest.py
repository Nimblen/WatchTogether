import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.core import Base
from MessangerService.main import app

DATABASE_URL = "sqlite+aiosqlite:///./test_messenger.db"

engine = create_async_engine(DATABASE_URL, future=True)
TestSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession)

@pytest.fixture(scope="function")
async def db_session():
    async with TestSessionLocal() as session:
        yield session

@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
