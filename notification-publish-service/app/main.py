from fastapi import FastAPI
from infrastructure.messaging.in_memory_event_bus import InMemoryQueueEventBus
from interface.controllers.notification_controller import router
import logging

logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(router)
