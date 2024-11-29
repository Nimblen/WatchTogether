import aioredis
from core.config import settings
from utils.cache import CacheService


redis_client = aioredis.from_url(settings.REDIS_URL)
cache_service = CacheService(redis_client)
