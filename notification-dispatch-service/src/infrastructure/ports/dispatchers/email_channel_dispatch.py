from src.domain.ports.dispatchers.channel_dispatcher  import ChannelDispatcher
from src.domain.entitites.notification import Notification
from src.domain.exceptions.email_channel_dispatch_error import EmailDispatcherException
from src.domain.ports.services.email_service import EmailService
import logging
import asyncio
logger = logging.getLogger(__name__)

class EmailChannelDispatch(ChannelDispatcher):

    def __init__(self,service:EmailService):
        self.service = service


    async def dispatch(self, notification:Notification) -> None:
        """
        Dispatch a notification to email channel
        
        """
        try:
            
            content = self._create_content_email(notification)
            self._validate_email_content(content)
            
            result = await self.service.send_to_provider(content)

            if result.get("status") == "sent":
                logger.info("[EMAILCHANNELDISPATCH]Email sent with success")
            else:
                logger.info("[EMAILCHANNELDISPATCH]Email sending failed")
        except EmailDispatcherException as email_error:
            logger.error("[EMAILCHANNELDISPATCH] Failed to dispatch notification", exc_info=email_error)
            raise
        except Exception as e:
            logger.exception("[EMAILCHANNELDISPATCH] An internal error occurred while dispatch noticfication by email")

            raise
    
    def _create_content_email(self,notification:Notification)->dict:
        if not notification.message or not notification.destination:
            raise ValueError("Notification must have message and destination")

        content = {
                "from":"no-reply@mysystem.com",
                "to": notification.destination,
                "subject":"New Notification",
                "text_body":notification.message,
                }
        return content

    
    def _validate_email_content(self,content):

        if "from" not in content or "to" not in content or \
           "subject" not in content or "text_body" not in content:

            raise ValueError("Mandatory field are missing")