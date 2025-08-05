from app.domain.ports.event_bus import EventBus
from app.domain.exceptions.notification_publish_error import NotificationPublishError
from app.domain.entities.notification_request import NotificationRequest
from app.domain.events.notification_event import NotificationEvent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PublishNotificationUseCase:

    def __init__(self,event_bus:EventBus):
        self.event_bus = event_bus

    def execute(self,notification:NotificationRequest,user_repo) -> None:
        logger.info(f"Trying to publish notification ...")
        
        if notification.channel == "email":
            destination = user_repo.email

        elif notification.channel == "sms":
            destination = user_repo.sms

        elif notification.channel == "push":
            destination = user_repo.push

        
        event = NotificationEvent(notification.user_id,
                                  notification.message,
                                  notification.channel,
                                  destination)

        success = self.event_bus.publish(event)
        if not success:
            logger.error(f" Failes dto publish notification")
            raise NotificationPublishError("Failed to publish event")
        
        logger.info("Notication published with successful.")