import redis.asyncio as redis
from app.core.config import settings

async def get_redis():
    """
    Dependency to get a Redis connection.
    """
    pool = redis.ConnectionPool.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    client = redis.Redis(connection_pool=pool)
    try:
        yield client
    finally:
        await client.close()