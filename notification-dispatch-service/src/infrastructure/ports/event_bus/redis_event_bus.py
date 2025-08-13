from src.domain.ports.event_bus.event_bus import EventBus
from src.domain.exceptions.server_unavailable_exception import ServerUnavailable
from src.domain.exceptions.empty_queue_exception import EmptyQueueException
from src.domain.exceptions.invalid_event_format_exception import InvalidEventFormatException
import logging
import json
import redis.asyncio as aioredis
from typing import Optional
logger = logging.getLogger(__name__)


class RedisEventBus(EventBus):
      
    def __init__(self,redis_client:aioredis.Redis,queue:str,timeout:Optional[int]):
          self.redis_client = redis_client
          self.queue = queue
          self.timeout = timeout
    
    async def consumer(self) -> dict:
        """Consume a single event from the Redis queue and return it as a dict."""
      
        event = await self._get_event_raw_from_queue()
        return self._deserialize_event(event)
    

    def _deserialize_event(self, event:bytes) -> dict:
        """Decode bytes and parse JSON."""
        try:
            if isinstance(event, bytes):
                # convert bytes to string
                event = event.decode()
            logger.debug("Event deserialized successfully.")
            return json.loads(event) # returs a dict
        
        except json.JSONDecodeError as e:
            logger.exception("Invalid Json in queue")
            raise InvalidEventFormatException("Event is not valid JSON") from e

    async def _get_event_raw_from_queue(self)->bytes:
        """ Get event from queue if exists"""
        try:
            logger.info("Waiting for event from queue...")
            # BLPOP command async with timeout
            item = await self.redis_client.blpop(self.queue,self.timeout)

            if not item:
                logger.warning("No events in queue yet")
                raise EmptyQueueException("No events in the notifications queue")
            logger.info("Consuming event of queue..")
            _, raw_event = item # it is a tuple -> (queuename,value)
            logger.debug(f"Raw event bytes: {raw_event}")  
            return raw_event
        except aioredis.RedisError as redis_error:
            logger.exception("Redis connection failed")
            raise ServerUnavailable("Could not connect to Redis") from redis_error
        except EmptyQueueException:
            raise
        