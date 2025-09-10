from app.domain.ports.event_bus import EventBus
from app.domain.exceptions.notification_publish_error import NotificationPublishError
from app.domain.events.notification_event import NotificationEvent
from app.domain.repositories.user_contact_info_repository import UserContactInfoRepository
from app.domain.exceptions.user_not_found_exception import UserNotFound
from app.factory.notification_factory import NotificationFactory
from app.interface.schemas.notification_input import NotificationInput
import logging


logger = logging.getLogger(__name__)

class PublishNotificationUseCase:

    def __init__(self,
                event_bus:EventBus,
                user_repository:UserContactInfoRepository):
        self.event_bus = event_bus
        self.user_repository = user_repository

    def execute(self,notification_input:NotificationInput) -> None:
        logger.info(f"Trying to publish notification ...")

        try:
            # TODO push notification
            user_contact =  self.user_repository.get_contact_info_by_user_id(notification_input.user_id)

            if not user_contact:
                raise UserNotFound("[PUBLISH SERVICE] User not found")

            destination = user_contact.email
           

        except UserNotFound:
            logger.debug("[PUBLISH SERVICE] user not found")
            raise   

        # create a notification with facotry
        notification = NotificationFactory.create(user_id=notification_input.user_id,
                                                  message=notification_input.message,
                                                  channel=notification_input.channel)


        # notification entity becomes event


        event = NotificationEvent(notification.user_id,
                                notification.message,
                                notification.channel,
                                destination
                                )
        
        try:
            self.event_bus.publish(event)
         
            logger.info("[PUBLISH SERVICE] Notication published with successful.")

        except Exception as e:
            logger.exception(f"[PUBLISH SERVICE] Unexpected error while publish event:{e}")
            raise NotificationPublishError("Failed to publish event") from e