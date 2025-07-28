from app.domain.messaging.event_bus import EventBus
from app.domain.exceptions.notification_publish_error import NotificationPublishError
from app.domain.entities.notification_request import NotificationRequest
class PublishNotificationUseCase:

    def __init__(self,event_bus:EventBus):
        self.event_bus = event_bus

    def execute(self,event:NotificationRequest) -> None:

        try:
            self.event_bus.publish(event)
            
        except Exception :
            raise NotificationPublishError("Failed to publish event")