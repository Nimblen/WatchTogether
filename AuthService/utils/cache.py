import json
import logging
import aioredis
from typing import Optional
from core.config import settings

logger = logging.getLogger(__name__)


redis = aioredis.from_url(settings.REDIS_URL)


async def get_data_from_cache(key: str) -> Optional[dict]:
    """
    Retrieve data from the Redis cache by a given key.

    Args:
        key (str): The cache key to retrieve data from.

    Returns:
        Optional[dict]: The data retrieved from the cache as a dictionary,
                        or None if the key does not exist or an error occurs.

    Raises:
        None: This function gracefully handles exceptions and logs errors.
    """
    try:
        data = await redis.get(key)
        if data:
            logger.info(f"Data fetched from cache for key {key}")
            return json.loads(data)
    except Exception as exp:
        logger.error(f"Error fetching data from cache for key {key}: {exp}")
    return None


async def set_data_to_cache(
    key: str, value: dict, ttl: int = settings.DEFAULT_CACHE_TTL
) -> bool:
    """
    Store data in the Redis cache with a specified time-to-live (TTL).

    Args:
        key (str): The cache key under which data will be stored.
        value (dict): The data to store in the cache. Must be JSON-serializable.
        ttl (int, optional): Time-to-live for the cache entry in seconds. Defaults to 3600 seconds (1 hour).

    Returns:
        bool: True if the operation is successful, False otherwise.

    Raises:
        None: This function gracefully handles exceptions and logs errors.
    """
    try:
        json_data = json.dumps(value)
        await redis.set(key, json_data, ex=ttl)
        logger.info(f"Data set in cache for key {key} with ttl {ttl} seconds")
        return True
    except TypeError as exp:
        logger.error(f"Failed to serialize data for key {key}: {exp}")
    except Exception as exp:
        logger.error(f"Error setting data to cache for key {key}: {exp}")
    return False
