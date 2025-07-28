from app.domain.messaging.event_bus import EventBus
from queue import Queue
from app.domain.entities.notification_request import NotificationRequest
import logging

logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)

class InMemoryEventBus(EventBus):
    
    def __init__(self):
        self.queue:Queue = Queue()

    def publish(self,event:NotificationRequest)-> None:
        
        try:
            event_to_queue ={
                "type": "NotificationRequest",
                "data": event.to_dict()
            }

            self.queue.put(event_to_queue)
            logger.info(f"Published event to queue: {event_to_queue}")

        except Exception as error:
            logger.exception(f"Failed to publish event to queue:{error}")
            raise