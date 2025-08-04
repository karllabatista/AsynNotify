import os
from dotenv import load_dotenv

# Carrega automaticamente o .env ao importar este módulo
load_dotenv()

def get_redis_host():
    return os.getenv("REDIS_HOST", "localhost")

def get_redis_port():
    return int(os.getenv("REDIS_PORT", 6379))
