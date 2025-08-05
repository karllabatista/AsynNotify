from app.domain.ports.event_bus import EventBus
from app.domain.exceptions.notification_publish_error import NotificationPublishError
from app.domain.entities.notification_request import NotificationRequest
from app.domain.events.notification_event import NotificationEvent
from app.domain.repositories.user_contact_info_repository import UserContactInfoRepository
from app.domain.exceptions.user_not_found_exception import UserNotFound
import logging


logger = logging.getLogger(__name__)

class PublishNotificationUseCase:

    def __init__(self,event_bus:EventBus):
        self.event_bus = event_bus

    def execute(self,notification:NotificationRequest,
                user_contact_info_repository: UserContactInfoRepository) -> None:
        logger.info(f"Trying to publish notification ...")

        try:

            user_contact = user_contact_info_repository.get_contactc_info(notification.user_id)

            if not user_contact:
                raise UserNotFound("[PUBLISH SERVICE] User not found")
            
            if notification.channel == "email":
                destination = user_contact.email

            elif notification.channel == "sms":
                destination = user_contact.sms

            elif notification.channel == "push":
                destination = user_contact.push

            
            event = NotificationEvent(notification.user_id,
                                    notification.message,
                                    notification.channel,
                                    destination)

            success = self.event_bus.publish(event)
            if not success:
                logger.error(f" Failes dto publish notification")
                raise NotificationPublishError("Failed to publish event")
         
            logger.info("Notication published with successful.")
        except UserNotFound:
            raise
        except Exception as e:
            logger.exception(f"[PUBLISH SERVICE] Unexpected error while publish event:{e}")
            raise