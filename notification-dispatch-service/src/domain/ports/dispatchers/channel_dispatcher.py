from abc import ABC,abstractmethod
from src.domain.entitites.notification import Notification
class ChannelDispatcher(ABC):
    
    @abstractmethod
    async def dispatch(self, notification: Notification) -> None:
        pass