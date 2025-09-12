from app.domain.entities.notification import Notification
from app.validators.notification_validator import NotificationValidator

class NotificationFactory:

   @staticmethod
   def create(user_id:str,message:str,channel:str) ->Notification:

        if not NotificationValidator.validate(user_id,message,channel):
            raise ValueError("Invalid data to Notification")

        return Notification(user_id=user_id,
                            message=message,
                            channel= channel)
