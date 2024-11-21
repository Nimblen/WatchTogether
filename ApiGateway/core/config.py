from pydantic_settings import BaseSettings
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Settings(BaseSettings):
    AUTH_SERVICE_URL: str = "http://localhost:8001"
    MESSENGER_SERVICE_URL: str = "http://localhost:8002"
    WATCH_PARTY_SERVICE_URL: str = "http://localhost:8003"

settings = Settings()
