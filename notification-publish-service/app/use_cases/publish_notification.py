from app.domain.ports.event_bus import EventBus
from app.domain.exceptions.notification_publish_error import NotificationPublishError
from app.domain.entities.notification_request import NotificationRequest
from app.domain.events.notification_event import NotificationEvent
from app.domain.repositories.user_contact_info_repository import UserContactInfoRepository
from app.domain.exceptions.user_not_found_exception import UserNotFound
import logging


logger = logging.getLogger(__name__)

class PublishNotificationUseCase:

    def __init__(self,
                event_bus:EventBus,
                user_repository:UserContactInfoRepository):
        self.event_bus = event_bus
        self.user_repository = user_repository

    def execute(self,notification:NotificationRequest) -> None:
        logger.info(f"Trying to publish notification ...")

        try:
            # TODO push notification
            user_contact =  self.user_repository.get_contact_info_by_user_id(notification.user_id)

            if not user_contact:
                raise UserNotFound("[PUBLISH SERVICE] User not found")
            
            destination = user_contact.preferred_channel
        except UserNotFound:
            raise   

        event = NotificationEvent(notification.user_id,
                                    notification.message,
                                    notification.channel,
                                    destination)
        
        try:
            success = self.event_bus.publish(event)
            if not success:
                logger.error(f" Failed to publish notification")
                raise NotificationPublishError("Failed to publish event")
         
            logger.info("Notication published with successful.")
        except NotificationPublishError:
            raise
        except Exception as e:
            logger.exception(f"[PUBLISH SERVICE] Unexpected error while publish event:{e}")
            raise