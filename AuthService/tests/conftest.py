import sys
import os
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from main import app
from database.sessions import engine, AsyncSessionLocal
from database.models import Base

# Добавляем корневую папку проекта в sys.path, чтобы модули корректно импортировались
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Настройка тестовой базы данных
@pytest.fixture(scope="module", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Создаём таблицы
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Удаляем таблицы после тестов

# Фикстура для подключения к тестовой сессии базы данных
@pytest.fixture
async def test_session():
    async with AsyncSessionLocal() as session:
        yield session

# Фикстура для асинхронного HTTP-клиента
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
