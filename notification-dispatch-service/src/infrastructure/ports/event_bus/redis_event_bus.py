from domain.ports.event_bus.event_bus import EventBus
from config.env import get_queue
import logging
import json

logger = logging.getLogger(__name__)

QUEUE = get_queue()

class RedisEventBus(EventBus):
      
      def __init__(self,redis_client):
          self.redis_client = redis_client
    
      def consumer(self) -> dict:
            logger.info("Trying to get event in queue ..")
            item = self.redis_client.blpop(QUEUE,timeout=0)

            if not item:
                logger.warning("There is not event in queue yet")
                return {}
            
            
            _, event = item # it is a tuple -> (queuename,value)
            logger.info(f"There is a new event:{event}")
            # if the event going yo bytes
            if isinstance(event,bytes):
                event = event.decode()

            # if event is json
            # trying to convert in dic

            try:
                return json.loads(event)
            except json.JSONDecodeError:
                raise