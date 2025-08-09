from redis import Redis
from config.env import get_redis_host, get_redis_port

def get_redis_connection()-> Redis:
    return Redis(
        host=get_redis_host(),
        port=get_redis_port(),
        db=0,
        decode_responses=True
    )