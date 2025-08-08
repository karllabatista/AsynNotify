import os
from dotenv import load_dotenv

load_dotenv()

def get_queue():

    return os.getenv("QUEUE_NAME","notifications")