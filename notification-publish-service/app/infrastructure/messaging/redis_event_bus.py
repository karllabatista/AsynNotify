from domain.ports.event_bus import EventBus
from queue import Queue,Full
from domain.entities.notification_request import NotificationRequest
from domain.events.notification_event import NotificationEvent
from domain.exceptions.notification_publish_error import NotificationPublishError
import logging
import json

logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)
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
            self.queue_redis.rpush("notifications",json.dumps(event.to_dict()))
            logger.info("A new event was added to the queue ")
            return True
        
        except Exception as error:
            logger.exception(f"Uexpected error while publishing event:{error}")     
