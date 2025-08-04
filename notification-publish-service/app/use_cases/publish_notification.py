from app.domain.ports.event_bus import EventBus
from app.domain.exceptions.notification_publish_error import NotificationPublishError
from app.domain.entities.notification_request import NotificationRequest
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PublishNotificationUseCase:

    def __init__(self,event_bus:EventBus):
        self.event_bus = event_bus

    def execute(self,notification:NotificationRequest) -> None:
        logger.info(f"Trying to publish notification ...")

        success = self.event_bus.publish(notification)
        if not success:
            logger.error(f" Failes dto publish notification")
            raise NotificationPublishError("Failed to publish event")
        
        logger.info("Notication published with successful.")