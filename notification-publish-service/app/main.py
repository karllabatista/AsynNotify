from fastapi import FastAPI
from app.interface.controllers.notification_controller import router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(router)
