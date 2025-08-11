
from src.domain.ports.dispatchers.channel_dispatcher import ChannelDispatcher
from src.domain.entitites.notification import Notification

from src.domain.exceptions.channel_dispatcher_error_exception import ChannelDispatchErrorException
from src.application.services.event_consumer_service import EventConsumerService
from src.application.services.notification_factory import NotificationFactory
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


    async def execute(self):
        
        event = await self.event_consumer.consumer()
        notification = self.notification_factory.create_from_event(event)
        await self.channel_dispatch.dispatch(notification)