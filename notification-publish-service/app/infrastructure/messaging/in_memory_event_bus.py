from app.domain.messaging.event_bus import EventBus
from queue import Queue,Full
from app.domain.entities.notification_request import NotificationRequest
from app.domain.events.notification_event import NotificationEvent
from app.domain.exceptions.notification_publish_error import NotificationPublishError
import logging

logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)

class InMemoryQueueEventBus(EventBus):
    
    def __init__(self):
        self.queue:Queue = Queue()

    def publish(self,notification:NotificationRequest,request_id:str)-> bool:
    
        try:
            if not isinstance(notification,NotificationRequest):
                raise TypeError("Expected NotificationRequest instance")
            
            event= NotificationEvent(notification,request_id)
            self.queue.put_nowait(event.to_dict())
            logger.info("A new event was added to the queue ")
            return True
        
        except Full as full_error:
            logger.error("The in-memory queue is full. Failed to enqueue the event.")
            raise NotificationPublishError("Queue is full") from full_error

        except Exception as error:
            logger.exception(f"Uexpected error while publishing event:{error}")     
