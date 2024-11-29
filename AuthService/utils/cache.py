import json
import logging
from typing import Optional


logger = logging.getLogger(__name__)





class CacheService:
    def __init__(self, redis_client, default_ttl: int = 3600):
        """
        Initialize the CacheService with a Redis client.

        Args:
            redis_client: The Redis client instance.
            default_ttl (int): Default time-to-live for cache entries.
        """
        self.redis = redis_client
        self.default_ttl = default_ttl

    async def get(self, key: str) -> Optional[dict]:
        """
        Retrieve data from cache by key.

        Args:
            key (str): The cache key.

        Returns:
            Optional[dict]: The cached data as a dictionary or None if the key doesn't exist.
        """
        try:
            data = await self.redis.get(key)
            if data:
                logger.info(f"Cache hit for key {key}")
                return json.loads(data)
        except Exception as exp:
            logger.error(f"Error fetching data from cache for key {key}: {exp}")
        return None

    async def set(self, key: str, value: dict, ttl: Optional[int] = None) -> bool:
        """
        Store data in cache.

        Args:
            key (str): The cache key.
            value (dict): The data to cache.
            ttl (int, optional): Time-to-live for cache entry in seconds.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            json_data = json.dumps(value)
            ttl = ttl or self.default_ttl
            await self.redis.set(key, json_data, ex=ttl)
            logger.info(f"Cache set for key {key} with TTL {ttl}")
            return True
        except TypeError as exp:
            logger.error(f"Failed to serialize data for key {key}: {exp}")
        except Exception as exp:
            logger.error(f"Error setting data to cache for key {key}: {exp}")
        return False
