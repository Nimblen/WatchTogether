from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MongoDB
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "messenger"

    # Redis
    REDIS_URI: str = "redis://localhost:6379/0"

settings = Settings()
