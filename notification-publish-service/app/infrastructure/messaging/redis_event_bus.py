from app.domain.ports.event_bus import EventBus
from app.domain.entities.notification_request import NotificationRequest
from app.domain.events.notification_event import NotificationEvent
from app.domain.exceptions.notification_publish_error import NotificationPublishError
from app.domain.exceptions.server_unavailable_error import ServerUnavailable
from app.domain.events.notification_event import NotificationEvent
import logging
import json
import redis
from config.env import get_queue_name

logger = logging.getLogger(__name__)

QUEUE_NAME = get_queue_name()

class RedisEventBus(EventBus):
    
    def __init__(self,redis_client):

        if not redis:
            raise ValueError("Redis is unavailable!") 
     
        self.queue_redis = redis_client
        

    def publish(self,event:NotificationEvent)-> bool:
    
        try:
            if not isinstance(event,NotificationEvent):
                raise TypeError("Expected NotificationRequest instance")
            
            payload = json.dumps(event.to_dict())
            self.queue_redis.rpush(QUEUE_NAME,payload)
            logger.info(f"[PUBLISH] Event pushed to queue '{QUEUE_NAME}' | user_id={event.user_id}")
            return True
        
        except (TypeError, ValueError, json.JSONDecodeError) as validation_error:
            logger.error(f"[PUBLISH] Invalid event format: {validation_error}")
            raise NotificationPublishError("Invalid event format") from validation_error
        except redis.exceptions.ConnectionError as redis_error:
            logger.exception("Redis connection failed")
            raise ServerUnavailable("Could not connect to Redis") from redis_error
        
        except Exception as error:
            logger.exception(f"[PUBLISH] Unexpected error while publishing event: {error}")
            raise NotificationPublishError("Failed to publish event") from error