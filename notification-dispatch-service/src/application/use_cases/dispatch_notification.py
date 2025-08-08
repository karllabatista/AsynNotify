
from domain.ports.dispatchers.channel_dispatcher import ChannelDispatcher
from domain.entitites.notification import Notification

from domain.exceptions.channel_dispatcher_error_exception import ChannelDispatchErrorException
from application.services.event_consumer_service import EventConsumerService
from application.services.notification_factory import NotificationFactory
import logging

logger = logging.getLogger(__name__)

class DispatchNotificationUseCase:
    
    def __init__(self, 
                event_consumer: EventConsumerService,
                notification_factory: NotificationFactory, 
                channel_dispatch:ChannelDispatcher):
        
        self.event_consumer = event_consumer
        self.notification_factory= notification_factory
        self.channel_dispatch= channel_dispatch


    def execute(self):
        
        event = self.event_consumer.consumer()
        notification = self.notification_factory.create_from_event(event)
        self.channel_dispatch.dispatch(notification)