import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from main import app 
from core.config import settings  # Настройки приложения

TEST_DATABASE_URL = "mongodb://localhost:27017"
TEST_DATABASE_NAME = "test_messenger" 

@pytest.fixture(scope="module")
async def mongodb_client():
    """
    Фикстура для подключения к MongoDB клиенту.
    """
    client = AsyncIOMotorClient(TEST_DATABASE_URL)
    yield client
    client.close()

@pytest.fixture(scope="module")
async def mongodb(mongodb_client):
    """
    Фикстура для использования тестовой базы данных.
    """
    db = mongodb_client[TEST_DATABASE_NAME]
    yield db
    await mongodb_client.drop_database(TEST_DATABASE_NAME)

@pytest.fixture(scope="function")
async def clear_collections(mongodb):
    for collection_name in await mongodb.list_collection_names():
        await mongodb[collection_name].delete_many({})
