from domain.ports.event_bus.event_bus import EventBus
from domain.ports.dispatchers.channel_dispatcher import ChannelDispatcher
from domain.entitites.notification import Notification
from domain.exceptions.event_bus_error_exception import EventBusErrorException
from domain.exceptions.channel_dispatcher_error_exception import ChannelDispatchErrorException
import logging

logger = logging.getLogger(__name__)

class DispatchNotificationUseCase:
    
    def __init__(self,event_bus:EventBus, channel_dispatcher:ChannelDispatcher):
        self.event_bus = event_bus
        self.channel_dispatcher= channel_dispatcher

    def execute(self)-> None:
        logger.info("[DISPATCH SERVICE] Try to process event")

        try:
        
            # get event of queue
            logger.info("[DISPATCH SERVICE] Get event in notification queue ..")
            event = self.event_bus.consumer()
        except EventBusErrorException as event_error:
            logger.error(f"Failed consumer event: {event_error}")
            raise

        # parse event to notification
        logger.info("[DISPATCH SERVICE] Parsing event to notification ..")
        notification = self._parse_event_to_notification(event)
        logger.info("[DISPATCH SERVICE] is ready to dispatcher")
        try:
            # redirect notification to specific channel
            self.channel_dispatcher(notification)
        except ChannelDispatchErrorException as channel_error:
            logger.error(f"Failed dispatcher notification: {channel_error}")
            raise    

    def _parse_event_to_notification(self,event:dict)-> Notification:

        user_id = event.get("data", None).get("user_id",None)
        message = event.get("data", None).get("message",None)
        channel = event.get("data", None).get("channel",None)
        destination = event.get("data", None).get("destination",None)
        
        return Notification(user_id=user_id,
                            message=message,
                            channel=channel,
                            destination=destination)
