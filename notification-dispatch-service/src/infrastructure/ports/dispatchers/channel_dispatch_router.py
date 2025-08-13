from typing import Dict
from src.domain.ports.dispatchers.channel_dispatcher import ChannelDispatcher
from src.domain.entitites.notification import Notification
from src.domain.exceptions.channel_dispatcher_error_exception import ChannelDispatchErrorException
import logging

logger = logging.getLogger(__name__)
class ChannelDispatchRouter(ChannelDispatcher):

    def __init__(self,dispatchers:Dict[str,ChannelDispatcher]):

        self.dispatchers = dispatchers

    async def dispatch(self,notification:Notification)->None:
        """
        Dispatch notification for a specific channel
        """
        logger.info(f"Dispatcher notification to specific channel")
       
        dispatch =  self.dispatchers.get(notification.channel)

        if not dispatch:
            raise ChannelDispatchErrorException(f"Channel does not supported:{notification.channel}")

        await dispatch.dispatch(notification)


