from domain.ports.event_bus import EventBus
from queue import Queue,Full
from domain.entities.notification_request import NotificationRequest
from domain.events.notification_event import NotificationEvent
from domain.exceptions.notification_publish_error import NotificationPublishError
import logging
import json

logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)

QUEUE_NAME = "notifications"
class RedisEventBus(EventBus):
    
    def __init__(self,redis):

        if not redis:
            raise ValueError("Redis is unavailable!") 
     
        self.queue_redis = redis
        

    def publish(self,notification:NotificationRequest,request_id:str=None)-> bool:
    
        try:
            if not isinstance(notification,NotificationRequest):
                raise TypeError("Expected NotificationRequest instance")
            
            event= NotificationEvent(notification)
            payload = json.dumps(event.to_dict())
            self.queue_redis.rpush(Queue,payload)
            logger.info(f"[PUBLISH] Event pushed to queue '{QUEUE_NAME}' | user_id={notification.user_id}")
            return True
        
        except Exception as error:
            logger.exception(f"Uexpected error while publishing event:{error}")     
