from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@db/users_db"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    TOKEN_TYPE: str = "bearer"
    SECRET_KEY: str = os.getenv("SECRET_KEY")


    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_SPECIAL_CHARACTERS: bool = True

    REDIS_URL = "redis://localhost:6379"
    DEFAULT_CACHE_TTL = 3600



settings = Settings()