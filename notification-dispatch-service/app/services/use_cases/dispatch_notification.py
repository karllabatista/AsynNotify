from domain.ports.event_bus.event_bus import EventBus
from domain.ports.dispatchers.channel_dispatcher import ChannelDispatcher
from domain.entitites.notification import Notification
from domain.exceptions.event_bus_error_exception import EventBusErrorException
from domain.exceptions.channel_dispatcher_error_exception import ChannelDispatchErrorException
from domain.exceptions.invalid_notification_event import InvalidNotificationEvent
import logging

logger = logging.getLogger(__name__)

class DispatchNotificationUseCase:
    
    def __init__(self,event_bus:EventBus, channel_dispatcher:ChannelDispatcher):
        self.event_bus = event_bus
        self.channel_dispatcher= channel_dispatcher


    def execute(self):
        
        notification = self.create_notification_from_event()
        try:
            self.channel_dispatcher.dispatch(notification)

        except ChannelDispatchErrorException as channel_error:
            logger.error(f"Failed dispatcher notification: {channel_error}")
            raise   

    def create_notification_from_event(self)-> Notification:

        event = self._event_consumer()

        return self._parse_event_to_notification(event)


    def  _event_consumer(self)->dict: ## criar um serivco auxiliar?

        try:

            logger.info("[DISPATCH SERVICE] Get event in notification queue ..")
            event = self.event_bus.consumer()
            return event
        
        except EventBusErrorException as event_error:
            logger.error(f"Failed consumer event: {event_error}")
            raise
    

    def _parse_event_to_notification(self,event:dict)-> Notification: 

        data = event.get("data")

        if not data:
            logger.error("Missing data key in event")
            raise InvalidNotificationEvent("Missing data key in event")

        
        return Notification(user_id=data.get("user_id"),
                            message=data.get("message"),
                            channel=data.get("channel"),
                            destination=data.get("destination"))
