from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/message_db"

    class Config:
        env_file = ".env" 

# Экземпляр настроек
settings = Settings()
