from app.domain.messaging.event_bus import EventBus
from queue import Queue,Full
from app.domain.entities.notification_request import NotificationRequest
import logging
import time

logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)

class InMemoryEventBus(EventBus):
    
    def __init__(self):
        self.queue:Queue = Queue()

    def publish(self,event:NotificationRequest)-> bool:
        
       
        for attempt in range(1,4):
            try:
                event_to_queue ={
                    "type": "NotificationRequest",
                    "data": event.to_dict()
                }

                self.queue.put_nowait(event_to_queue)
                logger.info(f"[Attempt {attempt}]:Published event to queue: {event_to_queue}")
                return True

            except Full :
               logger.warning(f"[Attempt {attempt}] Queue full. Retrying...")
               time.sleep(0.1 * attempt)
        
      
            logger.error("All retries failed")
            return False
            