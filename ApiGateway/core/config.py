import os

from dotenv import load_dotenv




load_dotenv()


from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AUTH_SERVICE_URL: str = "http://localhost:8001"
    MESSENGER_SERVICE_URL: str = "http://localhost:8002"
    WATCH_PARTY_SERVICE_URL: str = "http://localhost:8003"

settings = Settings()
