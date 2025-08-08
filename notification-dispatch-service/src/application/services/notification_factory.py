from domain.entitites.notification import Notification
from domain.exceptions.invalid_notification_event import InvalidNotificationEvent
import logging

logger = logging.getLogger(__name__)
class NotificationFactory:


  def create_from_event(self,event:dict)-> Notification: 

        data = event.get("data")

        if not data:
            logger.error("Missing data key in event")
            raise InvalidNotificationEvent("Missing data key in event")

        
        return Notification(user_id=data.get("user_id"),
                            message=data.get("message"),
                            channel=data.get("channel"),
                            destination=data.get("destination"))
