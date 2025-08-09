from src.domain.ports.event_bus.event_bus import EventBus
from src.domain.exceptions.server_unavailable_exception import ServerUnavailable
from src.domain.exceptions.empty_queue_exception import EmptyQueueException
from config.env import get_queue
import logging
import json
import redis
logger = logging.getLogger(__name__)

QUEUE = get_queue()

class RedisEventBus(EventBus):
      
      def __init__(self,redis_client):
          self.redis_client = redis_client
    
      def consumer(self) -> dict:
            try:
                logger.info("Trying to get event in queue ..")
                item = self.redis_client.blpop(QUEUE,timeout=0)

                if not item:
                    logger.warning("There is not event in queue yet")
                    raise EmptyQueueException("No events in the notifications queue")
                
                _, event = item # it is a tuple -> (queuename,value)
                logger.info(f"There is a new event:{event}")
            except redis.exceptions.ConnectionError as redis_error:
                logger.exception("Redis connection failed")
                raise ServerUnavailable("Could not connect to Redis") from redis_error
            except EmptyQueueException:
                raise

            try:
          
                # if the event going yo bytes
                if isinstance(event,bytes):
                    event = event.decode()
                    return event
                return json.loads(event)
            except json.JSONDecodeError:
                logger.error(f"Erro to decode event from jsont to python dict")
                raise
            except Exception as error:
                logger.exception(f"An error occurred while get event from notifcation queue:{error}")
                raise