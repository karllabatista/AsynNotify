import redis.asyncio as aioredis
from config.env import get_redis_host, get_redis_port

async def get_redis_connection() -> aioredis.Redis:
    redis_url = f"redis://{get_redis_host()}:{get_redis_port()}"
    redis = aioredis.from_url(
        redis_url,
        db=0,
        decode_responses=True
    )
    return redis