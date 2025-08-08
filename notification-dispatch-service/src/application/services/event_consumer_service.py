from src.domain.ports.event_bus.event_bus import EventBus
from src.domain.exceptions.event_bus_error_exception import EventBusErrorException
import logging
logger = logging.getLogger(__name__)
class EventConsumerService:

    def __init__(self,
                event_bus:EventBus):
        
        self.event_bus = event_bus

    def consumer(self)->dict:
        try:

            logger.info("[DISPATCH SERVICE] Get event in notification queue ..")
            event = self.event_bus.consumer()
            return event
        
        except EventBusErrorException as event_error:
            logger.error(f"Failed consumer event: {event_error}")
            raise


    
    