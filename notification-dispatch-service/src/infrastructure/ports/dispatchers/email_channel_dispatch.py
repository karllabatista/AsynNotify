from src.domain.ports.dispatchers.channel_dispatcher  import ChannelDispatcher
from src.domain.entitites.notification import Notification
from src.domain.exceptions.email_channel_dispatch_error import EmailDispatcherException
from src.domain.ports.services.email_service import EmailService
import logging
import asyncio
logger = logging.getLogger(logging.INFO)

class EmailChannelDispatch(ChannelDispatcher):

    def __init__(self,service:EmailService):
        self.service = service


    async def dispatch(self, notification:Notification) -> None:
        """
        Dispatch a notification to email channel
        
        """
        try:
            
            content = self._create_content_email(notification)


            # logger.info(f"Dispatching notification to {notification.channel} channel")
            # logger.debug(f"Payload: {email_notification}")
            # await asyncio.sleep(2) 
            # logger.info(f"Notifcation sent to {notification.destination}")
            await self.service.send(content)

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
                "message": notification.message,
                "destination":notification.destination
                }
        return content

        