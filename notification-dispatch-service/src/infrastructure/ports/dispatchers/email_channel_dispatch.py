from src.domain.ports.dispatchers.channel_dispatcher  import ChannelDispatcher
from src.domain.entitites.notification import Notification
import logging
import asyncio
logger = logging.getLogger(logging.INFO)

class EmailChannelDispatch(ChannelDispatcher):


    async def dispatch(self, notification:Notification) -> None:
        """
        Dispatch a notification to email channel
        """
        try:
            send_notification = {
                "message": notification.message,
                "destination":notification.destination
            }
            
            logger.info(f"Dispatching notification to {notification.channel} channel")
            logger.debug(f"Payload: {send_notification}")
            await asyncio.sleep(2) 
            logger.info(f"Notifcation sended to {notification.destination}")

        except Exception as e:
            logger.exception("[EMAICHANNELDISPATCH] An error occurred while send noticfication by email")

            raise
