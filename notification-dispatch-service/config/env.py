import os
from dotenv import load_dotenv

load_dotenv()

def get_queue():

    return os.getenv("QUEUE_NAME","notifications")

def get_redis_host():
    return os.getenv("REDIS_HOST", "localhost")

def get_redis_port():
    return int(os.getenv("REDIS_PORT", 6379))

def get_value_of_timeout_queue():
    return int(os.getenv("TIMEOUT","10"))