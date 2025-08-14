import os
from dotenv import load_dotenv

load_dotenv()

def get_base_url_publish_notitication_service():
    return os.getenv("BASE_URL_PUBLISH_NOTIFICATION_SERVICE","http://127.0.0.1:8002")

def get_base_url_user_service():
    return os.getenv("BASE_URL_USER_SERVICE","http://127.0.0.1:8001")