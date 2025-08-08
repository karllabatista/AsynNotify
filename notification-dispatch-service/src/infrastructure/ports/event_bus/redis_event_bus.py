from domain.ports.event_bus.event_bus import EventBus
QUEUE =""
import json

class RedisEventBus(EventBus):
      
      def __init__(self,redis_client):
          self.redis_client = redis_client
    
      def consumer(self) -> dict:
        
            item = self.redis_client.blpop(QUEUE,timeout=0)

            if not item:
                return {}
            
            _, event = item # it is a tuple -> (queuename,value)
            
            # if the event going yo bytes
            if isinstance(event,bytes):
                event = event.decode()

            # if event is json
            # trying to convert in dic

            try:
                return json.loads(event)
            except json.JSONDecodeError:
                return {"raw":event}