import os
from dotenv import load_dotenv

# Carrega automaticamente o .env ao importar este módulo
load_dotenv()

def get_redis_host():
    return os.getenv("REDIS_HOST", "localhost")

def get_redis_port():
    return int(os.getenv("REDIS_PORT", 6379))

def get_queue_name():
    return os.getenv("QUEUE_NAME","notifications")

def get_base_url_user_service():

    return os.getenv("BASE_URL_USER_SERVICE","http://127.0.0.1:8000")