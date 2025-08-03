from domain.ports.event_bus import EventBus
from queue import Queue,Full
from domain.entities.notification_request import NotificationRequest
from domain.events.notification_event import NotificationEvent
from domain.exceptions.notification_publish_error import NotificationPublishError
import logging
import json
import redis

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
        
        except (TypeError, ValueError, json.JSONDecodeError) as validation_error:
            logger.error(f"[PUBLISH] Invalid event format: {validation_error}")
            raise NotificationPublishError("Invalid event format") from validation_error
        except redis.exceptions.ConnectionError as redis_error:
            logger.exception("Redis connection failed")
            raise NotificationPublishError("Could not connect to Redis") from redis_error
        
        except Exception as error:
            logger.exception(f"[PUBLISH] Unexpected error while publishing event: {error}")
            raise NotificationPublishError("Failed to publish event") from error